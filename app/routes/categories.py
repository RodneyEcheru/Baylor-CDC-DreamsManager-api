from fastapi import APIRouter, Request
from loguru import logger
from app.core.form import Form
from app.core.form_validation import FormValidation
from app.core.database import Database
from app.core.pagination import Pagination
from app.core.generic import Generic
from app.routes.users import User

logger.add("logs/categories.log", colorize=True, backtrace=True, diagnose=True, format="{time} {level} {message}",
           rotation="1 MB", level="INFO")

router = APIRouter(prefix="/categories")


class CategoryService:
    collection_name = 'category'

    @staticmethod
    async def add(request: Request):
        try:
            form_data = await Form.extract_form_input(request)
            validation_message = await FormValidation.require_inputs(form_data, ['name', 'user_id'])
            if validation_message != 'valid_inputs':
                return validation_message

            category = await Database.fetch_one_item(CategoryService.collection_name, [{'name': form_data['name']}])
            if category:
                return await Form.return_response(
                    True,
                    'Category already exists',
                    "This category is already registered",
                    'error',
                    'danger'
                )

            form_data['status'] = 'active'
            await Database.insert_one_item(CategoryService.collection_name, form_data)

            return await Form.return_response(
                False,
                'Success',
                f"{form_data['name']} has been registered",
                'success',
                'success',
                response_action='reload_page'
            )
        except Exception as e:
            logger.error(f"Failed to create category: {e}")
            return await Form.return_response(
                True,
                'Failed to create category',
                str(e),
                'error',
                'danger'
            )

    @staticmethod
    async def paginated_report(page_number: int, page_size: int):
        try:
            table_title = "Product Categories"
            table_columns = ['Name', 'Registered by', 'Time']
            table_values = []

            categories = await Pagination.paginated_results(
                page_number,
                page_size,
                CategoryService.collection_name,
                '/dashboard/admin/categories/report'
            )

            users = await User.all_users()

            for category in categories.get('results', []):
                category['agent'] = next((user['fullname'] for user in users if int(user['id']) == int(category['user_id'])), 'Error')

                if category:
                    table_values.append([
                        category.get('name', '---'),
                        category.get('agent', '---'),
                        category.get('time_elapsed', '---')
                    ])

            total_categories = format(categories.get('total_count', 0), ',')
            sub_title = "Categories registered from field"

            cards = [{
                'title': 'Total number of categories',
                'content': total_categories,
            }]

            datatable = {
                'title': table_title,
                'sub_title': sub_title,
                'columns': table_columns,
                'values': table_values,
                'cards': cards,
                'pagination_details': categories.get('pagination_details')
            }

            return await Form.return_response(
                False,
                'Success',
                "Categories retrieved successfully",
                'success',
                'success',
                server_data=datatable
            )
        except Exception as e:
            logger.error(f"Failed to fetch category: {e}")
            return await Form.return_response(
                True,
                'Failed to fetch category',
                str(e),
                'error',
                'danger'
            )

    @staticmethod
    async def select_array():
        try:
            categories = await CategoryService.all_categories()
            select_array = await Generic.create_select_array(categories, 'id', 'name')

            return await Form.return_response(
                False,
                'Success',
                "Categories array retrieved successfully",
                'success',
                'success',
                server_data=select_array
            )
        except Exception as e:
            logger.error(f"Failed to fetch categories: {e}")
            return await Form.return_response(
                True,
                'Failed to fetch categories',
                str(e),
                'error',
                'danger'
            )

    @staticmethod
    async def all_categories():
        try:
            return await Database.fetch_many_items(CategoryService.collection_name)
        except Exception as e:
            logger.error(f"Failed to fetch categories: {e}")
            return await Form.return_response(
                True,
                'Failed to fetch categories',
                str(e),
                'error',
                'danger'
            )

    @staticmethod
    async def count():
        try:
            return await Database.count_items(CategoryService.collection_name)
        except Exception as e:
            logger.error(f"Failed to fetch categories count: {e}")
            return await Form.return_response(
                True,
                'Failed to fetch categories',
                str(e),
                'error',
                'danger'
            )

    @staticmethod
    async def latest_categories(limit: int):
        try:
            return await Database.fetch_many_items(CategoryService.collection_name, limit=limit)
        except Exception as e:
            logger.error(f"Failed to fetch categories: {e}")
            return await Form.return_response(
                True,
                'Failed to fetch categories',
                str(e),
                'error',
                'danger'
            )


# Routes
@router.post('/add')
async def add_category(request: Request):
    return await CategoryService.add(request)


@router.get('/paginated_report/{page_number}/{page_size}')
async def get_paginated_report(page_number: int, page_size: int):
    return await CategoryService.paginated_report(page_number, page_size)


@router.get('/latest/{limit}')
async def get_paginated_report(limit: int):
    return await CategoryService.latest_categories(int(limit))


@router.get('/count')
async def count():
    return await CategoryService.count()


@router.get('/select_array')
async def get_categories_select_array():
    return await CategoryService.select_array()
