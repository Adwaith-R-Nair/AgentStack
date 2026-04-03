from agentstack.tools.math.calculator import CalculatorTool
from agentstack.tools.registry import ToolRegistry

registry = ToolRegistry()

calculator = CalculatorTool()

registry.register(calculator)

tool = registry.get("calculator")

result = tool.run("45 * 67")

print(result)