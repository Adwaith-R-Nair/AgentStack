from .base_model import BaseModel


class MockModel(BaseModel):
    """
    Mock model used for development and testing.

    Instead of calling a real LLM, this model returns
    predefined reasoning outputs.
    """

    def generate(self, prompt: str) -> str:
        """
        Simulate a model response.
        """

        # simple simulation logic
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