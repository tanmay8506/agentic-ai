from __future__ import annotations

import asyncio
from typing import AsyncGenerator, Dict, List

import arxiv
from autogen_core.tools import FunctionTool
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv
import os

load_dotenv()

# ── TOOL ─────────────────────────────────────────────────────────────────────
def arxiv_search(query: str, max_results: int = 5) -> List[Dict]:
    """Search arXiv and return a list of papers."""
    client = arxiv.Client()
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance,
    )
    papers: List[Dict] = []
    for result in client.results(search):
        papers.append({
            "title": result.title,
            "authors": [a.name for a in result.authors],
            "published": result.published.strftime("%Y-%m-%d"),
            "summary": result.summary,
            "pdf_url": result.pdf_url,
        })
    return papers


arxiv_tool = FunctionTool(
    arxiv_search,
    description=(
        "Searches arXiv and returns papers with title, authors, "
        "publication date, abstract, and pdf_url."
    ),
)

# ── GROQ CLIENT ───────────────────────────────────────────────────────────────
def get_groq_client():
    return OpenAIChatCompletionClient(
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

# ── AGENTS & TEAM ─────────────────────────────────────────────────────────────
def build_team() -> RoundRobinGroupChat:
    llm_client = get_groq_client()

    search_agent = AssistantAgent(
        name="search_agent",
        description="Crafts arXiv queries and retrieves candidate papers.",
        system_message=(
            "Given a user topic, think of the best arXiv query and call the "
            "provided tool. Fetch papers and choose the most relevant ones. "
            "Pass them as concise JSON to the summarizer."
        ),
        tools=[arxiv_tool],
        model_client=llm_client,
        reflect_on_tool_use=True,
    )

    summarizer = AssistantAgent(
        name="summarizer",
        description="Produces a short Markdown review from provided papers.",
        system_message=(
            "You are an expert researcher. When you receive the list of papers, "
            "write a literature-review style report in Markdown:\n"
            "1. Start with a 2-3 sentence introduction of the topic.\n"
            "2. One bullet per paper with: title, authors, problem tackled, key contribution.\n"
            "3. Close with a single sentence takeaway.\n"
            "End with TERMINATE."
        ),
        model_client=llm_client,
    )

    return RoundRobinGroupChat(
        participants=[search_agent, summarizer],
        max_turns=2,
    )


# ── ORCHESTRATOR ──────────────────────────────────────────────────────────────
async def run_litrev(
    topic: str,
    num_papers: int = 5,
) -> AsyncGenerator[str, None]:
    """Yield strings representing the conversation in real-time."""
    team = build_team()
    task_prompt = (
        f"Conduct a literature review on **{topic}** "
        f"and return exactly {num_papers} papers."
    )

    async for msg in team.run_stream(task=task_prompt):
        if isinstance(msg, TextMessage):
            yield f"{msg.source}: {msg.content}"


# ── CLI TEST ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    async def _demo():
        async for line in run_litrev("graph neural networks for chemistry", num_papers=3):
            print(line)
            print("-" * 50)

    asyncio.run(_demo())