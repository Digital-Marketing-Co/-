import unittest
from coverage import check
BASE={'sections':['intro','methods','conclusion'],'equations':['eq1'],'figures':['fig1'],'tables':['t1'],'citations':['c1'],'appendices':['appendix-a'],'source_revision':'abc','last_section_text_sha256':'deadbeef'}
class Cases(unittest.TestCase):
 def test_all_present(self):self.assertEqual(check(BASE,dict(BASE))['status'],'PASS')
 def test_missing_section(self):self.assertIn('sections: missing',str(check(BASE,{**BASE,'sections':['intro','conclusion']})['issues']))
 def test_duplicate_figure(self):self.assertIn('duplicate',str(check(BASE,{**BASE,'figures':['fig1','fig1']})['issues']))
 def test_stale_export(self):self.assertIn('source_revision: mismatch',str(check(BASE,{**BASE,'source_revision':'old'})['issues']))
 def test_missing_appendix(self):self.assertEqual(check(BASE,{**BASE,'appendices':[]})['status'],'FAIL')
 def test_missing_end(self):self.assertEqual(check(BASE,{**BASE,'last_section_text_sha256':'wrong'})['status'],'FAIL')
 def test_missing_citation(self):self.assertEqual(check(BASE,{**BASE,'citations':[]})['status'],'FAIL')
 def test_invalid_id(self):self.assertEqual(check(BASE,{**BASE,'tables':['']})['status'],'FAIL')
if __name__=='__main__':unittest.main()
