import copy
import hashlib
import tempfile
import unittest
from pathlib import Path
from quality_gate import validate, BASELINES

class GateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name); (self.base/'final.txt').write_text('Reviewed text')
        self.file = {'path':'final.txt','sha256':hashlib.sha256((self.base/'final.txt').read_bytes()).hexdigest()}
        self.m = {'schema_version':1,'run_id':'test','revision':'r1','output_kind':'text','artifact':self.file,
          'required_checks':sorted(BASELINES['text']),
          'checks':[{'id':k,'revision':'r1','artifact_sha256':self.file['sha256'],'status':'PASS','note':'Actual test fixture observation','evidence':[self.file]} for k in BASELINES['text']],
          'expected_visual_units':['text:1'],'visual_units':[{'id':'text:1','revision':'r1','artifact_sha256':self.file['sha256'],'status':'PASS','observation':'Read fixture structure','reviewer':'fixture','evidence':self.file}], 'unresolved_defects':[]}
    def reject(self, change):
        m=copy.deepcopy(self.m);change(m);self.assertTrue(validate(m,self.base))
    def test_complete(self): self.assertEqual(validate(self.m,self.base),[])
    def test_stale_artifact(self):self.reject(lambda m:m['artifact'].update(sha256='stale'))
    def test_missing_check(self):self.reject(lambda m:m['checks'].pop())
    def test_missing_baseline(self):self.reject(lambda m:m.update(required_checks=[]))
    def test_blocked(self):self.reject(lambda m:m['checks'][0].update(status='BLOCKED'))
    def test_untested(self):self.reject(lambda m:m['checks'][0].update(status='NOT TESTED'))
    def test_no_evidence(self):self.reject(lambda m:m['checks'][0].update(evidence=[]))
    def test_wrong_artifact_binding(self):self.reject(lambda m:m['checks'][0].update(artifact_sha256='old'))
    def test_wrong_visual_binding(self):self.reject(lambda m:m['visual_units'][0].update(artifact_sha256='old'))
    def test_stale_revision(self):self.reject(lambda m:m['checks'][0].update(revision='r0'))
    def test_missing_page(self):self.reject(lambda m:m['expected_visual_units'].append('text:2'))
    def test_unreviewed(self):self.reject(lambda m:m['visual_units'][0].update(status='NOT TESTED'))
    def test_no_observation(self):self.reject(lambda m:m['visual_units'][0].update(observation=''))
    def test_missing_screenshot(self):self.reject(lambda m:m['visual_units'][0].update(evidence={'path':'absent.png','sha256':'x'}))
    def test_visual_na_on_app(self):
        def change(m):
            m['output_kind']='app';m['checks'].append({'id':'visual','revision':'r1','artifact_sha256':self.file['sha256'],'status':'NOT APPLICABLE','note':'skip'})
        self.reject(change)
    def test_duplicate_visual(self):self.reject(lambda m:m['visual_units'].append(m['visual_units'][0]))
    def test_defects(self):self.reject(lambda m:m['unresolved_defects'].append({'id':'D1','severity':'major'}))
    def test_bad_payload(self):self.assertTrue(validate([],self.base))
    def test_dataset_na(self):
        m=copy.deepcopy(self.m);m.update(output_kind='dataset',machine_readable_only=True,required_checks=sorted(BASELINES['dataset']),expected_visual_units=[],visual_units=[])
        m['checks']=[{'id':k,'revision':'r1','artifact_sha256':self.file['sha256'],'status':'PASS','note':'fixture','evidence':[self.file]} for k in BASELINES['dataset']]
        next(x for x in m['checks'] if x['id']=='visual').update(status='NOT APPLICABLE',note='CSV only, no preview requested')
        self.assertEqual(validate(m,self.base),[])

if __name__=='__main__':unittest.main()
