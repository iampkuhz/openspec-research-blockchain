#!/usr/bin/env python3
"""
校验 knowledge/ 下 artifact.md / verdict.md 的前置质量门。

用于 git pre-commit hook 与 CI，拦截不符合规约的写入。

检查项：
1. frontmatter 合法性（字段、枚举、deprecated field 拒绝）
2. artifact contract（frontmatter 存在性、object_type、最小章节）

用法:
    python scripts/general/check_knowledge_artifacts.py          # 全量检查 knowledge/
    python scripts/general/check_knowledge_artifacts.py f1 f2    # 只检查指定文件

返回码:
    0: 所有检查通过
    1: 发现 error 级别问题
"""

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent.parent


def run_check(script: str, *args: str) -> tuple:
    """运行校验脚本，返回 (stdout, stderr, returncode)"""
    result = subprocess.run(
        [sys.executable, str(ROOT / script), *args],
        capture_output=True,
        text=True,
    )
    return result.stdout, result.stderr, result.returncode


def main():
    # 如果传入了文件参数，只检查这些文件；否则全量扫描 knowledge/
    if len(sys.argv) > 1:
        # 只保留 knowledge/ 下的 artifact.md 和 verdict.md
        target_files = [
            f for f in sys.argv[1:]
            if f.startswith("knowledge/") and f.endswith((".md",))
            and ("/artifact.md" in f or "/verdict.md" in f)
        ]
        if not target_files:
            print("No knowledge/ artifact files changed; skipping validation.")
            sys.exit(0)
    else:
        target_files = [str(ROOT / "knowledge")]

    has_error = False

    # 第一层：frontmatter 校验
    out, err, rc = run_check("scripts/general/check_frontmatter.py", *target_files)
    if rc != 0:
        has_error = True
    if out:
        print(out)
    if err:
        print(err, file=sys.stderr)

    # 第二层：artifact contract 校验（只对 artifact.md）
    artifact_files = [f for f in target_files if "/artifact.md" in f]
    if artifact_files or not target_files:
        check_target = artifact_files if artifact_files else [str(ROOT / "knowledge")]
        out, err, rc = run_check("scripts/research/check_artifact_contract.py", *check_target)
        if rc != 0:
            has_error = True
        if out:
            print(out)
        if err:
            print(err, file=sys.stderr)

    if has_error:
        print("Knowledge artifact validation FAILED. Commit blocked.")
        sys.exit(1)
    else:
        print("Knowledge artifact validation passed.")
        sys.exit(0)


if __name__ == "__main__":
    main()
