#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("certifier", ROOT / "scripts" / "certify-audit-manifest.py")
certifier = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(certifier)


def valid_manifest():
    return {
        "schema": certifier.SCHEMA,
        "identity": {
            "audit_id": "AUD-1",
            "repository": "owner/repo",
            "commit_sha": "a" * 40,
            "release": "release-1",
            "environment": "production",
            "timestamp_utc": "2026-09-21T23:59:00Z",
            "certified_scope": "all material user journeys",
            "scope_is_explicit": True,
            "primary_auditor": "agent-a",
        },
        "evidence": {
            "fresh": True, "same_sha_build": True, "same_environment": True,
            "provenance_complete": True, "debt_count": 0,
        },
        "coverage": {
            "inventory_complete": True, "all_material_journeys_enumerated": True,
            "all_material_states_enumerated": True, "negative_paths_complete": True,
            "boundaries_complete": True, "environment_matrix_complete": True,
            "not_validated_count": 0,
        },
        "taxonomy": {"complete": True, "no_material_not_validated": True},
        "data": {"reconciliation_complete": True, "orphan_scan_complete": True, "no_unexplained_difference": True},
        "runtime": {
            "no_unresolved_5xx": True, "no_unresolved_pageerror": True,
            "no_unresolved_requestfailed": True, "no_unresolved_console_error": True,
            "no_silent_failure": True,
        },
        "external_effects": {"reconciled": True},
        "async_runtime": {"observed": True},
        "observability": {"proven": True},
        "recovery": {"proven_or_not_material": True},
        "architecture": {"complete": True},
        "legacy_duplication": {"checked": True},
        "baseline": {"acceptable_or_not_material": True},
        "tests": {"no_flaky_false_green": True, "self_test_complete_when_applicable": True},
        "unknown_unknowns": {"completed": True},
        "audit_escape": {
            "pending_count": 0, "historical_classes_reaudited": True,
            "regression_tests_added_for_new_escapes": True,
        },
        "contradictory_review": {
            "completed": True, "reviewer_distinct": True, "no_open_findings": True, "reviewer": "agent-b",
        },
        "remediation": {
            "loop_completed": True, "no_gate_weakening": True, "open_blockers": 0,
            "executable_blockers": 0, "blocked_external_count": 0,
        },
        "findings": {
            "p0": 0, "p1": 0, "p2": 0, "p3": 0, "open_defects_total": 0,
            "improvement_required_open": 0, "preexisting_active_defects": 0,
        },
        "browser": {
            "required": True, "real_browser": True, "graphical_session": True,
            "agent_executed": True, "same_release": True, "full_user_path": True,
            "reload_revisit": True, "persistence_checked": True, "console_checked": True,
            "network_checked": True, "visual_evidence": True, "no_user_delegation": True,
            "not_headless_only": True,
        },
        "deploy": {
            "required": True, "same_sha_active": True, "post_deploy_validation_complete": True,
            "post_deploy_browser_e2e_complete": True, "post_deploy_async_observation_complete": True,
        },
        "journeys": [{
            "id": "critical-ui-flow", "material": True, "critical": True, "ui": True,
            "status": "COMPROVADO", "contradictory_reaudit": True,
            "evidence_refs": ["trace.zip", "screenshot.png"],
            "browser_e2e": {
                "real_browser": True, "graphical_session": True, "agent_executed": True,
                "same_release": True, "full_user_path": True, "reload_revisit": True,
                "persistence_checked": True, "console_checked": True, "network_checked": True,
                "visual_evidence": True, "no_user_delegation": True, "not_headless_only": True,
            },
        }],
    }


class CertifierTests(unittest.TestCase):
    def test_valid_manifest_is_apto(self):
        verdict, failures = certifier.certify(valid_manifest())
        self.assertEqual("APTO", verdict)
        self.assertEqual([], failures)

    def test_every_boolean_gate_blocks_when_false(self):
        for path in certifier.REQUIRED_TRUE + certifier.BROWSER_REQUIRED_TRUE + certifier.DEPLOY_REQUIRED_TRUE:
            with self.subTest(path=path):
                data = valid_manifest()
                target = data
                parts = path.split(".")
                for part in parts[:-1]:
                    target = target[part]
                target[parts[-1]] = False
                verdict, _ = certifier.certify(data)
                self.assertNotEqual("APTO", verdict)

    def test_every_zero_gate_blocks_when_nonzero(self):
        for path in certifier.REQUIRED_ZERO:
            with self.subTest(path=path):
                data = valid_manifest()
                target = data
                parts = path.split(".")
                for part in parts[:-1]:
                    target = target[part]
                target[parts[-1]] = 1
                verdict, _ = certifier.certify(data)
                self.assertNotEqual("APTO", verdict)

    def test_ui_journey_cannot_be_headless_only(self):
        data = valid_manifest()
        data["journeys"][0]["browser_e2e"]["not_headless_only"] = False
        verdict, _ = certifier.certify(data)
        self.assertEqual("NAO_APTO", verdict)

    def test_user_delegated_browser_cannot_certify(self):
        data = valid_manifest()
        data["browser"]["no_user_delegation"] = False
        verdict, _ = certifier.certify(data)
        self.assertEqual("NAO_APTO", verdict)

    def test_preexisting_defect_blocks(self):
        data = valid_manifest()
        data["findings"]["preexisting_active_defects"] = 1
        verdict, _ = certifier.certify(data)
        self.assertEqual("NAO_APTO", verdict)

    def test_external_blocker_never_becomes_apto(self):
        data = valid_manifest()
        data["remediation"]["blocked_external_count"] = 1
        verdict, _ = certifier.certify(data)
        self.assertEqual("BLOCKED_EXTERNAL", verdict)

    def test_same_auditor_and_reviewer_blocks(self):
        data = valid_manifest()
        data["contradictory_review"]["reviewer"] = "agent-a"
        verdict, _ = certifier.certify(data)
        self.assertEqual("NAO_APTO", verdict)


if __name__ == "__main__":
    unittest.main()
