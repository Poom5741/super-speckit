"""Executable state authority. Evidence is local, bounded, and commit-specific."""
import json, os, re, subprocess, tempfile, hashlib
from pathlib import Path

GRAPH = {
 'planned': {'maker_running','blocked'}, 'maker_running': {'candidate_ready','blocked'},
 'candidate_ready': {'qa_running','retest_running','blocked'}, 'qa_running': {'qa_failed','ready_for_merge','blocked'},
 'qa_failed': {'bug_fixing','blocked'}, 'bug_fixing': {'candidate_ready','blocked'},
 'retest_running': {'qa_failed','ready_for_merge','blocked'},
 'ready_for_merge': {'merged','bug_fixing','blocked'}, 'merged': set(),
 'blocked': {'planned','maker_running','qa_running','bug_fixing','retest_running'} }

def git(repo, *args):
 p=subprocess.run(['git','-C',str(repo),*args],text=True,capture_output=True)
 if p.returncode: raise ValueError('Git check failed: '+p.stderr.strip())
 return p.stdout.strip()

def commit(repo, value):
 if not isinstance(value,str) or not re.fullmatch('[0-9a-f]{7,64}',value): raise ValueError('invalid candidate SHA')
 return git(repo,'rev-parse','--verify',value+'^{commit}')

def file(repo, value):
 if not isinstance(value,str) or not value.strip(): raise ValueError('nonempty evidence path required')
 p=(repo/value).resolve()
 if not p.is_relative_to(repo.resolve()) or not p.is_file() or not p.stat().st_size: raise ValueError('evidence must be a nonempty repository file: '+value)
 return p

def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def atomic(path,data):
 path.parent.mkdir(parents=True,exist_ok=True)
 fd,tmp=tempfile.mkstemp(dir=path.parent,prefix='.'+path.name)
 try:
  with os.fdopen(fd,'w') as f: f.write(json.dumps(data,indent=2)+'\n'); f.flush(); os.fsync(f.fileno())
  os.replace(tmp,path)
 finally:
  if os.path.exists(tmp): os.unlink(tmp)

def requirements(repo,data):
 p=file(repo,data['matrix'])
 if p.suffix=='.json':
  obj=json.loads(p.read_text()); ids=obj.get('requirements',[]) if isinstance(obj,dict) else obj
  ids=[x['id'] if isinstance(x,dict) else x for x in ids]
 else: ids=re.findall(r'\b(?:FR|REQ|SC)-[A-Za-z0-9_-]+\b',p.read_text())
 ids=set(ids)
 if not ids or not all(isinstance(x,str) and x for x in ids): raise ValueError('matrix requires explicit nonempty requirement IDs')
 return ids

def prerequisites(repo,data):
 purpose=data.get('purpose',{})
 if purpose.get('status')!='confirmed': raise ValueError('human purpose confirmation required')
 file(repo,purpose.get('map')); decision=json.loads(file(repo,purpose.get('decision')).read_text())
 if decision.get('status')!='confirmed' or not all(decision.get(k) for k in ['confirmed_by','confirmed_at','confirmation']): raise ValueError('purpose decision evidence incomplete')
 if data.get('grill',{}).get('status')!='complete': raise ValueError('completed spec grill required')
 file(repo,data['grill'].get('artifact'))
 route=data.get('route',{}).get('kind')
 if route not in {'micro','normal','milestone'}: raise ValueError('scope route required')
 file(repo,data.get('atlas',{}).get('path')); file(repo,data.get('change_story',{}).get('path'))
 directory=file(repo,data['matrix']).parent
 for name in (['spec.md'] if route=='micro' else ['spec.md','plan.md','tasks.md']): file(repo,str((directory/name).relative_to(repo)))
 requirements(repo,data)

def qa_checkout(repo,data,path):
 if not path: raise ValueError('QA requires --worktree')
 p=Path(path).resolve()
 if p==repo.resolve(): raise ValueError('checker must use a separate worktree')
 listed=git(repo,'worktree','list','--porcelain')
 if 'worktree '+str(p)+'\n' not in listed+'\n': raise ValueError('QA checkout must be a registered worktree')
 if git(p,'status','--porcelain'): raise ValueError('QA worktree must be clean')
 if git(p,'rev-parse','HEAD')!=data.get('candidate_sha'): raise ValueError('QA worktree must contain latest exact candidate')
 if not data.get('checker') or data.get('checker')==data.get('maker'): raise ValueError('independent checker required')
 return str(p)

def configured_gates(repo):
 path=repo/'super-speckit.yml'
 if not path.exists(): return {}
 text=path.read_text()
 try: gates=json.loads(text).get('gates',{})
 except json.JSONDecodeError:
  gates={}; active=False
  for line in text.splitlines():
   if line=='gates:': active=True; continue
   if active and line and not line.startswith((' ','#')): break
   if not active: continue
   match=re.match(r'^  ([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$',line)
   if not match: continue
   value=match.group(2).strip()
   if value.startswith('"'):
    try: value=json.JSONDecoder().raw_decode(value)[0]
    except json.JSONDecodeError: raise ValueError('unsupported gates YAML quoting; use JSON-compatible quoted commands')
   elif value.startswith("'"): value=value[1:value.rfind("'")].replace("''","'")
   else: value=value.split(' #',1)[0].strip()
   gates[match.group(1)]=value
 if not isinstance(gates,dict): raise ValueError('gates configuration must be a mapping')
 return {k:v for k,v in gates.items() if k not in {'app_start','app_url','ocr_review'} and v}

def proof(repo,data,receipt, archived=False):
 if receipt.get('candidate_sha')!=data.get('candidate_sha'): raise ValueError('proof must match latest exact candidate SHA')
 if receipt.get('checker')!=data.get('checker'): raise ValueError('proof checker identity mismatch')
 if not archived: qa_checkout(repo,data,receipt.get('worktree'))
 if receipt.get('attempt_id')!=data.get('qa_attempt'): raise ValueError('stale QA attempt')
 if receipt.get('matrix_digest')!=digest(file(repo,data['matrix'])): raise ValueError('matrix changed since proof')
 environment_file=file(repo,receipt.get('environment'))
 if receipt.get('environment_digest')!=digest(environment_file): raise ValueError('environment receipt changed or unfrozen')
 environment=json.loads(environment_file.read_text())
 if environment.get('candidate_sha')!=data['candidate_sha'] or environment.get('checker')!=data['checker'] or environment.get('attempt_id')!=data.get('qa_attempt'): raise ValueError('environment receipt mismatch')
 if environment.get('worktree')!=receipt.get('worktree'): raise ValueError('environment checkout mismatch')
 rows=receipt.get('requirements',[])
 if len({r.get('id') for r in rows})!=len(rows) or {r.get('id') for r in rows}!=requirements(repo,data): raise ValueError('proof requires exact nonempty matrix coverage')
 gates=receipt.get('gates',[])
 if not gates: raise ValueError('proof requires passing gates')
 names=[g.get('name') for g in gates]
 if len(set(names))!=len(names): raise ValueError('duplicate gates')
 configured=configured_gates(repo)
 if not set(configured).issubset(set(names)): raise ValueError('every configured gate requires proof')
 for gate in gates:
  if gate.get('name') in configured and gate.get('command')!=configured[gate['name']]: raise ValueError('proof command must match configured gate')
 for row in rows:
  if row.get('kind') not in {'runtime','public-behavior'} or not row.get('public_seam'): raise ValueError('requirements require public behavior proof; static review is insufficient')
 for row in rows+gates:
  if row.get('status')!='passed': raise ValueError('all proof rows and gates must pass')
  evidence=file(repo,row.get('evidence'))
  if row.get('evidence_digest')!=digest(evidence): raise ValueError('evidence changed since proof')
 for gate in gates:
  if not gate.get('command') or gate.get('exit_code')!=0: raise ValueError('gate requires command and successful exit code')
 if any(b.get('status')!='resolved' for b in data.get('bugs',[])): raise ValueError('open bugs block release')

def release(repo,data, archived=False):
 prerequisites(repo,data)
 candidates=data.get('candidates',[])
 if not candidates or candidates[-1]['sha']!=data['candidate_sha'] or candidates[-1]['matrix_digest']!=digest(file(repo,data['matrix'])): raise ValueError('candidate matrix is immutable')
 receipt=data.get('proof')
 if not receipt: raise ValueError('independent proof receipt required')
 proof(repo,data,receipt,archived=archived)
 if data.get('ui_change'):
  j=data.get('journey_ux',{})
  if j.get('status')!='passed' or j.get('candidate_sha')!=data.get('candidate_sha'): raise ValueError('latest passing Journey UX required')
  file(repo,j.get('report'))

def merged(repo,data):
 receipt=data.get('merge_receipt',{})
 if receipt.get('candidate_sha')!=data['candidate_sha'] or not receipt.get('authority') or receipt.get('forge_status')!='merged': raise ValueError('observed merge receipt with authority required')
 file(repo,receipt.get('evidence')); base=commit(repo,receipt.get('base_sha')); merge=commit(repo,receipt.get('merged_sha'))
 git(repo,'merge-base','--is-ancestor',data['candidate_sha'],merge)
 git(repo,'merge-base','--is-ancestor',base,merge)

def transition(repo,data,target,sha=None,worktree=None,attempt=None):
 if target not in GRAPH.get(data.get('state'),set()): raise ValueError('illegal state transition: '+str(data.get('state'))+' -> '+target)
 if target not in {'planned','blocked'}: prerequisites(repo,data)
 if target=='candidate_ready' and not sha: raise ValueError('new candidate commit --sha required')
 if target in {'maker_running','candidate_ready'}:
  for kind in ['baseline-feedback','phase-contract']:
   receipt=data.get('prerequisite_receipts',{}).get(kind,{})
   artifact=file(repo,receipt.get('artifact'))
   if receipt.get('digest')!=digest(artifact): raise ValueError('stale prerequisite '+kind)
 if sha:
  if target!='candidate_ready': raise ValueError('only candidate_ready registers a candidate')
  resolved=commit(repo,sha)
  if resolved in [x['sha'] for x in data.get('candidates',[])]: raise ValueError('candidate identity is immutable; register a new commit')
  matrix=file(repo,data['matrix'])
  relative=str(matrix.relative_to(repo))
  result=subprocess.run(['git','-C',str(repo),'show',resolved+':'+relative],capture_output=True)
  if result.returncode or result.stdout!=matrix.read_bytes(): raise ValueError('matrix must be frozen byte-for-byte in candidate commit')
  data.setdefault('candidates',[]).append({'sha':resolved,'maker':data['maker'],'matrix_digest':digest(matrix)})
  data['candidate_sha']=resolved; data.pop('proof',None); data.pop('qa_attempt',None)
 if target in {'candidate_ready','qa_running','retest_running','ready_for_merge','merged'}:
  if commit(repo,data.get('candidate_sha'))!=data['candidate_sha']: raise ValueError('candidate must be resolved full SHA')
 if target in {'qa_running','retest_running'}:
  data['qa_worktree']=qa_checkout(repo,data,worktree)
  if not attempt or attempt in data.get('attempt_history',[]): raise ValueError('new QA --attempt-id required')
  data['qa_attempt']=attempt; data.setdefault('attempt_history',[]).append(attempt)
 if target in {'ready_for_merge','merged'}: release(repo,data)
 if target=='merged': merged(repo,data)
 data['state']=target

def next_stage(repo,data):
 if data['state']=='merged': return 'complete'
 if data['state']=='blocked': return 'recovery'
 if any(b.get('status')!='resolved' for b in data.get('bugs',[])): return 'bug-fixing'
 if data.get('purpose',{}).get('status')!='confirmed': return 'purpose-gate'
 if data.get('grill',{}).get('status')!='complete': return 'spec-grill'
 if data.get('route',{}).get('kind') not in {'micro','normal','milestone'}: return 'route'
 try: prerequisites(repo,data)
 except ValueError: return 'native-prerequisites'
 if data['state'] in {'planned','maker_running'}:
  for kind in ['baseline-feedback','phase-contract']:
   receipt=data.get('prerequisite_receipts',{}).get(kind,{})
   try:
    if receipt.get('digest')!=digest(file(repo,receipt.get('artifact'))): return kind
   except ValueError: return kind
 return {'planned':'maker','maker_running':'maker','candidate_ready':'independent-qa','qa_running':'independent-qa','retest_running':'independent-qa','qa_failed':'bug-fixing','bug_fixing':'bug-fixing','ready_for_merge':'merge-readiness'}[data['state']]
