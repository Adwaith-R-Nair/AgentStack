import re
from .base_model import BaseModel


class MockModel(BaseModel):
    """
    Mock model used for development and testing.
    Simulates basic reasoning behaviour.
    """

    def generate(self, prompt: str) -> str:

        # If observation already exists, produce final answer
        if "Observation:" in prompt:
            observation = prompt.split("Observation:")[-1].strip()

            return f"""
Thought: I now know the answer.
Final Answer: {observation}
"""

        # detect simple math expression
        math_match = re.search(r"(\d+\s*[\+\-\*\/]\s*\d+)", prompt)

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