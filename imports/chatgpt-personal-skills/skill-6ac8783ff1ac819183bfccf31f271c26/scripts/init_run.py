#!/usr/bin/env python3
"""Initialize writable run records without fabricating completed research."""
import argparse,csv,json,datetime
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('run_dir');p.add_argument('--mode',choices=['research','update','dog','render'],default='research');a=p.parse_args()
r=Path(a.run_dir);r.mkdir(parents=True,exist_ok=True)
if any(r.iterdir()):p.error('Use a new empty directory; existing runs are never overwritten')
root=Path(__file__).resolve().parent.parent
manifest=json.loads((root/'references/run-manifest-template.json').read_text());manifest.update(run_id=r.name,mode=a.mode,created_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
(r/'manifest.json').write_text(json.dumps(manifest,indent=2))
for name in ['source_registry','curriculum','image_inventory']:(r/(name+'.json')).write_text('[]\n')
fields=['id','profile_id','category','purpose','prerequisites','baseline','success_criteria','environment','equipment','reinforcement','steps','progression','regression','generalization','maintenance','troubleshooting','welfare','evidence_ids','designer_selected_criteria','review_date','referral_conditions']
(r/'training_templates.json').write_text(json.dumps({'plan':dict.fromkeys(fields),'profile':dict.fromkeys(['profile_id','age','medical_status','sensory_status','mobility','household','observed_behavior','antecedents','consequences','bite_history','preferred_rewards','equipment','owner_constraints','missing_information'])},indent=2))
(r/'qa_report.json').write_text(json.dumps({'gates':[],'status':'incomplete','limitations':['Research, curriculum, images and PDF not yet produced.']},indent=2))
headers={'search_log':['pass_id','searched_at','platform','query_exact','filters','source_id','eligibility','decision_reason','retrieval_status','new_material_finding'], 'evidence_matrix':['claim_id','claim_text','claim_type','source_id','locator','locator_verified','evidence_grade','risk_of_bias','alternatives','transfer_limits','training_ids','note_numbers'],'session_template':['session_id','date','plan_id','setting','opportunities','successes','latency_seconds','prompt_level','reinforcement','observed_stress','recovery','opt_out','next_adjustment']}
for name,header in headers.items():
 with (r/(name+'.csv')).open('w',newline='') as f:csv.writer(f).writerow(header)
print('Initialized incomplete run:',r)
