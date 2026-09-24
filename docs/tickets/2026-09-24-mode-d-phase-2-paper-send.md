# Ticket: Mode D phase 2 — one paper covered-call send after the book is named

**Status:** Proposed
**Priority:** P1
**Date:** 2026-09-24
**Lane:** A
**Parent:** [Mode D phase 2](2026-09-24-mode-d-phase-2.md)
**Implementer:** Grok CLI
**Human gates:** operator names the portfolio, the TradingStrategy fingerprint, and the IBKR paper binding before any send; operator Desk Send only; agent never Sends
**DoD:** One accepted paper order id for a sell of one covered call, then one buy-to-close before the matching stock sale. Winston and the paper account agree the short call is closed before the shares are sold.
**Origin:** [session report](../session-reports/2026-09-24-1227-mode-d-phase-0-1.md)

## Goal

This is the last slice of Phase 2, not a separate phase. It stays blocked until:

- the [desk walk](2026-09-24-mode-d-phase-2-desk-walk.md) has been clicked through, and
- [portfolio list](2026-09-24-mode-d-phase-2-portfolio-list-mode.md) returns `fulfillment_mode`, and
- the operator has named the portfolio id, the fingerprint, and the paper `broker_binding_id`.

Then one Day limit sell, explicit conid, quantity in contracts, shares already long at Interactive Brokers (IBKR). Unwind is buy-to-close first. A stock sell while that call is open is refused.

The 2026-09-23 BUY of IBM Sep 17 2027 240 call (conid `911969657`) was rejected. This ticket does not retry a long-call BUY.

## Work items

- [ ] Operator records portfolio id, fingerprint, and binding on this ticket before Send
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
