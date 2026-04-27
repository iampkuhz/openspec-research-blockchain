#!/usr/bin/env python3
"""knowledge_artifact — 检查 publish target 的知识产出结构。

触发方式：post_publish
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
from lib.path_policy import is_knowledge_path
from lib.yaml_loader import load_yaml


def main():
    change_dir = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    gate_id = sys.argv[2] if len(sys.argv) > 2 else "post_publish"

    # 从 change.yaml 获取 publish_targets
    change_yaml_path = os.path.join(change_dir, "change.yaml")
    publish_targets = []
    if os.path.exists(change_yaml_path):
        try:
            change_yaml = load_yaml(change_yaml_path)
            publish_targets = change_yaml.get("publish_targets", [])
        except Exception:
            pass

    if not publish_targets:
        result = make_result(
            gate_id=gate_id,
            validator="knowledge_artifact",
            status="skip",
            blocking=False,
            errors=[],
            warnings=["未找到 publish_targets"],
            rule_refs=["harness/rules/research/traceability-rules.md"],
            metadata={"change_dir": change_dir},
        )
        print(json.dumps(result))
        sys.exit(0)

    errors = []
    warnings = []
    checked_files = []
    repo_root = _find_repo_root(change_dir)

    required_sections = ["Metadata", "Summary", "Body", "Evidence", "Traceability"]

    for pt in publish_targets:
        if isinstance(pt, dict):
            to_path = pt.get("to", "")
        else:
            to_path = pt

        if not to_path:
            continue

        if not is_knowledge_path(to_path):
            errors.append(f"publish target '{to_path}' 不在 knowledge/ 下")
            continue

        full_path = os.path.join(repo_root, to_path)
        checked_files.append(to_path)

        if not os.path.exists(full_path):
            errors.append(f"publish target file not found: {to_path}")
            continue

        content = read_markdown(full_path)
        if to_path.endswith("artifact.md"):
            for section in required_sections:
                if section not in content and section.lower() not in content.lower():
                    warnings.append(f"{to_path} 缺失 {section} 部分")

    status = "fail" if errors else ("warn" if warnings else "pass")
    exit_code = 1 if status == "fail" else 0

    result = make_result(
        gate_id=gate_id,
        validator="knowledge_artifact",
        status=status,
        blocking=True,
        checked_files=checked_files,
        errors=errors,
        warnings=warnings,
        rule_refs=["harness/rules/research/traceability-rules.md"],
        metadata={"change_dir": change_dir},
    )
    print(json.dumps(result))
    sys.exit(exit_code)


def _find_repo_root(start: str) -> str:
    d = Path(start).resolve()
    while d != d.parent:
        if (d / ".git").exists() or (d / "openspec").exists():
            return str(d)
        d = d.parent
    return start


if __name__ == "__main__":
    main()
