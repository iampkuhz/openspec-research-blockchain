#!/usr/bin/env python3
"""draft_contract — 检查 staging draft 的结构。

触发方式：post_draft
输入：change 目录路径
输出：校验通过返回 0，失败返回非 0 并写入 validation/draft_contract.json
"""

import json
import os
import sys


def main():
    change_dir = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    draft_path = os.path.join(change_dir, "draft.md")

    if not os.path.exists(draft_path):
        _write_fail_result(change_dir, "draft.md not found")
        sys.exit(1)

    with open(draft_path, "r") as fh:
        content = fh.read()

    if len(content.strip()) < 10:
        _write_fail_result(change_dir, "draft.md content is empty or too short")
        sys.exit(1)

    # 检查 work-products/ 不应存在
    work_products_dir = os.path.join(change_dir, "work-products")
    if os.path.exists(work_products_dir):
        _write_warn_result(change_dir, "work-products/ directory exists (should use draft.md instead)")

    # 检查核心章节
    required_sections = ["Metadata", "Summary", "Body", "Evidence", "Traceability"]
    missing = [s for s in required_sections if f"## {s}" not in content and f"### {s}" not in content]
    if missing:
        _write_fail_result(change_dir, f"Missing required sections in draft.md: {', '.join(missing)}")
        sys.exit(1)

    print("PASS: draft.md has required structure")
    sys.exit(0)


def _write_fail_result(change_dir, error_msg):
    validation_dir = os.path.join(change_dir, "validation")
    os.makedirs(validation_dir, exist_ok=True)
    result = {
        "gate_id": "post_draft",
        "validator": "draft_contract",
        "status": "fail",
        "blocking": True,
        "checked_files": ["draft.md"],
        "errors": [error_msg],
        "warnings": [],
        "rule_refs": ["harness/rules/artifacts/draft-rules.md"],
        "metadata": {"change_dir": change_dir},
    }
    with open(os.path.join(validation_dir, "draft_contract.json"), "w") as fh:
        json.dump(result, fh, indent=2)
    print(f"FAIL: {error_msg}")


def _write_warn_result(change_dir, warn_msg):
    validation_dir = os.path.join(change_dir, "validation")
    os.makedirs(validation_dir, exist_ok=True)
    result = {
        "gate_id": "post_draft",
        "validator": "draft_contract",
        "status": "warn",
        "blocking": True,
        "checked_files": ["draft.md"],
        "errors": [],
        "warnings": [warn_msg],
        "rule_refs": ["harness/rules/artifacts/draft-rules.md"],
        "metadata": {"change_dir": change_dir},
    }
    with open(os.path.join(validation_dir, "draft_contract.json"), "w") as fh:
        json.dump(result, fh, indent=2)
    print(f"WARN: {warn_msg}")


if __name__ == "__main__":
    main()
