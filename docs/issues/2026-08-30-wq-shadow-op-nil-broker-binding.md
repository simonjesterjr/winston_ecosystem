---
id: ISSUE-20260830-wq-shadow-op-nil-broker-binding
title: WQ shadow OP #1372 has nil broker_binding_id so dummy_sim fills are looked up at execute time
status: ready
type: bug
priority: medium
created: 2026-08-30
updated: 2026-08-30
labels: [wq, wv2, broker-gateway, binding, q8]
related:
  - 2026-08-30-wq-phase1-paper-cadence-verify
  - 2026-08-28-wq-monday-rebalance-plan
  - 2026-08-28-bg-dummy-sim-sandbox-fills
---

# WQ shadow OP #1372 has nil broker_binding_id so dummy_sim fills are looked up at execute time

**Status banner:** Ready — column exists; live OP unscoped; DummySimFills falls back to first dummy_sim binding

## Summary

Ticket `2026-08-28-wq-monday-rebalance-plan.md` scoped `broker_binding_id` on the WQ Shadow Portfolio. Live Operational Portfolio (OP) **#1372** still has `broker_binding_id` **nil**. `QuiverTracking::DummySimFills` lists Broker Gateway (BG) bindings and picks the first `dummy_sim` row. That is enough for a happy path today and will attach WQ evidence to the wrong binding once a Schwab row exists.

## Problem statement

Grill B Q8 is deferred as a full product, but the opaque OP → binding_id column already exists and is the only way sandbox_fills know which JSONL to append. A nil column plus “first dummy_sim in the list” is not a binding.

## Current behavior

- `portfolios.broker_binding_id` is nullable; #1372 is nil (rails runner 2026-08-30).
- `DummySimFills` uses `portfolio.broker_binding_id.presence` then `client.list_bindings` find-by `adapter_key == dummy_sim`.
- Seeded BG binding `bnd_f1feaf2e361799fc3ecd610a` is currently the only dummy_sim row, so the fallback would work **until** a second binding appears.
- Confirmation Intake matcher treats blank `broker_binding_id` as “any binding matches” (`match_notification.rb`).

## Expected behavior

Paper WQ #1372 has a persisted dummy_sim `broker_binding_id`. Plan Approve sandbox_fills go to that binding only. Later Schwab read bindings must not receive WQ paper fills. Intake must not treat blank as wildcard once WQ is bound.

Cite: `plans/production-ready-wq.md` Phase 1; CONTEXT Fulfillment adapter keys (`dummy_sim` default for paper).

## Reproduction

### Preconditions

Compose Wv2 + BG; OP #1372.

### Steps

1. `Portfolio.find(1372).broker_binding_id` → nil.
2. Read `QuiverTracking::DummySimFills#default_dummy_binding_id`.

### Observed result

`broker_binding_id` nil. Fallback list-bindings.

### Reproducibility

Always on current compose.

## Environment

Compose `winston_v2` + `broker_gateway` :3003. OP `#1372`. BG dummy_sim `bnd_f1feaf2e361799fc3ecd610a`. Wv2 `BROKER_GATEWAY_URL=http://broker_gateway:3000` in root `compose.yml`.

## Evidence

| Evidence | Source | What it establishes |
|---|---|---|
| `broker_binding_id: nil` | rails runner on #1372 2026-08-30 | Live gap |
| Fallback list-bindings | `winston_v2/app/services/quiver_tracking/dummy_sim_fills.rb` | Execute-time lookup |
| Blank binding matches any | `winston_v2/app/services/confirmation_intake/match_notification.rb` | Intake wildcard |
| Ticket already listed the column | `docs/tickets/2026-08-28-wq-monday-rebalance-plan.md` scope item 5 | Unfinished acceptance |
| Only dummy_sim binding today | `GET /api/v1/bindings` | Fallback is coincidentally unique |

## Impact and priority

Medium: paper loop still works with one dummy_sim row. Becomes a Phase 2/3 defect as soon as `schwab_trader_api` is a real binding. Fix in Phase 1 before that.

## Scope and preservation requirements

### In scope

- Persist dummy_sim binding id on #1372 (bootstrap / one-time runner / desk)
- DummySimFills fails closed if the OP has no binding (optional harden; at least stop picking “first dummy”)
- Do not treat blank binding as match-any for WQ once set

### Must preserve

- Q8 full multi-OP-same-account design remains deferred
- Secrets stay in BG
- `cap_order_write` false

### Out of scope

- Schwab OAuth
- Capital Activation / real series binding (Phase 3)
- Changing TF OP bindings

## Acceptance criteria

- [ ] Given OP #1372, when Plan Approve runs, then sandbox_fills POST uses the persisted dummy_sim `binding_id` (no list-bindings fallback required)
- [ ] Given a second BG binding (e.g. schwab stub row), when paper WQ executes, then events still append only on the dummy_sim binding
- [ ] Existing sandbox_fills specs still pass

## Investigation notes

Hypothesis: bootstrap / ingest never wrote the column after the Confirmation Intake migration added it (`20260819121000`).

## Unknowns and clarifying questions

- [ ] None blocking. Safe default: set #1372 to `bnd_f1feaf2e361799fc3ecd610a` and make bootstrap write it for new tracking OPs.

## Dependencies and risks

Phase 1 ticket. Phase 2 Schwab binding must not steal paper fills.

## Verification plan

Set column; Approve a plan (or spec with two bindings); `GET …/events` only on dummy_sim.

## History

- 2026-08-30 — Created from production-ready-WQ evaluation (live #1372 nil binding).
