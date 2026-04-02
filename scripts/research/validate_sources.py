#!/usr/bin/env python3
"""
验证来源格式和完整性。

用法:
    python scripts/research/validate_sources.py --topic <topic>
"""

import argparse
import yaml
from pathlib import Path
from datetime import datetime


def parse_args():
    parser = argparse.ArgumentParser(description='验证来源格式')
    parser.add_argument('--topic', required=True, help='主题名称')
    parser.add_argument('--knowledge-dir', default='knowledge/topics', help='knowledge 目录')
    return parser.parse_args()


def validate_sources(topic: str, knowledge_dir: str) -> dict:
    """验证来源格式和完整性"""
    topic_path = Path(knowledge_dir) / topic
    results = {
        'topic': topic,
        'valid': True,
        'errors': [],
        'warnings': [],
        'summary': {},
    }

    # 检查 source-pack.yaml
    source_pack_file = topic_path / 'sources' / 'source-pack.yaml'
    if not source_pack_file.exists():
        results['errors'].append("Missing source-pack.yaml")
        results['valid'] = False
        return results

    with open(source_pack_file) as f:
        source_data = yaml.safe_load(f)

    if not source_data:
        results['errors'].append("Empty source-pack.yaml")
        results['valid'] = False
        return results

    sources = source_data.get('sources', [])
    results['summary']['total'] = len(sources)

    # 按 tier 统计
    tier_counts = {'L1': 0, 'L2': 0, 'L3': 0, 'L4': 0}
    type_counts = {}

    for i, source in enumerate(sources):
        # 检查必需字段
        required = ['source_id', 'title', 'source_type', 'source_tier']
        for field in required:
            if field not in source:
                results['errors'].append(f"Source {i}: missing required field '{field}'")
                results['valid'] = False

        # 检查 source_tier
        tier = source.get('source_tier')
        if tier in tier_counts:
            tier_counts[tier] += 1

        # 检查 source_type
        src_type = source.get('source_type')
        if src_type:
            type_counts[src_type] = type_counts.get(src_type, 0) + 1

        # 检查 accessed_at
        if 'accessed_at' not in source:
            results['warnings'].append(f"Source {source.get('source_id', i)}: missing accessed_at")

        # 检查 url 或本地引用
        if 'url' not in source and 'local_ref' not in source:
            results['warnings'].append(f"Source {source.get('source_id', i)}: missing url or local_ref")

        # 检查 supported_claims
        claims = source.get('supported_claims', [])
        if not claims:
            results['warnings'].append(f"Source {source.get('source_id', i)}: no supported_claims")

    results['summary']['by_tier'] = tier_counts
    results['summary']['by_type'] = type_counts

    # 检查证据分布
    l1_count = tier_counts.get('L1', 0)
    l2_count = tier_counts.get('L2', 0)
    if l1_count == 0 and l2_count == 0:
        results['warnings'].append("No L1 or L2 sources - technical claims may lack evidence")

    return results


def main():
    args = parse_args()
    results = validate_sources(args.topic, args.knowledge_dir)

    print(f"\n=== Source Validation Report: {results['topic']} ===\n")

    print(f"Valid: {'Yes' if results['valid'] else 'No'}\n")

    print("Summary:")
    print(f"  Total sources: {results['summary'].get('total', 0)}")
    if 'by_tier' in results['summary']:
        print(f"  By tier: {results['summary']['by_tier']}")
    if 'by_type' in results['summary']:
        print(f"  By type: {results['summary']['by_type']}")

    print("\nErrors:")
    if results['errors']:
        for error in results['errors']:
            print(f"  - {error}")
    else:
        print("  No errors!")

    print("\nWarnings:")
    if results['warnings']:
        for warning in results['warnings']:
            print(f"  - {warning}")
    else:
        print("  No warnings!")

    print()


if __name__ == '__main__':
    main()
