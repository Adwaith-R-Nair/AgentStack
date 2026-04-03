from agentstack.models.mock_model import MockModel
from agentstack.tools.calculator import CalculatorTool
from agentstack.core.agent import Agent


agent = Agent(
    model=MockModel(),
    tools=[CalculatorTool()]
)

result = agent.run("What is 45 * 67?")

print("\nFINAL RESULT:")
print(result)