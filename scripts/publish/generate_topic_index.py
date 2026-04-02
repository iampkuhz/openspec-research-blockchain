#!/usr/bin/env python3
"""
生成 Topic 索引 Markdown 文件。

用法:
    python scripts/publish/generate_topic_index.py --output knowledge/indexes/topic-index.md
"""

import argparse
import yaml
from pathlib import Path
from datetime import datetime


def parse_args():
    parser = argparse.ArgumentParser(description='生成 Topic 索引')
    parser.add_argument('--knowledge-dir', default='knowledge/topics', help='Knowledge 目录')
    parser.add_argument('--output', default='knowledge/indexes/topic-index.md', help='输出文件')
    return parser.parse_args()


def scan_topics(knowledge_dir: str) -> list:
    """扫描所有 topics"""
    topics = []
    knowledge_path = Path(knowledge_dir)

    for overview_file in knowledge_path.rglob('overview.md'):
        topic_path = overview_file.parent
        topic_name = topic_path.name
        domain = topic_path.parent.name if topic_path.parent != knowledge_path else ''

        # 读取 frontmatter
        content = overview_file.read_text()
        metadata = {}

        if content.startswith('---'):
            lines = content.split('\n')
            in_frontmatter = False
            for line in lines:
                if line.strip() == '---':
                    if not in_frontmatter:
                        in_frontmatter = True
                        continue
                    else:
                        break
                if in_frontmatter and ':' in line:
                    key, value = line.split(':', 1)
                    metadata[key.strip()] = value.strip().strip('"')

        topics.append({
            'name': topic_name,
            'domain': domain,
            'path': str(topic_path.relative_to(knowledge_path)),
            'type': metadata.get('type', 'unknown'),
            'version': metadata.get('version', 'unknown'),
            'last_updated': metadata.get('last_updated', metadata.get('created_at', 'unknown')),
            'change_id': metadata.get('last_change_id', 'unknown'),
        })

    return sorted(topics, key=lambda x: (x['domain'], x['name']))


def generate_index(topics: list) -> str:
    """生成索引内容"""
    now = datetime.now().strftime('%Y-%m-%d %H:%M')

    content = f"""# Topic Index

最后更新：{now}

统计：共 {len(topics)} 个 topics

---

## By Domain

"""

    # 按 domain 分组
    domains = {}
    for topic in topics:
        domain = topic['domain'] or 'Unassigned'
        if domain not in domains:
            domains[domain] = []
        domains[domain].append(topic)

    for domain, domain_topics in sorted(domains.items()):
        content += f"### {domain}\n\n"
        content += "| Topic | Type | Version | Last Updated | Change ID |\n"
        content += "|-------|------|---------|--------------|----------|\n"

        for topic in domain_topics:
            content += (f"| [{topic['name']}](../topics/{topic['path']}/overview.md) | "
                       f"{topic['type']} | {topic['version']} | {topic['last_updated']} | "
                       f"{topic['change_id']} |\n")

        content += '\n'

    # 按类型统计
    content += "---\n\n## By Type\n\n"
    type_counts = {}
    for topic in topics:
        t = topic['type']
        type_counts[t] = type_counts.get(t, 0) + 1

    content += "| Type | Count |\n"
    content += "|------|-------|\n"
    for t, count in sorted(type_counts.items()):
        content += f"| {t} | {count} |\n"

    return content


def main():
    args = parse_args()
    topics = scan_topics(args.knowledge_dir)
    content = generate_index(topics)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content)

    print(f"Generated index with {len(topics)} topics at {output_path}")


if __name__ == '__main__':
    main()
