from loguru import logger

logger.add("logs/main_file.log", colorize=True, backtrace=True, diagnose=True, format="{time} {level} {message}", rotation="1 MB", level="INFO")
