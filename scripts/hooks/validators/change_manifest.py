#!/usr/bin/env python3
"""change_manifest — 检查 change.yaml 的最小字段。

触发方式：post_request
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
from lib.yaml_loader import load_yaml


def main():
    change_dir = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    gate_id = sys.argv[2] if len(sys.argv) > 2 else "post_request"

    change_yaml_path = os.path.join(change_dir, "change.yaml")
    if not os.path.exists(change_yaml_path):
        result = make_result(
            gate_id=gate_id,
            validator="change_manifest",
            status="fail",
            blocking=True,
            checked_files=["change.yaml"],
            errors=["change.yaml not found"],
            rule_refs=["harness/rules/artifacts/request-rules.md"],
            metadata={"change_dir": change_dir},
        )
        print(json.dumps(result))
        sys.exit(1)

    try:
        change_yaml = load_yaml(change_yaml_path)
    except Exception as e:
        result = make_result(
            gate_id=gate_id,
            validator="change_manifest",
            status="fail",
            blocking=True,
            checked_files=["change.yaml"],
            errors=[f"change.yaml 解析失败: {e}"],
            rule_refs=["harness/rules/artifacts/request-rules.md"],
            metadata={"change_dir": change_dir},
        )
        print(json.dumps(result))
        sys.exit(1)

    required_keys = ["id", "schema", "task_type", "change_operation", "execution_scope", "artifacts", "validators", "publish_targets"]
    missing = [k for k in required_keys if k not in change_yaml]

    if missing:
        result = make_result(
            gate_id=gate_id,
            validator="change_manifest",
            status="fail",
            blocking=True,
            checked_files=["change.yaml"],
            errors=[f"change.yaml 缺失字段: {', '.join(missing)}"],
            rule_refs=["harness/rules/artifacts/request-rules.md"],
            metadata={"change_dir": change_dir},
        )
        print(json.dumps(result))
        sys.exit(1)

    result = make_result(
        gate_id=gate_id,
        validator="change_manifest",
        status="pass",
        blocking=True,
        checked_files=["change.yaml"],
        rule_refs=["harness/rules/artifacts/request-rules.md"],
        metadata={"change_dir": change_dir},
    )
    print(json.dumps(result))
    sys.exit(0)


if __name__ == "__main__":
    main()
