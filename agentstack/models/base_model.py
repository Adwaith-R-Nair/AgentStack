class BaseModel:
    """
    Base class for all language models supported by AgentStack.

    Every model implementation must inherit from this class
    and implement the generate() method.
    """

    def generate(self, prompt: str) -> str:
        """
        Generate a response from the language model.

        Args:
            prompt (str): The input prompt sent to the model.

        Returns:
            str: Model response.
        """
        raise NotImplementedError("Models must implement the generate method.")