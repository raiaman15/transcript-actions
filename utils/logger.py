# Description: This file contains the functions for logging messages in the project.

# Importing the required libraries
import logging

# Setting up the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# A decorator function to log the function calls
def log_function_call(func):
    def wrapper(*args, **kwargs):
        logger.debug(f"Calling function: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper
