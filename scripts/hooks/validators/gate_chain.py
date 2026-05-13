#!/usr/bin/env python3
"""gate_chain — 检查历史 gate 状态，防止 blocking fail 后仍进入 publish。

触发方式：pre_publish
输入：change 目录路径
输出：若存在任何 blocking fail 的历史 gate 结果则 fail，否则 pass。
"""

import json
import os
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR.parent))
from lib.gate_result import make_result


# 在 pre_publish 之前必须全部通过的前置 gate
# 格式: (validation 文件, 对应的 artifact 文件)
PRE_PUBLISH_GATES = [
    ("validation/post-request.json", "request.md"),
    ("validation/post-plan.json", "plan.md"),
    ("validation/post-research.json", "sources/source-pack.md"),
    ("validation/post-draft.json", "draft.md"),
    ("validation/post-review.json", "review.md"),
]


def main():
    change_dir = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    gate_id = sys.argv[2] if len(sys.argv) > 2 else "pre_publish"

    errors = []
    warnings = []
    checked = []

    for rel_path, artifact_path in PRE_PUBLISH_GATES:
        full_path = os.path.join(change_dir, rel_path)
        checked.append(rel_path)

        if not os.path.exists(full_path):
            # gate 结果缺失：如果对应 artifact 已存在但 gate 未运行，说明绕过 gate 直接写了 artifact
            if artifact_path and os.path.exists(os.path.join(change_dir, artifact_path)):
                errors.append(
                    f"{artifact_path} 已存在但 {rel_path} 未执行，疑似绕过 gate 直接写入"
                )
            else:
                # artifact 也不存在，说明尚未到达该阶段，仅警告
                warnings.append(f"{rel_path} 不存在，对应 gate 尚未执行")
            continue

        try:
            with open(full_path, "r") as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            errors.append(f"{rel_path} 解析失败: {e}")
            continue

        status = data.get("status", "unknown")
        blocking = data.get("blocking", False)
        prev_gate = data.get("gate_id", rel_path)

        if status in ("fail", "error") and blocking:
            detail = data.get("errors", [])
            error_msg = f"{prev_gate} 状态为 {status} 且 blocking=true"
            if detail:
                error_msg += f"，原因: {'; '.join(detail[:3])}"
            errors.append(error_msg)

    if errors:
        errors.insert(0, "存在 blocking fail 的前置 gate，不得进入 publish")

    status = "fail" if errors else ("warn" if warnings else "pass")
    exit_code = 1 if status == "fail" else 0

    result = make_result(
        gate_id=gate_id,
        validator="gate_chain",
        status=status,
        blocking=True,
        checked_files=checked,
        errors=errors,
        warnings=warnings,
        rule_refs=[
            "harness/rules/artifacts/publish-rules.md",
            "harness/gates/registry.yaml",
        ],
        metadata={"change_dir": change_dir},
    )
    print(json.dumps(result))
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
