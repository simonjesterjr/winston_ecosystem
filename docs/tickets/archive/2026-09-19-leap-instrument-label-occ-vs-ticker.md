# Ticket: LEAP instrument label — OCC vs IBKR ticker vs conid

**Status:** Done  
**Priority:** P2  
**Date:** 2026-09-19  
**Mode:** contractor — design session locked 2026-09-21 (Q1–Q4)  
**Graph nodes:** broker_gateway (`LeapCandidates#build_candidate`); winston_v2 (`LeapPackaging` OCC/`instrument_symbol` desk fields)  
**Human gates:** Mode C paper; no OPT `place_order`; agent never Desk-Sends  
**DoD:** After the design session, desk HITL sees a human-readable LEAP instrument string that is not merely the underlying ticker, while **conid remains the Send/eval identity**.  
**Origin:** Wrap 2026-09-18 follow-up item 5 — [`../session-reports/2026-09-18-1720-mode-c-leap-desk-prefill.md`](../session-reports/2026-09-18-1720-mode-c-leap-desk-prefill.md)  
**Related:** BG quotes [`2026-09-18-bg-option-candidates-quotes.md`](2026-09-18-bg-option-candidates-quotes.md); packaging [`2026-09-15-wv2-leap-packaging-fields.md`](2026-09-15-wv2-leap-packaging-fields.md); ADR-017; domain [`../business-context/leap-extra-modal-proxy.md`](../business-context/leap-extra-modal-proxy.md)

## Design session required

Design session **closed 2026-09-21** (grill Q1–Q4). Implement the locked split; still no OPT Desk-Send / `place_order`.

Questions for that session (not pre-answered here):

1. Canonical HITL label: Options Clearing Corporation (OCC) OSI (`AAPL  281215C00340000`), IBKR `localSymbol`, `desc2` (`DEC 15 '28 340 Call`), or a Winston-built `UNDERLYING YYYY-MM-DD C strike`?  
   **Locked 2026-09-21:** Winston-built **Instrument Label** `{UNDERLYING} {YYYY-MM-DD} {C|P} {strike}` (e.g. `SEF 2027-02-19 C 30`). Glossary: `CONTEXT.md`.
2. Which field is **identity** (must be conid today) vs **audit** vs **speech/Telegram**?  
   **Locked 2026-09-21:** **Contract Identity** = IBKR conid (Send/eval). Speech (desk / Justification / DAR / Telegram) = **Instrument Label**. Audit = strike + expiry + right, plus **OCC Symbol**. Not **Fulfillment Label**.
3. When CPGW returns `symbol=AAPL` and empty `localSymbol`, do we construct OSI from strike/expiry/right we already trust, or show ticker + structured fields only?  
   **Locked 2026-09-21:** Do **not** construct OSI. **OCC Symbol** empty until IBKR `localSymbol` (or a real OSI) arrives. Audit = strike + expiry + right + **Contract Identity**. CPGW `symbol` is never copied into **OCC Symbol**.
4. Does Wv2 stamp one `instrument_label` or keep `occ_symbol` / `conid` / `desc2` as separate `fulfillment_details` keys?  
   **Locked 2026-09-21:** Separate keys: `instrument_label` (speech), `conid` (identity), `occ_symbol` (only if IBKR sent `localSymbol` / OSI), `strike` / `expiry` / `option_type`. `desc2` is not a Winston field.

## Problem

Live Mode C resolve (2026-09-18) returned **real** option conids and quotes, but `symbol` was the **underlying ticker**:

| Underlying | conid | strike | expiry | `symbol` as stamped |
|------------|-------|--------|--------|---------------------|
| AAPL | 844251614 | 340 | 20281215 | `AAPL` |
| RXT | 923585415 | 4 | 2029-01-19 | `RXT` |
| SEF (2026-09-21 Plan B) | 893744520 | 30 | 20270219 | `SEF` |
| BITQ (2026-09-21 Plan B) | 912464575 | 28 | 20270416 | `BITQ` |

Wrap 2026-09-21 follow-up item 4: still blocked on the design session. See [`../session-reports/2026-09-21-1457-mode-c-furthest-call-desk-uat.md`](../session-reports/2026-09-21-1457-mode-c-furthest-call-desk-uat.md).

`LeapCandidates#build_candidate` prefers `localSymbol || ticker || symbol || desc2`. CPGW `secdef/info` often fills `symbol`/`ticker` with the stock root. Desk then shows “RXT” as the LEAP instrument while strike/expiry live in other fields.

conid is usable. HITL/OCC speech is not.

## Non-goals

- OPT Desk Send / `place_order`
- Black-Scholes
- Changing ATM / 730d selection
- Plan B underlying fallback (separate ticket)

## Acceptance (after design lock)

- [x] Design session notes (grill or session report) pick the label grammar  
- [x] BG candidate payload has that label without inventing a second conid  
- [x] Wv2 desk GET shows it next to contracts/premium  
- [x] Specs: fixture where IBKR `symbol` is the root still produces the chosen label  
- [x] No `place_order`
