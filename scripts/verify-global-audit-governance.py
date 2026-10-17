#!/usr/bin/env python3
"""Verify Absolute Audit V5 governance across every repository in the canonical fleet."""

from __future__ import annotations

import argparse
import base64
import json
import os
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "docs/quality/GLOBAL_AUDIT_MANIFEST.json"
SELF_REF_ENV = "AUDIT_FLEET_SELF_REF"
TOKEN_ENV = "GH_TOKEN"


def load_manifest() -> dict:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def api_file(repo: str, path: str, ref: str) -> tuple[dict, bytes]:
    quoted_path = "/".join(urllib.parse.quote(part, safe="") for part in path.split("/"))
    quoted_ref = urllib.parse.quote(ref, safe="")
    url = f"https://api.github.com/repos/{repo}/contents/{quoted_path}?ref={quoted_ref}"
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "shopvivaliz-absolute-audit-fleet-v5",
        "X-GitHub-Api-Version": "2022-11-28",
        "Cache-Control": "no-cache",
    }
    token = os.environ.get(TOKEN_ENV, "").strip()
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=25) as response:
        payload = json.load(response)
    if not isinstance(payload, dict) or payload.get("type") != "file":
        raise RuntimeError(f"unexpected GitHub contents response for {repo}/{path}")
    content = payload.get("content", "")
    if payload.get("encoding") != "base64" or not isinstance(content, str):
        raise RuntimeError(f"missing base64 content for {repo}/{path}")
    return payload, base64.b64decode(content)


def repo_ref(repo: str, manifest: dict) -> str:
    if repo == manifest["canonical_repository"]:
        self_ref = os.environ.get(SELF_REF_ENV, "").strip()
        if self_ref:
            return self_ref
    return "main"


def add_finding(findings: list[dict], repo: str, path: str, kind: str, detail) -> None:
    findings.append({"repo": repo, "path": path, "kind": kind, "detail": detail})


def verify_repo(repo: str, manifest: dict, findings: list[dict]) -> None:
    ref = repo_ref(repo, manifest)

    try:
        _, raw_manifest = api_file(repo, "docs/quality/GLOBAL_AUDIT_MANIFEST.json", ref)
        remote_manifest = json.loads(raw_manifest.decode("utf-8-sig"))
        if remote_manifest != manifest:
            add_finding(findings, repo, "docs/quality/GLOBAL_AUDIT_MANIFEST.json", "manifest_drift", ref)
    except Exception as exc:
        add_finding(findings, repo, "docs/quality/GLOBAL_AUDIT_MANIFEST.json", "manifest_unreadable", str(exc))

    for path, expected_sha in manifest.get("required_blobs", {}).items():
        try:
            payload, _ = api_file(repo, path, ref)
            actual_sha = str(payload.get("sha", ""))
            if actual_sha != expected_sha:
                add_finding(
                    findings,
                    repo,
                    path,
                    "blob_drift",
                    {"expected": expected_sha, "actual": actual_sha, "ref": ref},
                )
        except Exception as exc:
            add_finding(findings, repo, path, "blob_unreadable", str(exc))

    for path, markers in manifest.get("required_entrypoint_markers", {}).items():
        try:
            _, raw = api_file(repo, path, ref)
            text = raw.decode("utf-8-sig")
            missing = [marker for marker in markers if marker not in text]
            if missing:
                add_finding(findings, repo, path, "entrypoint_markers_missing", missing)
        except Exception as exc:
            add_finding(findings, repo, path, "entrypoint_unreadable", str(exc))

    try:
        _, raw_requirements = api_file(repo, "docs/quality/AUDIT_PROJECT_REQUIREMENTS.json", ref)
        requirements = json.loads(raw_requirements.decode("utf-8-sig"))
        if requirements.get("schema") != "AUDIT_PROJECT_REQUIREMENTS_V1":
            add_finding(findings, repo, "docs/quality/AUDIT_PROJECT_REQUIREMENTS.json", "project_schema_invalid", requirements.get("schema"))
        if requirements.get("project") != repo:
            add_finding(findings, repo, "docs/quality/AUDIT_PROJECT_REQUIREMENTS.json", "project_identity_drift", requirements.get("project"))
        if requirements.get("policy_version") != manifest.get("version"):
            add_finding(findings, repo, "docs/quality/AUDIT_PROJECT_REQUIREMENTS.json", "project_policy_version_drift", requirements.get("policy_version"))
        if not requirements.get("required_invariants"):
            add_finding(findings, repo, "docs/quality/AUDIT_PROJECT_REQUIREMENTS.json", "project_invariants_missing", None)
    except Exception as exc:
        add_finding(findings, repo, "docs/quality/AUDIT_PROJECT_REQUIREMENTS.json", "project_requirements_unreadable", str(exc))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("artifacts/global-audit-governance"))
    args = parser.parse_args()

    manifest = load_manifest()
    findings: list[dict] = []

    if manifest.get("schema") != "GLOBAL_AUDIT_MANIFEST_V1":
        raise SystemExit("GLOBAL_AUDIT_MANIFEST_SCHEMA=FAIL")
    if not os.environ.get(TOKEN_ENV, "").strip():
        raise SystemExit("GLOBAL_AUDIT_FLEET_AUTH=FAIL missing GH_TOKEN")

    repositories = manifest.get("required_repositories", [])
    for repo in repositories:
        verify_repo(str(repo), manifest, findings)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    report = {
        "schema": "GLOBAL_AUDIT_FLEET_REPORT_V1",
        "version": manifest.get("version"),
        "canonical_repository": manifest.get("canonical_repository"),
        "repositories": repositories,
        "repository_count": len(repositories),
        "findings": findings,
        "status": "PASS" if not findings else "FAIL",
    }
    (args.output_dir / "report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    lines = [
        "# Global Audit Governance Fleet",
        "",
        f"- version: {report['version']}",
        f"- repositories: {report['repository_count']}",
        f"- status: {report['status']}",
        "",
    ]
    if findings:
        lines.append("## Findings")
        for item in findings:
            lines.append(f"- {item['repo']} :: {item['path']} :: {item['kind']} :: {item['detail']}")
    else:
        lines.append("No cross-repository governance drift detected.")
    (args.output_dir / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"GLOBAL_AUDIT_GOVERNANCE={report['status']} repositories={len(repositories)}")
    if findings:
        for item in findings:
            print(json.dumps(item, ensure_ascii=False))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
