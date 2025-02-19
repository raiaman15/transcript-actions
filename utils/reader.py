# Description: This file contains the functions to read the transcript files.

# Importing the required libraries
import os

from utils.logger import log_function_call, logger

# Transcript reader function to read the transcript files (txt files)
@log_function_call
def read_transcript(file_path) -> str:
    logger.info(f"Reading the transcript file from: {file_path}")

    # Check if the file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found at the specified path: {file_path}")

    # Check if the file is a text file
    if not file_path.endswith('.txt'):
        raise ValueError("Only text files (.txt) are supported.")

    # Open the file in read mode
    with open(file_path, 'r') as file:
        transcript = file.read()

    logger.info("Transcript file read successfully.")

    return transcript