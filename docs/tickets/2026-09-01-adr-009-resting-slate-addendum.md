# Ticket: ADR-009 addendum — next-open lab default vs live resting slate

**Status:** Proposed  
**Priority:** P2  
**Date:** 2026-09-01  
**Mode:** contractor  
**Graph nodes:** ecosystem, winston_unit_test, winston_v2  
**Human gates:** do not rewrite ADR-009 until this ticket is accepted  
**DoD:** ADR-009 point 3 addendum published; CONTEXT and the resting-slate ticket agree  
**Series:** `trade-fulfillment-engine`  
**Origin:** Grill 2026-09-01 Q7 — [`docs/session-reports/2026-09-01-1601-ibkr-paper-and-slate-grill.md`](../session-reports/2026-09-01-1601-ibkr-paper-and-slate-grill.md)

## Problem

ADR-009 §3 still says the default End of Day fill story is Signal Date T → Fill Date T+1 **next session open**. Grill Q7 locked the **live Trend Following** loop as a **Session Order Slate** of stop-market parks (entry, pyramid, protective Working Stop), with risk at the **Moment of Truth**. Next-open stays the **lab** default until a TradingStrategy is fingerprinted on resting-touch.

Leaving both sentences in force without an addendum will make implementers mix enter-at-open-100 with a 102 stop from the unfilled breakout (already rejected).

## Scope

1. Add an ADR-009 addendum (do not silently replace point 3).  
2. Lab / paper default: next-open (`next_bar_open`).  
3. Live TF target: Session Order Slate; unfilled entries/pyramids cancel at close; protective Working Stops replace overnight.  
4. Cross-link [`2026-08-20-resting-session-stop-orders.md`](2026-08-20-resting-session-stop-orders.md) and [`2026-08-20-wut-resting-stop-touch-fill-cadence.md`](2026-08-20-wut-resting-stop-touch-fill-cadence.md).

## Non-goals

- Implementing L3 Desk Send or parking orders  
- Changing Winston Quiver Plan Approve  
- Whole-slate accept-fill  

## Acceptance

- [ ] ADR-009 addendum accepted  
- [ ] CONTEXT flagged “Live TF session cycle” points at the addendum  
- [ ] Resting-session ticket cites the addendum instead of “ADR-009 next-open only”
