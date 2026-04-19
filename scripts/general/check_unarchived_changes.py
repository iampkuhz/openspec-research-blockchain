#!/usr/bin/env python3
"""
检查是否存在已归档但 change 目录仍留在 openspec/changes/ 下的情况。

在 commit 涉及 knowledge/ 时触发：如果 knowledge/ 下的 artifact 已存在，
但对应的 change 目录未归档（仍在 openspec/changes/ 而非 openspec/archive/），
则发出警告。

注意：这是 advisory 检查，不会阻止 commit。

用法:
    python scripts/general/check_unarchived_changes.py

返回码:
    0: 没有问题
    1: 发现未归档的 change（advisory warning）
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent


def main():
    changes_dir = ROOT / "openspec" / "changes"
    archive_dir = ROOT / "openspec" / "archive"

    if not changes_dir.exists():
        print("No openspec/changes/ directory found.")
        sys.exit(0)

    # 获取已归档的 change IDs
    archived_ids = set()
    if archive_dir.exists():
        for d in archive_dir.iterdir():
            if d.is_dir():
                archived_ids.add(d.name)

    # 检查 openspec/changes/ 下的目录（排除 archive/ 子目录）
    unarchived = []
    for d in sorted(changes_dir.iterdir()):
        if d.is_dir() and d.name != "archive":
            change_id = d.name
            if change_id in archived_ids:
                # 已归档但仍在 changes/ 下（可能重复）
                unarchived.append(change_id)

    # 更实用的检查：看 knowledge/ 下是否有 artifact，但 openspec/changes/ 下还有对应目录
    knowledge_dir = ROOT / "knowledge"
    if knowledge_dir.exists():
        for artifact_path in knowledge_dir.rglob("artifact.md"):
            rel = artifact_path.relative_to(knowledge_dir)
            parts = rel.parts
            # analysis/primitives/<domain>/<topic>/artifact.md
            # analysis/synthesis/<topic>/artifact.md
            # decisions/<domain>/<topic>/artifact.md
            if len(parts) >= 4 and parts[1] == "primitives":
                topic_slug = parts[3]
            elif len(parts) >= 3 and parts[1] == "synthesis":
                topic_slug = parts[2]
            elif len(parts) >= 3 and parts[0] == "decisions":
                topic_slug = parts[2]
            else:
                continue

            # 检查对应 change 是否仍在 openspec/changes/ 下
            change_path = changes_dir / topic_slug
            archive_path = archive_dir / topic_slug
            if change_path.exists() and not archive_path.exists():
                unarchived.append(f"{topic_slug} (artifact exists but change not archived)")

    # Deduplicate
    seen = set()
    unique_unarchived = []
    for item in unarchived:
        key = item.split(" ")[0] if " (" in item else item
        if key not in seen:
            seen.add(key)
            unique_unarchived.append(item)

    if unique_unarchived:
        print("WARNING: Unarchived changes detected (advisory only):")
        for item in unique_unarchived:
            print(f"  - {item}")
        print("\nRun: mv openspec/changes/<id>/ openspec/archive/<id>/")
        sys.exit(0)  # Advisory only, don't block commit
    else:
        print("Change archiving check passed.")
        sys.exit(0)


if __name__ == "__main__":
    main()
