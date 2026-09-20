# Ticket: BG option_candidates — delta / open interest for standard_call filter

**Status:** Proposed  
**Priority:** P1  
**Date:** 2026-09-20  
**Mode:** contractor  
**Graph nodes:** broker_gateway (`Adapters::Ibkr::LeapCandidates`); winston_v2 (`CallFulfillmentSelector`)  
**Human gates:** read-only Client Portal Gateway (CPGW); no OPT `place_order`; no Black–Scholes  
**DoD:** Frozen/live `option_candidates` rows can carry `delta`, `open_interest`, bid/ask so `standard_call` filters are honest. Missing greeks → that candidate untradeable (not synthesized).  
**Origin:** Wrap [`../session-reports/2026-09-20-1140-standard-call-packaging-rung.md`](../session-reports/2026-09-20-1140-standard-call-packaging-rung.md); parent [`2026-09-19-standard-call-fulfillment-packaging-rung.md`](2026-09-19-standard-call-fulfillment-packaging-rung.md)  
**Related:** [`2026-09-18-bg-option-candidates-quotes.md`](2026-09-18-bg-option-candidates-quotes.md) (quotes/conid — **reuse LeapCandidates, do not fork a third walker**)

## Problem

`CallFulfillmentSelector` rejects standard-call candidates without delta / quote / open interest. Today `LeapCandidates` snapshots last/bid/ask only. A live OP that opts into `packaging_preference` including `standard_call` will always fall through that rung (fail-closed). Not P0 until an OP opts in — then it becomes the blocker for Plan A/B listed-call.

## Scope

1. CPGW fields for greeks/OI if the snapshot (or secdef/info) actually has them.  
2. Pass through on `option_candidates` JSON. Empty → omit; selector treats missing as reject.  
3. Fixture chain for Wv2 frozen tests already has delta/OI — keep that as the unit source of truth.

## Non-goals

- Black–Scholes fill-in  
- A second chain walker  
- OPT Desk-Send

## Acceptance

- [ ] Live or documented CPGW path returns delta and/or OI when the gateway has them  
- [ ] Selector on a live-shaped chain can pick a standard_call without inventing greeks  
- [ ] Quotes ticket contract still holds (conid + bid/ask/last)
