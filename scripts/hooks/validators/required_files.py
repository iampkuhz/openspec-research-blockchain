#!/usr/bin/env python3
"""required_files — 检查 gate registry 声明的 required files 是否存在。

触发方式：按 gate 配置
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
    gate_id = sys.argv[2] if len(sys.argv) > 2 else "unknown"

    # 从 gate registry 获取该 gate 的 required files
    # 优先级：环境变量 > 默认路径
    registry_env = os.environ.get("GATE_REGISTRY", "")
    if registry_env:
        registry_path = Path(registry_env)
    else:
        # 默认路径：从脚本位置向上推导
        registry_path = Path(__file__).resolve().parent.parent.parent.parent / "harness" / "gates" / "registry.yaml"

    required = _get_required_files(registry_path, gate_id)

    if not required:
        # 无法确定 required files，skip
        result = make_result(
            gate_id=gate_id,
            validator="required_files",
            status="skip",
            blocking=False,
            errors=[],
            warnings=["无法从 gate registry 获取 required files 列表"],
            metadata={"change_dir": change_dir},
        )
        print(json.dumps(result))
        sys.exit(0)

    missing = [f for f in required if not os.path.exists(os.path.join(change_dir, f))]

    if missing:
        result = make_result(
            gate_id=gate_id,
            validator="required_files",
            status="fail",
            blocking=True,
            checked_files=required,
            errors=[f"Missing required files: {', '.join(missing)}"],
            metadata={"change_dir": change_dir},
        )
        print(json.dumps(result))
        sys.exit(1)

    result = make_result(
        gate_id=gate_id,
        validator="required_files",
        status="pass",
        blocking=True,
        checked_files=required,
        metadata={"change_dir": change_dir},
    )
    print(json.dumps(result))
    sys.exit(0)


def _get_required_files(registry_path: Path, gate_id: str) -> list[str]:
    """从 gate registry 获取指定 gate 的 required files。"""
    if not registry_path or not registry_path.exists():
        return []
    try:
        data = load_yaml(str(registry_path))
        gate = data.get("gates", {}).get(gate_id, {})
        return gate.get("files", {}).get("required", [])
    except Exception:
        return []


if __name__ == "__main__":
    main()
