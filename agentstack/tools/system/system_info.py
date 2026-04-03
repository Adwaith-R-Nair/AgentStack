import platform

from agentstack.tools.base_tool import BaseTool


class SystemInfoTool(BaseTool):

    name = "system_info"
    description = "Returns system information like OS and Python version."

    def run(self, input: str) -> str:

        if input == "os":
            return platform.system()

        if input == "python":
            return platform.python_version()

        return f"OS: {platform.system()}, Python: {platform.python_version()}"