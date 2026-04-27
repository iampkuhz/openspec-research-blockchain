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


if __name__ == "__main__":
    unittest.main()
