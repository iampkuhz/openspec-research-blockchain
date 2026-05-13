#!/usr/bin/env python3
"""Tests for the protected_paths validator."""

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent.parent.parent
VALIDATOR = ROOT / "scripts/hooks/validators/protected_paths.py"


def run_validator(files: list[str], change: str | None = None) -> subprocess.CompletedProcess:
    cmd = [sys.executable, str(VALIDATOR)]
    for f in files:
        cmd += ["--files", f]
    if change:
        cmd += ["--change", change]
    return subprocess.run(cmd, capture_output=True, text=True)


class TestProtectedPathsDetection:
    """验证受保护路径正确识别"""

    def test_blocks_claude_file(self):
        r = run_validator([".claude/commands/spec-research.md"])
        result = json.loads(r.stdout)
        assert result["status"] == "fail"
        assert any("blocked" in e for e in result["errors"])

    def test_blocks_harness_file(self):
        r = run_validator(["harness/workflows/research-pipeline.md"])
        result = json.loads(r.stdout)
        assert result["status"] == "fail"

    def test_blocks_openspec_specs(self):
        r = run_validator(["openspec/specs/evidence-policy/spec.md"])
        result = json.loads(r.stdout)
        assert result["status"] == "fail"

    def test_blocks_openspec_schemas(self):
        r = run_validator(["openspec/schemas/blockchain-research/schema.yaml"])
        result = json.loads(r.stdout)
        assert result["status"] == "fail"

    def test_blocks_agents_md(self):
        r = run_validator(["AGENTS.md"])
        result = json.loads(r.stdout)
        assert result["status"] == "fail"

    def test_blocks_claude_md(self):
        r = run_validator(["CLAUDE.md"])
        result = json.loads(r.stdout)
        assert result["status"] == "fail"

    def test_blocks_docs_governance(self):
        r = run_validator(["docs/governance/openspec-harness-boundary.md"])
        result = json.loads(r.stdout)
        assert result["status"] == "fail"

    def test_passes_normal_research_file(self):
        r = run_validator(["openspec/changes/primitive_test_draft/draft.md"])
        result = json.loads(r.stdout)
        assert result["status"] == "pass"

    def test_passes_knowledge_file(self):
        r = run_validator(["knowledge/analysis/primitives/test/artifact.md"])
        result = json.loads(r.stdout)
        assert result["status"] == "pass"


class TestGovernanceContextOverride:
    """治理上下文允许写入受保护路径"""

    def test_governance_change_allows_protected_writes(self, tmp_path):
        # 创建一个 governance 类型的 change
        change_dir = tmp_path / "openspec/changes" / "governance_hook_fix"
        change_dir.mkdir(parents=True)
        (change_dir / "change.yaml").write_text(
            "task_type: governance_review\nchange_operation: update\n"
        )

        # 使用相对路径形式，模拟 .claude/ 下的文件
        r = run_validator(
            [".claude/commands/spec-research.md"],
            change=str(change_dir),
        )
        result = json.loads(r.stdout)
        assert result["status"] == "pass"
        assert any("governance" in w.lower() for w in result["warnings"])

    def test_non_governance_change_blocks_protected_writes(self, tmp_path):
        change_dir = tmp_path / "openspec/changes" / "primitive_test"
        change_dir.mkdir(parents=True)
        (change_dir / "change.yaml").write_text(
            "task_type: primitive\nchange_operation: create\n"
        )

        r = run_validator(
            [".claude/agents/source-evidence-agent.md"],
            change=str(change_dir),
        )
        result = json.loads(r.stdout)
        assert result["status"] == "fail"
        assert any("protected" in e.lower() for e in result["errors"])


class TestPromptKeywords:
    """验证 prompt 中包含正确的引导信息"""

    def test_error_mentions_governance_review_command(self):
        r = run_validator([".claude/agents/publish-agent.md"])
        result = json.loads(r.stdout)
        assert any("spec-governance-review" in e for e in result["errors"])

    def test_error_mentions_direct_modification_prohibited(self):
        r = run_validator(["harness/rules/_index.yaml"])
        result = json.loads(r.stdout)
        assert any("direct modification" in e.lower() for e in result["errors"])
