import unittest,tempfile,pathlib,subprocess,json,sys
SCRIPT=pathlib.Path(__file__).with_name('verify_skills.py')
class AuditTests(unittest.TestCase):
    def run_audit(self,files):
        with tempfile.TemporaryDirectory() as d:
            root=pathlib.Path(d)
            for name,content in files.items():
                p=root/'skills'/name/'SKILL.md'
                p.parent.mkdir(parents=True)
                p.write_text(content)
            out=root/'report.json'
            proc=subprocess.run([sys.executable,str(SCRIPT),str(root),'--out',str(out)],capture_output=True,text=True)
            return proc.returncode,json.loads(out.read_text())
    def test_valid_skill(self):
        code,r=self.run_audit({'alpha':'---\nname: alpha\ndescription: test\n---\n# Alpha\n'})
        self.assertEqual(code,0)
        self.assertEqual(r['skill_count'],1)
    def test_missing_reference(self):
        _,r=self.run_audit({'alpha':'---\nname: alpha\ndescription: test\n---\n[missing](references/no.md)'})
        self.assertTrue(any(x['kind']=='missing-relative-reference' for x in r['findings']))
    def test_unicode_control(self):
        _,r=self.run_audit({'alpha':'---\nname: alpha\ndescription: test\n---\n\u202e'})
        self.assertTrue(any(x['kind']=='unicode-control' for x in r['findings']))
    def test_empty_repository_fails(self):
        code,r=self.run_audit({})
        self.assertEqual(code,2)
        self.assertEqual(r['release_status'],'NOT_VERIFIED')
    def test_secret_redacted(self):
        _,r=self.run_audit({'alpha':'---\nname: alpha\ndescription: test\n---\napi_key=abcdefghijklmnopqrstuvwx'})
        self.assertTrue(any(x['kind']=='possible-secret' for x in r['findings']))
        self.assertNotIn('abcdefghijklmnopqrstuvwx',json.dumps(r))
if __name__=='__main__':
    unittest.main(verbosity=2)
