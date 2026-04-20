#!/usr/bin/env python3
"""
Adapter: traceability validator

Wraps scripts/general/check_traceability.py.
Passes through extra arguments (--topic etc.) from the dispatcher.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent.parent


def main():
    script = ROOT / "scripts" / "general" / "check_traceability.py"
    # Pass through all extra args (--topic, --knowledge-dir, etc.)
    extra = sys.argv[1:]
    result = subprocess.run(
        [sys.executable, str(script)] + extra,
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
