#!/usr/bin/env python3
"""Auto-allow Claude Code permission prompts for this repo's .claude directory."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CLAUDE_DIR = ROOT / ".claude"


def _under_claude_dir(path_value: object, cwd_value: object) -> bool:
    if not isinstance(path_value, str) or not path_value.strip():
        return False

    raw = Path(path_value)
    base = Path(cwd_value) if isinstance(cwd_value, str) and cwd_value else ROOT
    candidate = raw if raw.is_absolute() else base / raw

    try:
        candidate = candidate.resolve()
        claude_dir = CLAUDE_DIR.resolve()
    except OSError:
        return False

    return candidate == claude_dir or claude_dir in candidate.parents


def _bash_touches_claude(command_value: object) -> bool:
    if not isinstance(command_value, str):
        return False

    command = command_value.strip()
    if ".claude" not in command:
        return False

    allowed_prefixes = (
        "mkdir ",
        "mkdir -p ",
        "rm ",
        "rm -r ",
        "rm -rf ",
        "ln ",
        "ln -s ",
        "cp ",
        "mv ",
        "chmod ",
        "touch ",
    )
    return command.startswith(allowed_prefixes)


def _allow() -> None:
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PermissionRequest",
                    "decision": {"behavior": "allow"},
                }
            }
        )
    )


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0

    if payload.get("hook_event_name") != "PermissionRequest":
        return 0

    tool_name = payload.get("tool_name")
    tool_input = payload.get("tool_input") or {}
    cwd = payload.get("cwd")

    if tool_name in {"Edit", "Write", "MultiEdit", "Update"}:
        if _under_claude_dir(tool_input.get("file_path"), cwd):
            _allow()
            return 0

    if tool_name == "Bash" and _bash_touches_claude(tool_input.get("command")):
        _allow()
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
