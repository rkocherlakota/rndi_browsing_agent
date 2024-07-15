# Importing the necessary libraries
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Define a function to set and retrieve API credentials
def set_credentials() -> str:
    anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    serper_api_key = os.getenv("SERPER_API_KEY")
    return anthropic_api_key, openai_api_key, serper_api_key