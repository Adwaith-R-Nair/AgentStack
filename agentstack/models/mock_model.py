import re
from agentstack.models.base_model import BaseModel


class MockModel(BaseModel):
    """
    Mock LLM used for testing AgentStack without real APIs.
    """

    def generate(self, prompt: str) -> str:

        # Find real observation values like "Observation: 242"
        observation_matches = re.findall(r"Observation:\s*(\d+)", prompt)

        if observation_matches:
            last_obs = observation_matches[-1]

            return f"""
Thought: I now know the answer.
Final Answer: {last_obs}
"""

        # Extract user task
        task_match = re.search(r"User Task:\s*(.*)", prompt)

        if task_match:
            task = task_match.group(1)

            math_match = re.search(r"(\d+\s*[\+\-\*\/]\s*\d+)", task)

            if math_match:
                expression = math_match.group(1)

                return f"""
Thought: I should calculate this.
Action: calculator
Action Input: {expression}
"""

        return """
Thought: I can answer directly.
Final Answer: Hello! This is a mock response.
"""