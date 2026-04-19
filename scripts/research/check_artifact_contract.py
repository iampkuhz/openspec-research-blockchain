#!/usr/bin/env python3
"""
按 object_type + research_depth 校验 artifact.md 的最小章节集合。

职责：
- 按 object_type + research_depth 校验最小章节集合
- 检查 primitive 的 deep / focused / light 是否满足对应最低结构
- 检查 synthesis 是否包含依赖对象说明
- 检查 decision 是否同时存在 artifact 与 verdict 的契约关系

用法:
    python scripts/research/check_artifact_contract.py knowledge/
"""

import sys
from pathlib import Path
import yaml


# 各 depth 对应的最低章节要求
PRIMITIVE_SECTIONS = {
    "deep": [
        "关键术语",
        "研究范围",
        "结构与角色",
        "核心流程",
        "设计取舍或机制原理",
        "能力边界",
    ],
    "focused": [
        "关键术语",
        "研究范围",
        "能力边界",
    ],
    "light": [
        "关键术语",
        "研究范围",
        "能力边界",
    ],
}

SYNTHESIS_SECTIONS = {
    "deep": [
        "研究问题",
        "依赖对象",
        "分析框架",
        "对象定位",
        "关系分析",
    ],
    "focused": [
        "研究问题",
        "依赖对象",
        "分析框架",
    ],
    "light": [
        "研究问题",
        "依赖对象",
    ],
}

DECISION_SECTIONS = {
    "deep": [
        "场景定义",
        "判断维度",
        "依赖抽取",
        "对比分析",
    ],
    "focused": [
        "场景定义",
        "判断维度",
        "依赖抽取",
    ],
    "light": [
        "场景定义",
    ],
}


def extract_headings(file_path: Path) -> list:
    """提取 Markdown 文件的二级标题"""
    headings = []
    content = file_path.read_text()
    for line in content.split("\n"):
        if line.startswith("## "):
            heading = line[3:].strip()
            headings.append(heading)
    return headings


def check_artifact(file_path: Path) -> list:
    """检查单个 artifact.md 的内容契约"""
    errors = []
    warnings = []

    if file_path.name != "artifact.md":
        return errors, warnings

    content = file_path.read_text()
    if not content.startswith("---"):
        errors.append(f"Missing frontmatter")
        return errors, warnings

    # 解析 frontmatter
    lines = content.split("\n")
    fm_lines = []
    in_fm = False
    for line in lines:
        if line.strip() == "---":
            if not in_fm:
                in_fm = True
                continue
            else:
                break
        if in_fm:
            fm_lines.append(line)

    try:
        fm = yaml.safe_load("\n".join(fm_lines))
    except yaml.YAMLError:
        errors.append("Invalid YAML in frontmatter")
        return errors, warnings

    if not fm:
        errors.append("Empty frontmatter")
        return errors, warnings

    object_type = fm.get("object_type")
    research_depth = fm.get("research_depth", "light")

    if not object_type:
        errors.append("Missing object_type in frontmatter")
        return errors, warnings

    headings = extract_headings(file_path)

    # 根据类型和深度检查章节
    sections_map = {
        "primitive": PRIMITIVE_SECTIONS,
        "synthesis": SYNTHESIS_SECTIONS,
        "decision": DECISION_SECTIONS,
    }

    if object_type not in sections_map:
        errors.append(f"Unknown object_type: {object_type}")
        return errors, warnings

    required_sections = sections_map.get(object_type, {}).get(research_depth, [])
    for section in required_sections:
        # 模糊匹配：检查 heading 是否包含 required section 关键词
        found = any(section in h for h in headings)
        if not found:
            errors.append(
                f"Missing required section '{section}' for {object_type}/{research_depth}"
            )

    # 检查 decision 是否同时有 verdict.md
    if object_type == "decision":
        verdict_path = file_path.parent / "verdict.md"
        if not verdict_path.exists():
            warnings.append("Decision artifact found without accompanying verdict.md")

        # 检查 verdict.md 的 frontmatter
        if verdict_path.exists():
            verdict_content = verdict_path.read_text()
            if not verdict_content.startswith("---"):
                errors.append(f"verdict.md missing frontmatter")

    return errors, warnings


def main():
    if len(sys.argv) < 2:
        print("Usage: python check_artifact_contract.py knowledge/")
        sys.exit(1)

    target = Path(sys.argv[1])
    if not target.exists():
        print(f"Path not found: {target}")
        sys.exit(1)

    all_errors = []
    all_warnings = []

    for artifact_path in target.rglob("artifact.md"):
        errors, warnings = check_artifact(artifact_path)
        if errors:
            all_errors.append((artifact_path, errors))
        if warnings:
            all_warnings.append((artifact_path, warnings))

    if all_warnings:
        print("Warnings:")
        for file_path, warns in all_warnings:
            print(f"  {file_path}:")
            for w in warns:
                print(f"    [warning] {w}")
        print()

    if all_errors:
        print(f"Found issues in {len(all_errors)} artifacts:\n")
        for file_path, errs in all_errors:
            print(f"{file_path}:")
            for e in errs:
                print(f"  [error] {e}")
            print()
        sys.exit(1)
    else:
        print("All artifact contracts look good!")
        sys.exit(0)


if __name__ == "__main__":
    main()
