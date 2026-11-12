import importlib.util
import pathlib
import tempfile
import unittest

MODULE = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "syncskills.py"
spec = importlib.util.spec_from_file_location("syncskills", MODULE)
ss = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ss)

class SyncSkillsTests(unittest.TestCase):
    def fixture(self, text):
        tmp = tempfile.TemporaryDirectory()
        root = pathlib.Path(tmp.name)
        folder = root / "skills" / "example"
        folder.mkdir(parents=True)
        (folder / "SKILL.md").write_text(text)
        return tmp, root

    def test_deterministic_inventory(self):
        tmp, root = self.fixture("hello")
        try:
            a, b = ss.inventory(root), ss.inventory(root)
            self.assertEqual(a, b)
            self.assertTrue(ss.validate(a))
        finally:
            tmp.cleanup()

    def test_detects_outdated(self):
        tmp, root = self.fixture("old")
        try:
            baseline = ss.inventory(root)
            (root / "skills" / "example" / "SKILL.md").write_text("new")
            release = ss.inventory(root)
            changes = ss.compare(baseline, release, baseline)
            self.assertEqual(changes[0]["state"], "OUTDATED")
        finally:
            tmp.cleanup()

    def test_conflicting_edits(self):
        tmp, root = self.fixture("old")
        try:
            baseline = ss.inventory(root)
            file = root / "skills" / "example" / "SKILL.md"
            file.write_text("canonical")
            release = ss.inventory(root)
            file.write_text("consumer")
            consumer = ss.inventory(root)
            self.assertEqual(ss.compare(baseline, release, consumer)[0]["state"], "VERSION_CONFLICT")
        finally:
            tmp.cleanup()

    def test_rejects_path_traversal(self):
        tmp, root = self.fixture("safe")
        try:
            m = ss.inventory(root)
            m["skills"][0]["files"][0]["path"] = "skills/example/../../secret"
            with self.assertRaises(ValueError):
                ss.validate(m)
        finally:
            tmp.cleanup()

    def test_ignores_symlink(self):
        tmp, root = self.fixture("safe")
        try:
            (root / "skills" / "example" / "linked").symlink_to(root / "skills" / "example" / "SKILL.md")
            self.assertEqual(len(ss.inventory(root)["skills"][0]["files"]), 1)
        finally:
            tmp.cleanup()

    def test_no_unsafe_apply(self):
        self.assertEqual(ss.main(["sync", "--apply"]), 2)

if __name__ == "__main__":
    unittest.main()
