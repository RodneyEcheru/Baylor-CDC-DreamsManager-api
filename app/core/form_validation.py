
import re
from app.core.form import Form


class FormValidation:
    @staticmethod
    async def require_inputs(form_data: list, required_inputs: list):
        try:
            if not form_data:
                return await Form.return_response(
                    True,
                    'Validation Error',
                    'Enter some deployment data to submit',
                    'error',
                    'danger')

            for form_input in required_inputs:
                if await Form.dictionary_value_is_empty(form_input, form_data):
                    return await Form.return_response(
                        True,
                        'Validation Error',
                        f'{form_input} is required',
                        'error',
                        'danger')

            return 'valid_inputs'

        except Exception as e:
            error_message = f'Failed to validate data: {str(e)}'
            return await Form.return_response(
                True,
                'Failed to validate data',
                error_message,
                'error',
                'danger')
