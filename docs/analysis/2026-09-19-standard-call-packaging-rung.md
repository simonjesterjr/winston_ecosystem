# Design note: `standard_call` as a Fulfillment Packaging rung (ADR-018)

**Date:** 2026-09-19  
**Status:** First-deliverable lock (selector + stamp; not IBKR Desk-Send)  
**Does not reopen:** ADR-017 Model B timing (precalc OCC at Signal/slate; Send verifies; no silent re-ATM)  
**Law:** [ADR-018](../adr/ADR-018-mode-c-leap-plan-a-plan-b.md) addendum 2026-09-19; [`mode-c-leap-plan-a-plan-b.md`](../business-context/mode-c-leap-plan-a-plan-b.md); [`leap-extra-modal-proxy.md`](../business-context/leap-extra-modal-proxy.md)  
**Ticket:** [`2026-09-19-standard-call-fulfillment-packaging-rung.md`](../tickets/2026-09-19-standard-call-fulfillment-packaging-rung.md)  
**Code owner:** Winston v2 (Wv2) selector + desk stamp. Broker Gateway (BG) only refuse OPT intent without `conid`. Winston Unit Test (WUT) lab parity is **out of scope**.

## One-sentence mapping

**Plan A** is the first entry in the Operational Portfolio (OP) **Fulfillment Packaging Policy** `packaging_preference` list. **Plan B** is the next *tradeable* entry when Plan A is untradeable (not auth). `standard_call` is a new call rung between Long-term Equity Anticipation Security (LEAP) and underlying stock — not a second Trading Strategy (TS) signal.

## Ladder → ADR-018 + existing flags

| Surface today | Meaning | Ladder mapping |
|---------------|---------|----------------|
| `leap_fulfillment=all` (Mode C paper) | Plan A = LEAP; Plan B = stock @ `signal_share_units` | Default `packaging_preference: [leap, stock]`, `allow_equity_fallback: true` |
| `leap_fulfillment=none` | No extra-modal call packaging | Preference omitted / `[stock]` — selector is not invoked |
| New `fulfillment_packaging_policy` jsonb | Ordered rungs + call knobs | Additive; empty hash **derives** from `leap_fulfillment` so Mode C books do not change |
| `allow_equity_fallback: false` | Do not stock | Walk call rungs only; if none tradeable → **clean refuse** (not units=0 LEAP cosplay, not silent stock) |
| Auth / session / Client Portal Gateway (CPGW) | Hard stop | No Plan B stamp (ADR-018 §3) |

Example policies (same TS/TF signal):

```yaml
# Mode C today (derived, not stored)
packaging_preference: [leap, stock]
allow_equity_fallback: true
leap_min_dte: 365

# LEAP then standard listed call then stock
packaging_preference: [leap, standard_call, stock]

# Standard call as Plan A (pin)
packaging_preference: [standard_call]
allow_equity_fallback: false
```

Stock is a **policy rung** (or `allow_equity_fallback`), never a side door inside the call selector.

## Selector split (one interface, two jobs)

1. **`CallFulfillmentSelector`** — LEAP and `standard_call` only, given a frozen or live chain. Output: contract (OCC / strike / expiry / right / contracts / optional conid) + `selection_trace`, or typed untradeable.
2. **`FulfillmentPackagingSelector`** — walks `packaging_preference` (Plan A then Plan B). Calls (1) per call rung; applies stock only from policy. Classifies **hard stop** vs **untradeable**. Builds Justification stamp.

Mode C paper journals and ADR-017 Interactive Brokers (IBKR) OPT Desk-Send **share** this selector. Destination differs: paper stamps the journal; live Send still requires Model B `conid` (parked ticket `2026-09-15-bg-ibkr-opt-order-intent-prove`).

## What does not change

- Signal Spine: entry / pyramid / exit / Working Stop on the **underlying** Market.
- Book Market, Daily Analysis, Portfolio Correlation Score (PCS) remain the underlying.
- Geometry A (stock STP fills as option) stays forbidden.
- No Black–Scholes fill-in when delta/quote is missing — that candidate is untradeable.
- WUT Portfolio Backtest Run (PBR) LEAP floor-refuse stays lab law until a separate ticket.

## First-deliverable wiring

| Piece | Where |
|-------|--------|
| Policy derive + jsonb | `Operations::FulfillmentPackagingPolicy`; `portfolios.fulfillment_packaging_policy` |
| Frozen-chain pick | `Operations::CallFulfillmentSelector` + `spec/fixtures/files/option_chains/ibm_frozen_chain.json` |
| Ladder + Justification hash | `Operations::FulfillmentPackagingSelector` |
| Flatten / roll / no auto-exercise | `Operations::CallLifecycle` |
| Desk POST stamp | `DeskWorkflowsController#related_details` (replaces leap-only resolver block) |
| Type vocabulary | `RelatedInstrumentFulfillment`: `standard_call` is option-like (multiplier 100) |
| BG | OPT `asset_class=option` without `conid` → refuse; stock-biased `resolve_conid` not used |

Confirm already stamps `conid` when a call resolves. Full OPT Desk-Send is **not** in this deliverable.
