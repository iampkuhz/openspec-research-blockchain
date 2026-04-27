#!/usr/bin/env python3
"""
Backfill change.yaml for active changes that are missing their manifest.

Usage:
    python scripts/openspec/backfill_change_manifest.py --dry-run
    python scripts/openspec/backfill_change_manifest.py --write
"""

import argparse
import os
import sys
from pathlib import Path
from datetime import datetime


def parse_change_id_from_dirname(dirname: str) -> str:
    """Derive task_type from directory name prefix."""
    parts = dirname.split("-")
    if not parts:
        return "unknown"
    first = parts[0].lower()
    mapping = {
        "primitive": "primitive",
        "synthesis": "synthesis",
        "decision": "decision",
        "cr": "unknown",  # cr- prefix doesn't map cleanly
        "review": "unknown",
        "secondary": "unknown",
    }
    return mapping.get(first, "unknown")


def infer_change_operation(change_dir: Path) -> str:
    """Infer change_operation from directory name or existing files."""
    name = change_dir.name.lower()
    if "refresh" in name or "update" in name or "v2" in name:
        return "update"
    if "extend" in name:
        return "extend"
    if "supersede" in name:
        return "supersede"
    return "create"


def infer_publish_target(change_dir: Path, task_type: str) -> str:
    """Try to read publish target from publish.md or infer from change name."""
    publish_md = change_dir / "publish.md"
    if publish_md.exists():
        text = publish_md.read_text(errors="replace")
        for line in text.splitlines():
            if "knowledge/" in line and "to:" in line.lower():
                parts = line.split(":", 1)
                if len(parts) > 1 and "knowledge/" in parts[1]:
                    return parts[1].strip().strip("`").strip("'").strip('"')

    # Fallback: infer from change name
    if task_type == "primitive":
        topic = change_dir.name.replace("primitive-", "").replace("-pass-1", "").replace("-pass-2", "")
        return f"knowledge/analysis/primitives/blockchain-chains/{topic}/artifact.md"
    elif task_type == "synthesis":
        topic = change_dir.name.replace("synthesis-", "").replace("-pass-1", "").replace("-pass-2", "")
        return f"knowledge/analysis/synthesis/{topic}/artifact.md"
    elif task_type == "decision":
        topic = change_dir.name.replace("decision-", "").replace("-pass-1", "").replace("-pass-2", "")
        return f"knowledge/decisions/blockchain-chains/{topic}/artifact.md"

    return ""


def generate_change_yaml(change_dir: Path, dry_run: bool = False) -> dict:
    """Generate change.yaml content for a change directory."""
    change_id = change_dir.name
    task_type = parse_change_id_from_dirname(change_id)
    change_operation = infer_change_operation(change_dir)

    has_request = (change_dir / "request.md").exists()
    has_plan = (change_dir / "plan.md").exists()
    has_draft = (change_dir / "draft.md").exists()
    has_publish = (change_dir / "publish.md").exists()

    publish_target = infer_publish_target(change_dir, task_type)

    if task_type == "unknown" and has_request:
        req_text = (change_dir / "request.md").read_text(errors="replace").lower()
        if "对比" in req_text or "比较" in req_text or "synthesis" in req_text or "横向" in req_text:
            task_type = "synthesis"
        elif "选择" in req_text or "决策" in req_text or "decision" in req_text:
            task_type = "decision"
        else:
            task_type = "primitive"

    yaml_content = f"""id: {change_id}
schema: blockchain-research

task_type: {task_type}
change_operation: {change_operation}
execution_scope: single_artifact

instruction: "自动回填的 change manifest，请人工审查并补充 instruction。"

profile:
  task: {task_type}
  operation: {change_operation}

artifacts:
  request:
    path: request.md
"""
    if has_plan:
        yaml_content += "  plan:\n    path: plan.md\n"
    yaml_content += "  source_pack:\n    path: sources/source-pack.md\n"
    yaml_content += "  evidence_map:\n    path: sources/evidence-map.md\n"
    yaml_content += "  notes:\n    pattern: notes/*.md\n    required: false\n"
    yaml_content += "  claims:\n    pattern: claims/*.md\n    required: false\n"
    if has_draft:
        yaml_content += "  draft:\n    path: draft.md\n"
    yaml_content += "  review:\n    pattern: review/*.md\n    required: false\n"
    if has_publish:
        yaml_content += "  publish:\n    path: publish.md\n    required: true\n"

    yaml_content += f"""
validators:
  base:
    - required_files
    - markdown_sections
  profile:
    - traceability
  operation:
    - publish_targets
"""
    if publish_target:
        target_type = "knowledge_primitive"
        if task_type == "synthesis":
            target_type = "knowledge_synthesis"
        elif task_type == "decision":
            target_type = "knowledge_decision"
        yaml_content += f"""
publish_targets:
  - from: draft.md
    to: {publish_target}
    type: {target_type}
"""
    else:
        yaml_content += "\npublish_targets: []\n"

    return {
        "task_type": task_type,
        "change_operation": change_operation,
        "publish_target": publish_target,
        "yaml_content": yaml_content,
        "needs_manual_review": task_type == "unknown",
    }


def main():
    parser = argparse.ArgumentParser(description="Backfill change.yaml for active changes")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be written without writing")
    parser.add_argument("--write", action="store_true", help="Actually write change.yaml files")
    parser.add_argument("--changes-dir", default="openspec/changes", help="Changes directory")
    args = parser.parse_args()

    if not args.dry_run and not args.write:
        print("Specify --dry-run or --write")
        sys.exit(1)

    changes_dir = Path(args.changes_dir)
    if not changes_dir.exists():
        print(f"Changes directory not found: {changes_dir}")
        sys.exit(1)

    active_changes = sorted([
        d for d in changes_dir.iterdir()
        if d.is_dir()
        and d.name != "archive"
        and not d.name.startswith("_")
    ])

    stats = {"total": len(active_changes), "already_has_yaml": 0, "backfilled": 0, "needs_review": 0}

    print(f"Found {stats['total']} active changes")
    print(f"Changes dir: {changes_dir}")
    print(f"Mode: {'DRY RUN' if args.dry_run else 'WRITE'}")
    print()

    for change_dir in active_changes:
        change_yaml = change_dir / "change.yaml"
        if change_yaml.exists():
            stats["already_has_yaml"] += 1
            continue

        # Skip empty changes
        files = list(change_dir.iterdir())
        if not any(f.suffix == ".md" for f in files):
            print(f"SKIP (empty/no markdown): {change_dir.name}")
            continue

        result = generate_change_yaml(change_dir)

        if args.dry_run:
            review_flag = " [NEEDS MANUAL REVIEW]" if result["needs_manual_review"] else ""
            print(f"WOULD CREATE: {change_dir.name}/change.yaml | type={result['task_type']} | op={result['change_operation']}{review_flag}")
            stats["backfilled"] += 1
            if result["needs_manual_review"]:
                stats["needs_review"] += 1
        else:
            change_yaml.write_text(result["yaml_content"], encoding="utf-8")
            review_flag = " [NEEDS MANUAL REVIEW]" if result["needs_manual_review"] else ""
            print(f"CREATED: {change_dir.name}/change.yaml | type={result['task_type']} | op={result['change_operation']}{review_flag}")
            stats["backfilled"] += 1
            if result["needs_manual_review"]:
                stats["needs_review"] += 1

    print()
    print(f"Summary:")
    print(f"  Total active changes: {stats['total']}")
    print(f"  Already had change.yaml: {stats['already_has_yaml']}")
    print(f"  Backfilled: {stats['backfilled']}")
    print(f"  Needs manual review: {stats['needs_review']}")


if __name__ == "__main__":
    main()
