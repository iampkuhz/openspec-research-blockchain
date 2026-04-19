#!/usr/bin/env python3
"""
检查知识可追溯性（claims → sources → atoms 关联）。

用法:
    python scripts/general/check_traceability.py --topic <topic>
"""

import argparse
import yaml
from pathlib import Path
from collections import defaultdict


def parse_args():
    parser = argparse.ArgumentParser(description='检查知识可追溯性')
    parser.add_argument('--topic', required=True, help='主题名称')
    parser.add_argument('--knowledge-dir', default='knowledge', help='knowledge 目录')
    return parser.parse_args()


def check_traceability(topic: str, knowledge_dir: str) -> dict:
    """检查 topic 的可追溯性"""
    topic_path = Path(knowledge_dir) / topic
    results = {
        'topic': topic,
        'claims': {'total': 0, 'with_sources': 0, 'orphan_sources': []},
        'atoms': {'total': 0, 'with_claims': 0, 'missing_claims': []},
        'sources': {'total': 0, 'used': 0, 'unused': []},
        'issues': [],
    }

    # 检查 claims
    claims_file = topic_path / 'claims' / 'facts.yaml'
    if claims_file.exists():
        with open(claims_file) as f:
            claims_data = yaml.safe_load(f)

        claims = claims_data.get('facts', []) if claims_data else []
        results['claims']['total'] = len(claims)

        source_ids = set()
        for claim in claims:
            sources = claim.get('sources', [])
            if sources:
                results['claims']['with_sources'] += 1
                for src in sources:
                    source_ids.add(src.get('source_id'))
            else:
                results['issues'].append(f"{claim.get('claim_id', 'unknown')}: missing sources")

    # 检查 sources
    source_pack_file = topic_path / 'sources' / 'source-pack.yaml'
    if source_pack_file.exists():
        with open(source_pack_file) as f:
            source_data = yaml.safe_load(f)

        sources = source_data.get('sources', []) if source_data else []
        results['sources']['total'] = len(sources)

        used_sources = set()
        for src in sources:
            used_sources.add(src.get('source_id'))

        # 检查未使用的 sources
        # (需要在后续检查 claims 中实际引用的 sources)

    # 检查 atoms 中的 claims 引用
    atoms_dir = topic_path / 'atoms'
    if atoms_dir.exists():
        for atom_file in atoms_dir.glob('*.md'):
            results['atoms']['total'] += 1
            content = atom_file.read_text()

            # 检查是否有 claim 引用
            if '← claim-' in content or 'claim-' in content:
                results['atoms']['with_claims'] += 1
            else:
                results['atoms']['missing_claims'].append(atom_file.name)

    return results


def main():
    args = parse_args()
    results = check_traceability(args.topic, args.knowledge_dir)

    print(f"\n=== Traceability Report: {results['topic']} ===\n")

    print("Claims:")
    print(f"  Total: {results['claims']['total']}")
    print(f"  With sources: {results['claims']['with_sources']}")
    if results['claims']['total'] > 0:
        pct = results['claims']['with_sources'] / results['claims']['total'] * 100
        print(f"  Coverage: {pct:.1f}%")

    print("\nAtoms:")
    print(f"  Total: {results['atoms']['total']}")
    print(f"  With claims references: {results['atoms']['with_claims']}")
    if results['atoms']['missing_claims']:
        print(f"  Missing claims references: {', '.join(results['atoms']['missing_claims'])}")

    print("\nSources:")
    print(f"  Total: {results['sources']['total']}")

    print("\nIssues:")
    if results['issues']:
        for issue in results['issues']:
            print(f"  - {issue}")
    else:
        print("  No issues found!")

    print()


if __name__ == '__main__':
    main()
