"""Unified delivery gates against real Git, native artifacts and the public CLI."""
import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import test_knowledge_contract as knowledge
import state_contract as c
import pipeline_contract as p
import discipline_contract as d

ROOT = Path(__file__).resolve().parents[1]


class UnifiedTests(unittest.TestCase):
    def setUp(self):
        self.k = knowledge.KnowledgeTests('test_investigation_precedes_route_and_pending_execution_blocks_completion')
        self.k.setUp()
        self.f = self.k.fixture
        self.repo = self.f.repo
        self.k.data['pipeline_contract'] = 'unified-v1'
        self.k.data['gates_contract'] = 'discipline-v1'
        self.k.save()
        for kind in ('research', 'architecture'):
            self.f.ok('record-prerequisite', 'F', kind, '--artifact', 'log.txt')
        self.gates()

    def tearDown(self):
        self.k.tearDown()

    def data(self):
        return json.loads((self.repo / '.super-speckit/state/features/F.json').read_text())

    def learning(self):
        purpose = self.data()['purpose']['decision']
        manifest = json.loads((ROOT / 'vendor/vibe-wise-manifest.json').read_text())
        return {'status': 'engaged', 'level': 'intermediate',
                'purpose_digest': c.digest(self.repo / purpose),
                'vibe': {'skill': 'learn', 'source_revision': manifest['revision'],
                         'skill_digest': c.digest(ROOT / 'vendor/vibe-wise/skills/learn/SKILL.md')},
                'checkpoints': [
                    {'topic': 'approach', 'human': 'user', 'ts': '2026-11-03T00:00:00Z',
                     'summary': 'Reuse the existing export service boundary', 'agent_role': 'feedback only'},
                    {'topic': 'design', 'human': 'user', 'ts': '2026-11-03T00:00:00Z',
                     'summary': 'CSV adapter behind the current CLI', 'agent_role': 'feedback only'}],
                'authorization': {'human': 'user', 'ts': '2026-11-03T00:00:00Z', 'scope': 'FR-001 export only'},
                'evidence': self.k.evidence}

    def goldfish(self):
        route = self.data().get('route', {}).get('kind')
        artifact = 'playbook.md' if route == 'micro' else 'spec.md'
        manifest = json.loads((ROOT / 'vendor/elephant-goldfish-manifest.json').read_text())
        return {'status': 'passed', 'mode': 'goldfish',
                'reviewed': {'path': artifact, 'digest': c.digest(self.repo / artifact)},
                'harness_subagents': True,
                'reviewers': [{'id': 'goldfish-1', 'dispatch': 'subagent', 'fresh_context': True},
                              {'id': 'goldfish-2', 'dispatch': 'subagent', 'fresh_context': True}],
                'egm': {'skill': 'egm-review', 'source_revision': manifest['revision'],
                        'skill_digest': c.digest(ROOT / 'vendor/elephant-goldfish/skills/egm-review/SKILL.md')},
                'findings': [], 'resolution': 'Fresh reviewers confirmed the export boundary; no findings',
                'evidence': self.k.evidence}

    def gates(self):
        (self.repo / 'learning.json').write_text(json.dumps(self.learning()))
        self.f.ok('record-prerequisite', 'F', 'learning-checkpoint', '--artifact', 'learning.json')
        self.record_goldfish()

    def record_goldfish(self, value=None):
        (self.repo / 'goldfish.json').write_text(json.dumps(value or self.goldfish()))
        self.f.ok('record-prerequisite', 'F', 'goldfish-review', '--artifact', 'goldfish.json')

    def select(self):
        return self.f.ok('select-personas', 'F', '--persona', 'senior-backend-engineer',
                         '--specialist', 'golang-expert', '--rationale', 'Go export service extends the existing endpoint')

    def prepare_qa(self):
        self.select()
        self.f.candidate()
        self.f.qa_start()
        self.f.receipt()
        self.f.ok('record-proof', 'F', '--receipt', 'proof.json')
        review = {'candidate_sha': self.f.sha, 'checker': 'checker', 'status': 'passed',
                  'blocking_findings': [], 'evidence': 'log.txt'}
        (self.repo / 'review.json').write_text(json.dumps(review))
        self.f.ok('record-prerequisite', 'F', 'engineering-review', '--artifact', 'review.json')
        self.k.data = self.data()
        self.k.result()
        self.k.save()

    def lens(self):
        return {'candidate_sha': self.f.sha, 'checker': 'checker', 'status': 'passed',
                'personas_digest': self.data()['prerequisite_receipts']['personas']['digest'],
                'lenses': [{'id': n, 'summary': n + ' scoped review', 'findings': [], 'evidence': self.k.evidence}
                           for n in ('pstack', 'lude-kit')],
                'reconciliation': 'Both lenses preserve the existing export boundary; no conflicting findings'}

    def convergence(self, mode='native'):
        return {'candidate_sha': self.f.sha, 'checker': 'checker', 'mode': mode,
                'outcome': 'converged', 'remaining': [], 'invocation': 'installed host speckit-converge fixture',
                'summary': 'Fixture assessment covered FR-001 and the existing tasks',
                'intent': p.intent_files(self.repo, self.data(), completion=True),
                'tasks_before_digest': c.digest(self.repo / 'tasks.md'),
                'tasks_after_digest': c.digest(self.repo / 'tasks.md'), 'evidence': self.k.evidence}

    def record_lens(self, value=None):
        (self.repo / 'lenses.json').write_text(json.dumps(value or self.lens()))
        self.f.ok('record-prerequisite', 'F', 'lens-review', '--artifact', 'lenses.json')

    def record_convergence(self, value=None, path='converge-1.json'):
        (self.repo / path).write_text(json.dumps(value or self.convergence()))
        return self.f.invoke('record-convergence', 'F', '--receipt', path)

    def test_new_records_default_to_unified_without_reinterpreting_legacy(self):
        result = subprocess.run([sys.executable, str(ROOT / 'scripts/super_speckit.py'), 'create-feature', 'NEW',
                                 '--repo', str(self.repo), '--maker', 'maker', '--checker', 'checker',
                                 '--matrix', 'matrix.json'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads((self.repo / '.super-speckit/state/features/NEW.json').read_text())
        self.assertEqual(data['pipeline_contract'], 'unified-v1')
        self.assertEqual(data['delivery_contract'], 'knowledge-v2')
        self.assertEqual(data['gates_contract'], 'discipline-v1')
        self.assertNotIn('pipeline_contract', self.f.invoke('status', '--feature', 'NEW').stderr)

    def test_discipline_gates_precede_maker_and_stale_intent_requires_rereview(self):
        data = self.data()
        data['prerequisite_receipts'].pop('learning-checkpoint')
        data['prerequisite_receipts'].pop('goldfish-review')
        c.atomic(self.repo / '.super-speckit/state/features/F.json', data)
        self.f.ok('init')
        self.assertEqual(json.loads(self.f.ok('next-stage', 'F').stdout)['next_stage'], 'learning-checkpoint')
        self.assertNotEqual(self.f.invoke('transition', 'F', 'maker_running').returncode, 0)
        (self.repo / 'learning.json').write_text(json.dumps(self.learning()))
        self.f.ok('record-prerequisite', 'F', 'learning-checkpoint', '--artifact', 'learning.json')
        self.assertEqual(json.loads(self.f.ok('next-stage', 'F').stdout)['next_stage'], 'goldfish-review')
        self.record_goldfish()
        d.goldfish_review(self.repo, self.data())
        (self.repo / 'spec.md').write_text('Rewritten after review')
        with self.assertRaises(ValueError):
            d.goldfish_review(self.repo, self.data())
        self.assertEqual(json.loads(self.f.ok('next-stage', 'F').stdout)['next_stage'], 'goldfish-review')

    def test_persona_selection_is_real_feature_bound_and_required(self):
        self.assertNotEqual(self.f.invoke('transition', 'F', 'maker_running').returncode, 0)
        self.assertEqual(json.loads(self.f.ok('next-stage', 'F').stdout)['next_stage'], 'personas')
        self.select()
        p.personas(self.repo, self.data())
        self.f.ok('transition', 'F', 'maker_running')
        for role in ('unknown', 'golang-expert'):
            self.assertNotEqual(self.f.invoke('select-personas', 'F', '--persona', role, '--rationale', 'Go').returncode, 0)
        (self.repo / 'plan.md').write_text('Now use a different architecture')
        self.assertEqual(json.loads(self.f.ok('next-stage', 'F').stdout)['next_stage'], 'personas')
        with self.assertRaises(ValueError):
            p.personas(self.repo, self.data())

    def test_native_qa_lenses_converge_then_release(self):
        self.prepare_qa()
        self.assertNotEqual(self.f.invoke('transition', 'F', 'ready_for_merge').returncode, 0)
        self.assertEqual(json.loads(self.f.ok('next-stage', 'F').stdout)['next_stage'], 'lens-review')
        self.record_lens()
        self.assertEqual(json.loads(self.f.ok('next-stage', 'F').stdout)['next_stage'], 'convergence')
        result = self.record_convergence()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(self.f.ok('next-stage', 'F').stdout)['next_stage'], 'release')
        self.f.ok('transition', 'F', 'ready_for_merge')
        self.f.ok('validate')

    def test_single_lens_self_review_unresolved_and_stale_reports_rejected(self):
        self.prepare_qa()
        original = self.lens()
        for patch in ({'lenses': original['lenses'][:1]}, {'checker': 'maker'},
                      {'candidate_sha': 'f' * 40}, {'personas_digest': 'wrong'}):
            self.record_lens({**original, **patch})
            with self.assertRaises(ValueError):
                p.lens_review(self.repo, self.data())
        unresolved = copy.deepcopy(original)
        unresolved['lenses'][1]['findings'] = [{'disposition': 'open', 'reason': 'Needs fix', 'evidence': self.k.evidence}]
        self.record_lens(unresolved)
        with self.assertRaises(ValueError):
            p.lens_review(self.repo, self.data())
        for patch in ({'candidate_sha': 'f' * 40}, {'checker': 'maker'}, {'remaining': ['FR-001']},
                      {'tasks_before_digest': 'wrong'}, {'mode': 'compact'}):
            self.record_lens(original)
            self.assertNotEqual(self.record_convergence({**self.convergence(), **patch}).returncode, 0)

    def test_remaining_tasks_reopen_maker_and_invalidate_old_acceptance(self):
        self.prepare_qa()
        self.record_lens()
        before = c.digest(self.repo / 'tasks.md')
        with (self.repo / 'tasks.md').open('a') as stream:
            stream.write('\n## Phase 2: Convergence\n- [ ] T002 Implement missing export edge per FR-001 (partial)\n')
        report = {**self.convergence(), 'outcome': 'tasks_appended', 'remaining': ['T002'], 'tasks_before_digest': before}
        result = self.record_convergence(report)
        self.assertEqual(result.returncode, 0, result.stderr)
        data = self.data()
        self.assertEqual(data['state'], 'maker_running')
        self.assertNotIn('proof', data)
        self.assertNotIn('qa_attempt', data)
        for key in ('convergence', 'lens-review', 'engineering-review', 'shared-result'):
            self.assertNotIn(key, data['prerequisite_receipts'])
        self.assertEqual(len(data['convergence_history']), 1)
        self.assertNotEqual(self.f.invoke('transition', 'F', 'ready_for_merge').returncode, 0)
        self.f.ok('record-prerequisite', 'F', 'phase-contract', '--artifact', 'tasks.md')
        self.assertNotEqual(self.f.invoke('transition', 'F', 'candidate_ready', '--sha', self.f.sha).returncode, 0)
        self.f.run_git('add', 'tasks.md')
        self.f.run_git('commit', '-m', 'implement convergence task')
        sha = self.f.run_git('rev-parse', 'HEAD')
        self.f.ok('transition', 'F', 'candidate_ready', '--sha', sha)
        self.assertNotEqual(self.data()['candidate_sha'], report['candidate_sha'])
        self.assertEqual(json.loads(self.f.ok('next-stage', 'F').stdout)['next_stage'], 'independent-qa')
        # The reopened slice must complete a fresh attempt and converge again.
        self.f.sha = sha
        self.k.sha = sha
        subprocess.check_call(['git', '-C', str(self.f.qa), 'checkout', '--detach', sha],
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        self.f.ok('transition', 'F', 'qa_running', '--worktree', str(self.f.qa), '--attempt-id', 'A2')
        receipt = self.f.receipt()
        receipt['attempt_id'] = 'A2'
        (self.repo / 'environment.json').write_text(json.dumps({key: receipt[key] for key in
                                                              ('candidate_sha', 'checker', 'worktree', 'attempt_id')}))
        (self.repo / 'proof.json').write_text(json.dumps(receipt))
        self.f.ok('record-proof', 'F', '--receipt', 'proof.json')
        (self.repo / 'review.json').write_text(json.dumps({'candidate_sha': sha, 'checker': 'checker',
                                                        'status': 'passed', 'blocking_findings': []}))
        self.f.ok('record-prerequisite', 'F', 'engineering-review', '--artifact', 'review.json')
        self.k.data = self.data()
        self.k.result()
        self.k.save()
        self.record_lens()
        result = self.record_convergence(path='converge-2.json')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.f.ok('transition', 'F', 'ready_for_merge')
        self.f.ok('validate')
        self.assertEqual(len(self.data()['convergence_history']), 2)

    def test_rewritten_intent_cannot_masquerade_as_append_only_convergence(self):
        self.prepare_qa()
        self.assertNotEqual(self.record_convergence().returncode, 0)
        self.record_lens()
        before = c.digest(self.repo / 'tasks.md')
        (self.repo / 'tasks.md').write_text('Delete old tasks; call everything complete')
        report = {**self.convergence(), 'outcome': 'tasks_appended', 'remaining': ['T002'], 'tasks_before_digest': before}
        self.assertNotEqual(self.record_convergence(report).returncode, 0)
        self.assertNotEqual(self.record_convergence().returncode, 0)
        original = subprocess.check_output(['git', '-C', str(self.repo), 'show', self.f.sha + ':tasks.md'])
        (self.repo / 'tasks.md').write_bytes(original + b'\n- [ ] T002 Finish missing work\n')
        (self.repo / 'spec.md').write_text('Silently remove previously required behavior')
        report = {**self.convergence(), 'outcome': 'tasks_appended', 'remaining': ['T002'], 'tasks_before_digest': before}
        self.assertNotEqual(self.record_convergence(report).returncode, 0)

    def test_compact_mode_does_not_claim_native_convergence(self):
        self.f.ok('route', 'F', 'micro', '--rationale', 'Existing bounded export')
        (self.repo / 'playbook.md').write_text('FR-001: use existing export; implement, verify and assess completion')
        self.record_goldfish()
        self.f.run_git('add', 'playbook.md')
        self.f.run_git('commit', '-m', 'compact intent')
        self.f.sha = self.f.run_git('rev-parse', 'HEAD')
        self.k.sha = self.f.sha
        self.prepare_qa()
        self.record_lens()
        self.assertNotEqual(self.record_convergence().returncode, 0)
        result = self.record_convergence(self.convergence('compact'))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.f.ok('transition', 'F', 'ready_for_merge')


class SourceTests(unittest.TestCase):
    def test_full_catalog_and_progressive_source(self):
        catalog = p.catalog()
        self.assertEqual(len(catalog['skills']), 64)
        loaded = p.read_persona('golang-expert')
        self.assertIn('Every goroutine', loaded['upstream_text'])
        self.assertIn('Super-SpecKit owns', loaded['adapter_contract'])
        with self.assertRaises(ValueError):
            p.read_persona('../orchestrate-feature-build')

    def test_vendor_drift_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            kit = Path(directory)
            for name in ('lude-kit', 'spec-kit'):
                shutil.copytree(ROOT / 'vendor' / name, kit / 'vendor' / name)
                shutil.copy2(ROOT / f'vendor/{name}-manifest.json', kit / f'vendor/{name}-manifest.json')
            p.verify_bundle(kit)
            with (kit / 'vendor/lude-kit/skills/stacks/golang-expert/SKILL.md').open('a') as stream:
                stream.write('\nChanged advice')
            with self.assertRaises(ValueError):
                p.verify_bundle(kit)


if __name__ == '__main__':
    unittest.main()
