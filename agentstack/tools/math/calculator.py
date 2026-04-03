from agentstack.tools.base_tool import BaseTool


class CalculatorTool(BaseTool):
    """
    Tool for performing mathematical calculations.
    """

    name = "calculator"
    description = "Performs basic math calculations."

    def run(self, input: str) -> str:
        try:
            result = eval(input)
            return str(result)
        except Exception as e:
            return f"Error: {str(e)}"