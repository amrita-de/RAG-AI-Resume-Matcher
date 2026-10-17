---
name: autonomous_execution
description: Authorizes full autonomous tool usage, package/dependency installation, file operations, and command execution for the project without requesting manual user confirmation.
---

# Autonomous Execution & Package Installation Policy

## Direct Authorization
The user has explicitly granted full permission to the agent to autonomously execute tasks, install dependencies, and run tools in this repository.

### Guidelines
1. **Package & Library Installation**:
   - You are fully authorized to install, update, or remove any required Python packages or system tools (e.g., via `uv add <package>` or `pip install <package>`).
   - Do NOT stop to ask the user "Would you like me to install package X?". Directly install necessary packages and proceed.

2. **Tool Invocation**:
   - You are fully authorized to use all available tools (file reads/writes, running commands, browser subagents, search, etc.) proactively to accomplish goals.
   - Do not request permission before running non-destructive scripts, tests, builders, or generators.

3. **Execution Momentum**:
   - When given a task or roadmap phase, execute all sub-steps, verify outputs, fix errors, and report final outcomes autonomously.
