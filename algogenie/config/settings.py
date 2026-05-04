import os
from dotenv import load_dotenv
from autogen_ext.models.openai import OpenAIChatCompletionClient
from config.constant import MODEL

load_dotenv()

def get_model_client():
    model_client = OpenAIChatCompletionClient(
        model=MODEL,
        api_key=os.getenv('GROQ_API_KEY'),
        base_url="https://api.groq.com/openai/v1",
        model_capabilities={
            "vision": False,
            "function_calling": True,
            "json_output": True,
            "structured_output": False,
        }
    )
    return model_client