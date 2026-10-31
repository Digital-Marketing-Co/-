#!/usr/bin/env python3
"""KARMA append-only hash-chain QA evidence ledger; stdlib-only local prototype."""
import argparse, datetime, fcntl, hashlib, json, os, pathlib, re, sys, uuid

def encode(v): return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def sha(v): return hashlib.sha256(encode(v).encode()).hexdigest()
def clean(v):
    if isinstance(v,dict): return {k:('[REDACTED]' if re.search('password|secret|token|api.?key',k,re.I) else clean(x)) for k,x in v.items()}
    if isinstance(v,list): return [clean(x) for x in v[:100]]
    if isinstance(v,str): return re.sub(r'(?i)(bearer\\s+\\S+|(?:password|secret|token|api.?key)\\s*[:=]\\s*\\S+)','[REDACTED]',v)[:8192]
    return v
def verify(path):
    previous=None; count=0
    if not path.exists(): return dict(count=0,head=None,status='PASS')
    for raw in path.read_text(encoding='utf8').splitlines():
        e=json.loads(raw);count+=1
        if e.get('sequence')!=count or e.get('previous_digest')!=previous or e.get('event_digest')!=sha({k:v for k,v in e.items() if k!='event_digest'}):
            raise ValueError('ledger integrity failure at event '+str(count))
        previous=e['event_digest']
    return dict(count=count,head=previous,status='PASS')
def append(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.with_suffix(path.suffix+'.lock').open('a+') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX);state=verify(path)
        if not isinstance(data,dict): raise ValueError('event must be a JSON object')
        if data.get('status','OBSERVED') not in ('OBSERVED','REPRODUCED','TRIAGED','FIX_PROPOSED','VERIFIED','REGRESSED','BLOCKED'):
            raise ValueError('unknown status')
        event={k:v for k,v in clean(data).items() if k not in ('sequence','event_digest','previous_digest')}
        event.update(schema_version='1.0',event_id=str(uuid.uuid4()),timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),sequence=state['count']+1,previous_digest=state['head'])
        event['event_digest']=sha(event)
        fd=os.open(str(path),os.O_WRONLY|os.O_APPEND|os.O_CREAT,0o600)
        with os.fdopen(fd,'a',encoding='utf8') as f:
            f.write(encode(event)+'\n');f.flush();os.fsync(f.fileno())
        return event
def main():
    p=argparse.ArgumentParser();p.add_argument('command',choices=['append','verify']);p.add_argument('ledger');p.add_argument('input',nargs='?');a=p.parse_args()
    path=pathlib.Path(a.ledger)
    try:
        if a.command=='append':
            if not a.input: raise ValueError('append requires an input JSON file')
            result=append(path,json.loads(pathlib.Path(a.input).read_text(encoding='utf8')))
        else: result=verify(path)
        print(encode(result))
    except (OSError,ValueError,json.JSONDecodeError) as exc:
        print('FAIL: '+str(exc),file=sys.stderr);sys.exit(1)
if __name__=='__main__':main()
