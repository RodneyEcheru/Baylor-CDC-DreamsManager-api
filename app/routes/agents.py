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

logger.add("logs/agents.log", colorize=True, backtrace=True, diagnose=True, format="{time} {level} {message}",
           rotation="1 MB", level="INFO")

router = APIRouter(prefix="/agents")


class AgentService:
    collection_name = 'user'

    @staticmethod
    async def paginated_report(page_number: int, page_size: int):
        try:
            table_title = "Agents"
            table_columns = ['Name', 'role', 'Account', 'Time']
            table_values = []

            agents = await Pagination.paginated_results(
                page_number,
                page_size,
                AgentService.collection_name,
                '/dashboard/admin/agents/report',
                exclude_list_of_dictionaries=[{'default_role': 'root'}]
            )

            for agent in agents.get('results', []):

                if agent:
                    button = f"""
                              <a href="/dashboard/admin/agents/{agent.get('id')}/profile"
                                class="rounded-full h-6 btn border border-primary font-medium text-primary hover:bg-primary hover:text-white focus:bg-primary focus:text-white active:bg-primary/90 dark:border-accent dark:text-accent-light dark:hover:bg-accent dark:hover:text-white dark:focus:bg-accent dark:focus:text-white dark:active:bg-accent/90"
                              >
                                View Agent
                              </a>
                        """
                    table_values.append([
                        agent.get('fullname', '---'),
                        agent.get('default_role', '---'),
                        button,
                        agent.get('time_elapsed', '---')
                    ])

            total_agents = format(agents.get('total_count', 0), ',')
            sub_title = "Agents / Staff registered from field"

            cards = [{
                'title': 'Total number of agents',
                'content': total_agents,
            }]

            datatable = {
                'title': table_title,
                'sub_title': sub_title,
                'columns': table_columns,
                'values': table_values,
                'cards': cards,
                'pagination_details': agents.get('pagination_details')
            }

            return await Form.return_response(
                False,
                'Success',
                "Agents retrieved successfully",
                'success',
                'success',
                server_data=datatable
            )
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
    async def agents_select_array():
        try:
            agents = await AgentService.all_agents()
            select_array = await Generic.create_select_array(agents, 'id', 'fullname')

            return await Form.return_response(
                False,
                'Success',
                "Agents array retrieved successfully",
                'success',
                'success',
                server_data=select_array
            )
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
    async def all_agents():
        try:
            return await Database.fetch_many_items(AgentService.collection_name, exclude_list_of_dictionaries=[
                {'default_role': 'root'}
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
    async def profile(agent_id: int):
        try:
            return await Database.fetch_one_item(AgentService.collection_name, query_list_of_dictionaries=[
                {'id': agent_id}
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
    async def count():
        try:
            return await Database.count_items(AgentService.collection_name, exclude_list_of_dictionaries=[
                {'default_role': 'root'}
            ])
        except Exception as e:
            logger.error(f"Failed to fetch agents count: {e}")
            return await Form.return_response(
                True,
                'Failed to fetch agents',
                str(e),
                'error',
                'danger'
            )

    @staticmethod
    async def latest_agents(limit: int):
        try:
            return await Database.fetch_many_items(AgentService.collection_name, limit=limit, exclude_list_of_dictionaries=[
                {'default_role': 'root'}
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


@router.get('/paginated_report/{page_number}/{page_size}')
async def get_paginated_report(page_number: int, page_size: int):
    return await AgentService.paginated_report(page_number, page_size)


@router.get('/latest/{limit}')
async def get_latest_agents(limit: int):
    return await AgentService.latest_agents(int(limit))


@router.get('/count')
async def count():
    return await AgentService.count()


@router.get('/agents_select_array')
async def get_agents_select_array():
    return await AgentService.agents_select_array()


@router.get('/profile/{agent_id}')
async def profile(agent_id: int):
    return await AgentService.profile((int(agent_id)))


# Authenticate user
@router.get('/change-role/{agentID}/{action}')
async def change_role(agentID: str, action: str):
    return await AgentService.change_role(agentID, action)
