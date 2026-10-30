---
name: build-rules
description: Use while implementing code from SPEC.md or any multi-file change. Enforces minimum diff, test gate and stop rules.
---

# Build rules

Follow ${CLAUDE_SKILL_DIR}/references/minimum-diff.md,
${CLAUDE_SKILL_DIR}/references/test-gate.md and
${CLAUDE_SKILL_DIR}/references/STOP-RULES.md.

Order of work:
1. Plan from SPEC.md; list files to create or change.
2. Write tests for every Business rule and Done when item first.
3. Implement with the smallest correct change.
4. Run the tests. Never claim done while a test fails.
5. If the privacy hook reports a problem, fix it before continuing.
6. Delegate a final check to the spec-reviewer agent and fix what it reports.
