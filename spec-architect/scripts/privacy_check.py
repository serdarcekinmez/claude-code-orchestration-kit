#!/usr/bin/env python3
"""PostToolUse hook: flag likely PII leaks in files Claude writes.

Exit 0 = fine. Exit 2 = problems; stderr is sent back to Claude to fix.
Heuristic, not a guarantee: it catches common mistakes, not every leak.
Sensitive field names come from <project>/.claude/pii-fields.txt.
"""
import json
import re
import sys
from pathlib import Path

EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@([A-Za-z0-9.-]+\.[A-Za-z]{2,})")
SAFE_DOMAINS = {"example.com", "example.org", "example.net", "test.com"}
IBAN = re.compile(r"\b[A-Z]{2}\d{2}(?:\s?[A-Z0-9]{4}){3,7}\b")
OUTPUT_CALLS = re.compile(
    r"print\(|console\.log|logging\.|logger\.|innerHTML|textContent|"
    r"\.to_csv\(|\.to_excel\(|render_template|jsonify\("
)
CHECKED_EXT = {".py", ".js", ".ts", ".jsx", ".tsx", ".html", ".css", ".json", ".sql"}


def load_fields(cwd: Path) -> list[str]:
    f = cwd / ".claude" / "pii-fields.txt"
    if not f.is_file():
        return []
    return [
        line.strip().lower()
        for line in f.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0
    path = Path(data.get("tool_input", {}).get("file_path", ""))
    if path.suffix.lower() not in CHECKED_EXT or not path.is_file():
        return 0

    fields = load_fields(Path(data.get("cwd", ".")))
    problems = []
    text = path.read_text(encoding="utf-8", errors="ignore")
    for n, line in enumerate(text.splitlines(), 1):
        for m in EMAIL.finditer(line):
            if m.group(1).lower() not in SAFE_DOMAINS:
                problems.append(f"line {n}: real-looking email address (put it in config/env)")
        if IBAN.search(line):
            problems.append(f"line {n}: IBAN-like number")
        low = line.lower()
        if fields and OUTPUT_CALLS.search(line) and any(f in low for f in fields):
            problems.append(f"line {n}: sensitive field sent to display, log or export")

    if problems:
        print(
            f"Privacy check failed for {path.name}:\n"
            + "\n".join(problems[:10])
            + "\nUse customer IDs or masked values instead (see SPEC.md > Privacy).",
            file=sys.stderr,
        )
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
