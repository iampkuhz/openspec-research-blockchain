#!/usr/bin/env python3
"""knowledge_tree — 检查 knowledge/ 树的目录结构约束。

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
from lib.yaml_loader import load_yaml


def main():
    change_dir = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    gate_id = sys.argv[2] if len(sys.argv) > 2 else "post_publish"

    repo_root = _find_repo_root(change_dir)
    knowledge_dir = os.path.join(repo_root, "knowledge")

    if not os.path.isdir(knowledge_dir):
        result = make_result(
            gate_id=gate_id,
            validator="knowledge_tree",
            status="skip",
            blocking=False,
            errors=[],
            warnings=["knowledge/ 目录不存在"],
            metadata={"change_dir": change_dir},
        )
        print(json.dumps(result))
        sys.exit(0)

    # 检查 publish_targets 的 to 路径是否在 knowledge/ 下有对应文件
    change_yaml_path = os.path.join(change_dir, "change.yaml")
    publish_targets = []
    if os.path.exists(change_yaml_path):
        try:
            change_yaml = load_yaml(change_yaml_path)
            publish_targets = change_yaml.get("publish_targets", [])
        except Exception:
            pass

    errors = []
    for pt in publish_targets:
        if isinstance(pt, dict):
            to_path = pt.get("to", "")
        else:
            to_path = pt
        if to_path and not to_path.startswith("knowledge/"):
            errors.append(f"publish target '{to_path}' 不在 knowledge/ 下")

    status = "fail" if errors else "pass"
    exit_code = 1 if status == "fail" else 0

    result = make_result(
        gate_id=gate_id,
        validator="knowledge_tree",
        status=status,
        blocking=True,
        checked_files=["knowledge/"],
        errors=errors,
        metadata={"change_dir": change_dir, "knowledge_dir": knowledge_dir},
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
