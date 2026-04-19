#!/usr/bin/env python3
"""
构建比较矩阵。

用法:
    python scripts/research/build_comparison_matrix.py --topics topic1,topic2,topic3 --output matrix.yaml
"""

import argparse
import yaml
from pathlib import Path
from datetime import datetime


def parse_args():
    parser = argparse.ArgumentParser(description='构建比较矩阵')
    parser.add_argument('--topics', required=True, help='逗号分隔的 topic 列表')
    parser.add_argument('--knowledge-dir', default='knowledge', help='knowledge 目录')
    parser.add_argument('--output', required=True, help='输出文件')
    parser.add_argument('--dimensions', nargs='+', default=['mechanism', 'performance', 'maturity'],
                       help='比较维度')
    return parser.parse_args()


def extract_topic_data(topic: str, knowledge_dir: str) -> dict:
    """从 topic 提取比较数据"""
    topic_path = Path(knowledge_dir) / topic
    data = {
        'topic': topic,
        'overview': None,
        'claims': [],
        'parameters': {},
    }

    # 读取 overview 获取基本信息
    overview_file = topic_path / 'overview.md'
    if overview_file.exists():
        data['overview'] = overview_file.read_text()[:500]  # 前 500 字

    # 读取 claims
    claims_file = topic_path / 'claims' / 'facts.yaml'
    if claims_file.exists():
        with open(claims_file) as f:
            claims_data = yaml.safe_load(f)
            if claims_data:
                data['claims'] = claims_data.get('facts', [])

    # 读取 limits-and-assumptions 获取参数
    limits_file = topic_path / 'atoms' / 'limits-and-assumptions.md'
    if limits_file.exists():
        data['parameters']['limits'] = limits_file.read_text()[:300]

    return data


def build_matrix(topics: list, knowledge_dir: str, dimensions: list) -> dict:
    """构建比较矩阵"""
    matrix = {
        'version': '1.0',
        'generated_at': datetime.now().isoformat(),
        'topics': topics,
        'dimensions': dimensions,
        'comparison': {},
    }

    # 提取每个 topic 的数据
    topic_data = {}
    for topic in topics:
        topic_data[topic] = extract_topic_data(topic, knowledge_dir)
        matrix['comparison'][topic] = {}

    # 填充维度数据（这里需要更复杂的逻辑来实际提取比较数据）
    for dim in dimensions:
        matrix['comparison'][f'dim_{dim}'] = {
            topic: 'TBD' for topic in topics
        }

    return matrix


def main():
    args = parse_args()
    topics = [t.strip() for t in args.topics.split(',')]

    matrix = build_matrix(topics, args.knowledge_dir, args.dimensions)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w') as f:
        yaml.dump(matrix, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

    print(f"Built comparison matrix for {len(topics)} topics: {output_path}")
    print(f"Dimensions: {', '.join(args.dimensions)}")
    print("\nNote: Matrix contains TBD values. Please fill in actual comparison data.")


if __name__ == '__main__':
    main()
