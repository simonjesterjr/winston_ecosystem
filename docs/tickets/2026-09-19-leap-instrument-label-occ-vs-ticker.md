# Ticket: LEAP instrument label — OCC vs IBKR ticker vs conid

**Status:** Proposed  
**Priority:** P2  
**Date:** 2026-09-19  
**Mode:** contractor — **blocked on a design session** (do not implement first)  
**Graph nodes:** broker_gateway (`LeapCandidates#build_candidate`); winston_v2 (`LeapPackaging` OCC/`instrument_symbol` desk fields)  
**Human gates:** Mode C paper; no OPT `place_order`; agent never Desk-Sends  
**DoD:** After the design session, desk HITL sees a human-readable LEAP instrument string that is not merely the underlying ticker, while **conid remains the Send/eval identity**.  
**Origin:** Wrap 2026-09-18 follow-up item 5 — [`../session-reports/2026-09-18-1720-mode-c-leap-desk-prefill.md`](../session-reports/2026-09-18-1720-mode-c-leap-desk-prefill.md)  
**Related:** BG quotes [`2026-09-18-bg-option-candidates-quotes.md`](2026-09-18-bg-option-candidates-quotes.md); packaging [`2026-09-15-wv2-leap-packaging-fields.md`](2026-09-15-wv2-leap-packaging-fields.md); ADR-017; domain [`../business-context/leap-extra-modal-proxy.md`](../business-context/leap-extra-modal-proxy.md)

## Design session required

**Do not ship a string-format fix from this ticket alone.** Book a `/grill-with-docs` (or dedicated design turn) on what the desk must display vs what BG must persist. Live evidence is enough to know the current label is weak; it is **not** enough to pick OCC vs `localSymbol` vs constructed OSI vs `desc2`.

Questions for that session (not pre-answered here):

1. Canonical HITL label: Options Clearing Corporation (OCC) OSI (`AAPL  281215C00340000`), IBKR `localSymbol`, `desc2` (`DEC 15 '28 340 Call`), or a Winston-built `UNDERLYING YYYY-MM-DD C strike`?
2. Which field is **identity** (must be conid today) vs **audit** vs **speech/Telegram**?
3. When CPGW returns `symbol=AAPL` and empty `localSymbol`, do we construct OSI from strike/expiry/right we already trust, or show ticker + structured fields only?
4. Does Wv2 stamp one `instrument_label` or keep `occ_symbol` / `conid` / `desc2` as separate `fulfillment_details` keys?

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

- [ ] Design session notes (grill or session report) pick the label grammar  
- [ ] BG candidate payload has that label without inventing a second conid  
- [ ] Wv2 desk GET shows it next to contracts/premium  
- [ ] Specs: fixture where IBKR `symbol` is the root still produces the chosen label  
- [ ] No `place_order`
