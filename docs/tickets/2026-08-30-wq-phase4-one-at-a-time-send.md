# Ticket: WQ Phase 4 — one-at-a-time Schwab Desk Send + Confirm

**Status:** Proposed  
**Priority:** P1  
**Date:** 2026-08-30  
**Mode:** contractor  
**Graph nodes:** winston_v2, broker_gateway, ecosystem  
**Edges:** new fulfillment-write ADR (next free id); CapabilityGate `order_write`; Desk Send ≠ Desk Confirm  
**Human gates:** grill + accept write ADR; operator authorizes implementation; each live Send click  
**DoD:** Plan Approve queues legs; Send one → evidence → Confirm one; no basket `place_order`; paper never live write  
**Series:** `production-ready-wq`  
**Plan:** [`plans/production-ready-wq.md`](../../plans/production-ready-wq.md) §8  
**Epic:** [`2026-08-30-production-ready-wq.md`](2026-08-30-production-ready-wq.md)  
**Monoliths:** winston_v2, broker_gateway, ecosystem  
**Blocked on:** Phases 1–3 green; **write ADR accepted**; operator implementation auth  

## Problem

Paper Plan Approve auto-executes remaining legs at-market on dummy_sim (ADR-009 §11). That must **not** become a 13-name Schwab `place_order`. The production aim is one-at-a-time **Desk Send** (order entry) then **Desk Confirm** (book). L3 write is out of scope for L1 and is **not** current ADR-010 (that number is Risk Scale Meta-Layer).

Older tickets that say “no `order_write` until ADR-010” mean this **future** write ADR.

## Scope (when unblocked)

1. Grill + file the next-free-id fulfillment-write ADR: Confirm ≠ Send; fail closed; paper never live write; WQ does not inherit paper auto-execute onto Schwab; kill switch; audit; no Daily Analysis place; G20-style idempotent `client_order_key`.
2. Enable `order_write` **only** on the real WQ `schwab_trader_api` binding. dummy_sim and paper #1372 stay `order_write: false`.
3. After Plan Approve on the real series: remaining legs = **send queue**, not auto place.
4. Desk Send one name → BG `place_order` → poll fill → Confirmation Intake → Desk Confirm books that lot. Repeat.
5. Skip-line still omits a name. Reject leaves lots unchanged.
6. Mint / TF Ops stay Confirm-only on their bindings.
7. Contract tests: refuse basket send; refuse write on L1 profile; refuse write if kill switch / auth failed.

Supersedes [`2026-08-21-quiver-tracking-bg-fulfillment.md`](2026-08-21-quiver-tracking-bg-fulfillment.md) for the write slice.

## Non-goals

- L4 autotrader / policy send without click
- Resting Turtle session stops (separate blocked ticket)
- IBKR as first write adapter
- Silent accept-fill without Confirm (unless the write ADR later carves it)
- Implementing this ticket before Phases 1–3 and the ADR

## Acceptance

- [ ] Fulfillment-write ADR exists and is Accepted (new number, not 010)
- [ ] Operator explicitly authorizes L3 implementation
- [ ] Send one / Confirm one works on the real WQ series in a dedicated account
- [ ] Remaining Monday legs do not auto-place
- [ ] dummy_sim / paper #1372 still cannot `place_order`
- [ ] CapabilityGate + specs cover refuse-write paths

## Resume

Do **not** implement in the Phase 1 or Phase 2 sessions. Track only. Unblock when the plan §8 gates are true.
