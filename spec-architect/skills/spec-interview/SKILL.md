---
name: spec-interview
description: Use when the user describes an app or feature in rough notes, or says "spec this". Interviews the user and writes SPEC.md before any code is written.
---

# Spec interview

Never write code in this skill. The only output is an approved SPEC.md.

1. Read the user's notes. List every requirement found, one line each,
   and show the list so the user can see nothing was lost.
2. Find the gaps:
   - formulas: per row or aggregate? zero, empty or missing values?
   - thresholds: is every range covered, with no hole and no overlap?
   - actions: what channel (email, Slack, database flag), which recipient,
     where the recipient is configured?
   - sensitive data: which fields, hidden where (screen, logs, exports)?
   - assets: do they exist (logo file, credentials, API access)?
   - "done": what test proves each rule works?
3. Ask about the gaps with AskUserQuestion: at most 4 questions per round,
   multiple choice when possible, recommended option first. Up to 3 rounds.
4. Always ask: "Should Claude see the real data, or only synthetic data with
   the same columns?" Recommend synthetic only.
5. Write SPEC.md with exactly these sections:
   Goal · Stack · Data · Business rules · Integrations · Privacy ·
   Branding/UI · Out of scope · Done when
   Business rules are written as testable statements ("if delta = 0 → show N/A").
   Done when is a checklist of tests.
6. Show SPEC.md and ask for approval. Apply changes until approved.
7. Then suggest: /spec-architect:setup-architect
