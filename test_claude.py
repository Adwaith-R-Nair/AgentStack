from agentstack.models.claude_model import ClaudeModel

model = ClaudeModel()

response = model.generate("Say hello in one sentence.")

print(response)