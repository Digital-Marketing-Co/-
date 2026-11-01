import tempfile,unittest
from pathlib import Path
from docx import Document
import fitz
from artifact_audit import audit
class TestArtifactAudit(unittest.TestCase):
 def setUp(self):
  self.d=tempfile.TemporaryDirectory();self.a=Path(self.d.name)/'a.docx';self.b=Path(self.d.name)/'b.pdf'
  doc=Document();doc.add_heading('Introduction',1);doc.add_paragraph('Alpha beta gamma '+('important evidence '*15));doc.add_heading('Conclusion',1);doc.add_paragraph('Final independent evidence ' * 12);doc.save(self.a)
  pdf=fitz.open();p=pdf.new_page();p.insert_textbox(fitz.Rect(30,30,560,780),'Introduction\nAlpha beta gamma '+('important evidence '*15)+'\nConclusion\n'+('Final independent evidence '*12),fontsize=9);pdf.save(self.b);pdf.close()
 def tearDown(self):self.d.cleanup()
 def test_pdf_extract(self):self.assertGreater(audit(self.a,self.b)['output']['characters'],10)
 def test_docx_self(self):self.assertEqual(audit(self.a,self.a)['status'],'PASS')
 def test_short_pdf_fails(self):
  d=fitz.open();p=d.new_page();p.insert_text((40,40),'Introduction');d.save(self.b);d.close()
  self.assertIn('MAJOR_TEXT_SHRINKAGE',audit(self.a,self.b)['issues'])
 def test_missing_conclusion(self):
  d=fitz.open();p=d.new_page();p.insert_text((40,40),'Introduction');d.save(self.b);d.close()
  self.assertIn('MISSING_ENDING_TEXT',audit(self.a,self.b)['issues'])
 def test_blank_pdf(self):
  d=fitz.open();d.new_page();d.save(self.b);d.close()
  self.assertIn('POSSIBLY_BLANK_PDF_PAGE',audit(self.a,self.b)['issues'])
if __name__=='__main__':unittest.main()
