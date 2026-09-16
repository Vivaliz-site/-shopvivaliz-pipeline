# Global Audit Runtime Parity Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Eliminate audit false positives by making real deployed-runtime operation coverage, browser/server error gates, persistence verification, and local-vs-deployed test parity mandatory across every active project repository, then re-audit every active project under the new rule.

**Architecture:** The universal audit policy remains repository-local so every agent reads the rule without depending on a central service. A canonical rule block is replicated into `AUDIT_POLICY.md` and `docs/quality/EXTREME_AUDIT_PROTOCOL.md` in every active repository. Each project then runs a fresh audit tied to an exact SHA/release, records local/deployed coverage parity, executes real state-changing paths in the target environment when applicable, treats unexpected runtime/browser failures as fatal, and updates `docs/quality/AUDIT_STATUS.md` only after contradictory re-audit.

**Tech Stack:** GitHub repositories/Actions, project-specific test stacks, Playwright/browser E2E where UI exists, production/staging runtime evidence, database/queue/API verification where applicable.

**Spec:** User-approved cross-project governance design in the 2026-09-16 conversation; canonical requirements are materialized by Task 1 into `AUDIT_POLICY.md` and `docs/quality/EXTREME_AUDIT_PROTOCOL.md`.

## Global Constraints

- Active repositories in scope: `fredmourao-ai/mei-mg-email`, `fredmourao-ai/solange-rolla-consultorio`, `Vivaliz-site/site-shopvivaliz`, `Vivaliz-site/-shopvivaliz-pipeline`, `Vivaliz-site/amazon-returns-safet`, `Vivaliz-site/ml-pricing-api`, `Vivaliz-site/mercadolivre-returns-recovery`, `Vivaliz-site/shopvivaliz-m365`.
- `fredmourao-ai/solange-rolla` is archived/superseded by `fredmourao-ai/solange-rolla-consultorio`; do not spend execution capacity re-auditing the archived implementation.
- Never certify a deployed system from local-only tests or page-load checks.
- For UI projects, every applicable state-changing operation must be exercised through the real UI against the release/environment being certified; API/database shortcuts may verify effects but may not replace the UI operation.
- Unexpected HTTP 5xx, `pageerror`, `requestfailed`, or unexpected `console.error` is a failing audit gate unless explicitly allowlisted with evidence and justification.
- After a mutation, reload and revisit the entity, verify persisted UI state, and verify the underlying durable/externally observable effect when authorized.
- Local E2E inventory and deployed/staging E2E inventory must be compared. Any critical flow present locally but absent from deployed validation is evidence debt and blocks `APTO`.
- Every audit is tied to an exact commit/release/build and must distinguish `COMPROVADO`, `FORTE EVIDÊNCIA`, `HIPÓTESE A VALIDAR`, and `NÃO VALIDADO`.
- No destructive action without explicit authorization; prefer SAFE corrections and reproducible validation.

---

### Task 1: Propagate the audit-escape prevention rule

**Files:**
- Modify in every active repository: `AUDIT_POLICY.md`
- Modify in every active repository: `docs/quality/EXTREME_AUDIT_PROTOCOL.md`

**Interfaces:**
- Consumes: existing universal audit policy/protocol.
- Produces: binding `AUDIT_RUNTIME_PARITY_V1` rule text read by all agents and audits.

- [ ] **Step 1: Add the policy-level rule**

Add a section that requires real-operation runtime parity, fatal unexpected browser/server errors, post-mutation persistence checks, local-vs-deployed test inventory comparison, and system-wide protocol revision when an escaped defect exposes a missing audit class.

- [ ] **Step 2: Add the protocol-level execution checklist**

The protocol must explicitly require:

```text
operation inventory -> local coverage -> deployed coverage -> execute mutation -> fail on runtime/browser error -> reload/revisit -> verify durable effect -> correlate logs/trace -> contradictory rerun
```

- [ ] **Step 3: Verify the marker exists exactly once per file**

Expected marker:

```text
AUDIT_RUNTIME_PARITY_V1
```

Expected result: one occurrence in `AUDIT_POLICY.md` and one occurrence in `docs/quality/EXTREME_AUDIT_PROTOCOL.md` for each active repository.

- [ ] **Step 4: Merge without leaving pending governance PRs**

Use isolated branches, inspect diffs, merge cleanly, then verify the marker on each default branch.

### Task 2: Reconstruct each project and build an operation/coverage matrix

**Files:**
- Read: repository docs, code, tests, workflows, deploy/runtime configuration.
- Update after audit: `docs/quality/AUDIT_STATUS.md`.

**Interfaces:**
- Consumes: exact default-branch SHA and deployed release identity.
- Produces: per-project operation matrix and evidence debt list.

- [ ] **Step 1: Inventory user-visible and automated operations**

For each entity/workflow enumerate applicable operations such as create/read/update/delete/archive/restore/cancel/reopen/retry/approve/reject/confirm/reconcile/send/refund/appeal/deploy/rollback.

- [ ] **Step 2: Map each operation to tests**

Record:

```text
Operation | local automated coverage | deployed/staging coverage | manual/real-runtime evidence | durable-effect verification | error-gate coverage
```

- [ ] **Step 3: Treat gaps as findings, not assumptions**

A critical operation without deployed-runtime evidence is `NÃO VALIDADO` and blocks an `APTO` verdict.

### Task 3: Execute runtime-equivalent audits

**Files:**
- Project-specific E2E/integration tests and workflows as required by findings.
- `docs/quality/AUDIT_STATUS.md`.

**Interfaces:**
- Consumes: Task 2 operation matrix.
- Produces: real-runtime evidence for every applicable critical operation.

- [ ] **Step 1: Execute state-changing flows through the canonical interface**

For UI projects, use the real browser UI. For API/worker-only projects, use the production-equivalent public/worker interface and verify the durable result.

- [ ] **Step 2: Install/verify fatal runtime guards where applicable**

Browser E2E must fail on unexpected:

```text
HTTP 5xx
pageerror
requestfailed
console.error
```

Document any narrowly-scoped allowlist entry with reason and evidence.

- [ ] **Step 3: Verify persistence and side effects**

After each mutation, reload/revisit and verify both visible state and the durable/externally observable effect when accessible.

- [ ] **Step 4: Correlate failures**

Preserve trace/network/screenshot/log/correlation evidence sufficient to distinguish frontend, backend, database, provider, and infrastructure failures.

### Task 4: Correct findings and prove regression safety

**Files:**
- Project-specific production/test/config files implicated by findings.

**Interfaces:**
- Consumes: reproduced findings from Task 3.
- Produces: corrected behavior with before/after proof.

- [ ] **Step 1: Reproduce before modifying**

Record the failing operation and exact SHA/release.

- [ ] **Step 2: Apply the smallest safe correction**

Classify as `SAFE`, `REVIEW`, `MIGRATION`, or `DESTRUCTIVE`; do not execute destructive corrections without explicit authorization.

- [ ] **Step 3: Run layered validation**

Run the project-appropriate sequence:

```text
lint/typecheck -> focused test -> full relevant suite -> real-runtime smoke/E2E -> persistence/side-effect verification
```

- [ ] **Step 4: Search for the same failure class globally**

Do not close an escaped defect as isolated until equivalent patterns/routes/operations are searched.

### Task 5: Contradictory re-audit and certification

**Files:**
- Update in every active repository: `docs/quality/AUDIT_STATUS.md`

**Interfaces:**
- Consumes: completed fixes and runtime evidence.
- Produces: SHA-bound audit verdict and residual-risk statement.

- [ ] **Step 1: Attempt to break every previously passing critical operation again**

Use different records/states where possible and include failure/edge paths.

- [ ] **Step 2: Recompare local versus deployed coverage**

No critical local-only operation may remain silently outside the deployed audit suite.

- [ ] **Step 3: Update status**

Record exact SHA/release, findings, corrections, unvalidated areas, evidence debt, residual risk, and verdict `NÃO APTO`, `APTO COM RESSALVAS`, or `APTO`.

- [ ] **Step 4: Final cross-project reconciliation**

Confirm all eight active repositories have the rule, a fresh audit status under `AUDIT_RUNTIME_PARITY_V1`, and no false claim of full certification where runtime evidence remains missing.
