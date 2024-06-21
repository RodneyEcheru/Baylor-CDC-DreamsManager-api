from fastapi import APIRouter, Request
from loguru import logger
from app.core.form import Form
from app.core.form_validation import FormValidation
from app.core.database import Database
from app.core.pagination import Pagination
from app.core.generic import Generic
from app.routes.users import User
from app.routes.categories import CategoryService

logger.add("logs/products.log", colorize=True, backtrace=True, diagnose=True, format="{time} {level} {message}",
           rotation="1 MB", level="INFO")

router = APIRouter(prefix="/products")


class ProductService:
    collection_name = 'product'

    @staticmethod
    async def add(request: Request):
        try:
            form_data = await Form.extract_form_input(request)
            validation_message = await FormValidation.require_inputs(form_data, ['name', 'user_id', 'category_id'])
            if validation_message != 'valid_inputs':
                return validation_message

            product = await Database.fetch_one_item(ProductService.collection_name, [{'name': form_data['name']}])
            if product:
                return await Form.return_response(
                    True,
                    'Product already exists',
                    "This product is already registered",
                    'error',
                    'danger'
                )

            form_data['status'] = 'active'
            await Database.insert_one_item(ProductService.collection_name, form_data)

            return await Form.return_response(
                False,
                'Success',
                f"{form_data['name']} has been registered",
                'success',
                'success',
                response_action='reload_page'
            )
        except Exception as e:
            logger.error(f"Failed to create product: {e}")
            return await Form.return_response(
                True,
                'Failed to create product',
                str(e),
                'error',
                'danger'
            )

    @staticmethod
    async def paginated_report(page_number: int, page_size: int):
        try:
            table_title = "Products"
            table_columns = ['Name', 'Category', 'Registered by', 'Time']
            table_values = []

            products = await Pagination.paginated_results(
                page_number,
                page_size,
                ProductService.collection_name,
                '/dashboard/admin/products/report'
            )

            users = await User.all_users()
            categories = await CategoryService.all_categories()

            for product in products.get('results', []):
                product['agent'] = next((user['fullname'] for user in users if int(user['id']) == int(product['user_id'])), 'Error')
                product['category'] = next((category['name'] for category in categories if int(category['id']) == int(product['category_id'])), 'Error')

                if product:
                    table_values.append([
                        product.get('name', '---'),
                        product.get('category', '---'),
                        product.get('agent', '---'),
                        product.get('time_elapsed', '---')
                    ])

            total_products = format(products.get('total_count', 0), ',')
            sub_title = "Products registered from field"

            cards = [{
                'title': 'Total number of products',
                'content': total_products,
            }]

            datatable = {
                'title': table_title,
                'sub_title': sub_title,
                'columns': table_columns,
                'values': table_values,
                'cards': cards,
                'pagination_details': products.get('pagination_details')
            }

            return await Form.return_response(
                False,
                'Success',
                "Products retrieved successfully",
                'success',
                'success',
                server_data=datatable
            )
        except Exception as e:
            logger.error(f"Failed to fetch product: {e}")
            return await Form.return_response(
                True,
                'Failed to fetch product',
                str(e),
                'error',
                'danger'
            )

    @staticmethod
    async def products_select_array():
        try:
            products = await ProductService.all_products()
            select_array = await Generic.create_select_array(products, 'id', 'name')

            return await Form.return_response(
                False,
                'Success',
                "Products array retrieved successfully",
                'success',
                'success',
                server_data=select_array
            )
        except Exception as e:
            logger.error(f"Failed to fetch products: {e}")
            return await Form.return_response(
                True,
                'Failed to fetch products',
                str(e),
                'error',
                'danger'
            )

    @staticmethod
    async def all_products():
        try:
            products = await Database.fetch_many_items(ProductService.collection_name)

            categories = await CategoryService.all_categories()

            for product in products:
                product['category'] = next((category['name'] for category in categories if int(category['id']) == int(product['category_id'])), 'Error')

            return products

        except Exception as e:
            logger.error(f"Failed to fetch products: {e}")
            return await Form.return_response(
                True,
                'Failed to fetch products',
                str(e),
                'error',
                'danger'
            )

    @staticmethod
    async def count():
        try:
            return await Database.count_items(ProductService.collection_name)
        except Exception as e:
            logger.error(f"Failed to fetch products count: {e}")
            return await Form.return_response(
                True,
                'Failed to fetch products',
                str(e),
                'error',
                'danger'
            )

    @staticmethod
    async def latest_products(limit: int):
        try:
            categories = await CategoryService.all_categories()
            products = await Database.fetch_many_items(ProductService.collection_name, limit=limit)

            for product in products:
                product['category'] = next((category['name'] for category in categories if int(category['id']) == int(product['category_id'])), 'Error')

            return products

        except Exception as e:
            logger.error(f"Failed to fetch products: {e}")
            return await Form.return_response(
                True,
                'Failed to fetch products',
                str(e),
                'error',
                'danger'
            )


# Routes
@router.post('/add')
async def add_product(request: Request):
    return await ProductService.add(request)


@router.get('/paginated_report/{page_number}/{page_size}')
async def get_paginated_report(page_number: int, page_size: int):
    return await ProductService.paginated_report(page_number, page_size)


@router.get('/latest/{limit}')
async def get_latest_products(limit: int):
    return await ProductService.latest_products(int(limit))


@router.get('/count')
async def count():
    return await ProductService.count()


@router.get('/products_select_array')
async def get_products_select_array():
    return await ProductService.products_select_array()
