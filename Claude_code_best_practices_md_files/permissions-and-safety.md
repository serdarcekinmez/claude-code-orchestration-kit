# Permissions and Safety

> **Least privilege: deny access to secrets, grant only what's needed.** Configure permissions to minimize risk.

---

## Least Privilege Principle

### Rule

Grant the **minimum permissions** required to complete the task. Deny everything else by default.

### Why It Matters

- **Secrets protection:** Prevents accidental exposure of API keys, passwords, tokens
- **Blast radius:** Limits damage from mistakes or misuse
- **Audit trail:** Clear record of what's allowed
- **Defense in depth:** Multiple layers of protection

---

## Configuration Scopes

### Project Config (Repository-Level)

**Location:** `.claude/settings.json` in your repository

**Scope:** Applies to anyone using Claude Code in this project

**Use for:**
- Project-specific safe commands
- Deny patterns for project secrets
- Shared team conventions

### User Config (User-Level)

**Location:** User's home directory config

**Scope:** Applies to all projects for this user

**Use for:**
- Personal preferences
- Global deny patterns
- User-specific tool allowances

### Precedence

```
User Config (broader) → Project Config (specific) → Runtime flags (most specific)
```

More specific settings override broader ones.

---

## Safe Example: .claude/settings.json

```json
{
  "permissions": {
    "allow": [
      "Bash(pytest *)",
      "Bash(npm test*)",
      "Bash(npm run lint*)",
      "Bash(go test ./...)",
      "Bash(cargo test*)",
      "Bash(git status)",
      "Bash(git diff*)",
      "Bash(git log*)",
      "Bash(ls *)",
      "Bash(cat package.json)",
      "Bash(cat pyproject.toml)",
      "Bash(cat Cargo.toml)"
    ],
    "deny": [
      "Bash(cat *secret*)",
      "Bash(cat *.env*)",
      "Bash(cat *credentials*)",
      "Bash(cat **/secrets/**)",
      "Bash(cat **/*.key)",
      "Bash(cat **/*.pem)",
      "Bash(cat **/*.p12)",
      "Bash(cat **/id_rsa*)",
      "Bash(cat **/.aws/**)",
      "Bash(cat **/.ssh/**)",
      "Bash(rm -rf *)",
      "Bash(*--force*)",
      "Bash(*sudo*)",
      "Bash(*chmod 777*)"
    ]
  }
}
```

---

## Deny Patterns: What to Block

### Secrets and Credentials

| Pattern | Blocks |
|---------|--------|
| `*.env*` | Environment files (.env, .env.local, .env.production) |
| `*secret*` | Files with "secret" in name |
| `*credentials*` | Credential files |
| `**/*.key` | Private key files |
| `**/*.pem` | Certificate files |
| `**/*.p12` | PKCS#12 keystores |
| `**/id_rsa*` | SSH private keys |
| `**/.aws/**` | AWS credentials |
| `**/.ssh/**` | SSH configuration |

### Dangerous Operations

| Pattern | Blocks |
|---------|--------|
| `rm -rf *` | Recursive force delete |
| `*--force*` | Force flags (git push --force, etc.) |
| `*sudo*` | Elevated privileges |
| `*chmod 777*` | Overly permissive permissions |

---

## Allow Patterns: What to Permit

### Safe Read-Only Commands

```json
{
  "allow": [
    "Bash(git status)",
    "Bash(git diff*)",
    "Bash(git log*)",
    "Bash(ls *)",
    "Bash(pwd)",
    "Bash(which *)",
    "Bash(cat package.json)",
    "Bash(cat README.md)"
  ]
}
```

### Safe Test Commands

```json
{
  "allow": [
    "Bash(pytest *)",
    "Bash(npm test*)",
    "Bash(npm run test*)",
    "Bash(go test ./...)",
    "Bash(cargo test*)",
    "Bash(bundle exec rspec*)",
    "Bash(mix test*)"
  ]
}
```

### Safe Build Commands

```json
{
  "allow": [
    "Bash(npm run build*)",
    "Bash(npm run lint*)",
    "Bash(pip install -r requirements.txt)",
    "Bash(pip install -e .)",
    "Bash(go build ./...)",
    "Bash(cargo build*)"
  ]
}
```

---

## Additional Directories

If Claude needs access to files outside the project root:

```json
{
  "additionalDirectories": [
    "/path/to/shared/library",
    "/path/to/test/fixtures"
  ]
}
```

### Guidance

- **Include only what's needed** — Don't add entire home directories
- **Be specific** — `/home/user/projects/shared-lib` not `/home/user`
- **Review periodically** — Remove access when no longer needed

---

## Warnings: Dangerous Patterns

### Never Do This

```json
{
  "permissions": {
    "allow": ["*"]
  }
}
```
**Why:** Grants unrestricted access to everything.

### Avoid Skip-Permission Flags

```bash
# DON'T DO THIS
claude --dangerously-skip-permissions
claude --skip-permissions
```

**Why:** Bypasses all safety checks.

### Don't Blanket-Allow Bash

```json
{
  "permissions": {
    "allow": ["Bash(*)"]
  }
}
```

**Why:** Allows any command execution.

---

## Best Practices

### 1. Deny First, Then Allow

Start with restrictive deny patterns, then add specific allows:

```json
{
  "permissions": {
    "deny": [
      "Bash(*secret*)",
      "Bash(*.env*)",
      "Bash(*credentials*)"
    ],
    "allow": [
      "Bash(pytest *)",
      "Bash(npm test*)"
    ]
  }
}
```

### 2. Use Specific Patterns

```json
{
  "allow": [
    "Bash(pytest tests/unit/*)",
    "Bash(pytest tests/integration/*)"
  ]
}
```

Not:

```json
{
  "allow": ["Bash(pytest *)"]
}
```

### 3. Audit Regularly

Review `.claude/settings.json` periodically:
- Remove unused permissions
- Tighten overly broad patterns
- Add new secret patterns as needed

### 4. Version Control Your Config

Commit `.claude/settings.json` to your repository:
- Team consistency
- Audit history
- Peer review of permission changes

---

## Security Review Handoff

For sensitive operations, hand off to the [Security Review Agent](./security-review-agent.md):

```xml
<task>
Review the authentication changes for security issues.
</task>

<security-scope>
- Check for injection vulnerabilities
- Verify authorization logic
- Ensure secrets are not logged or exposed
- Review error messages for information leakage
</security-scope>

<constraint>
The security review agent respects permissions.deny.
It will NOT request or reveal secrets.
</constraint>
```

---

## Example: Interview About Permissions

When working in a new codebase, ask:

```
Before proceeding, I need to understand the security boundaries:

1. Are there any files I should NEVER read or modify?
   (e.g., production configs, secret stores)

2. What test commands are safe to run?
   (e.g., `npm test`, `pytest tests/`)

3. Are there any destructive commands I should avoid?
   (e.g., database migrations, deployment scripts)

4. Should I add these to .claude/settings.json deny patterns?
```

---

## Quick Reference

```
┌─────────────────────────────────────────────────────────────┐
│              PERMISSIONS SAFETY CHECKLIST                    │
├─────────────────────────────────────────────────────────────┤
│ DENY these patterns:                                        │
│   □ *.env*, *secret*, *credentials*                         │
│   □ **/*.key, **/*.pem, **/*.p12                           │
│   □ **/.aws/**, **/.ssh/**, **/id_rsa*                     │
│   □ rm -rf *, *--force*, *sudo*                            │
├─────────────────────────────────────────────────────────────┤
│ ALLOW only:                                                 │
│   □ Specific test commands                                  │
│   □ Read-only git operations                                │
│   □ Safe build/lint commands                                │
├─────────────────────────────────────────────────────────────┤
│ NEVER:                                                      │
│   □ Use --skip-permissions flags                            │
│   □ Allow Bash(*) or allow: ["*"]                          │
│   □ Add broad directories to additionalDirectories          │
└─────────────────────────────────────────────────────────────┘
```

---

## Related Docs

- [./orchestrator.md](./orchestrator.md) — Hub & always-on rules
- [./security-review-agent.md](./security-review-agent.md) — Security sub-agent
- [./claude-code-overview.md](./claude-code-overview.md) — Session setup
