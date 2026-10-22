"""Unified lenses and native convergence receipts. No dispatch or second ledger."""
import hashlib
import json
import subprocess
from pathlib import Path
import state_contract as state

KIT = Path(__file__).resolve().parents[1]


def active(data):
    return data.get('pipeline_contract') == 'unified-v1'


def verify_bundle(kit=KIT):
    for name in ('lude-kit', 'spec-kit'):
        manifest = json.loads((kit / f'vendor/{name}-manifest.json').read_text())
        root = kit / manifest['root']
        expected = {r['path']: r['sha256'] for r in manifest['files']}
        actual = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
        if actual != set(expected):
            raise ValueError(f'{name} source inventory mismatch')
        for name_, checksum in expected.items():
            path = root / name_
            if path.is_symlink() or state.digest(path) != checksum:
                raise ValueError(f'{name} source integrity failed: {name_}')


def catalog(kit=KIT):
    verify_bundle(kit)
    entries = json.loads((kit / 'adapters/lude-kit/catalog.json').read_text())
    manifest = json.loads((kit / 'vendor/lude-kit-manifest.json').read_text())
    expected = {r['path']: r['sha256'] for r in manifest['files']
                if r['path'].startswith('skills/') and r['path'].endswith('/SKILL.md')}
    if (entries['source_revision'] != manifest['revision']
            or len(entries['skills']) != len(expected)
            or len({r['id'] for r in entries['skills']}) != len(expected)
            or {r['source']: r['sha256'] for r in entries['skills']} != expected):
        raise ValueError('Lude catalog does not match pinned source')
    for entry in entries['skills']:
        if entry['id'] != Path(entry['source']).parent.name or entry['category'] != entry['source'].split('/')[1]:
            raise ValueError('Lude catalog identity mismatch')
    return entries


def read_persona(name, kit=KIT):
    entry = next((r for r in catalog(kit)['skills'] if r['id'] == name), None)
    if not entry:
        raise ValueError('unknown Lude specialist: ' + name)
    return {'entry_command': 'ask-super-speckit', 'specialist': entry,
            'adapter_contract': (kit / 'adapters/lude-kit/override-contract.md').read_text(),
            'upstream_text': (kit / 'vendor/lude-kit' / entry['source']).read_text()}


def intent_files(repo, data, completion=False):
    matrix = state.file(repo, data['matrix'])
    directory = matrix.parent
    route = data.get('route', {}).get('kind')
    if route not in {'micro', 'normal', 'milestone'}:
        raise ValueError('scope route required before persona selection')
    names = ['playbook.md'] if route == 'micro' else ['spec.md', 'plan.md']
    if completion and route != 'micro':
        names += ['tasks.md']
    paths = [matrix] + [state.file(repo, str((directory / name).relative_to(repo))) for name in names]
    constitution = repo / '.specify/memory/constitution.md'
    if constitution.is_file():
        paths.append(constitution)
    return {p.relative_to(repo).as_posix(): state.digest(p) for p in paths}


def select(repo, data, maker, specialists, rationale):
    if data['state'] not in {'planned', 'maker_running', 'bug_fixing'}:
        raise ValueError('select personas before registering the next candidate')
    if not rationale.strip():
        raise ValueError('feature-specific persona rationale required')
    entries = {r['id']: r for r in catalog()['skills']}
    if maker not in entries or entries[maker]['category'] != 'personas':
        raise ValueError('maker must be a pinned Lude persona')
    names = [maker] + specialists
    if len(set(names)) != len(names) or any(n not in entries for n in names):
        raise ValueError('unique known specialists required')
    return {'route': data['route']['kind'], 'maker': data['maker'],
            'primary_persona': maker, 'rationale': rationale,
            'intent': intent_files(repo, data),
            'source_revision': catalog()['source_revision'],
            'specialists': [entries[n] for n in names]}


def personas(repo, data):
    receipt = state.knowledge_json(repo, data, 'personas')
    expected = select(repo, {**data, 'state': 'planned'}, receipt.get('primary_persona', ''),
                      [r['id'] for r in receipt.get('specialists', [])[1:]], receipt.get('rationale', ''))
    if receipt != expected:
        raise ValueError('stale or mismatched feature personas; select again')
    return receipt


def lens_review(repo, data):
    r = state.knowledge_json(repo, data, 'lens-review')
    if (r.get('candidate_sha') != data.get('candidate_sha') or r.get('checker') != data.get('checker')
            or r.get('checker') == data.get('maker') or r.get('status') != 'passed'):
        raise ValueError('lens review requires independent exact-candidate acceptance')
    if r.get('personas_digest') != state.digest(state.prerequisite_receipt(repo, data, 'personas')):
        raise ValueError('lens review must bind selected feature personas')
    lenses = r.get('lenses')
    if not isinstance(lenses, list) or len(lenses) != 2 or {x.get('id') for x in lenses} != {'pstack', 'lude-kit'}:
        raise ValueError('both PStack and Lude lenses required')
    for lens in lenses:
        if not lens.get('summary') or not isinstance(lens.get('findings'), list):
            raise ValueError('each lens needs a scoped summary and explicit findings')
        state.knowledge_evidence(repo, lens.get('evidence'))
        for finding in lens['findings']:
            if finding.get('disposition') not in {'fixed', 'accepted-risk', 'dismissed'} or not finding.get('reason'):
                raise ValueError('unresolved lens finding')
            state.knowledge_evidence(repo, finding.get('evidence'))
    if not r.get('reconciliation'):
        raise ValueError('reconcile lens disagreements explicitly')


def candidate_intent(repo, data, sha, exclude=()):
    for path in intent_files(repo, data, completion=True):
        if path in exclude:
            continue
        raw = subprocess.run(['git', '-C', str(repo), 'show', sha + ':' + path], capture_output=True)
        if raw.returncode or raw.stdout != state.file(repo, path).read_bytes():
            raise ValueError('intent must be frozen in candidate commit: ' + path)


def convergence_result(repo, data, r, allow_remaining=False):
    if not isinstance(r, dict):
        raise ValueError('convergence receipt must be an object')
    if (r.get('candidate_sha') != data.get('candidate_sha') or r.get('checker') != data.get('checker')
            or r.get('checker') == data.get('maker')):
        raise ValueError('convergence must match exact candidate and independent checker')
    mode = 'compact' if data['route']['kind'] == 'micro' else 'native'
    remaining = allow_remaining and r.get('outcome') == 'tasks_appended'
    if r.get('mode') != mode or (not remaining and (r.get('outcome') != 'converged' or r.get('remaining') != [])):
        raise ValueError('unfinished convergence blocks release')
    if r.get('intent') != intent_files(repo, data, completion=True):
        raise ValueError('convergence intent changed; rerun convergence')
    if not r.get('invocation') or not r.get('summary'):
        raise ValueError('observed convergence invocation and summary required')
    state.knowledge_evidence(repo, r.get('evidence'))
    if remaining:
        if not isinstance(r.get('remaining'), list) or not r['remaining']:
            raise ValueError('remaining convergence tasks required')
        work = 'tasks.md' if mode == 'native' else 'playbook.md'
        path = (state.file(repo, data['matrix']).parent / work).relative_to(repo).as_posix()
        candidate_intent(repo, data, data['candidate_sha'], exclude=(path,))
        if mode == 'native':
            raw = subprocess.run(['git', '-C', str(repo), 'show', data['candidate_sha'] + ':' + path], capture_output=True)
            current = state.file(repo, path).read_bytes()
            if (raw.returncode or not current.startswith(raw.stdout) or current == raw.stdout
                    or r.get('tasks_before_digest') != hashlib.sha256(raw.stdout).hexdigest()
                    or r.get('tasks_after_digest') != state.digest(state.file(repo, path))):
                raise ValueError('remaining native work must append tasks without rewriting existing intent')
        return r
    # A successful native convergence run leaves tasks byte-for-byte unchanged.
    if mode == 'native':
        tasks = state.file(repo, str((state.file(repo, data['matrix']).parent / 'tasks.md').relative_to(repo)))
        if r.get('tasks_before_digest') != state.digest(tasks) or r.get('tasks_after_digest') != state.digest(tasks):
            raise ValueError('native converged result must leave tasks unchanged')
    return r


def convergence(repo, data):
    candidate_intent(repo, data, data['candidate_sha'])
    return convergence_result(repo, data, state.knowledge_json(repo, data, 'convergence'))


def release(repo, data):
    for row in data.get('convergence_history', []):
        if row.get('digest') != state.digest(state.file(repo, row.get('artifact'))):
            raise ValueError('historical convergence receipt changed')
    personas(repo, data)
    lens_review(repo, data)
    convergence(repo, data)
