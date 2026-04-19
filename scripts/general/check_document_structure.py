#!/usr/bin/env python3
"""校验 Markdown 文档的结构约束。

检查项：
1. 标题深度不超过 H4（禁止 ##### 及以上）
2. 列表嵌套不超过 3 层
3. 代码块不超过 50 行

用法:
    python scripts/general/check_document_structure.py <file.md> [file.md ...]

返回码:
    0: 校验通过
    1: 校验失败（至少一个文件有问题）
"""

import re
import sys
from pathlib import Path


def check_heading_depth(content: str) -> list[str]:
    """检查标题深度不超过 H4。"""
    errors = []
    in_code_block = False
    for line_no, line in enumerate(content.splitlines(), start=1):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue
        if stripped.startswith("#####") and not stripped.startswith("######"):
            errors.append(
                f"第 {line_no} 行: 禁止使用 H5 标题（#####）。"
            )
        elif stripped.startswith("######"):
            errors.append(
                f"第 {line_no} 行: 禁止使用 H6 标题（######）。最大允许 H4。"
            )
    return errors


def check_list_nesting(content: str) -> list[str]:
    """检查列表嵌套不超过 3 层。"""
    errors = []
    in_code_block = False
    for line_no, line in enumerate(content.splitlines(), start=1):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue
        if not stripped:
            continue
        # 计算行首空格数
        leading_spaces = len(line) - len(line.lstrip())
        # 检查是否是列表项
        if re.match(r"^[\s]*[-*+]\s", line) or re.match(r"^[\s]*\d+\.\s", line):
            # 每 2 个空格或 1 个 tab 算一层嵌套
            nesting_level = leading_spaces // 2
            if nesting_level >= 3:  # 0-indexed: 0,1,2 是允许的，3 就是第 4 层
                errors.append(
                    f"第 {line_no} 行: 列表嵌套超过 3 层（当前约第 {nesting_level + 1} 层）。"
                )
    return errors


def check_code_block_length(content: str, max_lines: int = 50) -> list[str]:
    """检查代码块不超过指定行数。PlantUML/Mermaid 图表不做长度限制。"""
    errors = []
    in_code_block = False
    block_start = 0
    block_lines = 0
    block_lang = ""

    for line_no, line in enumerate(content.splitlines(), start=1):
        stripped = line.strip()
        if stripped.startswith("```"):
            if not in_code_block:
                in_code_block = True
                block_start = line_no
                block_lines = 0
                # 提取语言标识符
                block_lang = stripped.lstrip("`").strip().lower()
            else:
                in_code_block = False
                # PlantUML 和 Mermaid 图表不做长度限制
                if block_lang not in ("plantuml", "mermaid") and block_lines > max_lines:
                    errors.append(
                        f"第 {block_start}-{line_no} 行: 代码块超过 {max_lines} 行（实际 {block_lines} 行）。"
                    )
                block_lines = 0
                block_lang = ""
        elif in_code_block:
            block_lines += 1

    if in_code_block:
        errors.append(f"第 {block_start} 行: 代码块未闭合。")

    return errors


def check_file(file_path: Path) -> list[str]:
    """校验单个文件。"""
    if not file_path.exists():
        return [f"文件不存在: {file_path}"]

    content = file_path.read_text(encoding="utf-8")
    errors = []
    errors.extend(check_heading_depth(content))
    errors.extend(check_list_nesting(content))
    errors.extend(check_code_block_length(content))
    return errors


def main() -> int:
    if len(sys.argv) < 2:
        print("用法: python check_document_structure.py <file.md> [file.md ...]", file=sys.stderr)
        return 1

    all_errors = []
    for arg in sys.argv[1:]:
        file_path = Path(arg)
        errors = check_file(file_path)
        if errors:
            all_errors.append((str(file_path), errors))

    if all_errors:
        for file_path, errors in all_errors:
            print(f"\n[错误] {file_path}:")
            for error in errors:
                print(f"  - {error}")
        return 1

    print("Document structure check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
