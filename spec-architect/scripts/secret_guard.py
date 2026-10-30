#!/usr/bin/env python3
"""PreToolUse hook: block Read, Grep, Bash and PowerShell calls that touch secret files.

Exit 2 blocks the tool call; stderr tells Claude why.
Heuristic: catches common paths, not every possible way to read a file.
"""
import json
import re
import sys

SECRET = re.compile(
    r"((?<![\w-])\.env(\.[\w-]+)?\b|\.(pem|key|p12|pfx|keystore)\b|id_rsa|id_ed25519|"
    r"\.ssh/|\.aws/|\.netrc|credentials(\.json)?\b|secrets?/|\.npmrc|\.pypirc)",
    re.IGNORECASE,
)
ALLOWED = re.compile(r"\.env\.(example|sample|template)\b", re.IGNORECASE)
ENV_DUMP = re.compile(
    r"(^|[;&|]\s*)(env|printenv)(\s*$|\s*[;&|])"
    r"|\b(Get-ChildItem|gci|dir|ls)\s+env:|GetEnvironmentVariables\(",
    re.IGNORECASE,
)
SHELL_TOOLS = ("Bash", "PowerShell")


def touches_secret(text: str) -> bool:
    # Windows paths arrive with backslashes; match on forward slashes.
    return bool(SECRET.search(ALLOWED.sub("", text.replace("\\", "/"))))


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0
    tool = data.get("tool_name", "")
    inp = data.get("tool_input", {})

    if tool in SHELL_TOOLS:
        cmd = inp.get("command", "")
        if touches_secret(cmd) or ENV_DUMP.search(cmd):
            reason = "this command reads a secret file or dumps environment variables"
        else:
            return 0
    elif tool in ("Read", "Grep"):
        target = " ".join(str(inp.get(k, "")) for k in ("file_path", "path", "glob"))
        if not touches_secret(target):
            return 0
        reason = "this path looks like a secret file"
    else:
        return 0

    print(
        f"Blocked by secret_guard: {reason}. Secrets must never enter the conversation. "
        "Read configuration through environment variable NAMES only, and use "
        ".env.example to see which variables exist.",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
