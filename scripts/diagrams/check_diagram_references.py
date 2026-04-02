#!/usr/bin/env python3
"""
检查 Diagram 引用的组件是否在 atoms 中有定义。

用法:
    python scripts/diagrams/check_diagram_references.py <diagram-id>
"""

import argparse
import yaml
import re
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(description='检查 Diagram 引用')
    parser.add_argument('diagram_id', help='Diagram ID')
    parser.add_argument('--topic', required=True, help='Topic 名称')
    parser.add_argument('--knowledge-dir', default='knowledge/topics', help='knowledge 目录')
    return parser.parse_args()


def check_references(diagram_id: str, topic: str, knowledge_dir: str) -> dict:
    """检查 diagram 引用的组件是否有定义"""
    results = {
        'diagram_id': diagram_id,
        'topic': topic,
        'valid': True,
        'errors': [],
        'warnings': [],
    }

    topic_path = Path(knowledge_dir) / topic

    # 读取 diagram model
    model_file = topic_path / 'diagrams' / 'models' / f'{diagram_id}-model.yaml'
    if not model_file.exists():
        results['errors'].append(f"Model file not found: {model_file}")
        results['valid'] = False
        return results

    with open(model_file) as f:
        model_data = yaml.safe_load(f)

    components = model_data.get('components', [])
    component_ids = {comp['id'] for comp in components if 'id' in comp}

    # 读取 atoms 检查组件定义
    atoms_dir = topic_path / 'atoms'
    defined_terms = set()

    if atoms_dir.exists():
        for atom_file in atoms_dir.glob('*.md'):
            content = atom_file.read_text()

            # 查找术语定义模式：**Term** : definition
            pattern = r'\*\*([^*]+)\*\*\s*:'
            matches = re.findall(pattern, content)
            for match in matches:
                defined_terms.add(match.strip())

    # 检查组件是否在 atoms 中有定义
    for comp_id in component_ids:
        if comp_id not in defined_terms:
            # 检查是否是常见术语的变体
            comp_id_lower = comp_id.lower()
            found_similar = False
            for term in defined_terms:
                if comp_id_lower in term.lower() or term.lower() in comp_id_lower:
                    found_similar = True
                    results['warnings'].append(
                        f"Component '{comp_id}' might be '{term}' (similar name)"
                    )
                    break

            if not found_similar:
                results['warnings'].append(
                    f"Component '{comp_id}' not found in atoms definitions"
                )

    # 检查 source atoms 是否存在
    source_atoms = model_data.get('source_atoms', [])
    for atom in source_atoms:
        atom_file = atoms_dir / f"{atom}.md"
        if not atom_file.exists():
            results['errors'].append(f"Source atom not found: {atom}.md")
            results['valid'] = False

    return results


def main():
    args = parse_args()
    results = check_references(args.diagram_id, args.topic, args.knowledge_dir)

    print(f"\n=== Diagram References Check: {results['diagram_id']} ===\n")
    print(f"Topic: {results['topic']}")
    print(f"Valid: {'Yes' if results['valid'] else 'No'}\n")

    print("Errors:")
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
