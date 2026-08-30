# Ticket: Broker Gateway dummy_sim sandbox fills (not L3 order_write)

**Status:** In progress  
**Priority:** P1  
**Date:** 2026-08-28  
**Monoliths:** broker_gateway  
**Related:** [`2026-08-28-wq-monday-rebalance-plan.md`](2026-08-28-wq-monday-rebalance-plan.md)

## Problem

dummy_sim `refresh` only emits canned SPY/QQQ scenarios. WQ Plan Approve needs evidence events for the **actual selected names** at a supplied next-open price. Setting `cap_order_write` would break L1 refresh (fail-closed).

## Scope

1. `POST /api/v1/bindings/{id}/sandbox_fills` — **dummy_sim adapter_key only**.
2. Body: `{ fills: [{ symbol, side, quantity, fill_price, fill_date, client_order_id }] }`.
3. Append `trade.executed` evidence (idempotent). Do **not** set `cap_order_write`.
4. Refuse on non-dummy adapters (Schwab write stays off).

## Acceptance

- [ ] dummy_sim binding accepts fills and appends events
- [ ] schwab_trader_api binding (if present) is refused
- [ ] L1 refresh still refuses `cap_order_write`
