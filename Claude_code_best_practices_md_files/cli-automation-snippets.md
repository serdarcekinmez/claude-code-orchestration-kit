# CLI Automation Snippets

> **Copy-paste patterns for Claude Code automation.** Print mode, CI integration, and structured output.

---

## Print Mode Basics

Print mode (`-p` or `--print`) runs Claude Code non-interactively for scripting and CI.

```bash
# Basic print mode
claude -p "Explain what this code does"

# With stdin
cat src/utils.py | claude -p "Review this file for bugs"

# With file context
claude -p "What does this function do?" < src/auth.py
```

---

## Git Diff Review Pattern

Use Claude to review diffs before commits or in CI:

### Pre-Commit Review

```bash
# Review staged changes
git diff --cached | claude -p "Review this diff for:
1. Security issues (injection, auth bypass)
2. Logic errors
3. Missing error handling
4. Style violations

Report issues as a numbered list, or say 'No issues found.'"
```

### PR Review in CI

```bash
# Review PR diff against main
git diff main...HEAD | claude -p "Code review this PR diff. Focus on:
- Security vulnerabilities
- Breaking changes
- Test coverage gaps

Format: bullet list of concerns, or 'Approved' if none."
```

---

## Structured Output Formats

> **Note:** Output format flags may vary by version. Verify with `claude --help`.

### JSON Output (If Supported)

```bash
# Request JSON output
claude -p "List all TODO comments in this file" \
  --output-format json < src/main.py

# Example output structure
{
  "result": "...",
  "cost": {...},
  "duration": "..."
}
```

### Stream JSON (If Supported)

For real-time processing of responses:

```bash
# Stream JSON events
claude -p "Analyze this codebase" \
  --output-format stream-json

# Each line is a JSON event
{"type": "text", "content": "..."}
{"type": "result", "content": "..."}
```

### Fallback: Parse Text Output

If structured output isn't supported, parse text:

```bash
# Capture output
RESULT=$(claude -p "Is this code secure? Answer YES or NO only." < code.py)

# Check result
if [ "$RESULT" = "NO" ]; then
  echo "Security issue detected"
  exit 1
fi
```

---

## CI Gate Pattern: Fail on Issues

### Generic CI Script

```bash
#!/bin/bash
# ci-review.sh - Fail CI if issues found

# Run review
REVIEW=$(git diff main...HEAD | claude -p "Review for security issues.
If issues found, start response with 'ISSUES:'.
If no issues, start with 'OK:'")

# Check result
if [[ "$REVIEW" == ISSUES:* ]]; then
  echo "Security review failed:"
  echo "$REVIEW"
  exit 1
else
  echo "Security review passed"
  exit 0
fi
```

### GitHub Actions Example

```yaml
# .github/workflows/claude-review.yml
name: Claude Code Review

on:
  pull_request:
    branches: [main]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Get diff
        run: git diff origin/main...HEAD > pr.diff

      - name: Run Claude review
        run: |
          RESULT=$(cat pr.diff | claude -p "Review for security issues.
          Respond with 'PASS' if none, or 'FAIL: <reason>' if issues found.")

          if [[ "$RESULT" == FAIL:* ]]; then
            echo "::error::$RESULT"
            exit 1
          fi
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
```

---

## Linting and Analysis Patterns

### Code Style Check

```bash
# Check code style
claude -p "Does this code follow PEP 8? List violations or say 'Compliant'." \
  < src/module.py
```

### Documentation Check

```bash
# Check for missing docstrings
claude -p "List all public functions missing docstrings in this file." \
  < src/api.py
```

### Dependency Audit

```bash
# Review dependencies for security
cat requirements.txt | claude -p "Are any of these packages known to have
security vulnerabilities? List concerns or say 'No known issues.'"
```

---

## Extract and Process Pattern

### Extract Issues to File

```bash
# Extract issues to JSON-ish format for processing
git diff HEAD~1 | claude -p "List issues in this format:
- FILE: <path>
  LINE: <number>
  ISSUE: <description>

If no issues, output: NO_ISSUES" > review-output.txt

# Process output
if grep -q "NO_ISSUES" review-output.txt; then
  echo "Clean diff"
else
  echo "Issues found:"
  cat review-output.txt
fi
```

### Generate Report

```bash
# Generate markdown report
claude -p "Analyze this codebase and generate a markdown report with:
## Summary
## Security Concerns
## Recommendations" > REVIEW.md
```

---

## Prompt Templates for CI

### Security Review Prompt

```bash
SECURITY_PROMPT="Review this code for security issues:
- SQL injection
- XSS vulnerabilities
- Command injection
- Path traversal
- Hardcoded secrets
- Authentication bypass

Format:
PASS - if no issues
FAIL: <issue list> - if issues found"

git diff main...HEAD | claude -p "$SECURITY_PROMPT"
```

### Breaking Change Detection

```bash
BREAKING_PROMPT="Analyze this diff for breaking changes:
- API contract changes
- Removed public functions
- Changed function signatures
- Database schema changes

Respond with:
BREAKING: <list> - if breaking changes found
COMPATIBLE - if no breaking changes"

git diff main...HEAD | claude -p "$BREAKING_PROMPT"
```

---

## Error Handling in Scripts

### Timeout Handling

```bash
# Set timeout for long operations
timeout 60 claude -p "Analyze this large file" < big_file.py || {
  echo "Analysis timed out"
  exit 1
}
```

### Retry on Failure

```bash
# Retry pattern
MAX_RETRIES=3
RETRY=0

while [ $RETRY -lt $MAX_RETRIES ]; do
  if RESULT=$(claude -p "Quick check" < file.py 2>/dev/null); then
    echo "$RESULT"
    break
  fi
  RETRY=$((RETRY + 1))
  sleep 5
done
```

---

## Quick Reference

```
┌─────────────────────────────────────────────────────────────┐
│                 CLI AUTOMATION PATTERNS                      │
├─────────────────────────────────────────────────────────────┤
│ BASIC:                                                      │
│   claude -p "prompt"                                        │
│   cat file | claude -p "prompt"                             │
│   claude -p "prompt" < file                                 │
├─────────────────────────────────────────────────────────────┤
│ DIFF REVIEW:                                                │
│   git diff | claude -p "review for issues"                  │
│   git diff main...HEAD | claude -p "security review"        │
├─────────────────────────────────────────────────────────────┤
│ CI GATE:                                                    │
│   Check output for PASS/FAIL pattern                        │
│   Exit 1 on FAIL to break build                             │
├─────────────────────────────────────────────────────────────┤
│ OUTPUT (if supported):                                      │
│   --output-format json                                      │
│   --output-format stream-json                               │
└─────────────────────────────────────────────────────────────┘
```

---

## Related Docs

- [./claude-code-overview.md](./claude-code-overview.md) — CLI modes overview
- [./claude-code-workflow.md](./claude-code-workflow.md) — Workflow integration
- [./security-review-agent.md](./security-review-agent.md) — Security review prompts
