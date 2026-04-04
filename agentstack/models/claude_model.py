from agentstack.models.base_model import BaseModel


class ClaudeModel(BaseModel):
    """
    Placeholder Claude model implementation.

    This will later connect to the Anthropic Claude API.
    """

    def generate(self, prompt: str) -> str:
        raise NotImplementedError(
            "ClaudeModel is not implemented yet. Use --model mock for now."
        )