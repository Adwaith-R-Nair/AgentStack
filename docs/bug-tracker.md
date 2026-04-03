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
