import importlib.util
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('skill_sandbox', Path(__file__).parents[1] / 'scripts/skill_sandbox.py')
sandbox = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sandbox)


@unittest.skipUnless(shutil.which('sandbox-exec') and shutil.which('node'), 'macOS sandbox adapter')
class SkillSandboxTests(unittest.TestCase):
    def test_verifier_mentioning_product_is_not_a_product_edit(self):
        events = [{'type': 'tool_execution_start', 'toolCallId': 'test', 'toolName': 'write',
                   'args': {'path': '.tmp/verify.py', 'content': 'run notes.py'}},
                  {'type': 'tool_execution_end', 'toolCallId': 'test', 'result': {}, 'isError': False},
                  {'type': 'tool_execution_start', 'toolCallId': 'product', 'toolName': 'edit',
                   'args': {'path': 'notes.py', 'oldText': 'old', 'newText': 'new'}},
                  {'type': 'tool_execution_end', 'toolCallId': 'product', 'result': {}, 'isError': False}]
        summary = sandbox.summarize(events, 'baseline', None)
        self.assertEqual(summary['product_edit_events'], [2])

    def test_recovered_provider_error_differs_from_terminal_error(self):
        failed = {'type': 'message_end', 'message': {'role': 'assistant', 'content': [],
                  'stopReason': 'error', 'errorMessage': 'terminated'}}
        completed = {'type': 'message_end', 'message': {'role': 'assistant', 'content': [], 'stopReason': 'stop'}}
        summary = sandbox.summarize([failed, completed, {'type': 'agent_end'}], 'baseline', None)
        self.assertEqual(summary['provider_errors'], ['terminated'])
        self.assertEqual(summary['recovered_provider_errors'], ['terminated'])
        self.assertEqual(summary['terminal_stop_reason'], 'stop')
        summary = sandbox.summarize([failed, {'type': 'agent_end'}], 'baseline', None)
        self.assertEqual(summary['recovered_provider_errors'], [])
        self.assertEqual(summary['terminal_stop_reason'], 'error')

    def test_requested_skill_read_is_not_observed_skill_load(self):
        events = [{'type': 'tool_execution_start', 'toolCallId': 'one',
                   'toolName': 'read', 'args': {'path': '.experiment/selected/SKILL.md'}}]
        summary = sandbox.summarize(events, 'candidate', Path('.experiment/selected/SKILL.md'))
        self.assertEqual(summary['skill_read_events'], [])
        self.assertEqual(summary['incomplete_tool_calls'], ['one'])
        events.append({'type': 'tool_execution_end', 'toolCallId': 'one',
                       'result': {'content': [{'type': 'text', 'text': 'skill body'}]}, 'isError': False})
        summary = sandbox.summarize(events, 'candidate', Path('.experiment/selected/SKILL.md'))
        self.assertEqual(summary['skill_read_events'], [0])
        self.assertEqual(summary['incomplete_tool_calls'], [])

    def test_symlink_target_changes_frozen_manifest(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            link = root / 'link'
            link.symlink_to('/etc/hosts')
            before = sandbox.hashes(root)
            link.unlink()
            link.symlink_to('/etc/services')
            self.assertNotEqual(before, sandbox.hashes(root))

    def test_unsupported_import_cannot_pass_negative_cases(self):
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory) / 'fixture'
            sandbox.seed(fixture, 'import')
            before = sandbox.hashes(fixture)
            result = sandbox.oracle(fixture)
            self.assertEqual(result['passed'], 1)
            self.assertTrue(result['checks'][0]['passed'])
            self.assertTrue(all(not row['passed'] for row in result['checks'][1:]))
            self.assertEqual(sandbox.hashes(fixture), before)

    def test_real_broken_import_is_rejected_without_changing_output(self):
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory) / 'fixture'
            sandbox.seed(fixture, 'repair')
            before = sandbox.hashes(fixture)
            result = sandbox.oracle(fixture)
            failures = {row['id'] for row in result['checks'] if not row['passed']}
            self.assertIn('dry-existing-bytes', failures)
            self.assertIn('retry-and-identity', failures)
            self.assertIn('invalid-duplicate-atomic', failures)
            self.assertEqual(sandbox.hashes(fixture), before)

    def test_subject_boundary_denies_private_read_and_outside_write(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            work, config = root / 'work', root / 'config'
            work.mkdir()
            config.mkdir()
            secret = root / 'private.txt'
            secret.write_text('private oracle')
            profile = sandbox.sandbox_profile(work, config, Path.home())
            read = subprocess.run(['sandbox-exec', '-p', profile, '/bin/cat', str(secret)], capture_output=True)
            self.assertNotEqual(read.returncode, 0)
            write = subprocess.run(['sandbox-exec', '-p', profile, '/usr/bin/touch', str(root / 'outside')], capture_output=True)
            self.assertNotEqual(write.returncode, 0)
            self.assertFalse((root / 'outside').exists())
            allowed = subprocess.run(['sandbox-exec', '-p', profile, '/usr/bin/touch', str(work / 'inside')], capture_output=True)
            self.assertEqual(allowed.returncode, 0, allowed.stderr)


if __name__ == '__main__':
    unittest.main()
