#!/usr/bin/env python3
import copy, importlib.util, json, tempfile, unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location('learning',Path(__file__).with_name('learn.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class LearningTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name);self.db=m.connect(self.root/'events.sqlite');self.skills=self.root/'skills';self.skills.mkdir()
  for name,desc in [('app','WebGL runtime rendering app image import'),('images','Image alpha transparency fade photographic banner'),('latex','Compiled mathematical equations and symbols')]:
   p=self.skills/('skill-'+name);p.mkdir();(p/'SKILL.md').write_text('---\nname: '+name+'\ndescription: '+desc+'\n---\n# '+name+'\n')
  self.before=self.root/'before.log';self.before.write_text('WebGL failed in a browser with unavailable acceleration.');self.after=self.root/'after.log';self.after.write_text('Fallback renders and movie recording succeeds.')
  self.event={'schema_version':1,'origin_skill':'app','affected_skills':['app'],'category':'render failure','summary':'WebGL runtime failed without fallback','expected':'Scene visible','actual':'Blank scene','root_cause':'Graphics acceleration unavailable and no fallback','verification':'verified','regression':'PASS','sanitized':True,'evidence':[{'path':str(p),'sha256':m.digest(p),'phase':phase} for p,phase in [(self.before,'before'),(self.after,'after')]]}
 def tearDown(self):self.db.close();self.tmp.cleanup()
 def test_custody_dedup(self):
  a=m.record(self.db,self.event);b=m.record(self.db,self.event);self.assertTrue(a['inserted']);self.assertFalse(b['inserted']);self.assertEqual(len(m.events(self.db)),1)
 def test_bad_hash_rejected(self):
  self.event['evidence'][0]['sha256']='0'*64
  with self.assertRaises(ValueError):m.record(self.db,self.event)
 def test_unverified_not_learned(self):
  self.event.update(verification='blocked',regression='NOT_TESTED');m.record(self.db,self.event);self.assertEqual(m.rank(self.db,'WebGL rendering',self.skills)['training_events'],0)
 def test_secret_rejected(self):
  self.event['summary']='api_key=do-not-record-this'
  with self.assertRaises(ValueError):m.record(self.db,self.event)
 def test_synthetic_excluded(self):
  self.event['synthetic']=True;a=m.record(self.db,self.event);self.assertEqual(m.rank(self.db,'render',self.skills)['training_events'],0)
  with self.assertRaises(ValueError):m.promote(self.db,a['event_id'],'app',self.skills,m.digest(self.skills/'skill-app/SKILL.md'),'Add a fallback renderer for unavailable WebGL.')
 def test_cold_rank_and_abstain(self):
  r=m.rank(self.db,'alpha transparency fade banner',self.skills);self.assertEqual(r['suggestions'][0]['skill'],'images');self.assertTrue(m.rank(self.db,'zzzzzz',self.skills)['abstained'])
 def test_learned_mode(self):
  for i in range(5):
   e=copy.deepcopy(self.event);e['summary']+=' case '+str(i);m.record(self.db,e)
  r=m.rank(self.db,'WebGL runtime fallback',self.skills);self.assertEqual(r['mode'],'multinomial-naive-bayes');self.assertEqual(r['suggestions'][0]['skill'],'app');self.assertTrue(r['scores_are_uncalibrated'])
 def test_supersession(self):
  a=m.record(self.db,self.event);e=copy.deepcopy(self.event);e.update(supersedes=a['event_id'],verification='blocked',regression='NOT_TESTED');m.record(self.db,e);self.assertEqual(len(m.events(self.db)),2);self.assertEqual(m.rank(self.db,'WebGL',self.skills)['training_events'],0)
 def test_promotion_digest_and_idempotence(self):
  a=m.record(self.db,self.event);p=self.skills/'skill-app/SKILL.md';rule='Add a Canvas fallback and verify recording when WebGL is unavailable.'
  with self.assertRaises(ValueError):m.promote(self.db,a['event_id'],'app',self.skills,'0'*64,rule)
  r=m.promote(self.db,a['event_id'],'app',self.skills,m.digest(p),rule);self.assertTrue(r['git_sync_required']);self.assertTrue(m.promote(self.db,a['event_id'],'app',self.skills,m.digest(p),rule)['already_applied']);self.assertEqual(p.read_text().count(rule),1)
 def test_wrong_target_rejected(self):
  a=m.record(self.db,self.event)
  with self.assertRaises(ValueError):m.promote(self.db,a['event_id'],'latex',self.skills,m.digest(self.skills/'skill-latex/SKILL.md'),'Add a fallback.')
 def test_changed_evidence_rejected_before_promotion(self):
  a=m.record(self.db,self.event);self.after.write_text('changed')
  with self.assertRaises(ValueError):m.promote(self.db,a['event_id'],'app',self.skills,m.digest(self.skills/'skill-app/SKILL.md'),'Use fallback graphics.')
 def test_unknown_payload_rejected(self):
  self.event['private_payload']='Unrelated private data'
  with self.assertRaises(ValueError):m.record(self.db,self.event)
 def test_string_synthetic_rejected(self):
  self.event['synthetic']='false'
  with self.assertRaises(ValueError):m.record(self.db,self.event)
 def test_acquired_time_owned_by_ledger(self):
  self.event['acquired_utc']='2026-01-01'
  with self.assertRaises(ValueError):m.record(self.db,self.event)
 def test_untrained_candidates_preserved(self):
  for i in range(5):
   e=copy.deepcopy(self.event);e['summary']+=' case '+str(i);m.record(self.db,e)
  r=m.rank(self.db,'alpha transparency fade image',self.skills);self.assertIn('images',[x['skill'] for x in r['untrained_metadata_candidates']])
 def test_promotion_ignores_planted_temp_symlink(self):
  a=m.record(self.db,self.event);p=self.skills/'skill-app/SKILL.md';sentinel=self.root/'private.txt';sentinel.write_text('unchanged');p.with_suffix('.md.learning-tmp').symlink_to(sentinel)
  m.promote(self.db,a['event_id'],'app',self.skills,m.digest(p),'Provide a graphics fallback for unavailable WebGL.')
  self.assertEqual(sentinel.read_text(),'unchanged');self.assertFalse(p.is_symlink())
 def test_atomic_export_ignores_planted_temp_symlink(self):
  p=self.root/'export.json';sentinel=self.root/'private.txt';sentinel.write_text('unchanged');p.with_suffix('.json.tmp').symlink_to(sentinel);m.atomic_write(p,'{}');self.assertEqual(sentinel.read_text(),'unchanged');self.assertFalse(p.is_symlink())
if __name__=='__main__':unittest.main()
