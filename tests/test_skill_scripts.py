"""Small offline forward fixtures for deterministic skill utilities."""
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SKILLS = Path(__file__).resolve().parents[1] / 'skills'

def load(skill, script):
    path = SKILLS / skill / 'scripts' / (script + '.py')
    name = skill.replace('-', '_') + '_' + script
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

class ForwardFixtures(unittest.TestCase):
    def test_format_self_test_and_whitespace(self):
        mod = load('format', 'format_case')
        self.assertEqual(mod.self_test(), 0)
        self.assertEqual(mod.transform_text('  hELLO\nworld!', 'pc'), '  Hello\nWorld!')

    def test_base22_and_locked_operator(self):
        mod = load('q-base22', 'q_encode')
        for value in (0, 1, 21, 22, 484, 999):
            self.assertEqual(int(mod.to_base22(value), 22), value)
        self.assertIn(('furthermore_concat', 815, 'HO'), mod.furthermore_pair(3, 5))

    def test_decode_small_corpus_strict_json(self):
        mod = load('decode', 'decode_analyze')
        for text in ('', 'Hello', 'red blue red blue'):
            result = mod.analyze(text)
            json.dumps(result, allow_nan=False)
            self.assertEqual(result['n_tokens'], len(mod.tokenize(text)))

    def test_coffee_append_budget_and_subject(self):
        mod = load('coffee', 'parse_coffee_request')
        result = mod.parse_request('/coffee Route 66 travel 8 pages')
        self.assertEqual((result['subject'], result['page_count']), ('Route 66 travel', 8))
        result = mod.parse_request('/coffee more', {'subject':'Trees', 'mode':'square', 'pages':[{},{}]})
        self.assertEqual((result['append'], result['page_count'], result['mode']), (True, 26, 'square'))

    def test_image_slot_anchors_cover_long_paragraph_and_short_slot(self):
        mod = load('images', 'plan_image_slots')
        for count, slots in ((350,1),(1200,2)):
            result = mod.plan_section({'title':'Forest', 'paragraphs':['intro','context',' '.join(['tree']*count)]})
            self.assertEqual(result['slots'], slots)
            self.assertEqual(len(result['anchors']), slots)

    def test_banner_resolves_repository_images(self):
        self.assertEqual(load('banner', 'rebuild_document').resolve_images(), SKILLS / 'images')

    def test_rebuild_monograph_output_forwarding(self):
        mod = load('images', 'rebuild_document')
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root/'monograph.json').write_text('{}')
            with patch.object(sys, 'argv', ['rebuild', str(root), '--out', str(root/'final.pdf')]), patch.object(mod, 'run') as run:
                mod.main()
            command = run.call_args.args[0]
            self.assertTrue(command[1].endswith('build_monograph_pdf.py'))
            self.assertEqual(command[-2:], ['--out', str(root/'final.pdf')])

    def test_stamp_relative_paths_and_override(self):
        from pypdf import PdfWriter, PdfReader
        from PIL import Image
        mod = load('images', 'stamp_images_into_pdf')
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            writer = PdfWriter(); writer.add_blank_page(612,792)
            writer.write(root/'source.pdf')
            Image.new('RGB',(160,90),'green').save(root/'still.png')
            manifest = root/'stamp.json'
            manifest.write_text(json.dumps({'source_pdf':'source.pdf','output_pdf':'result.pdf','items':[{'path':'still.png','after_page':1}]}))
            self.assertEqual(mod.stamp(manifest), root/'result.pdf')
            self.assertEqual(len(PdfReader(root/'result.pdf').pages), 2)
            self.assertEqual(mod.stamp(manifest, root/'override.pdf'), root/'override.pdf')

    def test_image_fit_and_banner_alpha(self):
        from PIL import Image
        mod = load('images', 'fit_full_bleed')
        self.assertEqual(mod.upscale_to_width(Image.new('RGB',(80,40)),160).size,(160,80))
        self.assertEqual(mod.upscale_to_width(Image.new('RGB',(80,40)),40).size,(80,40))
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); Image.new('RGB',(80,40),'blue').save(root/'in.png')
            load('banner','apply_tb_alpha_blend').apply_tb_blend(root/'in.png',root/'out.png',target_w=80)
            with Image.open(root/'out.png') as image:
                self.assertEqual(image.getpixel((0,0))[3],0)
                self.assertEqual(image.getpixel((0,20))[3],255)

    def test_coffee_cover_crop(self):
        from PIL import Image
        image = load('coffee','fit_still').cover_crop(Image.new('RGBA',(40,80),(20,30,40,255)),80,60)
        self.assertEqual((image.size,image.mode),((80,60),'RGB'))

    def test_textbook_contrast(self):
        mod = load('textbook','contrast')
        self.assertAlmostEqual(mod.ratio(mod.rgb('#FFFFFF'),mod.rgb('#000000')),21)
        self.assertFalse(mod.evaluate(['#FFFFFF'], ['#000000'],7,alpha=0)['pass'])

    def test_transcript_lock_rejects_mutation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            for name in ('raw.txt','raw.lock.txt'): (root/name).write_text('Exact source\n')
            command=[sys.executable,str(SKILLS/'transcribe/scripts/qa_transcript.py'),tmp]
            self.assertEqual(subprocess.run(command,capture_output=True).returncode,0)
            (root/'raw.txt').write_text('Edited source\n')
            self.assertNotEqual(subprocess.run(command,capture_output=True).returncode,0)

    def test_citation_remap_preserves_bibliography_links(self):
        mod=load('wca-ivy-biblio','reorder_citations')
        data={'sections':[{'paragraphs':['Forest {{9, 3}} then {{9}}']}], 'notes':[{'n':3,'text':'A','biblio':0},{'n':9,'text':'B','biblio':1}], 'bibliography':['A','B']}
        self.assertEqual(mod.reorder(data),{9:1,3:2})
        self.assertEqual(data['bibliography'],['B','A'])
        self.assertEqual([n['biblio'] for n in data['notes']],[0,1])

    def test_7z_pack_scopes_archive_to_payload(self):
        mod=load('compression','compress')
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);tree=root/'payload';tree.mkdir()
            with patch.object(mod,'which',return_value='/usr/bin/7z'), patch.object(mod.subprocess,'run') as run:
                mod.pack(tree,root/'result.7z','7z','maximum')
            self.assertEqual(run.call_count,1)
            self.assertEqual(run.call_args.kwargs['cwd'],tree)
            self.assertEqual(run.call_args.args[0][-1],'.')
            self.assertTrue(run.call_args.kwargs['check'])

    def test_compression_twice_same_second_bit_exact(self):
        mod=load('compression','compress')
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); source=root/'source.txt';source.write_bytes(b'forest\n'*20)
            for index in range(2):
                out=root/str(index)
                with patch.object(sys,'argv',['compress','--input',str(source),'--out',str(out),'--profile','bit-exact']):
                    self.assertEqual(mod.main(),0)
                self.assertEqual((out/'payload/source.txt').read_bytes(),source.read_bytes())

if __name__ == '__main__': unittest.main()
