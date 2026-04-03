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

        # If math question
        if "*" in prompt:
            expression = prompt.split("What is")[-1].strip().replace("?", "")

            return f"""
Thought: I should calculate this.
Action: calculator
Action Input: {expression}
"""

        return """
Thought: I can answer directly.
Final Answer: Hello! This is a mock response.
"""