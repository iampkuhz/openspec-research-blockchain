#!/usr/bin/env python3
"""
检查 knowledge/ 下 artifact.md 是否以 TOC（目录）开头。

TOC 应覆盖所有一级和二级标题，使用标准 Markdown 列表格式。

用法:
    python scripts/general/check_artifact_toc.py <file1> <file2> ...
    python scripts/general/check_artifact_toc.py knowledge/

返回码:
    0: 所有检查通过
    1: 发现 error 级别问题
"""

import re
import sys
from pathlib import Path


def extract_headings(content: str) -> list:
    """提取内容中的 ## 级别标题（跳过 frontmatter）"""
    # 跳过 frontmatter
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            content = parts[2]

    headings = []
    for line in content.split("\n"):
        line = line.strip()
        if line.startswith("## "):
            heading = line[3:].strip()
            headings.append(heading)
    return headings


def extract_toc(content: str) -> list:
    """提取 TOC 中列出的标题"""
    # 跳过 frontmatter
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            content = parts[2]

    toc_entries = []
    in_toc = False
    for line in content.split("\n"):
        stripped = line.strip()
        # TOC 以 - [xxx](#xxx) 或 * [xxx](#xxx) 格式出现
        # 或简单的 - xxx 格式
        if stripped.startswith("- [") or stripped.startswith("* ["):
            in_toc = True
            # 提取标题文本：- [标题](#slug)
            match = re.match(r'^[-*]\s+\[([^\]]+)\]', stripped)
            if match:
                toc_entries.append(match.group(1).strip())
        elif in_toc and not stripped.startswith("- ") and not stripped.startswith("* "):
            # 遇到非 TOC 行，TOC 结束
            break

    return toc_entries


def check_toc(file_path: Path) -> list:
    errors = []
    content = file_path.read_text()

    # 检查是否有 TOC
    toc = extract_toc(content)
    if not toc:
        errors.append("Missing TOC: artifact.md must start with a table of contents after frontmatter")
        return errors

    # 提取实际标题（跳过 frontmatter，跳过 "目录"——TOC 自身不需要覆盖自己）
    headings = []
    for h in extract_headings(content):
        if h != "目录":
            headings.append(h)
    if not headings:
        return errors  # 没有标题，不需要 TOC

    # 检查 TOC 是否覆盖了所有标题
    missing = []
    for h in headings:
        found = any(h in t or t in h for t in toc)
        if not found:
            missing.append(h)

    if missing:
        errors.append(f"TOC missing coverage for: {', '.join(missing)}")

    return errors


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/general/check_artifact_toc.py knowledge/ | <file1> <file2> ...")
        sys.exit(1)

    all_errors = []

    if len(sys.argv) == 2 and sys.argv[1].startswith("knowledge/"):
        # 全量扫描
        for artifact_path in Path(sys.argv[1]).rglob("artifact.md"):
            errs = check_toc(artifact_path)
            if errs:
                all_errors.append((artifact_path, errs))
    else:
        # 指定文件
        for f in sys.argv[1:]:
            fp = Path(f)
            if fp.name == "artifact.md" and fp.exists():
                errs = check_toc(fp)
                if errs:
                    all_errors.append((fp, errs))

    if all_errors:
        print("TOC validation failed:\n")
        for fp, errs in all_errors:
            print(f"{fp}:")
            for e in errs:
                print(f"  [error] {e}")
            print()
        sys.exit(1)
    else:
        print("TOC validation passed.")
        sys.exit(0)


if __name__ == "__main__":
    main()
