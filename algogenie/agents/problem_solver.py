from autogen_agentchat.agents import AssistantAgent
from config.settings import get_model_client

model_client = get_model_client()

def get_problem_solver_agent():
    problem_solver_agent = AssistantAgent(
        name="DSA_Problem_Solver_Agent",
        description="An agent that solves DSA problems",
        model_client=model_client,
        system_message="""
            You are a problem solver agent that is an expert in solving DSA problems.
            You will be working with code executor agent to execute code.
            You will be given a task and you should:
            1. At the beginning of your response specify your plan to solve the task.
            2. Give the code in a Python code block.
            3. Write code in one code block at a time and pass it to code executor agent.
            4. Make sure to include at least 3 test cases.
            5. Explain the code execution result.
            6. Once done, ask the code executor agent to save the code like this:

```python
            code = '''
                print("Hello World")
            '''
            with open('solution.py', 'w') as f:
                f.write(code)
                print("Code saved successfully in solution.py")
```

            In the end once the code is executed successfully, say "STOP" to stop the conversation.
        """
    )
    return problem_solver_agent