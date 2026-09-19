import json, subprocess, tempfile, unittest
from pathlib import Path

SCRIPT = Path(__file__).parents[1] / "scripts/super_speckit.py"
CLOUD_SCRIPT = Path(__file__).parents[1] / "scripts/cloud_handoff.py"
class SuperSpecKitTests(unittest.TestCase):
    def invoke(self, *args):
        return subprocess.run(["python3", str(SCRIPT), *args], text=True, capture_output=True)
    def test_valid_feature_reaches_candidate_ready(self):
        with tempfile.TemporaryDirectory() as d:
            r=Path(d); matrix=r/"specs/f/verification-matrix.md"; matrix.parent.mkdir(parents=True); matrix.write_text("# matrix")
            self.assertEqual(self.invoke("init","--repo",d).returncode,0)
            self.assertEqual(self.invoke("create-feature","F-1","--repo",d,"--maker","maker","--checker","checker","--matrix","specs/f/verification-matrix.md").returncode,0)
            self.assertEqual(self.invoke("transition","F-1","candidate_ready","--repo",d,"--sha","abcdef1").returncode,0)
            self.assertEqual(self.invoke("validate","--repo",d).returncode,0)
    def test_same_person_cannot_be_maker_and_checker(self):
        with tempfile.TemporaryDirectory() as d:
            r=self.invoke("create-feature","F-1","--repo",d,"--maker","same","--checker","same","--matrix","x.md")
            self.assertNotEqual(r.returncode,0)
    def test_ready_requires_sha(self):
        with tempfile.TemporaryDirectory() as d:
            r=Path(d); m=r/"x.md"; m.write_text("x")
            self.invoke("init","--repo",d); self.invoke("create-feature","F-1","--repo",d,"--maker","a","--checker","b","--matrix","x.md")
            self.assertNotEqual(self.invoke("transition","F-1","ready_for_human_merge","--repo",d).returncode,0)
    def test_design_first_makes_safe_html_decision_artifacts(self):
        with tempfile.TemporaryDirectory() as d:
            result=self.invoke("design-first","F-9","--repo",d,"--title","Farmer <Edit>","--summary","Update contact details")
            self.assertEqual(result.returncode,0)
            prototype=Path(d)/".super-speckit/design/F-9/prototype.html"
            self.assertIn("Farmer &lt;Edit&gt;",prototype.read_text())
            decision=json.loads((prototype.parent/"decision.json").read_text())
            self.assertEqual(decision["status"],"draft")
    def test_manual_review_skill_requires_wait_and_isolated_fix_loop(self):
        skill=(Path(__file__).parents[1] / "skills/final-manual-review/SKILL.md").read_text()
        protocol=(Path(__file__).parents[1] / "skills/final-manual-review/references/review-protocol.md").read_text()
        self.assertIn("wait", skill.lower())
        self.assertIn("new bug worktree", skill)
        self.assertIn("Do not continue dependent steps", protocol)
    def test_complementary_workflow_artifacts_are_present(self):
        root=Path(__file__).parents[1]
        self.assertTrue((root/"templates/phase-contract.md").exists())
        self.assertTrue((root/"templates/durable-handoff.md").exists())
        self.assertTrue((root/"commands/super-speckit.phase-check.md").exists())
        self.assertTrue((root/"skills/upstream/mattpocock/tdd/SKILL.md").exists())
        self.assertTrue((root/"skills/upstream/mattpocock/diagnosing-bugs/SKILL.md").exists())
        self.assertTrue((root/"commands/super-speckit.diagnose.md").exists())
        orchestrator=(root/"commands/ask-super-speckit.md").read_text()
        self.assertIn("super-speckit.diagnose", orchestrator)
    def test_cloud_pack_is_bounded_and_rejects_obvious_secrets(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); handoff=root/"handoff.md"; pack=root/"pack.md"
            handoff.write_text("# Durable handoff\nVerified SHA: abcdef1\n")
            result=subprocess.run(["python3",str(CLOUD_SCRIPT),"--handoff",str(handoff),"--output",str(pack),"--role","maker","--base-sha","abcdef1","--branch","ss/feature/F-1","--objective","Add the scoped validation"],text=True,capture_output=True)
            self.assertEqual(result.returncode,0)
            self.assertIn("Do not merge",pack.read_text())
            handoff.write_text("Authorization: Bearer secret")
            denied=subprocess.run(["python3",str(CLOUD_SCRIPT),"--handoff",str(handoff),"--output",str(pack),"--role","maker","--base-sha","abcdef1","--branch","main","--objective","x"],text=True,capture_output=True)
            self.assertNotEqual(denied.returncode,0)
if __name__ == "__main__": unittest.main()
