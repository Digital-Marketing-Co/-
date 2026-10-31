#!/usr/bin/env python3
"""Deterministic coverage verifier for expected and exported document manifests."""
import argparse, json, pathlib, sys
CATEGORIES=('sections','equations','figures','tables','citations','appendices')
def check(source, output):
    issues=[]; counts={}
    for cat in CATEGORIES:
        s=source.get(cat,[]);o=output.get(cat,[])
        if not isinstance(s,list) or not isinstance(o,list):
            issues.append(f'{cat}: must be arrays');continue
        for label,items in [('source',s),('output',o)]:
            if any(not isinstance(v,str) or not v.strip() for v in items):issues.append(f'{cat}: invalid {label} ID')
            if len(items)!=len(set(items)):issues.append(f'{cat}: duplicate {label} ID')
        missing=sorted(set(s)-set(o));extra=sorted(set(o)-set(s))
        if missing:issues.append(f'{cat}: missing {missing}')
        if extra:issues.append(f'{cat}: unexpected {extra}')
        counts[cat]={'expected':len(s),'exported':len(o)}
    for key in ('last_section_text_sha256','source_revision'):
        if key in source and source[key]!=output.get(key):issues.append(f'{key}: mismatch')
    return {'status':'PASS' if not issues else 'FAIL','issues':issues,'counts':counts}
def main():
    p=argparse.ArgumentParser();p.add_argument('source');p.add_argument('export');a=p.parse_args()
    try:
        s=json.loads(pathlib.Path(a.source).read_text());o=json.loads(pathlib.Path(a.export).read_text())
        result=check(s,o);print(json.dumps(result,indent=2));return 0 if result['status']=='PASS' else 1
    except (ValueError,OSError) as e:print('ERROR:',e,file=sys.stderr);return 2
if __name__=='__main__':sys.exit(main())
