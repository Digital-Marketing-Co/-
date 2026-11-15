#!/usr/bin/env python3
"""Read-only skills inventory and heuristic audit; Python stdlib only."""
import argparse, pathlib, json, hashlib, re, unicodedata, sys
p=argparse.ArgumentParser()
p.add_argument('repo')
p.add_argument('--out',default='perfect-qa.json')
a=p.parse_args()
root=pathlib.Path(a.repo).resolve()
paths=sorted(root.glob('skills/*/SKILL.md'))
findings=[];items=[];aliases={}
def issue(path,kind,severity,detail):
    findings.append(dict(path=str(path.relative_to(root)),kind=kind,severity=severity,detail=detail))
for f in paths:
    s=f.read_text(encoding='utf-8',errors='replace')
    name=f.parent.name
    items.append(dict(name=name,path=str(f.relative_to(root)),sha256=hashlib.sha256(f.read_bytes()).hexdigest(),bytes=f.stat().st_size))
    if not s.startswith('---\n'):
        issue(f,'frontmatter','warning','No opening YAML frontmatter')
    if not re.search(r'(?m)^description\s*:',s[:4000]):
        issue(f,'description','warning','No description in initial frontmatter')
    for ch in s:
        if unicodedata.category(ch)=='Cf' and ch not in '\u200c\u200d':
            issue(f,'unicode-control','review',f'U+{ord(ch):04X}')
            break
    for match in re.finditer(r'(?i)(?:api[_-]?key|secret|token|password)\s*[:=]\s*["\']?([A-Za-z0-9_\-]{20,})',s):
        issue(f,'possible-secret','review','Potential credential assignment; value intentionally suppressed')
    for ref in re.findall(r'\]\(([^)#]+)(?:#[^)]*)?\)',s):
        if '://' in ref or ref.startswith(('#','@','/')):
            continue
        target=(f.parent/ref).resolve()
        if root in target.parents and not target.exists():
            issue(f,'missing-relative-reference','warning',ref)
    for al in re.findall(r'(?m)^\s*(?:Aliases?|aliases?)\s*:\s*(.+)$',s[:6000]):
        for tok in re.findall(r'/[A-Za-z][\w-]*',al):
            aliases.setdefault(tok.lower(),set()).add(name)
for alias,owners in sorted(aliases.items()):
    if len(owners)>1:
        findings.append(dict(path='(cross-skill)',kind='alias-collision',severity='review',detail=f'{alias}: {sorted(owners)}'))
report=dict(schema='perfect-qa-v1',repo=str(root),skill_count=len(items),skills=items,findings=findings,checks={'inventory':'executed','frontmatter':'heuristic','references':'heuristic','unicode':'heuristic','secrets':'heuristic','aliases':'heuristic','visual_qa':'NOT_RUN','unit_tests':'NOT_RUN','integration_tests':'NOT_RUN','two_clean_passes':'NOT_RUN'},release_status='NOT_VERIFIED')
pathlib.Path(a.out).write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'skills':len(items),'findings':len(findings),'report':a.out,'release_status':'NOT_VERIFIED'}))
sys.exit(2 if not items else 0)
