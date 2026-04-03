from agentstack.models.mock_model import MockModel
from agentstack.tools.calculator import CalculatorTool
from agentstack.core.agent import Agent


def main():

    model = MockModel()

    calculator = CalculatorTool()

    agent = Agent(
        model=model,
        tools=[calculator]
    )

    result = agent.run("What is 45 * 67?")

    print("\nResult:", result)


if __name__ == "__main__":
    main()