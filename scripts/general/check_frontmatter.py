#!/usr/bin/env python3
"""
检查 frontmatter 格式。

用法:
    python scripts/general/check_frontmatter.py [file|directory]
"""

import sys
from pathlib import Path
import yaml


def check_frontmatter(file_path: Path) -> list:
    """检查单个文件的 frontmatter"""
    errors = []
    content = file_path.read_text()

    if not content.startswith('---'):
        errors.append(f"Missing frontmatter (should start with '---')")
        return errors

    lines = content.split('\n')
    frontmatter_lines = []
    in_frontmatter = False

    for i, line in enumerate(lines):
        if line.strip() == '---':
            if not in_frontmatter:
                in_frontmatter = True
                continue
            else:
                break
        if in_frontmatter:
            frontmatter_lines.append(line)

    # 解析 frontmatter
    try:
        frontmatter = yaml.safe_load('\n'.join(frontmatter_lines))
    except yaml.YAMLError as e:
        errors.append(f"Invalid YAML in frontmatter: {e}")
        return errors

    if frontmatter is None:
        errors.append("Empty frontmatter")
        return errors

    # 检查必需字段
    required_fields = {
        'overview.md': ['topic', 'version', 'type'],
    }

    filename = file_path.name
    if filename in required_fields:
        for field in required_fields[filename]:
            if field not in frontmatter:
                errors.append(f"Missing required field: {field}")

    # 检查字段格式
    if 'version' in frontmatter:
        version = frontmatter['version']
        if not isinstance(version, str):
            errors.append(f"Version should be a string (quoted), got: {type(version)}")

    return errors


def main():
    if len(sys.argv) < 2:
        print("Usage: python check_frontmatter.py [file|directory]")
        sys.exit(1)

    target = Path(sys.argv[1])
    all_errors = []

    if target.is_file():
        errors = check_frontmatter(target)
        if errors:
            all_errors.append((target, errors))
    elif target.is_dir():
        for md_file in target.rglob('*.md'):
            errors = check_frontmatter(md_file)
            if errors:
                all_errors.append((md_file, errors))

    if all_errors:
        print(f"Found issues in {len(all_errors)} files:\n")
        for file_path, errors in all_errors:
            print(f"{file_path}:")
            for error in errors:
                print(f"  - {error}")
            print()
        sys.exit(1)
    else:
        print("All frontmatter looks good!")
        sys.exit(0)


if __name__ == '__main__':
    main()
