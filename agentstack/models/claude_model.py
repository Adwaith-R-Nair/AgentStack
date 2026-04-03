import os
import anthropic

from .base_model import BaseModel


class ClaudeModel(BaseModel):
    """
    Claude model implementation for AgentStack.
    """

    def __init__(self, model_name="claude-3-sonnet-20240229"):
        self.model_name = model_name

        api_key = os.getenv("ANTHROPIC_API_KEY")

        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set.")

        self.client = anthropic.Anthropic(api_key=api_key)

    def generate(self, prompt: str) -> str:
        """
        Send prompt to Claude and return response.
        """

        response = self.client.messages.create(
            model=self.model_name,
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.content[0].text