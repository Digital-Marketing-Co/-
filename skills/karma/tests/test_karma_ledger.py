import json, pathlib, tempfile, unittest
from karma_ledger import append,verify
class TestLedger(unittest.TestCase):
 def setUp(self):
  self.t=tempfile.TemporaryDirectory();self.p=pathlib.Path(self.t.name)/'ledger.jsonl'
 def tearDown(self):self.t.cleanup()
 def test_chain(self):
  append(self.p,{'status':'OBSERVED'});append(self.p,{'status':'VERIFIED'})
  self.assertEqual(verify(self.p)['count'],2)
 def test_tamper(self):
  append(self.p,{'status':'OBSERVED','observed':'before'})
  self.p.write_text(self.p.read_text().replace('before','after'))
  with self.assertRaises(ValueError):verify(self.p)
 def test_redaction(self):
  append(self.p,{'token':'sensitive','observed':'password=exposed'})
  self.assertNotIn('sensitive',self.p.read_text());self.assertNotIn('exposed',self.p.read_text())
 def test_status(self):
  with self.assertRaises(ValueError):append(self.p,{'status':'NONSENSE'})
 def test_empty(self):self.assertEqual(verify(self.p)['count'],0)
if __name__=='__main__':unittest.main()
