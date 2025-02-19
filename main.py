# The intent of the project is the following:
# 1. Lists all transcripts in the "transcripts" directory and asks the user to select a standup meeting transcript.
# 2. Reads the selected standup meeting transcript.
# 3. Cleans the transcript:
#    -  Standardize the JIRA ticket numbers mentioned in the transcript.
# 4. Identifies the team members mentioned in the transcript.
# 5. Parses the transcript and extract the following information:
#    -  List of all JIRA tickets mentioned in the transcript.
# 6. For each JIRA ticket mentioned in the transcript, the following steps are performed:
#    -  Pull the JIRA ticket details from the JIRA API to have a better understanding of the tickets.
#    -  Extract the following information from the JIRA ticket:
#       -  Ticket summary
#       -  Ticket description
#       -  Ticket comments
#    -  Using ticket summary, description, and comments, extract any new information from the transcript related to the ticket using LLM (OpenAI API).
#    -  Prepare a comment to be added to the JIRA ticket with the new information extracted from the transcript:
#       -  The comment should be formatted in a specific way.
#       -  The comment should include the name of the team member who mentioned the ticket in the transcript.
#       -  The comment should include the new information extracted from the transcript.
#    -  Display the prepared comment to the user.
#    -  Seek user confirmation to add the comment to the JIRA ticket.
#    -  If the user confirms, add the comment to the JIRA ticket.
#    -  If the user denies, continue to the next JIRA ticket.

# Importing the required libraries and modules
import os

from utils import (
    clean_transcript,
    extract_jira_tickets,
    extract_team_members,
    JiraClient,
    OpenAIClient,
    read_transcript
)

# Setting up the logger
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Setting up constants
TRANSCRIPT_FILE_PATH = os.path.join(os.path.dirname(__file__), "transcripts", "19-02-2024.txt")
VALID_JIRA_BOARDS = {"OSC", "ML"}

# Setting up environment variables
JIRA_EMAIL = os.environ.get("JIRA_EMAIL")
if not JIRA_EMAIL:
    raise EnvironmentError("The JIRA_EMAIL environment variable is not set. Please set it to the JIRA_EMAIL of JIRA Cloud.")

JIRA_SERVER = os.environ.get("JIRA_SERVER")
if not JIRA_SERVER:
    raise EnvironmentError("The JIRA_SERVER environment variable is not set. Please set it to the JIRA server URL.")

JIRA_TOKEN = os.environ.get("JIRA_TOKEN")
if not JIRA_TOKEN:
    raise EnvironmentError("The JIRA_TOKEN environment variable is not set. Please set it to your JIRA API token.")

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise EnvironmentError("The OPENAI_API_KEY environment variable is not set. Please set it to your OpenAI API key.")

# Actual code
if __name__ == "__main__":
    # Initialize the clients
    jira_client = JiraClient(email=JIRA_EMAIL, server=JIRA_SERVER, token=JIRA_TOKEN)
    openai_client = OpenAIClient()  # Initialize with the OpenAI API key

    # Listing all transcripts in the "transcripts" directory
    transcripts = os.listdir(os.path.join(os.path.dirname(__file__), "transcripts"))
    logger.info("List of Standup Meeting Transcripts:")
    for i, transcript in enumerate(transcripts, 1):
        logger.info(f"{i}. {transcript}")

    # Asking the user to select a standup meeting transcript
    transcript_number = int(input("Enter the number of the standup meeting transcript you want to select: "))
    TRANSCRIPT_FILE_PATH = os.path.join(os.path.dirname(__file__), "transcripts", transcripts[transcript_number - 1])

    # Reading the transcript file
    transcript = read_transcript(TRANSCRIPT_FILE_PATH)

    # Cleaning the transcript data
    # Standardizing the JIRA ticket numbers mentioned in the transcript as per the JIRA board names.
    cleaned_transcript = clean_transcript(transcript, VALID_JIRA_BOARDS)
    logger.debug(f"Cleaned Transcript: {cleaned_transcript}")

    # Identifying the team members mentioned in the transcript.
    team_members = list(sorted(extract_team_members(cleaned_transcript)))
    logger.debug(f"Team Members: {team_members}")

    # Parsing the transcript and extracting the JIRA tickets mentioned in the transcript.
    jira_tickets = list(sorted(extract_jira_tickets(cleaned_transcript, VALID_JIRA_BOARDS)))
    logger.debug(f"JIRA Tickets: {jira_tickets}")

    # For each JIRA ticket mentioned in the transcript:
    for jira_ticket in jira_tickets:
        # Extracting the JIRA ticket details using the JIRA API.
        jira_ticket_details= jira_client.extract_jira_ticket_details(jira_ticket)

        # Displaying the extracted JIRA ticket details.
        logger.debug(f"JIRA Ticket Details for {jira_ticket}: {jira_ticket_details}")

        # Extracting new information from the transcript related to the ticket using LLM (OpenAI API).
        llm_user_context = (
            f"You are a support agent working on a JIRA ticket. "
            f"The summary of the ticket is as follows: {jira_ticket_details['summary']}. "
            f"The description of the ticket is as follows: {jira_ticket_details['description']}. "
            f"The comments on the ticket are as follows: {jira_ticket_details['comments']}. "
            f"A standup meeting took place recently where this ticket might have been discussed. "
            f"You need to find out if there is any new information related to this ticket from the standup meeting transcript which will be provided to you. "
        )
        llm_assistant_confirmation = (
            "Okay, I will look for new information related to this ticket in the standup meeting transcript. "
            "If I find any new information, I will provide you with a concise summary to be added as a comment to the JIRA ticket. "
            "If there is no new information, I will respond 'NO NEW INFO'."
        )
        llm_user_prompt = (
            f"The standup meeting transcript is as follows: {cleaned_transcript} \n\n"
            f"The standup meeting transcript may contain information about other JIRA tickets as well, which you can ignore. "
            f"If there is significant new information, provide the  new information related to this ticket in concise form. "
            f"Please make sure that the information similar to what you extracted is not already present anywhere in JIRA ticket (summary, description or comments). "
            f"If there is no significant new information related to this ticket, respond 'NO NEW INFO'."
        )
        new_information = openai_client.generate_response(
            user_context=llm_user_context,
            assistant_confirmation=llm_assistant_confirmation,
            user_prompt=llm_user_prompt
        )

        # Skip adding comment, if no new information is extracted
        if new_information == "NO NEW INFO":
            logger.info(f"No new information extracted for JIRA ticket: {jira_ticket}")
            continue

        # Preparing a comment to be added to the JIRA ticket with the new information extracted from the transcript.
        comment = f"Stand-up update: \n{new_information}"

        # Displaying the prepared comment to the user.
        logger.info(
            f"\nPLEASE REVIEW:"
            f"\nPrepared Comment for {jira_ticket}: "
            f"\n{comment}"
        )

        # Seeking user confirmation to add the comment to the JIRA ticket.
        user_confirmation = input("Do you want to add this comment to the JIRA ticket? (y/n): ")

        # If the user confirms, adding the comment to the JIRA ticket.
        if user_confirmation.lower() == "y":
            jira_client.add_comment_to_jira_ticket(jira_ticket, comment)
            logger.info(f"Comment added successfully to JIRA ticket: {jira_ticket}")

        # If the user denies, continuing to the next JIRA ticket.
        else:
            logger.info(f"Skipping adding comment to JIRA ticket: {jira_ticket}")
            continue
