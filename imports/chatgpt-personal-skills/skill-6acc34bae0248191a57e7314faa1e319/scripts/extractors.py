"""Read-only document extraction adapters. Document content is never executed.

Public interface: extract(path) returns source-independent extraction records.
Adapter errors are reported in limitations; incomplete extraction is never success.
"""
from __future__ import annotations
import importlib.metadata
import json
import mimetypes
import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

VERSION = '1.0.0'
MAX_MEMBER_BYTES = 64 * 1024 * 1024
MAX_ARCHIVE_BYTES = 512 * 1024 * 1024
W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'

def _version(package):
    try: return importlib.metadata.version(package)
    except importlib.metadata.PackageNotFoundError: return VERSION

def _result(mime, adapter, version=VERSION):
    return dict(mime=mime, adapter=adapter, adapter_version=version, complete=True,
                limitations=[], metadata={}, existing_jsonld=[], records=[])

def _record(out, kind, text, locator, parent=None):
    if not text or not text.strip(): return
    row = dict(kind=kind, text=text, locator=locator, ordinal=len(out['records']))
    if parent is not None: row['parent'] = parent
    out['records'].append(row)

def _limit(out, text):
    out['complete'] = False
    out['limitations'].append(text)

def _read_member(z, name):
    info = z.getinfo(name)
    if info.file_size > MAX_MEMBER_BYTES: raise ValueError('Archive member exceeds extraction size limit')
    return z.read(name)

def _xml(z, name):
    data = _read_member(z, name)
    if b'<!DOCTYPE' in data.upper() or b'<!ENTITY' in data.upper():
        raise ValueError('Unsafe XML entity declarations rejected')
    return ET.fromstring(data)

def _zip_kind(path):
    with zipfile.ZipFile(path) as z:
        if sum(i.file_size for i in z.infolist()) > MAX_ARCHIVE_BYTES:
            raise ValueError('Archive exceeds extraction size limit')
        names=set(z.namelist())
        if 'word/document.xml' in names: return 'docx'
        if 'xl/workbook.xml' in names: return 'xlsx'
        if 'ppt/presentation.xml' in names: return 'pptx'
        if 'META-INF/container.xml' in names: return 'epub'
    return 'zip'

def _html_content(out, text, prefix=None):
    from bs4 import BeautifulSoup
    soup=BeautifulSoup(text,'html.parser')
    if soup.title and soup.title.get_text(strip=True):
        out['metadata'].setdefault('title',soup.title.get_text(strip=True))
    hidden=[]
    for tag in soup.find_all('meta'):
        hidden.append({k:tag.get(k) for k in ('name','property','content','http-equiv') if tag.get(k)})
    if hidden: out['metadata'].setdefault('html_meta',[]).extend(hidden)
    for script in soup.find_all('script'):
        if (script.get('type') or '').lower().split(';')[0].strip() == 'application/ld+json':
            raw=script.string or script.get_text()
            try: out['existing_jsonld'].append({'data':json.loads(raw), 'locator':{'element_id':script.get('id'), **(prefix or {})}})
            except (ValueError,TypeError) as e:
                out['existing_jsonld'].append({'raw':raw,'error':str(e),'locator':prefix or {}})
                out['limitations'].append('Malformed existing JSON-LD retained for review')
        script.decompose()
    for tag in soup.find_all(['style','noscript','template']): tag.decompose()
    root=soup.body or soup
    candidates=root.find_all(re.compile(r'^(h[1-6]|p|li|table|caption|figcaption|img|blockquote|pre|dt|dd)$'))
    used_text=[]
    for index,tag in enumerate(candidates):
        if tag.find_parent(['table','li','blockquote','pre','p']): continue
        loc={'selector': f'{tag.name}:source-ordinal({index})', **(prefix or {})}
        # source-ordinal is a locator descriptor, not a claimed CSS selector.
        loc.pop('selector'); loc['html_tag']=tag.name; loc['element_ordinal']=index
        if tag.get('id'): loc['anchor']=tag['id']
        if tag.name == 'table':
            caption=tag.find('caption')
            if caption: _record(out,'caption',caption.get_text(' ',strip=True),loc)
            for r,row in enumerate(tag.find_all('tr')):
                for c,cell in enumerate(row.find_all(['td','th'],recursive=False)):
                    _record(out,'table_cell',cell.get_text(' ',strip=True),dict(loc,row=r,column=c,rowspan=cell.get('rowspan','1'),colspan=cell.get('colspan','1')))
        elif tag.name == 'img':
            _record(out,'image_description',tag.get('alt',''),loc)
            if not tag.get('alt'): out['limitations'].append('Image has no available alternative description')
        else:
            kind='heading' if re.match(r'h[1-6]',tag.name) else {'li':'list_item','figcaption':'caption','dt':'defined_term','dd':'definition','pre':'code'}.get(tag.name,'paragraph')
            _record(out,kind,tag.get_text(' ',strip=True),loc)
        used_text.append(tag)
    # Capture text outside semantic block elements instead of dropping div-only pages.
    for index,node in enumerate(root.find_all(string=True)):
        if node.find_parent(re.compile(r'^(h[1-6]|p|li|table|caption|figcaption|blockquote|pre|dt|dd)$')): continue
        if str(node).strip(): _record(out,'text',str(node).strip(),{'text_node_ordinal':index,**(prefix or {})})

def _pdf(path):
    import fitz
    out=_result('application/pdf','pymupdf',_version('PyMuPDF'))
    with fitz.open(path) as doc:
        if doc.needs_pass:
            _limit(out,'Encrypted PDF requires a password'); return out
        out['metadata']={k:v for k,v in doc.metadata.items() if v}
        out['metadata']['page_count']=len(doc)
        for p,page in enumerate(doc):
            blocks=page.get_text('blocks',sort=True)
            available=False
            for block in blocks:
                if len(block)>6 and block[6] != 0: continue
                if str(block[4]).strip():
                    available=True
                    _record(out,'paragraph',block[4],{'page':p+1,'bbox':list(block[:4]),'block':block[5]})
            if not available: _limit(out,f'Page {p+1} has no extractable text; OCR not configured')
            elif page.get_images():
                out['limitations'].append(f'Page {p+1}: image text/descriptions are not available without OCR or supplied alternatives')
                out['complete']=False
    out['limitations'].append('PDF blocks retain geometry; table cells and heading roles require downstream review')
    return out

def _docx(path):
    out=_result('application/vnd.openxmlformats-officedocument.wordprocessingml.document','ooxml-xml')
    with zipfile.ZipFile(path) as z:
        names=set(z.namelist())
        if 'docProps/core.xml' in names:
            out['metadata']={e.tag.split('}')[-1]:e.text for e in _xml(z,'docProps/core.xml') if e.text}
        def body_records(root,part):
            # XML document order captures paragraphs and table cell relationships.
            for idx,element in enumerate(root.iter()):
                if element.tag != W+'p': continue
                text=''.join((e.text or '') if e.tag==W+'t' else '\t' if e.tag==W+'tab' else '\n' if e.tag==W+'br' else '' for e in element.iter())
                style=element.find('./'+W+'pPr/'+W+'pStyle')
                kind='heading' if style is not None and 'heading' in style.get(W+'val','').lower() else 'paragraph'
                loc={'part':part,'paragraph_xml_ordinal':idx}
                # identify ancestor table coordinates using root traversal
                for ti,table in enumerate(root.iter(W+'tbl')):
                    for ri,row in enumerate(table.findall(W+'tr')):
                        for ci,cell in enumerate(row.findall(W+'tc')):
                            if any(p is element for p in cell.iter(W+'p')):
                                kind='table_cell'; loc.update(table=ti,row=ri,column=ci)
                _record(out,kind,text,loc)
        body_records(_xml(z,'word/document.xml'),'body')
        for name in sorted(names):
            if re.match(r'word/(footnotes|endnotes|comments|header\d*|footer\d*)\.xml$',name):
                body_records(_xml(z,name),name)
        if any(n.startswith('word/media/') for n in names): _limit(out,'Embedded images require supplied descriptions or visual review')
        if 'word/vbaProject.bin' in names: out['limitations'].append('Macros ignored and never executed')
        for name in names:
            if name.startswith('word/') and name.endswith('.xml'):
                root=_xml(z,name)
                for e in root.iter():
                    if e.tag.split('}')[-1]=='docPr' and e.get('descr'):
                        _record(out,'image_description',e.get('descr'),{'part':name,'drawing_id':e.get('id')})
    return out

def _xlsx(path):
    import openpyxl
    out=_result('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet','openpyxl',_version('openpyxl'))
    book=openpyxl.load_workbook(path,read_only=False,data_only=False,keep_links=False)
    try:
        out['metadata']={'title':book.properties.title,'creator':book.properties.creator}
        out['metadata']={k:v for k,v in out['metadata'].items() if v}
        for sheet in book:
            for row in sheet.iter_rows():
                for cell in row:
                    if cell.value is None: continue
                    loc={'sheet':sheet.title,'cell':cell.coordinate,'row':cell.row,'column':cell.column,'sheet_state':sheet.sheet_state}
                    _record(out,'formula' if cell.data_type=='f' else 'table_cell',str(cell.value),loc)
                    if cell.comment: _record(out,'comment',cell.comment.text,loc)
            if sheet._images or sheet._charts: _limit(out,f'Sheet {sheet.title}: embedded charts/images require visual review')
    finally: book.close()
    return out

def _pptx(path):
    from pptx import Presentation
    out=_result('application/vnd.openxmlformats-officedocument.presentationml.presentation','python-pptx',_version('python-pptx'))
    pres=Presentation(path)
    for s,slide in enumerate(pres.slides):
        for i,shape in enumerate(slide.shapes):
            loc={'slide':s+1,'shape':i,'bbox_emu':[shape.left,shape.top,shape.width,shape.height]}
            if shape.has_table:
                for r,row in enumerate(shape.table.rows):
                    for c,cell in enumerate(row.cells): _record(out,'table_cell',cell.text,dict(loc,row=r,column=c))
            elif shape.has_text_frame:
                for p,paragraph in enumerate(shape.text_frame.paragraphs): _record(out,'paragraph',paragraph.text,dict(loc,paragraph=p))
            elif shape.shape_type==13: _limit(out,f'Slide {s+1}: image requires alternative description or visual review')
            else: out['limitations'].append(f'Slide {s+1}: non-text shape {i} retained only as a limitation')
        if slide.has_notes_slide:
            for p,paragraph in enumerate(slide.notes_slide.notes_text_frame.paragraphs): _record(out,'speaker_note',paragraph.text,{'slide':s+1,'notes_paragraph':p})
    return out

def _epub(path):
    import posixpath
    out=_result('application/epub+zip','epub-xml-bs4',_version('beautifulsoup4'))
    with zipfile.ZipFile(path) as z:
        container=_xml(z,'META-INF/container.xml')
        package=next(e.get('full-path') for e in container.iter() if e.tag.endswith('rootfile'))
        opf=_xml(z,package); base=posixpath.dirname(package)
        manifest={e.get('id'):e.get('href') for e in opf.iter() if e.tag.endswith('}item')}
        out['metadata']={e.tag.split('}')[-1]:e.text for e in opf.iter() if e.tag.startswith('{http://purl.org/dc/elements/1.1/') and e.text}
        for order,e in enumerate(x for x in opf.iter() if x.tag.endswith('}itemref')):
            member=posixpath.normpath(posixpath.join(base,manifest[e.get('idref')].split('#')[0]))
            _html_content(out,_read_member(z,member).decode('utf-8'),{'spine_ordinal':order,'epub_member':member})
        if 'META-INF/encryption.xml' in z.namelist(): _limit(out,'EPUB contains encryption metadata; encrypted resources may be unreadable')
    return out

def _text(path,kind):
    text=path.read_bytes().decode('utf-8-sig')
    out=_result('text/markdown' if kind=='markdown' else 'text/plain','utf8-text')
    offset=0
    for line in text.splitlines(keepends=True):
        value=line.rstrip('\r\n')
        role='heading' if kind=='markdown' and re.match(r'^#{1,6}\s',value) else 'list_item' if re.match(r'^\s*(?:[-*+] |\d+[.)] )',value) else 'paragraph'
        _record(out,role,value,{'char_start':offset,'char_end':offset+len(value)})
        offset+=len(line)
    return out

def extract(path):
    """Extract readable content without modifying sources or executing embeddings."""
    path=Path(path)
    out=_result('application/octet-stream','unsupported')
    try:
        if not path.is_file(): raise OSError('Input is inaccessible or not a regular file')
        with path.open('rb') as stream: head=stream.read(4096)
        if head.startswith(b'%PDF-'): return _pdf(path)
        if head.startswith(b'PK\x03\x04'):
            kind=_zip_kind(path)
            adapters={'docx':_docx,'xlsx':_xlsx,'pptx':_pptx,'epub':_epub}
            if kind in adapters: return adapters[kind](path)
            _limit(out,'ZIP container has no verified supported document format'); return out
        stripped=head.lstrip(b'\xef\xbb\xbf \t\r\n')
        if re.search(br'<(?:!doctype\s+html|html|head|body)\b',stripped,re.I) or path.suffix.lower() in ('.html','.htm','.xhtml'):
            out=_result('text/html','beautifulsoup4',_version('beautifulsoup4'))
            _html_content(out,path.read_bytes().decode('utf-8-sig')); return out
        if path.suffix.lower()=='.json' or (path.suffix.lower() not in ('.md','.markdown','.txt') and stripped[:1] in (b'{',b'[')):
            out=_result('application/json','stdlib-json')
            data=json.loads(path.read_bytes().decode('utf-8-sig'))
            if isinstance(data,dict) and ('@context' in data or '@graph' in data): out['existing_jsonld'].append({'data':data,'locator':{'json_pointer':''}})
            def walk(value,pointer=''):
                if isinstance(value,dict):
                    for key,item in value.items(): walk(item,pointer+'/'+str(key).replace('~','~0').replace('/','~1'))
                elif isinstance(value,list):
                    for i,item in enumerate(value): walk(item,pointer+'/'+str(i))
                else: _record(out,'data_value',json.dumps(value,ensure_ascii=False),{'json_pointer':pointer})
            walk(data); return out
        # Explicit known binary signatures cannot masquerade as text.
        if b'\x00' in head or head.startswith((b'\xd0\xcf\x11\xe0',b'\x89PNG',b'GIF8',b'\xff\xd8')):
            _limit(out,'Unsupported binary format; no verified extraction adapter'); return out
        return _text(path,'markdown' if path.suffix.lower() in ('.md','.markdown') else 'text')
    except Exception as exc:
        _limit(out,f'{type(exc).__name__}: {exc}')
        return out
