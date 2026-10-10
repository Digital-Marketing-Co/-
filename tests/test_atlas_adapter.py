"""Offline schema, adaptation, and actual PDF integration fixtures."""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SKILLS = Path(__file__).resolve().parents[1] / 'skills'
SCRIPT = SKILLS / 'atlas/scripts/atlas_to_deep.py'
spec = importlib.util.spec_from_file_location('atlas_adapter_test', SCRIPT)
adapter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(adapter)


def fixture():
    return {'title':'River Network', 'author':'Fixture Author', 'abstract':'Two supplied stations and their connection.',
            'subtitle':'Offline source fixture', 'date':'2026', 'keywords':['river'],
            'projection':'WGS 84; decimal degrees; supplied fixture coordinates.',
            'sections':[{'id':'method', 'title':'Sources and method', 'paragraphs':['Station evidence {{7}}.']}],
            'nodes':[{'id':'north','name':'North Station','description':'Upstream station.','coordinates':{'latitude':42.0,'longitude':-71.0,'note':7},'notes':[7],'variants':['North Point'],'status':'fixture'},
                     {'id':'south','name':'South Station','description':'Downstream station.'}],
            'edges':[{'source':'north','target':'south','relation':'supplied route'}],
            'gazetteer':[{'id':'north-entry','name':'North Station','period':'2026','description':'Test entry.','notes':[7]}],
            'notes':[{'n':7,'text':'Fixture source, supplied for software validation.', 'biblio':0}],
            'bibliography':[{'text':'Fixture Source. Station Inventory. 2026.','work_id':'fixture'}]}


class AtlasFixtureTests(unittest.TestCase):
    def test_schema_contract_and_invalid_spatial_records(self):
        data=fixture();adapter.validate(data)
        schema=json.loads(adapter.SCHEMA.read_text())
        self.assertEqual(schema['$schema'],'https://json-schema.org/draft/2020-12/schema')
        for mutate in (lambda d:d.pop('title'),lambda d:d['nodes'][0]['coordinates'].update(latitude=95),
                       lambda d:d.pop('projection'),lambda d:d['edges'][0].update(target='absent'),
                       lambda d:d['nodes'][0]['coordinates'].pop('note'),
                       lambda d:d['nodes'][0]['coordinates'].update(longitude=float('nan'))):
            invalid=copy.deepcopy(data);mutate(invalid)
            with self.assertRaises(ValueError):adapter.validate(invalid)

    def test_preservation_and_supported_visible_mapping(self):
        original=fixture();snapshot=copy.deepcopy(original)
        result=adapter.adapt(original)
        self.assertEqual(original,snapshot)
        for key in ('title','author','subtitle','notes','nodes','edges','gazetteer'):
            self.assertEqual(result[key],original[key])
        self.assertEqual(result['sections'][0],original['sections'][0])
        self.assertEqual(result['atlas_bibliography'],original['bibliography'])
        self.assertEqual(result['bibliography'],[original['bibliography'][0]['text']])
        visible=' '.join(p for s in result['sections'] for p in s.get('paragraphs',[]) if isinstance(p,str))
        for field in ('North Station','42.0','-71.0','North Point','2026','Source notes: {{7}}','supplied route'):
            self.assertIn(field,visible)
        self.assertEqual([s['kind'] for s in result['sections'][-2:]],['notes','bibliography'])

    def test_conversion_visual_paths_and_source_guard(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);source=root/'atlas.json';data=fixture()
            data['sections'][0]['banner']={'path':'banners/map.png','caption':'Test map'}
            source.write_text(json.dumps(data))
            out=adapter.convert(source,root/'elsewhere/deep.json')
            result=json.loads(out.read_text())
            self.assertEqual(result['sections'][0]['banner']['path'],str(root/'banners/map.png'))
            self.assertEqual(json.loads(source.read_text()),data)
            with self.assertRaises(ValueError):adapter.convert(source,source)

    def test_pdf_fixture_with_supplied_banner(self):
        from PIL import Image
        from pypdf import PdfReader
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);source=root/'atlas.json';data=fixture()
            Image.new('RGB',(640,360),(25,70,105)).save(root/'map.png')
            data['sections'][0]['banner']={'path':'map.png','caption':'Supplied software fixture raster.'}
            source.write_text(json.dumps(data))
            output=root/'2026-river-network-wca-atlas.pdf'
            run=subprocess.run([sys.executable,str(SKILLS/'atlas/scripts/build_atlas_pdf.py'),str(source),'--out',str(output)],capture_output=True,text=True)
            self.assertEqual(run.returncode,0,run.stdout+run.stderr)
            self.assertTrue((root/'deep.json').is_file())
            reader=PdfReader(output)
            text='\n'.join(page.extract_text() or '' for page in reader.pages)
            for expected in ('River Network','North Station','Gazetteer','Fixture Source'):
                self.assertIn(expected,text)
            self.assertGreater(len(reader.pages),1)
            self.assertEqual(sum(len(page.images) for page in reader.pages),1)
            for page in reader.pages:
                self.assertEqual((page.extract_text() or '').count('All rights reserved.'),1)
            # The section heading remains on the page containing its supplied banner.
            banner_pages=[p for p in reader.pages if p.images]
            self.assertEqual(len(banner_pages),1)
            self.assertIn('Sources and method',banner_pages[0].extract_text())

if __name__=='__main__':unittest.main()
