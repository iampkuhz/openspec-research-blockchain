#!/usr/bin/env python3
"""schema_package — 校验 schema package 完整性。

验证：
1. artifact ids 唯一
2. 声明的 template 文件存在
3. profile required/optional artifact ids 在 schema 中定义
4. operation 文件存在
5. final/support template 路径存在

触发方式：post_request / manual
输入：change 目录路径
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
from lib.yaml_loader import load_yaml

ROOT = Path(__file__).resolve().parent.parent.parent.parent
SCHEMA_DIR = ROOT / "openspec" / "schemas" / "blockchain-research"
SCHEMA_PATH = SCHEMA_DIR / "schema.yaml"
TEMPLATES_DIR = SCHEMA_DIR / "templates"
PROFILES_DIR = SCHEMA_DIR / "profiles"
OPERATIONS_DIR = SCHEMA_DIR / "operations"


def validate_schema_package() -> tuple[list[str], int]:
    """校验 schema package 完整性。返回 (errors, artifact_count)。"""
    errors = []

    if not SCHEMA_PATH.exists():
        return [f"schema.yaml not found at {SCHEMA_PATH}"], 0

    schema = load_yaml(str(SCHEMA_PATH))
    artifacts = schema.get("artifacts", [])
    artifact_count = len(artifacts)

    # 1. artifact ids 唯一
    artifact_ids = set()
    artifact_templates = set()
    for art in artifacts:
        aid = art.get("id")
        if not aid:
            errors.append("artifact missing 'id'")
            continue
        if aid in artifact_ids:
            errors.append(f"duplicate artifact id: '{aid}'")
        artifact_ids.add(aid)
        tpl = art.get("template")
        if tpl:
            artifact_templates.add(tpl)

    # 2. 声明的 template 文件存在
    for tpl in artifact_templates:
        tpl_path = TEMPLATES_DIR / tpl
        if not tpl_path.exists():
            errors.append(f"template '{tpl}' not found at {tpl_path.relative_to(ROOT)}")

    # 3. profile required/optional artifact ids 在 schema 中定义
    if PROFILES_DIR.exists():
        for profile_file in sorted(PROFILES_DIR.glob("*.yaml")):
            profile = load_yaml(str(profile_file))
            profile_name = profile_file.stem
            for kind in ("required", "optional"):
                for aid in profile.get(kind, []):
                    if aid not in artifact_ids:
                        errors.append(f"profile '{profile_name}': {kind} artifact '{aid}' not defined in schema")

    # 4. operation 文件存在
    if OPERATIONS_DIR.exists():
        for op_file in sorted(OPERATIONS_DIR.glob("*.yaml")):
            op = load_yaml(str(op_file))
            op_name = op_file.stem
            # 检查 operation 引用的 templates 是否存在
            for tpl in op.get("templates", []):
                tpl_path = TEMPLATES_DIR / tpl
                if not tpl_path.exists():
                    errors.append(f"operation '{op_name}': template '{tpl}' not found")

    # 5. final/support templates 一致性
    final_templates = schema.get("x_final_templates", {})
    if isinstance(final_templates, dict):
        for key, config in final_templates.items():
            tpl_path_str = config.get("path", "").replace("./templates/", "")
            if tpl_path_str:
                tpl_path = TEMPLATES_DIR / tpl_path_str
                if not tpl_path.exists():
                    errors.append(f"final template '{key}' ({tpl_path_str}) not found")

    support_templates = schema.get("x_support_templates", {})
    if isinstance(support_templates, dict):
        for key, config in support_templates.items():
            tpl_path_str = config.get("path", "").replace("./templates/", "")
            if tpl_path_str:
                tpl_path = TEMPLATES_DIR / tpl_path_str
                if not tpl_path.exists():
                    errors.append(f"support template '{key}' ({tpl_path_str}) not found")

    return errors, artifact_count


def main():
    change_dir = sys.argv[1] if len(sys.argv) > 1 else str(ROOT)
    gate_id = sys.argv[2] if len(sys.argv) > 2 else "schema_package"

    errors, artifact_count = validate_schema_package()

    if errors:
        result = make_result(
            gate_id=gate_id,
            validator="schema_package",
            status="fail",
            blocking=True,
            checked_files=[str(SCHEMA_PATH.relative_to(ROOT))],
            errors=errors,
            rule_refs=["openspec/schemas/blockchain-research/schema.yaml"],
            metadata={"total_errors": len(errors)},
        )
        print(json.dumps(result, indent=2, ensure_ascii=False))
        sys.exit(1)

    result = make_result(
        gate_id=gate_id,
        validator="schema_package",
        status="pass",
        blocking=True,
        checked_files=[str(SCHEMA_PATH.relative_to(ROOT))],
        rule_refs=["openspec/schemas/blockchain-research/schema.yaml"],
        metadata={"artifacts_checked": artifact_count},
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0)


if __name__ == "__main__":
    main()
