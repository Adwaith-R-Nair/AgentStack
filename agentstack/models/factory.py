from agentstack.models.mock_model import MockModel
from agentstack.models.claude_model import ClaudeModel


class ModelFactory:
    """
    Factory class to create models based on name.
    """

    MODELS = {
        "mock": MockModel,
        "claude": ClaudeModel,
    }

    @classmethod
    def create(cls, model_name: str):

        if model_name not in cls.MODELS:
            raise ValueError(f"Unknown model: {model_name}")

        return cls.MODELS[model_name]()