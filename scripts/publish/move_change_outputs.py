#!/usr/bin/env python3
"""
将 change 的产物移动到 knowledge 目录。

用法:
    python scripts/publish/move_change_outputs.py --change <change-id> --topic <topic>
"""

import argparse
import shutil
from pathlib import Path
from datetime import datetime


def parse_args():
    parser = argparse.ArgumentParser(description='移动 change 产物到 knowledge')
    parser.add_argument('--change', required=True, help='Change ID')
    parser.add_argument('--topic', required=True, help='Topic 名称')
    parser.add_argument('--changes-dir', default='openspec/changes', help='Changes 目录')
    parser.add_argument('--knowledge-dir', default='knowledge/topics', help='Knowledge 目录')
    parser.add_argument('--domain', help='Domain 名称')
    parser.add_argument('--archive', action='store_true', help='移动后归档 change')
    return parser.parse_args()


def move_change_outputs(change: str, topic: str, domain: str,
                       changes_dir: str, knowledge_dir: str, archive: bool):
    """移动 change 产物"""

    change_path = Path(changes_dir) / change
    if not change_path.exists():
        print(f"Error: Change directory not found: {change_path}")
        return False

    # 确定目标路径
    if domain:
        target_path = Path(knowledge_dir) / domain / topic
    else:
        target_path = Path(knowledge_dir) / topic

    # 创建目标目录结构
    directories = ['atoms', 'claims', 'sources', 'diagrams/build', 'diagrams/source',
                   'diagrams/reviews', 'terms']

    for dir_rel in directories:
        (target_path / dir_rel).mkdir(parents=True, exist_ok=True)

    # 复制 atoms
    atoms_src = change_path / 'atoms'
    if atoms_src.exists():
        for atom_file in atoms_src.glob('*.md'):
            shutil.copy2(atom_file, target_path / 'atoms' / atom_file.name)
        print(f"Copied atoms from {atoms_src}")

    # 复制 claims
    claims_src = change_path / 'claims'
    if claims_src.exists():
        for claim_file in claims_src.glob('*.yaml'):
            shutil.copy2(claim_file, target_path / 'claims' / claim_file.name)
        print(f"Copied claims from {claims_src}")

    # 复制 sources
    sources_src = change_path / 'sources'
    if sources_src.exists():
        # 复制 source-pack.yaml
        source_pack = sources_src / 'source-pack.yaml'
        if source_pack.exists():
            shutil.copy2(source_pack, target_path / 'sources' / 'source-pack.yaml')

        # 复制 excerpts
        excerpts_src = sources_src / 'excerpts'
        if excerpts_src.exists():
            excerpts_dst = target_path / 'sources' / 'excerpts'
            excerpts_dst.mkdir(exist_ok=True)
            for excerpt_file in excerpts_src.glob('*'):
                shutil.copy2(excerpt_file, excerpts_dst / excerpt_file.name)

        print(f"Copied sources from {sources_src}")

    # 复制 diagrams
    diagrams_src = change_path / 'diagrams'
    if diagrams_src.exists():
        for subdir in ['build', 'source', 'reviews']:
            src = diagrams_src / subdir
            if src.exists():
                dst = target_path / 'diagrams' / subdir
                for f in src.iterdir():
                    shutil.copy2(f, dst / f.name)
        print(f"Copied diagrams from {diagrams_src}")

    # 复制 overview/draft 到 overview.md
    draft_file = change_path / 'draft.md'
    if draft_file.exists():
        shutil.copy2(draft_file, target_path / 'overview.md')
        print(f"Copied draft.md to overview.md")

    # 创建/更新 changelog
    changelog_file = target_path / 'changelog.md'
    if not changelog_file.exists():
        changelog_content = f"""# Changelog

## Version 1.0 ({datetime.now().strftime('%Y-%m-%d')})

**Change ID**: {change}

**Type**: new-topic

**Summary**: Initial version from change

**Merged At**: {datetime.now().isoformat()}
"""
        changelog_file.write_text(changelog_content)
        print(f"Created changelog.md")

    # 归档
    if archive:
        archive_path = Path('openspec/archive') / change
        archive_path.parent.mkdir(exist_ok=True)
        shutil.move(change_path, archive_path)
        print(f"Archived change to {archive_path}")

    print(f"\nDone! Topic available at: {target_path}")
    return True


def main():
    args = parse_args()
    success = move_change_outputs(
        change=args.change,
        topic=args.topic,
        domain=args.domain,
        changes_dir=args.changes_dir,
        knowledge_dir=args.knowledge_dir,
        archive=args.archive
    )
    exit(0 if success else 1)


if __name__ == '__main__':
    main()
