---
id: ISSUE-20260830-wq-dual-path-can-double-book
title: WQ Monday Plan Approve and leftover add_book tasks can double-book the same name
status: in-progress
type: bug
priority: high
created: 2026-08-30
updated: 2026-08-30
labels: [wq, wv2, quiver-tracking, desk, double-book]
related:
  - 2026-08-30-wq-phase1-paper-cadence-verify
  - 2026-08-28-wq-monday-rebalance-plan
  - ADR-009
---

# WQ Monday Plan Approve and leftover add_book tasks can double-book the same name

**Status banner:** In progress — operator lock 2026-08-30: Approve locks; tasks execute 1-at-a-time. Plan #8 auto-booked 12 lots then failed on BRK.B while 14 tasks stayed pending.

## Summary

Winston Quiver (WQ) ingest still mints per-leg gap tasks (`add_book` / `drop_book` / `reweight`) **and** builds a Monday Rebalance Plan. Plan Approve auto-books remaining legs. Confirming the gap tasks in the same cycle can open the same name twice on paper Operational Portfolio (OP) #1372.

## Problem statement

The tracking desk exposes two fulfillment verbs for one published book. Single Fulfillment Identity (ADR-009) requires one work item per leg. The leftover per-leg rail was the v1 tracking desk; Monday plan is now the canonical Human-Gated verb.

## Current behavior

- Ingest (`QuiverTracking::Ingest`) builds a `QuiverRebalancePlan` **and** still runs the task minter path (child ingest job / `TaskMinter`).
- `/quiver_tracking` shows Monday plan **and** pending population / confirm forms.
- `PlanExecute` calls `Population.add_book` + `Population.confirm` for each remaining enter.
- Per-leg confirm on an `add_book` task uses the same population spine.

Live 2026-08-30: plan #8 is still `draft`, 0 journals — double-book has not been observed on compose yet because Approve has not been clicked.

## Expected behavior

One cycle, one path. Canonical: **Monday plan**. Confirming leftover gap tasks while a draft/approved/executing plan exists for those names should refuse (or the minter should not create add/drop/reweight tasks when a plan is the product). Flatten vs rebalance remain exclusive.

Cite: CONTEXT **Monday Rebalance Plan** / **Plan Approve**; ADR-009 §11; `plans/production-ready-wq.md` Phase 1.

## Reproduction

### Preconditions

Compose Wv2 + WQ OP #1372; a target snapshot with N names; a draft Monday plan; pending `add_book` tasks for the same names.

### Steps

1. Open `/quiver_tracking`.
2. Approve the Monday plan (auto-books remaining enters).
3. Confirm the leftover `add_book` tasks (or reverse the order).

### Observed result

Not yet fired on live compose (plan #8 unapproved). Code paths both call `Population.add_book` / `confirm` for the same ticker. Session report `2026-08-30-1326-wq-paste-monday-plan.md` §9 named this risk.

### Reproducibility

Investigation-only until Approve; always available as two UI rails.

## Environment

`winston_v2` compose, OP `#1372`, plan `#8` draft, snapshot `#4` (13 holdings). Branch `main` after `aad8cb8`.

## Evidence

| Evidence | Source | What it establishes |
|---|---|---|
| Plan Approve auto-books via Population | `winston_v2/app/services/quiver_tracking/plan_execute.rb` | First booking path |
| Pending confirm forms still on the desk | `winston_v2/app/views/quiver_tracking/_pending.html.erb`, `_population_forms.html.erb` | Second booking path |
| Ingest still mints plans **and** tasks | `winston_v2/spec/jobs/quiver_tracking_ingest_job_spec.rb` (plan count + prior task minter) | Dual emit |
| Named residual risk | `ecosystem/docs/session-reports/2026-08-30-1326-wq-paste-monday-plan.md` §9 | Operator/session awareness |

## Impact and priority

Paper only today (WQ shadow is paper). Double-book poisons the tracking book and any later Schwab mapping. Priority **high** because Phase 1 Approve is the next operator click.

Workaround: Approve the plan **or** confirm add_book tasks — never both. Blow-away if it happens.

## Scope and preservation requirements

### In scope

- One canonical path per cycle on the tracking desk
- Refuse or hide the conflicting rail when a plan is actionable / executing / just executed

### Must preserve

- Plan Approve auto-execute on **paper** tracking (ADR-009 §11)
- Blow-away on paper tracking only
- Flatten vs rebalance exclusive calendar
- Mint / TF desks unchanged

### Out of scope

- Schwab `place_order`
- Deleting paste ingest
- Changing TF Desk Confirm

## Acceptance criteria

- [ ] Given Plan Approve, when the desk is refreshed, then no new Positions exist until a task is Confirmed
- [ ] Given Confirm of one `add_book` task, then that one lot opens and current book shows it
- [ ] Given a name with no fill price, when the plan is Approved, then that row is HITL and the plan is still `approved`
- [ ] Existing plan_approve_spec and ingest specs still pass
- [ ] Mint / real OPs still cannot use WQ blow-away / auto-fill

## Investigation notes

Operator lock 2026-08-30: both rails stay, with split verbs. Plan Approve **locks** the package. Tracking tasks **execute** one at a time. Auto-book on Approve was the defect (plan #8 booked 12 lots then `failed` on BRK.B).

## Unknowns and clarifying questions

- [ ] Operator preference if both rails must remain visible for a transition week (safe default: Monday plan canonical; per-leg rail refuses when a covering plan exists)

## Dependencies and risks

Phase 1 ticket `2026-08-30-wq-phase1-paper-cadence-verify.md`. Approving plan #8 without this guard is the live risk.

## Verification plan

Compose: blow-away residue → paste → Approve (no lots) → Confirm one task (one lot). Specs: `plan_approve_spec`.

## History

- 2026-08-30 — Created from production-ready-WQ Phase 1 evaluation (live OP #1372, plan #8 draft).
- 2026-08-30 — Operator after Approve: auto-book filled Positions/journals; 14 HITL tasks remained; BRK.B `missing_fill_price` failed the whole plan. Product correction: Approve does not book; HITL is per-leg; Confirm books one lot.
