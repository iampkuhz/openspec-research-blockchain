#!/usr/bin/env python3
"""markdown_sections — 检查 Markdown artifact 的必要章节。

触发方式：post_write
输入：被修改的 Markdown 文件路径
输出：校验通过返回 0，失败返回非 0 并写入 validation/markdown_sections.md
"""

import os
import sys
import re


# 不同 artifact 类型的最小章节要求（可扩展）
SECTION_REQUIREMENTS = {
    "request.md": ["## 研究背景", "## 范围", "## 非目标"],
    "plan.md": ["## 研究路径", "## 完成标准"],
}


def main():
    if len(sys.argv) < 2:
        print("SKIP: no file specified")
        sys.exit(0)

    filepath = sys.argv[1]
    basename = os.path.basename(filepath)

    requirements = SECTION_REQUIREMENTS.get(basename, [])
    if not requirements:
        print(f"SKIP: no section requirements for {basename}")
        sys.exit(0)

    with open(filepath, "r") as fh:
        content = fh.read()

    missing = [s for s in requirements if s not in content]

    if missing:
        change_dir = find_change_dir(filepath)
        validation_dir = os.path.join(change_dir, "validation")
        os.makedirs(validation_dir, exist_ok=True)
        with open(os.path.join(validation_dir, "markdown_sections.md"), "w") as fh:
            fh.write(f"# markdown_sections 校验失败 ({basename})\n\n缺失章节：{', '.join(missing)}\n")
        print(f"FAIL: missing sections in {basename}: {', '.join(missing)}")
        sys.exit(1)

    print(f"PASS: {basename} has all required sections")
    sys.exit(0)


def find_change_dir(filepath):
    """向上查找包含 change.yaml 的目录。"""
    d = os.path.dirname(os.path.abspath(filepath))
    while d != os.path.dirname(d):
        if os.path.exists(os.path.join(d, "change.yaml")):
            return d
        d = os.path.dirname(d)
    return os.path.dirname(filepath)


if __name__ == "__main__":
    main()
