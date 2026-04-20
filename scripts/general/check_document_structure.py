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


def _is_ascii_art(block_content: str) -> bool:
    """判断代码块内容是否为 ASCII 框线图/架构图。"""
    # 如果语言标签本身表明是 ASCII art
    # （这个函数只接收 block_content，不含标签，标签判断在调用方做）
    # 通过特征字符判断：包含框线字符或 ASCII 艺术典型模式
    box_chars = set("│┌┐└┘├┤┬┴┼─│┏┓┗┛┣┫┳┻╋━┃")
    lines = block_content.split("\n")
    if not lines:
        return False
    # 如果超过一半的行包含框线字符，认为是 ASCII 框线图
    box_line_count = sum(1 for line in lines if any(c in box_chars for c in line))
    if box_line_count > len(lines) * 0.5:
        return True
    # 如果包含典型的 ASCII 艺术框图模式（+--+ 边框 + 内部文字）
    ascii_art_pattern = re.compile(r"^\s*[+|].*[+|]\s*$")
    art_lines = sum(1 for line in lines if ascii_art_pattern.match(line))
    if art_lines > len(lines) * 0.4:
        return True
    return False


def check_code_block_length(content: str, max_lines: int = 50) -> list[str]:
    """检查代码块不超过指定行数。PlantUML/Mermaid/ASCII 图表不做长度限制。"""
    errors = []
    in_code_block = False
    block_start = 0
    block_lines = 0
    block_lang = ""
    block_content = ""

    for line_no, line in enumerate(content.splitlines(), start=1):
        stripped = line.strip()
        if stripped.startswith("```"):
            if not in_code_block:
                in_code_block = True
                block_start = line_no
                block_lines = 0
                # 提取语言标识符
                block_lang = stripped.lstrip("`").strip().lower()
                block_content = ""
            else:
                in_code_block = False
                # PlantUML、Mermaid、ASCII 框线图不做长度限制
                lang_exempt = block_lang in ("plantuml", "mermaid", "ascii", "text", "txt")
                content_exempt = _is_ascii_art(block_content)
                if not lang_exempt and not content_exempt and block_lines > max_lines:
                    errors.append(
                        f"第 {block_start}-{line_no} 行: 代码块超过 {max_lines} 行（实际 {block_lines} 行）。"
                    )
                block_lines = 0
                block_lang = ""
                block_content = ""
        elif in_code_block:
            block_lines += 1
            block_content += line + "\n"

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
