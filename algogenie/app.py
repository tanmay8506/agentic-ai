import streamlit as st
from team.dsa_team import get_dsa_team_and_docker
from config.docker_utils import start_docker_container, stop_docker_container
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.base import TaskResult
import asyncio

st.set_page_config(page_title="AlgoGenie", page_icon="🧞")
st.title("🧞 AlgoGenie — DSA Problem Solver")
st.write("Enter a DSA problem and I'll write, execute and verify the solution using AI agents!")

task = st.text_input(
    "Enter your DSA problem:",
    value='Write a function to add two numbers'
)

async def run(team, docker, task):
    try:
        await start_docker_container(docker)
        async for message in team.run_stream(task=task):
            if isinstance(message, TextMessage):
                msg = f"{message.source} : {message.content}"
                yield msg
            elif isinstance(message, TaskResult):
                msg = f"Stop Reason: {message.stop_reason}"
                yield msg
    except Exception as e:
        yield f"Error: {e}"
    finally:
        await stop_docker_container(docker)

if st.button("🚀 Solve"):
    st.write("Running the task...")
    team, docker = get_dsa_team_and_docker()

    async def collect_messages():
        async for msg in run(team, docker, task):
            if isinstance(msg, str):
                if msg.startswith("user"):
                    with st.chat_message('user', avatar='👤'):
                        st.markdown(msg)
                elif msg.startswith('DSA_Problem_Solver_Agent'):
                    with st.chat_message('assistant', avatar='🧑‍💻'):
                        st.markdown(msg)
                elif msg.startswith('CodeExecutorAgent'):
                    with st.chat_message('assistant', avatar='🤖'):
                        st.markdown(msg)
                else:
                    with st.chat_message('assistant', avatar='✅'):
                        st.markdown(msg)

    try:
        asyncio.run(collect_messages())
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(collect_messages())