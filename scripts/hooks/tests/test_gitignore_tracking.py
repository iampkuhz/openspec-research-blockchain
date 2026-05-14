#!/usr/bin/env python3
"""防止核心 hook helper 再次被 .gitignore 误伤的回归测试。

验证关键 lib 文件存在、可 import，且不在 gitignore 屏蔽范围内。
"""

import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent.parent.parent

# 必须在版本控制中的核心 helper
REQUIRED_LIB_FILES = [
    "scripts/hooks/lib/gate_result.py",
    "scripts/hooks/lib/path_policy.py",
    "scripts/hooks/lib/yaml_loader.py",
    "scripts/hooks/lib/change_context.py",
    "scripts/hooks/lib/markdown_utils.py",
]

# 允许不存在的可选文件
OPTIONAL_LIB_FILES = [
    "scripts/hooks/lib/__init__.py",
]


class TestLibFilesExist:
    """核心 lib 文件必须存在于磁盘。"""

    @pytest.mark.parametrize("rel_path", REQUIRED_LIB_FILES)
    def test_required_file_exists(self, rel_path):
        full = ROOT / rel_path
        assert full.is_file(), f"核心 helper 文件不存在: {rel_path}"


class TestLibFilesTracked:
    """核心 lib 文件必须被 git 追踪。"""

    @pytest.mark.parametrize("rel_path", REQUIRED_LIB_FILES)
    def test_tracked_by_git(self, rel_path):
        r = subprocess.run(
            ["git", "ls-files", "--stage", rel_path],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
        )
        assert r.stdout.strip(), f"文件未被 git 追踪: {rel_path}"


class TestLibFilesNotIgnored:
    """核心 lib 文件不应被 .gitignore 屏蔽。"""

    @pytest.mark.parametrize("rel_path", REQUIRED_LIB_FILES)
    def test_not_ignored(self, rel_path):
        r = subprocess.run(
            ["git", "check-ignore", rel_path],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
        )
        # check-ignore 返回 0 = 被忽略，返回 1 = 不被忽略
        assert r.returncode != 0, (
            f"文件被 .gitignore 误伤: {rel_path}\n"
            f"匹配规则: {r.stdout.strip()}"
        )


class TestLibFilesImportable:
    """核心 lib 模块必须可 import。"""

    def test_gate_result_importable(self):
        from scripts.hooks.lib.gate_result import make_result, aggregate_results

        assert callable(make_result)
        assert callable(aggregate_results)

    def test_path_policy_importable(self):
        from scripts.hooks.lib.path_policy import is_in_changes, is_knowledge_path

        assert callable(is_in_changes)
        assert callable(is_knowledge_path)

    def test_yaml_loader_importable(self):
        from scripts.hooks.lib.yaml_loader import load_yaml

        assert callable(load_yaml)

    def test_change_context_importable(self):
        from scripts.hooks.lib.change_context import load_change_context

        assert callable(load_change_context)

    def test_markdown_utils_importable(self):
        from scripts.hooks.lib.markdown_utils import extract_headings

        assert callable(extract_headings)


class TestChangesReadmeTracked:
    """openspec/changes/README.md 必须被追踪且不被 ignore。"""

    def test_tracked(self):
        r = subprocess.run(
            ["git", "ls-files", "--stage", "openspec/changes/README.md"],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
        )
        assert r.stdout.strip(), "openspec/changes/README.md 未被 git 追踪"

    def test_not_ignored(self):
        r = subprocess.run(
            ["git", "check-ignore", "openspec/changes/README.md"],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
        )
        assert r.returncode != 0, (
            f"openspec/changes/README.md 被 .gitignore 误伤: {r.stdout.strip()}"
        )
