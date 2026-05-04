import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.tools import FunctionTool
from dotenv import load_dotenv
import os

load_dotenv()

# Groq is OpenAI-compatible — we just point to Groq's base URL
groq_client = OpenAIChatCompletionClient(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
    model_capabilities={
        "vision": False,
        "function_calling": True,
        "json_output": True,
    }
)

# Define a custom tool
def reverse_string(text: str) -> str:
    """Reverse the given text."""
    return text[::-1]

reverse_tool = FunctionTool(reverse_string, description="A tool to reverse a string")

# Create the agent
agent = AssistantAgent(
    name="ReverseAgent",
    model_client=groq_client,
    system_message="You are a helpful assistant that can reverse text using the reverse_string tool.",
    tools=[reverse_tool]
)

task = "Reverse the text 'Hello, how are you?'"

async def main():
    result = await agent.run(task=task)
    
    # Print each message cleanly
    for message in result.messages:
        print(f"\n{'='*40}")
        print(f"📌 Source: {message.source}")
        print(f"💬 Content: {message.content}")

if __name__ == "__main__":
    asyncio.run(main())

