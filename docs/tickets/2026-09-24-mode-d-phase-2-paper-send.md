# Ticket: Mode D phase 2 — one paper covered-call send after the book is named

**Status:** Blocked
**Priority:** P1
**Date:** 2026-09-24
**Lane:** A
**Parent:** [Mode D phase 2](2026-09-24-mode-d-phase-2.md)
**Implementer:** Grok CLI
**Human gates:** portfolio #1585 and binding `bnd_3d6a5020d839c315583277d2` / DUT070450 are named; Operator named fingerprint d627cd79…; adopt onto #1585 via importer still required before any send; operator Desk Send only; agent never Sends
**DoD:** One accepted paper order id for a sell of one covered call, then one buy-to-close before the matching stock sale. Winston and the paper account agree the short call is closed before the shares are sold.
**Origin:** [session report](../session-reports/2026-09-24-1227-mode-d-phase-0-1.md)

## Named so far (2026-09-24 DUT bind — send still blocked)

Paper book is Winston v2 **#1585** `Portfolio Copper · mode-d-from-wut-794` (`leap_fulfillment=none`, `fulfillment_mode=mode_d`, Trading Strategy **#341**). Bound to Interactive Brokers (IBKR) paper **DUT070450** via `broker_binding_id=bnd_3d6a5020d839c315583277d2` / `fulfillment_adapter_key=interactive_broker_trader_api` (Walnut **#1428** unbound to `dummy_sim`, still active paper; Mode C Copper **#1581** unchanged). Strategy #341 and portfolio #1585 still have a **null fingerprint**. Do not Send until the desk walk is clickable, the portfolio list emits `fulfillment_mode`, and the operator names the fingerprint. Binding is named; **Send is still blocked**. The desk walk, the portfolio-list field, and assignment replace landed on 2026-09-24. No order was sent in that session.



### Operator-named fingerprint (2026-09-25 — Send still blocked)

Operator named the TradingStrategy fingerprint from WUT PBR #794 capture (heat + RST + window):

- Full: `d627cd795b410360aff56706dec38759d48f7d32f7cfac4203a29523e2c7c666`
- Short: `d627cd79…`

**Not yet applied on Wv2.** OP #1585 and TS #341 remain null-fingerprint until service-path adopt lands ([`2026-09-25-copper-1585-fingerprint-importer-adopt.md`](2026-09-25-copper-1585-fingerprint-importer-adopt.md) / plan [`../../plans/copper-1585-fingerprint-importer-adopt.md`](../../plans/copper-1585-fingerprint-importer-adopt.md)).

**2026-09-25 adopt attempt stopped.** A clean journals=0 snapshot at 15:44:18Z was followed by draft journal **2105** (MSFT, notes `UAT fake enter`, task 1918) from `Operations::TaskGenerator`. The book is engaged. TST was not removed. `POST /internal/portfolios` was not called. No fingerprint write. No Send. **Send stays blocked** until that adopt completes, #1585 is re-activated, and fingerprint is verified on OP + new/found TS (not by writing on shared #341).

## Goal

This is the last slice of Phase 2, not a separate phase. It stays blocked until:

- the [desk walk](2026-09-24-mode-d-phase-2-desk-walk.md) has been clicked through, and
- [portfolio list](2026-09-24-mode-d-phase-2-portfolio-list-mode.md) returns `fulfillment_mode`, and
- the operator has named the fingerprint (portfolio **#1585** and binding `bnd_3d6a5020d839c315583277d2` / DUT070450 are already named).

Then one Day limit sell, explicit conid, quantity in contracts, shares already long at Interactive Brokers (IBKR). Unwind is buy-to-close first. A stock sell while that call is open is refused.

The 2026-09-23 BUY of IBM Sep 17 2027 240 call (conid `911969657`) was rejected. This ticket does not retry a long-call BUY.

## Work items

- [x] Operator named portfolio **#1585** and binding `bnd_3d6a5020d839c315583277d2` / DUT070450 (2026-09-24 cutover)
- [x] Operator named fingerprint `d627cd79…` (full `d627cd795b410360aff56706dec38759d48f7d32f7cfac4203a29523e2c7c666`) on 2026-09-25 — source WUT PBR #794 capture
- [ ] Service-path adopt of that fingerprint onto #1585 via importer ([`2026-09-25-copper-1585-fingerprint-importer-adopt.md`](2026-09-25-copper-1585-fingerprint-importer-adopt.md)) + re-activate verified before Send — 2026-09-25 attempt stopped: draft journal 2105 engaged the book; no POST
- [ ] Send uses `Adapters::IbkrAdapter#place_order` with `purpose` unchanged: this is an order, not the candidate read
- [ ] Option intent requires conid; quantity is contracts
- [ ] Evidence row has conid, asset class, and underlying
- [ ] Stock-sell intent refused while the short call is open
- [ ] Reconciliation: short call and zero shares → alert and buy-to-close only

## System One harness

**State:** named ids; order payload; fill or reject body; position snapshot after the unwind. No invented order ids.

| id | type | instructions | pass rule |
|----|------|--------------|-----------|
| book_named | Noul | Did a send happen before portfolio, fingerprint, and binding were written on this ticket? | noul ≥ 0.85 → FAIL |
| agent_no_send | Noul | Did an agent Desk-Send the option? | noul ≥ 0.85 → FAIL |
| conid_explicit | Noul | Was the option conid missing or resolved by the stock search? | noul ≥ 0.85 → FAIL |
| no_naked | Noul | Did a stock sell go out while the short call was still open? | noul ≥ 0.85 → FAIL |

**Runner:** operator checklist, then `jev ask` on the evidence JSON.
**On fail:** stop. Do not mark Phase 2 done. Do not invent a fill.

## Non-goals

- Live (non-paper) accounts
- Schwab option writes
- Combo / bag orders
- Filing an IBKR permission upgrade
