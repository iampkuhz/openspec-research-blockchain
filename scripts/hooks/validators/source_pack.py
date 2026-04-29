#!/usr/bin/env python3
"""source_pack — 检查 sources/source-pack.md 的来源元信息和清单。

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
    source_pack_path = os.path.join(change_dir, "sources", "source-pack.md")

    if not os.path.exists(source_pack_path):
        result = make_result(
            gate_id=gate_id,
            validator="source_pack",
            status="fail",
            blocking=False,
            checked_files=["sources/source-pack.md"],
            errors=["sources/source-pack.md not found"],
            rule_refs=["harness/rules/artifacts/source-pack-rules.md"],
            metadata={"change_dir": change_dir},
        )
        print(json.dumps(result))
        sys.exit(1)

    with open(source_pack_path, "r") as fh:
        content = fh.read()

    if len(content.strip()) < 10:
        result = make_result(
            gate_id=gate_id,
            validator="source_pack",
            status="fail",
            blocking=False,
            checked_files=["sources/source-pack.md"],
            errors=["sources/source-pack.md content is empty or too short"],
            rule_refs=["harness/rules/artifacts/source-pack-rules.md"],
            metadata={"change_dir": change_dir},
        )
        print(json.dumps(result))
        sys.exit(1)

    # 检查 Source List 标题（支持中英文）
    if "Source List" not in content and "## Source" not in content and "来源清单" not in content and "## 来源" not in content:
        result = make_result(
            gate_id=gate_id,
            validator="source_pack",
            status="warn",
            blocking=False,
            checked_files=["sources/source-pack.md"],
            errors=[],
            warnings=["source-pack.md 未包含 'Source List' 标题"],
            rule_refs=["harness/rules/artifacts/source-pack-rules.md"],
            metadata={"change_dir": change_dir},
        )
        print(json.dumps(result))
        sys.exit(0)

    result = make_result(
        gate_id=gate_id,
        validator="source_pack",
        status="pass",
        blocking=False,
        checked_files=["sources/source-pack.md"],
        errors=[],
        warnings=[],
        rule_refs=["harness/rules/artifacts/source-pack-rules.md"],
        metadata={"change_dir": change_dir},
    )
    print(json.dumps(result))
    sys.exit(0)


if __name__ == "__main__":
    main()
