#!/usr/bin/env python3
"""
检查 request.md / plan.md 是否包含最小必需字段。

用于 git pre-commit hook，拦截不完整的 process 文件。

用法:
    python scripts/general/check_process_files.py <file1> <file2> ...

返回码:
    0: 所有检查通过
    1: 发现 error 级别问题
"""

import sys
from pathlib import Path


REQUIRED_REQUEST_FIELDS = ["research_type", "research_path"]
REQUIRED_PLAN_FIELDS = ["研究深度", "来源", "完成标准"]


def check_request(file_path: Path) -> list:
    errors = []
    content = file_path.read_text()

    for field in REQUIRED_REQUEST_FIELDS:
        if field not in content:
            errors.append(f"Missing required field '{field}' in request.md")

    return errors


def check_plan(file_path: Path) -> list:
    errors = []
    content = file_path.read_text()

    # 检查 plan.md 是否包含关键章节标题
    for section in REQUIRED_PLAN_FIELDS:
        if section not in content:
            errors.append(f"Missing required section '{section}' in plan.md")

    return errors


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/general/check_process_files.py <file1> <file2> ...")
        sys.exit(1)

    all_errors = []

    for f in sys.argv[1:]:
        fp = Path(f)
        if not fp.exists():
            continue

        if fp.name == "request.md":
            errs = check_request(fp)
        elif fp.name == "plan.md":
            errs = check_plan(fp)
        else:
            continue

        if errs:
            all_errors.append((fp, errs))

    if all_errors:
        print("Found issues in process files:\n")
        for fp, errs in all_errors:
            print(f"{fp}:")
            for e in errs:
                print(f"  [error] {e}")
            print()
        sys.exit(1)
    else:
        print("Process files validation passed.")
        sys.exit(0)


if __name__ == "__main__":
    main()
