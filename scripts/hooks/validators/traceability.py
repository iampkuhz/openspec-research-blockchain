#!/usr/bin/env python3
"""traceability — 检查从来源到知识目标的可追溯性。

触发方式：pre_publish / post_publish
输入：change 目录路径
输出：校验通过返回 0，失败返回非 0 并输出 JSON result
"""

import json
import os
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR.parent))
from lib.gate_result import make_result
from lib.markdown_utils import read_markdown


def main():
    change_dir = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    gate_id = sys.argv[2] if len(sys.argv) > 2 else "pre_publish"

    errors = []
    warnings = []
    checked_files = []

    # 检查 draft.md Traceability 是否存在
    draft_path = os.path.join(change_dir, "draft.md")
    if os.path.exists(draft_path):
        checked_files.append("draft.md")
        content = read_markdown(draft_path)
        if "Traceability" not in content and "traceability" not in content.lower():
            warnings.append("draft.md 未包含 Traceability 部分")

    # 检查 publish.md 是否引用 draft.md
    publish_path = os.path.join(change_dir, "publish.md")
    if os.path.exists(publish_path):
        checked_files.append("publish.md")
        content = read_markdown(publish_path)
        if "draft.md" not in content and "Draft" not in content:
            warnings.append("publish.md 未引用 draft.md")

    # 检查 sources 目录
    source_pack = os.path.join(change_dir, "sources", "source-pack.md")
    if os.path.exists(source_pack):
        checked_files.append("sources/source-pack.md")

    status = "warn" if (warnings and not errors) else ("fail" if errors else "pass")
    exit_code = 1 if status == "fail" else 0

    result = make_result(
        gate_id=gate_id,
        validator="traceability",
        status=status,
        blocking=False,
        checked_files=checked_files,
        errors=errors,
        warnings=warnings,
        rule_refs=["harness/rules/research/traceability-rules.md"],
        metadata={"change_dir": change_dir},
    )
    print(json.dumps(result))
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
