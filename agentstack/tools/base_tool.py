class BaseTool:
    """
    Base class for all tools in AgentStack.
    """

    name = ""
    description = ""

    def run(self, input: str) -> str:
        """
        Execute the tool.

        Args:
            input (str): Input provided to the tool

        Returns:
            str: Result of the tool execution
        """
        raise NotImplementedError("Tools must implement the run method.")