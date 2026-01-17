# Iterative Debugging

> **No guessing.** Follow a systematic workflow: observe → reproduce → isolate → fix → verify.

---

## The "No Guessing" Policy

### Rule

**Never make changes based on speculation.** Before fixing anything:

1. Understand what's happening
2. Reproduce the issue
3. Identify the root cause
4. Then—and only then—make targeted changes

### Anti-patterns

| Anti-pattern | Problem |
|--------------|---------|
| "Try this and see" | Random changes, wasted time |
| "It's probably X" | Assumption-driven fixes miss root cause |
| Shotgun debugging | Many changes at once, unclear what worked |
| Cargo cult fixes | Copying solutions without understanding |
| "Works on my machine" | Not actually verified |

---

## Root-Cause Workflow

### The Five Steps

```
OBSERVE → REPRODUCE → ISOLATE → FIX → VERIFY
    │         │          │        │       │
    │         │          │        │       └── Tests pass, bug gone
    │         │          │        └── Minimum diff change
    │         │          └── Find exact line(s) causing issue
    │         └── Trigger bug reliably
    └── Gather symptoms, logs, error messages
```

### Step 1: Observe

**Goal:** Understand the symptoms without making assumptions.

**Actions:**
- Read error messages carefully (entire stack trace)
- Check logs for context around the error
- Note the exact inputs that trigger the issue
- Identify what was expected vs. what happened

**Questions to ask:**
- What is the exact error message?
- When did this start happening?
- What changed recently?
- Does it happen every time or intermittently?

### Step 2: Reproduce

**Goal:** Trigger the bug reliably.

**Actions:**
- Create a minimal reproduction case
- Write a failing test that captures the bug
- Confirm you can trigger the issue on demand

**Example: Failing Test First**

```python
def test_bug_456_division_by_zero_on_empty_list():
    """
    Repro for #456: calculate_average crashes on empty input.
    Expected: Return 0 or raise clear error
    Actual: ZeroDivisionError
    """
    result = calculate_average([])  # Should not crash
    assert result == 0  # Or assert raises ValueError
```

```javascript
test('bug #456: calculate average handles empty array', () => {
  // Repro: function crashes with empty input
  // Expected: return 0 or throw clear error
  expect(() => calculateAverage([])).not.toThrow();
  expect(calculateAverage([])).toBe(0);
});
```

**If you can't reproduce:**
- Gather more information
- Check environment differences
- Ask for more details before proceeding

### Step 3: Isolate

**Goal:** Find the exact code causing the issue.

**Actions:**
- Trace the code path from input to error
- Add targeted logging/debugging
- Use binary search to narrow down (comment out half, test, repeat)
- Check recent changes (git log, git bisect)

**Techniques:**

```python
# Strategic logging to isolate
def process_order(order):
    print(f"DEBUG: order received: {order}")
    validated = validate_order(order)
    print(f"DEBUG: validation result: {validated}")
    if validated:
        result = calculate_total(order)
        print(f"DEBUG: calculated total: {result}")  # Crash here?
        return result
```

```bash
# Git bisect to find breaking commit
git bisect start
git bisect bad HEAD
git bisect good v1.2.0
# Git will binary search through commits
```

### Step 4: Fix

**Goal:** Make the minimum change to address root cause.

**Rules:**
- Fix the root cause, not symptoms
- Minimum diff—change only what's necessary
- Don't refactor or "improve" while fixing
- Keep the fix focused and reviewable

**Example: Targeted Fix**

```python
# BAD: Over-engineered fix
def calculate_average(numbers):
    """Calculate average with robust error handling."""  # Added
    if numbers is None:  # Added
        raise ValueError("Input cannot be None")  # Added
    if not isinstance(numbers, (list, tuple)):  # Added
        raise TypeError("Input must be a sequence")  # Added
    if len(numbers) == 0:
        return 0  # The actual fix
    return sum(numbers) / len(numbers)

# GOOD: Minimum fix
def calculate_average(numbers):
    if len(numbers) == 0:
        return 0  # Just handle the empty case
    return sum(numbers) / len(numbers)
```

### Step 5: Verify

**Goal:** Confirm the fix works and nothing else broke.

**Actions:**
1. Run the repro test—it should now pass
2. Run the full test suite—no regressions
3. Manually verify (if applicable) using original repro steps
4. Check edge cases

**Verification Checklist:**
```
□ Failing test now passes
□ All other tests still pass
□ Manual repro confirms bug is fixed
□ Edge cases checked (null, empty, boundary values)
□ No new warnings or errors in logs
```

---

## Example Prompts That Force Analysis

### Prompt: Observe Before Acting

```xml
<task>
Debug the authentication failure reported in issue #789.
</task>

<instructions>
BEFORE making any changes:

1. OBSERVE: Read the error logs and stack trace
   - What is the exact error message?
   - What code path leads to the error?
   - What inputs trigger it?

2. REPRODUCE: Create a failing test
   - Write a test that captures the bug
   - Confirm the test fails

3. ISOLATE: Find the root cause
   - Trace the code path
   - Add logging if needed
   - Identify the exact line(s) causing the issue

Only after completing steps 1-3, show me your analysis and proposed fix.
Do NOT make any code changes until I approve the analysis.
</instructions>
```

### Prompt: No Guessing

```xml
<task>
The API returns 500 errors intermittently.
</task>

<constraints>
- NO GUESSING. Do not suggest fixes based on assumptions.
- Gather evidence first: logs, stack traces, request patterns
- If you cannot reproduce, say so and ask for more information
- Only propose changes after identifying root cause with evidence
</constraints>

<output-format>
## Observations
[What symptoms did you find?]

## Reproduction
[How can the bug be triggered? Include test code.]

## Root Cause Analysis
[What is causing the issue? Show evidence.]

## Proposed Fix
[What specific change fixes the root cause?]
</output-format>
```

### Prompt: Long Debug Session Management

```xml
<task>
Debug the memory leak in the data processing pipeline.
</task>

<context>
This may require a long debugging session. To manage context:
</context>

<instructions>
1. Create a DEBUG_LOG.md to track your progress:
   - What you've tried
   - What you've ruled out
   - Current hypotheses

2. After each investigation step:
   - Update DEBUG_LOG.md
   - Use /compact if context is getting large

3. Follow the root-cause workflow:
   - Observe: Profile memory usage, check for obvious leaks
   - Reproduce: Create minimal test case
   - Isolate: Binary search through code paths
   - Fix: Minimum change to address leak
   - Verify: Memory profile before/after

4. Do NOT make speculative changes. Evidence first.
</instructions>
```

---

## Using Tests/Logs to Validate

### Tests as Validation

Each step of your debugging should be testable:

| Step | Validation |
|------|------------|
| Observe | Logs confirm the error matches the report |
| Reproduce | Failing test captures the bug |
| Isolate | Adding logging pinpoints the location |
| Fix | Test now passes |
| Verify | Full suite passes, no regressions |

### Log-Driven Debugging

Add strategic logging to trace execution:

```python
import logging
logger = logging.getLogger(__name__)

def process_payment(payment):
    logger.debug(f"Processing payment: {payment.id}")
    logger.debug(f"Payment amount: {payment.amount}")

    validated = validate_payment(payment)
    logger.debug(f"Validation result: {validated}")

    if not validated:
        logger.warning(f"Payment {payment.id} failed validation")
        return False

    result = charge_card(payment)
    logger.debug(f"Charge result: {result}")

    return result
```

**Remember:** Remove debug logging before committing (or use proper log levels).

---

## Long Session Management

For complex bugs requiring extended debugging:

### Create DEBUG_LOG.md

```markdown
# Debug Log: Issue #789 - Intermittent 500 Errors

## Session 1 (2024-01-15)

### Observations
- Error occurs ~5% of requests
- Stack trace points to database connection pool
- Happens more under load

### Tried
- [x] Checked database connection settings - normal
- [x] Reviewed connection pool config - within limits
- [ ] Profile under load conditions

### Hypotheses
1. Connection pool exhaustion under load
2. Query timeout not handled properly

### Next Steps
- Add connection pool metrics logging
- Create load test to reproduce

---

## Session 2 (2024-01-16)

### New Observations
- Connection pool hits max during errors
- Some queries taking >30s

### Root Cause
Query in get_user_orders() missing index, causing slow queries that exhaust pool.

### Fix
Add index on orders.user_id column.
```

### Token Discipline

- Use `/compact` after completing investigation phases
- Keep DEBUG_LOG.md as external memory
- Focus context on current hypothesis only

---

## Warnings / Notes

### Warning: Don't Fix What You Don't Understand

If you can't explain WHY the bug occurs, you haven't found the root cause. Keep investigating.

### Warning: Intermittent Bugs

For bugs that don't reproduce consistently:
- Look for race conditions
- Check for external dependencies (network, database, time)
- Increase logging/monitoring
- Don't guess—gather more data

### Note: When to Escalate

If after systematic debugging you cannot:
- Reproduce the issue
- Identify root cause
- Find relevant logs

Escalate with your findings:
- What you observed
- What you tried
- What you ruled out
- Current hypotheses

---

## Quick Reference

```
┌─────────────────────────────────────────────────────────────┐
│              DEBUGGING WORKFLOW                              │
├─────────────────────────────────────────────────────────────┤
│ 1. OBSERVE    │ Read errors, logs, symptoms                │
│ 2. REPRODUCE  │ Write failing test, trigger bug           │
│ 3. ISOLATE    │ Find exact cause, trace code path         │
│ 4. FIX        │ Minimum change to root cause              │
│ 5. VERIFY     │ Tests pass, bug gone, no regressions      │
├─────────────────────────────────────────────────────────────┤
│ NO GUESSING: Evidence before changes                        │
│ REPRO FIRST: Failing test before fix                       │
│ MINIMUM DIFF: Fix only what's broken                       │
└─────────────────────────────────────────────────────────────┘
```

---

## Related Docs

- [./orchestrator.md](./orchestrator.md) — Always-on rules
- [./test-gate.md](./test-gate.md) — Test verification
- [./claude-code-workflow.md](./claude-code-workflow.md) — Bug fix workflow
- [./context-management.md](./context-management.md) — Long session management
- [./project-template-3.md](./project-template-3.md) — Deep debugging template
