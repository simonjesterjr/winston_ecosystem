# Ticket: WQ Phase 1 — paper cadence human-verify + glue

**Status:** In progress  
**Priority:** P1  
**Date:** 2026-08-30  
**Mode:** normal  
**Graph nodes:** winston_v2, broker_gateway  
**Edges:** dummy_sim `POST /sandbox_fills`; `#1372.broker_binding_id`  
**Human gates:** operator Approve / Reject / blow-away / flatten on `/quiver_tracking`  
**DoD:** two clean dummy_sim Monday cycles; flatten once on open lots; dummy_sim evidence for those names; dual-path cannot double-book; `broker_binding_id` persisted  
**Series:** `production-ready-wq`  
**Plan:** [`plans/production-ready-wq.md`](../../plans/production-ready-wq.md) §5  
**Epic:** [`2026-08-30-production-ready-wq.md`](2026-08-30-production-ready-wq.md)  
**Monoliths:** winston_v2 (primary), broker_gateway (evidence check)  

## Problem

Monday plan + dummy_sim sandbox_fills **code** landed 2026-08-28–30. Live desk has **not** Approved a plan. Operational Portfolio (OP) **#1372** has 0 lots, `broker_binding_id` nil, leftover per-leg `add_book` rail beside Plan Approve. Dummy_sim JSONL still only has 2026-08-10 SPY `exact`. Production-ready WQ cannot start Schwab work on an unverified paper loop.

## Live snapshot (2026-08-30)

- OP `#1372` `qtrack-cls-pdf-v1`, paper, $2,000, active, 0 positions, 0 journals
- Plan `#8` draft rebalance, 13 enters, fill 2026-08-31
- Snapshot `#4` target, 13 holdings
- BG dummy_sim `bnd_f1feaf2e361799fc3ecd610a`; head_cursor `2`

## Scope

1. Close issues:
   - [`docs/issues/2026-08-30-wq-dual-path-can-double-book.md`](../issues/2026-08-30-wq-dual-path-can-double-book.md) — **operator lock:** Approve locks; tasks execute 1-at-a-time; missing fill = per-leg HITL
   - [`docs/issues/2026-08-30-wq-shadow-op-nil-broker-binding.md`](../issues/2026-08-30-wq-shadow-op-nil-broker-binding.md)
2. Persist `#1372.broker_binding_id` to the seeded dummy_sim binding (do not rely on list-bindings fallback).
3. Canonical desk path = **Monday plan Approve** then **task Confirm**. Do not auto-book on Approve.
4. Operator **cycle A:** Approve plan #8 **or** blow-away + fresh paste + Approve — not both rails.
5. Verify lots book at next-open prices; WQ `trade.executed` events appear on the dummy_sim binding (`client_order_id` `wq-{planId}-{legId}`).
6. Operator **cycle B:** blow-away → paste → Approve again.
7. Once: flatten plan against **open lots** (not pending adds).
8. Tick acceptance on child tickets only after compose proof, not specs alone.

## Child tickets (code already on `main`)

| Ticket | Remaining |
|--------|-----------|
| [`2026-08-28-wq-monday-rebalance-plan.md`](2026-08-28-wq-monday-rebalance-plan.md) | Live acceptance boxes |
| [`2026-08-28-bg-dummy-sim-sandbox-fills.md`](2026-08-28-bg-dummy-sim-sandbox-fills.md) | Live sandbox_fills on dummy_sim (specs already green) |

## Non-goals

- Schwab OAuth / read adapter (Phase 2)
- Confirmation Intake as WQ booking spine (paper still auto-books after Plan Approve)
- `place_order` / `cap_order_write`
- Native Premium PDF parse

## Acceptance

- [ ] `#1372.broker_binding_id` = dummy_sim public_id
- [ ] Dual rail cannot book the same name twice in one cycle
- [ ] Cycle A: Approved plan → open lots match remaining legs; dummy_sim events for those symbols
- [ ] Blow-away clears paper tracking lots / journals / plans; Mint / real OPs refused
- [ ] Cycle B succeeds after blow-away
- [ ] Flatten on a populated book lists exits of open lots only
- [ ] Child 2026-08-28 tickets acceptance checked or explicitly deferred with reason

## Resume

Operator on `/quiver_tracking`. Agent watches BG events + Wv2 lots after Approve. Small code: binding persist + dual-path guard.
