# Transcript Actions
This project aims to take actions on the basis of a meeting transcript. 

## Supported Actions
### Jira Ticket Update based on the transcript
A comment is added to the Jira ticket with the transcript discussion around that ticket.
The Jira ticket summary, description and previous comments are used as context to avoid duplication of information.
The current implementation supports the Jira Cloud.

For the Jira Server, the implementation can be done by changing the `JiraClient` class in the `jira_client.py` file along with the `.env` variables.

## Upcoming actions
### Google Task Creation based on the transcript
A Google Task is created with the transcript discussion around that task.

### Google Calendar Event Creation based on the transcript
A Google Calendar event is created with the transcript discussion around that event.

## How to use
1. Clone the repository
2. Install the required packages using `pip install -r requirements.txt`
3. Create a `.env` file in the root directory with the following variables:
    - `JIRA_EMAIL`: The Jira Cloud email
    - `JIRA_SERVER`: The Jira Cloud server URL
    - `JIRA_TOKEN`: The Jira Cloud API token
    - `OPENAI_API_KEY`: The OpenAI API key
   You may refer to the `.env.example` file for reference.
- Source the `.env` file using `source .env`
- Run the `main.py` file with the transcript file path as an argument. For example, `python main.py transcript.txt`
- The script will read the transcript file and update the Jira tickets accordingly upon user confirmation.

## Tips to achieve the best results
- Always mention the Jira ticket number before starting the discussion about that ticket.
- Discuss one Jira ticket at a time to avoid confusion.
- The shorter the meeting, the shorter is the transcript, the better the results.
