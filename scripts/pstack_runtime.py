#!/usr/bin/env python3
"""Evidence-producing PStack methods. Receipts never confer delivery authority."""
import argparse
import hashlib
import json
import os
import statistics
import math
from pathlib import Path
import subprocess
import uuid
import urllib.request
import time


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def panel(intent, diff, rubric, sha, models):
    if len(set(models)) < 2:
        raise ValueError('Panel requires actual distinct model identifiers')
    prompt = json.dumps(dict(intent=intent, diff=diff, rubric=rubric, candidate_sha=sha), sort_keys=True)
    return [dict(model=model, prompt=prompt, input_hash=digest(prompt), candidate_sha=sha) for model in models]


def review_panel(seats, receipts, dispositions):
    expected = {s['model']: s for s in seats}
    if len(receipts) != len(expected) or {r['model'] for r in receipts} != set(expected): raise ValueError('Required model dropout')
    findings = {}
    for receipt in receipts:
        seat = expected[receipt['model']]
        if receipt['input_hash'] != seat['input_hash'] or receipt['candidate_sha'] != seat['candidate_sha']: raise ValueError('Review input mismatch')
        for finding in receipt['findings']:
            if not finding.get('id') or not finding.get('evidence'): raise ValueError('Evidence-backed finding required')
            findings.setdefault(finding['id'], []).append(dict(finding, model=receipt['model']))
    if set(dispositions) != set(findings): raise ValueError('Every finding, including lone dissent, needs disposition')
    for value in dispositions.values():
        if value.get('action') not in ('Act On', 'Consider', 'Noted', 'Dismissed') or not value.get('rationale'): raise ValueError('Invalid disposition')
    return dict(findings=findings, dispositions=dispositions, status='reviewed', candidate_sha=seats[0]['candidate_sha'])


def arena_brief(brief, base, candidates):
    return [dict(candidate=c, brief=brief, base=base, input_hash=digest([brief, base])) for c in candidates]


def freeze_candidate(path):
    path = Path(path)
    if not path.is_file():
        raise ValueError('Candidate must be an artifact file')
    return dict(path=str(path.resolve()), sha256=hashlib.sha256(path.read_bytes()).hexdigest())


def judge(frozen, rubric):
    if len(frozen) < 2 or len({item['path'] for item in frozen}) != len(frozen): raise ValueError('Judge requires at least two distinct frozen candidates')
    for item in frozen:
        if freeze_candidate(item['path']) != item:
            raise ValueError('Candidate changed after freeze')
    return dict(candidates=frozen, rubric=rubric, status='awaiting-independent-selection')


class Swarm:
    def __init__(self, units, limit=2, mode='partition', selection='all-required'):
        if mode not in ('partition', 'race', 'mixed') or not selection or limit < 1:
            raise ValueError('Declare mode, selection and positive concurrency')
        self.units = {u['id']: dict(u, status='pending', attempt=None, history=[], retries=0) for u in units}
        if len(self.units) != len(units):
            raise ValueError('Duplicate units')
        self.limit, self.mode, self.selection = limit, mode, selection
        for u in units:
            if any(d not in self.units for d in u.get('depends', [])):
                raise ValueError('Unknown dependency')
        visiting, done = set(), set()
        def visit(key):
            if key in visiting: raise ValueError('Dependency cycle')
            if key in done: return
            visiting.add(key)
            for d in self.units[key].get('depends', []): visit(d)
            visiting.remove(key); done.add(key)
        for key in self.units: visit(key)

    def dispatch(self):
        slots = self.limit - sum(u['status'] == 'running' for u in self.units.values())
        ready = []
        for u in self.units.values():
            if slots and u['status'] == 'pending' and all(self.units[d]['status'] == 'passed' for d in u.get('depends', [])):
                u.update(status='running', attempt=uuid.uuid4().hex)
                ready.append(dict(u)); slots -= 1
        return ready

    def complete(self, unit, attempt, sha, evidence, passed):
        u = self.units[unit]
        if u['status'] != 'running' or u['attempt'] != attempt or sha != u['base']:
            raise ValueError('Stale, duplicate or wrong-base completion')
        if passed and (not evidence or any(not Path(p).is_file() or not Path(p).stat().st_size for p in evidence)):
            raise ValueError('Passing completion needs retained evidence')
        u['history'].append(dict(attempt=attempt, base=sha, passed=passed, evidence=evidence))
        u.update(status='passed' if passed else 'failed', evidence=evidence)

    def retry(self, unit):
        if self.units[unit]['status'] != 'failed': raise ValueError('Only failed units may retry')
        if self.units[unit]['retries'] >= 1: raise ValueError('Recovery exhausted; reassess or block')
        self.units[unit].update(status='pending', attempt=None, retries=self.units[unit]['retries']+1)

    def covered(self):
        return all(u['status'] == 'passed' for u in self.units.values() if u.get('required', True))



def swarm_operation(path, operation, data):
    """Serialize scheduler updates under an advisory lock and atomic replace."""
    import fcntl
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    with Path(str(path)+'.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        if operation == 'init':
            if path.exists(): raise ValueError('Swarm already exists')
            scheduler = Swarm(**data)
        else:
            value = json.loads(path.read_text())
            scheduler = Swarm(list(value['units'].values()), value['limit'], value['mode'], value['selection'])
            scheduler.units = value['units']
        if operation == 'dispatch': result = scheduler.dispatch()
        elif operation == 'complete': scheduler.complete(**data); result = {'coverage_complete': scheduler.covered()}
        elif operation == 'retry': scheduler.retry(**data); result = {'coverage_complete': scheduler.covered()}
        elif operation == 'status': return dict(units=scheduler.units, coverage_complete=scheduler.covered())
        elif operation == 'init': result = {'coverage_complete': scheduler.covered()}
        else: raise ValueError('Unknown scheduler operation')
        value = dict(units=scheduler.units, limit=scheduler.limit, mode=scheduler.mode, selection=scheduler.selection)
        temporary = path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp')
        with temporary.open('w') as stream:
            json.dump(value, stream, indent=2); stream.flush(); os.fsync(stream.fileno())
        temporary.replace(path)
        return result


def append_decision(path, run, claim, evidence, supersedes=None):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('a+') as stream:
        import fcntl
        fcntl.flock(stream, fcntl.LOCK_EX)
        stream.seek(0); rows = [json.loads(line) for line in stream if line.strip()]
        if supersedes and not any(r['id'] == supersedes and r['run'] == run for r in rows):
            raise ValueError('Unknown correction target')
        row = dict(id=uuid.uuid4().hex, run=run, claim=claim, evidence=evidence, supersedes=supersedes, previous=digest(rows[-1]) if rows else None)
        stream.seek(0, 2); stream.write(json.dumps(row, sort_keys=True) + '\n'); stream.flush(); os.fsync(stream.fileno())
    return row


def audit_decisions(path, run, transcript, run_root=None):
    rows = [json.loads(line) for line in Path(path).read_text().splitlines()]
    errors = []
    if isinstance(transcript, dict):
        if transcript.get('run') != run: raise ValueError('Transcript run identity mismatch')
        transcript = transcript['text']
    for i, row in enumerate(rows):
        if row['previous'] != (digest(rows[i-1]) if i else None): errors.append('broken-chain:' + row['id'])
        if row['run'] == run:
            if row['claim'] not in transcript: errors.append('unsupported-claim:' + row['id'])
            for evidence in row['evidence']:
                excerpt = evidence.get('excerpt', '') if isinstance(evidence, dict) else evidence
                if not excerpt or excerpt not in transcript: errors.append('unsupported:' + row['id'])
                if isinstance(evidence, dict):
                    file = Path(evidence['path']).resolve()
                    if not run_root or not file.is_relative_to(Path(run_root).resolve()) or not file.is_file() or not file.stat().st_size:
                        errors.append('invalid-run-artifact:' + row['id'])
                    elif evidence.get('sha256') != hashlib.sha256(file.read_bytes()).hexdigest(): errors.append('artifact-drift:' + row['id'])
            if not row['evidence']: errors.append('unsupported:' + row['id'])
    return dict(status='failed' if errors else 'passed', errors=errors)


def benchmark(samples, equivalent_tuning, limiter):
    if not equivalent_tuning or not limiter or len(samples) < 10:
        raise ValueError('Need equivalent tuning, measured limiter and five alternating samples per side')
    for index, sample in enumerate(samples):
        if sample['side'] != ('baseline' if index % 2 == 0 else 'candidate') or type(sample['completed']) is not int or sample['completed'] <= 0 or type(sample['errors']) is not int or sample['errors'] != 0 or not isinstance(sample['seconds'], (float,int)) or not math.isfinite(sample['seconds']) or sample['seconds'] <= 0:
            raise ValueError('Invalid or non-alternating completed-work sample')
    if len(samples) % 2 or len({s['completed'] for s in samples}) != 1: raise ValueError('Equal completed workloads required')
    means = {side: sum(s['seconds']/s['completed'] for s in samples if s['side'] == side)/sum(s['side'] == side for s in samples) for side in ('baseline', 'candidate')}
    paired = [samples[i]['seconds']/samples[i]['completed'] - samples[i+1]['seconds']/samples[i+1]['completed'] for i in range(0, len(samples), 2)]
    lower = statistics.mean(paired) - 2.776 * statistics.stdev(paired)/(len(paired)**.5)
    return dict(status='valid-measurement', seconds_per_work=means, median={side: statistics.median(s['seconds'] for s in samples if s['side']==side) for side in means}, ranges={side: [min(s['seconds'] for s in samples if s['side']==side), max(s['seconds'] for s in samples if s['side']==side)] for side in means}, improvement=1-means['candidate']/means['baseline'], significant_win=lower > 0, paired_delta_lower_bound=lower)


def command(argv, cwd, env, timeout=30):
    if not isinstance(argv, list) or not argv or any(not isinstance(x, str) for x in argv):
        raise ValueError('Commands must be explicit argv arrays')
    p = subprocess.run(argv, cwd=cwd, env={**os.environ, **env}, capture_output=True, text=True, timeout=timeout)
    return dict(argv=argv, returncode=p.returncode, stdout=p.stdout, stderr=p.stderr)


def verify(recipe, cwd, output):
    """Synchronous launch recipes start their own detached service if needed.

    Every control receives a unique instance token and evidence directory. Doctor
    must interrogate the actual running target and report token/build/health as JSON.
    A self-echo fixture tests the contract only; it cannot certify a product.
    """
    cwd, output = Path(cwd).resolve(), Path(output).resolve()
    output.mkdir(parents=True, exist_ok=False)
    token = uuid.uuid4().hex
    env = dict(PSTACK_INSTANCE=token, PSTACK_EVIDENCE=str(output))
    controls = recipe['controls']; features = recipe['features']
    if not recipe.get('build_id'): raise ValueError('Declare the candidate build identity')
    env['PSTACK_BUILD_ID'] = recipe['build_id']
    if not features or len(features) != len(set(features)): raise ValueError('Declare unique features')
    if set(recipe['drive']) != set(features): raise ValueError('Maintenance requires every declared feature')
    receipts = []; errors = []
    observable = recipe.get('probe', {}).get('kind') == 'http'
    observations = recipe.get('observations', {})
    if observable and set(observations) != set(features): raise ValueError('Every feature requires an independent public seam observation')
    def observe(url):
        with urllib.request.urlopen(url, timeout=3) as response:
            body = json.loads(response.read())
        if body.get('instance') != token or body.get('build_id') != recipe['build_id'] or body.get('healthy') is not True: raise ValueError('Public seam wrong instance/build/health')
        return body
    try:
        for stage in ('launch', 'doctor'):
            r = command(controls[stage], cwd, env); r['stage'] = stage; receipts.append(r)
            if r['returncode']: raise ValueError(stage + ' failed')
            if stage == 'doctor':
                observed = json.loads(r['stdout'])
                if observed.get('instance') != token: raise ValueError('Wrong running instance')
                if observed.get('build_id') != recipe['build_id'] or observed.get('healthy') is not True: raise ValueError('Wrong build or unhealthy instance')
        if observable:
            deadline = time.monotonic()+3
            while True:
                try: observe(recipe['probe']['url']); break
                except OSError:
                    if time.monotonic() >= deadline: raise
                    time.sleep(.05)
        for feature in features:
            before = observe(observations[feature]['url']) if observable else None
            r = command(recipe['drive'][feature], cwd, env); r['stage'] = 'drive'; r['feature'] = feature; receipts.append(r)
            if r['returncode']: errors.append('regression:' + feature)
            if observable:
                assertion = observations[feature]; after = observe(assertion['url'])
                if not assertion.get('expected') or any(after.get(key) != value for key,value in assertion['expected'].items()): errors.append('public-seam-regression:' + feature)
                changes = assertion.get('changes', [])
                if not changes and assertion.get('read_only') is not True: errors.append('missing-side-effect-assertion:' + feature)
                if any(before.get(key) == after.get(key) for key in changes): errors.append('unobserved-side-effect:' + feature)
                (output/('observation-'+str(features.index(feature))+'.json')).write_text(json.dumps(dict(feature=feature,before=before,after=after)))
        r = command(controls['evidence'], cwd, env); r['stage'] = 'evidence'; receipts.append(r)
        if r['returncode']: errors.append('evidence failed')
    except (ValueError, subprocess.TimeoutExpired, OSError) as exc:
        errors.append(str(exc))
    finally:
        try:
            r = command(controls['cleanup'], cwd, env); r['stage'] = 'cleanup'; receipts.append(r)
            if r['returncode']: errors.append('cleanup failed')
        except (KeyError, subprocess.TimeoutExpired, OSError, ValueError) as exc: errors.append('cleanup:' + str(exc))
    artifacts = [p for p in output.rglob('*') if p.is_file() and p.stat().st_size]
    if not artifacts: errors.append('No evidence survived cleanup')
    output.mkdir(parents=True, exist_ok=True)
    result = dict(status='draft' if errors else ('verified' if observable else 'controls-passed'), build_id=recipe['build_id'], instance=token, errors=errors, controls=receipts, features=features, artifacts=[freeze_candidate(p) for p in artifacts])
    (output/'receipt.json').write_text(json.dumps(result, indent=2)+'\n')
    return result


def normalize_event(event):
    aliases = {'channel': ('channel', 'channel_id', 'source_channel_id'), 'thread': ('thread', 'thread_ts', 'parent_ts', 'source_thread_ts'), 'event': ('event', 'event_id')}
    event = dict(event)
    if not any(event.get(k) for k in aliases['thread']): event['thread'] = event.get('message_ts')
    if not any(event.get(k) for k in aliases['event']): event['event'] = event.get('message_ts')
    normalized = {}
    for key, names in aliases.items():
        values = {str(event[n]) for n in names if event.get(n)}
        if len(values) != 1: raise ValueError('Missing or conflicting ' + key)
        normalized[key] = values.pop()
    normalized['key'] = digest(normalized)
    return normalized


def claim_event(directory, event, trusted=False, owner=None):
    if not trusted or owner: raise ValueError('Untrusted triage or existing human ownership')
    item = normalize_event(event); directory = Path(directory); directory.mkdir(parents=True, exist_ok=True)
    try:
        with (directory/(item['key']+'.json')).open('x') as f: json.dump(dict(item, receipts=[], status='claimed'), f)
    except FileExistsError: return dict(item, status='duplicate')
    return dict(item, status='claimed')



def record_event_receipt(directory, key, receipt):
    """Retain external-write outcomes without executing external actions."""
    import fcntl
    if not receipt.get('id') or receipt.get('status') not in ('succeeded', 'failed') or not receipt.get('action'):
        raise ValueError('Receipt requires external identity, action and terminal outcome')
    if len(key) != 64 or any(c not in '0123456789abcdef' for c in key): raise ValueError('Invalid event identity')
    path = Path(directory)/(key+'.json')
    with Path(str(path)+'.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        event = json.loads(path.read_text())
        for previous in event['receipts']:
            if previous['id'] == receipt['id'] and previous['action'] == receipt['action']:
                if previous != receipt: raise ValueError('Conflicting external-write receipt')
                return dict(status='duplicate', event=event)
        event['receipts'].append(receipt)
        event['reconciliation'] = reconcile_writes(event['receipts'])
        temporary = path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp')
        with temporary.open('w') as stream:
            json.dump(event, stream, indent=2); stream.flush(); os.fsync(stream.fileno())
        temporary.replace(path)
        return dict(status='recorded', event=event)


def reconcile_writes(receipts):
    created = [r['id'] for r in receipts if r['action'] == 'ticket-create' and r['status'] == 'succeeded']
    failed = any(r['status'] == 'failed' for r in receipts)
    compensated = {r['id'] for r in receipts if r['action'] == 'ticket-compensate' and r['status'] == 'succeeded'}
    return dict(status='needs-compensation' if failed and set(created)-compensated else ('failed-reconciled' if failed else 'complete'), compensate=sorted(set(created)-compensated) if failed else [])


def watcher(payload):
    return dict(watcher_status=payload.get('status', 'unknown'), ledger_found=payload.get('ledger_found') is True, behavioral_verified=payload.get('verification') == 'passed', mergeable=payload.get('mergeable') is True, merged=payload.get('merged') is True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation', choices=['panel', 'review-panel', 'arena', 'freeze', 'judge', 'swarm', 'decision', 'benchmark', 'verify', 'watcher', 'normalize-event', 'claim-event', 'event-receipt', 'reconcile-writes', 'audit'])
    parser.add_argument('--input', required=True, help='JSON request file')
    args = parser.parse_args(); data = json.loads(Path(args.input).read_text())
    handlers = {'panel': lambda: panel(**data), 'review-panel': lambda: review_panel(**data), 'arena': lambda: arena_brief(**data), 'freeze': lambda: freeze_candidate(**data), 'judge': lambda: judge(**data), 'swarm': lambda: swarm_operation(**data), 'decision': lambda: append_decision(**data), 'claim-event': lambda: claim_event(**data), 'event-receipt': lambda: record_event_receipt(**data), 'reconcile-writes': lambda: reconcile_writes(**data), 'benchmark': lambda: benchmark(**data), 'verify': lambda: verify(**data), 'watcher': lambda: watcher(data), 'normalize-event': lambda: normalize_event(data), 'audit': lambda: audit_decisions(**data)}
    try:
        result = handlers[args.operation](); print(json.dumps(result, indent=2))
        if args.operation == 'verify' and result['status'] != 'verified': raise SystemExit(1)
        if args.operation == 'audit' and result['status'] != 'passed': raise SystemExit(1)
    except (ValueError, KeyError, OSError) as exc: parser.exit(1, str(exc)+'\n')

if __name__ == '__main__': main()
