# Claude Code Workflows

> **Repeatable workflows for common engineering tasks.** Each workflow includes inputs, steps, test gates, and a Definition of Done checklist.

---

## Workflow Categories

| Workflow | Use When | Key Focus |
|----------|----------|-----------|
| [Feature Development](#workflow-a-feature-development) | Adding new functionality | Plan → Interview → Implement → Test |
| [Bug Fix](#workflow-b-bug-fix) | Fixing broken behavior | Repro → Failing test → Root cause → Fix |
| [Refactor](#workflow-c-refactor) | Restructuring without behavior change | Behavior lock → Small steps → Tests |

---

## Workflow A: Feature Development

### Inputs Required

<input>
- Feature description (what it should do)
- Acceptance criteria (how to verify it works)
- Scope constraints (what's NOT included)
- Relevant files/modules to modify
- Tech stack context (Python/FastAPI, JS/React, etc.)
</input>

### Steps

1. **Orient & Plan**
   - Read existing code in the target area
   - Enter Plan Mode if feature spans multiple files
   - Identify integration points and dependencies

2. **Interview (if needed)**
   - Clarify ambiguous requirements (max 5 questions)
   - Confirm edge case handling
   - Validate approach before coding

3. **Test Gate: Pre-flight**
   ```bash
   # Python
   pytest tests/ -v

   # JavaScript
   npm test
   ```
   - Ensure existing tests pass before changes
   - Note any pre-existing failures

4. **Implement**
   - Write tests first (TDD when practical)
   - Make minimum diff changes
   - Follow existing code patterns
   - Add only the requested feature—no extras

5. **Test Gate: Post-flight**
   ```bash
   # Python
   pytest tests/ -v --tb=short

   # JavaScript
   npm test -- --coverage
   ```
   - All existing tests still pass
   - New tests for the feature pass
   - Coverage maintained or improved

6. **Review**
   - Verify diff contains only feature-related changes
   - Check for hardcoded values, secrets, debug code
   - Confirm acceptance criteria met

### Definition of Done

```
□ Feature meets acceptance criteria
□ All tests pass (existing + new)
□ No unrelated changes in diff
□ No secrets or debug code committed
□ Code follows existing project patterns
□ Security review if feature handles user input/auth
```

---

## Workflow B: Bug Fix

### Inputs Required

<input>
- Bug description (observed vs expected behavior)
- Reproduction steps (how to trigger the bug)
- Environment details (versions, OS, config)
- Error messages/logs/stack traces
- Affected file(s) if known
</input>

### Steps

1. **Reproduce**
   - Follow the reproduction steps exactly
   - Confirm you can trigger the bug
   - If can't reproduce, gather more info before proceeding

2. **Write a Failing Test**
   ```python
   # Python example
   def test_bug_123_user_cannot_login_with_special_chars():
       """Repro for issue #123: login fails with special characters."""
       result = login(username="user@test", password="p@ss!word")
       assert result.success is True  # Currently fails
   ```
   ```javascript
   // JavaScript example
   test('bug #123: login with special characters', () => {
     const result = login({ username: 'user@test', password: 'p@ss!word' });
     expect(result.success).toBe(true); // Currently fails
   });
   ```
   - Test must fail, proving the bug exists

3. **Test Gate: Pre-flight**
   ```bash
   # Run full suite, note the expected failure
   pytest tests/ -v  # or: npm test
   ```
   - Baseline: all tests pass except the new repro test

4. **Root Cause Analysis**
   - Read the failing code path
   - Add logging/debugging to isolate the issue
   - Identify the exact line(s) causing the bug
   - Understand WHY it fails, not just WHERE

5. **Fix**
   - Make the minimum change to fix the root cause
   - Do NOT refactor surrounding code
   - Do NOT fix "other things you noticed"

6. **Test Gate: Post-flight**
   ```bash
   pytest tests/ -v  # or: npm test
   ```
   - Repro test now passes
   - All other tests still pass
   - No regressions introduced

7. **Verify Manually (if applicable)**
   - Follow original repro steps
   - Confirm bug no longer occurs
   - Check edge cases

### Definition of Done

```
□ Bug is reproducible (or documented why not)
□ Failing test captures the bug
□ Root cause identified and documented
□ Fix addresses root cause (not symptoms)
□ Repro test now passes
□ All other tests pass (no regressions)
□ Diff is minimal—only bug fix, no extras
```

---

## Workflow C: Refactor

### Inputs Required

<input>
- Refactor goal (why restructure?)
- Target code area (files, modules, classes)
- Behavior to preserve (what must NOT change)
- Constraints (naming conventions, patterns to follow)
- Test coverage status (are there existing tests?)
</input>

### Steps

1. **Behavior Lock**
   - Identify all behaviors the code currently exhibits
   - Ensure test coverage for each behavior
   - If tests are missing, write them FIRST

   ```python
   # Example: characterization tests before refactor
   def test_calculate_total_with_discount():
       assert calculate_total(100, discount=0.1) == 90

   def test_calculate_total_without_discount():
       assert calculate_total(100) == 100

   def test_calculate_total_with_tax():
       assert calculate_total(100, tax=0.08) == 108
   ```

2. **Test Gate: Pre-flight (Behavior Lock Verified)**
   ```bash
   pytest tests/ -v --cov=src/  # or: npm test -- --coverage
   ```
   - All tests pass
   - Coverage confirms behaviors are locked

3. **Plan the Refactor**
   - Enter Plan Mode for multi-file refactors
   - Break into small, atomic steps
   - Each step should keep tests passing

4. **Refactor in Small Steps**
   - One transformation at a time
   - Run tests after EACH step
   - If tests fail, revert and try smaller step

   **Example sequence:**
   ```
   Step 1: Rename variable → run tests → pass
   Step 2: Extract method → run tests → pass
   Step 3: Move method to new class → run tests → pass
   Step 4: Update callers → run tests → pass
   ```

5. **Test Gate: After Each Step**
   ```bash
   pytest tests/ -v  # or: npm test
   ```
   - Tests must pass after every atomic change
   - If tests fail, revert immediately

6. **Test Gate: Post-flight (Final Verification)**
   ```bash
   pytest tests/ -v --cov=src/  # or: npm test -- --coverage
   ```
   - All tests pass
   - Coverage same or better
   - No behavior changes

7. **Review**
   - Diff shows only structural changes
   - No functional/behavior changes
   - Code is cleaner, more maintainable

### Definition of Done

```
□ Behavior lock tests exist and pass (before & after)
□ Refactor done in small, atomic steps
□ Tests run after each step
□ No behavior changes (same inputs → same outputs)
□ Code coverage maintained or improved
□ Diff contains only structural changes
□ No "while I'm here" extras
```

---

## Test Gate Summary

### Pre-flight (Before Changes)

| Check | Command (Python) | Command (JS) |
|-------|------------------|--------------|
| Run all tests | `pytest tests/ -v` | `npm test` |
| Note baseline | Record pass/fail counts | Record pass/fail counts |
| Check coverage | `pytest --cov=src/` | `npm test -- --coverage` |

### Post-flight (After Changes)

| Check | Criteria |
|-------|----------|
| All tests pass | No new failures |
| New tests pass | Feature/bug tests green |
| No regressions | Same or better than baseline |
| Coverage maintained | Not decreased |

### If Tests Don't Exist

1. **Stop** — do not proceed with the change
2. **Write minimal tests** that capture current behavior
3. **Run tests** to establish baseline
4. **Then proceed** with the workflow

---

## Workflow Selection Guide

```
┌─────────────────────────────────────────────────────────────┐
│                  WHICH WORKFLOW?                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  "Add a new capability"                                     │
│       └──► Workflow A: Feature Development                  │
│                                                             │
│  "Something is broken"                                      │
│       └──► Workflow B: Bug Fix                              │
│                                                             │
│  "Improve structure without changing behavior"              │
│       └──► Workflow C: Refactor                             │
│                                                             │
│  "Not sure" → Ask: Does it change observable behavior?      │
│       Yes  └──► Feature or Bug Fix                          │
│       No   └──► Refactor                                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

---

## Standard Completion Output

All workflows should conclude with this standardized output format:

```
1. **Summary:** 1-2 sentence description of what was done
2. **Files changed:** List of files modified/created
3. **Commands run:** Test commands and results (pass/fail counts)
4. **Risks/assumptions:** Any caveats, edge cases, or follow-up needed
```

This ensures consistent, auditable results across all workflows.

---

## STOP Rules

**STOP Rules apply to all workflows.** See [./STOP-RULES.md](./STOP-RULES.md) for conditions that require stopping and asking before proceeding:
- Missing information → STOP and ask
- Baseline tests fail → STOP and ask
- Cannot find expected code → STOP and ask

---

## Automation and CI Patterns

For automated workflows (CI pipelines, pre-commit hooks), see [./cli-automation-snippets.md](./cli-automation-snippets.md):
- Print mode patterns
- Diff review automation
- CI gate examples

---

## Related Docs

- [./orchestrator.md](./orchestrator.md) — Hub & always-on rules
- [./test-gate.md](./test-gate.md) — Test Gate details
- [./minimum-diff.md](./minimum-diff.md) — Minimum diff discipline
- [./plan-mode.md](./plan-mode.md) — When and how to plan
- [./iterative-debugging.md](./iterative-debugging.md) — Deep debugging workflow
- [./STOP-RULES.md](./STOP-RULES.md) — Universal hard-stop conditions
- [./cli-automation-snippets.md](./cli-automation-snippets.md) — CI/automation patterns
