from fastapi.responses import JSONResponse
from app.core.form import Form
from app.core.database import Database


async def not_found_exception_handler(request, exc):
    response = await Form.return_response(
        True,
        'Resource Error',
        f'The requested resource <br/> ( {request.url.path} )<br/>does not exist',
        'error',
        'danger')
    return JSONResponse(response, status_code=404)


async def method_not_allowed_exception_handler(request, exc):
    response = await Form.return_response(
        True,
        'HTTP Method error',
        'The requested HTTP method (post/get method) was not found',
        'error',
        'danger')
    return JSONResponse(response, status_code=405)


async def internal_server_error_exception_handler(request, exc):
    response = await Form.return_response(
        True,
        'Server error',
        'An error happened during the execution, check server logs for more information',
        'error',
        'danger')
    return JSONResponse(response, status_code=500)
