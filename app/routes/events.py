from fastapi import APIRouter, Request
from loguru import logger
from app.core.form import Form
from app.core.form_validation import FormValidation
from app.core.database import Database
from app.core.pagination import Pagination
from app.core.generic import Generic
from app.routes.users import User
from app.routes.stages import StageService

logger.add("logs/events.log", colorize=True, backtrace=True, diagnose=True, format="{time} {level} {message}",
           rotation="1 MB", level="INFO")

router = APIRouter(prefix="/events")


class EventService:
    collection_name = 'event'

    @staticmethod
    async def check_existing_event(field, value):
        event = await Database.fetch_one_item(EventService.collection_name, [{field: value}])
        if event:
            return await Form.return_response(
                True,
                'Event already exists',
                f"An event with this {field} already exists",
                'error',
                'danger'
            )
        return None

    @staticmethod
    async def add(request: Request):
        try:
            form_data = await Form.extract_form_input(request)
            validation_message = await FormValidation.require_inputs(form_data,
                                                                     ['title', 'event_type', 'start_date', 'end_date',
                                                                      'location'])
            if validation_message != 'valid_inputs':
                return validation_message

            # check if event already exists
            fields_to_check = ['title', 'start_date', 'location']
            for field in fields_to_check:
                response = await EventService.check_existing_event(field, form_data.get(field, ''))
                if response:
                    return response

            form_data['status'] = 'planned'
            await Database.insert_one_item(EventService.collection_name, form_data)

            return await Form.return_response(
                False,
                'Success',
                f"Event '{form_data['title']}' has been scheduled",
                'success',
                'success',
                response_action='reload_page'
            )
        except Exception as e:
            logger.error(f"Failed to create event: {e}")
            return await Form.return_response(
                True,
                'Failed to create event',
                str(e),
                'error',
                'danger'
            )

    @staticmethod
    async def paginated_report(page_number: int, page_size: int):
        try:
            table_title = "Events"
            table_columns = ['Title', 'Type', 'Start', 'End', 'Location',  'Author',
                             'Time']
            table_values = []

            events = await Pagination.paginated_results(
                page_number,
                page_size,
                EventService.collection_name,
                '/dashboard/admin/events/report'
            )

            users = await User.all_users()

            for event in events.get('results', []):
                event['agent'] = next(
                    (user['fullname'] for user in users if int(user['id']) == int(event['user_id'])), 'Error')

                if event:
                    table_values.append([
                        event.get('title', '---'),
                        event.get('event_type', '---'),
                        event.get('start_date', '---'),
                        event.get('end_date', '---'),
                        event.get('location', '---'),
                        event.get('agent', '---'),
                        event.get('time_elapsed', '---')
                    ])

            total_events = format(events.get('total_count', 0), ',')
            sub_title = "Events scheduled"

            cards = [{
                'title': 'Total number of events',
                'content': total_events,
            }]

            datatable = {
                'title': table_title,
                'sub_title': sub_title,
                'columns': table_columns,
                'values': table_values,
                'cards': cards,
                'pagination_details': events.get('pagination_details')
            }

            return await Form.return_response(
                False,
                'Success',
                "Events retrieved successfully",
                'success',
                'success',
                server_data=datatable
            )
        except Exception as e:
            logger.error(f"Failed to fetch events: {e}")
            return await Form.return_response(
                True,
                'Failed to fetch events',
                str(e),
                'error',
                'danger'
            )

    @staticmethod
    async def events_select_array():
        try:
            events = await EventService.all_events()
            select_array = await Generic.create_select_array(events, 'id', 'title')

            return await Form.return_response(
                False,
                'Success',
                "Events array retrieved successfully",
                'success',
                'success',
                server_data=select_array
            )
        except Exception as e:
            logger.error(f"Failed to fetch events: {e}")
            return await Form.return_response(
                True,
                'Failed to fetch events',
                str(e),
                'error',
                'danger'
            )

    @staticmethod
    async def all_events():
        try:
            events = await Database.fetch_many_items(EventService.collection_name)

            return events

        except Exception as e:
            logger.error(f"Failed to fetch events: {e}")
            return await Form.return_response(
                True,
                'Failed to fetch events',
                str(e),
                'error',
                'danger'
            )

    @staticmethod
    async def count():
        try:
            return await Database.count_items(EventService.collection_name)
        except Exception as e:
            logger.error(f"Failed to fetch events count: {e}")
            return await Form.return_response(
                True,
                'Failed to fetch events count',
                str(e),
                'error',
                'danger'
            )

    @staticmethod
    async def latest_events(limit: int):
        try:
            users = await User.all_users()
            events = await Database.fetch_many_items(EventService.collection_name, limit=limit)

            for event in events:
                event['agent'] = next(
                    (user['fullname'] for user in users if int(user['id']) == int(event['user_id'])), 'Error')

            return events

        except Exception as e:
            logger.error(f"Failed to fetch events: {e}")
            return await Form.return_response(
                True,
                'Failed to fetch events',
                str(e),
                'error',
                'danger'
            )


# Routes
@router.post('/add')
async def add_event(request: Request):
    return await EventService.add(request)


@router.get('/paginated_report/{page_number}/{page_size}')
async def get_paginated_report(page_number: int, page_size: int):
    return await EventService.paginated_report(page_number, page_size)


@router.get('/latest/{limit}')
async def get_latest_events(limit: int):
    return await EventService.latest_events(int(limit))


@router.get('/count')
async def count():
    return await EventService.count()


@router.get('/events_select_array')
async def get_events_select_array():
    return await EventService.events_select_array()
