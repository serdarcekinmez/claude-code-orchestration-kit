# Plan Mode

> **For multi-file changes, architecture decisions, or risky operations—plan before you code.** Plan Mode is a read-only exploration phase that prevents premature edits.

---

## What Is Plan Mode?

Plan Mode is a **read-only state** where Claude:

- Explores the codebase
- Designs an implementation approach
- Creates a detailed plan
- Waits for explicit approval before making any edits

**Key property:** No code changes are made until the plan is approved.

---

## When to Force Plan Mode

### Always Use Plan Mode When:

| Scenario | Why |
|----------|-----|
| Changes span **multiple files** | Coordination required; easy to miss dependencies |
| **Architecture decisions** involved | Wrong choice is expensive to undo |
| Changes are **risky or hard to reverse** | Plan reduces blast radius |
| Requirements are **complex or ambiguous** | Planning surfaces unknowns |
| You want to **review the approach** first | Catch issues before code exists |
| **New to the codebase** | Understand before modifying |
| Working on **critical paths** (auth, payments, data) | Extra scrutiny warranted |

### May Skip Plan Mode When:

- Single-file, obvious changes
- Simple bug fixes with clear root cause
- Trivial additions (add a log line, fix a typo)
- You've done identical changes before in this codebase

---

## Plan Template

When creating a plan, use this structure:

```xml
<plan>
  <objective>
    What are we trying to accomplish? (1-2 sentences)
  </objective>

  <constraints>
    - Technical constraints (language, framework, patterns)
    - Business constraints (backwards compatibility, performance)
    - Scope constraints (what's explicitly OUT of scope)
  </constraints>

  <files>
    Files to READ (for understanding):
    - src/services/auth.py
    - src/api/routes/login.py

    Files to MODIFY:
    - src/services/auth.py (add token refresh logic)
    - src/api/routes/login.py (update endpoint response)

    Files to CREATE:
    - src/services/token_manager.py (new module)
    - tests/test_token_manager.py (tests for new module)
  </files>

  <steps>
    1. [Read] Understand current auth flow in auth.py
    2. [Read] Check how login route uses auth service
    3. [Test] Run existing auth tests to establish baseline
    4. [Create] Create token_manager.py with refresh logic
    5. [Create] Write tests for token_manager
    6. [Modify] Update auth.py to use token_manager
    7. [Modify] Update login route to return refresh token
    8. [Test] Run all tests, verify green
  </steps>

  <test-plan>
    Pre-flight: pytest tests/auth/ -v (establish baseline)

    New tests to write:
    - test_token_refresh_valid_token
    - test_token_refresh_expired_token
    - test_token_refresh_invalid_token

    Post-flight: pytest tests/ -v (full suite, all green)
  </test-plan>

  <rollback>
    If something goes wrong:
    1. Revert changes to auth.py and login.py
    2. Delete token_manager.py if created
    3. Tests should return to baseline state

    Git recovery: git checkout HEAD -- src/services/auth.py src/api/routes/login.py
  </rollback>

  <risks>
    - Risk: Existing sessions may be invalidated
      Mitigation: Add backwards-compatible fallback

    - Risk: Token refresh adds latency
      Mitigation: Measure before/after, set performance budget
  </risks>
</plan>
```

---

## Approval Handshake

### The Rule

**Do not leave Plan Mode until the plan is explicitly approved.**

### Flow

```
1. Enter Plan Mode
       │
       ▼
2. Explore codebase (read-only)
       │
       ▼
3. Create plan document
       │
       ▼
4. Present plan to user
       │
       ▼
5. User reviews plan
       │
       ├──► "Approved" ──► Exit Plan Mode, begin implementation
       │
       ├──► "Revise X" ──► Update plan, return to step 4
       │
       └──► "Cancel" ──► Abandon plan, no changes made
```

### Approval Phrases

Proceed when user says:
- "Approved"
- "Looks good, proceed"
- "Go ahead"
- "LGTM" (Looks Good To Me)

Wait/revise when user says:
- "What about X?"
- "Can you also consider Y?"
- "I'm not sure about step 3"
- Asks clarifying questions

---

## Plan Mode Commands

```bash
# Enter Plan Mode
/plan

# During Plan Mode
- Read files
- Search code
- Ask clarifying questions
- Create/update plan document

# After approval
- (User approves)
- Exit Plan Mode
- Begin implementation

# If plan goes off-track
/rewind    # Go back to earlier state
```

---

## Example: Plan Mode Prompt

```xml
<task>
Add a password reset feature to the authentication system.
</task>

<instructions>
Enter Plan Mode and create a detailed implementation plan.

Your plan must include:
1. Objective: What the feature does
2. Constraints: Technical and scope limits
3. Files: What to read, modify, and create
4. Steps: Numbered implementation sequence
5. Test plan: Pre-flight, new tests, post-flight
6. Rollback: How to undo if needed

Do NOT make any code changes until I approve the plan.
</instructions>

<output-format>
Present the plan using the XML template, then ask:
"Does this plan look correct? Reply 'Approved' to proceed or let me know what to revise."
</output-format>
```

---

## Common Pitfalls

### Pitfall 1: Staying in Plan Mode Too Long

**Problem:** Endless planning without execution.

**Fix:**
- Set a time/iteration limit for planning
- If stuck, ask specific questions
- "Good enough" plans can be refined during implementation

### Pitfall 2: Plan Goes Off-Track

**Problem:** Plan addresses wrong problem or misses key requirements.

**Fix:**
- Re-read original requirements
- Ask clarifying questions
- Use `/rewind` to reset if needed
- Start fresh with clearer scope

### Pitfall 3: Plan Is Too Vague

**Problem:** Plan lacks specific files, steps, or test strategy.

**Fix:** A good plan should answer:
- Exactly which files will be touched?
- In what order?
- What tests will be run/written?
- What does "done" look like?

### Pitfall 4: Skipping Plan Mode

**Problem:** Jumping into multi-file changes without planning.

**Fix:**
- If you're unsure, plan first
- Ask: "Would a reviewer want to see this approach first?"
- Default to planning for anything non-trivial

### Pitfall 5: Ignoring the Plan During Implementation

**Problem:** Plan approved, then implementation diverges.

**Fix:**
- Check plan before each step
- If plan needs adjustment, pause and update it
- Communicate deviations explicitly

---

## When to Use

### Ideal for:

- New features with multiple components
- Refactors touching 3+ files
- Changes to authentication, authorization, or payments
- Database schema changes
- API contract changes
- Performance optimizations
- Security-sensitive modifications

### Less critical for:

- Single-function bug fixes
- Adding a log statement
- Fixing typos or documentation
- Changes where the path is obvious

---

## Warnings / Notes

### Warning: Plan ≠ Implementation

A plan is a map, not the territory. Be prepared to adjust during implementation if you discover:
- Unexpected code patterns
- Missing dependencies
- Test failures revealing new requirements

### Note: Plans Are Documentation

Good plans serve as:
- Design documents
- PR descriptions
- Future reference for "why did we do it this way?"

Consider keeping approved plans in your repo's `docs/` or PR description.

---

## Quick Reference

```
┌─────────────────────────────────────────────────────────────┐
│                    PLAN MODE CHECKLIST                       │
├─────────────────────────────────────────────────────────────┤
│ ENTER when:                                                 │
│   □ Multi-file changes                                      │
│   □ Architecture decisions                                  │
│   □ Risky/irreversible operations                          │
│   □ Complex/ambiguous requirements                          │
├─────────────────────────────────────────────────────────────┤
│ PLAN must include:                                          │
│   □ Objective (what)                                        │
│   □ Constraints (limits)                                    │
│   □ Files (read/modify/create)                             │
│   □ Steps (ordered)                                         │
│   □ Test plan (pre/post)                                    │
│   □ Rollback (how to undo)                                  │
├─────────────────────────────────────────────────────────────┤
│ EXIT when:                                                  │
│   □ User explicitly approves                                │
│   □ Plan is complete and clear                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Related Docs

- [./orchestrator.md](./orchestrator.md) — Hub & always-on rules
- [./claude-code-overview.md](./claude-code-overview.md) — Session lifecycle
- [./minimum-diff.md](./minimum-diff.md) — Scope discipline
- [./test-gate.md](./test-gate.md) — Test verification
