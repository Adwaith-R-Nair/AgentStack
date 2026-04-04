class ConversationMemory:
    """
    Stores conversation history between the user and the agent.
    """

    def __init__(self):
        self.history = []

    def add_user_message(self, message: str):
        self.history.append(f"User: {message}")

    def add_agent_message(self, message: str):
        self.history.append(f"Agent: {message}")

    def get_context(self) -> str:
        """
        Returns conversation history as a formatted string.
        """

        if not self.history:
            return ""

        return "\n".join(self.history)

    def clear(self):
        """
        Clears conversation history.
        """
        self.history = []