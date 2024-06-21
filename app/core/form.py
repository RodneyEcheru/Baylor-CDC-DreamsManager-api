import os
import re
from pathlib import Path
from pprint import pprint

# from fastapi import File, UploadFile
from starlette.datastructures import UploadFile

from app.core.dateFunctions import DateFunctions

# configure logger
from loguru import logger

logger.add("logs/main_file.log", colorize=True, backtrace=True, diagnose=True, format="{time} {level} {message}",
           rotation="1 MB", level="INFO")


class Form:
    @staticmethod
    async def extract_form_input(request):
        form_data = await request.form()

        # process files
        item = {}
        keys_to_ignore = ['password', 'confirm_password']
        for key, value in form_data.items():
            # check if the item is an UploadFile object
            if isinstance(value, UploadFile):
                file = value
                # do something with the file
                # save the file to the folder if it exists
                if file:
                    # create the folder if it doesn't exist
                    Path("uploaded_files").mkdir(parents=True, exist_ok=True)

                    # write file to disk
                    # get the current time in the format YYYYMMDD_HHMMSS_microseconds
                    timestamp = await DateFunctions.return_current_timestamp()
                    # split the file name into the base name and the extension
                    base_name, extension = os.path.splitext(file.filename)
                    # append the timestamp to the base name
                    file_name = f"{base_name}_{timestamp}"
                    # add the extension back to the file name
                    file_name = file_name + extension
                    file_name = re.sub(r"[^\w.-]", "_", file_name)
                    # append the timestamp to the file name
                    # file_name = f"{file.filename}_{timestamp}"
                    with open(f"../../uploaded_files/{file_name}", "wb") as f:
                        f.write(await file.read())

                    # form_data[key] = f"uploaded_files/{file_name}"
                    item[key] = f"uploaded_files/{file_name}"
                    keys_to_ignore.append(key)

        # do not parse passwords coz passwords can either be int or string hence affected by password hashing
        password = False if await Form.dictionary_value_is_empty('password', form_data) else form_data['password']
        confirm_password = False if await Form.dictionary_value_is_empty('confirm_password', form_data) else form_data[
            'confirm_password']

        # parse form values converting them to either string or int
        formatted_dictionary = {
            key: int(value.strip()) if value.strip().isdigit() else value.strip()
            for key, value in form_data.items()
            if key not in keys_to_ignore
        }

        formatted_dictionary.update(item)

        # reassign password and confirm password
        if password:
            formatted_dictionary['password'] = password
        if confirm_password:
            formatted_dictionary['confirm_password'] = confirm_password

        # return dictionary representation of form
        return formatted_dictionary

    @staticmethod
    async def create_initials(string):
        return "".join(word[0].upper() for word in string.split())

    @staticmethod
    async def dictionary_value_is_empty(key, dictionary):
        if key not in dictionary:
            return True
        value = dictionary[key]
        return value is None or (isinstance(value, str) and value.strip() == '')

    @staticmethod
    async def return_response(server_error: bool, server_message, message_detail, response_status, response_color,
                              server_data=None, response_action=''):
        try:
            server_data = server_data if server_data is not None else {}
            logger.info(f"server_error: {server_error}")
            logger.info(f"server_message: {server_message}")
            return {
                "server_error": server_error,
                "server_message": server_message,
                "message_detail": message_detail,
                "response_status": response_status,
                "response_color": response_color,
                "response_action": response_action,
                "server_data": server_data,
            }
        # Use the except keyword to catch the exception and handle it
        except Exception as e:
            # You can print the error message or do something else
            pprint(str(e))
            # You can also return a different value or None
            return None

    @staticmethod
    async def is_valid_email(email):
        pattern = r"[^@]+@[^@]+\.[^@]+"
        return bool(re.match(pattern, email))
