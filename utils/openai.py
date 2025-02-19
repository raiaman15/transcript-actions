# Description: This file contains the utility functions to interact with the OpenAI API.

# Importing the required libraries
from openai import OpenAI

from utils.logger import log_function_call, logger

# OpenAI Client class to interact with the OpenAI API
class OpenAIClient:
    """
    A class to interact with the OpenAI API.
    """

    def __init__(self):
        """
        Initialize the OpenAI client with the API key.
        Note that the API key should be set as an environment variable.
        """
        self.client = OpenAI()

    @log_function_call
    def generate_response(self, user_context: str, assistant_confirmation: str, user_prompt: str):
        """
        Generate a response using the OpenAI API.
        Args:
            user_context: The context provided by the user.
            assistant_confirmation: The confirmation from the assistant.
            user_prompt: The prompt provided by the user.
        Returns:
            str: The generated response from the model.
        """
        logger.info("Generating response using OpenAI API.")

        # Call the OpenAI API to generate a response
        completion = self.client.chat.completions.create(
            model="o1-mini",
            messages=[
                {
                    "role": "user",
                    "content": user_context
                },
                {
                    "role": "assistant",
                    "content": assistant_confirmation
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ]
        )

        # Extract the generated text from the response
        generated_text = completion.choices[0].message.content

        logger.info("Response generated successfully.")

        return generated_text