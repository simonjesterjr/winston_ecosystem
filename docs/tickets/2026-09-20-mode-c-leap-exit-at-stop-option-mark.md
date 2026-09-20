# Ticket: Mode C LEAP stop-out must book option mark, not underlying Working Stop

**Status:** Proposed  
**Priority:** P0  
**Date:** 2026-09-20  
**Mode:** contractor  
**Graph nodes:** winston_v2 (`ExitAtStopService`, `AdHocExitService`, `RelatedInstrumentFulfillment`)  
**Implementer:** Winston Dev  
**Human gates:** Mode C paper Operational Portfolios (OPs) already hold Long-term Equity Anticipation Security (LEAP) lots; do not Desk-Send options  
**DoD:** Stop-out of an option-packaged lot journals sell-to-close at **option mark** (Client Portal Gateway last/mid, else last stamped premium). `fulfillment_details["exit_at_stop"]=true`. Cash = contracts × mark × 100. Working Stop stays on the **underlying** (signal) and is **not** the fill price. Spec `mode_c_paper_leap_spec` Exit STC green.  
**Origin:** Wrap [`../session-reports/2026-09-20-1140-standard-call-packaging-rung.md`](../session-reports/2026-09-20-1140-standard-call-packaging-rung.md) §14; failing spec `winston_v2/spec/integration/mode_c_paper_leap_spec.rb` Exit STC  
**Related:** [`2026-09-15-wv2-leap-packaging-fields.md`](2026-09-15-wv2-leap-packaging-fields.md) (DoD item 6 marked done — **not true on `main` ad-hoc path**); ADR-013 extra-modal HITL; [`leap-extra-modal-proxy.md`](../business-context/leap-extra-modal-proxy.md)

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

- [ ] Ad-hoc LEAP stop-out: `exit_at_stop=true`, fill = option mark, flow = contracts × mark × 100  
- [ ] Underlying Working Stop recorded beside, not as premium  
- [ ] `mode_c_paper_leap_spec` Exit example green  
- [ ] Stock exit-at-stop regression still green
