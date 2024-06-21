from fastapi import Request
from fastapi.responses import JSONResponse
from app.core.database import Database
from app.core.form import Form


async def handle_database_connection_error():
    response = await Form.return_response(
        True,
        'Database Error',
        'Database is not connected, please check your database connection',
        'error',
        'danger'
    )
    return JSONResponse(status_code=500, content=response)


async def check_database_connection(request: Request, call_next):
    connection = await Database.is_live()
    if connection:
        return await call_next(request)
    else:
        return await handle_database_connection_error()
