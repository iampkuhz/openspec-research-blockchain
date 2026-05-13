#!/usr/bin/env python3
"""
Protected Paths Guard — 非治理上下文禁止修改核心规约文件

当 Write/Edit 命中以下路径时拦截：
  .claude/**
  harness/**
  openspec/specs/**
  openspec/schemas/**
  AGENTS.md, CLAUDE.md, docs/governance/**

如果当前 change context 不是 governance review 类型，则拒绝写入。

用法:
    python scripts/hooks/validators/protected_paths.py --files <path1> --files <path2>
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


# 受保护路径前缀（相对于 repo root）
PROTECTED_PREFIXES = [
    ".claude/",
    "harness/",
    "openspec/specs/",
    "openspec/schemas/",
]

# 受保护的根级文件
PROTECTED_ROOT_FILES = {
    "AGENTS.md",
    "CLAUDE.md",
    "QODER.md",
}

# 受保护的目录
PROTECTED_DIRS = [
    "docs/governance/",
]


def is_protected(file_path: str) -> bool:
    """判断文件路径是否属于受保护范围"""
    # 统一用 / 分隔
    normalized = file_path.replace("\\", "/")
    # 去掉前导 ./
    if normalized.startswith("./"):
        normalized = normalized[2:]

    # 检查前缀匹配（相对路径场景）
    for prefix in PROTECTED_PREFIXES + PROTECTED_DIRS:
        if normalized.startswith(prefix):
            return True

    # 检查路径组件（绝对路径或嵌套场景）
    for protected in [".claude", "harness", "openspec/specs", "openspec/schemas", "docs/governance"]:
        parts = normalized.split("/")
        for i, part in enumerate(parts):
            if part == protected.split("/")[0]:
                # 检查后续部分是否匹配完整前缀
                remainder = "/".join(parts[i:])
                if remainder.startswith(protected):
                    return True

    # 检查根级文件（basename 匹配）
    base_name = normalized.split("/")[-1]
    if base_name in PROTECTED_ROOT_FILES:
        # 只匹配项目根目录下的文件（深度 0 或 1）
        depth = normalized.count("/")
        if depth <= 1:
            return True

    return False


def is_governance_context(change_dir: Path) -> bool:
    """判断当前 change 是否为 governance review 类型"""
    change_yaml = change_dir / "change.yaml"
    if not change_yaml.exists():
        return False

    content = change_yaml.read_text(encoding="utf-8")
    # 检查 task_type 或 change_operation 是否包含 governance
    governance_keywords = ["governance", "governance_review", "governance-review"]
    for keyword in governance_keywords:
        if keyword in content.lower():
            return True
    return False


def find_change_dir(file_path: str) -> Path | None:
    """从文件路径向上查找 change directory"""
    p = Path(file_path).resolve()
    # 尝试查找 openspec/changes/<id>
    for parent in p.parents:
        if parent.name == "changes" and (parent.parent / "changes").exists():
            # 返回 changes 下的子目录
            return parent
        if (parent / "change.yaml").exists():
            return parent
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Protected paths guard")
    parser.add_argument("--files", action="append", default=[], help="Files being written")
    parser.add_argument("--change", help="Change directory path")
    args = parser.parse_args()

    errors: list[str] = []
    warnings: list[str] = []

    # 确定 change directory
    change_dir = None
    if args.change:
        change_dir = Path(args.change)
    else:
        for fp in args.files:
            cd = find_change_dir(fp)
            if cd:
                change_dir = cd
                break

    protected_hits = []
    for fp in args.files:
        if is_protected(fp):
            protected_hits.append(fp)

    if not protected_hits:
        # 没有命中受保护路径，直接通过
        result = {
            "validator": "protected_paths",
            "status": "pass",
            "errors": [],
            "warnings": [],
        }
        print(json.dumps(result, indent=2))
        return 0

    # 命中了受保护路径，检查是否为 governance context
    if change_dir and is_governance_context(change_dir):
        result = {
            "validator": "protected_paths",
            "status": "pass",
            "errors": [],
            "warnings": [
                f"governance change detected, allowing protected path writes: {', '.join(protected_hits)}"
            ],
        }
        print(json.dumps(result, indent=2))
        return 0

    # 非治理上下文，拒绝写入受保护路径
    for fp in protected_hits:
        errors.append(
            f"blocked: '{fp}' is a protected governance file. "
            f"Use /spec-governance-review to modify governance files. "
            f"Direct modification during normal research is prohibited."
        )

    result = {
        "validator": "protected_paths",
        "status": "fail",
        "errors": errors,
        "warnings": warnings,
    }
    print(json.dumps(result, indent=2))
    return 1


if __name__ == "__main__":
    sys.exit(main())
