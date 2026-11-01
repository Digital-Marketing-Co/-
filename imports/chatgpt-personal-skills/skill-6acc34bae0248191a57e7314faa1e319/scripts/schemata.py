#!/usr/bin/env python3
"""Evidence-backed document graphs; semantic decisions are supplied by the agent."""
import argparse
import copy
import datetime
import hashlib
import json
import re
import sqlite3
import sys
import unicodedata
import uuid
from pathlib import Path
from urllib.parse import urlparse
from pyld import jsonld
from extractors import extract

ROOT = Path(__file__).resolve().parents[1]
VERSION = '1.0.0'
SCHEMA = 'https://schema.org/'
MULTI = {'@type','hasPart','isPartOf','mentions','about','citation','sameAs','author','publisher','keywords','image','encoding','associatedMedia'}

def strict(text):
    def pairs(items):
        d = {}
        for k,v in items:
            if k in d: raise ValueError('Duplicate JSON key: '+k)
            d[k]=v
        return d
    return json.loads(text, object_pairs_hook=pairs, parse_constant=lambda s: (_ for _ in ()).throw(ValueError(s)))

def digest(value):
    return hashlib.sha256(value if isinstance(value,bytes) else json.dumps(value,sort_keys=True,ensure_ascii=False).encode()).hexdigest()

def save(path, value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2,allow_nan=False)+'\n')

def iri(value):
    return isinstance(value,str) and bool(urlparse(value).scheme) and not re.search(r'\s',value)

def opaque(value):
    return 'urn:uuid:'+str(uuid.uuid5(uuid.NAMESPACE_URL,value))

class Vocabulary:
    def __init__(self):
        self.provenance = strict((ROOT/'references/vocabulary-provenance.json').read_text())
        for name,info in self.provenance.items():
            if digest((ROOT/'references'/name).read_bytes())!=info['sha256']: raise ValueError('Vocabulary cache checksum mismatch')
        data=strict((ROOT/'references/vocabulary.jsonld').read_text())
        self.terms={}
        for n in data['@graph']:
            ident=n.get('@id','')
            if ident.startswith('schema:'): self.terms[ident[7:]]=n
            elif ident.startswith(SCHEMA): self.terms[ident[len(SCHEMA):]]=n
        self.context=strict((ROOT/'references/context.json').read_text())
    def loader(self,url,options=None):
        if url.rstrip('/') not in {'https://schema.org','http://schema.org','https://schema.org/docs/jsonldcontext.json'}:
            raise ValueError('Blocked remote context: '+url)
        return {'contextUrl':None,'documentUrl':url,'document':self.context}
    def opts(self): return {'documentLoader':self.loader,'processingMode':'json-ld-1.1'}
    def canonical(self,g):
        return jsonld.normalize(g,{**self.opts(),'algorithm':'URDNA2015','format':'application/n-quads'})
    def compact(self,g):
        expanded=jsonld.expand(g,self.opts())
        c=jsonld.compact(expanded,'https://schema.org',self.opts())
        if self.canonical(g)!=self.canonical(c): raise ValueError('Compaction changes RDF semantics')
        return c
    def ancestors(self,t):
        seen=set(); stack=[t]
        while stack:
            x=stack.pop()
            if x in seen: continue
            seen.add(x)
            for y in values(self.terms.get(x,{}).get('rdfs:subClassOf',[])):
                if isinstance(y,dict): stack.append(y.get('@id','').split(':')[-1])
        return seen
    def check(self,typ,pred,value):
        term=value if pred=='@type' else pred
        if term not in self.terms: raise ValueError('Unknown Schema.org term: '+str(term))
        definition=self.terms[term]
        if 'schema:supersededBy' in definition: raise ValueError('Superseded term: '+term)
        part=str(definition.get('schema:isPartOf',''))
        if 'pending' in part or 'attic' in part: raise ValueError('Non-stable term: '+term)
        expected='rdfs:Class' if pred=='@type' else 'rdf:Property'
        if expected not in values(definition.get('@type',[])): raise ValueError('Incorrect term kind: '+term)
        if pred in {'datePublished','dateModified'} and not re.fullmatch(r'\d{4}-\d{2}-\d{2}(T.*)?',str(value)): raise ValueError('Invalid date shape')
        if pred in {'url','sameAs'} and not iri(value): raise ValueError('Expected absolute IRI')
        if pred in {'position','numberOfPages','wordCount'} and (isinstance(value,bool) or not isinstance(value,int)): raise ValueError('Expected integer: '+pred)
        warnings=[]
        domain={x.get('@id','').split(':')[-1] for x in values(definition.get('schema:domainIncludes',[])) if isinstance(x,dict)}
        if domain and not any(domain & self.ancestors(t) for t in typ): warnings.append('domainIncludes guidance mismatch: '+pred)
        ranges={x.get('@id','').split(':')[-1] for x in values(definition.get('schema:rangeIncludes',[])) if isinstance(x,dict)}
        if pred!='@type' and isinstance(value,dict) and '@id' not in value and '@value' not in value and '@list' not in value: raise ValueError('Expected JSON-LD value or identified node')
        if ranges and isinstance(value,bool) and 'Boolean' not in ranges: warnings.append('rangeIncludes Boolean mismatch: '+pred)
        if ranges and isinstance(value,(int,float)) and not isinstance(value,bool) and not ranges & {'Number','Integer','Float'}: warnings.append('rangeIncludes numeric mismatch: '+pred)
        return warnings

def values(x): return x if isinstance(x,list) else [x]

def merge(nodes,claims):
    result={n['@id']:{'@id':n['@id']} for n in nodes}; conflicts=[]
    buckets={}
    for c in claims:
        buckets.setdefault((c['subject'],c['predicate']),[]).append(c['value'])
    for (sub,pred),vs in buckets.items():
        unique=[]
        for v in vs:
            if v not in unique: unique.append(v)
        result.setdefault(sub,{'@id':sub})
        if len(unique)>1 and pred not in MULTI:
            conflicts.append({'subject':sub,'predicate':pred,'values':unique}); continue
        result[sub][pred]=unique if len(unique)>1 else unique[0]
    return list(result.values()),conflicts

def validate(g,v):
    errors=[]; warnings=[]; nodes=g.get('@graph',[]); ids=[n.get('@id') for n in nodes]
    if len(ids)!=len(set(ids)): errors.append('Duplicate node IDs')
    if not all(iri(x) for x in ids): errors.append('Every node must have an absolute IRI')
    for n in nodes:
        for p,val in n.items():
            if p=='@id': continue
            for x in values(val):
                try: warnings.extend(v.check(values(n.get('@type',[])),p,x))
                except Exception as e: errors.append(str(e))
                if isinstance(x,dict) and '@id' in x:
                    ref=x['@id']
                    if not iri(ref): errors.append('Relative reference '+ref)
                    if ref.startswith('urn:uuid:') and ref not in ids: errors.append('Unresolved local reference '+ref)
                if x is None or x=='': errors.append('Empty value')
    try:
        v.compact(g)
        jsonld.expand(g,v.opts())
    except Exception as e: errors.append('JSON-LD: '+str(e))
    return {'syntax':True,'jsonld_and_vocabulary':not errors,'errors':errors,'compatibility_warnings':sorted(set(warnings)),'publication_eligibility':'not assessed; no rich-result guarantee'}

def pipeline(args):
    out=Path(args.output); out.mkdir(parents=True,exist_ok=True); v=Vocabulary()
    if args.validate_only:
        g=strict(Path(args.validate_only).read_text());r=validate(g,v);save(out/'validation.json',r);return 1 if r['errors'] else 0
    mappings=strict(Path(args.canonical_map).read_text()) if args.canonical_map else {}
    annotations=strict(Path(args.annotations).read_text()) if args.annotations else {'claims':[],'coverage':{}}
    # Withdraw stale publication exports before any failed review can leave them visible.
    for name in ['corpus.jsonld','corpus.min.jsonld','corpus-jsonld.html']:
        (out/name).unlink(missing_ok=True)
    for previous in (out/'documents').glob('*.jsonld'): previous.unlink()
    db=sqlite3.connect(out/'index.sqlite');db.execute('CREATE VIRTUAL TABLE IF NOT EXISTS records USING fts5(document_id UNINDEXED, record_id UNINDEXED,text)')
    db.execute('DELETE FROM records')
    registry_path=out/'identity-registry.json'
    registry=strict(registry_path.read_text()) if registry_path.exists() else {}
    manifests=[]; documents=[]; records={}; nodes=[]; claims=[]; warnings=[]
    corpus_id=registry.setdefault('_corpus', 'urn:uuid:'+str(uuid.uuid4()))
    def assert_(sub,pred,value,doc,rec,reason,explicit=False):
        claims.append({'subject':sub,'predicate':pred,'value':value,'document_id':doc,'record_id':rec['id'] if rec else None,'locator':rec['locator'] if rec else {'manifest':True},'excerpt':rec['text'][:240] if rec else None,'evidence_digest':digest(rec['text']) if rec else None,'extraction_quality':'partial' if rec and rec.get('partial') else 'native','rationale':reason,'explicit':explicit})
    unique_digests={}
    for file in args.inputs:
        p=Path(file).resolve(); entry={'source':str(p),'status':'failed','language':args.language or 'undetermined'}
        try:
            raw=p.read_bytes();sha=digest(raw);entry['content_digest']=sha
            key=str(p); old=registry.setdefault(key,{'id':'urn:uuid:'+str(uuid.uuid4())})
            ident=mappings.get(file,mappings.get(key,old['id']))
            if not iri(ident): raise ValueError('Canonical document ID must be absolute')
            entry.update(document_id=ident,previous_id=old['id'] if old['id']!=ident else None)
            if old['id']!=ident: old.setdefault('migrations',[]).append({'from':old['id'],'to':ident})
            old['id']=ident
            cachekey=digest([sha,VERSION,v.provenance]);cache=out/'cache'/f'{cachekey}.json'
            cached=cache.exists();data=strict(cache.read_text()) if cached else extract(p)
            if not cached: save(cache,data)
            entry.update({k:data[k] for k in ['mime','adapter','adapter_version','complete','limitations']});entry['cached']=cached
            entry['analysis_digest']=digest([sha,VERSION,v.provenance,annotations])
            entry['status']='extracted' if data['complete'] else 'partial'
            if not data['records']:
                entry['status']='unreadable';manifests.append(entry);continue
            if sha in unique_digests:
                entry['duplicate_of']=unique_digests[sha];manifests.append(entry);continue
            unique_digests[sha]=ident; documents.append(ident);nodes.append({'@id':ident})
            assert_(ident,'@type','CreativeWork',ident,None,'Readable document representation')
            assert_(ident,'encodingFormat',data['mime'],ident,None,'Detected format')
            assert_(ident,'isPartOf',{'@id':corpus_id},ident,None,'Input corpus membership')
            if args.language: assert_(ident,'inLanguage',args.language,ident,None,'User-supplied language')
            db.execute('DELETE FROM records WHERE document_id=?',(ident,))
            for i,rec in enumerate(data['records']):
                rid=opaque(ident+'|'+json.dumps(rec['locator'],sort_keys=True));rec={**rec,'id':rid,'document_id':ident,'ordinal':i,'partial':not data['complete'],'normalized_text':unicodedata.normalize('NFKC',rec['text']).casefold()}
                records[rid]=rec; db.execute('INSERT INTO records VALUES (?,?,?)',(ident,rid,rec['text']))
                if rec['kind'] in {'heading','table','image','chapter'}:
                    nodes.append({'@id':rid});t='Table' if rec['kind']=='table' else 'ImageObject' if rec['kind']=='image' else 'CreativeWork'
                    assert_(rid,'@type',t,ident,rec,'Structural extraction')
                    assert_(rid,'isPartOf',{'@id':ident},ident,rec,'Document part')
                    assert_(ident,'hasPart',{'@id':rid},ident,rec,'Document structure')
                    assert_(rid,'position',i+1,ident,rec,'Extracted source order')
                    if rec['kind'] in {'heading','chapter'}: assert_(rid,'name',re.sub(r'^#{1,6}\s+','',rec['text']) if data['mime']=='text/markdown' else rec['text'],ident,rec,'Visible heading',True)
            headings=[r for r in data['records'] if r['kind']=='heading']
            if headings:
                rr=next(r for r in records.values() if r['document_id']==ident and r['kind']=='heading')
                title=re.sub(r'^#{1,6}\s+','',rr['text']) if data['mime']=='text/markdown' else rr['text']
                assert_(ident,'name',title,ident,rr,'First extracted heading; descriptive document name',True)
            for existing in data.get('existing_jsonld',[]):
                try:
                    if isinstance(existing,dict) and 'error' in existing: raise ValueError(existing['error'])
                    payload=existing.get('data',existing) if isinstance(existing,dict) else strict(existing)
                    jsonld.expand(payload,v.opts())
                except Exception as e: warnings.append({'document_id':ident,'existing_jsonld_error':str(e)})
            entry['existing_jsonld']=data.get('existing_jsonld',[]);entry['metadata']=data.get('metadata',{})
        except Exception as e: entry['error']=str(e)
        manifests.append(entry)
    nodes.insert(0,{'@id':corpus_id})
    assert_(corpus_id,'@type','Collection',corpus_id,None,'Selected document corpus')
    for d in documents: assert_(corpus_id,'hasPart',{'@id':d},d,None,'Corpus membership')
    # The agent must review every semantic assertion; literal excerpts are checked here.
    for c in annotations.get('claims',[]):
        rec=records.get(c.get('record_id'))
        if not rec: raise ValueError('Annotation references nonexistent source record')
        quote=c.get('quote','')
        if not quote or quote not in rec['text']: raise ValueError('Evidence quote missing from source')
        if not c.get('rationale') or c.get('status')!='accepted': raise ValueError('Unreviewed semantic assertion')
        sub=c['subject'];pred=c['predicate'];val=c['value']
        if not iri(sub): raise ValueError('Annotation subject must be absolute IRI')
        if val is None or val=='': raise ValueError('Empty annotation')
        v.check([],pred,val)
        if c.get('explicit') and isinstance(val,str) and pred not in {'@type','url','sameAs'} and val not in quote:
            raise ValueError('Explicit value not present in evidence quote')
        nodes.append({'@id':sub})
        assert_(sub,pred,val,rec['document_id'],rec,c['rationale'],c.get('explicit',False))
        claims[-1]['excerpt']=quote;claims[-1]['context']=c.get('context','assertion');claims[-1]['reviewed']=True
    merged,conflicts=merge(nodes,claims)
    # More specific accepted classifications replace a redundant CreativeWork baseline.
    for n in merged:
        ts=values(n.get('@type',[]))
        if 'CreativeWork' in ts and len(ts)>1 and any('CreativeWork' in v.ancestors(t) for t in ts if t!='CreativeWork'):
            ts.remove('CreativeWork');n['@type']=ts if len(ts)>1 else ts[0]
    order=[corpus_id,*documents,*[r['id'] for r in records.values() if r['kind'] in {'heading','table','image','chapter'}]]
    priority={x:i for i,x in enumerate(order)};merged.sort(key=lambda n:(priority.get(n['@id'],len(order)),n['@id']))
    g={'@context':'https://schema.org','@graph':merged};r=validate(g,v)
    cov=annotations.get('coverage',{}); unresolved=[rid for rid in records if cov.get(rid,{}).get('status') not in {'mapped','inherits','no-useful-mapping'}]
    r.update(extraction_complete=all(m.get('complete',False) for m in manifests),semantic_review_complete=bool(records) and not unresolved and annotations.get('review_rounds',0)>=2,unresolved_records=unresolved,record_count=len(records),node_count=len(merged),assertion_count=len(claims),conflicts=conflicts,existing_data_warnings=warnings,vocabulary=v.provenance,coverage_review_rounds=annotations.get('review_rounds',0),evidence_fidelity='Automatic assertions and quote presence checked; semantic truth requires agent review')
    save(out/'manifest.json',manifests);save(out/'records.json',list(records.values()));save(out/'identity-registry.json',registry);save(out/'evidence.json',claims);save(out/'validation.json',r)
    chunks=[]
    for rec in records.values():
        text=rec['text']
        for start in range(0,len(text),3800):
            chunks.append({'record_id':rec['id'],'document_id':rec['document_id'],'source_locator':rec['locator'],'char_start_in_record':start,'char_end_in_record':min(start+4000,len(text)),'text':text[start:start+4000]})
            if start+4000>=len(text): break
    save(out/'chunks.json',chunks)
    save(out/'annotation-template.json',{'claims':[],'coverage':{rid:{'status':'unresolved','rationale':''} for rid in records},'review_rounds':0})
    if r['errors']: db.commit();db.close();return 1
    v.compact(g) # Verify standards compaction without changing readable presentation order.
    save(out/'corpus.jsonld',g)
    compact=json.dumps(g,ensure_ascii=False,separators=(',',':'),allow_nan=False)
    (out/'corpus.min.jsonld').write_text(compact)
    html='<script type="application/ld+json">'+compact.replace('<','\\u003c')+'</script>\n'
    assert strict(html.split('>',1)[1].rsplit('</script>',1)[0])==g
    (out/'corpus-jsonld.html').write_text(html)
    assert v.canonical(strict((out/'corpus.min.jsonld').read_text()))==v.canonical(g)
    for d in documents:
        wanted={d}; changed=True
        while changed:
            changed=False
            for n in merged:
                if n['@id'] not in wanted: continue
                for pred,val in n.items():
                    if pred=='isPartOf':continue
                    for x in values(val):
                        if isinstance(x,dict) and x.get('@id') not in wanted and x.get('@id')!=corpus_id:
                            wanted.add(x['@id']);changed=True
        dg={'@context':'https://schema.org','@graph':[copy.deepcopy(n) for n in merged if n['@id'] in wanted]}
        for n in dg['@graph']:
            if n['@id']==d:n.pop('isPartOf',None)
        save(out/'documents'/(digest(d)[:20]+'.jsonld'),dg)
    db.commit();db.close()
    print(json.dumps({'documents':len(documents),'records':len(records),'validation_errors':len(r['errors']),'semantic_review_complete':r['semantic_review_complete'],'output':str(out)}))
    return 0

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('inputs',nargs='*');p.add_argument('--output',required=True);p.add_argument('--canonical-map');p.add_argument('--language');p.add_argument('--annotations');p.add_argument('--offline',action='store_true',help='All processing uses bundled pinned vocabulary and contexts; no network calls')
    p.add_argument('--scope',choices=['document','corpus'],default='corpus');p.add_argument('--validate-only',metavar='JSONLD')
    a=p.parse_args()
    if not a.inputs and not a.validate_only:p.error('Provide at least one document')
    if a.scope=='document' and len(a.inputs)>1:p.error('Document scope requires one input')
    try:return pipeline(a)
    except Exception as e: print('schemata: '+str(e),file=sys.stderr);return 1

if __name__=='__main__':sys.exit(main())
