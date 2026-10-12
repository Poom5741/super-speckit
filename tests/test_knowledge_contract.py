"""Evidence-backed gates exercised against real Git and the public state CLI."""
import copy
import json
from pathlib import Path
import re
import unittest
import test_state_contract as fixtures
import state_contract as c

class KnowledgeTests(unittest.TestCase):
 def setUp(self):
  self.fixture=fixtures.StateTests('test_paths_and_selector'); self.fixture.setUp()
  self.repo=self.fixture.repo; self.sha=self.fixture.sha
  self.data=json.loads((self.repo/'.super-speckit/state/features/F.json').read_text())
  self.data['delivery_contract']='knowledge-v2'
  self.evidence=[{'path':'log.txt','digest':c.digest(self.repo/'log.txt')}]
  self.view={'renderer':'mermaid','source':'log.txt','source_digest':c.digest(self.repo/'log.txt'),'artifact':'log.txt','artifact_digest':c.digest(self.repo/'log.txt'),'limitation':'Archify unavailable in fixture'}
  self.investigation={'base_sha':self.sha,'playbook':'feature','intent':'Add CSV export','flow':'CLI uses existing export service','scope_rationale':'Established local boundary','unknowns':[],'unresolved_blockers':[],'conventions':[{'id':'C1','rule':'Use existing service','scope':'CSV export','source':'log.txt','plan_application':'Reuse export service'}],'evidence':self.evidence,'steps':[{'id':'S1','source_step':'Investigate callers','status':'completed','evidence':self.evidence},{'id':'S2','source_step':'Implement and verify','status':'pending'}]}
  source=Path(c.__file__).resolve().parents[1]/'vendor/pstack/skills/poteto-mode/playbooks/feature.md'
  self.investigation['playbook_digest']=c.digest(source)
  numbers=re.findall(r'^(\d+)\. ',source.read_text(),re.MULTILINE)
  self.investigation['steps'][0]['source_step']=numbers[0]
  self.investigation['steps'][1]['source_step']=numbers[1]
  self.investigation['steps'] += [{'id':'S'+n,'source_step':n,'status':'skipped','reason':'Fixture exercises receipt gates only'} for n in numbers[2:]]
  self.record('investigation',self.investigation)
  self.design={'investigation_digest':c.digest(self.repo/'investigation.json'),'observed':'Existing export service','proposed':'CSV adapter','invariants':['Single export owner'],'verification_plan':['CLI export roundtrip'],'view':self.view}
  self.record('shared-design',self.design)
 def tearDown(self): self.fixture.tearDown()
 def record(self,kind,value):
  p=self.repo/(kind+'.json');p.write_text(json.dumps(value))
  self.data.setdefault('prerequisite_receipts',{})[kind]={'artifact':p.name,'digest':c.digest(p)}
 def save(self):
  c.atomic(self.repo/'.super-speckit/state/features/F.json',self.data)
  self.fixture.ok('init')
 def result(self):
  self.investigation['steps'][1].update(status='completed',evidence=self.evidence)
  self.record('investigation',self.investigation)
  self.design['investigation_digest']=c.digest(self.repo/'investigation.json');self.record('shared-design',self.design)
  self.data['candidate_sha']=self.sha
  self.record('shared-result',{'candidate_sha':self.sha,'checker':'checker','design_digest':c.digest(self.repo/'shared-design.json'),'status':'passed','summary':'CSV verified','deviations':[],'conventions':[{'id':'C1','status':'preserved','reason':'Existing service reused','evidence':self.evidence}],'evidence':self.evidence,'view':self.view})
 def bug(self):
  return {'bug_id':'B1','candidate_sha':self.sha,'checker':'checker','status':'passed','expected':'One order','actual':'Two orders','trigger':'Repeated payment','root_cause':'Missing operation identity','fix':'Unique operation key','retest':'Original duplicate requests produce one order','evidence':self.evidence,'view':self.view,'regression':{'status':'covered','evidence':self.evidence},'prevention':{'status':'encoded','reason':'Reject repeated operation creation','scope':'Payment operations','evidence':self.evidence}}
 def test_investigation_precedes_route_and_pending_execution_blocks_completion(self):
  self.data['prerequisite_receipts'].pop('investigation'); self.save()
  self.assertNotEqual(self.fixture.invoke('route','F','micro','--rationale','Small feature').returncode,0)
  self.assertEqual(json.loads(self.fixture.ok('next-stage','F').stdout)['next_stage'],'investigation')
  self.record('investigation',self.investigation); self.save()
  self.fixture.ok('route','F','micro','--rationale','Investigated small feature')
  c.knowledge_prework(self.repo,self.data)
  with self.assertRaisesRegex(ValueError,'unfinished'):c.knowledge_release(self.repo,self.data)
 def test_shared_result_binds_conventions_candidate_and_renderer_bytes(self):
  self.result();c.knowledge_release(self.repo,self.data)
  p=self.repo/'shared-result.json';r=json.loads(p.read_text())
  for patch in [{'candidate_sha':'bad'},{'checker':'maker'},{'conventions':[]},{'design_digest':'bad'}]:
   self.record('shared-result',{**r,**patch})
   with self.assertRaises(ValueError):c.knowledge_release(self.repo,self.data)
  self.record('shared-result',r)
  (self.repo/'log.txt').write_text('Changed view and evidence')
  with self.assertRaises(ValueError):c.knowledge_release(self.repo,self.data)
 def test_bug_resolution_rejects_maker_wrong_candidate_missing_prevention(self):
  self.data['candidate_sha']=self.sha
  for patch in [{'checker':'maker'},{'candidate_sha':'bad'},{'prevention':{}},{'root_cause':''},{'regression':{}}]:
   with self.assertRaises(ValueError):c.knowledge_bug(self.repo,self.data,{'id':'B1'},{**self.bug(),**patch})
  c.knowledge_bug(self.repo,self.data,{'id':'B1'},self.bug())
 def test_public_bug_command_and_release_recheck_resolution(self):
  self.result();self.save()
  self.fixture.ok('record-bug','F','B1','--evidence','log.txt')
  (self.repo/'resolution.json').write_text(json.dumps({**self.bug(),'checker':'maker'}))
  self.assertNotEqual(self.fixture.invoke('resolve-bug','F','B1','--evidence','resolution.json').returncode,0)
  (self.repo/'resolution.json').write_text(json.dumps(self.bug()))
  self.fixture.ok('resolve-bug','F','B1','--evidence','resolution.json')
  self.data=json.loads((self.repo/'.super-speckit/state/features/F.json').read_text())
  c.knowledge_release(self.repo,self.data)
  self.fixture.ok('resolve-bug','F','B1','--evidence','resolution.json')
  self.data['candidate_sha']='f'*40
  with self.assertRaises(ValueError):c.knowledge_release(self.repo,self.data)
 def test_full_compact_feature_release_through_public_cli(self):
  self.save()
  self.fixture.ok('route','F','micro','--rationale','Established export boundary')
  (self.repo/'playbook.md').write_text('CSV export through existing service. FR-001. Investigate, implement, verify.')
  for kind in ['research','architecture']: self.fixture.ok('record-prerequisite','F',kind,'--artifact','log.txt')
  self.fixture.candidate();self.fixture.qa_start();self.fixture.receipt()
  self.fixture.ok('record-proof','F','--receipt','proof.json')
  review={'candidate_sha':self.sha,'checker':'checker','status':'passed','blocking_findings':[],'evidence':'log.txt'}
  (self.repo/'review.json').write_text(json.dumps(review))
  self.fixture.ok('record-prerequisite','F','engineering-review','--artifact','review.json')
  self.assertNotEqual(self.fixture.invoke('transition','F','ready_for_merge').returncode,0)
  self.data=json.loads((self.repo/'.super-speckit/state/features/F.json').read_text())
  self.result();self.save()
  self.fixture.ok('transition','F','ready_for_merge');self.fixture.ok('validate')
 def test_invented_or_incomplete_playbook_rejected(self):
  for patch in [{'playbook':'invented'},{'playbook_digest':'bad'},{'steps':self.investigation['steps'][:1]}]:
   self.record('investigation',{**self.investigation,**patch})
   with self.assertRaises(ValueError): c.knowledge_investigation(self.repo,self.data)
 def test_skip_requires_reason_and_archify_requires_bound_validation(self):
  self.investigation['steps'][1]['status']='skipped';self.record('investigation',self.investigation)
  with self.assertRaises(ValueError):c.knowledge_investigation(self.repo,self.data)
  self.investigation['steps'][1]['reason']='No implementation for research-only slice';self.record('investigation',self.investigation)
  c.knowledge_investigation(self.repo,self.data)
  v={**self.view,'renderer':'archify'}
  with self.assertRaises(ValueError):c.knowledge_view(self.repo,v)
  (self.repo/'raw.json').write_text('{}')
  receipt={'status':'passed','exit_code':0,'command':['node','archify.mjs','finalize'],'source_digest':v['source_digest'],'artifact_digest':v['artifact_digest'],'raw_receipt':'raw.json','raw_digest':c.digest(self.repo/'raw.json')}
  (self.repo/'diagram-validation.json').write_text(json.dumps(receipt))
  v.update(validation_receipt='diagram-validation.json',validation_digest=c.digest(self.repo/'diagram-validation.json'));c.knowledge_view(self.repo,v)
  v.update(validation_receipt='log.txt',validation_digest=c.digest(self.repo/'log.txt'))
  with self.assertRaises(ValueError):c.knowledge_view(self.repo,v)

if __name__=='__main__': unittest.main()
