---
name: setup-architect
description: Use after SPEC.md is approved, or when the user asks which skills, subagents, hooks, MCP servers or permissions a project needs. Designs and writes the Claude Code setup.
---

# Setup architect

1. Read SPEC.md. If it is missing or unapproved, run spec-interview first.
2. For exact file syntax, never rely on memory: delegate to the
   claude-code-guide agent or read https://code.claude.com/docs/llms.txt.
3. Map each need to the cheapest primitive that guarantees it:
   - always-true project facts, commands, stack → CLAUDE.md (keep it short)
   - a rule that must never be broken → permissions deny or a hook,
     never only a sentence in CLAUDE.md
   - repeatable workflow or domain knowledge → skill
   - heavy or noisy work (research, review, data checks) → subagent,
     on a cheaper model when quality allows
   - external system (email, Slack, database, another AI such as Codex)
     → an existing MCP server first; custom bridge only if none exists
   For each choice, give one line: why, and its context or token cost.
4. Privacy defaults when SPEC.md has sensitive data:
   - .claude/settings.json: deny Read and Bash access to the real data folder
   - .claude/pii-fields.txt: one sensitive field name per line
     (the plugin's privacy hook reads it)
   - a script that generates synthetic data with the same columns into data/sample/
5. Show the proposed file tree with one line per file. Wait for approval.
6. Write the files. Then tell the user to start the build with:
   "Implement SPEC.md following the build-rules skill."
