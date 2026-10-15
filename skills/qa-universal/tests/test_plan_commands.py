import importlib.util
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location("planner", Path(__file__).resolve().parents[1] / "scripts" / "plan_commands.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class CommandPlannerTests(unittest.TestCase):
    def test_order_independence(self):
        a = module.plan("Please /images create a report /banner")
        b = module.plan("Please /banner create a report /images")
        self.assertEqual(a["execution_order"], b["execution_order"])
        self.assertEqual(a["execution_order"], ["banner", "images"])

    def test_dedup(self):
        p = module.plan("/banner /banner /images /images")
        self.assertEqual(p["execution_order"], ["banner", "images"])

    def test_any_position(self):
        p = module.plan("Start with a report and later /images then /copyright.")
        self.assertEqual(p["execution_order"], ["banner", "images", "copyright"])

    def test_inert_source_and_url(self):
        p = module.plan("https://example.com/banner `/images` ```\n/banner\n```\n> /images\n/copyright")
        self.assertEqual(p["execution_order"], ["copyright"])

    def test_math_dependency(self):
        p = module.plan("/itqe /latex")
        self.assertEqual(p["execution_order"], ["latex", "itqe"])

    def test_cycle_rejected(self):
        old = dict(module.DEPENDENCIES)
        try:
            module.DEPENDENCIES.update({"alpha": ["beta"], "beta": ["alpha"]})
            with self.assertRaises(ValueError):
                module.plan("/alpha")
        finally:
            module.DEPENDENCIES.clear()
            module.DEPENDENCIES.update(old)

if __name__ == "__main__":
    unittest.main()
