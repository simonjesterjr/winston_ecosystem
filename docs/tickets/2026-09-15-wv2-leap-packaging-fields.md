# Ticket: Wv2 — attach proposed OCC packaging to handoff/slate (Model B)

**Status:** Proposed  
**Priority:** P1  
**Date:** 2026-09-15  
**Mode:** contractor  
**Graph nodes:** winston_v2 (primary); broker_gateway (read resolve only); winston_unit_test (sizing skeleton reuse only)  
**Human gates:** paper DUT only; no option Desk Send in this ticket; agent never Desk-Sends; no pack promotion  
**DoD:** Signal/slate (or Confirm packaging step) stamps Model B LEAP fields on handoff / `fulfillment_details` so Desk Approve sees OCC / optional conid / premium cash outlay while Book Market stays the underlying  
**Origin:** Plan [`plans/wv2-bg-ibkr-leap-fulfillment.md`](../../plans/wv2-bg-ibkr-leap-fulfillment.md) Phase 1; ADR-017 Proposed; analysis inventory [`2026-09-15-wv2-bg-ibkr-leap-fulfillment-plan.md`](../analysis/2026-09-15-wv2-bg-ibkr-leap-fulfillment-plan.md)  
**Related:** domain law [`leap-extra-modal-proxy.md`](../business-context/leap-extra-modal-proxy.md); sticky 20D_BO [`turtle-s2-pyramid-and-working-stop.md`](../business-context/turtle-s2-pyramid-and-working-stop.md); parent [`spending-capacity-and-leap-fulfillment.md`](../../plans/spending-capacity-and-leap-fulfillment.md); read-only 1×1 [`2026-09-09-extra-modal-leap-unit-evaluation.md`](2026-09-09-extra-modal-leap-unit-evaluation.md); BG prove [`2026-09-15-bg-ibkr-opt-order-intent-prove.md`](2026-09-15-bg-ibkr-opt-order-intent-prove.md); packaging UI [`2026-09-01-fulfillment-packaging-policy-ops-ui.md`](2026-09-01-fulfillment-packaging-policy-ops-ui.md); ADR-009; ADR-013; ADR-017

## Problem

Wv2 can book extra-modal packaging types, but Desk Send / slate today build **stock** intents (no OPT fields / conid). Model B requires the candidate LEAP to be **stamped before Send** so HITL Approve is not blind and BG never stock-resolves a LEAP ticker.

## Scope

1. Extend `fulfillment_details` / Desk Handoff (and slate leg metadata when used) with Model B fields from the plan/analysis Phase 1 table: `fulfillment_type: leap`, strike/expiry/right, `leap_atr_offset`, `leap_expiration_days`, `contracts`, optional `ibkr_conid`, OCC / `instrument_label`, `packaging_resolved_at`, `underlying_last_at_resolve`, `signal_market` (underlying ≠ OCC).  
2. Packaging path reuses WUT **contract-count** math (`desired_shares/100` floor); refuse contracts = 0.  
3. Optional: call BG read resolve for candidate conid/snapshot when CPGW up — **not** Black-Scholes for paper/live eval.  
4. Desk Workflow UI surfaces instrument_label, premium snapshot, cash outlay vs share notional, SC remaining (SC Check may be stubbed if Part 1 not live — call out gap).  
5. Journal / Book Market remains underlying; no DA inventing OPT Positions; no retargeting Books to OCC.

## Non-goals

- Option Desk Send / `place_order` (BG ticket + grill)  
- Silent re-ATM at Send  
- Protective option STP  
- Pack promotion / Capital Activation  
- Rewriting Part 1 Spending Capacity  
- Treating WUT BS as live Edge

## Acceptance

- [ ] Specs prove Model B fields stamp on handoff/slate path; Book Market unchanged  
- [ ] UI (or equivalent desk surface) shows OCC / label / cash outlay before any Send  
- [ ] Missing/zero contracts refuse packaging  
- [ ] No OPT `place_order` shipped by this ticket  
- [ ] Cross-links to plan + ADR-017 + leap-extra-modal-proxy remain accurate

## Gates

- Paper DUT only for any broker read used to resolve candidates.  
- Grill / ADR-017 accept recommended before treating stamps as production desk law.  
- Option Desk Send still blocked until SC + 1×1 + grill (parent + 2026-09-09 ticket).
