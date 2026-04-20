#!/usr/bin/env python3
"""
Adapter: draft_diagram_contract validator

Wraps scripts/research/validate_draft_diagram_contract.py.
Accepts a single file path from the dispatcher.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent.parent


def main():
    if len(sys.argv) < 2:
        print("Usage: draft_diagram_contract.py <draft.md>", file=sys.stderr)
        sys.exit(1)

    script = ROOT / "scripts" / "research" / "validate_draft_diagram_contract.py"
    result = subprocess.run(
        [sys.executable, str(script), sys.argv[1]],
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
