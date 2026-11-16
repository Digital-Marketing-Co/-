"""Regression guard for the cross-skill terminal mathematical QA contract.

This tests repository instructions, NOT PDF rendering or actual ITQE execution.
"""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CONSUMERS = (
    "skills/God/SKILL.md",
    "skills/pe/SKILL.md",
    "skills/4629/SKILL.md",
    "skills/Complete/SKILL.md",
    "skills/latex/SKILL.md",
    "skills/expound/SKILL.md",
    "skills/exhaustive/SKILL.md",
    "skills/textbook/SKILL.md",
    "skills/book/SKILL.md",
    "skills/iterate/SKILL.md",
    "skills/disabled/SKILL.md",
    "skills/karma/SKILL.md",
    "skills/sync/SKILL.md",
)

class TestTerminalMathContract(unittest.TestCase):
    def test_consumers_reference_terminal_math_gate(self):
        for rel in CONSUMERS:
            with self.subTest(path=rel):
                content = (ROOT / rel).read_text(encoding="utf-8").lower()
                self.assertIn("post-artifact-itqe-latex-qa.md", content)
                self.assertIn("/itqe", content)
                self.assertIn("/latex", content)

    def test_terminal_gate_is_not_self_invoking(self):
        contract = (ROOT / "skills/references/post-artifact-itqe-latex-qa.md").read_text(encoding="utf-8")
        self.assertNotIn("invoke the canonical shared `skills/references/post-artifact-itqe-latex-qa.md` gate", contract)
        self.assertIn("execute this canonical shared gate exactly once", contract)

    def test_ci_triggers_on_consumer_edits(self):
        workflow = (ROOT / ".github/workflows/god-document-qa.yml").read_text(encoding="utf-8")
        for rel in ("skills/pe/**", "skills/4629/**", "skills/latex/**",
                    "skills/Complete/**", "skills/references/post-artifact-itqe-latex-qa.md"):
            with self.subTest(path=rel):
                self.assertIn(rel, workflow)

if __name__ == "__main__":
    unittest.main()
