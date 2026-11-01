#!/usr/bin/env python3
"""Read-only PDF/DOCX content audit. Requires PyMuPDF and python-docx.
Comparison reports evidence; PDF reflow/headers may differ from DOCX.
"""
import argparse, hashlib, json, re, sys
from pathlib import Path

def norm(s): return re.sub(r'\s+', ' ', s).strip()
def digest(s): return hashlib.sha256(s.encode('utf-8')).hexdigest()
def extract(path):
    ext=Path(path).suffix.lower()
    if ext=='.pdf':
        import fitz
        d=fitz.open(path)
        pages=[p.get_text(sort=True) for p in d]
        headings=[]
        for p in d:
            blocks=p.get_text('dict')['blocks']
            for b in blocks:
                if 'lines' not in b: continue
                for line in b['lines']:
                    spans=line.get('spans',[])
                    s=norm(''.join(x['text'] for x in spans))
                    if s and len(s)<160 and any(x['size']>=15 for x in spans): headings.append(s)
        return {'type':'pdf','pages':len(pages),'text': '\n'.join(pages),'headings':headings,'page_chars':[len(x.strip()) for x in pages]}
    if ext=='.docx':
        from docx import Document
        d=Document(path)
        paras=[p.text for p in d.paragraphs]
        cells=[]
        for table in d.tables:
            for row in table.rows:
                cells.extend(c.text for c in row.cells)
        headers=[]
        for sec in d.sections:
            headers.extend(p.text for p in sec.header.paragraphs)
            headers.extend(p.text for p in sec.footer.paragraphs)
        return {'type':'docx','pages':None,'text':'\n'.join(paras+cells+headers),'headings':[norm(p.text) for p in d.paragraphs if p.style.name.startswith('Heading') and norm(p.text)],'tables':len(d.tables),'paragraphs':len(paras)}
    raise ValueError('Supported: PDF, DOCX')

def audit(source,output):
    a=extract(source);b=extract(output)
    sa=norm(a['text']);sb=norm(b['text']); issues=[]
    if not sa:issues.append('SOURCE_EMPTY')
    if not sb:issues.append('OUTPUT_EMPTY')
    if sa and sb and len(sb)<len(sa)*0.75:issues.append('MAJOR_TEXT_SHRINKAGE')
    src_words=re.findall(r'\w+',sa.casefold());out_words=re.findall(r'\w+',sb.casefold())
    for position,chunk in [('opening',src_words[:35]),('ending',src_words[-35:])]:
        if len(chunk)>=10 and ' '.join(chunk) not in ' '.join(out_words):issues.append('MISSING_'+position.upper()+'_TEXT')
    if a['type']=='docx':
        missing=[h for h in a['headings'] if norm(h).casefold() not in sb.casefold()]
        if missing:issues.append('MISSING_HEADINGS')
    else:missing=[]
    if b['type']=='pdf' and any(c==0 for c in b['page_chars']):issues.append('POSSIBLY_BLANK_PDF_PAGE')
    return {'status':'FAIL' if issues else 'PASS','issues':issues,'source':{'type':a['type'],'characters':len(sa),'sha256':digest(sa),'headings':len(a['headings'])},'output':{'type':b['type'],'characters':len(sb),'sha256':digest(sb),'pages':b.get('pages'),'headings':len(b['headings'])},'missing_headings':missing[:30],'limitations':['Text extraction does not establish visual layout, image fidelity or scientific validity.','Head/tail comparisons may flag legitimate document restructuring and require review.']}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('source');p.add_argument('output');z=p.parse_args()
    try:
        r=audit(z.source,z.output);print(json.dumps(r,indent=2));sys.exit(0 if r['status']=='PASS' else 1)
    except Exception as e:print(json.dumps({'status':'ERROR','message':str(e)}));sys.exit(2)
