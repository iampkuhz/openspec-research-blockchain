#!/usr/bin/env python3
"""change_context — 加载并标准化 change 上下文信息。

职责：
1. 定位 repo root
2. 定位 change_dir
3. 读取 change.yaml
4. 根据 change.yaml schema 读取 openspec schema
5. 根据 task_type 读取 profile
6. 根据 change_operation 读取 operation
7. 返回统一 context dict
"""

import os
from pathlib import Path
from typing import Any

from .yaml_loader import load_yaml


def find_repo_root(start: str | None = None) -> str:
    """从 start 向上查找 repo root（包含 .git 且 .git 是目录的目录）。

    优先匹配 .git 目录，避免误匹配 scripts/openspec/ 等子目录。
    """
    d = Path(start or os.getcwd()).resolve()
    while d != d.parent:
        if (d / ".git").is_dir():
            return str(d)
        d = d.parent
    raise RuntimeError(f"Cannot find repo root from {start or os.getcwd()}")


def find_change_dir(repo_root: str, change_dir: str | None = None) -> str:
    """定位 change 目录。

    优先级：
    1. 显式传入的 change_dir
    2. openspec/changes/ 下唯一的 change 目录
    """
    if change_dir and os.path.isdir(change_dir):
        return os.path.abspath(change_dir)

    # 尝试 openspec/changes/ 下找
    changes_root = os.path.join(repo_root, "openspec", "changes")
    if os.path.isdir(changes_root):
        candidates = [
            os.path.join(changes_root, d)
            for d in os.listdir(changes_root)
            if os.path.isdir(os.path.join(changes_root, d))
            and os.path.exists(os.path.join(changes_root, d, "change.yaml"))
        ]
        if len(candidates) == 1:
            return candidates[0]
        if len(candidates) > 1 and change_dir:
            # 尝试匹配 change_id
            for c in candidates:
                if change_dir in c:
                    return c

    return None


def load_change_context(
    repo_root: str,
    change_dir: str | None = None,
    gate: str | None = None,
    changed_files: list[str] | None = None,
) -> dict[str, Any]:
    """加载 change 上下文。

    返回包含以下 key 的 dict：
    - repo_root: 仓库根目录
    - change_dir: change 目录（可能为 None）
    - change_yaml: change.yaml 内容（可能为 None）
    - task_type: 任务类型
    - change_operation: 变更操作
    - gate: 当前 gate（可能为 None）
    - changed_files: 变更文件列表（可能为 None）
    - error: 错误信息（如果有）
    """
    context: dict[str, Any] = {
        "repo_root": repo_root,
        "change_dir": None,
        "change_yaml": None,
        "task_type": None,
        "change_operation": None,
        "execution_scope": None,
        "gate": gate,
        "changed_files": changed_files or [],
    }

    if not change_dir:
        change_dir = find_change_dir(repo_root)

    if not change_dir:
        context["error"] = "Cannot locate change directory"
        return context

    context["change_dir"] = change_dir
    change_yaml_path = os.path.join(change_dir, "change.yaml")

    if not os.path.exists(change_yaml_path):
        context["error"] = f"change.yaml not found at {change_yaml_path}"
        return context

    try:
        change_yaml = load_yaml(change_yaml_path)
        context["change_yaml"] = change_yaml
        context["task_type"] = change_yaml.get("task_type")
        context["change_operation"] = change_yaml.get("change_operation")
        context["execution_scope"] = change_yaml.get("execution_scope")
        context["change_id"] = change_yaml.get("id")
    except Exception as e:
        context["error"] = f"Failed to load change.yaml: {e}"

    return context
