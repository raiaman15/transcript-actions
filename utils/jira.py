# Description: This file contains the class and functions to perform operations related to JIRA tickets.

# Importing the required libraries
from jira import JIRA

from utils.logger import log_function_call, logger


# JIRA Client class to interact
class JiraClient:
    """
    A class to interact with the JIRA API.
    """

    def __init__(self, email: str, server:str, token: str):
        """
        Initialize the JIRA client with the server URL and API token.
        Note that this implementation is for Jira Cloud.

        Args:
            email: The JIRA email for Jira Cloud.
            token: The JIRA API token.
        """
        self.email = email
        self.server = server
        self.token = token
        self.jira_client = JIRA(
            server=self.server,
            basic_auth=(self.email, self.token)
        )

    def get_jira_client(self) -> JIRA:
        """
        Get the JIRA client object.
        Returns:
            JIRA: The JIRA client object.
        """
        return self.jira_client


    @log_function_call
    def extract_jira_ticket_details(self, jira_ticket: str):
        """
        Extract the JIRA ticket details using the JIRA API.
        Args:
            jira_ticket: The JIRA ticket number.
        Returns:
            dict: The JIRA ticket details.
        """

        logger.info(f"Extracting JIRA ticket details for ticket: {jira_ticket}")

        # Get the JIRA ticket details using the JIRA API
        jira_issue = self.jira_client.issue(jira_ticket)

        # Extract the required information from the JIRA ticket
        jira_ticket_details = {
            "summary": jira_issue.fields.summary,
            "description": jira_issue.fields.description,
            "comments": "\n".join([comment.body for comment in jira_issue.fields.comment.comments])
        }

        logger.info("JIRA ticket details extracted successfully.")

        return jira_ticket_details

    @log_function_call
    def add_comment_to_jira_ticket(self, jira_ticket: str, comment: str):
        """
        Add a comment to a JIRA ticket using the JIRA API.
        Args:
            jira_ticket: The JIRA ticket number.
            comment: The comment to be added to the JIRA ticket.
        """
        logger.info(f"Adding comment to JIRA ticket: {jira_ticket}")

        # Add the comment to the JIRA ticket using the JIRA API
        self.jira_client.add_comment(jira_ticket, comment)

        logger.info("Comment added to JIRA ticket successfully.")