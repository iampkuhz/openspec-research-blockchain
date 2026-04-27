#!/usr/bin/env python3
"""decision_verdict — 检查 decision 类型的 verdict 文件。

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
from lib.markdown_utils import read_markdown
from lib.yaml_loader import load_yaml


def main():
    change_dir = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    gate_id = sys.argv[2] if len(sys.argv) > 2 else "pre_publish"

    # 检查 task_type
    change_yaml_path = os.path.join(change_dir, "change.yaml")
    task_type = None
    if os.path.exists(change_yaml_path):
        try:
            change_yaml = load_yaml(change_yaml_path)
            task_type = change_yaml.get("task_type")
        except Exception:
            pass

    # 非 decision 类型可 skip
    if task_type != "decision":
        result = make_result(
            gate_id=gate_id,
            validator="decision_verdict",
            status="skip",
            blocking=False,
            errors=[],
            warnings=[f"task_type={task_type}，非 decision 类型跳过"],
            rule_refs=["harness/rules/research/decision-criteria-rules.md"],
            metadata={"change_dir": change_dir, "task_type": task_type},
        )
        print(json.dumps(result))
        sys.exit(0)

    # decision 类型强检查
    errors = []
    warnings = []

    # 检查 decision-criteria.md 或 draft.md Decision Analysis
    criteria_path = os.path.join(change_dir, "decision-criteria.md")
    draft_path = os.path.join(change_dir, "draft.md")
    has_criteria = os.path.exists(criteria_path)
    has_draft_decision = False
    if os.path.exists(draft_path):
        content = read_markdown(draft_path)
        has_draft_decision = "Decision Analysis" in content

    if not has_criteria and not has_draft_decision:
        errors.append("decision 类型需要 decision-criteria.md 或 draft.md 包含 Decision Analysis")

    # 检查 draft.md Verdict Draft
    if os.path.exists(draft_path):
        content = read_markdown(draft_path)
        if "Verdict Draft" not in content and "verdict" not in content.lower():
            errors.append("draft.md 需要包含 Verdict Draft")

    # 检查 publish.md 中的 verdict mapping
    publish_path = os.path.join(change_dir, "publish.md")
    if os.path.exists(publish_path):
        content = read_markdown(publish_path)
        if "verdict" not in content.lower() and "verdict.md" not in content:
            warnings.append("publish.md 未包含 verdict mapping")

    status = "fail" if errors else ("warn" if warnings else "pass")
    exit_code = 1 if status == "fail" else 0

    result = make_result(
        gate_id=gate_id,
        validator="decision_verdict",
        status=status,
        blocking=True,
        checked_files=["decision-criteria.md", "draft.md", "publish.md"],
        errors=errors,
        warnings=warnings,
        rule_refs=["harness/rules/research/decision-criteria-rules.md"],
        metadata={"change_dir": change_dir, "task_type": task_type},
    )
    print(json.dumps(result))
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
