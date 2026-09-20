# Ticket: Add non-LEAP long-call as a third Fulfillment Packaging path (Wv2)

**Status:** In progress  
**Priority:** P1  
**Date:** 2026-09-19  
**Mode:** contractor  
**Graph nodes:** winston_v2 (`LeapCandidateResolver`, desk workflow stamp, Justification); broker_gateway (OPT intent `conid` refuse); ecosystem ADR-018  
**Implementer:** Winston Dev  
**Human gates:** Mode C paper first; agent never Desk-Sends options; no pack promotion; no WUT lab parity unless asked  
**DoD (first deliverable):** design note; `CallFulfillmentSelector` + frozen-chain fixtures; Wv2 packaging stamp + Justification copy for `standard_call`; listed tests green. BG OPT Desk-Send **not** required beyond missing-`conid` refuse.  
**Origin:** Operator ticket 2026-09-19 (standard listed call as packaging rung)  
**Related:** ADR-018 + addendum; ADR-017 (unchanged Model B timing); [`../analysis/2026-09-19-standard-call-packaging-rung.md`](../analysis/2026-09-19-standard-call-packaging-rung.md); Mode C [`2026-09-18-mode-c-leap-preferred-underlying-fallback.md`](2026-09-18-mode-c-leap-preferred-underlying-fallback.md); BG OPT prove [`2026-09-15-bg-ibkr-opt-order-intent-prove.md`](2026-09-15-bg-ibkr-opt-order-intent-prove.md)

## Goal

Extend **Fulfillment Packaging Policy** so an Operational Portfolio / Trading Strategy that today prefers Long-term Equity Anticipation Security (LEAP) packaging can also prefer (or fall through to) **standard (non-LEAP) long calls**, with underlying stock remaining a packaging choice — without touching core Trend Following (TF) signal engines.

Three packaging instruments, same signal:

1. **LEAP** — listed call with DTE ≥ `leap_min_dte` (default 365)
2. **Standard long call** — listed call with DTE in `[standard.min_dte, leap_min_dte)` — **NEW**
3. **Underlying stock/ETF** — Plan B instance when preferred call packaging is untradeable and policy permits

## Non-goals

- Short calls, credit spreads, iron condors, Level 3/4 multi-leg
- Changing TS/TF signal, pyramid Average True Range (ATR) geometry, or Working Stop law
- Silent Plan B on auth/session/Client Portal Gateway (CPGW) failure
- Geometry A; Book/Daily Analysis/PCS retargeted onto the OCC symbol
- WUT lab Plan-B parity

## First deliverable (this ticket)

- [x] Design note mapping ladder → ADR-018 Plan A/B + `leap_fulfillment`
- [x] Selector interface + frozen-chain fixtures
- [x] Wv2 packaging stamp + Justification copy for `standard_call`
- [x] Tests (ladder, refuse, sizing, flatten/roll, frozen OCC, auth hard-stop, BG missing conid)
- [x] BG OPT Desk-Send **deferred** (Confirm stamps `conid`; prove ticket still parked)

**Not in this slice:** Winston Unit Test (WUT) lab parity; Interactive Brokers (IBKR) OPT Desk-Send / `place_order` (still `2026-09-15-bg-ibkr-opt-order-intent-prove`). Confirm already stamps `conid` when a call resolves; BG now **refuses** `asset_class=option` without `conid` so stock-biased resolve cannot run.
