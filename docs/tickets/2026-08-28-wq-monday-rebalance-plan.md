# Ticket: WQ Monday rebalance plan → Plan Approve → dummy_sim execute

**Status:** In progress  
**Priority:** P1  
**Date:** 2026-08-28  
**Monoliths:** winston_v2 (primary), broker_gateway (sandbox fills), ecosystem  
**Plan:** [`plans/wq-shadow-monday-plan.md`](../../plans/wq-shadow-monday-plan.md)

## Problem

Quiver Tracking mints per-leg gap tasks on PDF ingest. The operator wants: Monday (or test-anytime) **TXT/PDF ingest → one plan** (exits with P/L, ±% rebalances, enters) → **whole-plan Approve/Reject** → auto-execute at **next session open** on dummy_sim → **blow-away** and retry. Exclusive flatten mode is the other calendar policy.

## Scope

1. One paper **WQ Shadow Portfolio** (`/quiver_tracking`). DA skipped.
2. Ingest TXT or PDF; build `QuiverRebalancePlan` (do not mint add/drop/reweight tasks).
3. Desk: Approve / Reject / skip-line+reason; Mode A flatten plan; test blow-away (paper tracking OP only).
4. After Approve: dummy_sim sandbox fills + auto-book lots. Live Schwab write is **not** this ticket.
5. `broker_binding_id` on the shadow OP (Grill B Q8 column already exists).

## Non-goals

- Turtle-from-PDF OP, PCS gates, top-4 slim policy
- Auto-send on Mint / Ops TF
- Live Schwab `place_order`
- Native Premium PDF extraction (still HITL / sidecar; TXT is the test path)

## Acceptance

- [ ] TXT → draft plan with exits/rebalances/enters
- [ ] Approve books next-open lots on the shadow OP
- [ ] Reject unchanged; skip-line omits that leg
- [ ] Blow-away clears paper tracking lots/journals/plans; second cycle works
- [ ] Flatten mode produces all-exit plan
- [ ] Mint / real OPs cannot blow-away or auto-fill
