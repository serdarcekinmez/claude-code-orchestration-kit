# Claude Code Overview

> **Operational overview of Claude Code**—session lifecycle, Plan Mode, context management, and CLI patterns.

---

## Session Lifecycle

Every Claude Code session follows this flow:

```
START → PLAN → IMPLEMENT → VERIFY → REVIEW
  │       │        │          │        │
  │       │        │          │        └── Final check, cleanup
  │       │        │          └── Test Gate (tests must pass)
  │       │        └── Minimum diff edits
  │       └── Plan Mode (if non-trivial)
  └── Orient: scope, permissions, context
```

### Phase Details

| Phase | Activities | Key Tools/Commands |
|-------|------------|-------------------|
| **Start** | Review task, check permissions, identify relevant files | `/context`, file reads |
| **Plan** | Design approach, get approval for multi-file changes | Plan Mode, interview questions |
| **Implement** | Make minimum diff changes | Edit, Write tools |
| **Verify** | Run tests, confirm behavior | Bash (test commands), Test Gate |
| **Review** | Final check, clean up, confirm done | `/compact` if needed |

---

## Plan Mode

### What It Is

Plan Mode is a **read-only exploration phase** where Claude:
- Analyzes the codebase
- Designs an implementation approach
- Presents a plan for approval
- **Does NOT make any edits**

### How It Works

1. **Enter Plan Mode**: Explicitly request planning or use `/plan`
2. **Exploration**: Claude reads files, searches code, understands patterns
3. **Plan Creation**: Claude produces a plan section with objectives, steps, and test strategy (write to `PLAN.md` only if explicitly requested)
4. **Approval Handshake**: User must approve before implementation begins
5. **Exit Plan Mode**: Once approved, Claude can make edits

### When to Force Plan Mode

Force Plan Mode when:
- Changes span **multiple files**
- The task involves **architecture decisions**
- Changes are **risky or hard to reverse**
- Requirements are **complex or ambiguous**
- You want to **review the approach** before any code changes

### Plan Mode Commands

```
/plan          — Enter Plan Mode
(approval)     — User approves the plan, exits Plan Mode
```

> **Note:** Some versions may support `/rewind` to go back if plan went off-track. Verify available commands with your installed version.

See: [./plan-mode.md](./plan-mode.md)

---

## Context Management

### Why It Matters

Claude Code has a context window limit. When context fills up:
- Earlier conversation details may be lost
- Responses slow down
- Quality degrades

### /compact

**Purpose:** Summarize and compress the conversation to free up context space.

**When to use:**
- Before context reaches ~80% capacity
- After completing a major task
- When responses mention lost context

```
/compact       — Summarize conversation, free context
```

### /context

**Purpose:** Review what's currently in context; manage focus.

**When to use:**
- To see what files/information Claude currently has loaded
- To understand what context is being used
- Before starting a new focused task

```
/context       — Review current context state
```

### Memory Anchor: CLAUDE.md

Create a `CLAUDE.md` file in your project root for **durable constraints** that persist across sessions:

```markdown
# CLAUDE.md

## Project Constraints
- Python 3.11+ required
- Use pytest for all tests
- Follow existing code style (black, isort)

## Sensitive Files (DO NOT MODIFY)
- config/production.py
- secrets/**

## Key Patterns
- API routes in src/api/
- Business logic in src/services/
- Tests mirror source structure in tests/
```

See: [./context-management.md](./context-management.md)

---

## Custom Commands vs Built-ins

### Built-in Commands

Claude Code includes built-in commands:

| Command | Purpose |
|---------|---------|
| `/help` | Show available commands |
| `/compact` | Compress context |
| `/context` | Review context state |
| `/plan` | Enter Plan Mode |
| `/clear` | Clear conversation |

### Custom Commands

Custom commands are **project-specific** Markdown files in `.claude/commands/`:

```
.claude/
└── commands/
    ├── review.md       # /project:review
    ├── test.md         # /project:test
    └── deploy.md       # /project:deploy
```

**Example custom command** (`.claude/commands/review.md`):

```markdown
# Code Review

Review the following code for:
1. Security issues (injection, auth)
2. Performance concerns
3. Test coverage gaps
4. Code style violations

Focus on: $ARGUMENTS
```

Invoke: `/project:review src/api/users.py`

---

## CLI Modes

### Interactive Mode (Default)

Standard REPL session for back-and-forth collaboration:

```bash
claude
```

### Print Mode (Automation)

Single-shot mode for scripts and automation:

```bash
claude -p "Explain what this function does" < src/utils.py
```

**Flags:**
- `-p` or `--print` — Print mode (non-interactive)
- `--output-format json` — Structured JSON output
- `--output-format text` — Plain text output (default)

**Example: CI Integration**

```bash
# Run code review in CI
claude -p "Review this diff for security issues" --output-format json < changes.diff
```

### Headless/SDK Mode

For programmatic integration:

```bash
claude --output-format stream-json
```

Returns structured events for parsing by external tools.

---

## Session Best Practices

### Starting a Session

1. **Check permissions** — Verify `.claude/settings.json` denies secrets (see [./permissions-patterns.md](./permissions-patterns.md))
2. **Set context** — Read `CLAUDE.md` if present
3. **Scope the task** — Clarify what's in/out of scope
4. **Decide on Plan Mode** — Multi-file or risky? Plan first.
5. **Session isolation** — Use separate worktree for separate tasks (see [./session-ops.md](./session-ops.md))

### During a Session

1. **Stay focused** — One task at a time
2. **Test frequently** — Run tests after each logical change
3. **Watch context** — Use `/compact` before hitting limits
4. **Minimum diff** — Avoid unrelated changes

### Ending a Session

1. **Verify tests pass** — Never leave with red tests
2. **Review changes** — Check diff is minimal and correct
3. **Clean up** — Remove debug code, temp files
4. **Document** — Note any follow-up tasks

---

## Quick Reference

```
┌─────────────────────────────────────────────────────────────┐
│                   SESSION LIFECYCLE                          │
├─────────────────────────────────────────────────────────────┤
│  START ──► PLAN ──► IMPLEMENT ──► VERIFY ──► REVIEW         │
├─────────────────────────────────────────────────────────────┤
│  /plan      Enter Plan Mode (read-only exploration)         │
│  /compact   Compress context (use at ~80% capacity)         │
│  /context   Review what's in context                        │
│  /clear     Clear conversation                              │
├─────────────────────────────────────────────────────────────┤
│  claude -p "prompt"              Print mode (automation)    │
│  claude --output-format json     Structured output          │
└─────────────────────────────────────────────────────────────┘
```

---

## Related Docs

- [./orchestrator.md](./orchestrator.md) — Hub & always-on rules
- [./plan-mode.md](./plan-mode.md) — Plan Mode details
- [./context-management.md](./context-management.md) — Token discipline
- [./permissions-and-safety.md](./permissions-and-safety.md) — Security configuration
- [./permissions-patterns.md](./permissions-patterns.md) — Permission syntax & examples
- [./session-ops.md](./session-ops.md) — Session resume & worktree discipline
- [./cli-automation-snippets.md](./cli-automation-snippets.md) — CI/automation patterns
