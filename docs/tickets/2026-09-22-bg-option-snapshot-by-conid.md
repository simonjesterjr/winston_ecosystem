# Ticket: Broker Gateway snapshot by option Contract Identity

**Status:** Proposed  
**Priority:** P2  
**Date:** 2026-09-22  
**Mode:** contractor  
**Lane:** B  
**Graph nodes:** broker_gateway (`Adapters::Ibkr::LeapCandidates#snapshot`); winston_v2 (`Operations::OptionMark.cpgw_quote`)  
**Human gates:** read-only Client Portal Gateway (CPGW); no OPT `place_order`; no Desk-Send; no Black–Scholes  
**DoD:** A Mode C paper stop-out can mark an open listed call by its option Contract Identity (conid) even when that contract is outside the furthest-month at-the-money three. Fill is snapshot mid (bid and ask), else last. Missing quote keeps the stamped premium. Account `GET /snapshot` stays lots and cash.  
**Origin:** [`../session-reports/2026-09-22-1720-mode-c-leap-exit-option-mark.md`](../session-reports/2026-09-22-1720-mode-c-leap-exit-option-mark.md) §14  
**Related:** Archived [`archive/2026-09-20-mode-c-leap-exit-at-stop-option-mark.md`](archive/2026-09-20-mode-c-leap-exit-at-stop-option-mark.md); quotes [`2026-09-18-bg-option-candidates-quotes.md`](2026-09-18-bg-option-candidates-quotes.md); greeks [`2026-09-20-bg-option-candidates-greeks.md`](2026-09-20-bg-option-candidates-greeks.md). Reuse `LeapCandidates` — do not add a third chain walker.

## Goal

Winston v2 stop-out already prefers a CPGW mid, else last, else the stamped premium. The live read is `option_candidates`, which walks the furthest listed month and returns three strikes nearest the money (`ATM_LIMIT = 3`). An open contract that has drifted off that set never gets a fresh print.

`LeapCandidates#snapshot` already calls CPGW `GET /iserver/marketdata/snapshot` for one conid (fields `31` last, `84` bid, `86` ask). That method is private and is only used while building the at-the-money three. Expose a read-only binding route for one **option** conid, and point `OptionMark.cpgw_quote` at it before the chain match.

The public `GET /api/v1/bindings/:id/snapshot` is the account lots-and-cash snapshot. Do not overload it. `option_candidates?conid=` is the **underlying** conid for `secdef/search`, not the option conid.

## Scope

1. Broker Gateway: read-only quote for one option conid. Reuse `LeapCandidates#snapshot` (same session, same fields). Return bid, ask, last. Empty or unauthenticated is not a synthesized price. No `place_order`.
2. Winston v2: `BrokerGateway::Client` method, then `OptionMark.cpgw_quote` tries that conid before `option_candidates`.
3. Spec: open contract absent from the candidate list still books mid (else last). No snapshot and no chain match still books the stamped premium. Stock exit-at-stop unchanged.

## Non-goals

- Black–Scholes, or vendor field `7635` as a third price (fill law stays mid, else last)
- A new chain walker, or changing furthest-month selection
- OPT Desk-Send
- Winston Unit Test (WUT) lab parity

## Acceptance

- [ ] Read-only route returns last/bid/ask for an option conid when CPGW has them
- [ ] Auth failure or an empty print does not invent a premium and does not hard-stop the exit
- [ ] `mode_c_paper_leap_spec` stop-out uses the conid snapshot when the contract is not in the at-the-money three
- [ ] Stamped-premium fallback and stock exit-at-stop stay green
- [ ] Account `GET /snapshot` response shape unchanged

## System One harness

**State:** Stop-out law is in `leap-extra-modal-proxy.md` (Working Stop signals; fill is the option mark). Today `winston_v2/app/services/operations/option_mark.rb` `cpgw_quote` calls `option_candidates` and matches conid only inside that list. `broker_gateway` `Adapters::Ibkr::LeapCandidates` `ATM_LIMIT = 3`; `#snapshot` is private. Parent stop-out ticket is Done (`winston_v2` `2551984`).

**Checkpoints:**

| id | type | instructions | pass rule |
|----|------|--------------|-----------|
| conid_not_atm3 | Noul | An open option conid absent from the furthest-month at-the-money three still fills at snapshot mid, else last | noul ≥ 0.85 |
| no_invented_price | Noul | Auth failure or an empty snapshot does not synthesize a premium; exit keeps the stamped premium | noul ≥ 0.85 |
| account_snapshot | Noul | `GET /snapshot` remains lots and cash, not an option print | noul ≥ 0.85 |
| stock_unchanged | Noul | Stock exit-at-stop still uses the Working Stop as the fill | noul ≥ 0.85 |

**Runner:** Broker Gateway quote spec, then `bundle exec rspec spec/integration/mode_c_paper_leap_spec.rb` and `spec/services/operations/exit_at_stop_service_spec.rb`. `jev ask` only on residual smells.  
**Order:** deterministic specs first  
**On fail:** stop; do not Done

## CLI seed

```
cwd: /home/johnkoisch/Documents/com/sawtooth
Lane B. Ticket: ecosystem/docs/tickets/2026-09-22-bg-option-snapshot-by-conid.md
Goal: read-only CPGW snapshot for one option conid. Wv2 stop-out uses it before the at-the-money-three chain. No place_order. Do not overload account GET /snapshot. Push broker_gateway and winston_v2 main (no PR). Never commit graphify-out/.
```
