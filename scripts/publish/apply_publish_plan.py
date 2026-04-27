#!/usr/bin/env python3
"""
Apply publish plan: read publish.md and copy/move draft to knowledge target.

Usage:
    python scripts/publish/apply_publish_plan.py --change <change-id> --dry-run
    python scripts/publish/apply_publish_plan.py --change <change-id> --write
"""

import argparse
import os
import re
import shutil
import sys
from pathlib import Path


def parse_publish_md(publish_md_path: Path) -> list:
    """Parse publish.md and extract from/to mappings."""
    if not publish_md_path.exists():
        return []

    text = publish_md_path.read_text(encoding="utf-8")
    mappings = []

    # Look for table rows with from/to
    # Format: | draft.md | knowledge/... | type | strategy |
    for line in text.splitlines():
        if "knowledge/" in line and "from:" in line.lower():
            continue  # Skip header lines
        parts = [p.strip() for p in line.split("|") if p.strip()]
        if len(parts) >= 2:
            from_path = parts[0].strip()
            to_path = parts[1].strip()
            if to_path.startswith("knowledge/") and from_path.endswith(".md"):
                mappings.append({
                    "from": from_path,
                    "to": to_path,
                    "type": parts[2] if len(parts) > 2 else "",
                    "strategy": parts[3] if len(parts) > 3 else "create",
                })

    # Fallback: also check publish_targets in change.yaml
    if not mappings:
        change_yaml = publish_md_path.parent / "change.yaml"
        if change_yaml.exists():
            text = change_yaml.read_text(encoding="utf-8")
            in_targets = False
            current_from = "draft.md"
            for line in text.splitlines():
                if "publish_targets:" in line:
                    in_targets = True
                    continue
                if in_targets:
                    if line.strip().startswith("- from:"):
                        current_from = line.split(":", 1)[1].strip()
                    elif line.strip().startswith("to:") and "knowledge/" in line:
                        to_path = line.split(":", 1)[1].strip().strip("'").strip('"')
                        mappings.append({
                            "from": current_from,
                            "to": to_path,
                            "type": "",
                            "strategy": "create",
                        })
                    elif line.strip() and not line.strip().startswith("-") and not line.strip().startswith("to:") and not line.strip().startswith("from:") and not line.strip().startswith("type:"):
                        in_targets = False

    return mappings


def validate_mapping(mapping: dict, change_dir: Path) -> list:
    """Validate a publish mapping. Returns list of errors."""
    errors = []
    src = change_dir / mapping["from"]
    if not src.exists():
        errors.append(f"Source file not found: {mapping['from']}")
    if not mapping["to"].startswith("knowledge/"):
        errors.append(f"Target must start with knowledge/: {mapping['to']}")
    return errors


def apply_publish(mappings: list, change_dir: Path, base_dir: Path, dry_run: bool = True) -> bool:
    """Apply publish mappings."""
    if not mappings:
        print("No publish mappings found.")
        return False

    print(f"Found {len(mappings)} publish mapping(s)")

    all_valid = True
    for m in mappings:
        errors = validate_mapping(m, change_dir)
        if errors:
            all_valid = False
            for e in errors:
                print(f"  ERROR: {e}")
        else:
            src = change_dir / m["from"]
            dst = base_dir / m["to"]
            action = "DRY RUN: would copy" if dry_run else "COPY"
            print(f"  {action}: {m['from']} -> {m['to']}")

            if not dry_run:
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
                print(f"  Written: {dst}")

    return all_valid


def main():
    parser = argparse.ArgumentParser(description="Apply publish plan")
    parser.add_argument("--change", required=True, help="Change ID")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done")
    parser.add_argument("--write", action="store_true", help="Actually write files")
    parser.add_argument("--changes-dir", default="openspec/changes", help="Changes directory")
    parser.add_argument("--base-dir", default=".", help="Repository root")
    args = parser.parse_args()

    if not args.dry_run and not args.write:
        print("Specify --dry-run or --write")
        sys.exit(1)

    base_dir = Path(args.base_dir)
    change_dir = Path(args.changes_dir) / args.change

    if not change_dir.exists():
        print(f"Change directory not found: {change_dir}")
        sys.exit(1)

    publish_md = change_dir / "publish.md"
    mappings = parse_publish_md(publish_md)

    print(f"Change: {args.change}")
    print(f"Publish file: {publish_md}")
    print(f"Mode: {'DRY RUN' if args.dry_run else 'WRITE'}")
    print()

    valid = apply_publish(mappings, change_dir, base_dir, dry_run=args.dry_run)

    if not valid:
        print("\nValidation failed. Fix errors before writing.")
        sys.exit(1)
    else:
        print("\nAll mappings valid.")


if __name__ == "__main__":
    main()
