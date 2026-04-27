#!/usr/bin/env python3
"""evidence_map — 检查 sources/evidence-map.md 的证据映射。

触发方式：post_research
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


def main():
    change_dir = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    gate_id = sys.argv[2] if len(sys.argv) > 2 else "post_research"
    evidence_map_path = os.path.join(change_dir, "sources", "evidence-map.md")

    if not os.path.exists(evidence_map_path):
        result = make_result(
            gate_id=gate_id,
            validator="evidence_map",
            status="fail",
            blocking=False,
            checked_files=["sources/evidence-map.md"],
            errors=["sources/evidence-map.md not found"],
            rule_refs=["harness/rules/artifacts/evidence-map-rules.md"],
            metadata={"change_dir": change_dir},
        )
        print(json.dumps(result))
        sys.exit(1)

    with open(evidence_map_path, "r") as fh:
        content = fh.read()

    if len(content.strip()) < 10:
        result = make_result(
            gate_id=gate_id,
            validator="evidence_map",
            status="fail",
            blocking=False,
            checked_files=["sources/evidence-map.md"],
            errors=["sources/evidence-map.md content is empty or too short"],
            rule_refs=["harness/rules/artifacts/evidence-map-rules.md"],
            metadata={"change_dir": change_dir},
        )
        print(json.dumps(result))
        sys.exit(1)

    # 检查 Mapping 标题
    has_mapping = "Mapping" in content or "mapping" in content or "## " in content
    if not has_mapping:
        result = make_result(
            gate_id=gate_id,
            validator="evidence_map",
            status="warn",
            blocking=False,
            checked_files=["sources/evidence-map.md"],
            errors=[],
            warnings=["evidence-map.md 未包含 'Mapping' 标题"],
            rule_refs=["harness/rules/artifacts/evidence-map-rules.md"],
            metadata={"change_dir": change_dir},
        )
        print(json.dumps(result))
        sys.exit(0)

    result = make_result(
        gate_id=gate_id,
        validator="evidence_map",
        status="pass",
        blocking=False,
        checked_files=["sources/evidence-map.md"],
        errors=[],
        warnings=[],
        rule_refs=["harness/rules/artifacts/evidence-map-rules.md"],
        metadata={"change_dir": change_dir},
    )
    print(json.dumps(result))
    sys.exit(0)


if __name__ == "__main__":
    main()
