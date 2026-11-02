"""Regression checks for the canonical quality-cases fixture contract."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class QualityCaseContractTests(unittest.TestCase):
    def test_all_skill_fixtures_have_required_fields(self):
        fixtures = sorted((ROOT / "skills").glob("*/evals/quality-cases.json"))
        self.assertTrue(fixtures, "No skill fixtures found")
        for path in fixtures:
            with self.subTest(path=str(path.relative_to(ROOT))):
                data = json.loads(path.read_text(encoding="utf-8"))
                self.assertEqual(data.get("skill"), path.parent.parent.name)
                cases = data.get("cases")
                self.assertIsInstance(cases, list)
                self.assertTrue(cases)
                seen = set()
                for case in cases:
                    self.assertIsInstance(case, dict)
                    if case.get("id") is not None:
                        self.assertTrue(str(case["id"]).strip())
                        self.assertNotIn(case["id"], seen)
                        seen.add(case["id"])
                    self.assertIsInstance(case.get("prompt"), str)
                    self.assertTrue(case["prompt"].strip())
                    self.assertIsInstance(case.get("assertions"), list)
                    self.assertTrue(case["assertions"])
                    self.assertTrue(all(isinstance(x, str) and x.strip() for x in case["assertions"]))
                    self.assertIsInstance(case.get("grader"), str)
                    self.assertTrue(case["grader"].strip())


if __name__ == "__main__":
    unittest.main()
