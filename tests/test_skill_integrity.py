import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def module(path):
    spec=importlib.util.spec_from_file_location(path.stem,path)
    result=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


class IntegrityTests(unittest.TestCase):
    def test_canonical_tree(self):
        report=module(ROOT/'scripts/validate_skills.py').audit(ROOT)
        self.assertEqual(report['errors'],[])
        self.assertEqual(report['skill_count'],59)

    def test_resolver_checkout_identity(self):
        resolver=module(ROOT/'skills/interop/scripts/resolve_root.py')
        self.assertEqual(resolver.resolve('deep'),ROOT/'skills/deep')
        with self.assertRaises(ValueError):resolver.resolve('../deep')

    def test_resolver_installed_identity_and_ambiguity(self):
        resolver=module(ROOT/'skills/interop/scripts/resolve_root.py')
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp); a=root/'generated-id';a.mkdir()
            (a/'SKILL.md').write_text('---\nname: example\ndescription: fixture\n---\n')
            self.assertEqual(resolver.resolve('example',[root]),a)
            b=root/'second-id';b.mkdir();(b/'SKILL.md').write_bytes((a/'SKILL.md').read_bytes())
            with self.assertRaises(ValueError):resolver.resolve('example',[root])
            with self.assertRaises(FileNotFoundError):resolver.resolve('absent',[root])

    def test_artifact_staging_creation(self):
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/'new'/'artifacts'
            run=subprocess.run([sys.executable,str(ROOT/'skills/interop/scripts/resolve_artifacts.py'),'--path',str(path)],capture_output=True,text=True)
            self.assertEqual(run.returncode,0,run.stderr)
            self.assertEqual(run.stdout.strip(),str(path))
            self.assertTrue(path.is_dir())


if __name__=='__main__':unittest.main()
