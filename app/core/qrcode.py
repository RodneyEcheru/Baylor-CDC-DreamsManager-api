from pathlib import Path
import qrcode
from fastapi import APIRouter
from typing import Optional, Union
import os
import re


# dependencies
from app.core.dateFunctions import DateFunctions
from app.core.form import Form

# modules

router = APIRouter(prefix="/qrcode")

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
QRCODE_DESTINATION_PATH = Path('uploaded_files').resolve()
QRCODE_DESTINATION_PATH.mkdir(parents=True, exist_ok=True)
QRCODE_API_IMAGE_PATH = "uploaded_files"


class Qrcode:
    @staticmethod
    @staticmethod
    async def generate_qrcode(data: str, entity_type: str, entity_id: Optional[Union[str, int]] = None,
                              qr_code_type: str = "id") -> str:
        try:
            # Create a QR code instance
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )

            # Add data to the QR code
            qr.add_data(data)
            qr.make(fit=True)

            # Generate the QR code image
            img = qr.make_image(fill_color="black", back_color="white")

            # Get the absolute path of the 'uploaded_files' directory
            QRCODE_DESTINATION_PATH = Path('uploaded_files').resolve()

            # Create the destination folder if it doesn't exist
            QRCODE_DESTINATION_PATH.mkdir(parents=True, exist_ok=True)

            # Generate the file name
            timestamp = await DateFunctions.return_current_timestamp()
            file_name = f"{entity_type}_{qr_code_type}_{entity_id}_{timestamp}.png" if entity_id else f"{entity_type}_{qr_code_type}_{timestamp}.png"
            file_name = re.sub(r'[^a-zA-Z0-9._]', '_', file_name)
            # Construct the file path using Path.joinpath()
            file_path = QRCODE_DESTINATION_PATH.joinpath(file_name)

            # Save the QR code image to a file
            with file_path.open('wb') as f:
                img.save(f)

            print(f"QR code for {entity_type} {qr_code_type} saved as {file_name}")
            return f"{QRCODE_API_IMAGE_PATH}/{file_name}"

        except Exception as e:
            print(str(e))
            return await Form.return_response(
                True,
                'Failed to generate QR code',
                (str(e)),
                'error',
                'danger'
            )

    @staticmethod
    async def generate_id_qrcode(entity_type: str, entity_id: Union[str, int]):
        return await Qrcode.generate_qrcode(str(entity_id), entity_type, entity_id, "id")

    @staticmethod
    async def generate_api_qrcode(entity_type: str, entity_id: Union[str, int], api_url: str):
        return await Qrcode.generate_qrcode(api_url, entity_type, entity_id, "api")

    @staticmethod
    async def generate_web_qrcode(entity_type: str, entity_id: Union[str, int], web_url: str):
        return await Qrcode.generate_qrcode(web_url, entity_type, entity_id, "web")


# @router.get('/school/{school_id}')
# async def all_students_datatable_(request: Request, school_id: str):
    # return await Student.all_students_datatable(request, school_id)