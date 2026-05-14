#!/usr/bin/env python3
"""path_policy — 路径策略工具。

职责：
1. 判断路径是否在 openspec/changes/<id>/
2. 判断 publish target 是否在 knowledge/**
3. 禁止 publish target 指向 openspec/** 或 harness/**
4. 标准化相对路径
"""

from pathlib import Path


def normalize_path(path: str, repo_root: str) -> str:
    """标准化路径为相对于 repo_root 的相对路径。"""
    p = Path(path)
    if not p.is_absolute():
        p = Path(repo_root) / p
    return str(p.relative_to(repo_root))


def is_in_changes(path: str) -> bool:
    """判断路径是否在 openspec/changes/ 下。"""
    return "openspec/changes/" in path


def is_knowledge_path(path: str) -> bool:
    """判断路径是否在 knowledge/ 下。"""
    return path.startswith("knowledge/")


def is_valid_publish_target(path: str) -> bool:
    """判断路径是否是合法的 publish target。

    必须指向 knowledge/**。
    不得指向 openspec/** 或 harness/**。
    """
    if path.startswith("openspec/") or path.startswith("harness/"):
        return False
    return path.startswith("knowledge/")


def validate_publish_targets(targets: list[str]) -> list[str]:
    """校验 publish targets 列表。

    返回非法 target 列表。
    """
    invalid = []
    for t in targets:
        if not is_valid_publish_target(t):
            invalid.append(t)
    return invalid
