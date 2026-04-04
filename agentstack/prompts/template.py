def build_prompt(task: str, tools: list) -> str:
    """
    Build the structured prompt for the agent.
    """

    tool_descriptions = "\n".join(
        [f"{tool.name} — {tool.description}" for tool in tools]
    )

    prompt = f"""
You are an AI agent that can use tools to solve tasks.

Available Tools:
{tool_descriptions}

Use the following format:

Thought:
Action:
Action Input:
Observation:
Final Answer:

User Task:
{task}
"""

    return prompt.strip()