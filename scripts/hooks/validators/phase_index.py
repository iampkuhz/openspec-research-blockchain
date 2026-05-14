#!/usr/bin/env python3
"""phase_index — 校验 harness/rules/_phase_index.yaml 引用完整性。

验证：
1. specs 引用指向存在的 openspec/specs/<id>/spec.md
2. rules 引用指向存在的 harness/rules/<ref>.md
3. workflows 引用指向存在的 harness/workflows/<ref>.md 或在 workflows/_index.yaml 中声明
4. 支持 conditional: 前缀

触发方式：post_request / manual
输入：change 目录路径（可选，默认使用 ROOT）
输出：JSON gate result
"""

import json
import os
import sys
from pathlib import Path

import yaml

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR.parent))
from lib.gate_result import make_result

ROOT = Path(__file__).resolve().parent.parent.parent.parent
INDEX_PATH = ROOT / "harness" / "rules" / "_phase_index.yaml"
WF_INDEX_PATH = ROOT / "harness" / "workflows" / "_index.yaml"


def validate_phase_index() -> list[str]:
    """验证 phase index 中的所有引用。"""
    errors = []

    if not INDEX_PATH.exists():
        return [f"_phase_index.yaml not found at {INDEX_PATH}"]

    data = yaml.safe_load(INDEX_PATH.read_text())
    if not isinstance(data, dict) or "phases" not in data:
        return ["_phase_index.yaml missing 'phases' key"]

    phases = data["phases"]

    # 加载 workflow index 用于快速查找
    wf_ids = set()
    if WF_INDEX_PATH.exists():
        wf_data = yaml.safe_load(WF_INDEX_PATH.read_text())
        if isinstance(wf_data, dict) and "workflows" in wf_data:
            wf_ids = set(wf_data["workflows"].keys())

    for phase, config in phases.items():
        depends = config.get("depends", {})

        # 验证 specs
        for spec_id in depends.get("specs", []):
            spec_path = ROOT / "openspec" / "specs" / spec_id / "spec.md"
            if not spec_path.exists():
                errors.append(f"phase '{phase}': spec '{spec_id}' → {spec_path.relative_to(ROOT)} not found")

        # 验证 rules
        for rule_ref in depends.get("rules", []):
            ref = rule_ref.removeprefix("conditional:")
            rule_path = ROOT / "harness" / "rules" / f"{ref}.md"
            if not rule_path.exists():
                errors.append(f"phase '{phase}': rule '{rule_ref}' → {rule_path.relative_to(ROOT)} not found")

        # 验证 workflows
        for wf_ref in depends.get("workflows", []):
            wf_path = ROOT / "harness" / "workflows" / f"{wf_ref}.md"
            if wf_path.exists():
                continue
            # 检查是否在 workflow index 中
            if wf_ref in wf_ids:
                continue
            errors.append(f"phase '{phase}': workflow '{wf_ref}' not found in harness/workflows/ or _index.yaml")

    return errors


def main():
    change_dir = sys.argv[1] if len(sys.argv) > 1 else str(ROOT)
    gate_id = sys.argv[2] if len(sys.argv) > 2 else "phase_index"

    errors = validate_phase_index()

    if errors:
        result = make_result(
            gate_id=gate_id,
            validator="phase_index",
            status="fail",
            blocking=True,
            checked_files=[str(INDEX_PATH.relative_to(ROOT))],
            errors=errors,
            rule_refs=["harness/rules/_phase_index.yaml"],
            metadata={"total_errors": len(errors)},
        )
        print(json.dumps(result, indent=2, ensure_ascii=False))
        sys.exit(1)

    result = make_result(
        gate_id=gate_id,
        validator="phase_index",
        status="pass",
        blocking=True,
        checked_files=[str(INDEX_PATH.relative_to(ROOT))],
        rule_refs=["harness/rules/_phase_index.yaml"],
        metadata={"phases_checked": len(yaml.safe_load(INDEX_PATH.read_text()).get("phases", {}))},
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0)


if __name__ == "__main__":
    main()
