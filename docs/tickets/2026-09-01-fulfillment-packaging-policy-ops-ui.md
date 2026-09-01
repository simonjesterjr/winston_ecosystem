# Ticket: Fulfillment Packaging Policy UI in Winston v2 operations

**Status:** Proposed  
**Priority:** P2  
**Date:** 2026-09-01  
**Mode:** contractor  
**Graph nodes:** winston_v2  
**Human gates:** policy edits are desk actions on the Operational Portfolio, not Broker Gateway  
**DoD:** Ops can set rule-based packaging on an OP; desk create-time default still works  
**Origin:** Grill 2026-09-01 Q4–Q5 — [`docs/session-reports/2026-09-01-1601-ibkr-paper-and-slate-grill.md`](../session-reports/2026-09-01-1601-ibkr-paper-and-slate-grill.md)

## Problem

**Fulfillment Packaging Policy** lives on the **Operational Portfolio** (Winston v2). It is rule-based (shares as-printed, round lot, long-dated calls, ask the human for a per-share price). Packaging may differ by Desk Action on the same lot (entrance LEAPs, pyramid shares). Later an LLM may compare allowed shapes without a new TradingStrategy fingerprint.

There is no Ops place to set this yet. Broker Gateway must not own it.

## Scope

1. Persist policy on the Operational Portfolio (JSON/rules, not a fingerprint).  
2. Winston v2 operations UI to view/edit.  
3. Desk (Quiver Tracking vs Trend Following) supplies create-time default only.  
4. At least one rule: ask the human for a per-share price.  
5. Confirm/book path can read the policy when choosing packaging.

## Non-goals

- LLM bakeoff of LEAP vs calendar spread (later)  
- Putting packaging choice in Broker Gateway  
- A second Daily Analysis signal for the fill symbol  

## Acceptance

- [ ] Policy stored on OP; spec for default + round-lot + ask-per-share-price  
- [ ] Ops page can edit without changing TradingStrategy fingerprint  
- [ ] Confirm path surfaces the policy (even if only as notes/prefill)
