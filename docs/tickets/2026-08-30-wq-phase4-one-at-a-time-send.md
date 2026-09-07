# Ticket: WQ Phase 4 — one-at-a-time Schwab Desk Send + Confirm

**Status:** Done  
**Priority:** P1  
**Date:** 2026-08-30  
**Mode:** contractor  
**Graph nodes:** winston_v2, broker_gateway, ecosystem  
**Edges:** ADR-013; CapabilityGate `order_write`; WQ IBKR-paper Confirm = Desk Send MKT + Accept-Fill at print  
**Human gates:** ADR-013 accepted (2026-09-06); each Confirm-Send click (paper DUT)  
**DoD:** Plan Approve queues legs; one Confirm-Send → working journal → DUT fill evidence → Accept-Fill at print; no basket; no live Schwab; IBKR adapter still fixtures limit/stop-market  
**Series:** `production-ready-wq`  
**Plan:** [`plans/production-ready-wq.md`](../../plans/production-ready-wq.md) §8  
**Epic:** [`2026-08-30-production-ready-wq.md`](2026-08-30-production-ready-wq.md)  
**Monoliths:** winston_v2, broker_gateway, ecosystem  
**Blocked on:** — implementation session 2026-09-06  

## Problem

Paper Plan Approve auto-executes remaining legs at-market on dummy_sim (ADR-009 §11). That must **not** become a 13-name Schwab `place_order`. The production aim is one-at-a-time **Desk Send** (order entry) then **Desk Confirm** (book). L3 write is out of scope for L1 and is **not** current ADR-010 (that number is Risk Scale Meta-Layer).

Older tickets that say “no `order_write` until ADR-010” mean this **future** write ADR.

## Scope (when unblocked)

1. ~~Grill + file fulfillment-write ADR~~ → **ADR-013** (2026-09-06). First write is IBKR **paper DUT**, not live Schwab.
2. Enable `order_write` **only** on the IBKR **paper** DUT binding used by WQ #1372. dummy_sim, live IBKR, and Schwab stay `order_write: false`.
3. After Plan Approve: remaining legs = **send queue** (exits, then rebalances, then enters), not auto place.
4. Tracking Confirm on that OP = Desk Send of one **market** Order Intent → journal **working** → BG poll fill → **Accept-Fill** at the print. Repeat. IBKR adapter must still transport limit and stop-market for a later paper Mint bind.
5. Skip-line still omits a name. Reject leaves lots unchanged.
6. Mint / TF Ops stay Confirm-only on their bindings.
7. Contract tests: refuse basket send; refuse write on L1 profile; refuse write if kill switch / auth failed.

Supersedes [`2026-08-21-quiver-tracking-bg-fulfillment.md`](2026-08-21-quiver-tracking-bg-fulfillment.md) for the write slice.

## Non-goals

- L4 autotrader / policy send without a Confirm click
- Resting Turtle session stops (separate ticket; same IBKR adapter must still **accept** stop-market Order Intents)
- Live Schwab or live IBKR `order_write`
- Hard-coding the IBKR adapter to market-only because WQ is market
- Basket Send; Daily Analysis `place_order`
- Implementing `place_order` in the ADR-draft session

## Acceptance

- [x] Fulfillment-write ADR exists and is Accepted — **ADR-013** (not 010)
- [x] Operator explicitly authorizes **implementation** of paper DUT write
- [x] One Confirm-Send → working journal → DUT fill → Accept-Fill at print (WQ paper)
- [x] Remaining Monday legs do not auto-place; exits before rebalances before enters
- [x] dummy_sim, live IBKR, and Schwab still cannot `place_order`
- [x] IBKR adapter fixtures include market **and** limit/stop-market Order Intents
- [x] CapabilityGate + specs cover refuse-write paths (cite ADR-013)

## Resume

Law is **ADR-013**. Paper DUT write shipped 2026-09-06: kill switch + `cap_order_write` on the DUT binding; WQ Confirm = Desk Send MKT; Accept-Fill at print.
