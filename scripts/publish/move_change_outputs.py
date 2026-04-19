#!/usr/bin/env python3
"""
将 change 的产物移动到 knowledge 目录（新目录模型）。

按新目录模型落位：
- primitive → knowledge/analysis/primitives/<domain_id>/<topic_slug>/artifact.md
- synthesis → knowledge/analysis/synthesis/<topic_slug>/artifact.md
- decision → knowledge/decisions/<domain_id>/<topic_slug>/artifact.md + verdict.md

用法:
    python scripts/publish/move_change_outputs.py \
        --change <change-id> --topic <topic_slug> --type <primitive|synthesis|decision> \
        [--domain <domain_id>]
"""

import argparse
import subprocess
import shutil
import yaml
from pathlib import Path
from datetime import datetime


VALID_TYPES = {"primitive", "synthesis", "decision"}


def parse_args():
    parser = argparse.ArgumentParser(description="移动 change 产物到 knowledge（新模型）")
    parser.add_argument("--change", required=True, help="Change ID")
    parser.add_argument("--topic", required=True, help="Topic slug (topic_slug)")
    parser.add_argument("--type", required=True, choices=sorted(VALID_TYPES), help="对象类型")
    parser.add_argument("--domain", help="Domain ID（primitive/decision 必需）")
    parser.add_argument("--changes-dir", default="openspec/changes", help="Changes 目录")
    parser.add_argument("--knowledge-dir", default="knowledge", help="Knowledge 根目录")
    parser.add_argument("--archive", action="store_true", help="移动后归档 change")
    return parser.parse_args()


def run_validation(knowledge_dir: Path) -> list:
    """运行校验脚本，返回 errors"""
    errors = []
    scripts = [
        ["scripts/general/check_frontmatter.py", str(knowledge_dir)],
        ["scripts/general/validate_knowledge_tree.py", str(knowledge_dir)],
        ["scripts/research/check_artifact_contract.py", str(knowledge_dir)],
    ]
    for script in scripts:
        script_path = Path(script[0])
        if not script_path.exists():
            continue
        result = subprocess.run(
            ["python3"] + script,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            errors.append(f"{script[0]} failed:\n{result.stdout}\n{result.stderr}")
    return errors


def move_change_outputs(args) -> bool:
    """移动 change 产物到新目录模型"""

    change_path = Path(args.changes_dir) / args.change
    if not change_path.exists():
        print(f"Error: Change directory not found: {change_path}")
        return False

    knowledge_root = Path(args.knowledge_dir)

    # 确定目标路径
    if args.type == "primitive":
        if not args.domain:
            print("Error: --domain is required for primitive type")
            return False
        target_dir = knowledge_root / "analysis" / "primitives" / args.domain / args.topic
    elif args.type == "synthesis":
        target_dir = knowledge_root / "analysis" / "synthesis" / args.topic
    elif args.type == "decision":
        if not args.domain:
            print("Error: --domain is required for decision type")
            return False
        target_dir = knowledge_root / "decisions" / args.domain / args.topic
    else:
        print(f"Error: Unknown type: {args.type}")
        return False

    target_dir.mkdir(parents=True, exist_ok=True)

    # 从 draft.md 提炼 artifact.md
    draft_file = change_path / "draft.md"
    if draft_file.exists():
        shutil.copy2(draft_file, target_dir / "artifact.md")
        print(f"Copied draft.md → {target_dir / 'artifact.md'}")
    else:
        print(f"Warning: draft.md not found in {change_path}")

    # decision 类型需要 verdict.md
    if args.type == "decision":
        verdict_src = change_path / "verdict.md"
        if verdict_src.exists():
            shutil.copy2(verdict_src, target_dir / "verdict.md")
            print(f"Copied verdict.md → {target_dir / 'verdict.md'}")
        else:
            # 从 decision-criteria.md 或 draft 中提取
            criteria_src = change_path / "decision-criteria.md"
            if criteria_src.exists():
                shutil.copy2(criteria_src, target_dir / "verdict.md")
                print(f"Copied decision-criteria.md → verdict.md")
            else:
                print(f"Warning: no verdict source found for decision {args.topic}")

    # 运行校验
    print("\nRunning validation scripts...")
    errors = run_validation(knowledge_root)
    if errors:
        print("Validation errors found:")
        for e in errors:
            print(f"  {e}")
        print("\nProceeding anyway (review errors manually)")
    else:
        print("All validations passed!")

    # 归档
    if args.archive:
        archive_path = Path("openspec/archive") / args.change
        archive_path.parent.mkdir(exist_ok=True)
        shutil.move(change_path, archive_path)
        print(f"Archived change to {archive_path}")

    print(f"\nDone! Topic available at: {target_dir}")
    return True


def main():
    args = parse_args()
    success = move_change_outputs(args)
    exit(0 if success else 1)


if __name__ == "__main__":
    main()
