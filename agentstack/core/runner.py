import typer
import subprocess

from agentstack.models.mock_model import MockModel
from agentstack.tools.math.calculator import CalculatorTool
from agentstack.core.agent import Agent
from agentstack.tools.registry import ToolRegistry

app = typer.Typer()


@app.command()
def chat():
    """
    Start interactive AgentStack chat session.
    """

    model = MockModel()
    calculator = CalculatorTool()

    agent = Agent(
        model=model,
        tools=[calculator]
    )

    print("\nAgentStack Chat")
    print("Type 'exit' to quit.\n")

    while True:

        user_input = input("User > ")

        if user_input.lower() in ["exit", "quit"]:
            break

        result = agent.run(user_input)

        print("\nAgent >", result)
        print()


@app.command()
def version():
    """
    Show AgentStack version.
    """

    print("AgentStack v0.1.0")

@app.command()
def run(script: str):
    """
    Run an AgentStack example script.
    """

    print(f"\nRunning script: {script}\n")

    subprocess.run(["python", script])

@app.command()
def tools():
    """
    List all available tools.
    """

    registry = ToolRegistry()

    registry.auto_discover()

    print("\nAvailable Tools\n")

    for tool_name in registry.list_tools():
        tool = registry.get(tool_name)

        print(f"{tool.name}  →  {tool.description}")

    print()

if __name__ == "__main__":
    app()