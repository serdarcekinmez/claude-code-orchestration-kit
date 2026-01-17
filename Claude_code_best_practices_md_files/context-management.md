# Context Management

> **Token discipline: keep scope narrow, manage context proactively.** Use `/compact`, `/context`, and memory anchors effectively.

---

## Why Context Management Matters

### The Problem

Claude Code has a finite context window. When it fills up:
- Earlier conversation details are lost
- Response quality degrades
- Important constraints may be forgotten
- Sessions become slow and unreliable

### The Solution

Proactive context management:
- Keep scope narrow and focused
- Use `/compact` before hitting limits
- Anchor persistent constraints in `CLAUDE.md`
- Use `/context` to review and manage state

---

## Token Discipline

### Rule: Stay Focused

Each session should focus on **one task** at a time. Avoid:
- Reading entire files when only one function matters
- Loading multiple unrelated modules
- Keeping old, irrelevant context around

### Rule: Scope Reads Narrowly

```xml
<!-- BAD: Reading entire file for one function -->
<task>Fix the bug in calculate_total()</task>
Action: Read entire 2000-line orders.py

<!-- GOOD: Focused read -->
<task>Fix the bug in calculate_total()</task>
Action: Read lines 150-200 of orders.py (the function + context)
```

### Rule: Clean Up Between Tasks

After completing a task:
1. Run `/compact` to summarize
2. Clear irrelevant context
3. Start fresh for the next task

---

## /compact Command

### What It Does

Summarizes the conversation, compressing context while preserving:
- Key decisions made
- Important code changes
- Relevant constraints
- Current task state

### When to Use

| Trigger | Action |
|---------|--------|
| Context ~80% full | Run `/compact` immediately |
| Completed a major task | Run `/compact` before starting next |
| Session feels slow | Context may be bloated, `/compact` |
| Lost earlier context | Too late—but `/compact` and re-state key info |

### How to Use

```bash
/compact
```

Or request explicitly: "Please summarize this conversation and compress context."

### Best Practice: Proactive, Not Reactive

Don't wait for symptoms. Run `/compact`:
- After every major task completion
- Before starting a new focus area
- When switching between files/modules

---

## /context Command

### What It Does

Shows what's currently in context:
- Files that have been read
- Key information loaded
- Approximate context usage

### When to Use

- Before starting a focused task
- When unsure what Claude "knows"
- To identify bloated context
- After `/compact` to verify state

### How to Use

```bash
/context
```

---

## Memory Anchor: CLAUDE.md

### What It Is

A `CLAUDE.md` file in your project root that contains **persistent constraints** Claude should always respect.

### Why Use It

- Survives across sessions
- Always available as reference
- Defines project-wide rules
- Reduces repetition

### Template

```markdown
# CLAUDE.md

## Project Overview
[1-2 sentences about what this project does]

## Tech Stack
- Language: Python 3.11+
- Framework: FastAPI
- Database: PostgreSQL
- Testing: pytest

## Key Commands
```bash
# Run tests
pytest tests/ -v

# Run linting
ruff check src/

# Start dev server
uvicorn src.main:app --reload
```

## Code Patterns
- API routes in `src/api/routes/`
- Business logic in `src/services/`
- Database models in `src/models/`
- Tests mirror source structure in `tests/`

## Constraints
- All functions must have type hints
- No print statements in production code
- Tests required for new features

## Sensitive Files (DO NOT MODIFY)
- `config/production.py`
- `secrets/**`
- `.env*`

## Known Issues
- [Issue #123] Auth token refresh not implemented
- [Issue #456] Slow query in user search (needs index)
```

### Location

Place at project root:
```
project/
├── CLAUDE.md        ← Here
├── src/
├── tests/
└── ...
```

---

## Context Checklist Before Coding

Run through this checklist before starting a task:

```
□ Is the task scope clear and narrow?
□ Have I reviewed /context to see what's loaded?
□ Am I reading only the files I need?
□ Is CLAUDE.md available with project constraints?
□ Should I /compact from previous work first?
□ Am I focused on ONE task?
```

---

## State Restore After /compact

After running `/compact`, immediately restate the working context in 3 bullets:

```markdown
## Context Restored
1. **Goal:** What are you trying to accomplish?
2. **Scope:** Files to touch / files forbidden
3. **Validation:** How to verify success (test command, repro steps)
```

**Example:**

```markdown
## Context Restored
1. **Goal:** Fix the authentication timeout bug in user login
2. **Scope:** Touch src/auth/login.py only; do NOT modify src/api/ routes
3. **Validation:** pytest tests/test_auth.py passes; login works within 30s
```

This ensures continuity and prevents drift after context compression.

See: [./session-ops.md](./session-ops.md) for complete session discipline.

---

## Managing Long Sessions

### For Extended Debugging Sessions

1. **Create DEBUG_LOG.md** as external memory:
   ```markdown
   # Debug Log: Issue #789

   ## Observations
   - [What you've seen]

   ## Tried
   - [x] Checked X - result
   - [ ] Still need to check Y

   ## Current Hypothesis
   [What you think is happening]
   ```

2. **Use `/compact` between investigation phases**

3. **Re-read DEBUG_LOG.md** after compacting to restore context

### For Multi-File Refactors

1. **Plan first** (Plan Mode) - reduces exploratory reads
2. **Work in batches** - complete one file, `/compact`, move to next
3. **Keep CLAUDE.md updated** with progress notes

### For Feature Development

1. **Define scope clearly upfront**
2. **Read only relevant files**
3. **`/compact` after each milestone:**
   - After planning
   - After writing tests
   - After implementation
   - After verification

---

## Example: Context-Aware Prompts

### Prompt: Narrow Focus

```xml
<task>
Fix the validation bug in the user registration endpoint.
</task>

<context-management>
- ONLY read files directly related to user registration
- Do NOT explore unrelated parts of the codebase
- Focus: src/api/routes/auth.py and src/services/user_service.py
- If you need additional context, ask before reading
</context-management>
```

### Prompt: Session Reset

```xml
<task>
Starting a new task: implement password reset feature.
</task>

<instructions>
1. First, run /compact to clear context from previous work
2. Re-read CLAUDE.md for project constraints
3. Only then begin exploring relevant files
</instructions>
```

### Prompt: Long Session Awareness

```xml
<task>
Continue debugging the performance issue.
</task>

<context-management>
This is a long debugging session. To manage context:

1. Check DEBUG_LOG.md for what we've already tried
2. Use /compact after each investigation phase
3. Update DEBUG_LOG.md with findings before compacting
4. Keep focus narrow—one hypothesis at a time
</context-management>
```

---

## Warnings / Notes

### Warning: Lost Context Symptoms

If you notice:
- Claude forgetting earlier decisions
- Repeated questions about things already discussed
- Responses ignoring stated constraints

Context is likely full. `/compact` immediately and re-state critical information.

### Warning: Over-reading

Reading "just in case" files bloats context fast:

```
# BAD: "Let me read everything to understand"
Read: models.py, services.py, routes.py, utils.py, config.py, helpers.py...

# GOOD: Focused reading
Read: routes/auth.py (the file with the bug)
Read: services/user.py (the service it calls) - only if needed
```

### Note: CLAUDE.md Is Not Magic

Claude must actively read CLAUDE.md. Prompt it:
- "Please review CLAUDE.md for project constraints"
- "Check CLAUDE.md before proceeding"
- Reference specific sections when relevant

---

## Quick Reference

```
┌─────────────────────────────────────────────────────────────┐
│              CONTEXT MANAGEMENT                              │
├─────────────────────────────────────────────────────────────┤
│ /compact    │ Compress context (use at ~80% or after task) │
│ /context    │ Review what's currently loaded               │
│ CLAUDE.md   │ Persistent project constraints               │
├─────────────────────────────────────────────────────────────┤
│ BEFORE CODING:                                              │
│   □ Scope clear and narrow?                                 │
│   □ /compact from previous work?                            │
│   □ Only reading necessary files?                           │
│   □ CLAUDE.md reviewed?                                     │
├─────────────────────────────────────────────────────────────┤
│ DURING SESSION:                                             │
│   □ /compact after major milestones                         │
│   □ Keep focus on one task                                  │
│   □ Use DEBUG_LOG.md for long sessions                      │
├─────────────────────────────────────────────────────────────┤
│ IF CONTEXT BLOATS:                                          │
│   □ /compact immediately                                    │
│   □ Re-state critical constraints                           │
│   □ Narrow scope going forward                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Related Docs

- [./orchestrator.md](./orchestrator.md) — Hub & always-on rules
- [./claude-code-overview.md](./claude-code-overview.md) — Session lifecycle
- [./session-ops.md](./session-ops.md) — Session resume & worktree discipline
- [./iterative-debugging.md](./iterative-debugging.md) — Long session debugging
- [./plan-mode.md](./plan-mode.md) — Planning reduces exploratory reads
