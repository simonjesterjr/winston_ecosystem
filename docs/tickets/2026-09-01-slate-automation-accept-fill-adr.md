# Ticket: Slate Automation + Accept-Fill ADR (leave discovery)

**Status:** Proposed  
**Priority:** P2  
**Date:** 2026-09-01  
**Mode:** contractor  
**Graph nodes:** ecosystem, winston_v2, broker_gateway  
**Human gates:** later grill; operator Q12 **D** — no calendar promotion  
**DoD:** ADR exists only after a later grill reopens whole-slate accept-fill or write ships  
**Blocked on:** discovery/learning mode; L3 `order_write`; [`2026-08-20-resting-session-stop-orders.md`](2026-08-20-resting-session-stop-orders.md)  
**Origin:** Grill 2026-09-01 Q9–Q12 — [`docs/session-reports/2026-09-01-1601-ibkr-paper-and-slate-grill.md`](../session-reports/2026-09-01-1601-ibkr-paper-and-slate-grill.md)

## Problem

CONTEXT now names **Slate Automation** (opt-in per Operational Portfolio + TradingStrategy fingerprint, policy-automatic Desk Send of a mechanical Session Order Slate) and discovery **Accept-Fill** of matched protective Working Stop prints only. That is glossary law ahead of write capability. An ADR is required before leaving discovery — not because “the paper week went well.”

## Scope

When a later grill (or write ADR) unblocks this:

1. ADR for Slate Automation flag, policy Send, halt / Desk Pass, DAR-as-review.  
2. Accept-Fill of protective stops (Stop-Out Reconciliation, warn on gap).  
3. Explicitly **not** whole-slate accept-fill unless that later grill locks Q11-C.  
4. Confirm ≠ Send; Daily Analysis still never opens Positions.

## Non-goals

- Shipping `order_write` in this ticket  
- Auto-booking entries or pyramids  
- Implying automation from paper, Active, or an Interactive Brokers bind  
- Winston Quiver Plan Approve changes  

## Acceptance

- [ ] Later grill or operator says leave discovery  
- [ ] ADR accepted  
- [ ] Sibling [`2026-09-01-whole-slate-accept-fill-later-grill.md`](2026-09-01-whole-slate-accept-fill-later-grill.md) still Proposed unless C is locked
