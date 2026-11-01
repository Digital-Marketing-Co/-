#!/usr/bin/env python3
"""Integration fixtures generated locally; no paid or network services."""
import argparse
import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from schemata import pipeline,strict,Vocabulary,merge,opaque,digest
from extractors import extract

def run(inputs,out,annotations=None,**kw):
    args=dict(output=str(out),inputs=[str(p) for p in inputs],canonical_map=None,language=None,annotations=str(annotations) if annotations else None,validate_only=None,offline=True,scope='corpus')
    args.update(kw);return pipeline(argparse.Namespace(**args))

class Integration(unittest.TestCase):
    def setUp(self):
        self.t=tempfile.TemporaryDirectory();self.p=Path(self.t.name)
    def tearDown(self):self.t.cleanup()
    def source(self,name,text):
        p=self.p/name;p.write_text(text);return p
    def test_formats_and_source_preservation(self):
        import fitz
        from docx import Document
        from openpyxl import Workbook
        from pptx import Presentation
        from pptx.util import Inches
        files=[]
        files.append(self.source('book.md','# Book\n\n## Chapter One\nStory.\n## Chapter Two\nEnd.'))
        files.append(self.source('article.html','<html><h1>Study</h1><p>References: W3C</p><table><tr><td>0</td></tr></table></html>'))
        files.append(self.source('data.json','{"zero":0,"flag":false}'))
        d=Document();d.add_heading('Study',0);d.add_paragraph('Reference to W3C.');d.add_table(rows=1,cols=1).cell(0,0).text='Value';p=self.p/'a.docx';d.save(p);files.append(p)
        w=Workbook();w.active['A1']=0;w.active['B1']='=1+1';p=self.p/'a.xlsx';w.save(p);files.append(p)
        pr=Presentation();s=pr.slides.add_slide(pr.slide_layouts[6]);s.shapes.add_textbox(Inches(1), Inches(1), Inches(2), Inches(1)).text='Slide content';p=self.p/'a.pptx';pr.save(p);files.append(p)
        pdf=fitz.open();pdf.new_page().insert_text((50,50),'Scholarly article, cited work.');p=self.p/'a.pdf';pdf.save(p);pdf.close();files.append(p)
        p=self.p/'book.epub'
        with zipfile.ZipFile(p,'w') as z:
            z.writestr('META-INF/container.xml','<container><rootfiles><rootfile full-path="book.opf"/></rootfiles></container>')
            z.writestr('book.opf','<package xmlns="http://www.idpf.org/2007/opf"><manifest><item id="one" href="one.xhtml"/><item id="two" href="two.xhtml"/></manifest><spine><itemref idref="two"/><itemref idref="one"/></spine></package>')
            z.writestr('one.xhtml','<html><h1>One</h1></html>');z.writestr('two.xhtml','<html><h1>Two</h1></html>')
        files.append(p)
        before={str(p):digest(p.read_bytes()) for p in files}
        for p in files:
            r=extract(p);self.assertTrue(r['records'],(p,r));self.assertIn('locator',r['records'][0])
        self.assertEqual(extract(p)['records'][0]['text'],'Two')
        out=self.p/'out';self.assertEqual(run(files,out),0)
        self.assertEqual(before,{str(p):digest(p.read_bytes()) for p in files})
        self.assertEqual(len(strict((out/'manifest.json').read_text())),8)
    def test_unsafe_script_and_roundtrip(self):
        p=self.source('unsafe.md','# Hostile text\n</script><script>alert(1)</script>')
        out=self.p/'out';run([p],out)
        records=strict((out/'records.json').read_text());r=records[-1]
        a=self.p/'a.json';a.write_text(json.dumps({'claims':[{'subject':r['document_id'],'predicate':'description','value':r['text'],'record_id':r['id'],'quote':r['text'],'rationale':'Description quotes text for test','status':'accepted','explicit':True}], 'coverage':{x['id']:{'status':'mapped','rationale':'Reviewed'} for x in records},'review_rounds':2}))
        run([p],out,a)
        html=(out/'corpus-jsonld.html').read_text();self.assertEqual(html.count('</script>'),1)
        g=strict((out/'corpus.jsonld').read_text());self.assertEqual(strict(html.split('>',1)[1].rsplit('</script>',1)[0]),g)
        self.assertEqual(Vocabulary().canonical(g),Vocabulary().canonical(strict((out/'corpus.min.jsonld').read_text())))
        self.assertTrue(strict((out/'validation.json').read_text())['semantic_review_complete'])
    def test_conflicts_and_distinct_names(self):
        a,b=opaque('person-a'),opaque('person-b');shared=opaque('org')
        nodes,conflicts=merge([{'@id':a},{'@id':b},{'@id':shared}],[{'subject':s,'predicate':p,'value':v} for s,p,v in [(a,'name','Alex'),(b,'name','Alex'),(shared,'name','Org'),(shared,'datePublished','2020-01-01'),(shared,'datePublished','2021-01-01')]])
        self.assertEqual(len(nodes),3);self.assertEqual(len(conflicts),1);self.assertNotIn('datePublished',nodes[-1])
    def test_incremental_and_duplicates(self):
        p=self.source('a.md','# A\nFirst');q=self.source('b.md','# A\nFirst');out=self.p/'out'
        run([p,q],out);m=strict((out/'manifest.json').read_text());ident=m[0]['document_id'];self.assertEqual(m[1]['duplicate_of'],ident)
        run([p,q],out);self.assertTrue(strict((out/'manifest.json').read_text())[0]['cached'])
        p.write_text('# A\nChanged');run([p,q],out);m=strict((out/'manifest.json').read_text());self.assertEqual(m[0]['document_id'],ident);self.assertFalse(m[0]['cached']);self.assertTrue(m[1]['cached'])
    def test_failures_scan_and_existing_data(self):
        import fitz
        p=self.p/'scan.pdf';d=fitz.open();d.new_page();d.save(p);d.close();self.assertFalse(extract(p)['complete'])
        binary=self.p/'bad.png';binary.write_bytes(b'\x89PNG\0');self.assertFalse(extract(binary)['complete'])
        malformed=self.source('broken.html','<html><h1>Page</h1><script type="application/ld+json">{bad</script></html>')
        out=self.p/'out';run([p,binary,malformed,self.p/'missing'],out)
        r=strict((out/'validation.json').read_text());self.assertFalse(r['extraction_complete']);self.assertTrue(r['existing_data_warnings'])
    def test_no_fictional_offer_in_baseline(self):
        p=self.source('fiction.md','# Fiction\nAn imagined organization offers moon insurance at $50.');out=self.p/'out';run([p],out)
        g=(out/'corpus.jsonld').read_text();self.assertNotIn('Offer',g);self.assertNotIn('price',g);self.assertNotIn('Organization',g)
    def test_bad_evidence_rejected(self):
        p=self.source('a.txt','Actual sentence');out=self.p/'out';run([p],out);r=strict((out/'records.json').read_text())[0]
        a=self.p/'a.json';a.write_text(json.dumps({'claims':[{'subject':r['document_id'],'predicate':'name','value':'Invented','record_id':r['id'],'quote':'Absent','rationale':'x','status':'accepted'}]}))
        with self.assertRaises(ValueError):run([p],out,a)
    def test_blocked_context_unknown_and_shapes(self):
        v=Vocabulary()
        with self.assertRaises(ValueError):v.loader('http://127.0.0.1/private')
        with self.assertRaises(ValueError):v.check(['CreativeWork'],'imaginarySchemaProperty','x')
        with self.assertRaises(ValueError):v.check(['CreativeWork'],'datePublished','Yesterday')
        with self.assertRaises(ValueError):strict('{"x":1,"x":2}')
        with self.assertRaises(ValueError):strict('{"x":NaN}')
    def test_shared_verified_entity(self):
        a=self.source('a.txt','Research Institute is a named organization.');b=self.source('b.txt','Research Institute is a named organization. More text.');out=self.p/'out';run([a,b],out)
        records=strict((out/'records.json').read_text());entity=opaque('verified-shared-org');claims=[]
        for r in records:
            for sub,pred,val in [(entity,'@type','Organization'),(entity,'name','Research Institute'),(r['document_id'],'mentions',{'@id':entity})]:
                claims.append(dict(subject=sub,predicate=pred,value=val,record_id=r['id'],quote=r['text'],rationale='Verified shared identifier in fixture',status='accepted'))
        anno=self.p/'a.json';anno.write_text(json.dumps({'claims':claims,'coverage':{r['id']:{'status':'mapped'} for r in records},'review_rounds':2}));run([a,b],out,anno)
        nodes=strict((out/'corpus.jsonld').read_text())['@graph'];self.assertEqual(sum(n['@id']==entity for n in nodes),1)

if __name__=='__main__':unittest.main(verbosity=2)
