# Ticket: Mode C LEAP stop-out must book option mark, not underlying Working Stop

**Status:** Done  
**Priority:** P0  
**Date:** 2026-09-20  
**Mode:** contractor  
**Graph nodes:** winston_v2 (`ExitAtStopService`, `AdHocExitService`, `RelatedInstrumentFulfillment`)  
**Implementer:** Grok CLI  
**Lane:** B (sharp DoD; System One harness below)  
**Human gates:** Mode C paper Operational Portfolios (OPs) already hold Long-term Equity Anticipation Security (LEAP) lots; do not Desk-Send options  
**DoD:** Stop-out of an option-packaged lot journals sell-to-close at **option mark** (Client Portal Gateway last/mid, else last stamped premium). `fulfillment_details["exit_at_stop"]=true`. Cash = contracts × mark × 100. Working Stop stays on the **underlying** (signal) and is **not** the fill price. Spec `mode_c_paper_leap_spec` Exit STC green.  
**Origin:** Wrap [`../../session-reports/2026-09-20-1140-standard-call-packaging-rung.md`](../../session-reports/2026-09-20-1140-standard-call-packaging-rung.md) §14; failing spec `winston_v2/spec/integration/mode_c_paper_leap_spec.rb` Exit STC  
**Related:** [`../2026-09-15-wv2-leap-packaging-fields.md`](../2026-09-15-wv2-leap-packaging-fields.md) (DoD item 6 was wrong on the ad-hoc path; closed here); ADR-013 extra-modal HITL; [`../../business-context/leap-extra-modal-proxy.md`](../../business-context/leap-extra-modal-proxy.md)  
**Closed:** 2026-09-22. `OptionMark.for_position(live: true)` — Client Portal Gateway mid (`cpgw_mid`), else last (`cpgw_last`), else stamped premium (`stamped`). Ceiling: `option_candidates` is furthest-month at-the-money three strikes, not a quote by Contract Identity. Follow-up: [`../2026-09-22-bg-option-snapshot-by-conid.md`](../2026-09-22-bg-option-snapshot-by-conid.md).

## Why P0

Mode C paper books are live. `ExitAtStopService#exit_one` with **no draft** calls `AdHocExitService` with `price: stop_price` (underlying Working Stop) and does **not** stamp `exit_at_stop`. For a LEAP, that books `units × underlying_stop × 100` (e.g. 2 × $140 × 100 = $28,000 credit on a ~$12.50 premium lot). Law: Working Stop pierce **signals** the exit; the fill is the **option mark**.

Draft-confirm path does stamp `exit_at_stop` but still passes `execution_price: stop_price`.

## Scope

1. Resolve option mark (CPGW snapshot last/mid, else last stamped `option_premium` / `option_mark` with source label). Never Black–Scholes.  
2. Ad-hoc and draft Confirm paths: fill = mark; details `exit_at_stop`, `exit_reason`, packaging fields preserved (`standard_call` too).  
3. Spec: LEAP (and later standard_call) STC cash ≠ Working Stop × 100.  
4. Stock lots unchanged (fill may remain Working Stop).

## Non-goals

- Silent option STP at Interactive Brokers  
- Geometry A  
- WUT lab

## Acceptance

- [x] Ad-hoc LEAP stop-out: `exit_at_stop=true`, fill = option mark, flow = contracts × mark × 100  
- [x] Underlying Working Stop recorded beside, not as premium  
- [x] `mode_c_paper_leap_spec` Exit example green  
- [x] Stock exit-at-stop regression still green

## System One harness

**State:** Done 2026-09-22. Pre-fix, `ExitAtStopService#exit_one` called `AdHocExitService` with `price: stop_price` and did not stamp `exit_at_stop`. Law in `leap-extra-modal-proxy.md`: Working Stop signals; fill is the option mark. Specs now green (stamped, Client Portal Gateway mid, Client Portal Gateway last, draft confirm, stock regression).

**Checkpoints:**

| id | type | instructions | pass rule |
|----|------|--------------|-----------|
| fill_is_mark | Noul | Ad-hoc LEAP stop-out journals fill at option mark (CPGW last/mid else stamped premium), not underlying Working Stop | noul ≥ 0.85 |
| exit_flag | Noul | `fulfillment_details["exit_at_stop"]=true` on option STC | noul ≥ 0.85 |
| cash_formula | Noul | Cash credit = contracts × mark × 100 (not units × underlying_stop × 100) | noul ≥ 0.85 |
| stock_unchanged | Noul | Stock exit-at-stop still uses Working Stop as fill | noul ≥ 0.85 |

**Runner:** `bundle exec rspec spec/integration/mode_c_paper_leap_spec.rb` (+ focused Exit example) then `jev ask` on residual smells  
**Order:** deterministic specs first  
**On fail:** stop; do not Done/archive

## CLI seed

```
cwd: /home/johnkoisch/Documents/com/sawtooth/winston_v2
Lane B. Ticket: ecosystem/docs/tickets/2026-09-20-mode-c-leap-exit-at-stop-option-mark.md
Read the ticket + leap-extra-modal-proxy.md (Working Stop signals exit; fill is option mark).
Goal: Mode C / paper LEAP (and standard_call) stop-out books sell-to-close at option mark, not underlying Working Stop.

Facts:
- ExitAtStopService#exit_one with no draft calls AdHocExitService with price: stop_price and does not stamp exit_at_stop — books units × underlying_stop × 100 (wrong).
- Draft-confirm may stamp exit_at_stop but still passes execution_price: stop_price.
- Resolve mark: CPGW snapshot last/mid, else last stamped option_premium / option_mark with source label. Never Black–Scholes on this path.
- Stock lots unchanged (fill may remain Working Stop).
- Do not Desk-Send options. Push winston_v2 main (no PR). Never commit graphify-out/.

Steps:
1. Reproduce failing Exit STC in spec/integration/mode_c_paper_leap_spec.rb.
2. Fix AdHocExitService + ExitAtStopService (and draft Confirm path) so option-packaged lots fill at mark; stamp exit_at_stop / exit_reason; preserve packaging fields.
3. Specs green: Exit STC LEAP cash ≠ Working Stop × 100; stock exit-at-stop regression green.
4. In-band wrap (ecosystem session-report + ticket acceptance checkboxes); push main; update INDEX when Done.

DoD: ad-hoc LEAP stop-out exit_at_stop=true, fill=option mark, cash=contracts×mark×100; Working Stop recorded beside not as premium; mode_c_paper_leap_spec Exit green; stock regression green.
```

