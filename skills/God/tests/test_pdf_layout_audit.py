import tempfile, unittest
from pathlib import Path
import fitz
from pdf_layout_audit import inspect
class Tests(unittest.TestCase):
    def make(self, callback):
        f=tempfile.NamedTemporaryFile(suffix='.pdf',delete=False);f.close()
        d=fitz.open();p=d.new_page();callback(p);d.save(f.name);d.close()
        self.addCleanup(lambda:Path(f.name).unlink(missing_ok=True))
        return f.name
    def test_normal(self):
        p=self.make(lambda pg:pg.insert_text((40,50),'Readable text',fontsize=12))
        self.assertEqual(inspect(p)['status'],'NO_GEOMETRY_FLAGS')
    def test_blank(self):
        p=self.make(lambda pg:None)
        self.assertIn('NO_EXTRACTABLE_TEXT',[x['type'] for x in inspect(p)['issues']])
    def test_tiny(self):
        p=self.make(lambda pg:pg.insert_text((40,50),'Tiny text',fontsize=4))
        self.assertIn('VERY_SMALL_TEXT',[x['type'] for x in inspect(p)['issues']])
if __name__=='__main__': unittest.main()
