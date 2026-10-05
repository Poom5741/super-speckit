import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location('pstack_adapter',ROOT/'scripts/pstack_adapter.py')
ADAPTER=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(ADAPTER)
INSTALL=ROOT/'installable/super-speckit/scripts/install_project.py'

class BundleTests(unittest.TestCase):
    def install(self,target,*extra):
        return subprocess.run(['python3',str(INSTALL),'--source',str(ROOT),'--target',str(target),*extra],capture_output=True,text=True)

    def test_whole_inventory_and_dormant_source(self):
        self.assertEqual(ADAPTER.inventory()['status'],'pass')
        manifest=json.loads((ROOT/'vendor/pstack-manifest.json').read_text())
        self.assertEqual(len(manifest['files']),164)
        self.assertFalse((ROOT/'skills/upstream/pstack').exists())
        self.assertEqual(len(ADAPTER.catalog()['playbooks']),23)
        self.assertEqual(len(ADAPTER.catalog()['principles']),24)

    def test_modified_missing_and_added_vendor_bytes_fail(self):
        with tempfile.TemporaryDirectory() as d:
            kit=Path(d); shutil.copytree(ROOT/'vendor',kit/'vendor')
            target=kit/'vendor/pstack/LICENSE'; original=target.read_bytes()
            target.write_bytes(original+b'changed')
            self.assertEqual(ADAPTER.verify_source(kit)['status'],'fail')
            target.write_bytes(original); target.unlink()
            self.assertIn('missing: LICENSE',ADAPTER.verify_source(kit)['failures'])
            target.write_bytes(original); (target.parent/'unknown.txt').write_text('extra')
            self.assertEqual(ADAPTER.verify_source(kit)['status'],'fail')

    def test_all_route_outputs_supply_overrides_and_source(self):
        catalog=ADAPTER.catalog()
        for group in ADAPTER.GROUPS:
            for entry in catalog[group]:
                route=ADAPTER.route(entry['id'],group)
                self.assertEqual(route['entry_command'],'ask-super-speckit')
                self.assertTrue((ROOT/'vendor/pstack'/route['route']['source']).is_file())
        result=subprocess.run(['python3',str(ROOT/'scripts/pstack_adapter.py'),'read','feature'],capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr)
        loaded=json.loads(result.stdout)
        self.assertIn('fidelity_overrides',loaded)
        self.assertIn('upstream_text',loaded)

    def test_reinstall_preserves_project_config_runtime_and_discovery(self):
        with tempfile.TemporaryDirectory() as d:
            target=Path(d)/'project'
            first=self.install(target); self.assertEqual(first.returncode,0,first.stderr)
            config=target/'super-speckit.yml'; config.write_text('user-owned: true\n')
            retained=target/'.super-speckit/qa/kept.log'; retained.parent.mkdir(exist_ok=True); retained.write_text('evidence')
            again=self.install(target); self.assertEqual(again.returncode,0,again.stderr)
            self.assertEqual(config.read_text(),'user-owned: true\n'); self.assertEqual(retained.read_text(),'evidence')
            self.assertTrue((target/'.super-speckit/vendor/pstack/automations/benny/README.md').is_file())
            names={p.parent.name for p in (target/'.agents/skills').glob('*/SKILL.md')}
            self.assertEqual(names,{'ask-super-speckit','super-speckit','super-speckit-design-first','super-speckit-final-manual-review'})
            self.assertFalse(list((target/'.agents').rglob('*benny*')))

    def test_local_bundle_drift_is_not_silently_overwritten(self):
        with tempfile.TemporaryDirectory() as d:
            target=Path(d)/'project'
            self.assertEqual(self.install(target).returncode,0)
            changed=target/'.super-speckit/SKILL.md'; changed.write_text(changed.read_text()+'\nlocal edit\n')
            result=self.install(target,'--upgrade')
            self.assertNotEqual(result.returncode,0)
            self.assertIn('local edit',changed.read_text())

    def test_deliberate_upgrade_backs_up_bundle_and_preserves_evidence(self):
        with tempfile.TemporaryDirectory() as d:
            area=Path(d); source=area/'source'; target=area/'project'
            shutil.copytree(ROOT,source,ignore=shutil.ignore_patterns('.git','__pycache__','node_modules','.super-speckit'))
            self.assertEqual(self.install(target).returncode,0)
            kept=target/'.super-speckit/qa/retained.log'; kept.parent.mkdir(exist_ok=True); kept.write_text('proof')
            config=target/'super-speckit.yml'; config.write_text('user-owned: true\n')
            prior=(source/'SKILL.md').read_text(); (source/'SKILL.md').write_text(prior+'\nupgrade fixture\n')
            update=subprocess.run(['python3',str(INSTALL),'--source',str(source),'--target',str(target),'--upgrade'],capture_output=True,text=True)
            self.assertEqual(update.returncode,0,update.stderr)
            self.assertIn('upgrade fixture',(target/'.super-speckit/SKILL.md').read_text())
            self.assertTrue((target/'.super-speckit-upgrade-backup/SKILL.md').is_file())
            self.assertEqual(kept.read_text(),'proof'); self.assertEqual(config.read_text(),'user-owned: true\n')

if __name__=='__main__': unittest.main()
