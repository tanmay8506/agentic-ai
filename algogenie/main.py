import asyncio
from team.dsa_team import get_dsa_team_and_docker
from config.docker_utils import start_docker_container, stop_docker_container
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.base import TaskResult

async def main():
    dsa_team, docker = get_dsa_team_and_docker()
    try:
        await start_docker_container(docker)
        print("✅ Docker container started successfully.")

        task = 'Write a Python function to check if a number is prime.'

        async for message in dsa_team.run_stream(task=task):
            if isinstance(message, TextMessage):
                print('=' * 50)
                print(f"{message.source}: {message.content}")
            elif isinstance(message, TaskResult):
                print(f"\n✅ Done! Stop reason: {message.stop_reason}")

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        await stop_docker_container(docker)

if __name__ == "__main__":
    asyncio.run(main())