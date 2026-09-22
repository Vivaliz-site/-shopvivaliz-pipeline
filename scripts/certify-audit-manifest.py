#!/usr/bin/env python3
"""Fail-closed certifier for a completed Extreme Audit evidence manifest."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCHEMA = "AUDIT_CERTIFICATION_MANIFEST_V1"

REQUIRED_TRUE = [
    "identity.scope_is_explicit",
    "evidence.fresh",
    "evidence.same_sha_build",
    "evidence.same_environment",
    "evidence.provenance_complete",
    "coverage.inventory_complete",
    "coverage.all_material_journeys_enumerated",
    "coverage.all_material_states_enumerated",
    "coverage.negative_paths_complete",
    "coverage.boundaries_complete",
    "coverage.environment_matrix_complete",
    "taxonomy.complete",
    "taxonomy.no_material_not_validated",
    "data.reconciliation_complete",
    "data.orphan_scan_complete",
    "data.no_unexplained_difference",
    "runtime.no_unresolved_5xx",
    "runtime.no_unresolved_pageerror",
    "runtime.no_unresolved_requestfailed",
    "runtime.no_unresolved_console_error",
    "runtime.no_silent_failure",
    "external_effects.reconciled",
    "async_runtime.observed",
    "observability.proven",
    "recovery.proven_or_not_material",
    "architecture.complete",
    "legacy_duplication.checked",
    "baseline.acceptable_or_not_material",
    "tests.no_flaky_false_green",
    "tests.self_test_complete_when_applicable",
    "unknown_unknowns.completed",
    "audit_escape.historical_classes_reaudited",
    "audit_escape.regression_tests_added_for_new_escapes",
    "contradictory_review.completed",
    "contradictory_review.reviewer_distinct",
    "contradictory_review.no_open_findings",
    "remediation.loop_completed",
    "remediation.no_gate_weakening",
]

REQUIRED_ZERO = [
    "findings.p0",
    "findings.p1",
    "findings.p2",
    "findings.p3",
    "findings.open_defects_total",
    "findings.improvement_required_open",
    "audit_escape.pending_count",
    "remediation.open_blockers",
    "remediation.executable_blockers",
    "remediation.blocked_external_count",
]

DEPLOY_REQUIRED_TRUE = [
    "deploy.same_sha_active",
    "deploy.post_deploy_validation_complete",
    "deploy.post_deploy_browser_e2e_complete",
    "deploy.post_deploy_async_observation_complete",
]

BROWSER_REQUIRED_TRUE = [
    "browser.real_browser",
    "browser.graphical_session",
    "browser.agent_executed",
    "browser.same_release",
    "browser.full_user_path",
    "browser.reload_revisit",
    "browser.persistence_checked",
    "browser.console_checked",
    "browser.network_checked",
    "browser.visual_evidence",
    "browser.no_user_delegation",
    "browser.not_headless_only",
]


def get_path(data: dict, dotted: str):
    value = data
    for part in dotted.split("."):
        if not isinstance(value, dict) or part not in value:
            return None
        value = value[part]
    return value


def add_bool_failures(data: dict, paths: list[str], failures: list[str]) -> None:
    for path in paths:
        if get_path(data, path) is not True:
            failures.append(f"{path} must be true")


def add_zero_failures(data: dict, paths: list[str], failures: list[str]) -> None:
    for path in paths:
        value = get_path(data, path)
        if type(value) is not int or value != 0:
            failures.append(f"{path} must be integer 0")


def validate_identity(data: dict, failures: list[str]) -> None:
    for path in [
        "identity.audit_id",
        "identity.repository",
        "identity.commit_sha",
        "identity.release",
        "identity.environment",
        "identity.timestamp_utc",
        "identity.certified_scope",
        "identity.primary_auditor",
    ]:
        value = get_path(data, path)
        if not isinstance(value, str) or not value.strip():
            failures.append(f"{path} must be non-empty")

    primary = get_path(data, "identity.primary_auditor")
    reviewer = get_path(data, "contradictory_review.reviewer")
    if not isinstance(reviewer, str) or not reviewer.strip():
        failures.append("contradictory_review.reviewer must be non-empty")
    elif isinstance(primary, str) and reviewer.strip() == primary.strip():
        failures.append("contradictory reviewer must differ from primary auditor")


def validate_journeys(data: dict, failures: list[str]) -> None:
    journeys = data.get("journeys")
    if not isinstance(journeys, list) or not journeys:
        failures.append("journeys must contain at least one enumerated journey")
        return

    seen = set()
    for index, journey in enumerate(journeys):
        prefix = f"journeys[{index}]"
        if not isinstance(journey, dict):
            failures.append(f"{prefix} must be an object")
            continue

        jid = journey.get("id")
        if not isinstance(jid, str) or not jid.strip():
            failures.append(f"{prefix}.id must be non-empty")
        elif jid in seen:
            failures.append(f"{prefix}.id duplicate: {jid}")
        else:
            seen.add(jid)

        if journey.get("material") is not True:
            failures.append(f"{prefix}.material must be true for every inventoried certification journey")
        if journey.get("status") != "COMPROVADO":
            failures.append(f"{prefix}.status must be COMPROVADO")
        refs = journey.get("evidence_refs")
        if not isinstance(refs, list) or not refs or not all(isinstance(x, str) and x.strip() for x in refs):
            failures.append(f"{prefix}.evidence_refs must contain evidence")

        if journey.get("ui") is True:
            browser = journey.get("browser_e2e")
            if not isinstance(browser, dict):
                failures.append(f"{prefix}.browser_e2e required for UI journey")
                continue
            for field in [
                "real_browser",
                "graphical_session",
                "agent_executed",
                "same_release",
                "full_user_path",
                "reload_revisit",
                "persistence_checked",
                "console_checked",
                "network_checked",
                "visual_evidence",
                "no_user_delegation",
                "not_headless_only",
            ]:
                if browser.get(field) is not True:
                    failures.append(f"{prefix}.browser_e2e.{field} must be true")
        if journey.get("critical") is True and journey.get("contradictory_reaudit") is not True:
            failures.append(f"{prefix}.contradictory_reaudit must be true for critical journey")


def certify(data: dict) -> tuple[str, list[str]]:
    failures: list[str] = []

    if data.get("schema") != SCHEMA:
        failures.append(f"schema must be {SCHEMA}")

    validate_identity(data, failures)
    add_bool_failures(data, REQUIRED_TRUE, failures)
    add_zero_failures(data, REQUIRED_ZERO, failures)
    validate_journeys(data, failures)

    if get_path(data, "browser.required") is True:
        add_bool_failures(data, BROWSER_REQUIRED_TRUE, failures)

    if get_path(data, "deploy.required") is True:
        add_bool_failures(data, DEPLOY_REQUIRED_TRUE, failures)

    # Fail closed on any declared residual uncertainty that can invalidate certification.
    if get_path(data, "evidence.debt_count") not in (0, None):
        failures.append("evidence.debt_count must be 0")
    if get_path(data, "coverage.not_validated_count") not in (0, None):
        failures.append("coverage.not_validated_count must be 0")
    if get_path(data, "findings.preexisting_active_defects") not in (0, None):
        failures.append("findings.preexisting_active_defects must be 0")

    external = get_path(data, "remediation.blocked_external_count")
    if type(external) is int and external > 0:
        return "BLOCKED_EXTERNAL", failures or ["external blocker remains"]

    return ("APTO" if not failures else "NAO_APTO"), failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--json-output", type=Path)
    args = parser.parse_args()

    try:
        data = json.loads(args.manifest.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"AUDIT_CERTIFIER_ERROR={type(exc).__name__}: {exc}", file=sys.stderr)
        return 1

    verdict, failures = certify(data)
    report = {"schema": SCHEMA, "verdict": verdict, "failures": failures}

    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"AUDIT_VERDICT={verdict}")
    for item in failures:
        print(f"AUDIT_BLOCKER={item}")

    return 0 if verdict == "APTO" else (2 if verdict == "BLOCKED_EXTERNAL" else 1)


if __name__ == "__main__":
    raise SystemExit(main())
