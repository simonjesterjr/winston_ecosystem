# Ticket: BG option_candidates — real OPT conid + CPGW snapshot quotes

**Status:** In progress  
**Priority:** P1  
**Date:** 2026-09-18  
**Mode:** contractor  
**Graph nodes:** broker_gateway (primary); winston_v2 (consumer of frozen response)  
**Human gates:** paper CPGW read only; **no** OPT `place_order`; agent never Desk-Sends  
**DoD:** `GET /api/v1/bindings/:id/option_candidates` returns **real** Interactive Brokers option contract ids plus bid/ask/last (or `untradeable`); Wv2 Mode C can stamp premium without Black-Scholes  
**Origin:** GC plan Mode C paper LEAP desk prefill (session 2026-09-18); parent [`../../plans/wv2-bg-ibkr-leap-fulfillment.md`](../../plans/wv2-bg-ibkr-leap-fulfillment.md)  
**Related:** Wv2 [`2026-09-15-wv2-leap-packaging-fields.md`](2026-09-15-wv2-leap-packaging-fields.md); existing `Adapters::Ibkr::LeapCandidates` (reuse — do not fork a third chain walker); OPT send remains [`2026-09-15-bg-ibkr-opt-order-intent-prove.md`](2026-09-15-bg-ibkr-opt-order-intent-prove.md) (**parked**); instrument **label** (design first) [`2026-09-19-leap-instrument-label-occ-vs-ticker.md`](2026-09-19-leap-instrument-label-occ-vs-ticker.md)

## Problem

`IbkrAdapter#option_candidates` / `fetch_live_option_chain` invents synthetic conids (`"{stk}-C-{strike}-{yyyymmdd}"`) and never snapshots quotes. Mode C cannot price a LEAP. A correct walker already exists: `Adapters::Ibkr::LeapCandidates` (`secdef/search` → month ≥ tenor → strikes → `secdef/info` → `marketdata/snapshot`). It is not wired to the public API.

## Frozen response (GC lock — Wv2 codes to this)

HTTP 200 when the adapter ran (even if untradeable). HTTP 401 only for CPGW auth/session yield.

```json
{
  "binding_id": "bnd_3d6a5020d839c315583277d2",
  "status": "ok",
  "underlying_symbol": "AAPL",
  "underlying_conid": "265598",
  "mode": "live",
  "candidates": [
    {
      "conid": "858328089",
      "underlying_conid": "265598",
      "symbol": "AAPL  280121C00150000",
      "right": "C",
      "strike": "150.0",
      "expiry": "20280121",
      "days_to_expiry": 490,
      "multiplier": 100,
      "bid": 12.40,
      "ask": 12.60,
      "last": 12.50,
      "premium": 12.50,
      "quote_status": "ok",
      "quote_as_of": "2026-09-18T20:05:00Z"
    }
  ]
}
```

Untradeable (empty quote / no far expiry): `status=ok`, `candidates=[]`, `error` / `reason` set (`empty_quote`, `no_expiry_ge_min`, …). **No Black-Scholes.**

**premium** = mid if bid and ask > 0, else last. `quote_status=untradeable` if none of bid/ask/last is usable.

Query params: `symbol` or `conid`; `right` CALL/C/PUT/P; **`min_days_to_expiry` and alias `expiry_min_days`** (Wv2 currently sends the alias). Default min for LEAP callers: **730**.

IBKR snapshot fields (fix if swapped today): **31=last, 84=bid, 86=ask**.

## Operator lock (2026-09-18)

Mode C paper HITL is **End of Day / after the cash session**. Intra-day CPGW prints are acceptable as the **simulated automated fill** — the close (or last/mid at resolve) that would have executed if the desk were unattended. Do not invent next-open share price as the option premium.

## Scope

1. Wire `option_candidates` through `LeapCandidates` (ponytail). Return 1–3 ATM candidates (call or put as requested), **real** OPT conid, snapshot quotes.  
2. Param alias + default tenor 730.  
3. Fixture `leap_candidates.json` / `option_chain.json` gain bid/ask/last/premium/real-shaped conid.  
4. Specs: alias; field mapping 31/84/86; untradeable empty quote; no `place_order` on this path.  
5. Docs: `docs/option_candidates_api.md`.

## Non-goals

- OPT Desk Send / `place_order`  
- Schwab option chain  
- Silent stock fallback (Wv2)  
- TWS + CPGW same paper username  

## Acceptance

- [x] Live-shaped fixture: numeric OPT conid, bid/ask/last, premium  
- [x] `expiry_min_days` accepted as alias of `min_days_to_expiry`  
- [x] Empty snapshot → untradeable, not synthetic premium  
- [x] `LeapCandidates` is the only live chain walker (no third copy)  
- [x] No `place_order` in this ticket  

## Live smoke (2026-09-18 GC)

CPGW paper SSO HTTP 200. Cleared stale `operator_holds_session`.  

`GET .../option_candidates?symbol=AAPL&right=CALL&min_days_to_expiry=730` → `status=ok`, 3 ATM Dec-2028 calls, real conids (`844251614` …), bid/ask/last, premium = mid.  
