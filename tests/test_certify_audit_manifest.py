#!/usr/bin/env python3
from __future__ import annotations

import copy
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("certifier", ROOT / "scripts" / "certify-audit-manifest.py")
certifier = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(certifier)


def valid_manifest():
    data = {
        "schema": certifier.SCHEMA,
        "policy_version": certifier.POLICY_VERSION,
        "identity": {
            "audit_id": "AUD-1", "repository": "owner/repo", "commit_sha": "a" * 40,
            "build_digest": "sha256:" + "b" * 64, "release": "release-1",
            "environment": "production", "timestamp_utc": "2026-09-21T23:59:00Z",
            "certified_scope": "all material user journeys", "scope_is_explicit": True,
            "primary_auditor": "agent-a",
        },
        "fingerprint": {
            "complete": True, "schema_version": "schema-1", "config_fingerprint": "cfg-1",
            "feature_flags_fingerprint": "flags-1", "provider_versions": {"provider": "v1"},
            "material_change_invalidation_checked": True,
        },
        "evidence": {
            "fresh": True, "same_sha_build": True, "same_environment": True,
            "provenance_complete": True, "artifact_hashes_verified": True, "debt_count": 0,
            "artifacts": [{
                "id": "trace", "path": "trace.zip", "kind": "trace",
                "sha256": "c" * 64, "sha_release_environment": "a"*40 + "|release-1|production",
            }],
        },
        "coverage": {
            "inventory_complete": True, "all_material_journeys_enumerated": True,
            "all_material_states_enumerated": True, "all_material_controls_classified": True,
            "negative_paths_complete": True, "boundaries_complete": True,
            "environment_matrix_complete": True, "not_validated_count": 0,
            "routes_discovered": 1, "interactive_controls_discovered": 1,
            "material_journeys": 1, "covered_controls": 1, "unmapped_surfaces": 0,
            "untested_material_controls": 0, "uncovered_material_journeys": 0,
        },
        "taxonomy": {"complete": True, "no_material_not_validated": True},
        "browser": {
            "required": True, "real_browser": True, "graphical_session": True,
            "agent_executed": True, "same_release": True, "full_user_path": True,
            "reload_revisit": True, "persistence_checked": True, "console_checked": True,
            "network_checked": True, "visual_evidence": True, "no_user_delegation": True,
            "not_headless_only": True, "clean_context_exercised_when_material": True,
            "mobile_desktop_exercised_when_material": True,
            "navigation_variants_exercised_when_material": True,
        },
        "clean_room": {
            "required": True, "completed_or_not_material": True, "clean_storage": True,
            "cold_cache": True, "auth_states_exercised": True,
            "cache_service_worker_checked": True, "navigation_reality_checked": True,
            "concurrency_checked": True, "partial_failure_recovery_checked": True,
            "cold_start_checked": True, "temporal_edges_checked": True,
            "soak_leak_checked_or_not_material": True,
        },
        "chaos_recovery": {
            "required": True, "completed_or_not_material": True, "timeout_checked": True,
            "rate_limit_checked": True, "server_error_checked": True,
            "partial_failure_checked": True, "retry_idempotency_checked": True,
            "alert_recovery_checked": True,
        },
        "authorization": {"matrix_complete_or_not_material": True},
        "visual": {"interaction_regression_complete_or_not_material": True},
        "data": {
            "reconciliation_complete": True, "orphan_scan_complete": True,
            "no_unexplained_difference": True, "unexplained_difference_count": 0,
        },
        "runtime": {
            "no_unresolved_5xx": True, "no_unresolved_pageerror": True,
            "no_unresolved_requestfailed": True, "no_unresolved_console_error": True,
            "no_silent_failure": True, "unresolved_error_count": 0,
        },
        "external_effects": {"reconciled": True},
        "async_runtime": {"observed": True, "settlement_complete": True},
        "observability": {"proven": True},
        "recovery": {"proven_or_not_material": True},
        "architecture": {"complete": True},
        "legacy_duplication": {"checked": True},
        "baseline": {"acceptable_or_not_material": True},
        "tests": {
            "no_flaky_false_green": True, "self_test_complete_when_applicable": True,
            "certifier_mutation_self_test_passed": True,
        },
        "unknown_unknowns": {"completed": True},
        "audit_escape": {
            "pending_count": 0, "historical_classes_reaudited": True,
            "regression_tests_added_for_new_escapes": True,
            "certification_invalidation_checked": True,
        },
        "contradictory_review": {
            "completed": True, "reviewer_distinct": True, "no_open_findings": True,
            "reviewer": "agent-b",
        },
        "remediation": {
            "loop_completed": True, "no_gate_weakening": True,
            "no_executable_issue_deferred": True, "open_blockers": 0,
            "executable_blockers": 0, "blocked_external_count": 0,
            "blocked_external_proven": False,
        },
        "findings": {
            "p0": 0, "p1": 0, "p2": 0, "p3": 0, "open_defects_total": 0,
            "improvement_required_open": 0, "preexisting_active_defects": 0,
        },
        "deploy": {
            "required": True, "same_sha_active": True, "post_deploy_validation_complete": True,
            "post_deploy_browser_e2e_complete_or_not_material": True,
            "post_deploy_async_observation_complete": True, "release_fingerprint_matches": True,
        },
        "certification": {"scope_label_exact": True, "no_self_attestation": True},
        "journeys": [{
            "id": "critical-ui-flow", "material": True, "critical": True, "ui": True,
            "status": "COMPROVADO", "contradictory_reaudit": True,
            "evidence_refs": ["trace"],
            "browser_e2e": {
                "real_browser": True, "graphical_session": True, "agent_executed": True,
                "same_release": True, "full_user_path": True, "reload_revisit": True,
                "persistence_checked": True, "console_checked": True, "network_checked": True,
                "visual_evidence": True, "no_user_delegation": True, "not_headless_only": True,
            },
        }],
    }
    return data


def set_path(data, path, value):
    target = data
    parts = path.split(".")
    for part in parts[:-1]:
        target = target[part]
    target[parts[-1]] = value


class CertifierTests(unittest.TestCase):
    def test_valid_manifest_is_apto(self):
        verdict, failures = certifier.certify(valid_manifest())
        self.assertEqual("APTO", verdict, failures)
        self.assertEqual([], failures)

    def test_every_boolean_gate_blocks_when_false(self):
        all_paths = (
            certifier.REQUIRED_TRUE + certifier.BROWSER_REQUIRED_TRUE +
            certifier.DEPLOY_REQUIRED_TRUE + certifier.CLEAN_ROOM_REQUIRED_TRUE +
            certifier.CHAOS_REQUIRED_TRUE
        )
        for path in all_paths:
            with self.subTest(path=path):
                data = valid_manifest()
                set_path(data, path, False)
                verdict, _ = certifier.certify(data)
                self.assertNotEqual("APTO", verdict)

    def test_every_zero_gate_blocks_when_nonzero(self):
        for path in certifier.REQUIRED_ZERO:
            with self.subTest(path=path):
                data = valid_manifest()
                set_path(data, path, 1)
                verdict, _ = certifier.certify(data)
                self.assertNotEqual("APTO", verdict)

    def test_ui_journey_cannot_be_headless_only(self):
        data = valid_manifest()
        data["journeys"][0]["browser_e2e"]["not_headless_only"] = False
        self.assertEqual("NAO_APTO", certifier.certify(data)[0])

    def test_user_delegated_browser_cannot_certify(self):
        data = valid_manifest()
        data["browser"]["no_user_delegation"] = False
        self.assertEqual("NAO_APTO", certifier.certify(data)[0])

    def test_preexisting_defect_blocks(self):
        data = valid_manifest()
        data["findings"]["preexisting_active_defects"] = 1
        self.assertEqual("NAO_APTO", certifier.certify(data)[0])

    def test_unmapped_surface_blocks(self):
        data = valid_manifest()
        data["coverage"]["unmapped_surfaces"] = 1
        self.assertEqual("NAO_APTO", certifier.certify(data)[0])

    def test_evidence_hash_is_required(self):
        data = valid_manifest()
        data["evidence"]["artifacts"][0]["sha256"] = "bad"
        self.assertEqual("NAO_APTO", certifier.certify(data)[0])

    def test_unknown_evidence_reference_blocks(self):
        data = valid_manifest()
        data["journeys"][0]["evidence_refs"] = ["missing"]
        self.assertEqual("NAO_APTO", certifier.certify(data)[0])

    def test_self_attested_verdict_blocks(self):
        data = valid_manifest()
        data["verdict"] = "APTO"
        self.assertEqual("NAO_APTO", certifier.certify(data)[0])

    def test_same_auditor_and_reviewer_blocks(self):
        data = valid_manifest()
        data["contradictory_review"]["reviewer"] = "agent-a"
        self.assertEqual("NAO_APTO", certifier.certify(data)[0])

    def test_external_blocker_requires_proof_and_no_executable_blockers(self):
        data = valid_manifest()
        data["remediation"]["blocked_external_count"] = 1
        data["remediation"]["blocked_external_proven"] = True
        verdict, _ = certifier.certify(data)
        self.assertEqual("BLOCKED_EXTERNAL", verdict)

        data = valid_manifest()
        data["remediation"]["blocked_external_count"] = 1
        data["remediation"]["blocked_external_proven"] = True
        data["remediation"]["executable_blockers"] = 1
        verdict, failures = certifier.certify(data)
        self.assertEqual("BLOCKED_EXTERNAL", verdict)
        self.assertTrue(any("executable blockers remain" in x for x in failures))

    def test_wrong_policy_version_blocks(self):
        data = valid_manifest()
        data["policy_version"] = "old"
        self.assertEqual("NAO_APTO", certifier.certify(data)[0])


if __name__ == "__main__":
    unittest.main()
