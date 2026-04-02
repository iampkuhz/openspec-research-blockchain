#!/usr/bin/env python3
"""
验证 Diagram Model 格式和一致性。

用法:
    python scripts/diagrams/validate_diagram_model.py <model-file.yaml>
"""

import argparse
import yaml
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(description='验证 Diagram Model')
    parser.add_argument('model_file', help='Diagram model YAML 文件')
    return parser.parse_args()


def validate_model(model_file: str) -> dict:
    """验证 diagram model 格式"""
    results = {
        'valid': True,
        'errors': [],
        'warnings': [],
    }

    with open(model_file) as f:
        data = yaml.safe_load(f)

    if not data:
        results['errors'].append("Empty model file")
        results['valid'] = False
        return results

    # 检查必需字段
    required = ['diagram_id', 'source_atoms']
    for field in required:
        if field not in data:
            results['errors'].append(f"Missing required field: {field}")
            results['valid'] = False

    # 验证 components
    components = data.get('components', [])
    component_ids = set()

    for i, comp in enumerate(components):
        # 检查必需字段
        if 'id' not in comp:
            results['errors'].append(f"Component {i}: missing 'id' field")
            results['valid'] = False
            continue

        comp_id = comp['id']
        if comp_id in component_ids:
            results['errors'].append(f"Component {i}: duplicate id '{comp_id}'")
        component_ids.add(comp_id)

        # 检查 label
        if 'label' not in comp:
            results['warnings'].append(f"Component {comp_id}: missing 'label' field")

        # 检查 layer（如果有）
        layer = comp.get('layer')
        if layer and layer not in ['protocol', 'implementation', 'ecosystem', 'application']:
            results['warnings'].append(f"Component {comp_id}: unknown layer '{layer}'")

        # 检查 stereotype（如果有）
        stereotype = comp.get('stereotype')
        if stereotype and not stereotype.startswith('<<'):
            results['warnings'].append(f"Component {comp_id}: stereotype should be like '<<type>>'")

    # 验证 relationships
    relationships = data.get('relationships', [])
    for i, rel in enumerate(relationships):
        # 检查必需字段
        if 'from' not in rel:
            results['errors'].append(f"Relationship {i}: missing 'from' field")
            results['valid'] = False
        elif rel['from'] not in component_ids:
            results['errors'].append(f"Relationship {i}: 'from' references unknown component '{rel['from']}'")

        if 'to' not in rel:
            results['errors'].append(f"Relationship {i}: missing 'to' field")
            results['valid'] = False
        elif rel['to'] not in component_ids:
            results['errors'].append(f"Relationship {i}: 'to' references unknown component '{rel['to']}'")

        # 检查 type
        rel_type = rel.get('type')
        if rel_type and rel_type not in ['depends', 'implements', 'contains', 'processes', 'calls', 'creates']:
            results['warnings'].append(f"Relationship {i}: unusual type '{rel_type}'")

    # 检查组件覆盖率（source atoms 中的组件是否都在 model 中）
    source_atoms = data.get('source_atoms', [])
    if source_atoms:
        # 这里可以进一步检查 atoms 中提到的组件是否都在 model 中
        pass

    return results


def main():
    args = parse_args()
    results = validate_model(args.model_file)

    print(f"\n=== Diagram Model Validation: {args.model_file} ===\n")

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

    exit(0 if results['valid'] else 1)


if __name__ == '__main__':
    main()
