# Claude Code Orchestration Kit

> **A structured documentation system for disciplined, safe, and effective Claude Code sessions.**

---

## 🧩 Version 2: spec-architect plugin

Version 2 packages the kit's discipline as an installable Claude Code plugin, **spec-architect**.
It turns rough notes into an approved `SPEC.md`, designs the Claude Code setup the project needs
(CLAUDE.md, skills, subagents, hooks, MCP servers, permissions), then enforces build rules while the code is written.

| Component | Type | What it does |
|---|---|---|
| `spec-interview` | Skill | Interviews you about gaps in your notes (formulas, thresholds, actions, sensitive data, "done") and writes `SPEC.md`. Writes no code. |
| `setup-architect` | Skill | Maps each need in `SPEC.md` to the cheapest primitive that guarantees it, shows the file tree, and writes the setup once you approve. |
| `build-rules` | Skill | Tests first, minimum diff, test gate and STOP rules while implementing. |
| `spec-reviewer` | Subagent (Sonnet, read-only) | Checks the code and tests against every rule in `SPEC.md` and reports gaps as a table. |
| `privacy_check.py` | PostToolUse hook | After each Write/Edit, flags real-looking emails, IBAN-like numbers, and sensitive fields (from `.claude/pii-fields.txt`) sent to print, logs, screens or exports. |
| `secret_guard.py` | PreToolUse hook | Blocks Read, Grep, Bash and PowerShell calls that touch secret files (`.env`, keys, `~/.ssh`, `secrets/`…) or dump environment variables. |
| `secret_scan.py` | PostToolUse hook | After each Write/Edit, flags API keys, tokens, private keys and hard-coded passwords without printing the value. |

### Install

In a Claude Code session:

```
/plugin marketplace add serdarcekinmez/claude-code-orchestration-kit
/plugin install spec-architect@serdar-kit
```

Or in one step (Claude Code 2.1.275 or later):

```
/plugin install spec-architect --marketplace serdarcekinmez/claude-code-orchestration-kit
```

From a shell, use `claude plugin marketplace add …` and `claude plugin install …` with the same arguments.
To try a local clone without installing: `claude --plugin-dir ./spec-architect`.

The hooks run `python3`, so Python 3.9+ must be on your PATH as `python3`.

### Use

1. **Spec:** paste your rough notes and run `/spec-architect:spec-interview`. Answer the questions, then approve `SPEC.md`.
2. **Setup:** run `/spec-architect:setup-architect`. Review the proposed file tree, approve it, and it writes the files.
3. **Build:** ask Claude to *"Implement SPEC.md following the build-rules skill."*
   When the build is done, the **spec-reviewer** agent checks the result against `SPEC.md`. `build-rules` calls it at the end, or you can ask for it directly.

### 🔐 How secrets are handled

Secrets are protected by several independent layers, so one miss is not a leak:

| Layer | When | What it does |
|---|---|---|
| Interview | Before any code | `spec-interview` asks which keys the app needs, where they live in dev and prod, and who owns rotation. `SPEC.md` lists variable **names** only. |
| Permissions | Every session | `setup-architect` writes `.claude/settings.json` deny rules for `.env`, `.env.*`, `*.pem`, `*.key`, `secrets/`, `~/.ssh` and `~/.aws`, plus `.gitignore` entries and a `.env.example`. |
| Guard hook | Before each Read, Grep, Bash or PowerShell call | `secret_guard.py` blocks calls that touch secret files or dump environment variables. |
| Scan hook | After each Write or Edit | `secret_scan.py` flags keys, tokens and hard-coded passwords written into files, without echoing the value. |
| Pre-commit | At `git commit` | [gitleaks](https://github.com/gitleaks/gitleaks) (pinned in `templates/.pre-commit-config.yaml`) refuses commits that contain secrets. |
| README | Always | This section: the rules no tool can enforce for you. |

**What remains your responsibility**

- Never paste a secret into the chat; hooks can't catch that.
- Hooks are pattern-based safety nets, not guarantees. Review diffs.
- If a key was ever committed or shown to Claude, rotate it. Deleting the file or the commit does not remove it from git history.
- Use a real secrets manager in production; `.env` is for local development only.
- Give each key the minimum scope it needs, and separate dev and prod keys.

This repository contains a comprehensive set of Markdown files designed to be used with Claude Code—Anthropic's command-line agentic coding tool. These documents establish best practices, enforce safety guardrails, and provide copy-paste prompt templates for common engineering workflows.

---

## 🎯 What Is This?

This kit is a **prompt engineering framework** specifically designed for Claude Code. It provides:

- **Operational guides** for managing Claude Code sessions effectively
- **Workflow templates** for common engineering tasks (features, bugs, refactors)
- **Sub-agent prompts** for specialized work (security, testing, performance)
- **Safety guardrails** to prevent scope creep, token bloat, and security issues
- **Copy-paste templates** ready to use in Claude Code or generate via other AIs

---

## 📁 Repository Structure

```
.
├── README.md                      # This file
│
├── 📘 CORE DOCUMENTATION
│   ├── orchestrator.md            # Central hub - start here
│   ├── claude-code-overview.md    # Session lifecycle, commands, modes
│   └── claude-code-workflow.md    # Feature/Bug/Refactor workflows
│
├── 🛡️ BEST PRACTICES
│   ├── minimum-diff.md            # Smallest correct change principle
│   ├── test-gate.md               # Test verification checkpoints
│   ├── plan-mode.md               # Planning before execution
│   ├── iterative-debugging.md     # No-guess debugging methodology
│   ├── context-management.md      # Token discipline, /compact usage
│   ├── session-ops.md             # Session resume, worktree isolation
│   ├── permissions-and-safety.md  # Least privilege, secrets protection
│   ├── permissions-patterns.md    # Permission syntax & examples
│   ├── STOP-RULES.md              # Universal hard-stop conditions
│   └── cli-automation-snippets.md # CI/CD integration patterns
│
├── 🤖 SUB-AGENT TEMPLATES
│   ├── refactor-agent.md          # Behavior-lock refactoring
│   ├── test-engineer-agent.md     # Test-first development
│   ├── security-review-agent.md   # Threat modeling & vulnerabilities
│   ├── performance-agent.md       # Profiling & optimization
│   └── domain-specialist-agent.md # Domain-specific constraints
│
└── 📋 PROJECT TEMPLATES
    ├── project-template-1.md      # API & Backend Updates
    ├── project-template-2.md      # Complex Refactoring
    └── project-template-3.md      # Deep Debugging
```

---

## 🚀 Quick Start

### Option 1: Direct Use in Claude Code

1. **Clone this repository** into your project or a dedicated location
2. **Reference documents** when starting a Claude Code session:
   ```
   Please read ./orchestrator.md and follow its guidelines for this session.
   ```
3. **Use templates** by copying the prompt blocks into Claude Code

### Option 2: Embed in Your Project

Add the relevant files to your project's `.claude/` directory:
```
your-project/
├── .claude/
│   ├── commands/           # Custom slash commands
│   └── docs/               # This documentation kit
│       ├── orchestrator.md
│       ├── workflows/
│       └── agents/
```

### Option 3: Use with Other AIs to Generate Prompts

Feed these documents to ChatGPT, NotebookLM, or other AI tools to:
- Generate customized prompts for specific tasks
- Create project-specific workflow templates
- Adapt the patterns to your team's conventions

---

## 📖 How to Use This Kit

### Start Here: The Orchestrator

**[orchestrator.md](./orchestrator.md)** is the central hub. It defines:

- **5 Always-On Rules** that apply to every session
- **Universal STOP Rules** for hard-stop conditions
- **3-Step Operating Procedure** (Orient → Plan → Execute)
- **Quick reference** checklist for every session

### Understand the Session Lifecycle

**[claude-code-overview.md](./claude-code-overview.md)** explains:

```
START → PLAN → IMPLEMENT → VERIFY → REVIEW
```

Key concepts:
- **Plan Mode**: Read-only exploration before editing (produces a plan section; optionally write PLAN.md only if explicitly requested)
- **Context Management**: `/compact`, `/context`, `CLAUDE.md`
- **CLI Modes**: Interactive, Print (automation), Headless

> **Note:** Available slash commands can vary by version. Use `/help` in your Claude Code session to confirm supported commands.

### Follow Structured Workflows

**[claude-code-workflow.md](./claude-code-workflow.md)** provides three workflows:

| Workflow | Use When | Key Pattern |
|----------|----------|-------------|
| **Feature Development** | Adding new functionality | Plan → Interview → Implement → Test |
| **Bug Fix** | Fixing broken behavior | Repro → Failing test → Root cause → Fix |
| **Refactor** | Restructuring without behavior change | Behavior lock → Small steps → Tests |

### Invoke Specialized Agents

For complex tasks, use the sub-agent templates:

```xml
<agent>Security Review Agent</agent>
<task>Review the authentication changes for vulnerabilities.</task>
<scope>src/api/routes/auth.py</scope>
```

Available agents:
- **Refactor Agent** → Behavior-preserving restructuring
- **Test Engineer Agent** → Test-first development
- **Security Review Agent** → Threat modeling
- **Performance Agent** → Profiling & optimization
- **Domain Specialist Agent** → Domain-specific validation

### Use Project Templates

Copy-paste ready prompts for common scenarios:

- **[project-template-1.md](./project-template-1.md)** → API & Backend Updates
- **[project-template-2.md](./project-template-2.md)** → Complex Refactoring
- **[project-template-3.md](./project-template-3.md)** → Deep Debugging (intermittent bugs, production incidents)

---

## ⚡ The 5 Always-On Rules

These rules apply to **every** Claude Code session:

### 1. Plan Mode First
> For multi-file changes, architecture decisions, or risky operations—force Plan Mode before any edits.

### 2. Interview If Ambiguous
> If requirements are unclear, ask up to 5 clarifying questions before proceeding.

### 3. Minimum Diff
> Make the smallest correct change. No drive-by refactors.

### 4. Test Gate
> Never claim "done" unless tests pass.

### 5. Permissions & Least Privilege
> Deny access to secrets. Grant only what's needed.

---

## 🛑 Universal STOP Rules

These conditions require **immediate halt**. See [STOP-RULES.md](./STOP-RULES.md):

| Condition                 | Action              |
|---------------------------|---------------------|
| Required info missing     | **STOP and ask**    |
| Forbidden paths needed    | **STOP and ask**    |
| Baseline tests fail       | **STOP and ask**    |
| Cannot find expected code | **STOP and ask**    |
| Refactor changes behavior | **STOP and report** |

---

## 🔧 Configuration

### Recommended `.claude/settings.json`

> **Tip:** Permission patterns are generally matched by prefix (e.g., `Bash(git diff:*)`). Keep rules conservative, and prefer explicit denies for secrets and sensitive files. See [permissions-patterns.md](./permissions-patterns.md).

```json
{
  "permissions": {
    "allow": [
      "Bash(pytest:*)",
      "Bash(npm test:*)",
      "Bash(git status)",
      "Bash(git diff:*)",
      "Bash(ls:*)"
    ],
    "deny": [
      "Read(./.env)",
      "Read(./secrets/**)",
      "Read(**/*.pem)",
      "Read(**/*.key)",
      "Bash(sudo:*)",
      "Bash(rm -rf:*)"
    ]
  }
}
```

### Recommended `CLAUDE.md` (Project Root)

```markdown
# CLAUDE.md

## Project Overview
[1-2 sentences about what this project does]

## Tech Stack
- Language: [e.g., Python 3.11+]
- Framework: [e.g., FastAPI]
- Testing: [e.g., pytest]

## Key Commands
- Run tests: `pytest tests/ -v`
- Run linting: `ruff check src/`

## Constraints
- All functions must have type hints
- Tests required for new features

## Sensitive Files (DO NOT MODIFY)
- config/production.py
- secrets/**
```

---

## 📋 Cheat Sheet

```
┌──────────────────────────────────────────────────────────────┐
│                 CLAUDE CODE QUICK REFERENCE                  │
├──────────────────────────────────────────────────────────────┤
│ NOTE: Commands can vary by version — use /help to confirm.   │
├──────────────────────────────────────────────────────────────┤
│ COMMANDS:                                                    │
│   /plan      → Enter Plan Mode (read-only exploration)       │
│   /compact   → Compress context (use at ~80% capacity)       │
│   /context   → Review what's currently loaded                │
│   /clear     → Clear conversation                            │
├──────────────────────────────────────────────────────────────┤
│ CLI MODES:                                                   │
│   claude                    → Interactive mode               │
│   claude -p "prompt"        → Print mode (automation)        │
│   claude -p "prompt" --output-format json → Structured output│
├──────────────────────────────────────────────────────────────┤
│ WORKFLOW:                                                    │
│   1. Orient: scope, permissions, context                     │
│   2. Plan: if multi-file or risky                            │
│   3. Baseline: run tests before changes                      │
│   4. Implement: minimum diff, test frequently                │
│   5. Verify: all tests green                                 │
│   6. Report: summary, files, test results                    │
├──────────────────────────────────────────────────────────────┤
│ STOP CONDITIONS:                                             │
│   • Missing information → STOP and ask                       │
│   • Forbidden paths → STOP and ask                           │
│   • Baseline tests fail → STOP and ask                       │
│   • Can't find code → STOP and ask                           │
│   • Refactor changes behavior → STOP and report              │
└──────────────────────────────────────────────────────────────┘
```

---

## 🎓 Use Cases

### For Individual Developers

- Establish consistent coding practices with Claude Code
- Reduce debugging time with structured workflows
- Prevent accidental exposure of secrets
- Maintain high code quality standards

### For Teams

- Onboard team members to Claude Code best practices
- Standardize AI-assisted development workflows
- Create project-specific templates and agents
- Integrate with CI/CD pipelines

### For AI-Assisted Prompt Generation

Feed these documents to other AI tools (ChatGPT, NotebookLM) to:
- Generate customized prompts for your specific tech stack
- Create domain-specific agent templates
- Adapt workflows to your team's conventions
- Build training materials for team adoption

---

## 📚 Document Index

### Core Documentation

| Document | Purpose |
|----------|---------|
| [orchestrator.md](./orchestrator.md) | Central hub, always-on rules |
| [claude-code-overview.md](./claude-code-overview.md) | Session lifecycle, commands |
| [claude-code-workflow.md](./claude-code-workflow.md) | Feature/Bug/Refactor workflows |

### Best Practices

| Document | Purpose |
|----------|---------|
| [minimum-diff.md](./minimum-diff.md) | Smallest correct change |
| [test-gate.md](./test-gate.md) | Test verification gates |
| [plan-mode.md](./plan-mode.md) | Planning before execution |
| [iterative-debugging.md](./iterative-debugging.md) | No-guess debugging |
| [context-management.md](./context-management.md) | Token discipline |
| [session-ops.md](./session-ops.md) | Session resume, worktrees |
| [permissions-and-safety.md](./permissions-and-safety.md) | Secrets protection |
| [permissions-patterns.md](./permissions-patterns.md) | Permission syntax |
| [STOP-RULES.md](./STOP-RULES.md) | Hard-stop conditions |
| [cli-automation-snippets.md](./cli-automation-snippets.md) | CI/CD patterns |

### Sub-Agent Templates

| Document | Purpose |
|----------|---------|
| [refactor-agent.md](./refactor-agent.md) | Behavior-lock refactoring |
| [test-engineer-agent.md](./test-engineer-agent.md) | Test-first development |
| [security-review-agent.md](./security-review-agent.md) | Threat modeling |
| [performance-agent.md](./performance-agent.md) | Profiling & optimization |
| [domain-specialist-agent.md](./domain-specialist-agent.md) | Domain constraints |

### Project Templates

| Document | Purpose |
|----------|---------|
| [project-template-1.md](./project-template-1.md) | API & Backend Updates |
| [project-template-2.md](./project-template-2.md) | Complex Refactoring |
| [project-template-3.md](./project-template-3.md) | Deep Debugging |

---

## 🤝 Contributing

To extend this kit:

1. Follow the existing document structure
2. Include cross-references to related docs
3. Provide copy-paste prompt blocks where applicable
4. Add to the orchestrator's file index
5. Test with actual Claude Code sessions

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🔗 Related Resources

- Claude Code Docs: [https://docs.anthropic.com/en/docs/claude-code](https://docs.anthropic.com/en/docs/claude-code)
- Claude Code Settings: [https://docs.anthropic.com/en/docs/claude-code/settings](https://docs.anthropic.com/en/docs/claude-code/settings)
- Claude Code CLI Reference: [https://docs.anthropic.com/en/docs/claude-code/cli-usage](https://docs.anthropic.com/en/docs/claude-code/cli-usage)
- Anthropic Documentation: [https://docs.anthropic.com](https://docs.anthropic.com)

---

**Happy coding with Claude Code!** 🚀