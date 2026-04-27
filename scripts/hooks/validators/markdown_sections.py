#!/usr/bin/env python3
"""markdown_sections — 检查 Markdown artifact 的必要章节。

触发方式：按 gate 配置
输入：change 目录路径
输出：校验通过返回 0，失败返回非 0 并输出 JSON result
"""

import json
import os
import sys
import re
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR.parent))
from lib.gate_result import make_result
from lib.markdown_utils import read_markdown, check_required_sections

# 不同 artifact 类型的最小章节要求
SECTION_REQUIREMENTS = {
    "request": ["Summary", "Scope"],
    "plan": ["Summary", "Plan"],
    "draft": ["Metadata", "Summary", "Body", "Evidence", "Traceability"],
    "review": ["Review Target", "Decision"],
    "publish": ["Publish Targets"],
}

ARTIFACT_FILE_MAP = {
    "request": "request.md",
    "plan": "plan.md",
    "draft": "draft.md",
    "review": "review.md",
    "publish": "publish.md",
}


def main():
    change_dir = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    # 优先从 --gate 标志获取，其次从位置参数 $2 获取
    gate_id = "unknown"
    for i, arg in enumerate(sys.argv):
        if arg == "--gate" and i + 1 < len(sys.argv):
            gate_id = sys.argv[i + 1]
            break
    else:
        if len(sys.argv) > 2:
            gate_id = sys.argv[2]

    # 根据 gate 推断 artifact 类型
    artifact_type = gate_id.replace("post_", "").replace("pre_", "")
    required_sections = SECTION_REQUIREMENTS.get(artifact_type, [])
    artifact_file = ARTIFACT_FILE_MAP.get(artifact_type)

    if not artifact_file or not required_sections:
        result = make_result(
            gate_id=gate_id,
            validator="markdown_sections",
            status="skip",
            blocking=False,
            errors=[],
            warnings=[f"no section requirements for {gate_id}"],
            metadata={"change_dir": change_dir},
        )
        print(json.dumps(result))
        sys.exit(0)

    artifact_path = os.path.join(change_dir, artifact_file)
    if not os.path.exists(artifact_path):
        result = make_result(
            gate_id=gate_id,
            validator="markdown_sections",
            status="skip",
            blocking=False,
            checked_files=[artifact_file],
            errors=[],
            warnings=[f"{artifact_file} not found (may not be applicable yet)"],
            metadata={"change_dir": change_dir},
        )
        print(json.dumps(result))
        sys.exit(0)

    content = read_markdown(artifact_path)
    missing = check_required_sections(content, required_sections)

    if missing:
        result = make_result(
            gate_id=gate_id,
            validator="markdown_sections",
            status="fail",
            blocking=True,
            checked_files=[artifact_file],
            errors=[f"Missing sections in {artifact_file}: {', '.join(missing)}"],
            metadata={"change_dir": change_dir},
        )
        print(json.dumps(result))
        sys.exit(1)

    result = make_result(
        gate_id=gate_id,
        validator="markdown_sections",
        status="pass",
        blocking=True,
        checked_files=[artifact_file],
        metadata={"change_dir": change_dir},
    )
    print(json.dumps(result))
    sys.exit(0)


if __name__ == "__main__":
    main()
