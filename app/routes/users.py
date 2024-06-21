from fastapi import APIRouter, Request
from pprint import pprint
from argon2 import PasswordHasher

# dependencies
from app.core.form import Form
from app.core.form_validation import FormValidation
from app.core.database import Database
from app.core.passwordutils import PasswordUtils

router = APIRouter(prefix="/user")


class User:
    collection_name = 'user'

    @staticmethod
    async def register(request: Request):
        """
        Register a new user.
        """
        try:
            form_data = await Form.extract_form_input(request)
            validation_message = await User.validate_registration_form(form_data)
            if validation_message:
                return validation_message

            await User.process_form_data(form_data)
            user_exists = await User.check_user_exists(form_data['phone_number'])
            if user_exists:
                return await Form.return_response(
                    True,
                    'Account already Exists',
                    "Phone number already exists, login if you already have an account",
                    'error',
                    'danger')

            form_data['default_role'] = 'Guest' if await Database.fetch_one_item(User.collection_name) else 'root'
            form_data['read_status'] = "active"
            await Database.insert_one_item(User.collection_name, form_data)

            return await Form.return_response(
                False,
                'Success',
                f"{form_data['first_name']}'s Account Created, You can now login",
                'success',
                'success',
                response_action='login_page')

        except Exception as e:
            return await User.handle_exception('Failed to create user account', str(e))

    @staticmethod
    async def validate_registration_form(form_data):
        """
        Validate the registration form data.
        """
        validation_message = await FormValidation.require_inputs(form_data, [
            'fullname',
            'password',
            'confirm_password',
            'phone_country_code',
            'phone',
        ])
        if not isinstance(validation_message, str):
            return validation_message

        full_name = form_data['fullname'].split(' ')
        if len(full_name) < 2:
            return await Form.return_response(
                True,
                'Validation Error',
                'Full name requires at least 2 names such as Mujabi John',
                'error',
                'danger')

        if form_data['password'] != form_data['confirm_password']:
            return await Form.return_response(
                True,
                'Validation Error',
                'Passwords do not match, repeat the password you just typed',
                'error',
                'danger')

        if not await Form.dictionary_value_is_empty('email', form_data) and not await Form.is_valid_email(
                form_data['email']):
            return await Form.return_response(
                True,
                'Validation Error',
                'Enter a valid email',
                'error',
                'danger')

        return None

    @staticmethod
    async def process_form_data(form_data):
        """
        Process the form data for registration.
        """
        full_name = form_data['fullname'].split(' ')
        form_data['first_name'] = full_name[0]
        form_data['last_name'] = full_name[1]
        form_data['other_names'] = " ".join(full_name[2:])
        form_data['name_abbreviation'] = await Form.create_initials(form_data['fullname'])

        form_data['password'] = PasswordUtils.hash_password(form_data['password'])
        del form_data['confirm_password']

        form_data['phone_number'] = f"{form_data['phone_country_code']}{form_data['phone'].lstrip('0')}" if \
            str(form_data['phone'])[0] == "0" else f"{form_data['phone_country_code']}{form_data['phone']}"

    @staticmethod
    async def check_user_exists(phone_number):
        """
        Check if a user already exists with the given phone number.
        """
        user = await Database.fetch_one_item(User.collection_name, [{'phone_number': phone_number}])
        return user is not None

    @staticmethod
    async def handle_exception(message, error):
        """
        Handle exceptions and return a formatted response.
        """
        print(error)
        return await Form.return_response(
            True,
            message,
            error,
            'error',
            'danger')

    @staticmethod
    async def all_users():
        """
        Retrieve all users.
        """
        try:
            return await Database.fetch_many_items(User.collection_name)
        except Exception as e:
            return await User.handle_exception('Failed to retrieve users', str(e))

    @staticmethod
    async def login(request: Request):
        """
        Authenticate a user.
        """
        try:
            form_data = await Form.extract_form_input(request)
            validation_message = await FormValidation.require_inputs(form_data, ['username', 'password'])
            if not isinstance(validation_message, str):
                return validation_message

            user = await Database.fetch_one_item(User.collection_name,
                                                 [{'phone': form_data['username']}, {'email': form_data['username']}])
            if not user:
                return await Form.return_response(
                    True,
                    'Account does not exist',
                    f"Phone / Email {form_data['username']} does not exist, create an account if you're new",
                    'error',
                    'danger')

            valid_password = PasswordUtils.verify_password(form_data['password'], user.get('password', ''))
            if not valid_password:
                return await Form.return_response(
                    True,
                    'Wrong password',
                    f"'{form_data['password']}' password is not valid",
                    'error',
                    'danger')

            user.pop('password', None)
            return await Form.return_response(
                False,
                'Login successful',
                f"{form_data['username']} authorised",
                'success',
                'info',
                response_action='login_user',
                server_data=user)

        except Exception as e:
            return await User.handle_exception('Failed to authenticate account', str(e))

    @staticmethod
    async def get_details_by_user_id(user_id):
        """
        Get user details by user id.
        """
        return await Database.fetch_one_item_by_integer_id(User.collection_name, user_id)


# Create account for a new user
@router.post('/register')
async def create_user(request: Request):
    return await User.register(request)


# Authenticate user
@router.post('/login')
async def login_user(request: Request):
    return await User.login(request)
