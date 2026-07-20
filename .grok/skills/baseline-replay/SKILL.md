---
name: baseline-replay
description: >
  Replay one scoped lab/ops comparison through baseline and candidate and
  classify differences. Use for WUT vs Wv2 parity, DM coverage vs consumer,
  backtest/DAR regressions, confirm-entry matrix cells, or journal/sizer drift.
  Invokes investigate-system-variance for unexplained differences. Triggers:
  "/baseline-replay", "parity replay", "compare baseline candidate".
metadata:
  short-description: "Scoped baseline vs candidate replay"
---

# Baseline replay (Winston lab/ops)

Run a **single scoped** baseline-versus-candidate comparison. Aggregate dashboards are not a substitute for one reproducible case.

## Load first

1. Owning `PROJECT_PROFILE.md` / `AGENTS.md` and `ecosystem/CONTEXT.md`
2. `investigate-system-variance` + its Winston `references/project-notes.md`
3. Relevant ADR / interface / handoff doc for the axis under test

## Procedure

### 1. Define scope and contract

Write down before running anything:

- **Axis:** handoff | signal/daily-analysis | data-coverage | journal/economics | agent-channel
- **Identity keys:** e.g. symbol + as-of date + strategy class + portfolio/PBR id
- **Baseline:** system, version/commit, config
- **Candidate:** system, version/commit, config
- **Governing contract:** ADR, interface, or expected behavior statement
- **Pass rule:** exact match | documented tolerance | known-difference list

### 2. Shared inputs

Prefer immutable artifacts:

- Pinned parquet / fixture dates
- Exported portfolio JSON under `portfolio_configs/`
- Committed RSpec fixtures
- Audit JSONL slices under `ecosystem/logs/audit/` for agent axes

Record source environment and capture time. External systems default **read-only**.

### 3. Execute both sides

Examples (adapt; do not invent flags):

| Axis | Baseline | Candidate | Helper |
|------|----------|-----------|--------|
| Signal lookback | WUT reference | Wv2 daily analysis path | `bin/verify-daily-analysis-parity` |
| Daily pipeline | prior known-good run | current compose | `bin/test-daily-pipeline` |
| Handoff | WUT export JSON | Wv2 import/ops portfolio | file + UI/API inspect |
| Coverage | DM DataCoverage + file | consumer skip/coverage | reconcile + consumer API |
| Agent | allowlist + skill intent | live MCP audit / Telegram | logs + `cron-tool-allowlist.json` |

Same clock, flags, and config on both sides unless the contract is “config change.”

### 4. Compare

- Side-by-side field table for the target identity
- Apply **only** documented exclusions (cite ADR/ticket)
- Large outputs → summary + small preview + searchable full artifact path

### 5. Route differences

- **Explained by known difference / intentional contract** → document; no defect
- **Unexplained** → `investigate-system-variance` (full classification + adversarial pass)
- **Confirmed defect** → `manage-issue-ticket` → when `ready`, `lightweight-bug-fix`

### 6. Report

- Scope, baseline/candidate identities, pass/fail vs threshold
- Largest consequential diffs
- Issue/ticket paths created
- Commands and artifact paths

## Guardrails

- Do not label aggregate drift a defect without one target case.
- Do not write production DBs or spam Telegram to “get a sample.”
- Do not cite dead code paths; verify the live entrypoint.
