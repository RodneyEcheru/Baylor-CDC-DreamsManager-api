from fastapi.middleware.cors import CORSMiddleware
from loguru import logger


def configure_logging():
    logger.add("logs/main_file.log", colorize=True, backtrace=True, diagnose=True, format="{time} {level} {message}",
               rotation="1 MB", level="INFO")


def configure_cors(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allows all origins
        allow_credentials=True,
        allow_methods=["*"],  # Allows all methods
        allow_headers=["*"],  # Allows all headers
    )
