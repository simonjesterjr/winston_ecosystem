# Ticket: Observe DUT DAY MKT queue when cash is closed

**Status:** Proposed  
**Priority:** P2  
**Date:** 2026-09-06  
**Mode:** contractor  
**Graph nodes:** broker_gateway, winston_v2  
**Edges:** ADR-013 § Consequences (overnight/queue must be verified on DUT)  
**Human gates:** Confirm click while the cash session is closed (weekend or after regular hours)  
**DoD:** written observation: DUT accepted / rejected / queued a regular-hours DAY MKT; WQ journal stayed working; no invented book  
**Series:** `production-ready-wq`  
**Plan:** [`plans/production-ready-wq.md`](../../plans/production-ready-wq.md)  
**Origin:** [`docs/session-reports/2026-09-06-1907-adr-013-wq-confirm-send.md`](../session-reports/2026-09-06-1907-adr-013-wq-confirm-send.md)  
**Related:** [`2026-09-06-wq-first-dut-confirm-send-proof.md`](2026-09-06-wq-first-dut-confirm-send-proof.md)

## Problem

Weekend Confirm is honest only if a regular-hours market Order Intent **queues** on Interactive Brokers paper DUT and fills at the next session print. ADR-013 forbids booking last close at the click. That queue behavior was not verified on DUT this session.

## Scope

1. With cash closed, Confirm-Send one small/known WQ command (prefer an already-chosen Monday exit, not a probe name).  
2. Record CPGW/IBKR response (order id, status, message).  
3. Record WQ journal status (`working` vs executed vs error).  
4. After the next regular session: fill vs reject vs cancel → Accept-Fill or attention.

## Non-goals

- Changing Time in Force without a new decision (WQ policy is regular-hours DAY MKT).  
- `outsideRTH: true`.  
- A second adapter.

## Acceptance

- [ ] Observation note in this ticket or a follow-on session report  
- [ ] If DUT rejects closed-cash MKT: desk copy / HITL path, not silent book  
- [ ] If DUT queues: first open print Accept-Fills  
