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
| —      | —           | —    | —            | —     | —        | —      |

---

# Bug Entry Format

When a bug is discovered, add a detailed entry below.

---

## Bug ID: BUG-001

**Description**

Describe the issue clearly. Include when the bug occurs and what behavior is observed.

Example:

Agent fails to parse tool output when the LLM response format deviates from the expected structure.

---

**File**

Specify the file where the bug occurs.

Example:

```id="f2"
agentstack/core/runner.py
```

---

**Code Snippet**

Include the problematic code.

Example:

```python id="f3"
if "Action:" in response:
    tool = extract_tool(response)
```

---

**Cause**

Explain why the bug happens.

Example:

The parser assumes the LLM response always contains "Action:" exactly, but some responses may use different formatting.

---

**Solution**

Explain how the bug was fixed.

Example:

Add robust parsing logic using regex to detect tool invocation.

---

**Status**

Possible values:

* Open
* In Progress
* Fixed
* Verified

Example:

```id="f4"
Status: Fixed
```

---

# Bug Logging Guidelines

When adding new bugs:

1. Assign a unique Bug ID.

Example:

```id="f5"
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
