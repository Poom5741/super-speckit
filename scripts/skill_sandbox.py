#!/usr/bin/env python3
"""Run small pure-Pi skill comparisons and check frozen outputs independently."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import uuid

ROOT = Path(__file__).resolve().parents[1]
RUNNER_HASH = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
RUNS = ROOT / '.skill-sandbox' / 'runs'
SKILLS = ROOT / 'experiments' / 'skill-sandbox' / 'skills'
PROFILES = {'pstack': 'pi-small-task-pstack', 'superspeckit': 'pi-small-task-superspeckit'}

APP = '''import argparse, json
from pathlib import Path

def load(path):
    return json.loads(path.read_text()) if path.exists() else []

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--store', required=True, type=Path)
    commands = parser.add_subparsers(dest='command', required=True)
    add = commands.add_parser('add')
    add.add_argument('id')
    add.add_argument('text')
    commands.add_parser('list')
    args = parser.parse_args()
    rows = load(args.store)
    if args.command == 'add':
        if any(row['id'] == args.id for row in rows):
            parser.error('duplicate id')
        rows.append({'id': args.id, 'text': args.text})
        args.store.parent.mkdir(parents=True, exist_ok=True)
        args.store.write_text(json.dumps(rows, ensure_ascii=False))
    print(json.dumps(rows, ensure_ascii=False))

if __name__ == '__main__':
    main()
'''

BROKEN = '''import argparse, csv, json
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--store', required=True, type=Path)
    commands = parser.add_subparsers(dest='command', required=True)
    add = commands.add_parser('add')
    add.add_argument('id')
    add.add_argument('text')
    commands.add_parser('list')
    imp = commands.add_parser('import')
    imp.add_argument('csv_path', type=Path)
    imp.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    rows = json.loads(args.store.read_text()) if args.store.exists() else []
    if args.command == 'add':
        if any(row['id'] == args.id for row in rows):
            parser.error('duplicate id')
        rows.append({'id': args.id, 'text': args.text})
    elif args.command == 'import':
        with args.csv_path.open(newline='') as stream:
            incoming = list(csv.DictReader(stream))
        rows.extend(incoming)
        args.store.parent.mkdir(parents=True, exist_ok=True)
        args.store.write_text(json.dumps(rows, ensure_ascii=False))
        print(json.dumps({'added': len(incoming), 'skipped': 0}))
        return
    if args.command == 'add':
        args.store.parent.mkdir(parents=True, exist_ok=True)
        args.store.write_text(json.dumps(rows, ensure_ascii=False))
    print(json.dumps(rows, ensure_ascii=False))

if __name__ == '__main__':
    main()
'''

REQUIREMENTS = '''Required interface: python3 notes.py --store PATH import CSV_PATH [--dry-run].
CSV has required id,text columns. Trim id whitespace; keep text unchanged, including
Unicode and quoted commas/newlines. Blank id or blank/whitespace-only text is invalid.
Skip IDs already in the store and repeated IDs within the CSV. The first valid new
row for an ID wins. Return JSON {"added": N, "skipped": N} on stdout.
Reimporting the same CSV adds zero rows. --dry-run reports the same counts but must
not change existing store bytes or create a missing store or its parent directory.
Validate the entire CSV before writing: invalid rows or missing required columns
must exit nonzero and leave the store unchanged, without partially adding valid rows.
Keep the existing add and list commands working. Use Python's standard library.
Add executable checks and briefly report the actual verification and remaining gaps.
'''


def brief(case):
    action = ('Add a CSV import feature to this tiny local notes CLI.' if case == 'import'
              else 'Repair the existing CSV importer in this tiny local notes CLI. Users report duplicate records and dry runs that modify their data.')
    return action + '\n\n' + REQUIREMENTS + '''
Work only inside this fixture. No external service, package install, delegation,
or interactive user is available. You have at most 20 minutes. Keep the change small.
'''


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


def hashes(path):
    result = {}
    for p in sorted(path.rglob('*')):
        if '__pycache__' in p.parts:
            continue
        if p.is_symlink():
            result[str(p.relative_to(path))] = 'symlink:' + hashlib.sha256(os.readlink(p).encode()).hexdigest()
        elif p.is_file():
            result[str(p.relative_to(path))] = hashlib.sha256(p.read_bytes()).hexdigest()
    return result


def seed(path, case):
    path.mkdir(parents=True, exist_ok=True)
    (path / 'notes.py').write_text(APP if case == 'import' else BROKEN)
    (path / 'README.md').write_text('''# Local notes

Python standard library only. A store is a JSON list of id/text objects.

python3 notes.py --store /tmp/my-notes.json add a 'a note'
python3 notes.py --store /tmp/my-notes.json list

Keep verification stores in a scratch directory. Do not use real user data.
''')


def oracle(output):
    """Only public CLI behavior; no agent-created tests or internal imports."""
    checks = []
    with tempfile.TemporaryDirectory(prefix='skill-oracle-') as directory:
        fixture = Path(directory) / 'product'
        shutil.copytree(output, fixture, symlinks=True)
        data = Path(directory) / 'data'
        data.mkdir()
        profile = sandbox_profile(fixture, data, Path.home()) + '\n(deny network*)'
        evaluator_env = {'PATH': os.environ.get('PATH', ''), 'HOME': str(data),
                         'TMPDIR': str(data), 'PYTHONDONTWRITEBYTECODE': '1'}

        def call(store, *args):
            proc = subprocess.run(['sandbox-exec', '-p', profile, sys.executable, str(fixture / 'notes.py'), '--store', str(store), *map(str, args)],
                                  cwd=fixture, env=evaluator_env, capture_output=True, text=True, timeout=15)
            try:
                value = json.loads(proc.stdout)
            except (ValueError, TypeError):
                value = None
            return proc, value

        def check(name, fn):
            try:
                if name != 'existing-add-list':
                    control = data / 'empty-control.csv'
                    control.write_text('id,text\n')
                    proc, counts = call(data / 'empty-control.json', 'import', control)
                    expect(proc.returncode == 0 and counts == {'added': 0, 'skipped': 0},
                           'positive import control failed: ' + str((proc.stderr, counts)))
                detail = fn()
                checks.append({'id': name, 'passed': True, 'detail': detail})
            except Exception as exc:
                checks.append({'id': name, 'passed': False, 'detail': str(exc)[:1200] or type(exc).__name__})

        def expect(condition, detail):
            if not condition:
                raise AssertionError(detail)

        def csv_file(name, content):
            p = data / name
            p.write_text(content)
            return p

        def existing_commands():
            store = data / 'existing.json'
            p, _ = call(store, 'add', 'old', 'old text')
            expect(p.returncode == 0, p.stderr)
            p, rows = call(store, 'list')
            expect(p.returncode == 0 and rows == [{'id': 'old', 'text': 'old text'}], str(rows))
            p, _ = call(store, 'add', 'old', 'another')
            expect(p.returncode != 0, 'duplicate add accepted')
            return 'add/list and existing duplicate rejection preserved'

        def retry_safe():
            store = data / 'retry.json'
            store.write_text('[{"id":"old","text":"keep"}]')
            csv = csv_file('retry.csv', 'id,text\nold,ignore\n a ,first\na,second\nb,third\n')
            p, counts = call(store, 'import', csv)
            expect(p.returncode == 0 and counts == {'added': 2, 'skipped': 2}, str((p.stderr, counts)))
            expect(json.loads(store.read_text()) == [{'id': 'old', 'text': 'keep'}, {'id': 'a', 'text': 'first'}, {'id': 'b', 'text': 'third'}], store.read_text())
            p, counts = call(store, 'import', csv)
            expect(p.returncode == 0 and counts == {'added': 0, 'skipped': 4}, str(counts))
            return 'trimmed identity, first occurrence, existing IDs and retries observed'

        def dry_existing():
            store = data / 'dry.json'
            original = b'[ {"id":"old", "text":"keep"} ]\n'
            store.write_bytes(original)
            csv = csv_file('dry.csv', 'id,text\nold,ignore\na,new\na,duplicate\n')
            p, counts = call(store, 'import', csv, '--dry-run')
            expect(p.returncode == 0 and counts == {'added': 1, 'skipped': 2}, str(counts))
            expect(store.read_bytes() == original, 'dry run changed existing bytes')
            return 'counts correct and existing bytes unchanged'

        def dry_missing():
            parent = data / 'absent-parent'
            csv = csv_file('absent.csv', 'id,text\na,new\n')
            p, counts = call(parent / 'store.json', 'import', csv, '--dry-run')
            expect(p.returncode == 0 and counts == {'added': 1, 'skipped': 0}, str(counts))
            expect(not parent.exists(), 'dry run created missing parent/store')
            return 'missing parent and store stayed absent'

        def invalid_atomic(content, label):
            store = data / (label + '.json')
            original = b'[{"id":"old","text":"keep"}]\n'
            store.write_bytes(original)
            p, _ = call(store, 'import', csv_file(label + '.csv', content))
            expect(p.returncode != 0, 'invalid CSV accepted')
            expect(store.read_bytes() == original, 'invalid CSV changed store')
            return 'nonzero exit and original bytes preserved'

        def invalid_missing():
            parent = data / 'invalid-absent'
            p, _ = call(parent / 'store.json', 'import', csv_file('invalid-absent.csv', 'id,text\na,good\nb,   \n'))
            expect(p.returncode != 0 and not parent.exists(), 'invalid import created store/parent or succeeded')
            return 'invalid import did not create parent/store'

        def rich_text():
            store = data / 'rich.json'
            csv = csv_file('rich.csv', 'id,text\n a ,"hello, café\nsecond line"\n')
            p, counts = call(store, 'import', csv)
            expect(p.returncode == 0 and counts == {'added': 1, 'skipped': 0}, str(counts))
            p, rows = call(store, 'list')
            expect(p.returncode == 0 and rows == [{'id': 'a', 'text': 'hello, café\nsecond line'}], str(rows))
            return 'public list returns literal multiline Unicode text'

        check('existing-add-list', existing_commands)
        check('retry-and-identity', retry_safe)
        check('dry-existing-bytes', dry_existing)
        check('dry-missing-parent', dry_missing)
        check('invalid-row-atomic', lambda: invalid_atomic('id,text\na,good\nb,   \n', 'invalid-row'))
        check('invalid-id-atomic', lambda: invalid_atomic('id,text\na,good\n  ,bad\n', 'invalid-id'))
        check('invalid-duplicate-atomic', lambda: invalid_atomic('id,text\na,good\na,   \n', 'invalid-duplicate'))
        check('missing-column-atomic', lambda: invalid_atomic('id,other\na,b\n', 'missing-column'))
        check('invalid-missing-store', invalid_missing)
        check('quoted-unicode-text', rich_text)
    return {'passed': sum(c['passed'] for c in checks), 'total': len(checks), 'checks': checks}


def sandbox_profile(work, config, home):
    """macOS containment; provider access allowed, other trials/checkout denied."""
    q = lambda p: json.dumps(str(Path(p).resolve()))
    return '\n'.join([
        '(version 1)', '(allow default)', '(deny file-write*)',
        f'(deny file-read* (subpath {q(home)}) (subpath "/private/tmp") (subpath {q(tempfile.gettempdir())}))',
        '(allow file-read-metadata)',
        f'(allow file-read* (subpath {q(work)}) (subpath {q(config)}) (subpath {q(Path.home()/".local/lib")}) (subpath {q(Path.home()/".local/bin")}) (subpath {q(Path(shutil.which("node")).resolve().parent.parent)}))',
        f'(allow file-write* (subpath {q(work)}) (subpath {q(config)}) (literal "/dev/null"))',
    ])


def scrubber(config, env):
    values = []
    def collect(obj, key=''):
        if isinstance(obj, dict):
            for k, v in obj.items():
                collect(v, k)
        elif isinstance(obj, list):
            for v in obj:
                collect(v, key)
        elif isinstance(obj, str) and len(obj) >= 8 and re.search(r'token|secret|api.?key|password|access|refresh', key, re.I):
            values.append(obj)
    for name in ('auth.json', 'models.json'):
        p = config / name
        if p.exists():
            collect(json.loads(p.read_text()))
    for key, value in env.items():
        if len(value) >= 8 and re.search(r'token|secret|api.?key|password', key, re.I):
            values.append(value)
    def scrub(text):
        for value in sorted(set(values), key=len, reverse=True):
            text = text.replace(value, '<REDACTED>')
        return text
    return scrub


def summarize(events, condition, skill_path):
    tools, texts, usage = [], [], []
    for index, event in enumerate(events):
        if event.get('type') == 'tool_execution_start':
            tools.append({'event': index, 'id': event.get('toolCallId'), 'name': event.get('toolName'), 'args': event.get('args', {})})
        if event.get('type') == 'tool_execution_end':
            tools.append({'event': index, 'id': event.get('toolCallId'), 'result': event.get('result'), 'is_error': event.get('isError', False)})
        if event.get('type') == 'message_end':
            message = event.get('message', {})
            if message.get('role') == 'assistant':
                texts.extend(c.get('text', '') for c in message.get('content', []) if c.get('type') == 'text')
                if message.get('usage'):
                    usage.append(message['usage'])
    starts = [t for t in tools if 'name' in t]
    ends = {t['id']: t for t in tools if 'result' in t}
    incomplete = [t['id'] for t in starts if t['id'] not in ends]
    edits = [t for t in starts if t['name'] in ('edit', 'write') and
             Path(t['args'].get('path', '')).name == 'notes.py']
    checks = [t for t in starts if t['name'] == 'bash' and re.search(r'python|pytest|unittest|notes\.py', t['args'].get('command', ''))]
    skill_reads = [t for t in starts if skill_path and
                   (str(skill_path) in str(t['args']) or '.experiment/selected/SKILL.md' in str(t['args']))
                   and t['name'] == 'read' and t['id'] in ends and not ends[t['id']]['is_error']]
    assistant_messages = [e['message'] for e in events if e.get('type') == 'message_end'
                          and e.get('message', {}).get('role') == 'assistant']
    terminal = assistant_messages[-1].get('stopReason') if assistant_messages else None
    errors = [e.get('message', {}).get('errorMessage') for e in events if e.get('type') == 'message_end'
              and e.get('message', {}).get('role') == 'assistant' and e.get('message', {}).get('stopReason') == 'error']
    return {'tool_calls': len(starts), 'tool_receipts': tools, 'incomplete_tool_calls': incomplete,
            'skill_read_events': [t['event'] for t in skill_reads],
            'check_command_events': [t['event'] for t in checks],
            'product_edit_events': [t['event'] for t in edits],
            'check_before_first_edit_signal': bool(edits and any(t['event'] < edits[0]['event'] for t in checks)),
            'check_after_last_edit_signal': bool(edits and any(t['event'] > edits[-1]['event'] for t in checks)),
            'signal_limit': 'A command-shaped event is not proof of a relevant assertion, failure, or successful verification. Review its receipt.',
            'assistant_text': '\n\n'.join(texts), 'usage': usage, 'provider_errors': errors,
            'terminal_stop_reason': terminal, 'agent_ended': any(e.get('type') == 'agent_end' for e in events),
            'recovered_provider_errors': errors if terminal == 'stop' else []}


def run(condition, case, repeat, timeout=1200, skill_override=None):
    if not shutil.which('pi') or not shutil.which('sandbox-exec'):
        raise RuntimeError('This adapter requires installed Pi and macOS sandbox-exec')
    user_config = Path(os.environ.get('PI_CODING_AGENT_DIR', str(Path.home() / '.pi/agent')))
    settings = json.loads((user_config / 'settings.json').read_text())
    provider, model = settings.get('defaultProvider'), settings.get('defaultModel')
    if not provider or not model:
        raise RuntimeError('Explicit configured provider/model required; no model fallback')
    identity = f'{case}-{condition}-{repeat}-{uuid.uuid4().hex[:8]}'
    evidence = RUNS / identity
    evidence.mkdir(parents=True)
    with tempfile.TemporaryDirectory(prefix='pi-skill-trial-') as directory:
        runtime = Path(directory).resolve()
        work, config = runtime / 'work', runtime / 'config'
        seed(work, case)
        config.mkdir(mode=0o700)
        for name in ('auth.json', 'models.json'):
            source = user_config / name
            if source.exists():
                shutil.copyfile(source, config / name)
                (config / name).chmod(0o600)
        thinking = settings.get('defaultThinkingLevel', 'medium')
        write_json(config / 'settings.json', {'defaultProvider': provider, 'defaultModel': model,
                                             'defaultThinkingLevel': thinking, 'packages': []})
        skill_path = None
        if condition != 'baseline':
            source = Path(skill_override) if skill_override else SKILLS / PROFILES[condition] / 'SKILL.md'
            skill_path = work / '.experiment' / 'selected' / 'SKILL.md'
            skill_path.parent.mkdir(parents=True)
            shutil.copyfile(source, skill_path)
            shutil.copyfile(source, evidence / 'skill.md')
        prompt = brief(case)
        if skill_path:
            prompt += f'\nRead and apply the selected skill at {skill_path}.\n'
        (evidence / 'brief.txt').write_text(prompt)
        initial = hashes(work)
        write_json(evidence / 'initial-files.json', initial)
        profile = sandbox_profile(work, config, Path.home())
        (evidence / 'sandbox.sb').write_text(profile)
        # Verify the boundary before allowing an agent trial.
        probe = subprocess.run(['sandbox-exec', '-p', profile, '/bin/cat', str(Path(__file__).resolve())], capture_output=True)
        if probe.returncode == 0:
            raise RuntimeError('Private evaluator unexpectedly readable')
        (work / '.tmp').mkdir()
        env = dict(os.environ, PI_CODING_AGENT_DIR=str(config), PI_OFFLINE='1', PI_TELEMETRY='0',
                   TMPDIR=str(work / '.tmp'), HOME=str(config))
        scrub = scrubber(config, env)
        argv = ['pi', '--offline', '--no-extensions', '--no-skills', '--no-context-files',
                '--no-prompt-templates', '--no-themes', '--no-session', '--approve', '--mode', 'json',
                '--provider', provider, '--model', model, '--thinking', thinking, '--tools', 'read,bash,edit,write']
        if skill_path:
            argv += ['--skill', str(skill_path)]
        argv += ['--print', prompt]
        write_json(evidence / 'configuration.json', {'run_id': identity, 'case': case, 'condition': condition,
            'repeat': repeat, 'provider': provider, 'model': model, 'thinking': thinking,
            'pi_version': subprocess.check_output(['pi', '--version'], text=True).strip(),
            'runner_sha256': RUNNER_HASH,
            'argv': argv, 'time_limit_seconds': timeout, 'private_read_probe_denied': True,
            'containment': 'macOS filesystem restrictions; provider credential/network isolation not claimed',
            'skill_hash': hashlib.sha256(skill_path.read_bytes()).hexdigest() if skill_path else None})
        start = time.monotonic()
        node = shutil.which('node')
        if not node:
            raise RuntimeError('Pi requires an installed Node runtime')
        cli = str(Path(shutil.which('pi')).resolve())
        # Execute the resolved runtime directly; /usr/bin/env lookup can hit denied home paths.
        runtime_argv = [str(Path(node).resolve()), cli, *argv[1:]]
        process = subprocess.Popen(['sandbox-exec', '-p', profile, *runtime_argv], cwd=work, env=env,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, start_new_session=True)
        timed_out = False
        try:
            stdout, stderr = process.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            timed_out = True
            os.killpg(process.pid, signal.SIGTERM)
            try:
                stdout, stderr = process.communicate(timeout=5)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                stdout, stderr = process.communicate()
        # Also stop descendants of normally completed trials before freezing.
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        elapsed = time.monotonic() - start
        stdout, stderr = scrub(stdout), scrub(stderr)
        (evidence / 'events.jsonl').write_text(stdout)
        (evidence / 'stderr.txt').write_text(stderr)
        events, malformed = [], []
        for number, line in enumerate(stdout.splitlines()):
            try:
                events.append(json.loads(line))
            except ValueError:
                malformed.append(number)
        trace = summarize(events, condition, skill_path)
        write_json(evidence / 'trace-summary.json', trace)
        output = evidence / 'output'
        shutil.copytree(work, output, symlinks=True, ignore=shutil.ignore_patterns('__pycache__'))
        frozen = hashes(output)
        write_json(evidence / 'artifact-manifest.json', frozen)
        behavioral = oracle(output)
        if hashes(output) != frozen:
            raise RuntimeError('Evaluator modified frozen output')
        invalid = bool(malformed or not events or
                       (not timed_out and (process.returncode != 0 or trace['incomplete_tool_calls'] or
                                           trace['terminal_stop_reason'] != 'stop' or not trace['agent_ended'])))
        result = {'run_id': identity, 'case': case, 'condition': condition, 'repeat': repeat,
                  'valid': not invalid, 'timed_out': timed_out, 'returncode': process.returncode,
                  'seconds': round(elapsed, 2), 'tool_calls': trace['tool_calls'],
                  'skill_read': bool(trace['skill_read_events']), 'malformed_event_lines': malformed,
                  'incomplete_tool_calls': trace['incomplete_tool_calls'], 'runner_sha256': RUNNER_HASH,
                  'provider_errors': trace['provider_errors'], 'behavior': behavioral,
                  'terminal_stop_reason': trace['terminal_stop_reason'],
                  'recovered_provider_errors': trace['recovered_provider_errors'],
                  'check_before_first_edit_signal': trace['check_before_first_edit_signal'],
                  'check_after_last_edit_signal': trace['check_after_last_edit_signal'],
                  'evidence': str(evidence)}
        write_json(evidence / 'evaluation.json', result)
        print(json.dumps({k: v for k, v in result.items() if k != 'behavior'}))
        print(json.dumps({'checks_passed': behavioral['passed'], 'checks_total': behavioral['total']}))
        return result


def report():
    results = [json.loads(p.read_text()) for p in sorted(RUNS.glob('*/evaluation.json'))]
    lines = ['# Pi skill pilot results', '', 'Observed trials, not a claim of general superiority.', '',
             '| Case | Condition | Repeat | Valid | Checks | Seconds | Tools | Pre-edit check signal | Final check signal |',
             '| --- | --- | --- | --- | --- | --- | --- | --- | --- |']
    for r in results:
        label = r['condition']
        skill = Path(r['evidence']) / 'skill.md'
        if r['condition'] == 'candidate' and skill.exists():
            label = re.search(r'^name: (.+)$', skill.read_text(), re.M).group(1)
        lines.append(f'| {r["case"]} | {label} | {r["repeat"]} | {r["valid"]} | {r["behavior"]["passed"]}/{r["behavior"]["total"]} | {r["seconds"]} | {r["tool_calls"]} | {r["check_before_first_edit_signal"]} | {r["check_after_last_edit_signal"]} |')
    lines += ['', 'Workflow columns are automated event signals. Read command receipts before deciding compliance.',
              'The separate oracle assessed the frozen product through the CLI. It did not assess every possible input.', '']
    RUNS.parent.mkdir(parents=True, exist_ok=True)
    (RUNS.parent / 'comparison.md').write_text('\n'.join(lines))
    print('\n'.join(lines))


def replay(evidence, command, negative_case=None):
    """Replay a declared verifier after relocating frozen output, without repairing it."""
    evidence = Path(evidence).resolve()
    output = evidence / 'output'
    expected = json.loads((evidence / 'artifact-manifest.json').read_text())
    if hashes(output) != expected:
        raise RuntimeError('Frozen artifact changed before replay')
    with tempfile.TemporaryDirectory(prefix='skill-replay-') as directory:
        work = Path(directory).resolve() / 'product'
        scratch = Path(directory).resolve() / 'scratch'
        shutil.copytree(output, work, symlinks=True)
        scratch.mkdir()
        if negative_case:
            (work / 'notes.py').write_text(APP if negative_case == 'import' else BROKEN)
        profile = sandbox_profile(work, scratch, Path.home()) + '\n(deny network*)'
        env = {'PATH': os.environ.get('PATH', ''), 'HOME': str(scratch), 'TMPDIR': str(scratch),
               'PYTHONDONTWRITEBYTECODE': '1'}
        start = time.monotonic()
        try:
            result = subprocess.run(['sandbox-exec', '-p', profile, *command], cwd=work,
                                    env=env, capture_output=True, text=True, timeout=60)
            record = {'command': command, 'returncode': result.returncode, 'stdout': result.stdout,
                      'stderr': result.stderr, 'timed_out': False}
        except subprocess.TimeoutExpired:
            record = {'command': command, 'returncode': None, 'stdout': '', 'stderr': '', 'timed_out': True}
        record['seconds'] = round(time.monotonic() - start, 2)
        record['variant'] = 'known-bad-' + negative_case if negative_case else 'as-built'
        record['limit'] = 'Exit status and transcript require semantic review; this is not an independent product oracle.'
        write_json(evidence / ('verifier-negative-control.json' if negative_case else 'verifier-replay.json'), record)
    if hashes(output) != expected:
        raise RuntimeError('Replay modified frozen artifact')
    print(json.dumps(record))
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='operation', required=True)
    trial = sub.add_parser('run')
    trial.add_argument('--condition', choices=[*PROFILES, 'baseline', 'candidate'], required=True)
    trial.add_argument('--case', choices=['import', 'repair'], default='import')
    trial.add_argument('--repeat', type=int, default=1)
    trial.add_argument('--timeout', type=int, default=1200)
    trial.add_argument('--skill', type=Path)
    sub.add_parser('report')
    repeat_check = sub.add_parser('replay')
    repeat_check.add_argument('--run', required=True, type=Path)
    repeat_check.add_argument('--command', required=True, help='JSON argv array for the declared verifier')
    repeat_check.add_argument('--negative-control', choices=['import', 'repair'])
    args = parser.parse_args()
    if args.operation == 'report':
        report()
    elif args.operation == 'replay':
        command = json.loads(args.command)
        if not isinstance(command, list) or not command or not all(isinstance(x, str) for x in command):
            parser.error('command must be a nonempty JSON string array')
        replay(args.run, command, args.negative_control)
    else:
        if not 1 <= args.timeout <= 1200:
            parser.error('timeout must be between 1 and 1200 seconds')
        if args.condition == 'candidate' and not args.skill:
            parser.error('candidate requires --skill')
        run(args.condition, args.case, args.repeat, args.timeout, args.skill)


if __name__ == '__main__':
    main()
