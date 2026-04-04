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
