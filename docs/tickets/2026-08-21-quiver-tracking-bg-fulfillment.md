# Ticket: Broker Gateway path for Quiver Tracking (future)

**Status:** Superseded  
**Priority:** P3  
**Date:** 2026-08-21  
**Monoliths:** broker_gateway (BG), winston_v2 (Wv2)  
**Blocked on:** tracking desk v1; L1 Confirmation Intake; fulfillment-write ADR (not current ADR-010) before `order_write`  
**See:** plan [`quiver-tracking-bg-fulfillment.md`](../../plans/quiver-tracking-bg-fulfillment.md)  
**Superseded by:** [`plans/production-ready-wq.md`](../../plans/production-ready-wq.md) Phases 3–4 (`2026-08-30-wq-phase3-wq-schwab-evidence-bind.md`, `2026-08-30-wq-phase4-one-at-a-time-send.md`)

## Problem

Eventually the tracking paper book may practice Confirmation Intake (`dummy_sim`) or, much later, a real series may send weekly reweights through Broker Gateway. **Not now.**

## Scope (when unblocked)

- Decision: dummy_sim rehearsal vs new real OP series (Capital Activation; same fingerprint)
- Human-Gated confirm still required
- Multi-name weekly reweight = one desk package, not N auto-sends
- BG never talks to Quiver

## Acceptance

- [ ] Written mode decision
- [ ] No `order_write` without ADR-010
- [ ] Tracking DA skip remains

## Non-goals

- Building this in the tracking-desk v1 slice
