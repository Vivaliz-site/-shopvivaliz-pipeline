#!/usr/bin/env python3
"""RED/GREEN tests for scripts/governance/check-issue-comment-listeners.py.

Governance invariant: ACTIVE_DIRECT_ISSUE_COMMENT_LISTENERS <= 1 per repository.
This guard scans .github/workflows for top-level `on: issue_comment` triggers
(skipping `.disabled` filenames and archive/historical directories) and fails
when more than one workflow declares a direct issue_comment listener.
"""
from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "governance" / "check-issue-comment-listeners.py"


def _load_module():
    spec = importlib.util.spec_from_file_location(
        "check_issue_comment_listeners", SCRIPT_PATH
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


TWO_LISTENERS_FIXTURE = {
    "workflow-a.yml": (
        "name: A\n"
        "on:\n"
        "  issue_comment:\n"
        "    types: [created]\n"
        "jobs:\n"
        "  x:\n"
        "    runs-on: ubuntu-latest\n"
        "    steps: []\n"
    ),
    "workflow-b.yml": (
        "name: B\n"
        "on: issue_comment\n"
        "jobs:\n"
        "  x:\n"
        "    runs-on: ubuntu-latest\n"
        "    steps: []\n"
    ),
    "workflow-c.yml": (
        "name: C\n"
        "on:\n"
        "  push:\n"
        "    branches: [main]\n"
        "jobs:\n"
        "  x:\n"
        "    runs-on: ubuntu-latest\n"
        "    steps: []\n"
    ),
}

ZERO_OR_ONE_LISTENER_FIXTURE = {
    "workflow-a.yml": (
        "name: A\n"
        "on:\n"
        "  issue_comment:\n"
        "    types: [created]\n"
        "jobs:\n"
        "  x:\n"
        "    runs-on: ubuntu-latest\n"
        "    steps: []\n"
    ),
    "workflow-b.yml": (
        "name: B\n"
        "on:\n"
        "  push:\n"
        "    branches: [main]\n"
        "  pull_request:\n"
        "    branches: [main]\n"
        "jobs:\n"
        "  x:\n"
        "    runs-on: ubuntu-latest\n"
        "    steps: []\n"
    ),
    "workflow-c.disabled.yml": (
        "name: C-disabled\n"
        "on:\n"
        "  issue_comment:\n"
        "    types: [created]\n"
        "jobs:\n"
        "  x:\n"
        "    runs-on: ubuntu-latest\n"
        "    steps: []\n"
    ),
    "archive/workflow-d.yml": (
        "name: D-archived\n"
        "on:\n"
        "  issue_comment:\n"
        "    types: [created]\n"
        "jobs:\n"
        "  x:\n"
        "    runs-on: ubuntu-latest\n"
        "    steps: []\n"
    ),
}


def _write_fixture(base: Path, files: dict) -> Path:
    workflows_dir = base / ".github" / "workflows"
    workflows_dir.mkdir(parents=True, exist_ok=True)
    for rel_path, content in files.items():
        target = workflows_dir / rel_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
    return workflows_dir


class IssueCommentListenerGuardTests(unittest.TestCase):
    def test_two_direct_listeners_fail(self):
        module = _load_module()
        with tempfile.TemporaryDirectory() as tmp:
            workflows_dir = _write_fixture(Path(tmp), TWO_LISTENERS_FIXTURE)
            count, matches = module.scan_workflows(workflows_dir)
            self.assertEqual(count, 2)
            names = sorted(Path(m).name for m in matches)
            self.assertEqual(names, ["workflow-a.yml", "workflow-b.yml"])
            self.assertEqual(module.evaluate(count), 1)

    def test_zero_or_one_listener_passes_and_skips_disabled_and_archive(self):
        module = _load_module()
        with tempfile.TemporaryDirectory() as tmp:
            workflows_dir = _write_fixture(Path(tmp), ZERO_OR_ONE_LISTENER_FIXTURE)
            count, matches = module.scan_workflows(workflows_dir)
            # only workflow-a.yml counts; the .disabled file and the
            # archive/ subdirectory must be skipped.
            self.assertEqual(count, 1)
            names = sorted(Path(m).name for m in matches)
            self.assertEqual(names, ["workflow-a.yml"])
            self.assertEqual(module.evaluate(count), 0)

    def test_real_repo_workflows_have_at_most_one_listener(self):
        module = _load_module()
        real_workflows_dir = ROOT / ".github" / "workflows"
        count, matches = module.scan_workflows(real_workflows_dir)
        self.assertLessEqual(
            count,
            1,
            f"ACTIVE_DIRECT_ISSUE_COMMENT_LISTENERS exceeded: {matches}",
        )


if __name__ == "__main__":
    unittest.main()
