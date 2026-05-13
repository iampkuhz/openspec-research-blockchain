#!/usr/bin/env python3
"""Test source-evidence-agent prompt contract.

Verifies that the agent prompt contains:
- Preflight as first mandatory step
- Read budget limits
- Loop protection with hard thresholds
- Blocked handoff path for no web tools
"""

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent.parent
AGENT_FILE = ROOT / ".claude" / "agents" / "source-evidence-agent.md"


class TestSourceAgentPreflight(unittest.TestCase):
    """Verify source-evidence-agent prompt has required guardrails."""

    def setUp(self):
        self.content = AGENT_FILE.read_text()

    def test_preflight_section_exists(self):
        """Agent must have a preflight section as first step."""
        self.assertIn("工具预检", self.content, "Missing preflight section (工具预检)")
        self.assertIn("preflight", self.content.lower(), "Missing preflight keyword")

    def test_preflight_is_first_step(self):
        """Preflight must appear before the main Workflow section."""
        preflight_idx = self.content.find("工具预检")
        workflow_idx = self.content.find("## Workflow")
        self.assertLess(
            preflight_idx, workflow_idx,
            "Preflight section must appear before Workflow section"
        )

    def test_read_budget_exists(self):
        """Agent must have explicit read budget limits."""
        self.assertIn("读取预算", self.content, "Missing read budget section (读取预算)")
        # Check for numeric limits
        self.assertIn("2 次", self.content, "Missing '2 次' limit for same template")
        self.assertIn("3 次", self.content, "Missing '3 次' limit for consecutive no-write calls")

    def test_blocked_handoff_for_no_tools(self):
        """Agent must have blocked handoff path when no web tools available."""
        self.assertIn("硬停止路径", self.content, "Missing hard stop path section")
        self.assertIn("blocked", self.content.lower(), "Missing blocked handoff")
        self.assertIn("web_tools_unavailable", self.content, "Missing web_tools_unavailable blocker")

    def test_no_repeat_template_read(self):
        """Agent must forbid repeating the same template read after unchanged response."""
        self.assertIn("File unchanged since last read", self.content,
                      "Missing unchanged file protection")

    def test_note_md_not_required_without_search(self):
        """Agent must not require reading note.md template when no search tools."""
        # The preflight should check tools BEFORE reading any template
        preflight_section = self.content[self.content.find("工具预检"):self.content.find("## 读取预算")]
        self.assertIn("写入能力检查", preflight_section,
                      "Preflight must check write capability first")
        self.assertIn("联网工具检查", preflight_section,
                      "Preflight must check web tools")


if __name__ == "__main__":
    unittest.main()
