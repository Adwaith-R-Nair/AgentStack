from agentstack.models.mock_model import MockModel
from agentstack.tools.math.calculator import CalculatorTool
from agentstack.core.agent import Agent


def main():

    model = MockModel()

    agent = Agent(
        model=model
    )

    result = agent.run("What is 45 * 67?")

    print("\nResult:", result)


if __name__ == "__main__":
    main()