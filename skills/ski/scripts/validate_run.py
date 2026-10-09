#!/usr/bin/env python3
import argparse,json,csv
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('run_dir');a=p.parse_args();r=Path(a.run_dir);issues=[]
for f in ['manifest.json','source_registry.json','evidence_matrix.csv','search_log.csv','curriculum.json','training_templates.json','image_inventory.json','qa_report.json','monograph.pdf']:
 if not (r/f).is_file():issues.append('Missing '+f)
src=json.loads((r/'source_registry.json').read_text()) if (r/'source_registry.json').exists() else [];ids=[s['source_id'] for s in src]
if len(ids)!=len(set(ids)):issues.append('Duplicate source IDs')
for s in src:
 for k in ['authors','title','date','venue','stable_url','access_level','study_design','sample','methods','findings','limitations','relevance','locators']:
  if k not in s:issues.append(s['source_id']+' missing '+k)
for c in json.loads((r/'curriculum.json').read_text()) if (r/'curriculum.json').exists() else []:
 for k in ['purpose','prerequisites','success_criteria','environment','equipment','reinforcement','steps','progression','generalization','maintenance','troubleshooting','welfare','evidence_ids']:
  if not c.get(k):issues.append(c['id']+' missing '+k)
 for sid in c.get('evidence_ids',[]):
  if sid not in ids:issues.append('Unknown source '+sid)
if (r/'evidence_matrix.csv').exists():
 for row in csv.DictReader((r/'evidence_matrix.csv').open()):
  for sid in row['source_ids'].split(';'):
   if sid and sid not in ids:issues.append('Unknown matrix source '+sid)
if (r/'image_inventory.json').exists():
 inv=json.loads((r/'image_inventory.json').read_text());hs=[i['sha256'] for i in inv]
 if len(hs)!=len(set(hs)):issues.append('Reused image')
 for i in inv:
  if i.get('status') not in ['verified','generated_not_used']:issues.append('Unverified image '+i['id'])
if (r/'qa_report.json').exists():
 for g in json.loads((r/'qa_report.json').read_text()).get('gates',[]):
  if g['status'] not in ['verified','not_applicable']:issues.append('Unpassed gate '+g['name'])
res={'issues':issues,'complete':not issues,'visual_review_automated':False};(r/'validation.json').write_text(json.dumps(res,indent=2));print(json.dumps(res,indent=2));raise SystemExit(2 if issues else 0)
