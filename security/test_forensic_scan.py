import unittest
from forensic_scan import inspect
class ScanTests(unittest.TestCase):
 def test_bidi(self): self.assertIn("bidi-control",[x["kind"] for x in inspect("x","safe\u202eunsafe")])
 def test_invisible(self): self.assertIn("invisible-character",[x["kind"] for x in inspect("x","a\u200bb")])
 def test_nfkc(self): self.assertIn("compatibility-normalization-difference",[x["kind"] for x in inspect("x","Ａ")])
 def test_clean(self): self.assertEqual([],inspect("x","plain ASCII list\n1. item"))
if __name__=="__main__": unittest.main()
