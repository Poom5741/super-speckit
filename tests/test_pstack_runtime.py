import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('runtime', Path(__file__).parents[1]/'scripts/pstack_runtime.py')
r = importlib.util.module_from_spec(spec); spec.loader.exec_module(r)

class RuntimeTests(unittest.TestCase):
    def test_identical_panel_and_real_diversity(self):
        seats = r.panel('intent', 'diff', 'rubric', 'sha', ['model-a', 'model-b'])
        self.assertEqual(seats[0]['prompt'], seats[1]['prompt'])
        with self.assertRaises(ValueError): r.panel('', '', '', '', ['same', 'same'])

    def test_arena_freezes_and_hides_rubric(self):
        self.assertNotIn('rubric', r.arena_brief('brief', 'base', ['a'])[0])
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'candidate'; p.write_text('one'); frozen=r.freeze_candidate(p)
            other=Path(d)/'other'; other.write_text('alternative'); r.judge([frozen,r.freeze_candidate(other)], 'hidden'); p.write_text('two')
            with self.assertRaises(ValueError): r.judge([frozen,r.freeze_candidate(other)], 'hidden')

    def test_swarm_dropout_retry_wrong_sha_duplicates_and_refill(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'proof'; p.write_text('proof')
            swarm=r.Swarm([dict(id='a', base='sha'), dict(id='b', base='sha'), dict(id='c', base='sha', depends=['a'])], limit=2)
            a,b=swarm.dispatch()
            with self.assertRaises(ValueError): swarm.complete('a', a['attempt'], 'wrong', [str(p)], True)
            swarm.complete('a', a['attempt'], 'sha', [str(p)], True)
            c=swarm.dispatch()[0]; self.assertEqual(c['id'], 'c')
            swarm.complete('b', b['attempt'], 'sha', [], False); self.assertFalse(swarm.covered())
            swarm.retry('b'); retry=swarm.dispatch()[0]
            with self.assertRaises(ValueError): swarm.complete('b', b['attempt'], 'sha', [str(p)], True)
            swarm.complete('b', retry['attempt'], 'sha', [str(p)], True)
            swarm.complete('c', c['attempt'], 'sha', [str(p)], True); self.assertTrue(swarm.covered())
            with self.assertRaises(ValueError): swarm.complete('c', c['attempt'], 'sha', [str(p)], True)

    def test_decisions_detect_fabrication_and_tampering(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'trail'; first=r.append_decision(p, 'run', 'tested', ['actual output'])
            r.append_decision(p, 'run', 'correction', ['invented'], first['id'])
            self.assertEqual(r.audit_decisions(p, 'run', 'actual output')['status'], 'failed')
            rows=p.read_text().splitlines(); item=json.loads(rows[0]); item['claim']='tampered'; rows[0]=json.dumps(item); p.write_text('\n'.join(rows))
            self.assertTrue(any(e.startswith('broken-chain') for e in r.audit_decisions(p, 'run', 'actual output invented')['errors']))

    def test_benchmark_rejects_no_work_and_bad_tuning(self):
        samples=[dict(side='baseline' if i%2==0 else 'candidate', completed=10, errors=0, seconds=2 if i%2==0 else 1) for i in range(10)]
        self.assertEqual(r.benchmark(samples, True, 'CPU profile')['improvement'], .5)
        with self.assertRaises(ValueError): r.benchmark(samples, False, 'CPU')
        samples[0]['completed']=0
        with self.assertRaises(ValueError): r.benchmark(samples, True, 'CPU')

    def recipe(self, wrong=False, broken=False, cleanup_delete=False):
        cmd=lambda code: [sys.executable, '-c', code]
        return dict(build_id='candidate-build',features=['save', 'load'], drive={'save':cmd('pass'), 'load':cmd('raise SystemExit(1)' if broken else 'pass')}, controls={'launch':cmd('pass'), 'doctor':cmd("import json; print(json.dumps(dict(instance='wrong',build_id='wrong',healthy=True)))" if wrong else "import os,json; print(json.dumps(dict(instance=os.environ['PSTACK_INSTANCE'],build_id=os.environ['PSTACK_BUILD_ID'],healthy=True)))"), 'evidence':cmd("import os,pathlib; (pathlib.Path(os.environ['PSTACK_EVIDENCE'])/'proof.txt').write_text('observed')"), 'cleanup':cmd("import os,pathlib; [p.unlink() for p in pathlib.Path(os.environ['PSTACK_EVIDENCE']).glob('*')]" if cleanup_delete else 'pass')})

    def test_live_verification_all_features_wrong_instance_and_cleanup(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(r.verify(self.recipe(), d, Path(d)/'good')['status'], 'controls-passed')
            wrong=r.verify(self.recipe(wrong=True),d,Path(d)/'wrong'); self.assertEqual(wrong['status'],'draft'); self.assertEqual(wrong['controls'][-1]['stage'],'cleanup')
            self.assertIn('regression:load',r.verify(self.recipe(broken=True),d,Path(d)/'broken')['errors'])
            self.assertEqual(r.verify(self.recipe(cleanup_delete=True),d,Path(d)/'deleted')['status'],'draft')
            recipe=self.recipe(); del recipe['drive']['load']
            with self.assertRaises(ValueError): r.verify(recipe,d,Path(d)/'missing')

    def test_automation_idempotency_aliases_ownership_compensation(self):
        event=dict(channel_id='c',thread_ts='t',event_id='e')
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError): r.claim_event(d,event,True,'human')
            self.assertEqual(r.claim_event(d,event,True)['status'],'claimed')
            self.assertEqual(r.claim_event(d,event,True)['status'],'duplicate')
        with self.assertRaises(ValueError): r.normalize_event(dict(event, channel='different'))
        receipts=[dict(action='ticket-create',status='succeeded',id='t'),dict(action='post',status='failed',id='post')]
        self.assertEqual(r.reconcile_writes(receipts)['compensate'],['t'])
        receipts.append(dict(action='ticket-compensate',status='succeeded',id='t'))
        self.assertEqual(r.reconcile_writes(receipts)['status'],'failed-reconciled')

    def test_watcher_statuses_are_independent(self):
        result=r.watcher(dict(status='success',ledger_found=True,verification='failed',mergeable=True,merged=False))
        self.assertTrue(result['ledger_found']); self.assertFalse(result['behavioral_verified']); self.assertFalse(result['merged'])

    def test_panel_preserves_dissent_and_rejects_dropout(self):
        seats=r.panel('intent','diff','rubric','sha',['a','b'])
        receipts=[dict(model=s['model'],input_hash=s['input_hash'],candidate_sha='sha',findings=[dict(id='lone',evidence='line 1',claim='bug')] if s['model']=='a' else []) for s in seats]
        dispositions={'lone':dict(action='Act On',rationale='confirmed')}
        self.assertEqual(len(r.review_panel(seats,receipts,dispositions)['findings']['lone']),1)
        with self.assertRaises(ValueError): r.review_panel(seats,receipts,{})
        with self.assertRaises(ValueError): r.review_panel(seats,receipts[:1],dispositions)

    def test_durable_swarm_retries_bounded_and_cycle_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'swarm.json'; r.swarm_operation(path,'init',dict(units=[dict(id='a',base='sha')]))
            first=r.swarm_operation(path,'dispatch',{})[0]
            r.swarm_operation(path,'complete',dict(unit='a',attempt=first['attempt'],sha='sha',evidence=[],passed=False))
            r.swarm_operation(path,'retry',dict(unit='a'))
            second=r.swarm_operation(path,'dispatch',{})[0]
            r.swarm_operation(path,'complete',dict(unit='a',attempt=second['attempt'],sha='sha',evidence=[],passed=False))
            with self.assertRaises(ValueError): r.swarm_operation(path,'retry',dict(unit='a'))
            self.assertEqual(len(r.swarm_operation(path,'status',{})['units']['a']['history']),2)
        with self.assertRaises(ValueError): r.Swarm([dict(id='a',base='sha',depends=['a'])])

    def test_decision_run_artifact_binding(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); artifact=root/'proof'; artifact.write_text('real'); trail=root/'trail'
            evidence=dict(path=str(artifact),sha256=r.freeze_candidate(artifact)['sha256'],excerpt='observed output')
            r.append_decision(trail,'run','claim shown',[evidence])
            transcript=dict(run='run',text='claim shown because observed output')
            self.assertEqual(r.audit_decisions(trail,'run',transcript,root)['status'],'passed')
            artifact.write_text('changed'); self.assertEqual(r.audit_decisions(trail,'run',transcript,root)['status'],'failed')
            with self.assertRaises(ValueError): r.audit_decisions(trail,'other',transcript,root)

    def test_benny_template_and_substantive_benchmark_workloads(self):
        item=r.normalize_event(dict(source_channel_id='C',message_ts='1.2'))
        self.assertEqual(item['thread'],'1.2'); self.assertEqual(item['event'],'1.2')
        samples=[dict(side='baseline' if i%2==0 else 'candidate', completed=10+i%2, errors=0, seconds=2) for i in range(10)]
        with self.assertRaises(ValueError): r.benchmark(samples,True,'limiter')

    def test_external_write_receipts_are_durable_idempotent_and_conflict_safe(self):
        with tempfile.TemporaryDirectory() as d:
            item=r.claim_event(d,dict(source_channel_id='c',message_ts='t'),True)
            receipt=dict(id='ticket',action='ticket-create',status='succeeded')
            self.assertEqual(r.record_event_receipt(d,item['key'],receipt)['status'],'recorded')
            self.assertEqual(r.record_event_receipt(d,item['key'],receipt)['status'],'duplicate')
            with self.assertRaises(ValueError): r.record_event_receipt(d,item['key'],dict(receipt,status='failed'))
            result=r.record_event_receipt(d,item['key'],dict(id='thread',action='post',status='failed'))
            self.assertEqual(result['event']['reconciliation']['compensate'],['ticket'])

    def test_real_public_service_side_effect_and_regression_survive_cleanup(self):
        import socket
        fixture=Path(__file__).parent/'fixtures/pstack/public_service.py'
        for broken in (False, True):
            with tempfile.TemporaryDirectory() as d:
                with socket.socket() as sock:
                    sock.bind(('127.0.0.1',0)); port=sock.getsockname()[1]
                url='http://127.0.0.1:'+str(port)
                cmd=lambda code: [sys.executable,'-c',code]
                launch="import subprocess,os,pathlib; p=subprocess.Popen("+repr([sys.executable,str(fixture),str(port)]+(['broken'] if broken else []))+",stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); (pathlib.Path(os.environ['PSTACK_EVIDENCE'])/'pid').write_text(str(p.pid))"
                doctor="import urllib.request,time; time.sleep(.15); print(urllib.request.urlopen("+repr(url)+").read().decode())"
                cleanup="import pathlib,os,signal; p=pathlib.Path(os.environ['PSTACK_EVIDENCE'])/'pid'; os.kill(int(p.read_text()),signal.SIGTERM); p.unlink()"
                recipe=dict(build_id='actual-fixture-build',features=['save','load'],probe=dict(kind='http',url=url),observations={'save':dict(url=url,expected={'count':1},changes=['count']),'load':dict(url=url,expected={'count':1},read_only=True)},drive={'save':cmd("import urllib.request; urllib.request.urlopen(urllib.request.Request("+repr(url)+",method='POST')).read()"),'load':cmd("import urllib.request; urllib.request.urlopen("+repr(url)+").read()")},controls={'launch':cmd(launch),'doctor':cmd(doctor),'evidence':cmd('pass'),'cleanup':cmd(cleanup)})
                result=r.verify(recipe,d,Path(d)/'evidence')
                self.assertEqual(result['status'],'draft' if broken else 'verified')
                self.assertTrue((Path(d)/'evidence/observation-0.json').is_file())
                if broken: self.assertIn('unobserved-side-effect:save',result['errors'])
