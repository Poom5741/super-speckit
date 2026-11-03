"""Executable discipline gates: Elephant/Goldfish fresh-context review and the
VibeWise learning checkpoint. Both are enforced here for every feature record
created with gates_contract=discipline-v1, regardless of harness: a scripted
harness that only runs scripts/super_speckit.py is blocked by these checks
until digest-bound gate receipts exist. Receipts are accountable observations;
they do not prove unseen agent reasoning."""
import json
from pathlib import Path
import state_contract as state

KIT = Path(__file__).resolve().parents[1]
GOLD = 'goldfish-review'
LEARN = 'learning-checkpoint'
EGM_REVIEW = 'skills/egm-review/SKILL.md'
VIBE_LEARN = 'skills/learn/SKILL.md'


def as_bool(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, str) and value.strip().lower() in {'true', 'false'}:
        return value.strip().lower() == 'true'
    raise ValueError('boolean configuration value expected')


def config(repo):
    section = state.config_section(repo, 'discipline_gates')
    def scalar(name, default, cast):
        try:
            return cast(section.get(name, default))
        except (TypeError, ValueError):
            raise ValueError('discipline_gates.' + name + ' has an invalid value')
    return {
        'min_reviewers': max(1, scalar('goldfish_min_reviewers', 2, int)),
        'allow_sequential_fresh': scalar('allow_sequential_fresh_fallback', True, as_bool),
    }


def verify_bundle(kit=KIT):
    for name in ('elephant-goldfish', 'vibe-wise'):
        manifest = json.loads((kit / f'vendor/{name}-manifest.json').read_text())
        root = kit / manifest['root']
        expected = {r['path']: r['sha256'] for r in manifest['files']}
        actual = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
        if actual != set(expected):
            raise ValueError(f'{name} source inventory mismatch')
        for rel, checksum in expected.items():
            path = root / rel
            if path.is_symlink() or state.digest(path) != checksum:
                raise ValueError(f'{name} source integrity failed: {rel}')


def _vendor_catalog(kit, vendor, adapter):
    verify_bundle(kit)
    entries = json.loads((kit / f'adapters/{adapter}/catalog.json').read_text())
    manifest = json.loads((kit / f'vendor/{vendor}-manifest.json').read_text())
    expected = {r['path']: r['sha256'] for r in manifest['files']
                if r['path'].startswith('skills/') and r['path'].endswith('/SKILL.md')}
    actual = {r['source']: r['sha256'] for r in entries['skills']}
    if (entries['source_revision'] != manifest['revision']
            or len(entries['skills']) != len(expected)
            or len(actual) != len(expected) or actual != expected):
        raise ValueError(f'{adapter} catalog does not match pinned source')
    for entry in entries['skills']:
        if entry['id'] != Path(entry['source']).parent.name:
            raise ValueError(f'{adapter} catalog identity mismatch')
    return entries


def egm_catalog(kit=KIT):
    return _vendor_catalog(kit, 'elephant-goldfish', 'elephant-goldfish')


def vibe_catalog(kit=KIT):
    return _vendor_catalog(kit, 'vibe-wise', 'vibe-wise')


def _read_skill(catalog, name, contract_path, kit):
    entry = next((r for r in catalog['skills'] if r['id'] == name), None)
    if not entry:
        raise ValueError('unknown pinned skill: ' + name)
    return {'entry_command': 'ask-super-speckit', 'skill': entry,
            'adapter_contract': (kit / contract_path).read_text(),
            'upstream_text': (kit / 'vendor' / catalog['vendor_root'] / entry['source']).read_text()}


def read_egm_skill(name, kit=KIT):
    catalog = egm_catalog(kit)
    catalog['vendor_root'] = 'elephant-goldfish'
    return _read_skill(catalog, name, 'adapters/elephant-goldfish/override-contract.md', kit)


def read_vibe_skill(name, kit=KIT):
    catalog = vibe_catalog(kit)
    catalog['vendor_root'] = 'vibe-wise'
    return _read_skill(catalog, name, 'adapters/vibe-wise/override-contract.md', kit)


def _pinned_digest(kit, vendor, path):
    verify_bundle(kit)
    return state.digest(kit / 'vendor' / vendor / path)


def learning_checkpoint(repo, data):
    r = state.knowledge_json(repo, data, LEARN)
    purpose = data.get('purpose', {})
    if purpose.get('status') != 'confirmed':
        raise ValueError('learning checkpoint requires a confirmed purpose')
    decision_path = state.file(repo, purpose.get('decision'))
    if r.get('purpose_digest') != state.digest(decision_path):
        raise ValueError('learning checkpoint must bind the current confirmed purpose decision')
    decision = json.loads(decision_path.read_text())
    manifest = json.loads((KIT / 'vendor/vibe-wise-manifest.json').read_text())
    vibe = r.get('vibe', {})
    if vibe.get('skill') != 'learn' or vibe.get('source_revision') != manifest['revision']:
        raise ValueError('pinned vibe-wise learn skill revision required')
    if vibe.get('skill_digest') != _pinned_digest(KIT, 'vibe-wise', VIBE_LEARN):
        raise ValueError('vibe-wise learn skill digest mismatch')
    agent_identities = {data.get('maker'), data.get('checker')}
    status = r.get('status')
    if status == 'engaged':
        if r.get('level') not in {'beginner', 'intermediate', 'advanced'}:
            raise ValueError('declared learning level required')
        checkpoints = r.get('checkpoints', [])
        topics = {cp.get('topic') for cp in checkpoints}
        if not {'approach', 'design'}.issubset(topics):
            raise ValueError('approach and design checkpoints are both required')
        for cp in checkpoints:
            if not cp.get('summary') or not cp.get('human'):
                raise ValueError('each checkpoint needs the human reasoning and its owner')
            if cp.get('human') in agent_identities:
                raise ValueError('a checkpoint must record the human, not a maker/checker agent identity')
        authorization = r.get('authorization', {})
        if not all(authorization.get(k) for k in ('human', 'ts', 'scope')):
            raise ValueError('explicit human implementation authorization required')
        if authorization.get('human') in agent_identities:
            raise ValueError('implementation authorization must come from the human')
    elif status == 'human-declined':
        if not r.get('reason'):
            raise ValueError('a recorded human reason is required to decline learning mode')
        if r.get('declined_by') != decision.get('confirmed_by'):
            raise ValueError('only the human who confirmed the purpose may decline the learning checkpoint')
    else:
        raise ValueError('learning checkpoint requires engaged or human-declined status')
    state.knowledge_evidence(repo, r.get('evidence'))


def goldfish_review(repo, data):
    r = state.knowledge_json(repo, data, GOLD)
    if r.get('status') != 'passed':
        raise ValueError('a passing goldfish review is required; inconclusive is never a pass')
    route = data.get('route', {}).get('kind')
    expected = 'playbook.md' if route == 'micro' else 'spec.md'
    reviewed = r.get('reviewed', {})
    if reviewed.get('path') != expected or reviewed.get('digest') != state.digest(state.file(repo, expected)):
        raise ValueError('goldfish review must bind the current ' + expected + ' bytes')
    manifest = json.loads((KIT / 'vendor/elephant-goldfish-manifest.json').read_text())
    egm = r.get('egm', {})
    if egm.get('skill') != 'egm-review' or egm.get('source_revision') != manifest['revision']:
        raise ValueError('the pinned egm-review protocol is required')
    if egm.get('skill_digest') != _pinned_digest(KIT, 'elephant-goldfish', EGM_REVIEW):
        raise ValueError('egm-review protocol digest mismatch')
    cfg = config(repo)
    reviewers = r.get('reviewers', [])
    if (len(reviewers) < cfg['min_reviewers']
            or len({x.get('id') for x in reviewers}) != len(reviewers)
            or any(not x.get('id') for x in reviewers)):
        raise ValueError(f'at least {cfg["min_reviewers"]} unique goldfish reviewers required')
    subagents = r.get('harness_subagents')
    if not isinstance(subagents, bool):
        raise ValueError('the harness subagent capability must be declared explicitly')
    for reviewer in reviewers:
        if reviewer.get('fresh_context') is not True:
            raise ValueError('every goldfish reviewer must run in a fresh context')
        dispatch = reviewer.get('dispatch')
        if subagents:
            # Upstream: a review in the same context is not a Goldfish review.
            if dispatch != 'subagent':
                raise ValueError('the harness has subagents: every goldfish reviewer must dispatch as a fresh subagent')
        elif dispatch != 'sequential-fresh':
            raise ValueError('undisclosed reviewer dispatch mode')
    if subagents:
        if r.get('mode') != 'goldfish':
            raise ValueError('subagent-dispatched review is mode goldfish')
    else:
        if not cfg['allow_sequential_fresh']:
            raise ValueError('configuration requires subagent review; a sequential fallback is not accepted here')
        if r.get('mode') != 'goldfish-equivalent':
            raise ValueError('a sequential fresh-context review is goldfish-equivalent, never goldfish')
        state.knowledge_evidence(repo, r.get('capability_absence'))
    for finding in r.get('findings', []):
        if (finding.get('disposition') not in {'fixed', 'accepted-risk', 'dismissed'}
                or not finding.get('summary') or not finding.get('reason')):
            raise ValueError('every goldfish finding needs a summary, disposition and reason')
        state.knowledge_evidence(repo, finding.get('evidence'))
    if not r.get('resolution'):
        raise ValueError('record how the goldfish findings were resolved')
    state.knowledge_evidence(repo, r.get('evidence'))
