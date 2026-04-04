# AgentStack — Bug Tracker

This document tracks bugs, errors, and unexpected behaviors discovered during the development of **AgentStack**.

Maintaining a structured bug log helps improve debugging efficiency, documentation quality, and overall framework stability.

Each bug entry should include:

* Bug ID
* Description
* File affected
* Code snippet
* Cause
* Solution
* Status

---

# Bug Tracking Table

| Bug ID | Description | File | Code Snippet | Cause | Solution | Status |
| ------ | ----------- | ---- | ------------ | ----- | -------- | ------ |
| BUG-001 | MockModel kept repeating tool actions and never produced a final answer | `agentstack/models/mock_model.py` | — | Mock model did not detect Observation context | Added logic to detect "Observation:" and return Final Answer | Fixed |
| BUG-002 | `agentstack.egg-info` folder was accidentally committed | `.gitignore` | — | `pip install -e .` generates egg-info metadata that was not excluded | Added `*.egg-info` to `.gitignore` and removed folder from git tracking | Resolved |
| BUG-003 | Tools previously required manual registration | `agentstack/tools/registry.py` | — | `ToolRegistry` lacked a dynamic discovery mechanism | Implemented `auto_discover()` using `pkgutil` and `importlib` | Resolved |
| BUG-004 | No CLI visibility for available tools | `agentstack/cli/main.py` | — | `ToolRegistry` auto-discovery worked internally but tools could not be listed via CLI | Added `agentstack tools` CLI command to list all discovered tools | Resolved |
| BUG-005 | `file_reader` tool did not appear in `agentstack tools` | `agentstack/tools/file_reader.py` | — | `file_reader.py` existed but contained no `BaseTool` implementation | Implemented `FileReaderTool` class inheriting from `BaseTool` | Resolved |
| BUG-006 | `agentstack chat --model mock` failed with "No such option: --model" | `agentstack/cli/main.py` | — | `chat()` CLI command did not define a Typer option for `model` | Added `model: str = typer.Option("mock", "--model", "-m")` to `chat()` | Resolved |
| BUG-007 | `ImportError` when loading `ModelFactory` due to empty `claude_model.py` | `agentstack/models/claude_model.py` | — | `ClaudeModel` class was not implemented but `ModelFactory` attempted to import it | Added placeholder `ClaudeModel` class inheriting from `BaseModel` | Resolved |
| BUG-008 | Invalid import `from pyexpat import model` appeared in `runner.py` | `agentstack/core/runner.py` | — | Accidental IDE auto-import | Removed incorrect import and cleaned CLI imports | Resolved |
| BUG-009 | Agent prompts lacked structured context for reasoning and tool usage | `agentstack/prompts/template.py` | — | Agent used a simple "User Task" prompt instead of a structured agent prompt | Implemented Prompt Template System using `build_prompt()` | Resolved |
| BUG-010 | MockModel produced incorrect outputs after introducing structured prompts | `agentstack/models/mock_model.py` | — | MockModel expected simple prompts and failed to parse structured agent prompts | Updated MockModel to extract the user task using regex | Resolved |
| BUG-011 | MockModel incorrectly detected Observation due to prompt template instructions | `agentstack/models/mock_model.py` | — | Observation detection logic matched the instruction section of the prompt | Updated regex logic to detect only actual observation values returned by tools | Resolved |
| BUG-012 | User messages were not stored in conversation memory | `agentstack/core/agent.py` | — | `add_user_message()` was referenced but never called | Updated `agent.py` to call `self.memory.add_user_message(task)` | Resolved |
| BUG-013 | `WebSearchTool` returned no results and produced a runtime warning | `agentstack/tools/web_search.py`, `requirements.txt` | — | `duckduckgo_search` package was deprecated and replaced by `ddgs` | Updated `WebSearchTool` and `requirements.txt` to use `ddgs` | Resolved |

---

# Bug Entry Format

When a bug is discovered, add a detailed entry below.

---

## Bug ID: BUG-001

**Description**

MockModel kept repeating tool actions and never produced a final answer.

---

**File**

```
agentstack/models/mock_model.py
```

---

**Code Snippet**

The fix — detecting `"Observation:"` and returning a Final Answer:

```python
# If observation already exists, produce final answer
if "Observation:" in prompt:
    observation = prompt.split("Observation:")[-1].strip()

    return f"""
Thought: I now know the answer.
Final Answer: {observation}
"""
```

---

**Cause**

Mock model did not detect Observation context. The model was not checking whether an "Observation:" block was present in the conversation, so it kept invoking tools in a loop instead of concluding with a final answer.

---

**Solution**

Added logic to detect `"Observation:"` in the response context and return a Final Answer when it is present, breaking the infinite tool-action loop.

---

**Status**

```
Status: Fixed
```

---

## Bug ID: BUG-002

**Description**

`agentstack.egg-info` folder was accidentally committed to the repository.

---

**File**

```
.gitignore
```

---

**Code Snippet**

— *(not applicable — git/config issue, no code snippet)*

---

**Cause**

Running `pip install -e .` generates an `agentstack.egg-info` metadata directory locally. This folder was not listed in `.gitignore` and was inadvertently staged and committed.

---

**Solution**

Added `*.egg-info` to `.gitignore` to prevent future commits, then removed the folder from git tracking without deleting it locally:

```bash
echo "*.egg-info/" >> .gitignore
git rm -r --cached agentstack.egg-info
git commit -m "fix: remove egg-info from tracking, update .gitignore"
```

---

**Status**

```
Status: Resolved
```

---

## Bug ID: BUG-003

**Description**

Tools previously required manual registration in `ToolRegistry`. Every new tool had to be explicitly imported and registered, making the process error-prone and not scalable.

---

**File**

```
agentstack/tools/registry.py
```

---

**Code Snippet**

The fix — `auto_discover()` using `pkgutil` and `importlib` to automatically find and register all tools:

```python
import pkgutil
import importlib
import agentstack.tools as tools_pkg

def auto_discover(self):
    for finder, name, ispkg in pkgutil.iter_modules(tools_pkg.__path__, tools_pkg.__name__ + "."):
        module = importlib.import_module(name)
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if callable(attr) and hasattr(attr, "is_tool"):
                self.register(attr)
```

---

**Cause**

`ToolRegistry` had no dynamic discovery mechanism. Tools had to be manually imported and registered, meaning any newly added tool module would be silently ignored unless explicitly wired up.

---

**Solution**

Implemented `auto_discover()` in `ToolRegistry` using `pkgutil.iter_modules()` to walk the `agentstack/tools/` package and `importlib.import_module()` to load each module, automatically registering any callable marked with `is_tool`.

---

**Status**

```
Status: Resolved
```

---

## Bug ID: BUG-004

**Description**

No CLI visibility for available tools. Even though `ToolRegistry` was successfully auto-discovering tools internally, there was no way to inspect which tools were loaded without digging into the source code.

---

**File**

```
agentstack/cli/main.py
```

---

**Code Snippet**

The fix — `agentstack tools` subcommand that prints all discovered tools:

```python
@cli.command()
def tools():
    """List all available tools discovered by ToolRegistry."""
    registry = ToolRegistry()
    registry.auto_discover()
    discovered = registry.list_tools()

    if not discovered:
        click.echo("No tools found.")
        return

    click.echo("Available tools:")
    for tool in discovered:
        click.echo(f"  - {tool.name}: {tool.description}")
```

---

**Cause**

`ToolRegistry.auto_discover()` populated the registry correctly, but no CLI surface exposed the registry's contents. Developers had no way to verify which tools were loaded at runtime without adding debug print statements manually.

---

**Solution**

Added an `agentstack tools` subcommand to the CLI that calls `auto_discover()` and prints all registered tools with their names and descriptions.

---

**Status**

```
Status: Resolved
```

---

## Bug ID: BUG-005

**Description**

`file_reader` tool did not appear in `agentstack tools`. Despite the file existing in the tools directory, it was silently skipped during auto-discovery and never showed up in the CLI listing.

---

**File**

```
agentstack/tools/file_reader.py
```

---

**Code Snippet**

The fix — `FileReaderTool` properly inheriting from `BaseTool`:

```python
from agentstack.tools.base_tool import BaseTool

class FileReaderTool(BaseTool):
    name: str = "file_reader"
    description: str = "Reads the contents of a file at a given path."

    def run(self, path: str) -> str:
        with open(path, "r") as f:
            return f.read()
```

---

**Cause**

`file_reader.py` existed in the tools directory but contained no class inheriting from `BaseTool`. Since `auto_discover()` scans for `BaseTool` subclasses, the file was loaded but nothing in it matched the discovery criteria, so it was silently ignored.

---

**Solution**

Implemented `FileReaderTool` as a proper `BaseTool` subclass with `name`, `description`, and a `run()` method, making it visible to `auto_discover()` and therefore listable via `agentstack tools`.

---

**Status**

```
Status: Resolved
```

---

## Bug ID: BUG-006

**Description**

`agentstack chat --model mock` failed with `"No such option: --model"`. The `--model` flag was not recognised by the CLI, making it impossible to select a model at runtime.

---

**File**

```
agentstack/cli/main.py
```

---

**Code Snippet**

The fix — adding a Typer `Option` for `model` in the `chat()` command:

```python
@app.command()
def chat(
    model: str = typer.Option("mock", "--model", "-m", help="Model to use for the agent.")
):
    """Start an interactive chat session with the agent."""
    agent = Agent(model=model)
    agent.run()
```

---

**Cause**

The `chat()` CLI command was defined without any Typer options, so passing `--model` raised an immediate `"No such option"` error before the agent could be initialised.

---

**Solution**

Updated the `chat()` function signature to include `model: str = typer.Option("mock", "--model", "-m")`, defaulting to the mock model while allowing the caller to override it.

---

**Status**

```
Status: Resolved
```

---

## Bug ID: BUG-007

**Description**

An `ImportError` occurred when loading `ModelFactory` due to an empty `claude_model.py`. The error prevented the entire models module from loading correctly.

---

**File**

```
agentstack/models/claude_model.py
```

---

**Code Snippet**

The fix — placeholder `ClaudeModel` inheriting from `BaseModel`:

```python
from agentstack.models.base_model import BaseModel

class ClaudeModel(BaseModel):
    """
    Placeholder ClaudeModel. Full Anthropic API integration to be implemented.
    """

    def generate(self, prompt: str) -> str:
        raise NotImplementedError("ClaudeModel is not yet implemented.")
```

---

**Cause**

`claude_model.py` was an empty file. `ModelFactory` attempted to import `ClaudeModel` from it at startup, causing an `ImportError` since the class did not exist.

---

**Solution**

Added a minimal `ClaudeModel` placeholder class inheriting from `BaseModel` with a `generate()` method that raises `NotImplementedError`, satisfying the import and deferring full implementation.

---

**Status**

```
Status: Resolved
```

---

## Bug ID: BUG-008

**Description**

An invalid import `from pyexpat import model` appeared in `runner.py`, causing an `ImportError` on startup and breaking the agent's core reasoning loop.

---

**File**

```
agentstack/core/runner.py
```

---

**Code Snippet**

The offending line that was removed:

```python
# BEFORE (incorrect — accidental IDE auto-import)
from pyexpat import model
```

---

**Cause**

An IDE auto-import incorrectly inserted `from pyexpat import model` when the developer typed `model` in the editor. `pyexpat` is a standard library XML parser module and has no relation to AgentStack's model layer.

---

**Solution**

Removed the erroneous `from pyexpat import model` import from `runner.py` and audited the file's remaining imports to remove any other stale or incorrect entries.

---

**Status**

```
Status: Resolved
```

---

## Bug ID: BUG-009

**Description**

Agent prompts lacked structured context for reasoning and tool usage. The agent received a bare "User Task" string with no instructions on how to think, which tools were available, or how to format its responses.

---

**File**

```
agentstack/prompts/template.py
```

---

**Code Snippet**

The fix — `build_prompt()` assembling a structured agent prompt:

```python
def build_prompt(task: str, tools: list, history: str = "") -> str:
    tool_descriptions = "\n".join(
        f"- {tool.name}: {tool.description}" for tool in tools
    )
    return f"""You are an autonomous AI agent. Reason step by step.

Available Tools:
{tool_descriptions}

Use this format:
Thought: <your reasoning>
Action: <tool name>
Action Input: <tool input>
Observation: <tool result>
... (repeat as needed)
Thought: I now know the answer.
Final Answer: <your answer>

{f"History:{chr(10)}{history}{chr(10)}" if history else ""}
User Task: {task}"""
```

---

**Cause**

The agent was building prompts by passing only the raw user task string, giving the model no instructions on reasoning format, available tools, or expected output structure.

---

**Solution**

Implemented a `build_prompt()` function in `agentstack/prompts/template.py` that injects tool descriptions, reasoning format instructions, optional history, and the user task into a structured prompt template.

---

**Status**

```
Status: Resolved
```

---

## Bug ID: BUG-010

**Description**

MockModel produced incorrect outputs after the introduction of structured prompts. Responses no longer matched expected patterns, breaking the agent reasoning loop.

---

**File**

```
agentstack/models/mock_model.py
```

---

**Code Snippet**

The fix — extracting the user task from the structured prompt using regex before processing:

```python
import re

def generate(self, prompt: str) -> str:
    # Extract the actual user task from structured prompt
    task_match = re.search(r"User Task:\s*(.+)", prompt)
    task = task_match.group(1).strip() if task_match else prompt

    if "Observation:" in prompt:
        observation = prompt.split("Observation:")[-1].strip()
        return f"\nThought: I now know the answer.\nFinal Answer: {observation}\n"

    math_match = re.search(r"(\d+\s*[\+\-\*\/]\s*\d+)", task)
    if math_match:
        expression = math_match.group(1)
        return f"\nThought: I should calculate this.\nAction: calculator\nAction Input: {expression}\n"

    return "\nThought: I can answer directly.\nFinal Answer: Hello! This is a mock response.\n"
```

---

**Cause**

MockModel was matching patterns directly against the full prompt string. With structured prompts, the raw task was buried inside a larger template, so simple string matching on `prompt` no longer extracted the right content.

---

**Solution**

Added a regex extraction step at the top of `generate()` to pull the `User Task:` value out of the structured prompt before applying any downstream logic.

---

**Status**

```
Status: Resolved
```

---

## Bug ID: BUG-011

**Description**

MockModel incorrectly detected an Observation on the first pass, causing it to skip tool usage entirely and return a premature Final Answer. This happened even when no tool had been called yet.

---

**File**

```
agentstack/models/mock_model.py
```

---

**Code Snippet**

The fix — tightening the regex to match only actual tool-returned observation values, not the instruction template:

```python
# BEFORE — too broad, matched "Observation:" in prompt instructions
if "Observation:" in prompt:
    ...

# AFTER — only matches an Observation line that has a non-empty value after it
observation_match = re.search(r"Observation:\s*(\S+.*)", prompt)
if observation_match:
    observation = observation_match.group(1).strip()
    return f"\nThought: I now know the answer.\nFinal Answer: {observation}\n"
```

---

**Cause**

The prompt template included `"Observation: <tool result>"` as a format example in the instructions block. The original `"Observation:" in prompt` check matched this literal text, making MockModel think a tool had already run and triggering a premature Final Answer.

---

**Solution**

Replaced the simple `in` check with a regex that requires a non-whitespace value after `"Observation:"`, ensuring the match only fires on actual tool results and not on placeholder instruction text.

---

**Status**

```
Status: Resolved
```

---

## Bug ID: BUG-012

**Description**

User messages were not being stored in conversation memory. The agent processed tasks correctly but the memory module had no record of what the user had asked, breaking any context-dependent behaviour across turns.

---

**File**

```
agentstack/core/agent.py
```

---

**Code Snippet**

The fix — calling `add_user_message()` before running the reasoning loop:

```python
def run(self, task: str) -> str:
    # Store user message in memory before processing
    self.memory.add_user_message(task)

    prompt = build_prompt(
        task=task,
        tools=self.registry.list_tools(),
        history=self.memory.get_history()
    )
    return self.runner.run(prompt)
```

---

**Cause**

`add_user_message()` was defined on the memory module and referenced in comments/docs, but the call was never actually placed inside `agent.py`'s `run()` method. As a result, every user turn was silently dropped from memory.

---

**Solution**

Added `self.memory.add_user_message(task)` at the start of `agent.run()`, before `build_prompt()` is called, so the user message is captured in memory and available to subsequent turns via `get_history()`.

---

**Status**

```
Status: Resolved
```

---

## Bug ID: BUG-013

**Description**

`WebSearchTool` returned no results and produced a runtime warning on every invocation. Web search queries passed through the agent silently failed, leaving the reasoning loop with empty observations.

---

**File**

```
agentstack/tools/web_search.py
requirements.txt
```

---

**Code Snippet**

The fix — switching from the deprecated `duckduckgo_search` to `ddgs`:

```python
# BEFORE
from duckduckgo_search import ddg

class WebSearchTool(BaseTool):
    name: str = "web_search"
    description: str = "Searches the web for a given query."

    def run(self, query: str) -> str:
        results = ddg(query, max_results=3)
        return str(results)

# AFTER
from ddgs import DDGS

class WebSearchTool(BaseTool):
    name: str = "web_search"
    description: str = "Searches the web for a given query."

    def run(self, query: str) -> str:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))
        return str(results)
```

`requirements.txt` updated:

```diff
- duckduckgo_search
+ ddgs
```

---

**Cause**

The `duckduckgo_search` package was deprecated upstream and its `ddg()` function no longer returned results, instead emitting a runtime deprecation warning. The replacement package `ddgs` exposes a different API via the `DDGS` context manager.

---

**Solution**

Replaced the `duckduckgo_search` import with `ddgs`, updated `WebSearchTool.run()` to use the `DDGS` context manager with `ddgs.text()`, and updated `requirements.txt` to reference `ddgs` instead of the deprecated package.

---

**Status**

```
Status: Resolved
```

---

# Bug Logging Guidelines

When adding new bugs:

1. Assign a unique Bug ID.

Example:

```
BUG-002
BUG-003
BUG-004
```

2. Provide a clear and reproducible description.

3. Include the code snippet causing the issue.

4. Document the solution after fixing the bug.

5. Update the bug status.

---

# Common Bug Categories

During development, bugs may fall into the following categories:

### Agent Reasoning Bugs

Issues in the reasoning loop such as:

* incorrect tool selection
* infinite loops
* malformed responses

### Tool Execution Bugs

Problems with tool invocation such as:

* tool input parsing errors
* tool registry failures

### Model Integration Bugs

Issues related to LLM APIs such as:

* API request formatting
* response parsing

### CLI Bugs

Problems with command-line interactions such as:

* argument parsing
* command failures

### Memory Bugs

Issues related to conversation context such as:

* memory overflow
* incorrect context retrieval

---

# Debugging Best Practices

To maintain high code quality:

* log reasoning steps during agent execution
* display tool calls clearly in CLI output
* use structured error messages
* reproduce bugs with minimal examples

---

# Maintainers

Maintained by **Adwaith R Nair** and **AgentStack Contributors**.
