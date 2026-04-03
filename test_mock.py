from agentstack.models.mock_model import MockModel

model = MockModel()

response = model.generate("What is 45 * 67?")

print(response)