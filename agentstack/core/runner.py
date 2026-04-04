import typer
import subprocess

from agentstack.core.agent import Agent
from agentstack.tools.registry import ToolRegistry
from agentstack.models.factory import ModelFactory

app = typer.Typer()


@app.command()
def chat(
    model: str = typer.Option(
        "mock",
        "--model",
        "-m",
        help="Model to use (mock or claude)"
    )
):
    """
    Start interactive AgentStack chat session.
    """

    selected_model = ModelFactory.create(model)

    agent = Agent(
        model=selected_model
    )

    print("\nAgentStack Chat")
    print(f"Using model: {model}")
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