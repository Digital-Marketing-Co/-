import tempfile,unittest
from pathlib import Path
import fitz
from pdf_render_evidence import render

class RenderTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
  self.src=self.root/"source.pdf"
  d=fitz.open()
  for i in range(3):
   p=d.new_page();p.insert_text((45,55),f"Page {i+1}",fontsize=12)
  d.save(self.src);d.close()
 def tearDown(self):self.tmp.cleanup()
 def test_all_pages_render_and_hash(self):
  r=render(self.src,self.root/"out")
  self.assertEqual(r["page_count"],3)
  self.assertEqual(len(list((self.root/"out").glob("page-*.png"))),3)
  self.assertEqual(len(r["rendered_pages"][0]["sha256"]),64)
  self.assertEqual(r["visual_inspection"],"NOT TESTED")
 def test_no_stale_overwrite(self):
  render(self.src,self.root/"out")
  with self.assertRaises(ValueError):render(self.src,self.root/"out")
 def test_reject_bad_dpi(self):
  with self.assertRaises(ValueError):render(self.src,self.root/"out",40)
 def test_geometry_flag_integrated(self):
  r=render(self.src,self.root/"out")
  self.assertEqual(r["geometry"]["pages_checked"],3)
if __name__=="__main__":unittest.main()
