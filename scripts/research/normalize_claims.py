#!/usr/bin/env python3
"""
标准化 claims 格式。

用法:
    python scripts/research/normalize_claims.py --topic <topic>
"""

import argparse
import yaml
from pathlib import Path
from datetime import datetime


def parse_args():
    parser = argparse.ArgumentParser(description='标准化 claims 格式')
    parser.add_argument('--topic', required=True, help='主题名称')
    parser.add_argument('--knowledge-dir', default='knowledge', help='knowledge 目录')
    parser.add_argument('--dry-run', action='store_true', help='仅显示变更，不实际写入')
    return parser.parse_args()


def normalize_claims(topic: str, knowledge_dir: str, dry_run: bool):
    """标准化 claims 格式"""
    topic_path = Path(knowledge_dir) / topic
    claims_file = topic_path / 'claims' / 'facts.yaml'

    if not claims_file.exists():
        print(f"Claims file not found for topic: {topic}")
        return

    with open(claims_file) as f:
        data = yaml.safe_load(f)

    if not data:
        print("Empty claims file")
        return

    changes = []

    # 标准化 claims
    claims = data.get('facts', [])
    for i, claim in enumerate(claims):
        claim_changes = []

        # 确保 claim_id 格式正确
        if 'claim_id' not in claim:
            new_id = f"claim-{i+1:03d}"
            claim['claim_id'] = new_id
            claim_changes.append(f"Added claim_id: {new_id}")

        # 确保 statement 存在
        if 'statement' not in claim:
            claim_changes.append("MISSING: statement field")

        # 确保 sources 是列表
        if 'sources' not in claim:
            claim['sources'] = []
            claim_changes.append("Added empty sources list")
        elif not isinstance(claim['sources'], list):
            claim['sources'] = [claim['sources']]
            claim_changes.append("Converted sources to list")

        # 确保 evidence_level 存在
        if 'evidence_level' not in claim:
            # 尝试从 sources 推断
            if claim['sources']:
                src = claim['sources'][0]
                if isinstance(src, dict):
                    tier = src.get('source_tier', 'L4')
                    claim['evidence_level'] = tier
                    claim_changes.append(f"Inferred evidence_level: {tier}")
            else:
                claim['evidence_level'] = 'unknown'
                claim_changes.append("Added evidence_level: unknown")

        # 确保 confidence 存在
        if 'confidence' not in claim:
            claim['confidence'] = 'medium'
            claim_changes.append("Added confidence: medium")

        # 确保 status 存在
        if 'status' not in claim:
            claim['status'] = 'active'
            claim_changes.append("Added status: active")

        # 确保 related_atoms 存在
        if 'related_atoms' not in claim:
            claim['related_atoms'] = []
            claim_changes.append("Added empty related_atoms list")

        if claim_changes:
            changes.append((claim.get('claim_id', f'claim-{i}'), claim_changes))

    # 更新元数据
    data['updated_at'] = datetime.now().isoformat()

    if dry_run:
        print("Dry run - changes that would be made:\n")
        for claim_id, claim_changes in changes:
            print(f"{claim_id}:")
            for change in claim_changes:
                print(f"  - {change}")
            print()
    else:
        # 写回文件
        with open(claims_file, 'w') as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

        print(f"Normalized claims for topic: {topic}")
        print(f"Total changes: {sum(len(c[1]) for c in changes)}")


def main():
    args = parse_args()
    normalize_claims(args.topic, args.knowledge_dir, args.dry_run)


if __name__ == '__main__':
    main()
