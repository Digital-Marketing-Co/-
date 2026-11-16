import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location('new_skill', Path(__file__).resolve().parents[1] / 'scripts' / 'new_skill.py')
new_skill = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(new_skill)

class SkillScaffoldingTests(unittest.TestCase):
    def test_complete_scaffold(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = new_skill.scaffold(root, 'example-skill', 'A sample skill')
            self.assertEqual(len(paths), 3)
            self.assertTrue(all(p.is_file() for p in paths))
            self.assertEqual(json.loads((root / 'skills/example-skill/evals/quality-cases.json').read_text())['skill'], 'example-skill')
            with self.assertRaises(FileExistsError):
                new_skill.scaffold(root, 'example-skill', 'A sample skill')
    def test_rejects_invalid_names(self):
        with tempfile.TemporaryDirectory() as tmp:
            for name in ('bad/name', 'bad name', ''):
                with self.assertRaises(ValueError):
                    new_skill.scaffold(Path(tmp), name, 'Description')

if __name__ == '__main__':
    unittest.main()
