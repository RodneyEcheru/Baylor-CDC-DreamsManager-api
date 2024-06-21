from fastapi import APIRouter, Request
from loguru import logger
from app.core.form import Form
from app.core.form_validation import FormValidation
from app.core.database import Database
from app.core.pagination import Pagination
from app.core.generic import Generic
from app.routes.users import User

logger.add("logs/materials.log", colorize=True, backtrace=True, diagnose=True, format="{time} {level} {message}",
           rotation="1 MB", level="INFO")

router = APIRouter(prefix="/materials")


class MaterialService:
    collection_name = 'material'

    @staticmethod
    async def check_existing_material(field, value):
        material = await Database.fetch_one_item(MaterialService.collection_name, [{field: value}])
        if material:
            return await Form.return_response(
                True,
                'Material already exists',
                f"A material with this {field} already exists",
                'error',
                'danger'
            )
        return None

    @staticmethod
    async def add(request: Request):
        try:
            form_data = await Form.extract_form_input(request)
            validation_message = await FormValidation.require_inputs(form_data,
                                                                     ['title', 'material_type', 'target_audience',
                                                                      'material_format'])
            if validation_message != 'valid_inputs':
                return validation_message

            # check if material already exists
            fields_to_check = ['title', 'publication_date', 'url']
            for field in fields_to_check:
                response = await MaterialService.check_existing_material(field, form_data.get(field, ''))
                if response:
                    return response

            await Database.insert_one_item(MaterialService.collection_name, form_data)

            return await Form.return_response(
                False,
                'Success',
                f"Material '{form_data['title']}' has been registered",
                'success',
                'success',
                response_action='reload_page'
            )
        except Exception as e:
            logger.error(f"Failed to create material: {e}")
            return await Form.return_response(
                True,
                'Failed to create material',
                str(e),
                'error',
                'danger'
            )

    @staticmethod
    async def paginated_report(page_number: int, page_size: int):
        try:
            table_title = "Materials"
            table_columns = ['Title', 'Type', 'Format', 'Audience', 'Registered by', 'Time']
            table_values = []

            materials = await Pagination.paginated_results(
                page_number,
                page_size,
                MaterialService.collection_name,
                '/dashboard/admin/materials/report'
            )

            users = await User.all_users()

            for material in materials.get('results', []):
                material['agent'] = next(
                    (user['fullname'] for user in users if int(user['id']) == int(material['user_id'])), 'Error')

                if material:
                    table_values.append([
                        material.get('title', '---'),
                        material.get('material_type', '---'),
                        material.get('material_format', '---'),
                        material.get('target_audience', '---'),
                        material.get('agent', '---'),
                        material.get('time_elapsed', '---')
                    ])

            total_materials = format(materials.get('total_count', 0), ',')
            sub_title = "Materials registered"

            cards = [{
                'title': 'Total number of materials',
                'content': total_materials,
            }]

            datatable = {
                'title': table_title,
                'sub_title': sub_title,
                'columns': table_columns,
                'values': table_values,
                'cards': cards,
                'pagination_details': materials.get('pagination_details')
            }

            return await Form.return_response(
                False,
                'Success',
                "Materials retrieved successfully",
                'success',
                'success',
                server_data=datatable
            )
        except Exception as e:
            logger.error(f"Failed to fetch materials: {e}")
            return await Form.return_response(
                True,
                'Failed to fetch materials',
                str(e),
                'error',
                'danger'
            )

    @staticmethod
    async def materials_select_array():
        try:
            materials = await MaterialService.all_materials()
            select_array = await Generic.create_select_array(materials, 'id', 'title')

            return await Form.return_response(
                False,
                'Success',
                "Materials array retrieved successfully",
                'success',
                'success',
                server_data=select_array
            )
        except Exception as e:
            logger.error(f"Failed to fetch materials: {e}")
            return await Form.return_response(
                True,
                'Failed to fetch materials',
                str(e),
                'error',
                'danger'
            )

    @staticmethod
    async def all_materials():
        try:
            materials = await Database.fetch_many_items(MaterialService.collection_name)

            return materials

        except Exception as e:
            logger.error(f"Failed to fetch materials: {e}")
            return await Form.return_response(
                True,
                'Failed to fetch materials',
                str(e),
                'error',
                'danger'
            )

    @staticmethod
    async def count():
        try:
            return await Database.count_items(MaterialService.collection_name)
        except Exception as e:
            logger.error(f"Failed to fetch materials count: {e}")
            return await Form.return_response(
                True,
                'Failed to fetch materials count',
                str(e),
                'error',
                'danger'
            )

    @staticmethod
    async def latest_materials(limit: int):
        try:
            users = await User.all_users()
            materials = await Database.fetch_many_items(MaterialService.collection_name, limit=limit)

            for material in materials:
                material['agent'] = next(
                    (user['fullname'] for user in users if int(user['id']) == int(material['user_id'])), 'Error')

            return materials

        except Exception as e:
            logger.error(f"Failed to fetch materials: {e}")
            return await Form.return_response(
                True,
                'Failed to fetch materials',
                str(e),
                'error',
                'danger'
            )


# Routes
@router.post('/add')
async def add_material(request: Request):
    return await MaterialService.add(request)


@router.get('/paginated_report/{page_number}/{page_size}')
async def get_paginated_report(page_number: int, page_size: int):
    return await MaterialService.paginated_report(page_number, page_size)


@router.get('/latest/{limit}')
async def get_latest_materials(limit: int):
    return await MaterialService.latest_materials(int(limit))


@router.get('/count')
async def count():
    return await MaterialService.count()


@router.get('/materials_select_array')
async def get_materials_select_array():
    return await MaterialService.materials_select_array()
