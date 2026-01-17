# Orchestrator

> **The central hub for Claude Code orchestration.** This file explains how all documentation pieces fit together and provides the operating framework for effective Claude Code sessions.

---

## What Is This Orchestration Kit?

A structured documentation system that enforces disciplined, safe, and effective use of Claude Code for software engineering tasks. It provides:

- **Best practice guides** for common workflows
- **Sub-agent templates** for specialized tasks
- **Project templates** with copy-paste prompts
- **Safety guardrails** to prevent scope creep, token bloat, and security issues

### When to Use

- Starting a new Claude Code session for non-trivial work
- Onboarding team members to Claude Code workflows
- Establishing project-specific coding standards
- Debugging sessions that have gone off-track

---

## The 5 Always-On Rules

These rules apply to **every** Claude Code session. They are non-negotiable.

### 1. Plan Mode First
> For multi-file changes, architecture decisions, or risky operations—force Plan Mode before any edits.

- Use `/plan` or request planning explicitly
- No code changes until the plan is approved
- See: [./plan-mode.md](./plan-mode.md)

### 2. Interview If Ambiguous
> If requirements are unclear, ask up to 5 clarifying questions before proceeding.

- Never assume; clarify constraints, edge cases, and expectations
- Use structured questions with explicit options when possible
- State assumptions explicitly if proceeding without full clarity

### 3. Minimum Diff
> Make the smallest correct change. No drive-by refactors.

- Touch only files directly related to the task
- Avoid unrelated formatting changes
- Isolate refactors from feature work
- See: [./minimum-diff.md](./minimum-diff.md)

### 4. Test Gate
> Never claim "done" unless tests pass.

- Run baseline tests before changes
- Run verification tests after changes
- If no tests exist, create a minimal repro test first
- See: [./test-gate.md](./test-gate.md)

### 5. Permissions & Least Privilege
> Deny access to secrets. Grant only what's needed.

- Configure `permissions.deny` for `.env`, `secrets/**`, `**/*.key`, `**/*.pem`
- Use `permissions.allow` for safe, scoped commands only
- Never bypass permission checks
- See: [./permissions-and-safety.md](./permissions-and-safety.md)
- See: [./permissions-patterns.md](./permissions-patterns.md) — Exact syntax and examples

---

## Universal STOP Rules

These conditions require immediate halt. See [./STOP-RULES.md](./STOP-RULES.md) for complete details.

| Condition | Action |
|-----------|--------|
| Required info missing | **STOP and ask** |
| Forbidden paths needed | **STOP and ask** |
| Baseline tests fail | **STOP and ask** |
| Cannot find expected code | **STOP and ask** |
| Refactor changes behavior | **STOP and report** |

---

## Custom Slash Commands & Sub-Agents

### Custom Slash Commands

Custom commands live in `.claude/commands/` as Markdown files:

```
.claude/
└── commands/
    ├── review.md       # Code review workflow
    ├── test.md         # Test generation workflow
    └── deploy.md       # Deployment checklist
```

Invoke with: `/project:review`, `/project:test`, etc.

### Sub-Agents

Sub-agents are specialized prompts for focused tasks. This kit provides templates for:

| Agent | Purpose | File |
|-------|---------|------|
| Refactor Agent | Behavior-lock refactors with minimal diff | [./refactor-agent.md](./refactor-agent.md) |
| Test Engineer Agent | Repro-first testing, coverage expansion | [./test-engineer-agent.md](./test-engineer-agent.md) |
| Security Review Agent | Threat modeling, injection vectors | [./security-review-agent.md](./security-review-agent.md) |
| Performance Agent | Profiling, hotspot identification | [./performance-agent.md](./performance-agent.md) |
| Domain Specialist Agent | Domain constraints, no hallucination | [./domain-specialist-agent.md](./domain-specialist-agent.md) |

Invoke agents explicitly by pasting the invoke prompt from the relevant template, or by creating a custom slash command that references the agent template.

---

## Quickstart: 3-Step Operating Procedure

### Step 1: Orient
```
1. Review the task scope
2. Check if Plan Mode is needed (multi-file? risky? architectural?)
3. Identify relevant best practice docs and agent templates
4. Verify permissions are configured (deny secrets)
```

### Step 2: Plan & Interview
```
1. If non-trivial: enter Plan Mode
2. Ask clarifying questions (max 5) if requirements are ambiguous
3. Define explicit constraints and Definition of Done
4. Get plan approval before proceeding
```

### Step 3: Execute & Verify
```
1. Run baseline tests (Test Gate pre-flight)
2. Make minimum diff changes
3. Run verification tests (Test Gate post-flight)
4. Confirm all tests pass before claiming "done"
5. Use /compact if approaching context limits
```

---

## Failure Modes & Fixes

### Scope Creep
**Symptoms:** Task expands beyond original request; "while I'm here" changes; unrelated refactors.

**Fixes:**
- Re-read original task requirements
- Apply Minimum Diff rule strictly
- Split tangential improvements into separate tasks
- Use Plan Mode to lock scope before coding

### Token Bloat
**Symptoms:** Context window filling up; slow responses; loss of earlier context.

**Fixes:**
- Use `/compact` proactively (before 80% full)
- Narrow file scope—don't read entire files when only one function matters
- Use `CLAUDE.md` to anchor persistent constraints
- See: [./context-management.md](./context-management.md)

### Shotgun Debugging
**Symptoms:** Rapid-fire changes without understanding root cause; "try this" edits; fixing symptoms not causes.

**Fixes:**
- Stop and reproduce the issue first
- Write a failing test that captures the bug
- Use observe → reproduce → isolate → fix → verify workflow
- See: [./iterative-debugging.md](./iterative-debugging.md)

### Unsafe Permissions
**Symptoms:** Commands accessing secrets; overly broad tool access; skip-permission flags.

**Fixes:**
- Audit `.claude/settings.json` for deny patterns
- Remove any `--skip-permissions` or `--dangerously-skip-permissions` usage
- Use allowlists instead of blanket approvals
- See: [./permissions-and-safety.md](./permissions-and-safety.md)

---

## File Index

### Orchestrator Files
- [orchestrator.md](./orchestrator.md) — This file (hub)
- [claude-code-overview.md](./claude-code-overview.md) — Operational overview
- [claude-code-workflow.md](./claude-code-workflow.md) — Repeatable workflows

### Best Practices
- [minimum-diff.md](./minimum-diff.md) — Minimal change discipline
- [test-gate.md](./test-gate.md) — Test verification gates
- [plan-mode.md](./plan-mode.md) — Planning before execution
- [permissions-and-safety.md](./permissions-and-safety.md) — Least privilege & secrets
- [permissions-patterns.md](./permissions-patterns.md) — Permission syntax & examples
- [iterative-debugging.md](./iterative-debugging.md) — No-guess debugging
- [context-management.md](./context-management.md) — Token discipline
- [session-ops.md](./session-ops.md) — Session resume & worktree discipline
- [cli-automation-snippets.md](./cli-automation-snippets.md) — CI/automation patterns
- [STOP-RULES.md](./STOP-RULES.md) — Universal hard-stop conditions

### Sub-Agent Templates
- [refactor-agent.md](./refactor-agent.md) — Behavior-lock refactors
- [test-engineer-agent.md](./test-engineer-agent.md) — Repro-first testing
- [security-review-agent.md](./security-review-agent.md) — Threat modeling
- [performance-agent.md](./performance-agent.md) — Profiling & benchmarks
- [domain-specialist-agent.md](./domain-specialist-agent.md) — Domain constraints

### Project Templates
- [project-template-1.md](./project-template-1.md) — API & Backend Updates
- [project-template-2.md](./project-template-2.md) — Complex Refactoring
- [project-template-3.md](./project-template-3.md) — Deep Debugging

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────────┐
│                    CLAUDE CODE CHECKLIST                     │
├─────────────────────────────────────────────────────────────┤
│ □ Plan Mode for multi-file/risky work?                      │
│ □ Questions asked if ambiguous?                             │
│ □ Permissions deny secrets?                                 │
│ □ Baseline tests run?                                       │
│ □ Minimum diff applied?                                     │
│ □ Verification tests pass?                                  │
│ □ Context under control? (/compact if needed)               │
└─────────────────────────────────────────────────────────────┘
```
