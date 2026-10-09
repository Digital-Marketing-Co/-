#!/usr/bin/env python3
"""Copy reproducible seed records without asserting a fresh evidence search."""
import argparse,json,shutil,hashlib
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('run_dir');a=p.parse_args();r=Path(a.run_dir);r.mkdir(parents=True,exist_ok=True)
ref=Path(__file__).resolve().parents[1]/'references'
for seed,out in [('seed_registry.json','source_registry.json'),('seed_curriculum.json','curriculum.json'),('seed_manuscript.json','manuscript.json'),('seed_training_templates.json','training_templates.json')]:
 if (r/out).exists():raise SystemExit('Refusing to overwrite '+out)
 shutil.copyfile(ref/seed,r/out)
m={'mode':'seed-reuse','cutoff':'2026-10-09','search_date':None,'saturation_reached':False,'completion':'seed only; research/update/render requirements pending','artifacts':{}}
for x in r.glob('*.json'):m['artifacts'][x.name]={'sha256':hashlib.sha256(x.read_bytes()).hexdigest(),'verification':'inherited bounded seed; access limitations retained'}
(r/'manifest.json').write_text(json.dumps(m,indent=2));print(r)
