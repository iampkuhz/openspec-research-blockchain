#!/usr/bin/env python3
"""review_readiness — 检查 review.md 的评审准备状态。

触发方式：post_review
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
from lib.markdown_utils import read_markdown, has_heading


def main():
    change_dir = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    gate_id = sys.argv[2] if len(sys.argv) > 2 else "post_review"

    review_path = os.path.join(change_dir, "review.md")
    if not os.path.exists(review_path):
        result = make_result(
            gate_id=gate_id,
            validator="review_readiness",
            status="fail",
            blocking=True,
            checked_files=["review.md"],
            errors=["review.md not found"],
            rule_refs=["harness/rules/artifacts/review-rules.md"],
            metadata={"change_dir": change_dir},
        )
        print(json.dumps(result))
        sys.exit(1)

    content = read_markdown(review_path)
    errors = []
    warnings = []

    # 检查 Review Target（支持中英文标题，通过 has_heading alias 系统）
    if not has_heading(content, "Review Target"):
        warnings.append("review.md 未包含 'Review Target' / '评审目标' 部分")

    # 检查 Decision（支持中英文标题）
    if not has_heading(content, "Decision"):
        warnings.append("review.md 未包含 'Decision' / '决策' 部分")

    # 检查是否有明确的拒绝发布决定
    # 只检查 "是否允许发布: no" 这种明确的拒绝，忽略模板占位符 "yes / no"
    has_blocker = False
    lines = content.split("\n")
    for line in lines:
        line_stripped = line.strip()
        # 匹配 "是否允许发布: no" 但排除 "yes / no" 占位符
        if "是否允许发布" in line_stripped:
            # 如果是 "yes / no" 或 "yes/no" 占位符，不算拒绝
            if "yes" in line_stripped.lower() and "/" in line_stripped:
                continue
            # 如果明确写 no
            if line_stripped.lower().endswith("no"):
                has_blocker = True
                break
        # 检查问题表格中的 FAIL 级别条目（实际填了 FAIL 的）
        if line_stripped.startswith("| FAIL") or line_stripped.startswith("|FAIL"):
            has_blocker = True
            break

    if has_blocker:
        errors.append("review.md 明确拒绝发布，应阻断 publish")

    status = "fail" if errors else ("warn" if warnings else "pass")
    exit_code = 1 if status == "fail" else 0

    result = make_result(
        gate_id=gate_id,
        validator="review_readiness",
        status=status,
        blocking=True,
        checked_files=["review.md"],
        errors=errors,
        warnings=warnings,
        rule_refs=["harness/rules/artifacts/review-rules.md"],
        metadata={"change_dir": change_dir},
    )
    print(json.dumps(result))
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
