import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import fitz
from reportlab.pdfgen import canvas

ROOT=Path(__file__).resolve().parents[1]


def load(skill,script):
    path=ROOT/'skills'/skill/'scripts'/script
    spec=importlib.util.spec_from_file_location(script.removesuffix('.py'),path)
    result=importlib.util.module_from_spec(spec);spec.loader.exec_module(result);return result


class FooterLinkTests(unittest.TestCase):
    def test_repeat_stamp_keeps_single_notice_and_brand(self):
        stamp=load('copyright','stamp_copyright.py')
        with tempfile.TemporaryDirectory() as tmp:
            source=Path(tmp)/'source.pdf';first=Path(tmp)/'first.pdf';second=Path(tmp)/'second.pdf'
            c=canvas.Canvas(str(source));c.drawString(60,700,'Original preserved body');c.showPage();c.drawString(60,700,'Second page');c.save()
            for a,b in ((source,first),(first,second)):
                stamp.stamp(a,b,2012,stamp.DEFAULT_OWNER,stamp.DEFAULT_LEGAL)
                with fitz.open(b) as doc:
                    for page in doc:
                        text=page.get_text()
                        self.assertEqual(text.count('All rights reserved.'),1)
                        self.assertEqual(text.count('Digital Marketing Co.'),1)
                        self.assertEqual(text.count('Web Development, Inc.'),1)
                        links=page.get_links()
                        self.assertEqual(sum(x.get('uri')=='https://WebDevelopment.tv' for x in links),2)
                        self.assertEqual(sum(x.get('uri')=='https://DigitalMarketingCo.org' for x in links),1)
                    self.assertIn('Original preserved body',doc[0].get_text())

    def test_owner_javascript_escaping(self):
        stamp=load('copyright','stamp_copyright.py')
        self.assertIn(json.dumps('A "Quoted" Owner'),stamp.open_js(2012,'A "Quoted" Owner'))

    def test_legacy_migration_preserves_following_sections(self):
        migration=load('copyright','append_prompt_appendix.py')
        original='# Fixture\n\n## House copyright footer\n\nOld duplicate notice\n\n## Important content\n\nRetain this paragraph.\n'
        revised=migration.strip_old_footer(original)
        self.assertIn('Retain this paragraph.',revised)
        self.assertNotIn('Old duplicate notice',revised)
        self.assertEqual(migration.strip_old_footer(revised),revised)

    def test_proposed_links_are_not_availability_claims(self):
        blink=load('blink','blink.py')
        self.assertEqual(blink.destination('example.org/article'),'https://example.org/article')
        self.assertTrue(all(x['status']=='UNVERIFIED' for x in blink.candidates('https://example.org/article')))
        for invalid in ('file:///etc/passwd','https://user:pass@example.org','https://example.org\n'):
            with self.assertRaises(ValueError):blink.destination(invalid)

    def test_bitly_response_destination_and_keyword(self):
        blink=load('blink','blink.py')
        response=io.BytesIO(json.dumps({'long_url':'https://example.org','link':'https://bit.ly/test'}).encode())
        with patch.object(blink,'urlopen',return_value=response) as request:
            result=blink.create('https://example.org','test','secret-fixture','group-fixture')
            self.assertEqual(result['status'],'CREATED')
            self.assertEqual(result['redirect_status'],'NOT TESTED')
            sent=request.call_args.args[0]
            self.assertEqual(sent.method,'POST')
            self.assertEqual(json.loads(sent.data)['keyword'],'test')
        bad=io.BytesIO(json.dumps({'long_url':'https://other.org','link':'https://bit.ly/test'}).encode())
        with patch.object(blink,'urlopen',return_value=bad):
            with self.assertRaises(ValueError):blink.create('https://example.org','test','secret','group')

    def test_blocklist_token_and_phrase_boundaries(self):
        negative=load('negative','sweep_negative.py')
        with patch.object(negative,'terms_from_file',return_value=['realm','deep dive','cutting-edge']):
            self.assertEqual(negative.find_hits('realms deep diver cutting-edgeless'),[])
            self.assertEqual(len(negative.find_hits('realm deep\n dive cutting-edge')),3)


if __name__=='__main__':unittest.main()
