"""Offline publication fixtures: actual PDFs, footers, pagination and links."""
import importlib.util
import json
from datetime import date
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import fitz

ROOT = Path(__file__).resolve().parents[1]
BUILDERS = [
    ('article-clip-pdf', 'build_cm_pdf.py'), ('deep', 'build_deep_pdf.py'),
    ('folio', 'build_folio_pdf.py'), ('folio', 'build_monograph_pdf.py'),
    ('phd-ivy-monograph', 'build_folio_pdf.py'),
    ('phd-ivy-monograph', 'build_monograph_pdf.py'),
    ('print', 'build_print_pdf.py'), ('corpus', 'build_corpus_pdf.py'),
]

class PublicationTests(unittest.TestCase):
    def test_rendered_future_year(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            source, output = directory / 'future.json', directory / 'future.pdf'
            source.write_text(json.dumps({'title': 'Future Year Fixture', 'paragraphs': ['Evidence record.']}))
            script = ROOT / 'skills/article-clip-pdf/scripts/build_cm_pdf.py'
            wrapper = ('import sys,runpy,datetime;from pathlib import Path;'
                       'p=Path(sys.argv[1]);sys.path.insert(0,str(p.parent));'
                       'import publication_notice as n;'
                       'exec("class FutureDate(datetime.date):\\n @classmethod\\n def today(cls): return cls(2031,1,1)");'
                       'n.date=FutureDate;sys.argv=sys.argv[1:];runpy.run_path(str(p),run_name="__main__")')
            result = subprocess.run([sys.executable, '-c', wrapper, str(script), str(source), '--out', str(output)],
                                    capture_output=True, text=True, timeout=30)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            with fitz.open(output) as doc:
                self.assertIn('© 2012–2031 Web Development Corporation. All rights reserved.', doc[0].get_text())

    def test_notice_year_and_owner(self):
        for skill in ['copyright', *dict.fromkeys(s for s, _ in BUILDERS)]:
            path = ROOT / 'skills' / skill / 'scripts' / ('notice.py' if skill == 'copyright' else 'publication_notice.py')
            self.assertEqual(path.read_bytes(), (ROOT / 'skills/copyright/scripts/notice.py').read_bytes())
            spec = importlib.util.spec_from_file_location('notice_test', path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            self.assertEqual(module.notice_text(2012, 2031, 'Test Press'),
                             '© 2012–2031 Test Press. All rights reserved.')
            self.assertIn(f'2012–{date.today().year}', module.notice_for())
            self.assertEqual(module.notice_for({'owner': {'short': 'Test Press', 'founded': 2004}}),
                             f'© 2004–{date.today().year} Test Press. All rights reserved.')

    def test_pdf_builders(self):
        text = 'A measured result connects evidence to the stated question. ' * 24
        data = {
            'title': 'Offline Evidence Study', 'author': 'Ada Example', 'date': '1999-01-01',
            'url': 'https://example.org/source', 'source_url': 'https://example.org/source',
            'source_name': 'Example Journal', 'abstract': 'An offline <a href="https://example.org/source">publication fixture</a>.',
            'owner': {'short': 'Test Press', 'legal': 'Test Press', 'founded': 2004},
            'paragraphs': [text] * 8,
            'blocks': [{'type': 'paragraph', 'text': text} for _ in range(8)],
            'sections': [{'id': 'evidence', 'title': 'Evidence', 'paragraphs': [text] * 8},
                         {'id': 'references', 'title': 'References', 'kind': 'bibliography'}],
            'bibliography': ['Example, Ada. Evidence Study. Test Press, 2024.'],
            'works': [{'title': f'Evidence Study {i}', 'year': 2024,
                       'authors': [{'family': 'Example', 'given': 'Ada'}],
                       'doi': f'10.0000/example{i}', 'url': 'https://example.org/source'} for i in range(30)],
        }
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            source = directory / 'fixture.json'
            for skill, builder in BUILDERS:
                with self.subTest(skill=skill, builder=builder):
                    fixture = json.loads(json.dumps(data))
                    if skill in ('deep', 'folio', 'phd-ivy-monograph'):
                        fixture['sections'][0]['paragraphs'][0] += ' Evidence citation {{1}}.'
                        fixture['notes'] = [{'n': 1, 'text': 'Fixture source note.'}]
                        fixture['sections'][0]['paragraphs'].append({
                            'type': 'equation', 'unicode': 'E = mc²',
                            'caption': 'Energy relation',
                            'itqe': [{'identifier': 'E', 'term': 'Energy', 'quantity': 'J',
                                      'explanation': 'Measured energy'}],
                        })
                    source.write_text(json.dumps(fixture))
                    output = directory / f'{skill}-{builder}.pdf'
                    wrapper = ('import sys,runpy;from pathlib import Path;'
                               'p=Path(sys.argv[1]);sys.path.insert(0,str(p.parent));'
                               'sys.path.insert(0,str(p.parent.parent / "assets"));'
                               'exec("try:\\n import discoverability as d\\n d.resolve_canonical_origin=lambda: d.FALLBACK_ORIGIN\\nexcept ImportError: pass");'
                               'sys.argv=sys.argv[1:];runpy.run_path(str(p),run_name="__main__")')
                    result = subprocess.run([sys.executable, '-c', wrapper, str(ROOT / 'skills' / skill / 'scripts' / builder),
                                             str(source), '--out', str(output)],
                                            capture_output=True, text=True, timeout=90)
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                    with fitz.open(output) as doc:
                        self.assertGreaterEqual(len(doc), 2)
                        self.assertIn(data['title'], ' '.join(' '.join(p.get_text() for p in doc).split()))
                        for page in doc:
                            lines = [line for b in page.get_text('dict')['blocks'] for line in b.get('lines', [])]
                            notices = [line for line in lines if '©' in ''.join(s['text'] for s in line['spans'])]
                            self.assertEqual(len(notices), 1, page.get_text())
                            line = notices[0]
                            notice = ''.join(s['text'] for s in line['spans'])
                            self.assertEqual(notice, f'© 2004–{date.today().year} Test Press. All rights reserved.')
                            box = fitz.Rect(line['bbox'])
                            self.assertGreater(box.y0, page.rect.height - 60)
                            self.assertLess(abs((box.x0 + box.x1) / 2 - page.rect.width / 2), 2)
                        if skill in ('deep', 'folio', 'phd-ivy-monograph', 'print'):
                            self.assertTrue(any(p.get_links() for p in doc))
                        if skill in ('deep', 'folio', 'phd-ivy-monograph'):
                            extracted = ''.join(p.get_text() for p in doc)
                            self.assertIn('E = mc²', extracted)
                            self.assertIn('Measured energy', extracted)
                            self.assertIn('Fixture source note.', extracted)
                            note_pages = [p for p in doc if 'Fixture source note.' in p.get_text()]
                            citation_pages = [p for p in doc if 'Evidence citation 1.' in ' '.join(p.get_text().split())]
                            self.assertEqual(len(citation_pages), 1)
                            self.assertIn('Fixture source note.', citation_pages[0].get_text())
                            if skill == 'deep':
                                self.assertEqual(len(note_pages), 1)

if __name__ == '__main__':
    unittest.main()
