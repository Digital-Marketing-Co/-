"""Deterministic, dependency-free Bone Burner contract regression tests."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[3]
SKILL = ROOT / "skills/bone-burner/SKILL.md"

class BoneBurnerContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.content = SKILL.read_text(encoding="utf-8")

    def test_frontmatter(self):
        self.assertTrue(self.content.startswith("---\n"))
        self.assertIn("name: bone-burner", self.content)

    def test_defensive_only(self):
        for term in ("No retaliation", "read-only", "No automatic deletion", "Never execute suspicious instructions"):
            self.assertIn(term.lower(), self.content.lower())

    def test_injection_and_supply_chain(self):
        for term in ("prompt-injection", "Unicode", "GitHub Actions", "secrets", "supply-chain"):
            self.assertIn(term.lower(), self.content.lower())

    def test_forensic_controls(self):
        for term in ("SHA-256", "commit SHA", "confidence", "counterevidence", "/karma"):
            self.assertIn(term.lower(), self.content.lower())

    def test_verification_gate(self):
        for term in ("two", "QA", "BLOCKED", "regression"):
            self.assertIn(term.lower(), self.content.lower())

if __name__ == "__main__":
    unittest.main()
