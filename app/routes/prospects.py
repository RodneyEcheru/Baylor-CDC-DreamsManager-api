from fastapi import APIRouter, Request
from loguru import logger
from app.core.form import Form
from app.core.form_validation import FormValidation
from app.core.database import Database
from app.core.pagination import Pagination
from app.core.generic import Generic
from app.routes.users import User
from app.routes.stages import StageService
from app.routes.products import ProductService

logger.add("logs/prospects.log", colorize=True, backtrace=True, diagnose=True, format="{time} {level} {message}",
           rotation="1 MB", level="INFO")

router = APIRouter(prefix="/prospects")


class ProspectService:
    collection_name = 'prospect'

    @staticmethod
    async def check_existing_prospect(field, value):
        prospect = await Database.fetch_one_item(ProspectService.collection_name, [{field: value}])
        if prospect:
            return await Form.return_response(
                True,
                'Prospect already exists',
                f"A prospect with this {field} already exists",
                'error',
                'danger'
            )
        return None

    @staticmethod
    async def add(request: Request):
        try:
            form_data = await Form.extract_form_input(request)
            validation_message = await FormValidation.require_inputs(form_data,
                                                                     ['name', 'user_id', 'stage_id', 'product_id'])
            if validation_message != 'valid_inputs':
                return validation_message

            # check if prospect already exists
            fields_to_check = ['name', 'email', 'phone']
            for field in fields_to_check:
                response = await ProspectService.check_existing_prospect(field, form_data[field])
                if response:
                    return response

            form_data['status'] = 'active'
            await Database.insert_one_item(ProspectService.collection_name, form_data)

            return await Form.return_response(
                False,
                'Success',
                f"{form_data['name']} has been registered",
                'success',
                'success',
                response_action='reload_page'
            )
        except Exception as e:
            logger.error(f"Failed to create prospect: {e}")
            return await Form.return_response(
                True,
                'Failed to create prospect',
                str(e),
                'error',
                'danger'
            )

    @staticmethod
    async def paginated_report(page_number: int, page_size: int):
        try:
            table_title = "Prospects"
            table_columns = ['Name', 'Product', 'Stage', 'Registered by', 'Time']
            table_values = []

            prospects = await Pagination.paginated_results(
                page_number,
                page_size,
                ProspectService.collection_name,
                '/dashboard/admin/prospects/report'
            )

            users = await User.all_users()
            products = await ProductService.all_products()
            stages = await StageService.all_stages()

            for prospect in prospects.get('results', []):
                prospect['agent'] = next(
                    (user['fullname'] for user in users if int(user['id']) == int(prospect['user_id'])), 'Error')
                prospect['stage'] = next(
                    (stage['name'] for stage in stages if int(stage['id']) == int(prospect['stage_id'])), 'Error')
                prospect['product'] = next(
                    (product['name'] for product in products if int(product['id']) == int(prospect['product_id'])),
                    'Error')

                if prospect:
                    table_values.append([
                        prospect.get('name', '---'),
                        prospect.get('product', '---'),
                        prospect.get('stage', '---'),
                        prospect.get('agent', '---'),
                        prospect.get('time_elapsed', '---')
                    ])

            total_prospects = format(prospects.get('total_count', 0), ',')
            sub_title = "Prospects registered from field"

            cards = [{
                'title': 'Total number of prospects',
                'content': total_prospects,
            }]

            datatable = {
                'title': table_title,
                'sub_title': sub_title,
                'columns': table_columns,
                'values': table_values,
                'cards': cards,
                'pagination_details': prospects.get('pagination_details')
            }

            return await Form.return_response(
                False,
                'Success',
                "Prospects retrieved successfully",
                'success',
                'success',
                server_data=datatable
            )
        except Exception as e:
            logger.error(f"Failed to fetch prospects: {e}")
            return await Form.return_response(
                True,
                'Failed to fetch prospects',
                str(e),
                'error',
                'danger'
            )

    @staticmethod
    async def prospects_select_array():
        try:
            prospects = await ProspectService.all_prospects()
            select_array = await Generic.create_select_array(prospects, 'id', 'name')

            return await Form.return_response(
                False,
                'Success',
                "Prospects array retrieved successfully",
                'success',
                'success',
                server_data=select_array
            )
        except Exception as e:
            logger.error(f"Failed to fetch prospects: {e}")
            return await Form.return_response(
                True,
                'Failed to fetch prospects',
                str(e),
                'error',
                'danger'
            )

    @staticmethod
    async def all_prospects():
        try:
            prospects = await Database.fetch_many_items(ProspectService.collection_name)

            categories = await CategoryService.all_categories()

            for prospect in prospects:
                prospect['category'] = next((category['name'] for category in categories if
                                             int(category['id']) == int(prospect['category_id'])), 'Error')

            return prospects

        except Exception as e:
            logger.error(f"Failed to fetch prospects: {e}")
            return await Form.return_response(
                True,
                'Failed to fetch prospects',
                str(e),
                'error',
                'danger'
            )

    @staticmethod
    async def count():
        try:
            return await Database.count_items(ProspectService.collection_name)
        except Exception as e:
            logger.error(f"Failed to fetch prospects count: {e}")
            return await Form.return_response(
                True,
                'Failed to fetch prospects',
                str(e),
                'error',
                'danger'
            )

    @staticmethod
    async def latest_prospects(limit: int):
        try:
            users = await User.all_users()
            prospects = await Database.fetch_many_items(ProspectService.collection_name, limit=limit)

            for prospect in prospects:
                prospect['agent'] = next(
                    (user['fullname'] for user in users if int(user['id']) == int(prospect['user_id'])), 'Error')

            return prospects

        except Exception as e:
            logger.error(f"Failed to fetch prospects: {e}")
            return await Form.return_response(
                True,
                'Failed to fetch prospects',
                str(e),
                'error',
                'danger'
            )


# Routes
@router.post('/add')
async def add_prospect(request: Request):
    return await ProspectService.add(request)


@router.get('/paginated_report/{page_number}/{page_size}')
async def get_paginated_report(page_number: int, page_size: int):
    return await ProspectService.paginated_report(page_number, page_size)


@router.get('/latest/{limit}')
async def get_latest_prospects(limit: int):
    return await ProspectService.latest_prospects(int(limit))


@router.get('/count')
async def count():
    return await ProspectService.count()


@router.get('/prospects_select_array')
async def get_prospects_select_array():
    return await ProspectService.prospects_select_array()
