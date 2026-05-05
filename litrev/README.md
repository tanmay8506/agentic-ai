# LitRev: Autonomous Agentic Literature Reviewer

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![AutoGen](https://img.shields.io/badge/AutoGen-Multi--Agent-orange.svg)
![Groq](https://img.shields.io/badge/Groq-Llama%203-black.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-red.svg)

### Core Purpose
An autonomous multi-agent system designed to streamline academic research. It leverages a two-agent workflow to dynamically query the arXiv database, retrieve relevant academic papers, and synthesize them into structured Markdown literature reviews in real-time.

### Tech Stack
*   **Framework:** Microsoft AutoGen
*   **LLM Engine:** Groq API (Llama-3.3-70b-versatile)
*   **Frontend:** Streamlit
*   **APIs & Libraries:** arXiv API, Asyncio, Pydantic, OpenAI SDK (Groq compatibility)

### System Architecture
The system utilizes a `RoundRobinGroupChat` orchestration model with two specialized agents:
1.  **Search Agent (Tool-Enabled):** Equipped with a custom `arxiv_search` Python function. It receives the user's topic, autonomously crafts an optimized arXiv query, executes the search, and extracts metadata (title, authors, summary, PDF link) into a strict JSON format.
2.  **Summarizer Agent:** An analytical agent configured via a strict system prompt. It parses the raw data retrieved by the Search Agent and synthesizes a professional, literature-review-style report formatted in Markdown.

The backend operates asynchronously, streaming state changes and agent-to-agent dialogue directly to the Streamlit frontend.

### Visual Workflow
```mermaid
graph TD
    A[User Topic] --> B[Search Agent]
    B -->|arxiv_search tool| C[(arXiv Database)]
    C -->|Returns JSON metadata| B
    B -->|Passes context| D[Summarizer Agent]
    D -->|Generates Markdown| E[Streamlit UI]