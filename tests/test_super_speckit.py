import json, shutil, subprocess, tempfile, unittest
from pathlib import Path

SCRIPT = Path(__file__).parents[1] / "scripts/super_speckit.py"
CLOUD_SCRIPT = Path(__file__).parents[1] / "scripts/cloud_handoff.py"
INSTALL_SCRIPT = Path(__file__).parents[1] / "installable/super-speckit/scripts/install_project.py"
ATLAS_EVAL_SCRIPT = Path(__file__).parents[1] / "scripts/atlas_eval.py"
class SuperSpecKitTests(unittest.TestCase):
    def invoke(self, *args):
        return subprocess.run(["python3", str(SCRIPT), *args], text=True, capture_output=True)
    def test_valid_feature_reaches_candidate_ready(self):
        with tempfile.TemporaryDirectory() as d:
            r=Path(d); matrix=r/"specs/f/verification-matrix.md"; matrix.parent.mkdir(parents=True); matrix.write_text("# matrix")
            self.assertEqual(self.invoke("init","--repo",d).returncode,0)
            self.assertEqual(self.invoke("create-feature","F-1","--repo",d,"--maker","maker","--checker","checker","--matrix","specs/f/verification-matrix.md").returncode,0)
            self.assertNotEqual(self.invoke("transition","F-1","maker_running","--repo",d).returncode,0)
            self.assertEqual(self.invoke("purpose-gate","F-1","--repo",d,"--title","Safe edit","--outcome","Save a profile safely","--people","Account holders","--success","The saved value persists","--non-goals","Do not change authorization").returncode,0)
            self.assertEqual(self.invoke("confirm-purpose","F-1","--repo",d,"--decision","confirmed","--confirmed-by","product-owner","--confirmed-at","2026-09-28T00:00:00Z","--confirmation","Purpose is correct").returncode,0)
            grill=r/".super-speckit/grills/F-1/spec-grill.md"; grill.parent.mkdir(parents=True); grill.write_text("# Evidence-labeled Spec Grill")
            self.assertEqual(self.invoke("record-grill","F-1","--repo",d,"--artifact",".super-speckit/grills/F-1/spec-grill.md").returncode,0)
            self.assertEqual(self.invoke("route","F-1","normal","--repo",d,"--rationale","Touches a persisted product workflow").returncode,0)
            self.assertEqual(self.invoke("atlas-init","F-1","--repo",d,"--summary","Save a profile safely").returncode,0)
            self.assertEqual(self.invoke("transition","F-1","candidate_ready","--repo",d,"--sha","abcdef1").returncode,0)
            self.assertEqual(self.invoke("validate","--repo",d).returncode,0)
    def test_ui_release_requires_latest_passing_journey_ux_report(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); matrix=root/"matrix.md"; matrix.write_text("# matrix")
            self.assertEqual(self.invoke("init","--repo",d).returncode,0)
            self.assertEqual(self.invoke("create-feature","UI-1","--repo",d,"--maker","maker","--checker","checker","--matrix","matrix.md","--ui-change").returncode,0)
            self.assertEqual(self.invoke("purpose-gate","UI-1","--repo",d,"--title","Edit profile","--outcome","Save a profile","--people","Account holder","--success","A saved profile","--non-goals","No permission change").returncode,0)
            self.assertEqual(self.invoke("confirm-purpose","UI-1","--repo",d,"--decision","confirmed","--confirmed-by","owner","--confirmed-at","2026-10-02T00:00:00Z","--confirmation","correct").returncode,0)
            grill=root/".super-speckit/grills/UI-1/spec-grill.md"; grill.parent.mkdir(parents=True); grill.write_text("# grill")
            self.assertEqual(self.invoke("record-grill","UI-1","--repo",d,"--artifact",".super-speckit/grills/UI-1/spec-grill.md").returncode,0)
            self.assertEqual(self.invoke("route","UI-1","normal","--repo",d,"--rationale","A UI workflow").returncode,0)
            self.assertEqual(self.invoke("atlas-init","UI-1","--repo",d,"--summary","Save profile").returncode,0)
            self.assertEqual(self.invoke("transition","UI-1","candidate_ready","--repo",d,"--sha","abcdef1").returncode,0)
            self.assertNotEqual(self.invoke("transition","UI-1","ready_for_merge","--repo",d).returncode,0)
            report=root/".super-speckit/qa/J-1/journey-ux-report.md"; report.parent.mkdir(parents=True); report.write_text("# journey report")
            self.assertEqual(self.invoke("record-journey-ux","UI-1","--repo",d,"--report",".super-speckit/qa/J-1/journey-ux-report.md","--sha","abcdef1","--status","passed").returncode,0)
            self.assertEqual(self.invoke("transition","UI-1","ready_for_merge","--repo",d).returncode,0)
    def test_status_reports_native_state_and_git_without_chat_memory(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); matrix=root/"matrix.md"; matrix.write_text("# matrix")
            self.assertEqual(self.invoke("init","--repo",d).returncode,0)
            self.assertEqual(self.invoke("create-feature","F-1","--repo",d,"--maker","maker","--checker","checker","--matrix","matrix.md").returncode,0)
            manifest=(root/".super-speckit/state/work-state.yml").read_text()
            self.assertIn('id: "F-1"', manifest)
            self.assertIn('state: "planned"', manifest)
            result=self.invoke("status","--repo",d,"--feature","F-1","--strict")
            self.assertEqual(result.returncode,0)
            state=json.loads(result.stdout)
            self.assertEqual(state["feature"]["state"],"planned")
            self.assertEqual(state["state_validation"]["status"],"pass")
            self.assertTrue(state["artifacts"]["work_state_manifest_exists"])
    def test_public_installer_copies_a_complete_kit_from_local_source(self):
        with tempfile.TemporaryDirectory() as d:
            destination=Path(d)/"project"
            result=subprocess.run(["python3",str(INSTALL_SCRIPT),"--source",str(Path(__file__).parents[1]),"--target",str(destination)],text=True,capture_output=True)
            self.assertEqual(result.returncode,0, result.stderr)
            self.assertTrue((destination/".super-speckit/SKILL.md").exists())
            self.assertTrue((destination/".super-speckit/state/work-state.yml").exists())
            self.assertTrue((destination/"super-speckit.yml").exists())
            for name in ("super-speckit", "ask-super-speckit", "super-speckit-design-first", "super-speckit-final-manual-review"):
                self.assertTrue((destination/".agents/skills"/name/"SKILL.md").exists())
            self.assertTrue((destination/".codex/skills/ask-super-speckit/SKILL.md").exists())
    def test_public_installer_repairs_missing_entrypoints_without_reinstalling_bundle(self):
        with tempfile.TemporaryDirectory() as d:
            destination=Path(d)/"project"
            installed=subprocess.run(["python3",str(INSTALL_SCRIPT),"--source",str(Path(__file__).parents[1]),"--target",str(destination)],text=True,capture_output=True)
            self.assertEqual(installed.returncode,0, installed.stderr)
            shutil.rmtree(destination/".agents")
            repaired=subprocess.run(["python3",str(INSTALL_SCRIPT),"--target",str(destination),"--register-only"],text=True,capture_output=True)
            self.assertEqual(repaired.returncode,0, repaired.stderr)
            self.assertTrue((destination/".agents/skills/ask-super-speckit/SKILL.md").exists())
    def test_same_person_cannot_be_maker_and_checker(self):
        with tempfile.TemporaryDirectory() as d:
            r=self.invoke("create-feature","F-1","--repo",d,"--maker","same","--checker","same","--matrix","x.md")
            self.assertNotEqual(r.returncode,0)
    def test_ready_requires_sha(self):
        with tempfile.TemporaryDirectory() as d:
            r=Path(d); m=r/"x.md"; m.write_text("x")
            self.invoke("init","--repo",d); self.invoke("create-feature","F-1","--repo",d,"--maker","a","--checker","b","--matrix","x.md")
            self.assertNotEqual(self.invoke("transition","F-1","ready_for_merge","--repo",d).returncode,0)
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
    def test_premium_ui_skill_sources_and_routing_are_present(self):
        root=Path(__file__).parents[1]
        sources=json.loads((root/"sources.lock.json").read_text())["sources"]
        names={source["name"] for source in sources}
        self.assertIn("UI/UX Pro Max", names)
        self.assertIn("Frontend Agent Skills", names)
        self.assertTrue((root/"skills/upstream/nextlevelbuilder/ui-ux-pro-max/SKILL.md").exists())
        self.assertTrue((root/"skills/upstream/hueyexe/ui-visual-composition/SKILL.md").exists())
        bridge=(root/"skills/design-first/SKILL.md").read_text()
        self.assertIn("Commit to one direction", bridge)
    def test_feedback_loop_is_a_required_orchestrator_stage(self):
        root=Path(__file__).parents[1]
        command=(root/"commands/super-speckit.feedback-loop.md").read_text()
        orchestrator=(root/"commands/ask-super-speckit.md").read_text()
        constitution=(root/"templates/constitution-addon.md").read_text()
        self.assertIn("public seam", command)
        self.assertIn("super-speckit.feedback-loop", orchestrator)
        self.assertIn("Native feedback loops", constitution)
    def test_purpose_gate_and_spec_grill_are_required_and_file_backed(self):
        root=Path(__file__).parents[1]
        purpose=(root/"commands/super-speckit.purpose-gate.md").read_text()
        grill=(root/"commands/super-speckit.spec-grill.md").read_text()
        template=(root/"templates/spec-grill.md").read_text()
        workflow=(root/"workflows/workflow.yml").read_text()
        self.assertIn("human", purpose.lower())
        self.assertIn("Builder", grill)
        self.assertIn("proven / inferred / assumed / unknown", template)
        self.assertIn("purpose-gate", workflow)
        self.assertIn("spec-grill", workflow)
    def test_atlas_route_and_transfer_are_file_backed(self):
        root=Path(__file__).parents[1]
        self.assertTrue((root/"commands/super-speckit.atlas.md").exists())
        self.assertTrue((root/"commands/super-speckit.route.md").exists())
        self.assertTrue((root/"commands/super-speckit.transfer.md").exists())
        transfer=(root/"templates/agent-transfer-handoff.md").read_text()
        self.assertIn("Attempt ID", transfer)
        self.assertIn("Re-run the status", transfer)
    def test_omp_team_lane_is_adaptive_and_preserves_boundaries(self):
        root=Path(__file__).parents[1]
        command=(root/"commands/super-speckit.omp-team.md").read_text()
        orchestrator=(root/"commands/ask-super-speckit.md").read_text()
        config=(root/"config/super-speckit.yml").read_text()
        self.assertIn("workspace isolation", command)
        self.assertIn("must not sit idle", command)
        self.assertIn("Makers never share a mutable worktree", command)
        self.assertIn("super-speckit.omp-team", orchestrator)
        self.assertIn("enabled_when_omp_detected: true", config)
    def test_journey_ux_loop_requires_full_rerun_and_latest_candidate(self):
        root=Path(__file__).parents[1]
        command=(root/"commands/super-speckit.journey-ux.md").read_text()
        template=(root/"templates/journey-ux-report.md").read_text()
        self.assertIn("full declared journey set", command)
        self.assertIn("latest candidate SHA", command)
        self.assertIn("No confirmed UX defect", template)
    def test_rakazo_is_the_default_private_manual_journey_reviewer(self):
        root=Path(__file__).parents[1]
        command=(root/"commands/super-speckit.rakazo-journey.md").read_text()
        packet=(root/"templates/rakazo-journey-task.md").read_text()
        config=(root/"config/super-speckit.yml").read_text()
        orchestrator=(root/"commands/ask-super-speckit.md").read_text()
        self.assertIn("provider: rakazo", config)
        self.assertIn("require_private_computer: true", config)
        self.assertIn("Never infer a generic Rakazo REST endpoint", command)
        self.assertIn("must not edit product code", command)
        self.assertIn("full declared journey set", command)
        self.assertIn("private Rakazo Computer", packet)
        self.assertIn("super-speckit.rakazo-journey", orchestrator)
    def test_atlas_evaluation_refuses_a_benefit_claim_without_three_qa_pairs(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); output=root/"report.md"
            common={"schema_version":1,"task_id":"T-1","base_sha":"abcdef1","agent_and_model":"test-agent","blind_task_brief":"Change one safe behavior"}
            run={"run_id":"1","completed":True,"duration_seconds":1,"token_count":1,"expected_impacted_components":["api"],"identified_impacted_components":["api"],"requirements_total":1,"requirements_correctly_covered":1,"unsupported_claims":0,"independent_qa_status":"pass"}
            control=root/"control.json"; atlas=root/"atlas.json"
            control.write_text(json.dumps({**common,"condition":"control","atlas_paths":[],"runs":[run]}))
            atlas.write_text(json.dumps({**common,"condition":"atlas","atlas_paths":["atlas.md"],"runs":[run]}))
            result=subprocess.run(["python3",str(ATLAS_EVAL_SCRIPT),"--control",str(control),"--atlas",str(atlas),"--output",str(output)],text=True,capture_output=True)
            self.assertEqual(result.returncode,0, result.stderr)
            self.assertIn("**inconclusive**",output.read_text())
    def test_orchestrator_is_autonomous_but_preserves_evidence_limits(self):
        root=Path(__file__).parents[1]
        skill=(root/"skills/ask-super-speckit/SKILL.md").read_text()
        policy=(root/"skills/ask-super-speckit/references/autonomous-execution.md").read_text()
        config=(root/"config/super-speckit.yml").read_text()
        self.assertIn("autonomous orchestrator", skill)
        self.assertIn("Self-healing loop", policy)
        self.assertIn("not a pass", policy)
        self.assertIn("autonomous_when_ready: true", config)
    def test_cloud_pack_is_bounded_and_rejects_obvious_secrets(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); handoff=root/"handoff.md"; pack=root/"pack.md"
            handoff.write_text("# Durable handoff\nVerified SHA: abcdef1\n")
            result=subprocess.run(["python3",str(CLOUD_SCRIPT),"--handoff",str(handoff),"--output",str(pack),"--role","maker","--base-sha","abcdef1","--branch","ss/feature/F-1","--objective","Add the scoped validation","--stage","maker_running","--attempt-id","ATT-1","--state-receipt",".super-speckit/receipts/ATT-1.json"],text=True,capture_output=True)
            self.assertEqual(result.returncode,0)
            self.assertIn("Do not merge",pack.read_text())
            self.assertIn("maker_running",pack.read_text())
            handoff.write_text("Authorization: Bearer secret")
            denied=subprocess.run(["python3",str(CLOUD_SCRIPT),"--handoff",str(handoff),"--output",str(pack),"--role","maker","--base-sha","abcdef1","--branch","main","--objective","x"],text=True,capture_output=True)
            self.assertNotEqual(denied.returncode,0)
if __name__ == "__main__": unittest.main()
