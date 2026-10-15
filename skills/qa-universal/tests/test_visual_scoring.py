import importlib.util
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location("scoring", Path(__file__).resolve().parents[1] / "scripts" / "score_visual_candidates.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def candidate(name, score, failures=None):
    return {"id": name, "scores": {k: score for k in module.WEIGHTS}, "critical_failures": failures or []}

class VisualScoringTests(unittest.TestCase):
    def test_best_eligible(self):
        self.assertEqual(module.evaluate([candidate("a", 6), candidate("b", 9)])["winner"], "b")
    def test_critical_failure(self):
        self.assertEqual(module.evaluate([candidate("a", 6), candidate("b", 10, ["wrong data"])])["winner"], "a")
    def test_missing_scores(self):
        result = module.evaluate([{"id": "a", "scores": {}}])
        self.assertIsNone(result["winner"])
        self.assertEqual(result["results"][0]["status"], "NOT_TESTED")
    def test_invalid_score(self):
        self.assertEqual(module.evaluate([candidate("a", 11)])["results"][0]["status"], "NOT_TESTED")

if __name__ == "__main__":
    unittest.main()
