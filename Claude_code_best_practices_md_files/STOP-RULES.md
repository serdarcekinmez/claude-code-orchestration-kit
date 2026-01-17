# STOP Rules

> **Single source of truth for hard-stop conditions.** These rules are non-negotiable. Reference this file from all workflows and agents.

---

## Purpose

This file defines the **exact wording** for all STOP conditions. Every workflow, agent, and template should reference these rules verbatim to ensure consistent behavior across the documentation kit.

---

## Universal STOP Rules

Use these exact phrases. They are non-negotiable.

### STOP: Missing Information

> If required information is missing or ambiguous, **STOP and ask** before proceeding.

**Examples:**
- Task description is unclear
- Expected behavior not specified
- File paths not provided
- Constraints not defined

### STOP: Forbidden Paths

> If the task requires accessing paths in `permissions.deny` or secrets, **STOP and ask** for guidance.

**Examples:**
- Task requires reading `.env` files
- Need to access `secrets/**` directory
- Credentials or API keys needed
- Production config files requested

### STOP: Baseline Tests Fail

> If baseline tests fail before making changes, **STOP and ask**—do not proceed.

**Rationale:** You cannot verify your changes don't introduce regressions if the baseline is already broken.

**Action:** Report the failing tests and wait for guidance before making any code changes.

### STOP: Cannot Find Required Files/Functions

> Do not invent file names, function names, or paths. If the expected code is not found, **STOP and ask**.

**Examples:**
- Task references `src/services/auth.py` but file doesn't exist
- Function `calculate_total()` not found in expected location
- Module import path doesn't resolve

**Never:** Make up plausible-sounding paths or function names.

### STOP: Behavior Change During Refactor

> If a refactor would change observable behavior, **STOP and report** immediately.

**Applies to:** Refactor Agent, any behavior-lock refactoring task.

**Action:** Report that the planned change would alter behavior, and treat it as a bug fix or feature change instead.

---

## How to Reference These Rules

### In Workflow Docs

Add this block to the constraints or safety section:

```markdown
**STOP Rules apply.** See [./STOP-RULES.md](./STOP-RULES.md) for conditions that require stopping and asking before proceeding.
```

### In Agent Templates

Add to the Safety Rules section:

```markdown
### Hard Stops

The following conditions require immediate stop:
- Missing information → STOP and ask
- Forbidden paths needed → STOP and ask
- Baseline tests fail → STOP and ask
- Cannot find expected code → STOP and ask
- Behavior change in refactor → STOP and report

See: [./STOP-RULES.md](./STOP-RULES.md)
```

### Inline Reference

When a specific STOP rule applies:

```markdown
If baseline tests fail, **STOP and ask**—do not proceed. (See [STOP-RULES.md](./STOP-RULES.md))
```

---

## Verbatim Text for Copy-Paste

Use these exact sentences when documenting STOP conditions:

```
If required information is missing or ambiguous, STOP and ask before proceeding.

If the task requires accessing paths in permissions.deny or secrets, STOP and ask for guidance.

If baseline tests fail before making changes, STOP and ask—do not proceed.

Do not invent file names, function names, or paths. If the expected code is not found, STOP and ask.

If a refactor would change observable behavior, STOP and report immediately.
```

---

## Anti-Patterns

### DON'T: Proceed with Assumptions

```
# BAD
"I couldn't find auth.py, so I'll create a new one based on common patterns."

# GOOD
"I couldn't find auth.py at the expected location. STOP: Please confirm the correct path."
```

### DON'T: Skip Failing Tests

```
# BAD
"3 tests are failing, but they look unrelated. Proceeding with changes."

# GOOD
"3 tests are failing in the baseline. STOP: Cannot proceed until we address whether these are known failures."
```

### DON'T: Guess at Missing Requirements

```
# BAD
"The error handling wasn't specified, so I'll add comprehensive error handling."

# GOOD
"Error handling requirements not specified. STOP: Should errors return JSON, raise exceptions, or log silently?"
```

---

## Related Docs

- [./orchestrator.md](./orchestrator.md) — References STOP rules in always-on rules
- [./test-gate.md](./test-gate.md) — Baseline fail = STOP
- [./refactor-agent.md](./refactor-agent.md) — Behavior change = STOP
- [./permissions-patterns.md](./permissions-patterns.md) — Forbidden paths details
