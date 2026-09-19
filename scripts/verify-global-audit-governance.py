#!/usr/bin/env python3
"""Verify ShopVivaliz audit-governance parity across all active repositories."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ORG = "Vivaliz-site"
CANONICAL = "site-shopvivaliz"
REPOSITORIES = [
    "site-shopvivaliz",
    "-shopvivaliz-pipeline",
    "amazon-returns-safet",
    "ml-pricing-api",
    "mercadolivre-returns-recovery",
    "shopvivaliz-m365",
]

EXACT_FILES = [
    "AUDIT_POLICY.md",
    "AGENTS.override.md",
    "docs/quality/EXTREME_AUDIT_PROTOCOL.md",
    "docs/quality/AUDIT_RUNTIME_PARITY_V1.md",
    "docs/quality/AUDIT_UNIVERSAL_COVERAGE_V1.md",
    "docs/quality/AUDIT_SELF_TEST_V1.md",
    "docs/quality/AUDIT_EVIDENCE_MANIFEST_TEMPLATE.md",
    "scripts/validate-audit-governance.py",
]

ENTRYPOINT_MARKERS = {
    "AGENTS.md": "AUDIT_UNIVERSAL_COVERAGE_V1.md",
    "CLAUDE.md": "AUDIT_UNIVERSAL_COVERAGE_V1.md",
    "GEMINI.md": "AUDIT_UNIVERSAL_COVERAGE_V1.md",
}

WORKFLOW_MARKERS = {
    "site-shopvivaliz": (".github/workflows/repository-governance.yml", "validate-audit-governance.py"),
    "-shopvivaliz-pipeline": (".github/workflows/repository-governance.yml", "validate-audit-governance.py"),
    "amazon-returns-safet": (".github/workflows/audit-governance.yml", "validate-audit-governance.py"),
    "ml-pricing-api": (".github/workflows/audit-governance.yml", "validate-audit-governance.py"),
    "mercadolivre-returns-recovery": (".github/workflows/audit-governance.yml", "validate-audit-governance.py"),
    "shopvivaliz-m365": (".github/workflows/audit-governance.yml", "validate-audit-governance.py"),
}

VERSION = "2026-09-19-universal-error-coverage-v4"


def fetch(repo: str, path: str, ref: str = "main") -> bytes:
    if repo == "-shopvivaliz-pipeline":
        ref = os.environ.get("AUDIT_FLEET_SELF_REF", ref)
    quoted = "/".join(urllib.parse.quote(part, safe="") for part in path.split("/"))
    url = f"https://raw.githubusercontent.com/{ORG}/{repo}/{ref}/{quoted}"
    request = urllib.request.Request(url, headers={"User-Agent": "shopvivaliz-audit-governance/1"})
    with urllib.request.urlopen(request, timeout=20) as response:
        return response.read()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def text(repo: str, path: str) -> str:
    return fetch(repo, path).decode("utf-8-sig")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("artifacts/global-audit-governance"))
    args = parser.parse_args()

    findings: list[dict[str, object]] = []
    canonical: dict[str, str] = {}

    for path in EXACT_FILES:
        try:
            canonical[path] = sha256(fetch(CANONICAL, path))
        except Exception as exc:
            findings.append({"repo": CANONICAL, "path": path, "kind": "canonical_fetch_failed", "detail": str(exc)})

    for repo in REPOSITORIES:
        try:
            policy = text(repo, "AUDIT_POLICY.md")
            if VERSION not in policy:
                findings.append({"repo": repo, "path": "AUDIT_POLICY.md", "kind": "version_drift", "detail": VERSION})
        except Exception as exc:
            findings.append({"repo": repo, "path": "AUDIT_POLICY.md", "kind": "missing_or_unreadable", "detail": str(exc)})

        for path, expected_hash in canonical.items():
            try:
                actual = sha256(fetch(repo, path))
                if actual != expected_hash:
                    findings.append({
                        "repo": repo,
                        "path": path,
                        "kind": "content_drift",
                        "detail": {"expected": expected_hash, "actual": actual},
                    })
            except Exception as exc:
                findings.append({"repo": repo, "path": path, "kind": "missing_or_unreadable", "detail": str(exc)})

        for path, marker in ENTRYPOINT_MARKERS.items():
            try:
                if marker not in text(repo, path):
                    findings.append({"repo": repo, "path": path, "kind": "bootstrap_marker_missing", "detail": marker})
            except Exception as exc:
                findings.append({"repo": repo, "path": path, "kind": "missing_or_unreadable", "detail": str(exc)})

        workflow_path, marker = WORKFLOW_MARKERS[repo]
        try:
            if marker not in text(repo, workflow_path):
                findings.append({"repo": repo, "path": workflow_path, "kind": "self_test_not_enforced", "detail": marker})
        except Exception as exc:
            findings.append({"repo": repo, "path": workflow_path, "kind": "missing_or_unreadable", "detail": str(exc)})

        try:
            overlay = text(repo, "docs/quality/AUDIT_OVERLAY.md")
            if "Extensões obrigatórias do projeto" not in overlay:
                findings.append({"repo": repo, "path": "docs/quality/AUDIT_OVERLAY.md", "kind": "overlay_contract_missing", "detail": "Extensões obrigatórias do projeto"})
        except Exception as exc:
            findings.append({"repo": repo, "path": "docs/quality/AUDIT_OVERLAY.md", "kind": "missing_or_unreadable", "detail": str(exc)})

    args.output_dir.mkdir(parents=True, exist_ok=True)
    report = {
        "schema": "AUDIT_CROSS_REPO_PROPAGATION_V1",
        "version": VERSION,
        "canonical_repository": f"{ORG}/{CANONICAL}",
        "repositories": REPOSITORIES,
        "exact_files": EXACT_FILES,
        "findings": findings,
        "status": "PASS" if not findings else "FAIL",
    }
    (args.output_dir / "report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = [
        "# Global Audit Governance Fleet",
        "",
        f"- version: {VERSION}",
        f"- canonical: {ORG}/{CANONICAL}",
        f"- repositories: {len(REPOSITORIES)}",
        f"- status: {report['status']}",
        "",
    ]
    if findings:
        lines.append("## Findings")
        for item in findings:
            lines.append(f"- {item['repo']} :: {item['path']} :: {item['kind']} :: {item['detail']}")
    else:
        lines.append("No governance drift detected.")
    (args.output_dir / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"GLOBAL_AUDIT_GOVERNANCE={report['status']}")
    if findings:
        for item in findings:
            print(json.dumps(item, ensure_ascii=False))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
