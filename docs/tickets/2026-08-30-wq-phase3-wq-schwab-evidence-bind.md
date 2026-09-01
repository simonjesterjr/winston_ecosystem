# Ticket: WQ Phase 3 — bind WQ to Schwab as evidence (not send)

**Status:** Proposed  
**Priority:** P1  
**Date:** 2026-08-30  
**Mode:** contractor  
**Graph nodes:** winston_v2, broker_gateway  
**Edges:** `broker_binding_id` (Grill B Q8 thin); Confirmation Intake; Winston Broker Evidence Standard pull API  
**Human gates:** Capital Activation of a **new real** WQ series; one hand-placed Schwab fill; Desk Confirm  
**DoD:** paper #1372 stays dummy_sim; real WQ series bound read-only to Schwab; one human-placed fill books via Confirm  
**Series:** `production-ready-wq`  
**Plan:** [`plans/production-ready-wq.md`](../../plans/production-ready-wq.md) §7  
**Epic:** [`2026-08-30-production-ready-wq.md`](2026-08-30-production-ready-wq.md)  
**Monoliths:** winston_v2, broker_gateway  
**Blocked on:** Phase 1 green; Phase 2 adapter + spike verdict  

## Problem

WQ Plan Approve auto-books in Wv2. Confirmation Intake is empty and TF-shaped (`/operations/intake`). Grill B Q8 (OP ↔ broker account) is still “opaque column.” Wiring Schwab as **send** before a proven **read** round-trip would skip the L1 product we already built.

## Scope

Thin Q8 — enough to ship, not the full multi-OP-same-account design:

| OP | Binding |
|----|---------|
| Paper WQ #1372 | `dummy_sim` (from Phase 1) |
| New **real** WQ series (same recipe, new CashEvent) | `schwab_trader_api`, `order_write: false` |

1. Capital Activation of a new real WQ series (ADR-006). Do **not** flip #1372 to `execution_mode: real` in place.
2. Persist `broker_binding_id` on that series to the Schwab **read** binding.
3. Confirmation Intake must match WQ (desk or tracking page), not only TF ops shell.
4. Operator places **one** equity in Schwab/thinkorswim by hand → BG refresh → Trade Notification → prefill → **Desk Confirm** books that lot.
5. Auth-failed / needs-reauth visible on the WQ desk.
6. Broker balances remain reconciliation **hints**, never `capital_base`.

Supersedes [`2026-08-21-quiver-tracking-bg-fulfillment.md`](2026-08-21-quiver-tracking-bg-fulfillment.md) for the read/evidence slice.

## Non-goals

- Desk Send / `place_order`
- Auto-send of the Monday basket
- Mixing this Schwab login with Mint / TF Ops
- Full Q8 multi-OP allocation on one account
- L2 position/balance as capital source of truth

## Acceptance

- [ ] Paper #1372 still dummy_sim / paper
- [ ] Real WQ series exists with its own CashEvent and Schwab read binding
- [ ] One hand-placed fill appears as evidence JSONL and a Trade Notification
- [ ] Desk Confirm books that one lot; no silent book-from-API
- [ ] `order_write` still false on the Schwab binding
- [ ] Kill switch / auth failure is operator-visible

## Resume

Do not start until Phase 1 cycles are human-verified and Phase 2 fixtures + spike exist. First live proof is **read**, not send.
