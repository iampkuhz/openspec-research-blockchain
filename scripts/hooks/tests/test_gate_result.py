#!/usr/bin/env python3
"""Test gate_result aggregation, especially advisory vs blocking semantics."""

import unittest

from scripts.hooks.lib.gate_result import make_result, aggregate_results


class TestAggregateResults(unittest.TestCase):
    """Test aggregate_results behavior."""

    def test_all_pass(self):
        results = [
            make_result("test", "v1", "pass", blocking=True),
            make_result("test", "v2", "pass", blocking=True),
        ]
        agg = aggregate_results("test", True, results)
        self.assertEqual(agg["status"], "pass")

    def test_blocking_fail(self):
        results = [
            make_result("test", "v1", "fail", blocking=True),
            make_result("test", "v2", "pass", blocking=True),
        ]
        agg = aggregate_results("test", True, results)
        self.assertEqual(agg["status"], "fail")

    def test_advisory_fail_does_not_block_gate(self):
        """blocking=false validator fail should downgrade to warn, not fail the gate."""
        results = [
            make_result("test", "advisory_v", "fail", blocking=False, errors=["dead ref"]),
            make_result("test", "blocking_v", "pass", blocking=True),
        ]
        agg = aggregate_results("test", True, results)
        self.assertEqual(agg["status"], "warn")
        # Advisory error should appear in warnings, not errors
        self.assertTrue(any("advisory" in w for w in agg["warnings"]))

    def test_advisory_fail_with_blocking_pass_other(self):
        """Advisory fail + pass other -> warn, not pass or fail."""
        results = [
            make_result("test", "advisory", "fail", blocking=False, errors=["some issue"]),
            make_result("test", "normal", "pass", blocking=True),
        ]
        agg = aggregate_results("test", True, results)
        self.assertEqual(agg["status"], "warn")

    def test_blocking_fail_with_advisory_pass(self):
        """blocking=true fail should still fail gate, even if advisory validator passes."""
        results = [
            make_result("test", "blocking_v", "fail", blocking=True, errors=["schema error"]),
            make_result("test", "advisory", "pass", blocking=False),
        ]
        agg = aggregate_results("test", True, results)
        self.assertEqual(agg["status"], "fail")

    def test_advisory_error_downgraded_to_warn(self):
        """blocking=false validator error should also be downgraded to warn."""
        results = [
            make_result("test", "advisory", "error", blocking=False, errors=["crash"]),
        ]
        agg = aggregate_results("test", True, results)
        self.assertEqual(agg["status"], "warn")

    def test_all_skip(self):
        results = [
            make_result("test", "v1", "skip", blocking=True),
            make_result("test", "v2", "skip", blocking=True),
        ]
        agg = aggregate_results("test", False, results)
        self.assertEqual(agg["status"], "skip")

    def test_default_blocking_is_true(self):
        """Validator without explicit blocking field should default to blocking=True."""
        # Manually construct a result without blocking field
        result_no_blocking = {"validator": "v1", "status": "fail", "errors": ["x"], "checked_files": [], "warnings": [], "rule_refs": []}
        results = [
            result_no_blocking,
            make_result("test", "v2", "pass", blocking=True),
        ]
        agg = aggregate_results("test", True, results)
        self.assertEqual(agg["status"], "fail")


if __name__ == "__main__":
    unittest.main()
