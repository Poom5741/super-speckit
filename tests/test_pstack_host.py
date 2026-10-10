import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

spec=importlib.util.spec_from_file_location('host',Path(__file__).parents[1]/'scripts/pstack_host.py')
h=importlib.util.module_from_spec(spec); spec.loader.exec_module(h)

class HostTests(unittest.TestCase):
    def test_no_guessed_dispatch(self):
        result=h.doctor({})
        self.assertTrue(result['zcode']['primary'])
        self.assertEqual(result['zcode']['dispatch'],'unavailable')
        self.assertEqual(result['codex']['certification'],'unverified')

    def test_explicit_fixture_dispatch_safe_argv_and_cancellation(self):
        with tempfile.TemporaryDirectory() as d:
            repo=Path(d)/'repo'; repo.mkdir()
            subprocess.run(['git','init','-q',str(repo)],check=True)
            subprocess.run(['git','-C',str(repo),'-c','user.name=Fixture','-c','user.email=fixture@example.test','commit','--allow-empty','-qm','fixture'],check=True)
            tree=Path(d)/'worker'
            subprocess.run(['git','-C',str(repo),'worktree','add','--detach','-q',str(tree)],check=True)
            brief=Path(d)/'brief;$(bad)'; brief.write_text('fixture')
            config={'zcode':dict(argv=[sys.executable,'-c','import sys; print(sys.argv[1])','{brief}'],isolation='git-worktree')}
            request=h.plan(config,'zcode',brief,tree)
            result=h.dispatch(request)
            self.assertEqual(result['status'],'completed'); self.assertEqual(result['stdout'].strip(),str(brief.resolve()))
            request['argv']=[sys.executable,'-c','import time; time.sleep(10)']
            self.assertEqual(h.dispatch(request,timeout=.05)['status'],'cancelled')
            with self.assertRaises(ValueError): h.plan(config,'zcode',brief,tree,model='unsupported')
            (tree/'dirty').write_text('change')
            with self.assertRaises(ValueError): h.plan(config,'zcode',brief,tree)

    def test_unavailable_and_undeclared_isolation(self):
        with self.assertRaises(ValueError): h.plan({},'pi','brief','.')
        with self.assertRaises(ValueError): h.plan({'pi':dict(argv=[sys.executable])},'pi','brief','.')

    def test_dispatch_rejects_outside_write_and_changed_brief(self):
        with tempfile.TemporaryDirectory() as d:
            repo=Path(d)/'repo'; repo.mkdir()
            subprocess.run(['git','init','-q',str(repo)],check=True)
            subprocess.run(['git','-C',str(repo),'-c','user.name=Fixture','-c','user.email=fixture@example.test','commit','--allow-empty','-qm','fixture'],check=True)
            tree=Path(d)/'worker'; subprocess.run(['git','-C',str(repo),'worktree','add','--detach','-q',str(tree)],check=True)
            brief=Path(d)/'brief'; brief.write_text('fixture')
            config={'pi':dict(argv=[sys.executable,'-c',"from pathlib import Path; Path('unexpected').write_text('bad')"],isolation='git-worktree')}
            request=h.plan(config,'pi',brief,tree,role='read-only',allowed_writes=['*'])
            brief.write_text('changed')
            with self.assertRaises(ValueError): h.dispatch(request)
            brief.write_text('fixture')
            result=h.dispatch(request); self.assertEqual(result['status'],'write-violation'); self.assertEqual(result['write_violations'],['unexpected'])

    def test_discovery_warns_user_shadow_and_provider_env_paths(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); user=root/'user/ask'; project=root/'project/ask'; user.mkdir(parents=True); project.mkdir(parents=True)
            for p in (user,project): (p/'SKILL.md').write_text('---\nname: ask-super-speckit\n---\nbody')
            result=h.doctor({'zcode':dict(skill_scopes=[dict(path=str(user.parent),kind='user'),dict(path=str(project.parent),kind='project')])})
            discovery=result['zcode']['discovery']; self.assertEqual(discovery['warning'],'user-scope-shadowing'); self.assertEqual(discovery['winner']['path'],str((user/'SKILL.md').resolve()))
            provider=root/'provider.json'; provider.write_text('{"secret":"never read"}')
            self.assertEqual(h.environment_paths({'ZCODE_BUILTIN_PROVIDER_CONFIG_FILE':str(provider)})['ZCODE_BUILTIN_PROVIDER_CONFIG_FILE'],str(provider))
            with self.assertRaises(ValueError): h.environment_paths({'API_SECRET':'must not log'})

class CloneHostTests(unittest.TestCase):
    def test_clone_dispatch_and_write_scope(self):
        with tempfile.TemporaryDirectory() as d:
            repo=Path(d)/'repo'; repo.mkdir()
            subprocess.run(['git','init','-q',str(repo)],check=True)
            subprocess.run(['git','-C',str(repo),'-c','user.name=Fixture','-c','user.email=fixture@example.test','commit','--allow-empty','-qm','fixture'],check=True)
            clone=Path(d)/'clone'
            subprocess.run(['git','clone','--no-local','-q',str(repo),str(clone)],check=True)
            brief=Path(d)/'brief'; brief.write_text('Review candidate; do not edit product code')
            config={'codex':dict(argv=[sys.executable,'-c','print("observed")'],isolation='git-clone')}
            request=h.plan(config,'codex',brief,clone,role='checker')
            self.assertEqual(h.dispatch(request)['status'],'completed')
            request['argv']=[sys.executable,'-c',"from pathlib import Path; Path('product').write_text('bad')"]
            self.assertEqual(h.dispatch(request)['status'],'write-violation')
