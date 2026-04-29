#!/usr/bin/env python3
"""draft_contract — 检查 staging draft 的结构。

触发方式：post_draft
输入：change 目录路径
输出：校验通过返回 0，失败返回非 0 并写入 validation/draft_contract.json
"""

import json
import os
import re
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

    # 检查核心章节（同时接受英文和中文模板名称）
    # 注意：draft 正文可以是编号章节（如 "## 1. 共识与亚秒出块层"），不一定需要 "## 正文"
    required_sections_en = ["Metadata", "Summary", "Evidence", "Traceability"]
    required_sections_cn = ["元数据", "摘要", "证据", "追踪链"]
    missing = []
    for en, cn in zip(required_sections_en, required_sections_cn):
        if f"## {en}" not in content and f"## {cn}" not in content and f"### {en}" not in content and f"### {cn}" not in content:
            missing.append(f"{en}/{cn}")
    # Body section: check for numbered sections as body content
    has_body = bool(re.search(r"^##\s+\d+[\.\s]", content, re.M)) or "## Body" in content or "## 正文" in content
    if not has_body:
        missing.append("Body/正文 (或编号章节)")
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
        "blocking": False,
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
