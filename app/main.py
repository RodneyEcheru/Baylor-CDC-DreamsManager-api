from fastapi import FastAPI
from app.core.logger import logger
from app.core.form import Form
from fastapi.staticfiles import StaticFiles
from app.middleware.check_database_live_status import check_database_connection
from app.exceptions.handlers import not_found_exception_handler, method_not_allowed_exception_handler, \
    internal_server_error_exception_handler
from app.routes import router as api_router
from app.config import configure_cors, configure_logging

app = FastAPI(debug=True)
app.mount("/uploaded_files", StaticFiles(directory="uploaded_files"), name="uploaded_files")

configure_logging()
configure_cors(app)

app.middleware("http")(check_database_connection)

# app.add_exception_handler(500, check_database_connection)
app.add_exception_handler(404, not_found_exception_handler)
app.add_exception_handler(405, method_not_allowed_exception_handler)
app.add_exception_handler(500, internal_server_error_exception_handler)

app.include_router(api_router)


@app.get("/")
async def welcome():
    return await Form.return_response(
        False,
        'Welcome message',
        "You have reached the memo API, Please specify the resources I can serve you",
        'success',
        'success')
