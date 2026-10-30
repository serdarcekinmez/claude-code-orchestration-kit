# Test Gate

> **Never claim "done" unless tests pass.** Every change requires a baseline run and a verification run.

---

## What Is a Test Gate?

A Test Gate is a **mandatory checkpoint** that verifies:

1. **Pre-flight (Baseline):** Tests pass BEFORE you make changes
2. **Post-flight (Verification):** Tests pass AFTER your changes

No change is complete until both gates pass.

```
┌─────────────────────────────────────────────────────────────┐
│                      TEST GATE FLOW                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   [Baseline]        [Changes]         [Verification]        │
│       │                 │                  │                │
│   Run tests ──► All pass? ──► Make edits ──► Run tests     │
│       │              │                      │               │
│       │         No: STOP                Yes: DONE           │
│       │         (fix first)              │                  │
│       │                             No: FIX                 │
│       ▼                             (your code)             │
│   Record baseline                                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## The Two Gates

### Gate 1: Pre-flight (Baseline)

**Purpose:** Establish that tests pass before you touch anything.

**Actions:**
1. Run the full test suite
2. Record the results (pass count, fail count, skip count)
3. Note any pre-existing failures

**Commands:**

```bash
# Python (pytest)
pytest tests/ -v

# Python with coverage
pytest tests/ -v --cov=src/ --cov-report=term-missing

# JavaScript (npm)
npm test

# JavaScript with coverage
npm test -- --coverage

# Go
go test ./...

# Rust
cargo test
```

**If baseline fails:**
- **STOP and ask** — do not proceed (see [./STOP-RULES.md](./STOP-RULES.md))
- Either fix the failing tests first (separate task)
- Or document the known failures and ensure you don't add more

### Gate 2: Post-flight (Verification)

**Purpose:** Confirm your changes haven't broken anything and new functionality works.

**Actions:**
1. Run the full test suite
2. Compare results to baseline
3. Ensure no regressions
4. Verify new tests pass

**Criteria:**
```
□ All previously passing tests still pass
□ New tests for your changes pass
□ No new failures introduced
□ Coverage not decreased (ideally improved)
```

---

## When Tests Don't Exist

### The Problem

You're asked to modify code that has no test coverage.

### The Solution: Write Tests First

1. **STOP** — do not make the change yet
2. **Write characterization tests** that capture current behavior
3. **Run the tests** to verify they pass (locking current behavior)
4. **Then proceed** with your change

### Example: Characterization Tests

```python
# Before modifying calculate_price(), lock its behavior:

def test_calculate_price_basic():
    """Lock current behavior: basic calculation."""
    assert calculate_price(100, quantity=1) == 100

def test_calculate_price_with_quantity():
    """Lock current behavior: quantity multiplier."""
    assert calculate_price(100, quantity=3) == 300

def test_calculate_price_with_discount():
    """Lock current behavior: discount applied."""
    assert calculate_price(100, quantity=1, discount=0.1) == 90

def test_calculate_price_zero_quantity():
    """Lock current behavior: edge case."""
    assert calculate_price(100, quantity=0) == 0
```

```javascript
// Before modifying calculatePrice(), lock its behavior:

describe('calculatePrice - current behavior lock', () => {
  test('basic calculation', () => {
    expect(calculatePrice(100, { quantity: 1 })).toBe(100);
  });

  test('quantity multiplier', () => {
    expect(calculatePrice(100, { quantity: 3 })).toBe(300);
  });

  test('discount applied', () => {
    expect(calculatePrice(100, { quantity: 1, discount: 0.1 })).toBe(90);
  });
});
```

### Minimal Repro Test for Bugs

When fixing a bug, write a test that **reproduces the bug first**:

```python
def test_bug_123_special_characters_in_username():
    """
    Repro for #123: Login fails when username contains '@'.
    This test should FAIL until the bug is fixed.
    """
    result = login(username="user@domain.com", password="valid")
    assert result.success is True
```

---

## Test Gate Policy

### The Golden Rule

> **Never claim a task is "done" if tests are not green.**

This is non-negotiable. If tests fail:
- The task is not complete
- Do not move on
- Do not create a PR
- Do not mark the ticket as resolved

### Handling Flaky Tests

If a test fails intermittently:
1. Re-run to confirm it's flaky (not a real failure)
2. Document the flaky test
3. Fix the flakiness in a separate task
4. Do NOT disable the test to pass the gate

### Handling Slow Tests

If the full suite is too slow:
1. Run focused tests during development: `pytest tests/unit/`
2. Run full suite before committing: `pytest tests/`
3. Never skip the full suite for the final gate

---

## Test Commands Reference

### Python (pytest)

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=src/ --cov-report=term-missing

# Run specific test file
pytest tests/test_auth.py -v

# Run tests matching pattern
pytest tests/ -k "login" -v

# Stop on first failure
pytest tests/ -x

# Show locals on failure
pytest tests/ -l
```

### JavaScript (npm/Jest)

```bash
# Run all tests
npm test

# Run with coverage
npm test -- --coverage

# Run specific file
npm test -- tests/auth.test.js

# Run tests matching pattern
npm test -- --testNamePattern="login"

# Watch mode (development)
npm test -- --watch
```

### Go

```bash
# Run all tests
go test ./...

# Verbose output
go test ./... -v

# With coverage
go test ./... -cover

# Specific package
go test ./pkg/auth/...
```

### Generic Placeholder

For other languages/frameworks, substitute your equivalent:

```bash
# Generic pattern
$TEST_RUNNER $TEST_DIRECTORY $VERBOSE_FLAG

# Examples:
# Ruby: bundle exec rspec spec/ --format documentation
# Java: mvn test
# Rust: cargo test
# Elixir: mix test
```

---

## Example: Test Gate Prompts

### Prompt: Enforce Test Gate

```xml
<task>
$TASK_DESCRIPTION
</task>

<test-gate>
MANDATORY: You must run tests before and after making changes.

Pre-flight:
1. Run: pytest tests/ -v (or equivalent)
2. Confirm all tests pass
3. If any tests fail, STOP and report—do not proceed

Post-flight:
1. Run: pytest tests/ -v (or equivalent)
2. Confirm all tests still pass
3. If any NEW failures, fix them before claiming done

Definition of Done requires: ALL TESTS GREEN
</test-gate>
```

### Prompt: Missing Tests

```xml
<task>
Modify the $FUNCTION_NAME function to $CHANGE_DESCRIPTION.
</task>

<constraints>
Before making any changes:
1. Check if tests exist for $FUNCTION_NAME
2. If NO tests exist:
   - Write characterization tests first
   - Lock current behavior
   - Get tests passing
3. Only THEN proceed with the modification
</constraints>
```

---

## Warnings / Notes

### Warning: "Tests Pass Locally"

CI/CD may have different:
- Environment variables
- Database state
- Dependency versions
- Operating system

Always verify in CI, not just locally.

### Warning: Coverage Traps

High coverage ≠ good tests. Ensure tests:
- Assert meaningful behavior
- Test edge cases
- Are not just "smoke tests"

### Note: When to Skip Tests

Almost never. The only acceptable reasons:
- Explicitly documented known failures
- Environment-specific tests (marked as such)
- Tests for features not yet implemented (marked `@skip`)

Never skip tests to "get the PR through."

---

## Quick Reference

```
┌─────────────────────────────────────────────────────────────┐
│                    TEST GATE CHECKLIST                       │
├─────────────────────────────────────────────────────────────┤
│ PRE-FLIGHT (before changes):                                │
│   □ Run full test suite                                     │
│   □ All tests pass (or known failures documented)           │
│   □ Record baseline metrics                                 │
├─────────────────────────────────────────────────────────────┤
│ POST-FLIGHT (after changes):                                │
│   □ Run full test suite                                     │
│   □ All previously passing tests still pass                 │
│   □ New tests for your changes pass                         │
│   □ Coverage maintained or improved                         │
├─────────────────────────────────────────────────────────────┤
│ DONE = ALL TESTS GREEN                                      │
└─────────────────────────────────────────────────────────────┘
```

---

## Related Docs

- [./orchestrator.md](./orchestrator.md) — Always-on rules
- [./STOP-RULES.md](./STOP-RULES.md) — Hard-stop conditions (baseline fails)
- [./claude-code-workflow.md](./claude-code-workflow.md) — Workflows with test gates
- [./iterative-debugging.md](./iterative-debugging.md) — Debug with tests
- [./test-engineer-agent.md](./test-engineer-agent.md) — Testing sub-agent
