# Session Operations

> **Session discipline for Claude Code.** Resume, continue, worktree isolation, and long task survival.

---

## Session Lifecycle Concepts

Claude Code sessions can be managed for continuity and isolation. The exact flags and commands may vary by version—verify available options with `claude --help`.

### Starting vs Resuming

| Scenario | Approach |
|----------|----------|
| New task, fresh start | Start new session |
| Continue previous work | Resume existing session |
| Switch to different task | New session or worktree |
| Long investigation | Same session with `/compact` checkpoints |

---

## Resume and Continue (If Supported)

> **Note:** The exact flags (`--continue`, `--resume`, `/resume`) may vary by Claude Code version. Verify with `claude --help` before use.

### Conceptual Patterns

**Continue a session:** Pick up where you left off, with full context preserved.

```bash
# If your version supports it:
claude --continue

# Or within a session:
/resume
```

**When to resume vs. start fresh:**

| Resume when... | Start fresh when... |
|----------------|---------------------|
| Continuing the same task | Starting a new, unrelated task |
| Need previous context | Previous context is irrelevant |
| Multi-day debugging | Context has become stale |
| Building on prior decisions | Prior decisions were wrong |

### Session Naming (If Supported)

Some versions support naming sessions:

```bash
# If supported:
claude --session "auth-refactor"

# Later resume:
claude --resume "auth-refactor"
```

**Naming conventions:**
- Use task/ticket identifiers: `fix-login-123`, `feature-export-456`
- Keep names short and descriptive
- Avoid spaces (use hyphens)

---

## One Worktree = One Task

### The Rule

> Keep one git worktree per active Claude Code task to prevent context bleed.

### Why It Matters

When you have multiple tasks in the same directory:
- Context accumulates across unrelated files
- Risk of editing wrong files
- Harder to isolate changes for review
- `/compact` might lose important task-specific context

### How to Apply

**Using git worktrees:**

```bash
# Create worktree for a task
git worktree add ../project-fix-auth fix-auth-branch

# Work in isolated directory
cd ../project-fix-auth
claude

# When done, remove worktree
git worktree remove ../project-fix-auth
```

**Using separate directories:**

```bash
# Clone for isolated work
git clone project project-task-123
cd project-task-123
git checkout -b task-123
claude
```

### When to Skip Isolation

- Quick, single-file fixes
- Sequential tasks (finish one completely before starting next)
- Tasks that deliberately span the same files

---

## Long Task Survival Kit

For debugging sessions, complex refactors, or multi-hour investigations:

### 1. Create a DEBUG_LOG.md

Track progress outside Claude's context:

```markdown
# Debug Log: Issue #789

## Goal
Fix intermittent timeout on /api/reports

## Status
[ ] Observe → [ ] Reproduce → [ ] Isolate → [ ] Fix → [ ] Verify

## Observations
- [timestamp] Checked slow query log - found N+1 pattern

## Tried
- [x] Profiled endpoint - 60% time in get_transactions()
- [ ] Check index on transactions.company_id

## Current Hypothesis
Missing database index on frequently-queried column

## Next Steps
1. Verify index exists
2. Add index if missing
3. Re-run profiling
```

### 2. Checkpoint with /compact

Run `/compact` between investigation phases:

```
Phase 1: Observe → /compact
Phase 2: Reproduce → /compact
Phase 3: Isolate → /compact
Phase 4: Fix → keep in context
Phase 5: Verify → final report
```

### 3. State Restore After /compact

After compacting, immediately restate:

```markdown
## Context Restored
- **Goal:** Fix timeout in /api/reports endpoint
- **Scope:** Touch src/services/report.py; avoid src/api/
- **Validation:** pytest tests/test_reports.py passes under 30s
```

### 4. Reference External Files

Keep DEBUG_LOG.md and CLAUDE.md updated so you can re-read them after context compression.

---

## Session Checklist

### Before Starting

```
□ Is this a new task or continuation?
□ If continuation, can I resume the previous session?
□ Is the working directory isolated (worktree/clone)?
□ Is CLAUDE.md present with project constraints?
□ Are permissions configured (deny secrets)?
```

### During Long Sessions

```
□ Am I tracking progress in DEBUG_LOG.md?
□ Should I /compact before context fills?
□ Did I update DEBUG_LOG.md before compacting?
□ Did I restate context after compacting?
```

### When Switching Tasks

```
□ Is the current task complete or paused at a good checkpoint?
□ Did I /compact and document state?
□ Am I switching to a separate worktree/directory?
□ Can I clearly identify what belongs to which task?
```

---

## Quick Reference

```
┌─────────────────────────────────────────────────────────────┐
│                   SESSION DISCIPLINE                         │
├─────────────────────────────────────────────────────────────┤
│ ONE WORKTREE = ONE TASK                                     │
│   Prevents context bleed between unrelated work             │
├─────────────────────────────────────────────────────────────┤
│ LONG TASKS:                                                 │
│   1. Create DEBUG_LOG.md                                    │
│   2. /compact between phases                                │
│   3. Restate context after compacting                       │
│   4. Update DEBUG_LOG.md before each /compact               │
├─────────────────────────────────────────────────────────────┤
│ RESUME/CONTINUE (verify with claude --help):                │
│   Same task → resume session                                │
│   New task → new session + separate worktree                │
└─────────────────────────────────────────────────────────────┘
```

---

## Related Docs

- [./context-management.md](./context-management.md) — Token discipline details
- [./project-template-3.md](./project-template-3.md) — DEBUG_LOG.md template
- [./iterative-debugging.md](./iterative-debugging.md) — Long debugging workflow
- [./orchestrator.md](./orchestrator.md) — Session setup in quickstart
