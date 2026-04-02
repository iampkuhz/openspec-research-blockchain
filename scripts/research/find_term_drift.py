#!/usr/bin/env python3
"""
查找术语漂移（同一术语在不同地方的定义不一致）。

用法:
    python scripts/research/find_term_drift.py --term <term> [--topic <topic>]
"""

import argparse
import re
from pathlib import Path
from collections import defaultdict


def parse_args():
    parser = argparse.ArgumentParser(description='查找术语漂移')
    parser.add_argument('--term', required=True, help='术语名称')
    parser.add_argument('--topic', help='限定在特定 topic')
    parser.add_argument('--knowledge-dir', default='knowledge', help='knowledge 目录')
    return parser.parse_args()


def find_term_definitions(term: str, knowledge_dir: str, topic_filter: str = None) -> dict:
    """查找术语的所有定义"""
    results = {
        'term': term,
        'definitions': [],
        'usages': defaultdict(list),
    }

    # 确定搜索范围
    if topic_filter:
        search_paths = [Path(knowledge_dir) / 'topics' / topic_filter]
    else:
        search_paths = [Path(knowledge_dir)]

    for base_path in search_paths:
        if not base_path.exists():
            continue

        # 查找术语定义
        for md_file in base_path.rglob('*.md'):
            content = md_file.read_text()

            # 查找术语定义模式
            # 如：**UserOperation** : 定义
            pattern = r'\*\*(' + re.escape(term) + r')\*\*\s*:\s*(.+?)(?:\n|$)'
            matches = re.findall(pattern, content, re.MULTILINE)

            for match in matches:
                definition = match[1].strip()
                results['definitions'].append({
                    'file': str(md_file.relative_to(knowledge_dir)),
                    'definition': definition,
                })

            # 查找术语使用
            if term in content:
                rel_path = str(md_file.relative_to(knowledge_dir))
                # 计算出现次数
                count = content.count(term)
                results['usages'][rel_path].append(count)

    return results


def detect_drift(definitions: list) -> list:
    """检测定义是否一致"""
    drifts = []

    if len(definitions) < 2:
        return drifts

    # 简单比较：检查定义长度差异
    first_def = definitions[0]['definition']
    first_len = len(first_def)

    for i, defn in enumerate(definitions[1:], 1):
        curr_def = defn['definition']
        curr_len = len(curr_def)

        # 如果长度差异超过 50%，可能存在问题
        if first_len > 0:
            diff_ratio = abs(curr_len - first_len) / first_len
            if diff_ratio > 0.5:
                drifts.append({
                    'files': [definitions[0]['file'], defn['file']],
                    'issue': f'Definition length differs by {diff_ratio*100:.0f}%',
                    'definitions': [first_def, curr_def],
                })

    return drifts


def main():
    args = parse_args()

    results = find_term_definitions(
        term=args.term,
        knowledge_dir=args.knowledge_dir,
        topic_filter=args.topic
    )

    print(f"\n=== Term Definition Report: {results['term']} ===\n")

    print(f"Definitions found: {len(results['definitions'])}\n")

    for i, defn in enumerate(results['definitions'], 1):
        print(f"{i}. File: {defn['file']}")
        print(f"   Definition: {defn['definition'][:100]}...")
        print()

    print("Usages:")
    for file, counts in results['usages'].items():
        total = sum(counts)
        print(f"  {file}: {total} occurrences")

    # 检测漂移
    drifts = detect_drift(results['definitions'])
    if drifts:
        print("\n=== Potential Drift Detected ===\n")
        for drift in drifts:
            print(f"Issue: {drift['issue']}")
            print(f"Files: {drift['files']}")
            print()
    else:
        print("\nNo obvious drift detected.")

    print()


if __name__ == '__main__':
    main()
