# Getting Started with AgentStack

This guide will help you install **AgentStack** and run your first AI agent.

AgentStack is a lightweight framework for building AI agents with reasoning loops, tools, and memory.

---

# 1. Prerequisites

Before installing AgentStack, ensure you have the following installed:

* Python 3.9 or higher
* pip (Python package manager)

You will also need an API key for Claude.

---

# 2. Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/agentstack.git
cd agentstack
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# 3. Configure API Key

Set your Claude API key as an environment variable.

Linux / macOS:

```bash
export ANTHROPIC_API_KEY=your_api_key_here
```

Windows:

```bash
set ANTHROPIC_API_KEY=your_api_key_here
```

---

# 4. Create Your First Agent

Create a file called:

```
my_agent.py
```

Example agent:

```python
from agentstack import Agent
from agentstack.tools import calculator

agent = Agent(
    model="claude",
    tools=[calculator]
)

result = agent.run("What is 45 * 67?")

print(result)
```

---

# 5. Run the Agent

Execute the script:

```bash
python my_agent.py
```

Example output:

```
Thought: I should calculate the result.
Action: calculator
Observation: 3015

Final Answer: 3015
```

---

# 6. Using the CLI

AgentStack also provides a CLI interface.

Start interactive mode:

```bash
agentstack chat
```

Run an example agent:

```bash
agentstack run examples/math_agent.py
```

---

# 7. Next Steps

After running your first agent, explore:

* Creating custom tools
* Extending the agent engine
* Adding new models

You can also check the following documents:

* `docs/architecture.md`
* `docs/roadmap.md`
* `docs/user-stories.md`

---

# Maintainers

Maintained by **Adwaith R Nair** and **AgentStack Contributors**.
