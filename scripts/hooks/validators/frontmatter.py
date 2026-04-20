#!/usr/bin/env python3
"""
Adapter: frontmatter validator

Wraps scripts/general/check_frontmatter.py.
Runs on the entire knowledge/ directory.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent.parent


def main():
    script = ROOT / "scripts" / "general" / "check_frontmatter.py"
    result = subprocess.run(
        [sys.executable, str(script), "knowledge"],
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
