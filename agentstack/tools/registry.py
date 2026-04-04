import pkgutil
import importlib
import inspect

from agentstack.tools.base_tool import BaseTool


class ToolRegistry:
    """
    Registry for all tools available to the agent.
    Supports manual registration and auto-discovery.
    """

    def __init__(self):
        self.tools = {}

    def register(self, tool):
        """
        Register a tool instance.
        """
        self.tools[tool.name] = tool

    def get(self, name):
        """
        Retrieve a tool by name.
        """
        return self.tools.get(name)

    def list_tools(self):
        """
        List available tool names.
        """
        return list(self.tools.keys())

    def auto_discover(self):
        """
        Automatically discover tools inside agentstack.tools.
        """

        package = "agentstack.tools"

        for finder, module_name, ispkg in pkgutil.walk_packages(
            importlib.import_module(package).__path__,
            package + "."
        ):

            module = importlib.import_module(module_name)

            for name, obj in inspect.getmembers(module):

                if (
                    inspect.isclass(obj)
                    and issubclass(obj, BaseTool)
                    and obj is not BaseTool
                ):

                    tool_instance = obj()

                    self.register(tool_instance)