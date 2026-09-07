# Ticket: Fulfillment Desk rebind / unbind waits on Q8

**Status:** Proposed  
**Priority:** P3  
**Date:** 2026-09-06  
**Mode:** contractor  
**Graph nodes:** winston_v2, broker_gateway  
**Human gates:** rebind is a desk action on the Operational Portfolio, not silent  
**DoD:** Operator can attach/detach an Adapter Binding from an OP on the Fulfillment Desk **after** Grill B Q8 (multi-OP same account) is locked  
**Origin:** Grill 2026-09-06 — Fulfillment Desk v1 is read-only  
**Blocked on:** Grill B Q8 (OP ↔ broker account). See `AdapterBinding` comments; `2026-08-09-bg-adapter-registry-and-capability-profile.md`; `2026-08-30-wq-phase3-wq-schwab-evidence-bind.md`

## Problem

Fulfillment Desk v1 is indication only. Wiring a new Schwab or live IBKR account still means a rails runner / seed, not a desk action. Q8 (multi-OP on one account, match ambiguity) is still deferred — do not invent a silent split.

## Scope

1. After Q8 is locked, add attach/detach on the Wv2 Fulfillment Desk (not in Broker Gateway HTML).  
2. Audit trail; refuse if it would mix evidence streams without a human gate.

## Non-goals

- Shipping rebind in the indication v1  
- Multi-OP auto-split without Q8  

## Acceptance

- [ ] Q8 product law written (business-context or ADR)  
- [ ] Desk can bind/unbind one OP to one Adapter Binding with a confirm  
