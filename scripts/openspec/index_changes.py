#!/usr/bin/env python3
"""
Generate openspec/changes/_index.yaml from active changes.

Usage:
    python scripts/openspec/index_changes.py --dry-run
    python scripts/openspec/index_changes.py --write
"""

import argparse
import os
import sys
from pathlib import Path
from datetime import datetime

try:
    import yaml
except ImportError:
    print("PyYAML not installed. Install with: pip install pyyaml")
    print("Using fallback YAML generation...")
    yaml = None


def read_change_yaml(change_dir: Path) -> dict:
    """Read change.yaml and return relevant fields."""
    change_file = change_dir / "change.yaml"
    if not change_file.exists():
        return {}

    text = change_file.read_text(encoding="utf-8")
    if yaml:
        return yaml.safe_load(text) or {}

    # Fallback: simple key extraction
    result = {}
    for line in text.splitlines():
        for key in ["task_type", "change_operation", "id"]:
            if line.startswith(f"{key}:"):
                result[key] = line.split(":", 1)[1].strip()
    return result


def read_publish_targets(change_dir: Path) -> list:
    """Read publish_targets from change.yaml."""
    change_file = change_dir / "change.yaml"
    if not change_file.exists():
        return []

    text = change_file.read_text(encoding="utf-8")
    targets = []
    in_targets = False
    for line in text.splitlines():
        if line.startswith("publish_targets:"):
            in_targets = True
            continue
        if in_targets:
            stripped = line.strip()
            if stripped.startswith("to:") and "knowledge/" in stripped:
                targets.append(stripped.split(":", 1)[1].strip().strip("'").strip('"'))
            elif stripped and not stripped.startswith("-") and not stripped.startswith("to:") and not stripped.startswith("from:") and not stripped.startswith("type:"):
                in_targets = False
    return targets


def scan_changes(changes_dir: Path) -> list:
    """Scan active changes and return list of change info dicts."""
    changes = []
    for d in sorted(changes_dir.iterdir()):
        if not d.is_dir():
            continue
        if d.name in ("archive",):
            continue
        if d.name.startswith("_"):
            continue

        change_info = read_change_yaml(d)
        if not change_info:
            # No change.yaml, mark as needs_review
            change_info = {
                "task_type": "unknown",
                "change_operation": "unknown",
                "id": d.name,
            }

        targets = read_publish_targets(d)
        has_manifest = (d / "change.yaml").exists()

        changes.append({
            "id": change_info.get("id", d.name),
            "task_type": change_info.get("task_type", "unknown"),
            "change_operation": change_info.get("change_operation", "unknown"),
            "has_manifest": has_manifest,
            "target_paths": targets,
            "path": f"openspec/changes/{d.name}",
        })

    return changes


def generate_yaml(changes: list) -> str:
    """Generate _index.yaml content."""
    lines = [
        "# changes 索引",
        "# 由 scripts/openspec/index_changes.py 自动生成，请勿手动编辑。",
        "version: 1",
        "index_type: changes",
        "",
        "changes:",
    ]

    for c in changes:
        lines.append(f"  {c['id']}:")
        lines.append(f"    path: {c['path']}")
        lines.append(f"    task_type: {c['task_type']}")
        lines.append(f"    change_operation: {c['change_operation']}")
        lines.append(f"    has_manifest: {'true' if c['has_manifest'] else 'false'}")
        if c["target_paths"]:
            lines.append("    target_paths:")
            for t in c["target_paths"]:
                lines.append(f"      - {t}")
        lines.append("")

    lines.append("# deprecated; kept for backward compatibility")
    lines.append("sessions: {}")
    lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate _index.yaml from active changes")
    parser.add_argument("--dry-run", action="store_true", help="Show output without writing")
    parser.add_argument("--write", action="store_true", help="Write _index.yaml")
    parser.add_argument("--changes-dir", default="openspec/changes", help="Changes directory")
    args = parser.parse_args()

    if not args.dry_run and not args.write:
        print("Specify --dry-run or --write")
        sys.exit(1)

    changes_dir = Path(args.changes_dir)
    if not changes_dir.exists():
        print(f"Changes directory not found: {changes_dir}")
        sys.exit(1)

    changes = scan_changes(changes_dir)
    output = generate_yaml(changes)

    if args.dry_run:
        print(output)
    else:
        index_file = changes_dir / "_index.yaml"
        index_file.write_text(output, encoding="utf-8")
        print(f"Written {index_file} with {len(changes)} changes")


if __name__ == "__main__":
    main()
