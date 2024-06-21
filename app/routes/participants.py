from fastapi import APIRouter, Request
from loguru import logger
from app.core.form import Form
from app.core.form_validation import FormValidation
from app.core.database import Database
from app.core.pagination import Pagination
from app.core.generic import Generic
from app.routes.users import User
from app.routes.stages import StageService

logger.add("logs/participants.log", colorize=True, backtrace=True, diagnose=True, format="{time} {level} {message}",
           rotation="1 MB", level="INFO")

router = APIRouter(prefix="/participants")


class ParticipantService:
    collection_name = 'participant'

    @staticmethod
    async def check_existing_participant(field, value):
        participant = await Database.fetch_one_item(ParticipantService.collection_name, [{field: value}])
        if participant:
            return await Form.return_response(
                True,
                'Participant already exists',
                f"A participant with this {field} already exists",
                'error',
                'danger'
            )
        return None

    @staticmethod
    async def add(request: Request):
        try:
            form_data = await Form.extract_form_input(request)
            validation_message = await FormValidation.require_inputs(form_data,
                                                                     ['name', 'user_id', 'hiv_status'])
            if validation_message != 'valid_inputs':
                return validation_message

            # check if participant already exists
            fields_to_check = ['name', 'email', 'phone']
            for field in fields_to_check:
                response = await ParticipantService.check_existing_participant(field, form_data.get(field, ''))
                if response:
                    return response

            form_data['status'] = 'active'
            await Database.insert_one_item(ParticipantService.collection_name, form_data)

            return await Form.return_response(
                False,
                'Success',
                f"{form_data['name']} has been registered",
                'success',
                'success',
                response_action='reload_page'
            )
        except Exception as e:
            logger.error(f"Failed to create participant: {e}")
            return await Form.return_response(
                True,
                'Failed to create participant',
                str(e),
                'error',
                'danger'
            )

    @staticmethod
    async def paginated_report(page_number: int, page_size: int):
        try:
            table_title = "Participants"
            table_columns = ['Name', 'HIV Status', 'Manage', 'Registered by', 'Time']
            table_values = []

            participants = await Pagination.paginated_results(
                page_number,
                page_size,
                ParticipantService.collection_name,
                '/dashboard/admin/participants/report'
            )

            users = await User.all_users()
            stages = await StageService.all_stages()

            for participant in participants.get('results', []):
                participant['agent'] = next(
                    (user['fullname'] for user in users if int(user['id']) == int(participant['user_id'])), 'Error')
                participant['stage'] = next(
                    (stage['name'] for stage in stages if int(stage['id']) == int(participant['stage_id'])), 'Error')

                button = f"""
                          <a href="/dashboard/admin/participants/{participant.get('id')}/profile"
                            class="rounded-full h-6 btn border border-primary font-medium text-primary hover:bg-primary hover:text-white focus:bg-primary focus:text-white active:bg-primary/90 dark:border-accent dark:text-accent-light dark:hover:bg-accent dark:hover:text-white dark:focus:bg-accent dark:focus:text-white dark:active:bg-accent/90"
                          >
                            Manage Participant
                          </a>
                    """

                if participant:
                    table_values.append([
                        participant.get('name', '---'),
                        participant.get('hiv_status', '---'),
                        button,
                        participant.get('agent', '---'),
                        participant.get('time_elapsed', '---')
                    ])

            total_participants = format(participants.get('total_count', 0), ',')
            sub_title = "Participants registered from field"

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
        try:
            participants = await ParticipantService.all_participants()
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
        try:
            participants = await Database.fetch_many_items(ParticipantService.collection_name)

            return participants

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
        try:
            return await Database.count_items(ParticipantService.collection_name)
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
        try:
            users = await User.all_users()
            participants = await Database.fetch_many_items(ParticipantService.collection_name, limit=limit)

            for participant in participants:
                participant['agent'] = next(
                    (user['fullname'] for user in users if int(user['id']) == int(participant['user_id'])), 'Error')

            return participants

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
    async def profile(participant_id: int):
        try:
            return await Database.fetch_one_item(ParticipantService.collection_name, query_list_of_dictionaries=[
                {'id': participant_id}
            ])

        except Exception as e:
            logger.error(f"Failed to fetch agents: {e}")
            return await Form.return_response(
                True,
                'Failed to fetch agents',
                str(e),
                'error',
                'danger'
            )

    @staticmethod
    async def change_role(agentID, action):
        """
        Update user account status
        """
        action_performed = ""
        agent = await User.get_details_by_user_id(agentID)
        if not agent:
            # return response
            return await Form.return_response(
                True,
                'Agent not found',
                f"agent with id {agentID} not found",
                'error',
                'danger',
                response_action='none'
            )

        if action == 'activate':
            await Database.update_one_item(AgentService.collection_name, {'default_role': 'agent'}, 'id', agentID, True)
            action_performed = "account activated"
        elif action == 'suspend':
            await Database.update_one_item(AgentService.collection_name, {'read_status': 'suspended'}, 'id', agentID, True)
            action_performed = "account suspended"
        elif action == 'deactivate':
            await Database.update_one_item(AgentService.collection_name, {'read_status': 'deactivated'}, 'id', agentID, True)
            action_performed = "account deactivated"

        # return response
        return await Form.return_response(
            False,
            'Account Modified',
            f"{agent['fullname']}'s {action_performed}",
            'success',
            'info',
            response_action='reload_page'
        )


# Routes
@router.post('/add')
async def add_participant(request: Request):
    return await ParticipantService.add(request)


@router.get('/paginated_report/{page_number}/{page_size}')
async def get_paginated_report(page_number: int, page_size: int):
    return await ParticipantService.paginated_report(page_number, page_size)


@router.get('/latest/{limit}')
async def get_latest_participants(limit: int):
    return await ParticipantService.latest_participants(int(limit))


@router.get('/count')
async def count():
    return await ParticipantService.count()


@router.get('/participants_select_array')
async def get_participants_select_array():
    return await ParticipantService.participants_select_array()


@router.get('/profile/{participant_id}')
async def profile(participant_id: int):
    return await ParticipantService.profile((int(participant_id)))
