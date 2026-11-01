#!/usr/bin/env python3
"""Local supervised error routing, forensic custody, and bounded rule promotion."""
import argparse, collections, datetime, hashlib, json, math, os, re, sqlite3, sys, tempfile
from pathlib import Path

SECRET = re.compile(r'(?:sk-[A-Za-z0-9_-]{16,}|(?:api[_-]?key|password|bearer|token)\s*[:=]\s*\S+)', re.I)
SECTIONS = {'visual system':{'alpha','image','visual','fade','contrast','layout','banner'}, 'engineering':{'render','webgl','buffer','memory','runtime','database','schema','error'}, 'quality gates':{'test','qa','regression','verify','failure','validation'}, 'discovery and provenance':{'source','revision','evidence','artifact','repository'}, 'functional requirements':{'import','export','save','record','keyboard','interaction'}, 'delivery':{'deploy','publish','release','report'}}
def canonical(x): return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def digest(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def tokens(t): return collections.Counter(re.findall(r'[a-z][a-z0-9_-]{2,}',str(t).lower()))
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def atomic_write(path, content):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    fd,temp=tempfile.mkstemp(prefix='.'+path.name+'.',dir=path.parent)
    try:
        with os.fdopen(fd,'w') as out:
            out.write(content);out.flush();os.fsync(out.fileno())
        if path.exists() and not path.is_symlink(): os.chmod(temp,path.stat().st_mode & 0o777)
        os.replace(temp,path)
    finally:
        if os.path.exists(temp): os.unlink(temp)

def registry(root):
    root=Path(root).resolve(); out={}
    for p in sorted([ *root.glob('skill-*/SKILL.md'), *root.glob('error-learning/SKILL.md') ]):
        if p.parent.name=='uninstalled' or p.is_symlink() or not p.resolve().is_relative_to(root): continue
        text=p.read_text();m=re.search(r'^name:\s*[\'"]?([^\n\'"]+)',text,re.M)
        if not m: continue
        name=m.group(1).strip();desc=re.search(r'^description:\s*(.*)',text,re.M)
        out.setdefault(name,[]).append({'path':p,'text':text,'description':name+' '+(desc.group(1) if desc else '')})
    return out

def connect(path):
    p=Path(path);p.parent.mkdir(parents=True,exist_ok=True);db=sqlite3.connect(p,timeout=10)
    db.execute('CREATE TABLE IF NOT EXISTS events (id TEXT PRIMARY KEY, acquired TEXT NOT NULL, payload TEXT NOT NULL)')
    db.execute('CREATE TABLE IF NOT EXISTS promotions (id TEXT PRIMARY KEY,event_id TEXT NOT NULL,skill TEXT NOT NULL,before_sha TEXT NOT NULL,after_sha TEXT NOT NULL,acquired TEXT NOT NULL,rule_sha TEXT NOT NULL)');db.commit();return db

def events(db): return [dict(json.loads(p),event_id=i,acquired_utc=t) for i,t,p in db.execute('SELECT id,acquired,payload FROM events ORDER BY id')]
def active(db):
    es=events(db);retired={e.get('supersedes') for e in es};return [e for e in es if e['event_id'] not in retired]
def trainable(e): return e['verification']=='verified' and e['regression']=='PASS' and not e.get('synthetic',False)
def clean(t):
    if SECRET.search(t): raise ValueError('Possible credential content; minimize and sanitize before recording.')

def validate(e, stored=False):
    allowed={"schema_version","origin_skill","affected_skills","category","summary","expected","actual","root_cause","verification","regression","sanitized","evidence","source_revision","source_report_id","synthetic","supersedes"}
    if stored: allowed|={"event_id","acquired_utc"}
    if not isinstance(e,dict) or set(e)-allowed: raise ValueError("Unknown or reserved event fields are not accepted")
    if "synthetic" in e and type(e["synthetic"]) is not bool: raise ValueError("synthetic must be Boolean")
    for k in ["source_revision","source_report_id","supersedes"]:
        if k in e and (not isinstance(e[k],str) or len(e[k])>300): raise ValueError("Invalid optional event metadata")
    if e.get('schema_version')!=1 or e.get('sanitized') is not True: raise ValueError('Require schema_version 1 and sanitized true.')
    for k in ['origin_skill','category','summary','expected','actual','root_cause']:
        if not isinstance(e.get(k),str) or not 1<=len(e[k])<=3000: raise ValueError('Missing or oversized '+k)
    if not isinstance(e.get('affected_skills'),list) or not e['affected_skills'] or not all(isinstance(x,str) and re.fullmatch(r'[a-z0-9-]{1,64}',x) for x in e['affected_skills']): raise ValueError('Invalid affected_skills')
    if e.get('verification') not in ['verified','observed','blocked'] or e.get('regression') not in ['PASS','FAIL','NOT_TESTED']: raise ValueError('Invalid verification/regression')
    if not isinstance(e.get('evidence'),list) or not 1<=len(e['evidence'])<=12: raise ValueError('Evidence required')
    for ev in e['evidence']:
        if not isinstance(ev,dict) or set(ev)!={'path','sha256','phase'}: raise ValueError('Invalid evidence fields')
        if ev.get('phase') not in ['before','after'] or not re.fullmatch('[a-f0-9]{64}',ev.get('sha256','')): raise ValueError('Invalid evidence metadata')
        if not Path(ev['path']).is_file() or digest(ev['path'])!=ev['sha256']: raise ValueError('Evidence missing or digest mismatch')
    if e['verification']=='verified' and (e['regression']!='PASS' or {x['phase'] for x in e['evidence']}!={'before','after'}): raise ValueError('Verified event requires before/after evidence and PASS')
    clean(canonical(e));return e

def record(db,e):
    validate(e);key=hashlib.sha256(canonical(e).encode()).hexdigest()
    if e.get('supersedes') and not db.execute('SELECT 1 FROM events WHERE id=?',(e['supersedes'],)).fetchone(): raise ValueError('Unknown superseded event')
    with db: cur=db.execute('INSERT OR IGNORE INTO events VALUES (?,?,?)',(key,now(),canonical(e)))
    return {'event_id':key,'inserted':bool(cur.rowcount)}

def rank(db,text,root):
    clean(text);reg=registry(root);q=tokens(text);es=[e for e in active(db) if trainable(e)]
    labels=collections.defaultdict(collections.Counter);counts=collections.Counter();vocab=set()
    for e in es:
        ts=tokens(' '.join(e[k] for k in ['summary','category','expected','actual','root_cause']))
        for label in sorted(set(e['affected_skills'])&reg.keys()): labels[label].update(ts);counts[label]+=1;vocab.update(ts)
    scored=[];mode='lexical-cold-start';abstain=False
    if len(es)>=5 and labels:
        mode='multinomial-naive-bayes';known=set(q)&vocab
        if not known: abstain=True
        else:
            total=sum(counts.values());V=max(1,len(vocab));scores={l:math.log((counts[l]+1)/(total+len(labels)))+sum(q[w]*math.log((cs[w]+1)/(sum(cs.values())+V)) for w in known) for l,cs in labels.items()}
            top=max(scores.values());den=sum(math.exp(x-top) for x in scores.values());scored=[{'skill':l,'score':round(math.exp(x-top)/den,6)} for l,x in scores.items()]
    else:
        for name,rs in reg.items():
            ts=tokens(' '.join(r['description'] for r in rs));dot=sum(q[w]*ts[w] for w in q);den=math.sqrt(sum(v*v for v in q.values())*sum(v*v for v in ts.values()))
            if dot and den: scored.append({'skill':name,'score':round(dot/den,6)})
        abstain=not scored
    untrained=[]
    if mode=='multinomial-naive-bayes':
        for name,rs in reg.items():
            if name in labels: continue
            ts=tokens(' '.join(r['description'] for r in rs));dot=sum(q[w]*ts[w] for w in q);den=math.sqrt(sum(v*v for v in q.values())*sum(v*v for v in ts.values()))
            if dot and den: untrained.append({'skill':name,'lexical_score':round(dot/den,6)})
    placements=[k for k,ws in SECTIONS.items() if set(q)&ws]
    return {'mode':mode,'training_events':len(es),'scores_are_uncalibrated':True,'abstained':abstain,'suggestions':sorted(scored,key=lambda x:(-x['score'],x['skill']))[:8],'prompt_sections':placements,'automatic_blame_assignment':False,'untrained_metadata_candidates':sorted(untrained,key=lambda x:(-x['lexical_score'],x['skill']))[:5]}

def promote(db,event_id,skill,root,expected,rule):
    es={e['event_id']:e for e in active(db)};e=es.get(event_id)
    if not e or not trainable(e): raise ValueError('Promotion requires an active real verified event with passing regression')
    validate(e,stored=True)
    if skill not in e['affected_skills']: raise ValueError('Target not in reviewed affected_skills')
    if not 10<=len(rule.strip())<=1800 or '\n#' in rule or '\n---' in rule: raise ValueError('Invalid rule length/structure')
    clean(rule);rs=registry(root).get(skill,[])
    if len(rs)!=1: raise ValueError('Target missing or ambiguous; resolve canonical variant first')
    p=rs[0]['path'];key=hashlib.sha256((event_id+skill+rule.strip()).encode()).hexdigest()
    if db.execute('SELECT 1 FROM promotions WHERE id=?',(key,)).fetchone(): return {'promotion_id':key,'already_applied':True}
    if digest(p)!=expected: raise ValueError('Skill revision changed; reread before promotion')
    marker='<!-- verified-rule:'+key+' -->'
    content=p.read_text()
    if marker in content: return {'promotion_id':key,'already_applied':True,'ledger_recovery_required':True}
    section='\n\n## Verified corrective rules\n'
    if '## Verified corrective rules' not in content: content+=section
    content+='\n'+marker+'\n- '+rule.strip().replace('\n',' ')+' (Verified event '+event_id[:12]+'.)\n'
    atomic_write(p,content);after=digest(p)
    with db: db.execute('INSERT INTO promotions VALUES (?,?,?,?,?,?,?)',(key,event_id,skill,expected,after,now(),hashlib.sha256(rule.strip().encode()).hexdigest()))
    return {'promotion_id':key,'path':str(p),'before_sha256':expected,'after_sha256':after,'git_sync_required':True}

def coverage(root):
    reg=registry(root);result=[]
    for name,rs in reg.items():
        for r in rs:
            direct='references/output-contract.md' in r['text'];indirect=not direct and ('expound' in r['text'] or 'prompt-engineer' in r['text'])
            own=name=='error-learning';result.append({'skill':name,'path':str(r['path']),'route':'shared-contract' if direct else 'dependency-contract' if indirect else 'engine' if own else 'uncovered'})
    return {'skills':len(result),'covered':sum(x['route']!='uncovered' for x in result),'routes':result,'note':'Static dependency inventory; execution compliance is not proven.'}

def report(db):
    es=events(db);return {'events':es,'promotions':[dict(zip(['id','event_id','skill','before_sha256','after_sha256','acquired_utc','rule_sha256'],r)) for r in db.execute('SELECT * FROM promotions ORDER BY acquired,id')],'counts':{'total':len(es),'active_verified':sum(trainable(e) for e in active(db)),'blocked':sum(e['verification']=='blocked' for e in es),'observed':sum(e['verification']=='observed' for e in es),'promoted':db.execute('SELECT COUNT(*) FROM promotions').fetchone()[0]},'model_accuracy':'NOT_TESTED'}
def main():
    p=argparse.ArgumentParser();p.add_argument('--db',required=True);sub=p.add_subparsers(dest='command',required=True)
    r=sub.add_parser('record');r.add_argument('--event',required=True)
    r=sub.add_parser('rank');r.add_argument('--text-file',required=True);r.add_argument('--skills-root',required=True)
    sub.add_parser('report');r=sub.add_parser('export');r.add_argument('--output',required=True)
    r=sub.add_parser('coverage');r.add_argument('--skills-root',required=True)
    r=sub.add_parser('promote');r.add_argument('--event-id',required=True);r.add_argument('--skill',required=True);r.add_argument('--skills-root',required=True);r.add_argument('--expected-sha256',required=True);r.add_argument('--rule-file',required=True)
    a=p.parse_args();db=connect(a.db)
    if a.command=='record': out=record(db,json.loads(Path(a.event).read_text()))
    elif a.command=='rank':out=rank(db,Path(a.text_file).read_text(),a.skills_root)
    elif a.command=='coverage':out=coverage(a.skills_root)
    elif a.command=='promote':out=promote(db,a.event_id,a.skill,a.skills_root,a.expected_sha256,Path(a.rule_file).read_text())
    else:
        out={'schema_version':1,'kind':'skill-error-forensics',**report(db),'integrations':{'existing_reporting_service':'unresolved'}}
        if a.command=='export':
            path=Path(a.output);atomic_write(path,json.dumps(out,indent=2));out={'output':str(path),'sha256':digest(path)}
    print(json.dumps(out,indent=2))
if __name__=='__main__':
    try:main()
    except (ValueError,OSError,KeyError,TypeError,sqlite3.Error) as e:print(json.dumps({'error':str(e)}),file=sys.stderr);sys.exit(2)
