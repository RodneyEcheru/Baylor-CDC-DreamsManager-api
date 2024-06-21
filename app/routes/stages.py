from fastapi import APIRouter, Request
from loguru import logger
from app.core.form import Form
from app.core.form_validation import FormValidation
from app.core.database import Database
from app.core.pagination import Pagination
from app.core.generic import Generic
from app.routes.users import User

logger.add("logs/stages.log", colorize=True, backtrace=True, diagnose=True, format="{time} {level} {message}",
           rotation="1 MB", level="INFO")

router = APIRouter(prefix="/stages")


class StageService:
    collection_name = 'stage'

    @staticmethod
    async def add(request: Request):
        try:
            form_data = await Form.extract_form_input(request)
            validation_message = await FormValidation.require_inputs(form_data, ['name', 'user_id'])
            if validation_message != 'valid_inputs':
                return validation_message

            stage = await Database.fetch_one_item(StageService.collection_name, [{'name': form_data['name']}])
            if stage:
                return await Form.return_response(
                    True,
                    'Stage already exists',
                    "This stage is already registered",
                    'error',
                    'danger'
                )

            form_data['status'] = 'active'
            await Database.insert_one_item(StageService.collection_name, form_data)

            return await Form.return_response(
                False,
                'Success',
                f"{form_data['name']} has been registered",
                'success',
                'success',
                response_action='reload_page'
            )
        except Exception as e:
            logger.error(f"Failed to create stage: {e}")
            return await Form.return_response(
                True,
                'Failed to create stage',
                str(e),
                'error',
                'danger'
            )

    @staticmethod
    async def paginated_report(page_number: int, page_size: int):
        try:
            table_title = "Stages"
            table_columns = ['Name', 'Registered by', 'Time']
            table_values = []

            stages = await Pagination.paginated_results(
                page_number,
                page_size,
                StageService.collection_name,
                '/dashboard/admin/stages/report'
            )

            users = await User.all_users()

            for stage in stages.get('results', []):
                stage['agent'] = next((user['fullname'] for user in users if int(user['id']) == int(stage['user_id'])), 'Error')

                if stage:
                    table_values.append([
                        stage.get('name', '---'),
                        stage.get('agent', '---'),
                        stage.get('time_elapsed', '---')
                    ])

            total_stages = format(stages.get('total_count', 0), ',')
            sub_title = "Stages registered from field"

            cards = [{
                'title': 'Total number of stages',
                'content': total_stages,
            }]

            datatable = {
                'title': table_title,
                'sub_title': sub_title,
                'columns': table_columns,
                'values': table_values,
                'cards': cards,
                'pagination_details': stages.get('pagination_details')
            }

            return await Form.return_response(
                False,
                'Success',
                "Stages retrieved successfully",
                'success',
                'success',
                server_data=datatable
            )
        except Exception as e:
            logger.error(f"Failed to fetch stage: {e}")
            return await Form.return_response(
                True,
                'Failed to fetch stage',
                str(e),
                'error',
                'danger'
            )

    @staticmethod
    async def select_array():
        try:
            stages = await StageService.all_stages()
            select_array = await Generic.create_select_array(stages, 'id', 'name')

            return await Form.return_response(
                False,
                'Success',
                "Stages array retrieved successfully",
                'success',
                'success',
                server_data=select_array
            )
        except Exception as e:
            logger.error(f"Failed to fetch stages: {e}")
            return await Form.return_response(
                True,
                'Failed to fetch stages',
                str(e),
                'error',
                'danger'
            )

    @staticmethod
    async def all_stages():
        try:
            return await Database.fetch_many_items(StageService.collection_name)
        except Exception as e:
            logger.error(f"Failed to fetch stages: {e}")
            return await Form.return_response(
                True,
                'Failed to fetch stages',
                str(e),
                'error',
                'danger'
            )

    @staticmethod
    async def count():
        try:
            return await Database.count_items(StageService.collection_name)
        except Exception as e:
            logger.error(f"Failed to fetch stages count: {e}")
            return await Form.return_response(
                True,
                'Failed to fetch stages',
                str(e),
                'error',
                'danger'
            )

    @staticmethod
    async def latest_stages(limit: int):
        try:
            return await Database.fetch_many_items(StageService.collection_name, limit=limit)
        except Exception as e:
            logger.error(f"Failed to fetch stages: {e}")
            return await Form.return_response(
                True,
                'Failed to fetch stages',
                str(e),
                'error',
                'danger'
            )


# Routes
@router.post('/add')
async def add_stage(request: Request):
    return await StageService.add(request)


@router.get('/paginated_report/{page_number}/{page_size}')
async def get_paginated_report(page_number: int, page_size: int):
    return await StageService.paginated_report(page_number, page_size)


@router.get('/latest/{limit}')
async def get_latest_stages(limit: int):
    return await StageService.latest_stages(int(limit))


@router.get('/count')
async def count():
    return await StageService.count()


@router.get('/select_array')
async def get_stages_select_array():
    return await StageService.select_array()
