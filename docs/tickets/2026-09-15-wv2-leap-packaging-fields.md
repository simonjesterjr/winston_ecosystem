# Ticket: Wv2 — attach proposed OCC packaging to handoff/slate (Model B)

**Status:** In progress  
**Priority:** P1  
**Date:** 2026-09-15 (amended 2026-09-18 — Mode C paper desk prefill)  
**Mode:** contractor  
**Graph nodes:** winston_v2 (primary); broker_gateway (read resolve only); winston_unit_test (sizing skeleton reuse only)  
**Human gates:** Mode C paper OPs only; no option Desk Send; agent never Desk-Sends; no pack promotion; no Mint #384 conversion  
**DoD:** On `leap_fulfillment=all` paper OPs, DA + Desk **GET** stamp LEAP packaging (OCC / real conid / premium / contracts / cash outlay). Confirm books `premium × 100 × contracts`. Book Market stays the underlying.  
**Origin:** Plan [`plans/wv2-bg-ibkr-leap-fulfillment.md`](../../plans/wv2-bg-ibkr-leap-fulfillment.md) Mode C + Phase 1; ADR-017 Proposed; GC plan 2026-09-18  
**Related:** BG quotes [`2026-09-18-bg-option-candidates-quotes.md`](2026-09-18-bg-option-candidates-quotes.md); domain [`leap-extra-modal-proxy.md`](../business-context/leap-extra-modal-proxy.md); WUT cash identity [`../../../winston_unit_test/docs/tickets/2026-09-14-wut-leap-packaged-pbr-faithful-sim.md`](../../../winston_unit_test/docs/tickets/2026-09-14-wut-leap-packaged-pbr-faithful-sim.md); OPT send **parked** [`2026-09-15-bg-ibkr-opt-order-intent-prove.md`](2026-09-15-bg-ibkr-opt-order-intent-prove.md)

## Operator lock (2026-09-18)

Mode C paper HITL is **End of Day / after the cash session**. It is OK to simulate entrance/exit at **intra-day Client Portal Gateway (CPGW) prints**. CPGW is required so the stamped premium is the **close (last/mid) that would have executed** in an automated environment — not next-open share price.

Entry remains human Confirm (pre-filled). Stop-out remains auto paper sell-to-close at **option mark**.

## Problem

Mode C paper OPs (`leap_fulfillment=all`, dummy_sim, bind nil — live **#1574–1578, #1581–1584**) still draft **stock** share-notional (e.g. Orange #1576 AAPL flow −$13,533). `LeapCandidateResolver` runs on Confirm POST only; Desk GET prefills share next-open; DA `TaskGenerator` hardcodes `fulfillment_type: "stock"`. Confirm can debit share-like cash if price is the underlying.

## Scope

1. DA `TaskGenerator`: on Mode C paper enter/pyramid, draft `fulfillment_type=leap` and stamp Model B fields via resolver (BG `option_candidates` frozen contract). Signal-path share units stay in details for heat/WS. If CPGW down: `leap_resolution_failed`, **do not** pretend the fill is stock.  
2. Desk **GET** prefills: type=leap, OCC/conid, strike, expiry ≥~730d ATM, **units=contracts**, **price=premium** (CPGW last/mid = simulated automated close), cash outlay, underlying share unit + Working Stop **beside**.  
3. Contract math: WUT `floor(desired_shares/100)`; refuse 0. Affordability: `premium×100×contracts` vs paper `capital_base`.  
4. Confirm: `RelatedInstrumentFulfillment` leap flow; Position `is_option`; Journal Market = underlying.  
5. Pyramids: same packaging (`all`); pyramid distance on underlying fill.  
6. Stop-out auto STC: option mark (CPGW quote, or labeled last stamped premium) — **never** underlying Working Stop × 100.  
7. `leap_fulfillment=all` + untradeable → banner; Confirm stock requires `force` + note.  
8. Resolver: target tenor **730**; prefer listed ≥730 else longest ≥365; CALL if long / PUT if short; send `min_days_to_expiry` **and** `expiry_min_days`. Spot for ATM = parquet/underlying last — **not** the form premium field.

## Non-goals

- Option Desk Send / `place_order`  
- Silent re-ATM at Confirm  
- Protective option STP  
- Pack promotion / Capital Activation  
- Converting Mint **#384**  
- Walnut IBKR write  
- Treating WUT Black-Scholes as live Edge  
- Full Exit Capital Reconcile ±$D vs share-story (follow-on `2026-08-05-…`)

## Acceptance

- [x] Desk GET / DA stamp on a Mode C enter draft selects leap; units=contracts; price=premium; cash = premium×100×n (Blue #1574 RXT journal 1914: 8×$2.30×100 = $1,840)  
- [ ] Confirm books leap cash; Position is option; Book symbol unchanged — **operator Confirm still pending**  
- [x] Zero contracts / empty quote refuse packaging (no silent stock) — Orange #1576 AAPL journal 1915: 40 shares → `zero_contracts`  
- [x] Auto STC uses option mark (specs)  
- [x] #384 and Walnut unchanged  
- [x] No OPT `place_order`  
- [x] Specs cover GET prefill, confirm cash, pyramid, untradeable banner  

## Live stamp (2026-09-18 GC, CPGW up)

| Journal | OP | Underlying | Result |
|---------|-----|------------|--------|
| 1914 | Blue #1574 | RXT | leap, 8 contracts @ $2.30, Jan 2029, conid 923585415, flow −$1,840 (was −$3,256 share) |
| 1915 | Orange #1576 | AAPL | `zero_contracts` — 40 share unit < 100 (WUT floor; not a silent stock fill) |
| 1916 | Mango #1577 | RXT | leap, 4 contracts @ $2.30, flow −$920 (was −$1,628 share) |

**Label quality:** stamped `occ`/`symbol` was the underlying ticker (`RXT`, `AAPL`), not an OCC OSI. conid is real. Follow-up (design first): [`2026-09-19-leap-instrument-label-occ-vs-ticker.md`](2026-09-19-leap-instrument-label-occ-vs-ticker.md).  

## Gates

- Reads via `LEAP_READ_BINDING_ID` only (`broker_binding_id` stays nil).  
- Live CPGW SSO is a human gate for smoke; fixtures cover the merge.  
- Option Desk Send still blocked (Walnut ticket).

## Related (2026-09-18)

John lock via Forensics (Indigo `#1583` BITQ `no_expiry_ge_min`): LEAP-preferred Mode C should **fall back to underlying** when LEAP is untradeable — tickets [`2026-09-18-mode-c-leap-preferred-underlying-fallback.md`](2026-09-18-mode-c-leap-preferred-underlying-fallback.md) + Justification UI [`2026-09-18-wv2-workflow-fulfillment-justification.md`](2026-09-18-wv2-workflow-fulfillment-justification.md). Do not BS-synthesize LEAP.
