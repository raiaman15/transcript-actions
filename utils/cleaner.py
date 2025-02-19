# Description: This file contains the functions to clean the transcript data.
import re
from typing import List, Set

from utils.logger import log_function_call, logger


# A function to clean the transcript data
@log_function_call
def clean_transcript(transcript: str, valid_jira_boards: Set[str]) -> str:
    """
    Standardize the JIRA ticket numbers mentioned in the transcript as per the JIRA board names.
    Args:
        transcript: The transcript data to be cleaned.
        valid_jira_boards: The list of valid JIRA board names.
    Returns:
        str: The cleaned transcript data.
    """

    logger.info("Cleaning the transcript data.")

    # Standardize the JIRA ticket numbers
    # Replace <JIRA_BOARD><anything><JIRA_TICKET_NUMBER> with <JIRA_BOARD>-<JIRA_TICKET_NUMBER> using regex
    # Make all JIRA board names as capital letters
    cleaned_transcript = transcript
    for jira_board in valid_jira_boards:
        cleaned_transcript = re.sub(rf"{jira_board}\D*(\d+)", rf"{jira_board}-\1", cleaned_transcript)
        cleaned_transcript = re.sub(rf"{jira_board}-", rf"{jira_board.upper()}-", cleaned_transcript)

    logger.info("Transcript data cleaned successfully.")

    return cleaned_transcript


# A function to identify the team members mentioned in the transcript
@log_function_call
def extract_team_members(transcript: str) -> Set[str]:
    """
    Identify the team members mentioned in the transcript.
    Args:
        transcript: The transcript data.
    Returns:
        List[str]: The list of team members mentioned in the transcript.
    """

    logger.info("Identifying the team members mentioned in the transcript.")

    # In the transcript, team members names are available at each new line before the colon (:) character
    team_members = set()
    lines = transcript.split("\n")
    for line in lines:
        if ":" in line:
            team_member = line.split(":")[0].strip()
            team_members.add(team_member)

    logger.info("Team members identified successfully.")

    return team_members

# A function to extract the JIRA tickets mentioned in the transcript
@log_function_call
def extract_jira_tickets(transcript: str, valid_jira_boards: Set[str]) -> Set[str]:
    """
    Extract the JIRA tickets mentioned in the transcript.
    Args:
        transcript: The transcript data.
        valid_jira_boards: The list of valid JIRA board names.
    Returns:
        List[str]: The list of JIRA tickets mentioned in the transcript.
    """

    logger.info("Extracting the JIRA tickets mentioned in the transcript.")

    # Extract JIRA tickets using regex pattern
    valid_jira_boards_regex = "|".join(valid_jira_boards)
    jira_tickets = set(re.findall(rf'\b(?:{valid_jira_boards_regex})-\d+\b', transcript))

    logger.info("JIRA tickets extracted successfully.")

    return jira_tickets