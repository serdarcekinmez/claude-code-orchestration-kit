# Minimum Diff

> **Make the smallest correct change.** Avoid drive-by refactors, unrelated formatting, and scope creep.

---

## Why Minimum Diff Matters

### Principle

Every line changed is a line that can introduce bugs, conflicts, and confusion. The best change is the smallest one that correctly solves the problem.

### Benefits

- **Easier code review** — Reviewers can focus on what matters
- **Fewer merge conflicts** — Less surface area for collisions
- **Lower risk** — Smaller changes = smaller blast radius
- **Clearer history** — Git blame stays meaningful
- **Faster iteration** — Ship sooner, learn faster

### Anti-patterns

| Anti-pattern | Problem |
|--------------|---------|
| "While I'm here..." | Scope creep, unreviewed changes |
| Drive-by refactors | Mixes concerns, hides real change |
| Auto-formatter on untouched files | Noise in diff, false positives |
| "Fixing" unrelated code style | Not your task, not your diff |
| Adding features to bug fixes | Ships untested functionality |

---

## Rules

### Rule 1: Touch Only What's Necessary

**Do:** Change only the files and lines required for the task.

**Don't:** Modify files that aren't directly related to the task.

```
# Bad: Bug fix + unrelated refactor
- def calculate(x, y):
-     result = x + y
-     return result
+ def calculate(first_num: int, second_num: int) -> int:
+     """Calculate the sum of two numbers."""
+     return first_num + second_num

# Good: Just the bug fix
- def calculate(x, y):
-     result = x + y
+ def calculate(x, y):
+     result = x + y + TAX_RATE  # Fix: was missing tax
      return result
```

### Rule 2: No Unrelated Formatting Changes

**Do:** Format only the code you're actively changing.

**Don't:** Run formatters on files you didn't modify substantively.

```
# Bad: Reformatted entire file for a one-line fix
diff --git a/src/utils.py
- 47 lines changed (46 whitespace, 1 actual fix)

# Good: Only the fix
diff --git a/src/utils.py
- 1 line changed (the actual fix)
```

### Rule 3: Isolate Refactors

**Do:** Keep refactors in separate commits/PRs from features and bug fixes.

**Don't:** Mix structural changes with behavioral changes.

```
# Bad: One PR with feature + refactor
PR #123: "Add user export feature"
  - Renamed UserService to UserManager (refactor)
  - Moved 5 files to new directory structure (refactor)
  - Added export_users() method (feature)

# Good: Separate PRs
PR #122: "Refactor: Rename UserService to UserManager"
PR #123: "Feature: Add user export"
```

### Rule 4: No "Improvements" Beyond Scope

**Do:** Complete the requested task.

**Don't:** Add unrequested "improvements."

```
# Task: "Fix the login timeout bug"

# Bad additions:
- Added logging throughout auth module
- Improved error messages
- Added type hints to 12 functions
- Created new AuthException class

# Good: Just the fix
- Changed timeout from 30s to 60s in login handler
```

---

## Diff Hygiene Checklist

Before committing, review your diff:

```
□ Every changed file is necessary for the task
□ No formatting-only changes to untouched code
□ No renamed variables in code I didn't modify
□ No added comments to code I didn't change
□ No "drive-by" type hints or docstrings
□ No refactoring mixed with features/fixes
□ No debug code or console.log statements
□ No TODOs added for unrelated issues
```

---

## Example: Enforcement Prompts

### Prompt: Task Scoping

```xml
<task>
Fix the authentication timeout issue reported in #456.
</task>

<constraints>
- ONLY modify code directly related to the timeout bug
- Do NOT refactor, rename, or restructure any code
- Do NOT add type hints, docstrings, or comments to unchanged code
- Do NOT fix other issues you might notice
- If you see other problems, note them separately—do not fix them now
</constraints>

<definition-of-done>
- Timeout bug is fixed
- Existing tests pass
- Diff contains ONLY timeout-related changes
- No files modified that aren't directly involved in the fix
</definition-of-done>
```

### Prompt: Diff Review

```xml
<task>
Review this diff before committing and identify any violations of minimum diff principles.
</task>

<checklist>
1. Are there any files changed that aren't necessary for the task?
2. Are there any formatting-only changes?
3. Are there any refactors mixed in with the main change?
4. Are there any "improvements" beyond the original scope?
5. Is there any dead code, debug statements, or TODO comments added?
</checklist>

<output>
List any violations found, or confirm "Diff is minimal and focused."
</output>
```

### Prompt: Scope Lock

```xml
<task>
$TASK_DESCRIPTION
</task>

<scope-lock>
This task is ONLY about: $SPECIFIC_GOAL

Out of scope (do not touch):
- Code style or formatting in unrelated files
- Refactoring opportunities you notice
- "Nice to have" improvements
- Other bugs you might discover
- Documentation for unchanged code

If you encounter something out of scope that needs attention, add it to a "Future Work" note at the end of your response—do NOT implement it.
</scope-lock>
```

---

## When to Use

### Always Apply Minimum Diff When:

- Fixing bugs
- Making small features
- Hotfixes to production
- Working in shared codebases
- PRs need quick review

### Minimum Diff Is Less Critical When:

- Dedicated refactoring sprints (but still scope carefully)
- Initial project setup
- Solo projects with no review process
- Explicitly scoped "cleanup" tasks

---

## Warnings / Notes

### Warning: Formatter Conflicts

If your team uses auto-formatters (Black, Prettier), ensure:
- Format ONLY files you're modifying
- Or format ALL files in a separate commit first
- Never mix formatting changes with logic changes

### Warning: IDE Auto-imports

Many IDEs auto-organize imports. This can cause:
- Import order changes in files you didn't touch
- Removed "unused" imports that are actually used dynamically

**Fix:** Configure IDE to only organize imports in modified files.

### Note: Exceptions

Sometimes a slightly larger change IS the minimum correct change:
- Security fix requires updating all call sites
- API change requires updating all consumers
- Deprecation requires migration

In these cases, the "minimum diff" is still the smallest change that fully addresses the issue—even if it touches many files.

### STOP Rule: Forbidden Paths

If your task requires modifying files listed in `permissions.deny` or accessing secrets:
- **STOP and ask** — do not proceed
- See [./STOP-RULES.md](./STOP-RULES.md) for complete STOP conditions

---

## Related Docs

- [./orchestrator.md](./orchestrator.md) — Always-on rules
- [./STOP-RULES.md](./STOP-RULES.md) — Hard-stop conditions
- [./test-gate.md](./test-gate.md) — Verify changes work
- [./plan-mode.md](./plan-mode.md) — Plan scope before coding
- [./refactor-agent.md](./refactor-agent.md) — Isolated refactor workflow
