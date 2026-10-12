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
 route=data.get('route',{}).get('kind')
 if route not in {'micro','normal','milestone'}: raise ValueError('scope route required')
 directory=file(repo,data['matrix']).parent
 if route=='micro' and (directory/'playbook.md').exists():
  file(repo,str((directory/'playbook.md').relative_to(repo)))
 else:
  if data.get('grill',{}).get('status')!='complete': raise ValueError('completed spec grill required')
  file(repo,data['grill'].get('artifact'))
  file(repo,data.get('atlas',{}).get('path')); file(repo,data.get('change_story',{}).get('path'))
  for name in (['spec.md'] if route=='micro' else ['spec.md','plan.md','tasks.md']): file(repo,str((directory/name).relative_to(repo)))
 requirements(repo,data)
 if data.get('delivery_contract')=='knowledge-v2': knowledge_prework(repo,data)

def playbook_led(repo,data):
 return data.get('delivery_contract') in {'playbook-v1','knowledge-v2'} or (data.get('route',{}).get('kind')=='micro' and (file(repo,data['matrix']).parent/'playbook.md').is_file())

def prework_kinds(repo,data):
 return ['baseline-feedback','phase-contract']+(['research','architecture'] if playbook_led(repo,data) else [])

def prerequisite_receipt(repo,data,kind):
 receipt=data.get('prerequisite_receipts',{}).get(kind,{})
 artifact=file(repo,receipt.get('artifact'))
 if receipt.get('digest')!=digest(artifact): raise ValueError('stale prerequisite '+kind)
 return artifact

def qa_checkout(repo,data,path):
 if not path: raise ValueError('QA requires --checkout')
 p=Path(path).resolve()
 if p==repo.resolve() or p.is_relative_to(repo.resolve()): raise ValueError('checker must use a separate checkout outside the maker repository')
 listed=git(repo,'worktree','list','--porcelain')
 linked='worktree '+str(p)+'\n' in listed+'\n'
 if not linked:
  if not (p/'.git').is_dir() or git(p,'rev-parse','--show-toplevel')!=str(p): raise ValueError('QA checkout must be a standalone clone or registered worktree')
  if (p/'.git'/'objects'/'info'/'alternates').exists(): raise ValueError('QA clone must not borrow maker objects')
 if git(p,'status','--porcelain','--untracked-files=all'): raise ValueError('QA checkout must be clean')
 if git(p,'rev-parse','HEAD')!=data.get('candidate_sha'): raise ValueError('QA checkout must contain latest exact candidate')
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
 if playbook_led(repo,data):
  review=json.loads(prerequisite_receipt(repo,data,'engineering-review').read_text())
  if review.get('candidate_sha')!=data['candidate_sha'] or review.get('checker')!=data.get('checker') or review.get('checker')==data.get('maker'): raise ValueError('engineering review must match exact candidate and independent checker')
  if review.get('status')!='passed' or review.get('blocking_findings')!=[]: raise ValueError('passing engineering review with no blocking findings required')
 if data.get('delivery_contract')=='knowledge-v2': knowledge_release(repo,data)
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
  for kind in prework_kinds(repo,data):
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
 if data.get('delivery_contract')=='knowledge-v2':
  try: knowledge_investigation(repo,data)
  except (ValueError,KeyError,TypeError): return 'investigation'
 if data.get('route',{}).get('kind') not in {'micro','normal','milestone'}: return 'route'
 if data.get('route',{}).get('kind')!='micro' and data.get('grill',{}).get('status')!='complete': return 'spec-grill'
 try: prerequisites(repo,data)
 except ValueError: return 'native-prerequisites'
 if data['state'] in {'planned','maker_running'}:
  for kind in prework_kinds(repo,data):
   receipt=data.get('prerequisite_receipts',{}).get(kind,{})
   try:
    if receipt.get('digest')!=digest(file(repo,receipt.get('artifact'))): return kind
   except ValueError: return kind
 return {'planned':'maker','maker_running':'maker','candidate_ready':'independent-qa','qa_running':'independent-qa','retest_running':'independent-qa','qa_failed':'bug-fixing','bug_fixing':'bug-fixing','ready_for_merge':'merge-readiness'}[data['state']]


# These receipts bind accountable observations; they do not prove unseen agent reasoning.
def knowledge_json(repo,data,kind):
 try:
  value=json.loads(prerequisite_receipt(repo,data,kind).read_text())
 except (json.JSONDecodeError,TypeError) as exc: raise ValueError('invalid '+kind+' receipt') from exc
 if not isinstance(value,dict): raise ValueError(kind+' must be an object')
 return value

def knowledge_evidence(repo,rows):
 if not isinstance(rows,list) or not rows: raise ValueError('nonempty evidence rows required')
 for row in rows:
  if not isinstance(row,dict): raise ValueError('evidence row must be an object')
  artifact=file(repo,row.get('path'))
  if row.get('digest')!=digest(artifact): raise ValueError('knowledge evidence changed')

def knowledge_investigation(repo,data):
 r=knowledge_json(repo,data,'investigation')
 commit(repo,r.get('base_sha'))
 if not all(isinstance(r.get(k),str) and r[k].strip() for k in ['playbook','intent','flow','scope_rationale']): raise ValueError('investigation context incomplete')
 if not isinstance(r.get('unknowns'),list) or not isinstance(r.get('conventions'),list): raise ValueError('unknowns and conventions must be explicit lists')
 if r.get('unresolved_blockers')!=[]: raise ValueError('investigation blockers remain')
 knowledge_evidence(repo,r.get('evidence'))
 if len({x.get('id') for x in r['conventions']})!=len(r['conventions']): raise ValueError('unique convention IDs required')
 for rule in r['conventions']:
  if not all(rule.get(k) for k in ['id','rule','scope','source','plan_application']): raise ValueError('convention needs provenance and plan application')
  file(repo,rule['source'])
  if rule['source'] not in {x['path'] for x in r['evidence']}: raise ValueError('convention source must be digest-bound investigation evidence')
 kit=Path(__file__).resolve().parents[1]
 catalog=json.loads((kit/'adapters/pstack/routes.json').read_text())
 selected=next((x for x in catalog['playbooks'] if x['id']==r['playbook']),None)
 if not selected: raise ValueError('unknown pinned PStack playbook')
 source=kit/'vendor/pstack'/selected['source']
 source_steps=re.findall(r'^(\d+)\. ',source.read_text(),re.MULTILINE)
 if r.get('playbook_digest')!=digest(source): raise ValueError('pinned playbook digest mismatch')
 steps=r.get('steps')
 if not isinstance(steps,list) or not steps or len({x.get('id') for x in steps})!=len(steps): raise ValueError('unique playbook steps required')
 if source_steps and [x.get('source_step') for x in steps]!=source_steps: raise ValueError('ordered pinned playbook step coverage required')
 for step in steps:
  if not step.get('id') or not step.get('source_step'): raise ValueError('playbook source step required')
  if step.get('status') not in {'pending','completed','skipped'}: raise ValueError('invalid playbook step status')
  if step['status']=='completed': knowledge_evidence(repo,step.get('evidence'))
  if step['status']=='skipped' and not step.get('reason'): raise ValueError('skip reason required')
 return r

def knowledge_view(repo,view):
 if not isinstance(view,dict) or view.get('renderer') not in {'archify','mermaid'}: raise ValueError('shared view renderer required')
 for key in ['source','artifact']:
  if view.get(key+'_digest')!=digest(file(repo,view.get(key))): raise ValueError('shared view changed: '+key)
 if view['renderer']=='archify':
  validation=file(repo,view.get('validation_receipt'))
  if view.get('validation_digest')!=digest(validation): raise ValueError('diagram validation receipt changed')
  receipt=json.loads(validation.read_text())
  if not isinstance(receipt,dict) or receipt.get('status')!='passed' or receipt.get('exit_code')!=0: raise ValueError('passing Archify command receipt required')
  if not isinstance(receipt.get('command'),list) or 'finalize' not in receipt['command']: raise ValueError('Archify finalize command required')
  if receipt.get('source_digest')!=view['source_digest'] or receipt.get('artifact_digest')!=view['artifact_digest']: raise ValueError('Archify receipt must bind view bytes')
  raw=file(repo,receipt.get('raw_receipt'))
  if receipt.get('raw_digest')!=digest(raw) or not isinstance(json.loads(raw.read_text()),dict): raise ValueError('Archify machine receipt required')
 elif not view.get('limitation'): raise ValueError('fallback limitation required')

def knowledge_prework(repo,data):
 r=knowledge_investigation(repo,data)
 design=knowledge_json(repo,data,'shared-design')
 if design.get('investigation_digest')!=digest(prerequisite_receipt(repo,data,'investigation')): raise ValueError('design must reflect current investigation')
 if not all(design.get(k) for k in ['observed','proposed','invariants','verification_plan']): raise ValueError('shared design incomplete')
 knowledge_view(repo,design.get('view'))
 return r

def knowledge_release(repo,data):
 r=knowledge_prework(repo,data)
 if any(x['status']=='pending' for x in r['steps']): raise ValueError('unfinished PStack playbook steps')
 result=knowledge_json(repo,data,'shared-result')
 if result.get('candidate_sha')!=data.get('candidate_sha') or result.get('checker')!=data.get('checker'): raise ValueError('shared result must match candidate and checker')
 if result.get('design_digest')!=digest(prerequisite_receipt(repo,data,'shared-design')): raise ValueError('result must reflect current design')
 if result.get('status')!='passed' or not result.get('summary') or not isinstance(result.get('deviations'),list): raise ValueError('verified reconciliation required')
 knowledge_evidence(repo,result.get('evidence')); knowledge_view(repo,result.get('view'))
 conventions=result.get('conventions')
 if not isinstance(conventions,list) or len(conventions)!=len(r['conventions']) or {x.get('id') for x in conventions}!={x['id'] for x in r['conventions']}: raise ValueError('all conventions require reconciliation')
 for rule in conventions:
  if rule.get('status') not in {'preserved','changed'} or not rule.get('reason'): raise ValueError('convention disposition required')
  knowledge_evidence(repo,rule.get('evidence'))
 for bug in data.get('bugs',[]):
  if bug.get('status')!='resolved': raise ValueError('open bugs block release')
  for previous in bug.get('resolution_history',[]):
   if previous.get('digest')!=digest(file(repo,previous.get('artifact'))): raise ValueError('historical bug resolution changed')
  artifact=file(repo,bug.get('resolution'))
  if bug.get('resolution_digest')!=digest(artifact): raise ValueError('bug resolution changed')
  knowledge_bug(repo,data,bug,json.loads(artifact.read_text()))

def knowledge_bug(repo,data,bug,r):
 if not isinstance(r,dict): raise ValueError('bug resolution must be an object')
 if r.get('bug_id')!=bug['id'] or r.get('candidate_sha')!=data.get('candidate_sha') or r.get('checker')!=data.get('checker') or r.get('checker')==data.get('maker'): raise ValueError('bug retest must match exact candidate and independent checker')
 if r.get('status')!='passed' or not all(r.get(k) for k in ['expected','actual','trigger','root_cause','fix','retest']): raise ValueError('verified Bug Story required')
 knowledge_evidence(repo,r.get('evidence')); knowledge_view(repo,r.get('view'))
 regression=r.get('regression',{})
 if regression.get('status')=='covered': knowledge_evidence(repo,regression.get('evidence'))
 elif regression.get('status')!='exception' or not regression.get('reason') or not regression.get('alternative'): raise ValueError('regression coverage or justified alternative required')
 prevention=r.get('prevention',{})
 if prevention.get('status') not in {'encoded','scoped-follow-up','no-broader-lesson'} or not prevention.get('reason') or not prevention.get('scope'): raise ValueError('scoped prevention decision required')
 if prevention['status']=='encoded': knowledge_evidence(repo,prevention.get('evidence'))
 if prevention['status']=='scoped-follow-up': file(repo,prevention.get('artifact'))
