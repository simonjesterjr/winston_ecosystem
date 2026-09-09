# Ticket: IBKR STP tick size beyond a hard 0.01

**Status:** Proposed  
**Priority:** P2  
**Date:** 2026-09-09  
**Mode:** contractor  
**Graph nodes:** broker_gateway, winston_v2  
**Human gates:** paper DUT only  
**DoD:** Stop prices sent to Client Portal Gateway (CPGW) use the instrument’s minimum price variation, not a blanket two decimals, when a name is not a US penny stock/ETF  
**Origin:** [`docs/session-reports/2026-09-09-1444-walnut-paper-stp-slate.md`](../session-reports/2026-09-09-1444-walnut-paper-stp-slate.md) §14 item 4  
**Related:** [`2026-09-09-walnut-paper-session-order-slate.md`](2026-09-09-walnut-paper-session-order-slate.md)

## Problem

DuPont (DD) DAY STP at **148.7655** was rejected:

> The price 148.7655 does not conform to the minimum price variation of 0.01 for this instrument.

The 2026-09-09 wrap rounds stock STP to **$0.01** on send (and new slate entry legs). That unblocked DD / KR / SCHZ. Some products (sub-dollar names, non-US, future ticks) are not 0.01. A second CPGW variation error will look like “no broker_order_id” unless we keep surfacing the raw error.

## Scope

1. Keep 0.01 as the US common-stock default.  
2. When CPGW returns a minimum-price-variation error: fail closed with that text (already started).  
3. Later: CPGW info-and-rules / contract increment per conid; round to that tick.  
4. Slate display should show the price that will be sent.

## Non-goals

- Crypto / FX adapters  
- Changing Turtle stop *distance* (2N / 0.5N) — only the broker tick of the trigger  

## Acceptance

- [ ] Default 0.01 still used for ordinary US STK  
- [ ] A non-penny instrument does not 422 with a four-decimal parquet high  
- [ ] Operator sees the CPGW tick error, not a blank reject  
