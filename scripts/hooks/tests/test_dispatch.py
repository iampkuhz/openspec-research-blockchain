#!/usr/bin/env python3
"""Test dispatch.py with fixtures."""

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent.parent
FIXTURES = Path(__file__).resolve().parent / "fixtures"
DISPATCH = Path(__file__).resolve().parent.parent / "dispatch.py"


class TestDispatch(unittest.TestCase):
    """Test dispatch with fixtures."""

    def run_dispatch(self, change_id: str, gate: str, expect_exit: int = 0):
        """Run dispatch.py with given change and gate."""
        change_dir = str(FIXTURES / change_id)
        result = subprocess.run(
            [sys.executable, str(DISPATCH), "--change", change_dir, "--gate", gate, "--json"],
            capture_output=True,
            text=True,
            cwd=str(ROOT),
        )
        return result

    def test_success_primitive_post_draft(self):
        """success-primitive should pass post_draft gate."""
        result = self.run_dispatch("success-primitive", "post_draft")
        # Should exit 0
        self.assertEqual(result.returncode, 0, f"stderr: {result.stderr}")

    def test_success_primitive_pre_publish(self):
        """success-primitive should pass pre_publish gate."""
        result = self.run_dispatch("success-primitive", "pre_publish")
        self.assertEqual(result.returncode, 0, f"stderr: {result.stderr}")

    def test_fail_missing_draft_section_post_draft(self):
        """fail-missing-draft-section should fail post_draft gate."""
        result = self.run_dispatch("fail-missing-draft-section", "post_draft")
        self.assertEqual(result.returncode, 2, f"Expected exit 2, got {result.returncode}, stderr: {result.stderr}")

    def test_fail_bad_publish_target_pre_publish(self):
        """fail-bad-publish-target should fail pre_publish gate."""
        result = self.run_dispatch("fail-bad-publish-target", "pre_publish")
        self.assertEqual(result.returncode, 2, f"Expected exit 2, got {result.returncode}, stderr: {result.stderr}")

    def test_fail_decision_missing_verdict(self):
        """fail-decision-missing-verdict should fail pre_publish gate."""
        result = self.run_dispatch("fail-decision-missing-verdict", "pre_publish")
        self.assertEqual(result.returncode, 2, f"Expected exit 2, got {result.returncode}, stderr: {result.stderr}")

    def test_fail_blocking_gate_chain_pre_publish(self):
        """fail-blocking-gate-chain: post-draft fail+blocking, pre_publish must fail."""
        result = self.run_dispatch("fail-blocking-gate-chain", "pre_publish")
        self.assertEqual(result.returncode, 2, f"Expected exit 2 (blocking gate chain), got {result.returncode}, stderr: {result.stderr}")

    def test_fail_draft_diagram_todo_post_review(self):
        """fail-draft-diagram-todo: draft has diagram TODO, post_review must fail."""
        result = self.run_dispatch("fail-draft-diagram-todo", "post_review")
        self.assertEqual(result.returncode, 2, f"Expected exit 2 (diagram TODO), got {result.returncode}, stderr: {result.stderr}")

    def test_pass_dedup_clean_post_plan(self):
        """pass-dedup-clean: no duplicate changes, consistent targets, post_plan should pass."""
        result = self.run_dispatch("pass-dedup-clean", "post_plan")
        self.assertEqual(result.returncode, 0, f"Expected exit 0 (clean dedup), got {result.returncode}, stderr: {result.stderr}")

    def test_pass_synthesis_inherited_post_research(self):
        """pass-synthesis-inherited: source_pack with inherited mode, post_research should pass."""
        result = self.run_dispatch("pass-synthesis-inherited", "post_research")
        self.assertEqual(result.returncode, 0, f"Expected exit 0 (inherited sources), got {result.returncode}, stderr: {result.stderr}")


class TestDispatchPrettyJsonParsing(unittest.TestCase):
    """Test that dispatch correctly parses pretty-printed JSON validator output."""

    def test_run_validator_parses_pretty_json(self):
        """Verify that run_validator parses multi-line (indented) JSON output, not just single-line."""
        from scripts.hooks.dispatch import run_validator
        from scripts.hooks.lib.gate_result import make_result
        import json

        # Simulate a validator entry that outputs pretty JSON
        validator_entry = {"script": "hooks/validators/schema_package.py"}

        # We can't easily test the actual subprocess call here, so test the
        # JSON extraction logic indirectly via a real validator that outputs pretty JSON
        validator_entry_ref = {"script": "hooks/validators/reference_integrity.py"}

        result = run_validator(
            "reference_integrity",
            validator_entry_ref,
            str(ROOT),
            "governance_check",
            {"blocking": True, "rule_refs": [], "files": {"required": []}},
            str(ROOT),
        )

        # The result should be a parsed dict, not have the JSON in warnings
        self.assertIsInstance(result, dict)
        self.assertIn("validator", result)
        self.assertEqual(result["validator"], "reference_integrity")
        # Should NOT have the JSON blob in warnings
        for w in result.get("warnings", []):
            self.assertFalse(
                w.strip().startswith("{"),
                f"Pretty JSON should not appear in warnings: {w[:100]}"
            )

    def test_run_validator_missing_script(self):
        """Missing validator script should return error result."""
        from scripts.hooks.dispatch import run_validator

        result = run_validator(
            "nonexistent_validator",
            {"script": "hooks/validators/nonexistent.py"},
            str(ROOT),
            "test_gate",
            {"blocking": True, "rule_refs": [], "files": {"required": []}},
            str(ROOT),
        )

        self.assertEqual(result["status"], "error")
        self.assertTrue(len(result["errors"]) > 0)


if __name__ == "__main__":
    unittest.main()
