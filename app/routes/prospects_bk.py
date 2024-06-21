from fastapi import APIRouter, Request
from pprint import pprint

# core dependencies
from app.core.form import Form
from app.core.form_validation import FormValidation
from app.core.database import Database
from app.core.passwordutils import PasswordUtils
from app.core.pagination import Pagination

# module dependencies
from app.routes.users import User

# configure logger
from loguru import logger

logger.add("logs/prospects.log", colorize=True, backtrace=True, diagnose=True, format="{time} {level} {message}",
           rotation="1 MB", level="INFO")

router = APIRouter(prefix="/prospects")


class Prospect:
    collection_name = 'prospect'

    @staticmethod
    async def register(request):
        try:
            form_data = await Form.extract_form_input(request)

            # Validate form - require input fields
            validation_message = await FormValidation.require_inputs(form_data, [
                'name',
                'email',
                'phone_number',
                'address',
            ])
            if not isinstance(validation_message, str):
                return validation_message

            # Validate email if submitted
            if not await Form.dictionary_value_is_empty('email', form_data):
                if not await Form.is_valid_email(form_data['email']):
                    return await Form.return_response(
                        True,
                        'Validation Error',
                        'Enter a valid email',
                        'error',
                        'danger')

            # Check if prospect already exists
            prospect = await Database.fetch_one_item('prospect', [
                {'phone_number': form_data['phone_number']},
                {'email': form_data['email']},
            ])
            if prospect:
                return await Form.return_response(
                    True,
                    'Account already Exists',
                    "Phone number or email already exists, This prospect is already suggested",
                    'error',
                    'danger')

            # Assign default role
            form_data['status'] = 'new'

            # Insert prospect into database
            await Database.insert_one_item('prospect', form_data)

            # Return success message
            return await Form.return_response(
                False,
                'Success',
                f"{form_data['name']}'s has been added as a prospect",
                'success',
                'success',
                response_action='previous_page')

        except Exception as e:
            print(str(e))
            return await Form.return_response(
                True,
                'Failed to create prospect',
                (str(e)),
                'error',
                'danger')

    @staticmethod
    async def all(page_number, page_size):
        try:

            # table data
            table_title = f"Prospects"
            table_columns = [
                'Name',
                'Email',
                'Phone',
                'Address',
                'Signed by',
                'Product',
                'Status',
                'Time',
            ]
            table_values = []

            # Fetch prospects
            prospects = await Pagination.paginated_results(
                page_number,
                page_size,
                Prospect.collection_name,
                '/dashboard/admin/prospects/all',
            )

            from app.routes.products import Product

            # Fetch all products
            products = await Product.all_products()

            # Fetch users
            users = await User.all_users()

            # assign agent details to each prospect
            for prospect in prospects.get('results', []):
                prospect['agent'] = next((user['fullname'] for user in users if int(user['id']) == int(prospect['user_id'])),
                                         'Error')
                prospect['product'] = next((product['name'] for product in products if product['_id'] == prospect['product_id']),
                                         'Not Assigned')

                # append values to table values
                if prospect:

                    table_values.append([
                        value for value in [
                            prospect['name'] if prospect and 'name' in prospect else '---',
                            prospect['email'] if prospect and 'email' in prospect else '---',
                            prospect['phone_number'] if prospect and 'phone_number' in prospect else '---',
                            prospect['address'] if prospect and 'address' in prospect else '---',
                            prospect['agent'] if prospect and 'agent' in prospect else '---',
                            prospect['product'] if prospect and 'product' in prospect else '---',
                            f"""
                            <button type="button" onclick="history.back()" class="flex flex-row text-green-200 hover:text-green-800 hover:bg-green-200 bg-green-800 hover:border hover:border-green-800 transition shadow-md hover:shadow-2xl hover:scale-110 py-1 px-5 sm:ms-4 text-sm font-medium focus:outline-none rounded-full border-green-200 focus:z-10 focus:ring-4 focus:ring-gray-100 dark:focus:ring-gray-700 dark:border-gray-600">
                                assign
                            </button>
                            """,
                            prospect['time_elapsed'] if prospect and 'time_elapsed' in prospect else '---',
                        ] if prospect
                    ])

            total_prospects = format(prospects.get('total_count', 0), ',')
            sub_title = f"Prospects registered from field"

            cards = [
                {
                    'title': 'Total number of prospects',
                    'content': total_prospects,
                }
            ]

            datatable = {
                'title': table_title,
                'sub_title': sub_title,
                'columns': table_columns,
                'values': table_values,
                'cards': cards,
                'pagination_details': prospects.get('pagination_details')
            }

            # Return success message
            return await Form.return_response(
                False,
                'Success',
                f"Prospects retrieved successfully",
                'success',
                'success',
                server_data=datatable)

        except Exception as e:
            print(str(e))
            return await Form.return_response(
                True,
                'Failed to create prospect',
                (str(e)),
                'error',
                'danger')


# create a new prospect
@router.post('/new')
async def new_prospect(request: Request):
    return await Prospect.register(request)


# fetch all prospects
@router.get('/all/{page_number}/{page_size}')
async def all_prospects(page_number, page_size):
    return await Prospect.all(page_number, page_size)
