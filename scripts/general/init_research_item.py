#!/usr/bin/env python3
"""
初始化研究项目目录结构。

用法:
    python scripts/general/init_research_item.py --topic <topic-name> --type <primitive|synthesis|domain|decision>
"""

import argparse
import os
import shutil
from pathlib import Path
from datetime import datetime


def parse_args():
    parser = argparse.ArgumentParser(description='初始化研究项目目录结构')
    parser.add_argument('--topic', required=True, help='主题名称')
    parser.add_argument('--type', required=True,
                       choices=['primitive', 'synthesis', 'domain', 'decision'],
                       help='研究对象类型')
    parser.add_argument('--domain', help='所属域（可选）')
    parser.add_argument('--output', default='knowledge/topics', help='输出目录')
    return parser.parse_args()


def create_directory_structure(topic: str, topic_type: str, domain: str, output_dir: str):
    """创建 topic 目录结构"""

    if topic_type == 'domain':
        base_path = Path(output_dir).parent / 'domains' / domain
    elif topic_type == 'decision':
        base_path = Path(output_dir).parent / 'decisions' / domain / topic
    else:
        base_path = Path(output_dir) / domain / topic if domain else Path(output_dir) / topic

    # 创建目录树
    directories = [
        'atoms',
        'claims',
        'comparisons',
        'diagrams/models',
        'diagrams/source',
        'diagrams/build',
        'diagrams/reviews',
        'reviews',
        'sources',
        'terms',
    ]

    for dir_rel in directories:
        dir_path = base_path / dir_rel
        dir_path.mkdir(parents=True, exist_ok=True)
        # 创建.gitkeep
        (dir_path / '.gitkeep').touch()

    # 创建模板文件
    templates = {
        'overview.md': f'''---
topic: {topic}
version: "1.0"
type: {topic_type}
domain: {domain or "TBD"}
created_at: {datetime.now().isoformat()}
---

# {topic}

[概述]
''',
        'changelog.md': f'''# Changelog

## Version 1.0 ({datetime.now().strftime('%Y-%m-%d')})

**Change ID**: primitive-{topic}-pass-1

**Type**: new-topic

**Summary**: 初始版本
''',
        'claims/facts.yaml': f'''version: "1.0"
topic: {topic}
updated_at: {datetime.now().isoformat()}

facts: []
''',
        'sources/source-pack.yaml': f'''version: "1.0"
topic: {topic}
generated_at: {datetime.now().isoformat()}

sources: []
''',
    }

    for filename, content in templates.items():
        file_path = base_path / filename
        file_path.write_text(content)

    print(f"Created directory structure for {topic} at {base_path}")
    return base_path


def main():
    args = parse_args()
    create_directory_structure(
        topic=args.topic,
        topic_type=args.type,
        domain=args.domain,
        output_dir=args.output
    )


if __name__ == '__main__':
    main()
