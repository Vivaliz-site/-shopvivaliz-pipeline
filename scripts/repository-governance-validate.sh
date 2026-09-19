#!/usr/bin/env bash
set -Eeuo pipefail
root="$(git rev-parse --show-toplevel)"; cd "$root"
python_bin="${PYTHON_BIN:-}"
if [ -z "$python_bin" ]; then
  if command -v python3 >/dev/null 2>&1; then python_bin=python3; else python_bin=python; fi
fi
cache_dir="${TMPDIR:-/tmp}/repo-governance-pycache-$$"
trap 'rm -rf "$cache_dir"' EXIT
PYTHONPYCACHEPREFIX="$cache_dir" "$python_bin" -m compileall -q scripts
if [ "${1:-manual}" = "ci" ]; then
  PYTHONPYCACHEPREFIX="$cache_dir" "$python_bin" scripts/validate-audit-governance.py --output-dir artifacts/audit-governance-self-test
else
  PYTHONPYCACHEPREFIX="$cache_dir" "$python_bin" scripts/validate-audit-governance.py
fi
if [ "${1:-manual}" = "ci" ]; then
  GITHUB_REPOSITORY="Vivaliz-site/-shopvivaliz-pipeline" PYTHONPYCACHEPREFIX="$cache_dir" "$python_bin" scripts/validate-global-audit-policy.py --output-dir artifacts/global-audit-policy
else
  GITHUB_REPOSITORY="Vivaliz-site/-shopvivaliz-pipeline" PYTHONPYCACHEPREFIX="$cache_dir" "$python_bin" scripts/validate-global-audit-policy.py
fi
if [ -d tests ]; then PYTHONPYCACHEPREFIX="$cache_dir" "$python_bin" -m unittest discover -s tests -p 'test*.py'; fi