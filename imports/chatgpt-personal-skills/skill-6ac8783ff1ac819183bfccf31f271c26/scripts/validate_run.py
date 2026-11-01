#!/usr/bin/env python3
"""Validate traceability and required run artifacts; never substitutes for visual review."""
import argparse,json,hashlib
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('run_dir');a=p.parse_args();r=Path(a.run_dir);issues=[];ids=[]
required=['manifest.json','source_registry.json','evidence_matrix.csv','search_log.csv','curriculum.json','training_templates.json','image_inventory.json','qa_report.json','monograph.pdf']
for f in required:
 if not (r/f).is_file():issues.append('Missing '+f)
if (r/'source_registry.json').exists():
 src=json.loads((r/'source_registry.json').read_text());ids=[s.get('source_id') for s in src]
 if not src:issues.append('Empty source registry')
 if len(set(ids))!=len(ids):issues.append('Duplicate source IDs')
 for s in src:
  for k in ['authors','title','date','venue','stable_url','access_level','study_design','sample','methods','findings','limitations','relevance','locators']:
   if k not in s:issues.append(s['source_id']+' missing '+k)
if (r/'curriculum.json').exists():
 curriculum=json.loads((r/'curriculum.json').read_text())
 if not curriculum:issues.append('Empty curriculum')
 for c in curriculum:
  for k in ['id','purpose','prerequisites','success_criteria','environment','equipment','reinforcement','steps','progression','generalization','maintenance','troubleshooting','welfare','evidence_ids']:
   if not c.get(k):issues.append(c.get('id','?')+' missing '+k)
  for sid in c.get('evidence_ids',[]):
   if sid not in ids:issues.append('Unknown curriculum source '+sid)
if (r/'image_inventory.json').exists():
 inv=json.loads((r/'image_inventory.json').read_text())
 if not inv:issues.append('Empty image inventory')
 hashes=[i.get('sha256') for i in inv if i.get('sha256')]
 if len(set(hashes))!=len(hashes):issues.append('Reused image file')
 for i in inv:
  if i.get('status')!='verified':issues.append('Unverified image '+i['id'])
if (r/'qa_report.json').exists():
 qa=json.loads((r/'qa_report.json').read_text())
 if not qa.get('gates'):issues.append('Empty QA gates')
 for g in qa.get('gates',[]):
  if g['status'] not in ['verified','not_applicable']:issues.append('Unpassed gate: '+g['name'])
result={'structural_issues':issues,'structural_checks_passed':not issues,'complete':False,'visual_review_automated':False};(r/'validation.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
raise SystemExit(0 if not issues else 2)
