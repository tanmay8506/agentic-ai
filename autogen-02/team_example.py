import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.base import TaskResult
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv
import os

load_dotenv()

# Groq client
groq_client = OpenAIChatCompletionClient(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
    model_capabilities={
        "vision": False,
        "function_calling": True,
        "json_output": True,
        "structured_output": False,
    }
)

# ── AGENT 1 — Idea Generator ─────────────────────────────────────────────────
idea_agent = AssistantAgent(
    name="IdeaGenerator",
    model_client=groq_client,
    system_message="""You are a creative idea generator.
When given a topic, generate 3 innovative project ideas.
Be concise — one line per idea."""
)

# ── AGENT 2 — Critic ─────────────────────────────────────────────────────────
critic_agent = AssistantAgent(
    name="Critic",
    model_client=groq_client,
    system_message="""You are a constructive critic.
When given a list of ideas, pick the BEST one and explain why in 2-3 sentences.
Then suggest one improvement to make it even better.
End your response with TERMINATE."""
)

# ── TEAM — RoundRobin: IdeaGenerator goes first, then Critic ─────────────────
team = RoundRobinGroupChat(
    participants=[idea_agent, critic_agent],
    max_turns=2,  # each agent speaks once
)

async def main():
    task = "Generate project ideas for an AI-powered mobile app"
    
    print(f"🎯 Task: {task}\n")
    print("=" * 50)

    async for message in team.run_stream(task=task):
        if isinstance(message, TextMessage):
            print(f"\n🤖 {message.source}:\n{message.content}")
            print("-" * 50)
        elif isinstance(message, TaskResult):
            print(f"\n✅ Done! Stop reason: {message.stop_reason}")

if __name__ == "__main__":
    asyncio.run(main())