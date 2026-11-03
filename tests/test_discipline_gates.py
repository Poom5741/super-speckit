"""Discipline gates: pinned Elephant/Goldfish + VibeWise sources and their
code-enforced receipts, exercised against real Git and the public state CLI."""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).parents[1] / 'scripts'))
import test_state_contract as fixtures
import state_contract as c
import discipline_contract as d

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts/super_speckit.py'


class SourceTests(unittest.TestCase):
    def test_both_bundles_pinned_and_catalogs_match(self):
        d.verify_bundle()
        self.assertEqual(len(d.egm_catalog()['skills']), 7)
        self.assertEqual(len(d.vibe_catalog()['skills']), 2)
        egm = d.read_egm_skill('egm-review')
        self.assertIn('not a Goldfish review', egm['upstream_text'])
        self.assertIn('never a second coordinator', egm['adapter_contract'])
        vibe = d.read_vibe_skill('learn')
        self.assertIn('learning mode', vibe['upstream_text'].lower())
        with self.assertRaises(ValueError):
            d.read_egm_skill('egm-invented')
        with self.assertRaises(ValueError):
            d.read_vibe_skill('../reset')
        sources = json.loads((ROOT / 'sources.lock.json').read_text())['sources']
        entries = {s['name']: s for s in sources}
        for name, vendor in (('elephant-goldfish-model', 'elephant-goldfish'), ('vibe-wise', 'vibe-wise')):
            self.assertIn(name, entries)
            self.assertEqual(entries[name]['manifest'], f'vendor/{vendor}-manifest.json')
            self.assertTrue((ROOT / f'vendor/{vendor}/LICENSE').is_file())

    def test_vendor_drift_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            kit = Path(directory)
            for name in ('elephant-goldfish', 'vibe-wise'):
                shutil.copytree(ROOT / 'vendor' / name, kit / 'vendor' / name)
                shutil.copy2(ROOT / f'vendor/{name}-manifest.json', kit / f'vendor/{name}-manifest.json')
                shutil.copytree(ROOT / 'adapters' / name, kit / 'adapters' / name)
            d.verify_bundle(kit)
            with (kit / 'vendor/elephant-goldfish/skills/egm-review/SKILL.md').open('a') as stream:
                stream.write('\nWeakened protocol')
            with self.assertRaises(ValueError):
                d.verify_bundle(kit)


class GateTests(unittest.TestCase):
    def setUp(self):
        self.fixture = fixtures.StateTests('test_real_feature_release_and_cas')
        self.fixture.setUp()
        self.repo = self.fixture.repo
        self.stamp()
        self.evidence = [{'path': 'log.txt', 'digest': c.digest(self.repo / 'log.txt')}]
        self.record('learning-checkpoint', self.learning())
        self.record('goldfish-review', self.goldfish())

    def tearDown(self):
        self.fixture.tmp.cleanup()

    def data(self):
        return json.loads((self.repo / '.super-speckit/state/features/F.json').read_text())

    def stamp(self):
        data = self.data()
        data['gates_contract'] = 'discipline-v1'
        c.atomic(self.repo / '.super-speckit/state/features/F.json', data)
        self.fixture.ok('init')

    def record(self, kind, value, name=None):
        path = self.repo / (name or kind + '.json')
        path.write_text(json.dumps(value))
        self.fixture.ok('record-prerequisite', 'F', kind, '--artifact', path.name)

    def pinned(self, vendor, skill):
        manifest = json.loads((ROOT / f'vendor/{vendor}-manifest.json').read_text())
        return manifest['revision'], c.digest(ROOT / 'vendor' / vendor / 'skills' / skill / 'SKILL.md')

    def learning(self):
        revision, skill_digest = self.pinned('vibe-wise', 'learn')
        purpose = self.data()['purpose']['decision']
        return {'status': 'engaged', 'level': 'intermediate',
                'purpose_digest': c.digest(self.repo / purpose),
                'vibe': {'skill': 'learn', 'source_revision': revision, 'skill_digest': skill_digest},
                'checkpoints': [
                    {'topic': 'approach', 'human': 'user', 'ts': '2026-11-03T00:00:00Z',
                     'summary': 'Extend the existing service', 'agent_role': 'feedback only'},
                    {'topic': 'design', 'human': 'user', 'ts': '2026-11-03T00:00:00Z',
                     'summary': 'Adapter at the CLI boundary', 'agent_role': 'feedback only'}],
                'authorization': {'human': 'user', 'ts': '2026-11-03T00:00:00Z', 'scope': 'FR-001 only'},
                'evidence': self.evidence}

    def goldfish(self):
        revision, skill_digest = self.pinned('elephant-goldfish', 'egm-review')
        return {'status': 'passed', 'mode': 'goldfish',
                'reviewed': {'path': 'spec.md', 'digest': c.digest(self.repo / 'spec.md')},
                'harness_subagents': True,
                'reviewers': [{'id': 'g1', 'dispatch': 'subagent', 'fresh_context': True},
                              {'id': 'g2', 'dispatch': 'subagent', 'fresh_context': True}],
                'egm': {'skill': 'egm-review', 'source_revision': revision, 'skill_digest': skill_digest},
                'findings': [], 'resolution': 'No findings from fresh reviewers',
                'evidence': self.evidence}

    def test_new_records_default_to_the_discipline_gates(self):
        result = subprocess.run([sys.executable, str(SCRIPT), 'create-feature', 'NEW', '--repo', str(self.repo),
                                 '--maker', 'maker', '--checker', 'checker', '--matrix', 'matrix.json'],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        new = json.loads((self.repo / '.super-speckit/state/features/NEW.json').read_text())
        self.assertEqual(new['gates_contract'], 'discipline-v1')

    def test_missing_receipts_block_maker_and_route_next_stage(self):
        data = self.data()
        for kind in ('learning-checkpoint', 'goldfish-review'):
            data['prerequisite_receipts'].pop(kind)
        c.atomic(self.repo / '.super-speckit/state/features/F.json', data)
        self.fixture.ok('init')
        self.assertEqual(json.loads(self.fixture.ok('next-stage', 'F').stdout)['next_stage'], 'learning-checkpoint')
        self.assertNotEqual(self.fixture.invoke('transition', 'F', 'maker_running').returncode, 0)
        self.record('learning-checkpoint', self.learning())
        self.assertEqual(json.loads(self.fixture.ok('next-stage', 'F').stdout)['next_stage'], 'goldfish-review')
        self.assertNotEqual(self.fixture.invoke('transition', 'F', 'maker_running').returncode, 0)
        self.record('goldfish-review', self.goldfish())
        self.fixture.ok('transition', 'F', 'maker_running')
        self.fixture.ok('validate')

    def test_learning_checkpoint_requires_the_purpose_confirming_human(self):
        original = self.learning()
        engaged = lambda patch: {**original, **patch}
        self.record('learning-checkpoint', original)
        d.learning_checkpoint(self.repo, self.data())
        for patch in ({'purpose_digest': 'wrong'}, {'status': 'skipped'},
                      {'level': 'expert'},
                      {'checkpoints': original['checkpoints'][:1]},
                      {'authorization': {'human': 'maker', 'ts': 't', 'scope': 's'}}):
            value = engaged(patch)
            self.record('learning-checkpoint', value)
            with self.assertRaises(ValueError):
                d.learning_checkpoint(self.repo, self.data())
        checkpoints = [dict(cp) for cp in original['checkpoints']]
        checkpoints[0]['human'] = 'checker'
        self.record('learning-checkpoint', engaged({'checkpoints': checkpoints}))
        with self.assertRaises(ValueError):
            d.learning_checkpoint(self.repo, self.data())
        declined = {'status': 'human-declined', 'reason': 'Experienced owner; no learning mode this cycle',
                    'declined_by': 'maker',
                    'purpose_digest': original['purpose_digest'], 'vibe': original['vibe'],
                    'evidence': self.evidence}
        self.record('learning-checkpoint', declined)
        with self.assertRaises(ValueError):
            d.learning_checkpoint(self.repo, self.data())
        declined.update(declined_by='user')
        declined.pop('level', None); declined.pop('checkpoints', None); declined.pop('authorization', None)
        self.record('learning-checkpoint', declined)
        d.learning_checkpoint(self.repo, self.data())
        self.fixture.ok('transition', 'F', 'maker_running')

    def test_goldfish_enforces_fresh_subagent_dispatch_when_available(self):
        original = self.goldfish()
        self.record('goldfish-review', original)
        d.goldfish_review(self.repo, self.data())
        reviewers = [dict(r) for r in original['reviewers']]
        reviewers[1]['dispatch'] = 'sequential-fresh'
        for patch in ({'reviewers': reviewers},
                      {'reviewers': reviewers[:1]},
                      {'mode': 'goldfish-equivalent'},
                      {'harness_subagents': 'yes'}):
            self.record('goldfish-review', {**original, **patch})
            with self.assertRaises(ValueError):
                d.goldfish_review(self.repo, self.data())
        not_fresh = [dict(r) for r in original['reviewers']]
        not_fresh[0]['fresh_context'] = False
        self.record('goldfish-review', {**original, 'reviewers': not_fresh})
        with self.assertRaises(ValueError):
            d.goldfish_review(self.repo, self.data())
        self.record('goldfish-review', original)
        self.fixture.ok('transition', 'F', 'maker_running')

    def test_sequential_fallback_is_disclosed_equivalent_and_config_bound(self):
        original = self.goldfish()
        fallback = {**original, 'mode': 'goldfish-equivalent', 'harness_subagents': False,
                    'reviewers': [{'id': 'g1', 'dispatch': 'sequential-fresh', 'fresh_context': True},
                                  {'id': 'g2', 'dispatch': 'sequential-fresh', 'fresh_context': True}]}
        self.record('goldfish-review', fallback)
        with self.assertRaises(ValueError):
            d.goldfish_review(self.repo, self.data())
        self.record('goldfish-review', {**fallback, 'capability_absence': self.evidence})
        d.goldfish_review(self.repo, self.data())
        self.record('goldfish-review', {**fallback, 'mode': 'goldfish'})
        with self.assertRaises(ValueError):
            d.goldfish_review(self.repo, self.data())
        (self.repo / 'super-speckit.yml').write_text(
            'discipline_gates:\n  goldfish_min_reviewers: 2\n  allow_sequential_fresh_fallback: false\n')
        self.record('goldfish-review', {**fallback, 'capability_absence': self.evidence})
        with self.assertRaises(ValueError):
            d.goldfish_review(self.repo, self.data())
        (self.repo / 'super-speckit.yml').write_text(
            'discipline_gates:\n  goldfish_min_reviewers: 3\n  allow_sequential_fresh_fallback: true\n')
        self.record('goldfish-review', {**fallback, 'capability_absence': self.evidence})
        with self.assertRaises(ValueError):
            d.goldfish_review(self.repo, self.data())

    def test_goldfish_binds_current_route_artifact_and_pinned_protocol(self):
        original = self.goldfish()
        revision, skill_digest = self.pinned('elephant-goldfish', 'egm-review')
        for patch in ({'reviewed': {'path': 'grill.md', 'digest': c.digest(self.repo / 'grill.md')}},
                      {'reviewed': {'path': 'spec.md', 'digest': 'stale'}},
                      {'egm': {'skill': 'egm-draft', 'source_revision': revision, 'skill_digest': skill_digest}},
                      {'egm': {'skill': 'egm-review', 'source_revision': 'deadbeef', 'skill_digest': skill_digest}},
                      {'egm': {'skill': 'egm-review', 'source_revision': revision, 'skill_digest': 'wrong'}},
                      {'findings': [{'summary': 'Gap', 'disposition': 'open', 'reason': 'later',
                                     'evidence': self.evidence}]},
                      {'resolution': ''}):
            self.record('goldfish-review', {**original, **patch})
            with self.assertRaises(ValueError):
                d.goldfish_review(self.repo, self.data())
        (self.repo / 'spec.md').write_text('changed after review')
        self.record('goldfish-review', original)
        with self.assertRaises(ValueError):
            d.goldfish_review(self.repo, self.data())
        self.record('goldfish-review', {**original, 'reviewed': {'path': 'spec.md', 'digest': c.digest(self.repo / 'spec.md')}})
        d.goldfish_review(self.repo, self.data())

    def test_micro_route_reviews_the_playbook_bytes(self):
        self.fixture.ok('route', 'F', 'micro', '--rationale', 'bounded fix')
        (self.repo / 'playbook.md').write_text('FR-001 bounded fix: reproduce, fix, verify.')
        self.record('goldfish-review', self.goldfish())
        with self.assertRaises(ValueError):
            d.goldfish_review(self.repo, self.data())
        self.record('goldfish-review', {**self.goldfish(),
                                        'reviewed': {'path': 'playbook.md', 'digest': c.digest(self.repo / 'playbook.md')}})
        d.goldfish_review(self.repo, self.data())


if __name__ == '__main__':
    unittest.main()
