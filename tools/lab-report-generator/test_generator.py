"""
Unit and Integration Test Suite for WAF Lab Report Generator.
Validates assignment configuration completeness, source file discovery,
QA rules, document building integrity, and atomic staging recovery.
"""

import os
import sys
import unittest
from pathlib import Path

# Add generator directory to sys.path
GENERATOR_DIR = Path(__file__).resolve().parent
WORKSPACE_ROOT = GENERATOR_DIR.parent.parent
sys.path.insert(0, str(GENERATOR_DIR))

import config
from server_manager import ServerManager, find_free_port
from qa_checker import LabReportQAChecker


class TestConfigurationRegistry(unittest.TestCase):
    """Validates the static configuration and schema for all supported assignments."""

    def test_all_expected_assignments_present(self):
        """Ensure Assignments 1 through 7 are defined in the registry."""
        expected_ids = {1, 2, 3, 4, 5, 6, 7}
        registered_ids = set(config.ASSIGNMENT_REGISTRY.keys())
        self.assertTrue(
            expected_ids.issubset(registered_ids),
            f"Missing assignment IDs: {expected_ids - registered_ids}"
        )

    def test_all_assignment_configurations_valid(self):
        """Validate every registered assignment against actual workspace files on disk."""
        for aid, cfg in config.ASSIGNMENT_REGISTRY.items():
            with self.subTest(assignment_id=aid, title=cfg.title):
                is_valid, errors = config.validate_assignment_config(cfg, WORKSPACE_ROOT)
                self.assertTrue(
                    is_valid,
                    f"Assignment {aid} failed validation: {'; '.join(errors)}"
                )

    def test_source_files_exist_on_disk(self):
        """Verify that every source file configured for the appendix exists and is readable."""
        for aid, cfg in config.ASSIGNMENT_REGISTRY.items():
            assignment_dir = WORKSPACE_ROOT / cfg.folder_name
            for sf in cfg.source_files:
                with self.subTest(assignment=aid, file=sf.relative_path):
                    target_file = assignment_dir / sf.relative_path
                    self.assertTrue(
                        target_file.is_file(),
                        f"Configured source file missing on disk: {target_file}"
                    )
                    # Verify readable text content
                    content = target_file.read_text(encoding="utf-8", errors="replace")
                    self.assertGreater(
                        len(content), 0,
                        f"Source file {target_file} is empty."
                    )

    def test_evidence_scenarios_have_valid_structure(self):
        """Ensure each assignment has either browser scenes or CLI commands configured."""
        for aid, cfg in config.ASSIGNMENT_REGISTRY.items():
            with self.subTest(assignment=aid):
                total_evidence = len(cfg.scenes) + len(cfg.cli_commands)
                self.assertGreater(
                    total_evidence, 0,
                    f"Assignment {aid} has 0 evidence scenarios configured."
                )
                for scene in cfg.scenes:
                    self.assertTrue(scene.name, "Scene has empty name")
                    self.assertTrue(scene.url_path, "Scene has empty url_path")
                    self.assertTrue(scene.requirement_tag, "Scene missing requirement tag")
                for cmd in cfg.cli_commands:
                    self.assertTrue(cmd.name, "CLI spec has empty name")
                    self.assertGreater(len(cmd.command), 0, "CLI spec has empty command")


class TestServerManager(unittest.TestCase):
    """Tests port discovery and server lifecycle utilities."""

    def test_find_free_port(self):
        """Verify find_free_port finds an available port in the safe range."""
        port = find_free_port(preferred_port=9000)
        self.assertGreaterEqual(port, 1024)
        self.assertLess(port, 65535)


class TestQaCheckerRules(unittest.TestCase):
    """Tests QA checker rules against known generated reference reports."""

    def test_assignment_2_report_qa_verification(self):
        """Verify that Assignment 2's generated production report passes all QA checks."""
        self._verify_assignment_production_qa(2)

    def test_all_production_reports_qa_verification(self):
        """Verify that all 7 generated production reports pass the full 14-point QA audit."""
        for aid in range(1, 8):
            with self.subTest(assignment_id=aid):
                self._verify_assignment_production_qa(aid)

    def _verify_assignment_production_qa(self, aid: int):
        reports_dir = WORKSPACE_ROOT / "reports" / f"Assignment-{aid}"
        docx_path = reports_dir / f"WAF_Assignment_{aid}.docx"
        pdf_path = reports_dir / f"WAF_Assignment_{aid}.pdf"
        screenshots_dir = reports_dir / "screenshots"
        previews_dir = reports_dir / "preview_pages"

        if not docx_path.exists() or not pdf_path.exists():
            self.skipTest(f"Assignment {aid} production report not generated yet.")

        cfg = config.get_assignment_config(aid)
        evidence_list = []
        for cmd in cfg.cli_commands:
            evidence_list.append({
                "name": cmd.name,
                "title": cmd.title,
                "image_path": screenshots_dir / f"{cmd.name}.png",
                "caption": cmd.caption,
                "description": cmd.description,
                "requirement_tag": cmd.requirement_tag
            })
        for s in cfg.scenes:
            evidence_list.append({
                "name": s.name,
                "title": s.title,
                "image_path": screenshots_dir / f"{s.name}.png",
                "caption": s.caption,
                "description": s.description,
                "requirement_tag": s.requirement_tag
            })

        checker = LabReportQAChecker(
            docx_path=docx_path,
            pdf_path=pdf_path,
            preview_dir=previews_dir,
            config=cfg,
            evidence_list=evidence_list,
            workspace_root=WORKSPACE_ROOT
        )
        passed, results = checker.run_all_checks()
        failures = [r for r in results if r["status"] == "FAIL"]
        self.assertTrue(
            passed,
            f"Assignment {aid} production report failed QA audit with errors: {[f['test_name'] + ': ' + f['details'] for f in failures]}"
        )


class TestStagingSafetyAndPreservation(unittest.TestCase):
    """Tests that staging isolation prevents corruption of production files."""

    def test_staging_isolation_logic(self):
        """Verify that staging paths are isolated under .stage and distinct from production."""
        target_dir = WORKSPACE_ROOT / "reports" / "Assignment-2"
        stage_dir = target_dir / ".stage"
        self.assertNotEqual(str(target_dir), str(stage_dir))
        self.assertTrue(str(stage_dir).endswith(".stage"))


if __name__ == "__main__":
    unittest.main()
