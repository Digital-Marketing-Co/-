#!/usr/bin/env python3
"""Durable single-process document operation ledger; caller serializes writes."""
import argparse,hashlib,json,os,tempfile
from pathlib import Path
from plan import canonical
class Ledger:
    def __init__(self,path):
        self.path=Path(path)
        self.data=json.loads(self.path.read_text()) if self.path.exists() else {'operations':{}}
    def save(self):
        self.path.parent.mkdir(parents=True,exist_ok=True)
        with tempfile.NamedTemporaryFile('w',dir=self.path.parent,delete=False) as f:
            json.dump(self.data,f,indent=2);f.flush();os.fsync(f.fileno());tmp=f.name
        os.replace(tmp,self.path)
    def begin(self,context):
        required={'run','document','revision','skill','phase','input_digest','options_digest','scope'}
        if set(context)!=required or not all(isinstance(v,str) and v for v in context.values()):
            raise ValueError('Provide all eight nonempty operation identity strings')
        context=dict(context,skill=canonical(context['skill']))
        key=hashlib.sha256(json.dumps(context,sort_keys=True).encode()).hexdigest()
        prior=self.data['operations'].get(key,{})
        if prior.get('state')=='running':raise ValueError('Operation already running; recursive or duplicate dispatch blocked')
        if prior.get('state')=='done':return key,'reuse'
        self.data['operations'][key]={'context':context,'state':'running','attempt':prior.get('attempt',0)+1}
        self.save();return key,'execute'
    def finish(self,key,state,evidence):
        if state not in {'done','failed','blocked'}:raise ValueError('Invalid terminal state')
        op=self.data['operations'][key]
        if op['state']!='running':raise ValueError('Only running operations may finish')
        if not evidence:raise ValueError('Evidence or failure reason required')
        op.update(state=state,evidence=evidence);self.save()
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('path');sub=p.add_subparsers(dest='action',required=True)
    a=sub.add_parser('begin');a.add_argument('context',help='JSON with eight identity strings')
    a=sub.add_parser('finish');a.add_argument('key');a.add_argument('state');a.add_argument('evidence')
    a=p.parse_args();ledger=Ledger(a.path)
    try:
        if a.action=='begin':print(json.dumps(ledger.begin(json.loads(a.context))))
        else:ledger.finish(a.key,a.state,a.evidence);print(a.state)
    except (ValueError,KeyError) as e:p.exit(1,str(e)+'\n')
