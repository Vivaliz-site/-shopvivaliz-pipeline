#!/usr/bin/env python3
"""Governance guard: ACTIVE_DIRECT_ISSUE_COMMENT_LISTENERS <= 1.

Scans .github/workflows for workflow files that declare `issue_comment` as a
direct, top-level trigger (`on: issue_comment`, `on: [..., issue_comment]`, or
`on:` as a block mapping/list containing `issue_comment`).

Skips:
- filenames containing ".disabled"
- any directory whose name contains "archive" or "historical" (case-insensitive)

No third-party dependencies (no PyYAML) so it runs on a bare `setup-python`
runner without an install step. Parsing is intentionally minimal: it only
needs to recognize the direct top-level `on:` trigger declaration, not
arbitrary workflow YAML.

Exit code: 0 when count <= 1 (invariant held), 1 when count > 1.
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_WORKFLOWS_DIR = REPO_ROOT / ".github" / "workflows"


def _strip_quotes(token: str) -> str:
    token = token.strip()
    if len(token) >= 2 and token[0] == token[-1] and token[0] in ("'", '"'):
        return token[1:-1]
    return token


def _has_direct_issue_comment_trigger(text: str) -> bool:
    lines = text.splitlines()
    for i, line in enumerate(lines):
        # Top-level `on:` key only (no leading whitespace), ignoring comments.
        if not line.startswith("on:") and not line.startswith("on "):
            continue
        if not line.split("#", 1)[0].rstrip().rstrip(":").strip() == "on":
            # line looks like "on:" possibly with inline value after colon
            if ":" not in line:
                continue
        key_part, _, after = line.partition(":")
        if key_part.strip() != "on":
            continue
        after = after.split("#", 1)[0].strip()

        if after:
            # Inline scalar or flow list, e.g. `on: issue_comment`
            # or `on: [push, issue_comment]`.
            inline = after.strip("[]")
            tokens = [_strip_quotes(t) for t in inline.split(",")]
            if "issue_comment" in tokens:
                return True
            continue

        # Block form: gather sibling lines more indented than `on:`.
        base_indent = None
        j = i + 1
        while j < len(lines):
            raw = lines[j]
            stripped = raw.split("#", 1)[0]
            if stripped.strip() == "":
                j += 1
                continue
            indent = len(raw) - len(raw.lstrip(" "))
            if indent == 0:
                break
            if base_indent is None:
                base_indent = indent
            if indent < base_indent:
                break
            if indent == base_indent:
                entry = stripped.strip()
                if entry.startswith("- "):
                    item = _strip_quotes(entry[2:].strip())
                    if item == "issue_comment":
                        return True
                elif ":" in entry:
                    entry_key = entry.split(":", 1)[0].strip()
                    if entry_key == "issue_comment":
                        return True
            j += 1
    return False


def scan_workflows(workflows_dir: os.PathLike) -> tuple[int, list[str]]:
    workflows_dir = Path(workflows_dir)
    matches: list[str] = []
    if not workflows_dir.is_dir():
        return 0, matches
    for root, dirs, files in os.walk(workflows_dir):
        dirs[:] = [
            d for d in dirs
            if "archive" not in d.lower() and "historical" not in d.lower()
        ]
        for fname in files:
            if not (fname.endswith(".yml") or fname.endswith(".yaml")):
                continue
            if ".disabled" in fname:
                continue
            fpath = Path(root) / fname
            try:
                text = fpath.read_text(encoding="utf-8")
            except OSError:
                continue
            if _has_direct_issue_comment_trigger(text):
                matches.append(str(fpath))
    matches.sort()
    return len(matches), matches


def evaluate(count: int) -> int:
    return 1 if count > 1 else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dir",
        default=str(DEFAULT_WORKFLOWS_DIR),
        help="Path to .github/workflows to scan (default: repo's own).",
    )
    args = parser.parse_args(argv)

    count, matches = scan_workflows(args.dir)

    print(f"ACTIVE_DIRECT_ISSUE_COMMENT_LISTENERS={count}")
    if matches:
        print("Workflows with a direct top-level issue_comment trigger:")
        for m in matches:
            print(f"  - {m}")
    else:
        print("No workflow declares issue_comment as a direct top-level trigger.")

    exit_code = evaluate(count)
    if exit_code != 0:
        print(
            "FAIL: more than one active direct issue_comment listener "
            "(invariant ACTIVE_DIRECT_ISSUE_COMMENT_LISTENERS <= 1 violated).",
            file=sys.stderr,
        )
    else:
        print("PASS: ACTIVE_DIRECT_ISSUE_COMMENT_LISTENERS <= 1.")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
