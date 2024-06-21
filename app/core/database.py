import motor.motor_asyncio
from bson import ObjectId
from app.core.dateFunctions import DateFunctions
from pprint import pprint
import re
from typing import List, Dict, Any
from loguru import logger

logger.add("logs/database.log", colorize=True, backtrace=True, diagnose=True, format="{time} {level} {message}",
           rotation="1 MB", level="INFO")


class Database:
    database_name = 'dreamsmanager'
    client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27011/")

    @staticmethod
    async def connection():
        return Database.client

    @staticmethod
    async def is_live():
        try:
            client = await Database.connection()
            if client:
                await client.admin.command('ping')
                return True
        except Exception as e:
            logger.error(f"Database is not running, Error in database is_live with message: {e}")
        return False

    @staticmethod
    async def create_collection_if_not_exists(collection: str):
        try:
            client = await Database.connection()
            database = client[Database.database_name]
            if collection not in await database.list_collection_names():
                await database.create_collection(collection)
            return True
        except Exception as e:
            logger.error(f"Error in create_collection_if_not_exists: {e}")
            return False

    @staticmethod
    async def create_collection_object(collection: str):
        try:
            await Database.create_collection_if_not_exists(collection)
            client = await Database.connection()
            database = client[Database.database_name]
            return database[collection]
        except Exception as e:
            logger.error(f"Error in create_collection_object: {e}")
            return None

    @staticmethod
    async def format_item_to_be_returned(item):
        try:
            if item:
                item = dict(item)
                item["_id"] = str(item["_id"])
                item['time_elapsed'] = await DateFunctions.time_elapsed(item['date_created']['timestamp'])
                return item
            return item
        except Exception as e:
            logger.error(f"Error in format_item_to_be_returned: {e}")
        return False

    @staticmethod
    async def fetch_one_item_by_id(collection: str, object_id: str):
        try:
            return await Database.fetch_one_item(collection, [{'_id': ObjectId(object_id)}])
        except Exception as e:
            logger.error(f"Error in fetch_one_item_by_id: {e}")
            return False

    @staticmethod
    async def fetch_one_item_by_integer_id(collection: str, id: int):
        try:
            return await Database.fetch_one_item(collection, [{'id': int(id)}])
        except Exception as e:
            logger.error(f"Error in fetch_one_item_by_id: {e}")
            return False

    @staticmethod
    async def fetch_one_item(collection: str, query_list_of_dictionaries: list = None):
        try:
            collection = await Database.create_collection_object(collection)
            if collection is None:
                return False
            query = {"$or": query_list_of_dictionaries} if query_list_of_dictionaries else {}
            item = await collection.find(query).sort("id", -1).limit(1).to_list(1)
            return await Database.format_item_to_be_returned(item[0]) if item else None
        except Exception as e:
            logger.error(f"Error in fetch_one_item: {e}")
            return False

    @staticmethod
    async def fetch_many_items(collection: str, query_list_of_dictionaries: list = None, and_query: bool = False,
                               exclude_list_of_dictionaries: list = None, limit: int = None):
        try:
            collection = await Database.create_collection_object(collection)
            if collection is None:
                return []
            query = {}
            if query_list_of_dictionaries:
                query["$and" if and_query else "$or"] = query_list_of_dictionaries
            if exclude_list_of_dictionaries:
                query["$nor"] = exclude_list_of_dictionaries
            cursor = collection.find(query).sort("id", -1)
            if limit:
                cursor = cursor.limit(limit)
            items = [await Database.format_item_to_be_returned(item) for item in await cursor.to_list(None)]
            return items
        except Exception as e:
            logger.error(f"Error in fetch_many_items: {e}")
            return []

    @staticmethod
    async def insert_one_item(collection: str, item: dict):
        try:
            collection = await Database.create_collection_object(collection)
            if collection is None:
                return False
            next_id = await Database.get_next_sequence(collection.name)
            item['id'] = next_id
            return await Database._insert_item(collection, item)
        except Exception as e:
            logger.error(f"Error in insert_one_item: {e}")
            return False

    @staticmethod
    async def get_next_sequence(collection_name):
        try:
            counter_collection = await Database.create_collection_object('counters')
            result = await counter_collection.find_one_and_update(
                {'_id': collection_name},
                {'$inc': {'seq': 1}},
                return_document=True,
                upsert=True
            )
            return result['seq']
        except Exception as e:
            logger.error(f"Error in get_next_sequence: {e}")
            return None

    @staticmethod
    async def _insert_item(collection, item):
        try:
            if 'manual_date_created' in item and item['manual_date_created']:
                date_created = item.pop('manual_date_created')
                item['date_created'] = date_created
                item = await DateFunctions.add_payback_timestamp(item, date_created, 'date_created')
            else:
                item = await DateFunctions.add_current_timestamp(item)
            result = await collection.insert_one(item)
            return result.inserted_id if result.inserted_id else False
        except Exception as e:
            logger.error(f"Error in _insert_item: {e}")
            return False

    @staticmethod
    async def update_one_item(collection: str, item: dict, id_column: str, id_value, id_is_integer=False):
        try:
            collection = await Database.create_collection_object(collection)
            if collection is None:
                return False
            myquery = {id_column: int(id_value) if id_is_integer else id_value}
            item = await DateFunctions.add_last_updated_timestamp(item)
            update_query = {"$set": {key: value for key, value in item.items() if key != 'id'}}
            result = await collection.update_one(myquery, update_query)
            return True if result else False
        except Exception as e:
            logger.error(f"Error in update_one_item: {e}")
            return False

    @staticmethod
    async def delete_one_item_by_id(collection: str, id_value):
        try:
            collection = await Database.create_collection_object(collection)
            if collection is None:
                return False
            object_id = ObjectId(id_value)
            myquery = {'_id': object_id}
            result = await collection.delete_one(myquery)
            return True if result.deleted_count > 0 else False
        except Exception as e:
            logger.error(f"Error in delete_one_item_by_id: {e}")
            return False

    @staticmethod
    async def fetch_many_items_paginated(collection: str, page_number: int, page_size: int,
                                         query_list_of_dictionaries: list = None,
                                         exclude_list_of_dictionaries: list = None):
        try:
            collection = await Database.create_collection_object(collection)
            if collection is None:
                return []
            skip = (page_number - 1) * page_size
            query = {"$or": query_list_of_dictionaries} if query_list_of_dictionaries else {}
            if exclude_list_of_dictionaries:
                query["$nor"] = exclude_list_of_dictionaries
            items = [await Database.format_item_to_be_returned(item) for item in
                     await collection.find(query).sort("id", -1).skip(skip).limit(page_size).to_list(None)]
            return items
        except Exception as e:
            logger.error(f"Error in fetch_many_items_paginated: {e}")
            return []

    @staticmethod
    async def count_items(collection: str, query_list_of_dictionaries: list = None,
                          exclude_list_of_dictionaries: list = None, ):
        try:
            collection = await Database.create_collection_object(collection)
            if collection is None:
                return 0
            query = {"$or": query_list_of_dictionaries} if query_list_of_dictionaries else {}
            if exclude_list_of_dictionaries:
                query["$nor"] = exclude_list_of_dictionaries
            total_count = await collection.count_documents(query)
            return max(total_count, 0)
        except Exception as e:
            logger.error(f"Error in count_items: {e}")
            return 0

    @staticmethod
    async def search_by_column(collection: str, column_name: str, search_text: str):
        try:
            collection = await Database.create_collection_object(collection)
            if collection is None:
                return []
            regex_pattern = re.compile(f'.*{re.escape(search_text)}.*', re.IGNORECASE)
            query = {column_name: {'$regex': regex_pattern}}
            items = [await Database.format_item_to_be_returned(item) for item in
                     await collection.find(query).sort("id", -1).to_list(None)]
            return items
        except Exception as e:
            logger.error(f"Error in search_by_column: {e}")
            return []
