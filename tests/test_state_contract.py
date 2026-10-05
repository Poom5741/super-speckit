import json, subprocess, tempfile, unittest, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/'scripts'))
import state_contract as c
SCRIPT=Path(__file__).parents[1]/'scripts/super_speckit.py'

class StateTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory(); self.repo=Path(self.tmp.name)/'repo'; self.repo.mkdir()
  self.run_git('init'); self.run_git('config','user.email','test@example.com'); self.run_git('config','user.name','Test')
  (self.repo/'.gitignore').write_text('.super-speckit/\n')
  for name in ['spec.md','plan.md','tasks.md','grill.md','log.txt']:(self.repo/name).write_text('real artifact\n')
  (self.repo/'matrix.json').write_text(json.dumps({'requirements':[{'id':'FR-001'}]}))
  self.run_git('add','.');self.run_git('commit','-m','candidate'); self.sha=self.run_git('rev-parse','HEAD')
  self.ok('init');self.ok('create-feature','F','--maker','maker','--checker','checker','--matrix','matrix.json')
  self.ok('purpose-gate','F','--title','Test','--outcome','Behavior','--people','Developers','--success','Pass','--non-goals','None')
  self.ok('confirm-purpose','F','--decision','confirmed','--confirmed-by','user','--confirmed-at','2026-10-06T00:00:00Z','--confirmation','Implement approved plan')
  self.ok('record-grill','F','--artifact','grill.md');self.ok('route','F','normal','--rationale','Contract');self.ok('atlas-init','F','--summary','Contract')
  self.ok('record-prerequisite','F','baseline-feedback','--artifact','log.txt');self.ok('record-prerequisite','F','phase-contract','--artifact','tasks.md')
  self.qa=Path(self.tmp.name)/'qa'
 def tearDown(self): self.tmp.cleanup()
 def run_git(self,*args):return subprocess.check_output(['git','-C',str(self.repo),*args],stderr=subprocess.DEVNULL,text=True).strip()
 def invoke(self,*args):return subprocess.run([sys.executable,str(SCRIPT),*args,'--repo',str(self.repo)],capture_output=True,text=True)
 def ok(self,*args):
  result=self.invoke(*args);self.assertEqual(result.returncode,0,result.stderr);return result
 def candidate(self):self.ok('transition','F','maker_running');self.ok('transition','F','candidate_ready','--sha',self.sha)
 def qa_start(self):
  self.run_git('worktree','add','--detach',str(self.qa),self.sha)
  self.ok('transition','F','qa_running','--worktree',str(self.qa),'--attempt-id','A1')
 def receipt(self):
  receipt={'candidate_sha':self.sha,'checker':'checker','worktree':str(self.qa),'attempt_id':'A1','requirements':[{'id':'FR-001','status':'passed','evidence':'log.txt','kind':'public-behavior','public_seam':'CLI'}],'gates':[{'name':'runtime','status':'passed','evidence':'log.txt'}]}
  environment={k:receipt[k] for k in ['candidate_sha','checker','worktree','attempt_id']}
  (self.repo/'environment.json').write_text(json.dumps(environment))
  receipt.update(environment='environment.json',matrix_digest=c.digest(self.repo/'matrix.json'))
  for row in receipt['requirements']+receipt['gates']:row['evidence_digest']=c.digest(self.repo/row['evidence'])
  receipt['gates'][0].update(command=['python3','-m','unittest'],exit_code=0)
  (self.repo/'proof.json').write_text(json.dumps(receipt)); return receipt
 def test_real_feature_release_and_cas(self):
  self.candidate();self.qa_start();self.receipt();self.ok('record-proof','F','--receipt','proof.json');self.ok('transition','F','ready_for_merge')
  self.assertNotEqual(self.invoke('route','F','normal','--rationale','stale','--expected-revision','1').returncode,0)
  self.ok('validate')
 def test_fabricated_commit_and_illegal_release(self):
  self.assertNotEqual(self.invoke('transition','F','candidate_ready','--sha',self.sha).returncode,0)
  self.ok('transition','F','maker_running')
  self.assertNotEqual(self.invoke('transition','F','candidate_ready','--sha','abcdef1').returncode,0)
 def test_bug_fix_new_candidate_retest(self):
  self.candidate();self.qa_start();self.ok('record-bug','F','B1','--evidence','log.txt');self.ok('transition','F','qa_failed');self.ok('transition','F','bug_fixing')
  (self.repo/'implementation.txt').write_text('fixed public behavior');self.run_git('add','implementation.txt');self.run_git('commit','-m','fix');self.sha=self.run_git('rev-parse','HEAD')
  self.ok('transition','F','candidate_ready','--sha',self.sha)
  subprocess.check_call(['git','-C',str(self.qa),'checkout','--detach',self.sha],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
  self.ok('resolve-bug','F','B1','--evidence','log.txt');self.ok('transition','F','qa_running','--worktree',str(self.qa),'--attempt-id','A2')
  receipt=self.receipt();receipt['attempt_id']='A2';(self.repo/'environment.json').write_text(json.dumps({k:receipt[k] for k in ['candidate_sha','checker','worktree','attempt_id']}));(self.repo/'proof.json').write_text(json.dumps(receipt))
  self.ok('record-proof','F','--receipt','proof.json');self.ok('transition','F','ready_for_merge')
 def test_dirty_checkout_open_bug_stale_and_empty_proof(self):
  self.candidate();self.qa_start(); receipt=self.receipt()
  (self.qa/'dirty.txt').write_text('dirty')
  self.assertNotEqual(self.invoke('record-proof','F','--receipt','proof.json').returncode,0);(self.qa/'dirty.txt').unlink()
  for patch in [{'attempt_id':'stale'},{'candidate_sha':'abcdef1'},{'requirements':[]},{'gates':[]},{'checker':'maker'}]:
   (self.repo/'proof.json').write_text(json.dumps({**receipt,**patch}));self.assertNotEqual(self.invoke('record-proof','F','--receipt','proof.json').returncode,0)
  self.ok('record-bug','F','B','--evidence','log.txt');(self.repo/'proof.json').write_text(json.dumps(receipt));self.assertNotEqual(self.invoke('record-proof','F','--receipt','proof.json').returncode,0)
 def test_paths_and_selector(self):
  for path in [None,'','.','../','/etc/passwd']:
   with self.assertRaises(ValueError):c.file(self.repo,path)
  self.candidate();self.assertEqual(json.loads(self.ok('next-stage','F').stdout)['next_stage'],'independent-qa')
 def test_immutable_candidate_and_duplicate_receipt(self):
  self.candidate();self.qa_start();self.receipt();self.ok('record-proof','F','--receipt','proof.json')
  self.assertNotEqual(self.invoke('record-proof','F','--receipt','proof.json').returncode,0)
  self.ok('transition','F','qa_failed');self.ok('transition','F','bug_fixing')
  self.assertNotEqual(self.invoke('transition','F','candidate_ready','--sha',self.sha).returncode,0)
 def test_required_gates_and_static_proof_rejected(self):
  self.candidate();self.qa_start();receipt=self.receipt()
  (self.repo/'super-speckit.yml').write_text('gates:\n  unit: "python3 -m unittest"\n  app_start: "python3 server.py"\n  app_url: "http://localhost"\n')
  self.assertNotEqual(self.invoke('record-proof','F','--receipt','proof.json').returncode,0)
  receipt['gates'][0].update(name='unit',command='python3 -m unittest')
  receipt['requirements'][0]['kind']='static'
  (self.repo/'proof.json').write_text(json.dumps(receipt));self.assertNotEqual(self.invoke('record-proof','F','--receipt','proof.json').returncode,0)
  receipt['requirements'][0]['kind']='public-behavior';(self.repo/'proof.json').write_text(json.dumps(receipt));self.ok('record-proof','F','--receipt','proof.json')
 def test_proof_drift_blocks_release(self):
  self.candidate();self.qa_start();self.receipt();self.ok('record-proof','F','--receipt','proof.json')
  (self.repo/'log.txt').write_text('replaced evidence')
  self.assertNotEqual(self.invoke('transition','F','ready_for_merge').returncode,0)
 def test_missing_prerequisite_and_matrix_drift(self):
  (self.repo/'plan.md').unlink();self.assertNotEqual(self.invoke('transition','F','maker_running').returncode,0)
  (self.repo/'plan.md').write_text('real artifact\n');self.candidate()
  (self.repo/'matrix.json').write_text(json.dumps({'requirements':[{'id':'FR-002'}]}))
  self.assertNotEqual(self.invoke('validate').returncode,0)
 def test_atomic_compare_and_swap(self):
  revision=json.loads((self.repo/'.super-speckit/state/features/F.json').read_text())['revision']
  args=[sys.executable,str(SCRIPT),'route','F','normal','--rationale','race','--repo',str(self.repo),'--expected-revision',str(revision)]
  processes=[subprocess.Popen(args,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True) for _ in range(2)]
  for process in processes:process.communicate()
  self.assertEqual(sorted(p.returncode for p in processes),[0,2])
 def test_migration_preserves_untrusted_legacy_backup(self):
  path=self.repo/'.super-speckit/state/features/F.json';data=json.loads(path.read_text());data.pop('schema_version');data['state']='ready_for_merge';data['candidate_sha']='abcdef1';path.write_text(json.dumps(data))
  self.ok('migrate-state'); migrated=json.loads(path.read_text())
  self.assertEqual(migrated['state'],'blocked');self.assertIsNone(migrated['candidate_sha'])
  self.assertTrue((self.repo/'.super-speckit/state/migration-backups/F.json').exists());self.ok('validate')
 def test_canonical_environment_cannot_be_replaced_or_unfrozen(self):
  self.candidate();self.qa_start();self.receipt();self.ok('record-proof','F','--receipt','proof.json')
  path=self.repo/'.super-speckit/state/features/F.json';data=json.loads(path.read_text())
  environment=self.repo/'environment.json';environment.write_text(environment.read_text()+'\n')
  with self.assertRaises(ValueError):c.proof(self.repo,data,data['proof'])
  data['proof'].pop('environment_digest')
  with self.assertRaises(ValueError):c.proof(self.repo,data,data['proof'])
 def test_maker_requires_prework_receipts_and_safe_feature_ids(self):
  state=self.repo/'.super-speckit/state/features/F.json';data=json.loads(state.read_text());data['prerequisite_receipts']={};state.write_text(json.dumps(data))
  self.assertEqual(json.loads(self.ok('next-stage','F').stdout)['next_stage'],'baseline-feedback')
  self.assertNotEqual(self.invoke('transition','F','maker_running').returncode,0)
  self.ok('record-prerequisite','F','baseline-feedback','--artifact','log.txt')
  self.assertEqual(json.loads(self.ok('next-stage','F').stdout)['next_stage'],'phase-contract')
  self.assertNotEqual(self.invoke('transition','F','maker_running').returncode,0)
  self.assertNotEqual(self.invoke('design-first','../escape','--title','Escape','--summary','Invalid').returncode,0)
  self.assertFalse((self.repo/'.super-speckit/escape').exists())
 def test_merged_record_survives_qa_worktree_cleanup(self):
  base=self.sha;main=self.run_git('branch','--show-current');self.run_git('checkout','-b','feature')
  (self.repo/'merge-feature.txt').write_text('behavior');self.run_git('add','merge-feature.txt');self.run_git('commit','-m','feature');self.sha=self.run_git('rev-parse','HEAD')
  self.candidate();self.qa_start();self.receipt();self.ok('record-proof','F','--receipt','proof.json');self.ok('transition','F','ready_for_merge')
  self.run_git('checkout',main);self.run_git('merge','--no-ff','feature','-m','observed merge');merged_sha=self.run_git('rev-parse','HEAD')
  merge={'candidate_sha':self.sha,'authority':'user approved merge','forge_status':'merged','base_sha':base,'merged_sha':merged_sha,'evidence':'log.txt'}
  (self.repo/'merge.json').write_text(json.dumps(merge));self.ok('record-merge','F','--receipt','merge.json');self.ok('transition','F','merged')
  self.run_git('worktree','remove',str(self.qa));self.ok('validate')
  (self.repo/'environment.json').write_text('changed')
  self.assertNotEqual(self.invoke('validate').returncode,0)
if __name__=='__main__':unittest.main()
