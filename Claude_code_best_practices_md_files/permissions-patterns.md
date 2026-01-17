# Permissions Patterns

> **Exact syntax and gotchas for Claude Code permissions.** Pattern matching rules, canonical examples, and enterprise considerations.

---

## Pattern Matching Rules

Claude Code permissions use **prefix matching** with glob-style patterns.

| Syntax | Meaning | Example |
|--------|---------|---------|
| `*` | Matches any characters (single segment) | `Bash(npm test*)` matches `npm test`, `npm test:unit` |
| `**` | Matches any path segments | `Bash(cat **/secrets/**)` matches any path containing `secrets/` |
| Literal | Exact match from start | `Bash(git status)` matches only `git status` |
| Prefix | Command must start with pattern | `Bash(pytest)` matches `pytest tests/` |

### Important: Prefix Matching

Patterns match from the **start** of the command:

```
Pattern: Bash(npm test)
✓ Matches: npm test
✓ Matches: npm test:unit
✓ Matches: npm test -- --coverage
✗ Does NOT match: sudo npm test
✗ Does NOT match: echo "npm test"
```

---

## Canonical Allow/Deny Examples

### Recommended Allow Patterns

```json
{
  "permissions": {
    "allow": [
      "Bash(pytest *)",
      "Bash(npm test*)",
      "Bash(npm run lint*)",
      "Bash(npm run build*)",
      "Bash(go test ./...)",
      "Bash(cargo test*)",
      "Bash(git status)",
      "Bash(git diff*)",
      "Bash(git log*)",
      "Bash(ls *)",
      "Bash(pwd)",
      "Bash(cat package.json)",
      "Bash(cat pyproject.toml)",
      "Bash(cat Cargo.toml)",
      "Bash(cat README*)"
    ]
  }
}
```

### Required Deny Patterns (Secrets)

```json
{
  "permissions": {
    "deny": [
      "Bash(cat .env*)",
      "Bash(cat **/secrets/**)",
      "Bash(cat **/*.key)",
      "Bash(cat **/*.pem)",
      "Bash(cat **/*.p12)",
      "Bash(cat **/id_rsa*)",
      "Bash(cat **/.aws/**)",
      "Bash(cat **/.ssh/**)",
      "Bash(cat **/credentials*)",
      "Bash(*sudo*)",
      "Bash(rm -rf *)",
      "Bash(*--force*)",
      "Bash(chmod 777*)"
    ]
  }
}
```

---

## Pattern Examples Table

| Pattern | Matches | Does NOT Match |
|---------|---------|----------------|
| `Bash(pytest *)` | `pytest tests/`, `pytest -v` | `python -m pytest` |
| `Bash(npm test*)` | `npm test`, `npm test:unit` | `npx test` |
| `Bash(git diff*)` | `git diff`, `git diff HEAD~1` | `git status` |
| `Bash(cat .env*)` | `cat .env`, `cat .env.local` | `cat env.txt` |
| `Bash(cat **/secrets/**)` | `cat config/secrets/api.key` | `cat secrets.txt` |
| `Bash(*sudo*)` | `sudo rm`, `echo sudo` | `sudoku` (unlikely command) |

---

## Deny Secrets From Context: Must-Have List

These patterns should **always** be denied to prevent secret exposure:

| Category | Patterns |
|----------|----------|
| **Environment files** | `.env*`, `*.env`, `.env.local`, `.env.production` |
| **Key files** | `**/*.key`, `**/*.pem`, `**/*.p12`, `**/id_rsa*` |
| **Cloud credentials** | `**/.aws/**`, `**/.gcp/**`, `**/.azure/**` |
| **SSH/Auth** | `**/.ssh/**`, `**/credentials*`, `**/secrets/**` |
| **Config with secrets** | `**/config/production*`, `**/*.secret.*` |

### Minimal Deny Block (Copy-Paste)

```json
{
  "permissions": {
    "deny": [
      "Bash(cat .env*)",
      "Bash(cat **/*.env)",
      "Bash(cat **/secrets/**)",
      "Bash(cat **/*.key)",
      "Bash(cat **/*.pem)",
      "Bash(cat **/.aws/**)",
      "Bash(cat **/.ssh/**)"
    ]
  }
}
```

---

## Enterprise Warning: Managed Settings

> **Warning:** In enterprise deployments, **managed settings override project settings**.

If your organization uses centrally managed Claude Code configuration:
- Project-level `.claude/settings.json` may be ignored
- Admin-defined permissions take precedence
- Check with your administrator for effective permissions

### How to Check

If permissions behave unexpectedly:
1. Check for organization-level settings
2. Verify no managed policy is overriding project config
3. Contact admin if patterns don't work as expected

---

## Complete Example: .claude/settings.json

```json
{
  "permissions": {
    "allow": [
      "Bash(pytest *)",
      "Bash(npm test*)",
      "Bash(npm run lint*)",
      "Bash(git status)",
      "Bash(git diff*)",
      "Bash(git log*)",
      "Bash(ls *)",
      "Bash(pwd)"
    ],
    "deny": [
      "Bash(cat .env*)",
      "Bash(cat **/secrets/**)",
      "Bash(cat **/*.key)",
      "Bash(cat **/*.pem)",
      "Bash(cat **/.aws/**)",
      "Bash(cat **/.ssh/**)",
      "Bash(*sudo*)",
      "Bash(rm -rf *)",
      "Bash(*--force*)"
    ]
  }
}
```

---

## Gotchas and Edge Cases

### Gotcha: Order Doesn't Matter (Usually)

Deny patterns are checked regardless of allow patterns. A command matching both allow and deny will be denied.

### Gotcha: Subshells and Pipes

Patterns match the **outer command**, not subshell contents:

```
Pattern: Bash(cat .env)
✓ Blocked: cat .env
✗ NOT blocked: bash -c "cat .env"
✗ NOT blocked: sh -c 'cat .env'
```

**Mitigation:** Also deny shell execution patterns if concerned:
```json
"Bash(bash -c *)",
"Bash(sh -c *)"
```

### Gotcha: Read Tool vs Bash

File read operations through Claude's native `Read` tool may not be affected by Bash permissions. Use `additionalDirectories` restrictions for file access control.

---

## Related Docs

- [./orchestrator.md](./orchestrator.md) — Permission rules overview
- [./permissions-and-safety.md](./permissions-and-safety.md) — Detailed safety configuration
- [./STOP-RULES.md](./STOP-RULES.md) — STOP when forbidden paths needed
- [./security-review-agent.md](./security-review-agent.md) — Security review patterns
