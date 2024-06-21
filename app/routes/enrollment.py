
# app/routes/enrollment.py
from fastapi import APIRouter, Request
from loguru import logger
from app.core.form import Form
from app.core.form_validation import FormValidation
from app.core.database import Database
from app.core.pagination import Pagination
from app.core.generic import Generic

logger.add("logs/enrollment.log", colorize=True, backtrace=True, diagnose=True, format="{time} {level} {message}",
           rotation="1 MB", level="INFO")

router = APIRouter(prefix="/enrollment")


class EnrollmentService:
    collection_name = 'enrollment'

    @staticmethod
    async def add(request: Request):
        """
        Add a new participant.
        """
        try:
            form_data = await Form.extract_form_input(request)
            validation_message = await FormValidation.require_inputs(form_data, [
                'name', 'address', 'age', 'hiv_status', 'dob', 'village', 'schooling_status'
            ])
            if validation_message != 'valid_inputs':
                return validation_message

            participant = await Database.fetch_one_item(EnrollmentService.collection_name, [{'name': form_data['name']}])
            if participant:
                return await Form.return_response(
                    True,
                    'Participant already exists',
                    "This participant is already enrolled",
                    'error',
                    'danger'
                )

            form_data['status'] = 'active'
            await Database.insert_one_item(EnrollmentService.collection_name, form_data)

            return await Form.return_response(
                False,
                'Success',
                f"{form_data['name']} has been enrolled",
                'success',
                'success',
                response_action='reload_page'
            )
        except Exception as e:
            logger.error(f"Failed to enroll participant: {e}")
            return await Form.return_response(
                True,
                'Failed to enroll participant',
                str(e),
                'error',
                'danger'
            )

    @staticmethod
    async def paginated_report(page_number: int, page_size: int):
        """
        Generate a paginated report of participants.
        """
        try:
            table_title = "Participants"
            table_columns = ['Name', 'Address', 'Age', 'HIV Status', 'DOB', 'Village', 'Schooling Status']
            table_values = []

            participants = await Pagination.paginated_results(
                page_number,
                page_size,
                EnrollmentService.collection_name,
                '/dashboard/admin/enrollment/report'
            )

            for participant in participants.get('results', []):
                table_values.append([
                    participant.get('name', '---'),
                    participant.get('address', '---'),
                    participant.get('age', '---'),
                    participant.get('hiv_status', '---'),
                    participant.get('dob', '---'),
                    participant.get('village', '---'),
                    participant.get('schooling_status', '---')
                ])

            total_participants = format(participants.get('total_count', 0), ',')
            sub_title = "Enrolled participants"

            cards = [{
                'title': 'Total number of participants',
                'content': total_participants,
            }]

            datatable = {
                'title': table_title,
                'sub_title': sub_title,
                'columns': table_columns,
                'values': table_values,
                'cards': cards,
                'pagination_details': participants.get('pagination_details')
            }

            return await Form.return_response(
                False,
                'Success',
                "Participants retrieved successfully",
                'success',
                'success',
                server_data=datatable
            )
        except Exception as e:
            logger.error(f"Failed to fetch participants: {e}")
            return await Form.return_response(
                True,
                'Failed to fetch participants',
                str(e),
                'error',
                'danger'
            )

    @staticmethod
    async def participants_select_array():
        """
        Get an array of participants for selection.
        """
        try:
            participants = await EnrollmentService.all_participants()
            select_array = await Generic.create_select_array(participants, 'id', 'name')

            return await Form.return_response(
                False,
                'Success',
                "Participants array retrieved successfully",
                'success',
                'success',
                server_data=select_array
            )
        except Exception as e:
            logger.error(f"Failed to fetch participants: {e}")
            return await Form.return_response(
                True,
                'Failed to fetch participants',
                str(e),
                'error',
                'danger'
            )

    @staticmethod
    async def all_participants():
        """
        Retrieve all participants.
        """
        try:
            return await Database.fetch_many_items(EnrollmentService.collection_name)
        except Exception as e:
            logger.error(f"Failed to fetch participants: {e}")
            return await Form.return_response(
                True,
                'Failed to fetch participants',
                str(e),
                'error',
                'danger'
            )

    @staticmethod
    async def count():
        """
        Get the total count of participants.
        """
        try:
            return await Database.count_items(EnrollmentService.collection_name)
        except Exception as e:
            logger.error(f"Failed to fetch participants count: {e}")
            return await Form.return_response(
                True,
                'Failed to fetch participants count',
                str(e),
                'error',
                'danger'
            )

    @staticmethod
    async def latest_participants(limit: int):
        """
        Retrieve the latest participants.
        """
        try:
            return await Database.fetch_many_items(EnrollmentService.collection_name, limit=limit)
        except Exception as e:
            logger.error(f"Failed to fetch participants: {e}")
            return await Form.return_response(
                True,
                'Failed to fetch participants',
                str(e),
                'error',
                'danger'
            )


# Routes
@router.post('/add')
async def add_participant(request: Request):
    return await EnrollmentService.add(request)


@router.get('/paginated_report/{page_number}/{page_size}')
async def get_paginated_report(page_number: int, page_size: int):
    return await EnrollmentService.paginated_report(page_number, page_size)


@router.get('/latest/{limit}')
async def get_latest_participants(limit: int):
    return await EnrollmentService.latest_participants(int(limit))


@router.get('/count')
async def count():
    return await EnrollmentService.count()


@router.get('/participants_select_array')
async def get_participants_select_array():
    return await EnrollmentService.participants_select_array()
