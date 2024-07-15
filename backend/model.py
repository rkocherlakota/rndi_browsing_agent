# Importing the necessary libraries
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI

from credentials import set_credentials

# Set credentials
anthropic_api_key, openai_api_key, serper_api_key = set_credentials()

# Initializing the model
ChatAnthropic.api_key = anthropic_api_key

# Define the Claude model from Anthropic
claude_model = ChatAnthropic(model_name="claude-3-haiku-20240307", max_tokens=4096)

# Define the embedding model for generating text embeddings
embed_model = embed_model = "text-embedding-3-small" 

# Define the OpenAI model
# openai_model = ChatOpenAI(model_name = "gpt-3.5-turbo", temperature=0)
openai_model = ChatOpenAI(model_name = "gpt-4-turbo", temperature=0)