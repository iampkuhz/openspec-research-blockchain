#!/usr/bin/env python3
"""publish_targets — 检查 publish.md 和 publish targets 合法性。

触发方式：pre_publish
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
from lib.path_policy import is_valid_publish_target
from lib.yaml_loader import load_yaml


def main():
    change_dir = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    gate_id = sys.argv[2] if len(sys.argv) > 2 else "pre_publish"

    errors = []
    warnings = []

    publish_path = os.path.join(change_dir, "publish.md")
    if not os.path.exists(publish_path):
        errors.append("publish.md not found")
        result = make_result(
            gate_id=gate_id,
            validator="publish_targets",
            status="fail",
            blocking=True,
            checked_files=["publish.md"],
            errors=errors,
            rule_refs=["harness/rules/artifacts/publish-rules.md"],
            metadata={"change_dir": change_dir},
        )
        print(json.dumps(result))
        sys.exit(1)

    with open(publish_path, "r") as fh:
        content = fh.read()

    # 检查 Publish Targets
    if "Publish Targets" not in content and "publish_targets" not in content:
        warnings.append("publish.md 未包含 'Publish Targets' 标题")

    # 检查不得从 request.md / plan.md 发布
    for line in content.split("\n"):
        if "from:" in line.lower() and ("request.md" in line or "plan.md" in line):
            errors.append(f"不得从 {('request.md' if 'request.md' in line else 'plan.md')} 发布")

    # 检查 to 路径是否指向 knowledge/
    draft_path = os.path.join(change_dir, "draft.md")
    if not os.path.exists(draft_path):
        errors.append("draft.md not found (required as publish source)")

    # 检查 change.yaml 中的 publish_targets
    change_yaml_path = os.path.join(change_dir, "change.yaml")
    if os.path.exists(change_yaml_path):
        try:
            change_yaml = load_yaml(change_yaml_path)
            publish_targets = change_yaml.get("publish_targets", [])
            for pt in publish_targets:
                if isinstance(pt, dict):
                    to_path = pt.get("to", "")
                    if to_path and not is_valid_publish_target(to_path):
                        errors.append(f"publish target '{to_path}' 必须指向 knowledge/**")
        except Exception:
            pass

    status = "fail" if errors else ("warn" if warnings else "pass")
    exit_code = 1 if status == "fail" else 0

    result = make_result(
        gate_id=gate_id,
        validator="publish_targets",
        status=status,
        blocking=True,
        checked_files=["publish.md", "draft.md"],
        errors=errors,
        warnings=warnings,
        rule_refs=["harness/rules/artifacts/publish-rules.md"],
        metadata={"change_dir": change_dir},
    )
    print(json.dumps(result))
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
