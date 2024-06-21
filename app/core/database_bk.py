import pymongo
from bson import ObjectId  # Import ObjectId from bson module
from app.core.dateFunctions import DateFunctions
from pprint import pprint
import re


class Database:
    database_name = 'memo'

    @staticmethod
    # check if database is live
    async def connection():
        return pymongo.MongoClient("mongodb://localhost:27011/")

    @staticmethod
    async def is_live():
        try:
            client = await Database.connection()
            if client:
                client.close()
                return True
            else:
                return False
        except Exception as e:
            return False

    @staticmethod
    async def create_collection_if_not_exists(collection: str):
        try:
            client = await Database.connection()
            database = client[Database.database_name]
            if collection in database.list_collection_names():
                return True
            else:
                await database.create_collection(collection)
                return True
        except Exception as e:
            return False

    @staticmethod
    async def create_collection_object(collection: str):
        try:
            client = await Database.connection()
            database = client[Database.database_name]
            collection_created = await Database.create_collection_if_not_exists(collection)
            if collection_created:
                return database[collection]
            else:
                return False
        except Exception as e:
            return False

    @staticmethod
    async def format_item_to_be_returned(item):
        try:
            if item:
                item = dict(item)
                item["_id"] = str(item["_id"])
                item['time_elapsed'] = await DateFunctions.time_elapsed(item['date_created']['timestamp'])
                return item
            else:
                return False
        except Exception as e:
            return False

    @staticmethod
    async def fetch_one_item_by_id(collection: str, object_id: str):
        collection = await Database.create_collection_object(collection)
        object_id = ObjectId(object_id)
        if isinstance(collection, bool):
            return False
        else:
            return await Database.format_item_to_be_returned(collection.find_one({'_id': object_id}))

    @staticmethod
    async def fetch_one_item(collection: str, query_list_of_dictionaries: list = False):
        collection = await Database.create_collection_object(collection)
        if query_list_of_dictionaries:
            query = {"$or": query_list_of_dictionaries}
            if isinstance(collection, bool):
                return False
            else:
                return await Database.format_item_to_be_returned(collection.find_one(query))
        else:
            if isinstance(collection, bool):
                return False
            else:
                return await Database.format_item_to_be_returned(collection.find_one())

    @staticmethod
    async def fetch_many_items(collection: str, query_list_of_dictionaries: list = False):
        try:
            collection = await Database.create_collection_object(collection)
            if query_list_of_dictionaries:
                query = {"$or": query_list_of_dictionaries}
                items = [await Database.format_item_to_be_returned(item) for item in collection.find(query)][::-1]
            else:
                items = [await Database.format_item_to_be_returned(item) for item in collection.find()][::-1]
            return items
        except Exception as e:
            return []

    @staticmethod
    async def fetch_many_items_and(collection: str, query_list_of_dictionaries: list = False):
        try:
            collection = await Database.create_collection_object(collection)
            if query_list_of_dictionaries:
                query = {"$and": query_list_of_dictionaries}
                items = [await Database.format_item_to_be_returned(item) for item in collection.find(query)][::-1]
            else:
                items = [await Database.format_item_to_be_returned(item) for item in collection.find()][::-1]
            return items
        except Exception as e:
            return []

    @staticmethod
    async def fetch_many_items_and_excluding(collection: str, query_list_of_dictionaries: list = False, exclude_list_of_dictionaries: list = False):
        try:
            collection = await Database.create_collection_object(collection)
            query = {}
            if query_list_of_dictionaries:
                query = {"$and": query_list_of_dictionaries}
            if exclude_list_of_dictionaries:
                exclude_query = {"$nor": exclude_list_of_dictionaries}
                query = {**query, **exclude_query}
            items = [await Database.format_item_to_be_returned(item) for item in collection.find(query)][::-1]
            return items
        except Exception as e:
            return []

    @staticmethod
    async def insert_one_item(collection: str, item: dict):
        try:
            collection_created = await Database.create_collection_if_not_exists(collection)
            if collection_created:
                return await Database._insert_item(collection, item)
            else:
                collection_created = await Database.create_collection_if_not_exists(collection)
                if collection_created:
                    return await Database._insert_item(collection, item)
        except Exception as e:
            return False

    @staticmethod
    async def _insert_item(collection, item):
        try:
            collection = await Database.create_collection_object(collection)
            if 'manual_date_created' in item and item['manual_date_created']:
                date_created = item['manual_date_created']
                del item['manual_date_created']
                item['date_created'] = date_created
                item = await DateFunctions.add_payback_timestamp(item, item['date_created'], 'date_created')
            else:
                item = await DateFunctions.add_current_timestamp(item)
            result = collection.insert_one(item)
            inserted_item_id = result.inserted_id
            return inserted_item_id if inserted_item_id else False
        except Exception as e:
            return False

    @staticmethod
    async def update_one_item(collection: str, item: dict, id_column: str, id_value):
        try:
            collection_created = await Database.create_collection_if_not_exists(collection)
            if collection_created:
                collection = await Database.create_collection_object(collection)
                myquery = {id_column: id_value}
                item = await DateFunctions.add_last_updated_timestamp(item)
                update_query = {"$set": {key: value for key, value in item.items() if key != '_id'}}
                result = collection.update_one(myquery, update_query)
                return True if result else False
            else:
                return False
        except Exception as e:
            return False

    @staticmethod
    async def update_one_item_by_id(collection: str, item: dict, id_value):
        try:
            collection_created = await Database.create_collection_if_not_exists(collection)
            if collection_created:
                collection = await Database.create_collection_object(collection)
                object_id = ObjectId(id_value)
                myquery = {'_id': object_id}
                item = await DateFunctions.add_last_updated_timestamp(item)
                update_query = {"$set": {key: value for key, value in item.items() if key != '_id'}}
                result = collection.update_one(myquery, update_query)
                return True if result else False
            else:
                return False
        except Exception as e:
            return False

    @staticmethod
    async def delete_one_item_by_id(collection: str, id_value):
        try:
            collection_created = await Database.create_collection_if_not_exists(collection)
            if collection_created:
                collection = await Database.create_collection_object(collection)
                object_id = ObjectId(id_value)
                myquery = {'_id': object_id}
                result = collection.delete_one(myquery)
                return True if result.deleted_count > 0 else False
            else:
                return False
        except Exception as e:
            return False

    @staticmethod
    async def fetch_many_items_paginated(collection: str, page_number: int, page_size: int, query_list_of_dictionaries: list | bool = False):
        try:
            collection = await Database.create_collection_object(collection)
            skip = (page_number - 1) * page_size
            if query_list_of_dictionaries:
                query = {"$or": query_list_of_dictionaries}
                items = [await Database.format_item_to_be_returned(item) for item in collection.find(query).skip(skip).limit(page_size)][::-1]
            else:
                items = [await Database.format_item_to_be_returned(item) for item in collection.find().skip(skip).limit(page_size)][::-1]
            return items
        except Exception as e:
            return []

    @staticmethod
    async def count_items(collection: str, query_list_of_dictionaries: list | bool = False):
        try:
            collection = await Database.create_collection_object(collection)
            if query_list_of_dictionaries:
                query = {"$or": query_list_of_dictionaries}
                total_count = collection.count_documents(query)
            else:
                total_count = collection.count_documents({})
            return max(total_count, 0)
        except Exception as e:
            return 0

    @staticmethod
    async def search_by_column(collection: str, column_name: str, search_text: str):
        try:
            collection = await Database.create_collection_object(collection)
            regex_pattern = re.compile(f'.*{re.escape(search_text)}.*', re.IGNORECASE)
            query = {column_name: {'$regex': regex_pattern}}
            items = [await Database.format_item_to_be_returned(item) for item in collection.find(query)][::-1]
            return items
        except Exception as e:
            return []

    @staticmethod
    async def fetch_latest_items(collection: str, limit: int, query_list_of_dictionaries: list = None):
        try:
            collection = await Database.create_collection_object(collection)
            if query_list_of_dictionaries:
                query = {"$and": query_list_of_dictionaries}
                cursor = collection.find(query).sort("timestamp", pymongo.DESCENDING).limit(limit)
            else:
                cursor = collection.find().sort("timestamp", pymongo.DESCENDING).limit(limit)
            items = [await Database.format_item_to_be_returned(item) for item in cursor]
            return items
        except Exception as e:
            return []

# Example usage:
# latest_items = await Database.fetch_latest_items('your_collection_name', 4)
