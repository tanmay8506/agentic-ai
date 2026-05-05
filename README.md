I'll strip the citations and the technical fluff. Here is the clean, high-impact README.md for AlgoGenie.

Copy this into a new file named README.md inside your algogenie folder.

AlgoGenie: Autonomous DSA Problem Solver
Core Purpose
AlgoGenie is an agentic AI system designed to solve Data Structures and Algorithms (DSA) problems. Unlike standard LLMs, it autonomously writes, executes, and verifies code within a secure, isolated Docker environment to ensure the logic is bug-free and efficient.

Tech Stack
Framework: Microsoft AutoGen (AgentChat)

Execution Environment: Docker (DockerCommandLineCodeExecutor)

LLM Engine: Groq API (Llama-3.3-70b-versatile)

Frontend: Streamlit

Orchestration: Round Robin Group Chat with Text-Mention Termination

System Architecture
The system employs a collaborative two-agent loop:

DSA Problem Solver Agent: Analyzes the task, creates a step-by-step logic plan, and writes the Python implementation with integrated test cases.

Code Executor Agent: Manages the runtime. It spins up an isolated Docker container, executes the code, and feeds the output or error logs back to the solver for iterative debugging.

Visual Workflow
Code snippet
graph LR
    User[User Input] --> Team[AlgoGenie Team]
    subgraph Sandbox [Isolated Docker Environment]
    Executor[Code Executor Agent]
    end
    Team --> Solver[DSA Solver Agent]
    Solver -->|Generates Code| Executor
    Executor -->|Returns Result/Error| Solver
    Solver -->|Verifies/Fixes| Team
    Team -->|Final Verified Solution| User
Installation & Setup
Prerequisites: Ensure Docker Desktop is installed and running.

Clone and Install:

Bash
git clone https://github.com/tanmay8506/algogenie-autonomous-sandbox.git
cd algogenie-autonomous-sandbox
pip install -r requirements.txt
Configure API:
Add your GROQ_API_KEY to a .env file.

Launch:

Bash
streamlit run app.py
💼 Resume Bullet Points
AlgoGenie — Autonomous DSA Solution Engine | Python, AutoGen, Docker, Streamlit, Groq API

Engineered a multi-agent system utilizing DockerCommandLineCodeExecutor to autonomously solve and verify DSA problems in a secured, isolated sandbox.

Implemented a RoundRobinGroupChat orchestration logic allowing for iterative self-debugging between a Solver Agent and an Execution Agent.

Architected a real-time Streamlit dashboard that streams agent dialogue and execution logs, leveraging Llama-3.3 via Groq for high-speed reasoning.
