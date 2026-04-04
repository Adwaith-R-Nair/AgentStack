import re

from agentstack.tools.registry import ToolRegistry
from agentstack.prompts.template import build_prompt


class Agent:
    """
    Core Agent class that orchestrates reasoning,
    tool usage, and final responses.
    """

    def __init__(self, model, tools=None, max_iterations=5):
        self.model = model
        self.registry = ToolRegistry()

        # auto-discover tools
        self.registry.auto_discover()

        # register additional tools if provided
        if tools:
            for tool in tools:
                self.registry.register(tool)

        self.max_iterations = max_iterations

    def run(self, task: str):
        """
        Execute an agent task.
        """

        context = build_prompt(task, list(self.registry.tools.values())) + "\n"

        for step in range(self.max_iterations):

            response = self.model.generate(context)

            print("\nMODEL RESPONSE:")
            print(response)

            # check if final answer
            if "Final Answer:" in response:
                final = response.split("Final Answer:")[-1].strip()
                return final

            # detect tool action
            action_match = re.search(r"Action:\s*(\w+)", response)
            input_match = re.search(r"Action Input:\s*(.*)", response)

            if action_match and input_match:

                tool_name = action_match.group(1)
                tool_input = input_match.group(1)

                tool = self.registry.get(tool_name)

                if not tool:
                    return f"Tool '{tool_name}' not found."

                observation = tool.run(tool_input)

                print(f"\nTOOL [{tool_name}] RESULT:")
                print(observation)

                context += f"\nObservation: {observation}\n"

            else:
                return "Agent could not determine next action."

        return "Max iterations reached without final answer."