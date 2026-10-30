#!/usr/bin/env python3
"""PostToolUse hook: flag secrets written into files.

Exit 2 sends the findings back to Claude. The matched value is never printed.
Heuristic safety net; gitleaks at commit time is the second net.
"""
import json
import re
import sys
from pathlib import Path

PATTERNS = {
    "Anthropic API key": r"sk-ant-[A-Za-z0-9_-]{20,}",
    "OpenAI API key": r"sk-(?!ant-)(proj-)?[A-Za-z0-9_-]{20,}",
    "AWS access key": r"\bAKIA[0-9A-Z]{16}\b",
    "GitHub token": r"\bgh[pousr]_[A-Za-z0-9]{36,}\b",
    "Slack token": r"\bxox[abprs]-[A-Za-z0-9-]{10,}",
    "Google API key": r"\bAIza[0-9A-Za-z_-]{35}\b",
    "Private key": r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    "Hard-coded credential": (
        r"(?i)\b(password|passwd|pwd|secret|api_?key|access_?token|auth_?token)\b"
        r"\s*[:=]\s*[\"'][^\"'\s]{8,}[\"']"
    ),
}
PLACEHOLDER = re.compile(
    r"(?i)(changeme|your[_-]|example|placeholder|xxx|dummy|fake|test|<|\$\{|os\.environ|getenv)"
)
SKIP_NAMES = {".env.example", ".env.sample", ".env.template"}


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0
    path = Path(data.get("tool_input", {}).get("file_path", ""))
    if path.name in SKIP_NAMES or not path.is_file():
        return 0
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return 0

    findings = []
    for n, line in enumerate(lines, 1):
        for label, pattern in PATTERNS.items():
            m = re.search(pattern, line)
            if m and not PLACEHOLDER.search(m.group(0)):
                findings.append(f"line {n}: {label}")

    if findings:
        print(
            f"Secret scan failed for {path.name}:\n"
            + "\n".join(findings[:10])
            + "\nRemove the value, read it from an environment variable, and add "
            "the variable NAME to .env.example. If this was a real key, tell the "
            "user to rotate it.",
            file=sys.stderr,
        )
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
