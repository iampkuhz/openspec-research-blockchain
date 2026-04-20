#!/usr/bin/env python3
"""
Adapter: document_structure validator

Wraps scripts/general/check_document_structure.py.
Accepts a single file path from the dispatcher.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent.parent


def main():
    if len(sys.argv) < 2:
        print("Usage: document_structure.py <file.md> [file.md ...]", file=sys.stderr)
        sys.exit(1)

    script = ROOT / "scripts" / "general" / "check_document_structure.py"
    files = sys.argv[1:]
    result = subprocess.run(
        [sys.executable, str(script)] + files,
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
