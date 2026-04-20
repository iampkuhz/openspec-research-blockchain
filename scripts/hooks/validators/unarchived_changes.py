#!/usr/bin/env python3
"""
Adapter: unarchived_changes validator

Wraps scripts/general/check_unarchived_changes.py.
No file arguments needed.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent.parent


def main():
    script = ROOT / "scripts" / "general" / "check_unarchived_changes.py"
    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
