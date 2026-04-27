#!/usr/bin/env python3
"""child_change_graph — 检查 plan.md 是否包含 child changes 判断。

触发方式：post_plan
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
    gate_id = sys.argv[2] if len(sys.argv) > 2 else "post_plan"

    plan_path = os.path.join(change_dir, "plan.md")
    if not os.path.exists(plan_path):
        result = make_result(
            gate_id=gate_id,
            validator="child_change_graph",
            status="skip",
            blocking=False,
            checked_files=["plan.md"],
            errors=[],
            warnings=["plan.md not found"],
            rule_refs=["harness/rules/artifacts/plan-rules.md"],
            metadata={"change_dir": change_dir},
        )
        print(json.dumps(result))
        sys.exit(0)

    content = read_markdown(plan_path)

    # 检查是否有 child changes 或是否需要拆分的说明
    has_child_section = (
        "Child Changes" in content
        or "child changes" in content
        or "拆分" in content
        or "不需要拆分" in content
        or "无需拆分" in content
        or "child_change" in content
    )

    if not has_child_section:
        result = make_result(
            gate_id=gate_id,
            validator="child_change_graph",
            status="warn",
            blocking=False,
            checked_files=["plan.md"],
            errors=[],
            warnings=["plan.md 未包含 child changes 判断或拆分说明"],
            rule_refs=["harness/rules/artifacts/plan-rules.md"],
            metadata={"change_dir": change_dir},
        )
        print(json.dumps(result))
        sys.exit(0)

    result = make_result(
        gate_id=gate_id,
        validator="child_change_graph",
        status="pass",
        blocking=False,
        checked_files=["plan.md"],
        rule_refs=["harness/rules/artifacts/plan-rules.md"],
        metadata={"change_dir": change_dir},
    )
    print(json.dumps(result))
    sys.exit(0)


if __name__ == "__main__":
    main()
