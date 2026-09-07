# Ticket: Set Broker Gateway binding labels (DUT / UT)

**Status:** Proposed  
**Priority:** P2  
**Date:** 2026-09-06  
**Mode:** contractor  
**Graph nodes:** broker_gateway, winston_v2  
**Human gates:** none (nickname only; no capital)  
**DoD:** Interactive Brokers paper binding `label` is `DUT070450`; live binding (when it exists) is `UT` or last-4; Wv2 chip reads `IBKR DUT070450` / `IBKR UT`  
**Origin:** Grill 2026-09-06 Fulfillment Label — [`docs/session-reports/2026-09-06-2149-fulfillment-label-and-desk.md`](../session-reports/2026-09-06-2149-fulfillment-label-and-desk.md)

## Problem

Winston v2 **Fulfillment Label** is `{Vendor} {Nickname}` from Broker Gateway `AdapterBinding.label`. A fixture name (`IBKR L1 fixture`) would show as `IBKR L1 fixture` on the ops shell. Operator speech is `DUT070450` (paper) and `UT` (live).

## Scope

1. Set `label` on the paper Interactive Brokers binding to `DUT070450` (or the current paper account id).  
2. When a live IBKR binding exists, set `label` to the operator nickname (`UT`) — never a full live account number.  
3. Confirm the Wv2 chip after restart.

## Non-goals

- Rebind UI  
- Changing `vendor_account_ref` hashing for evidence JSONL  

## Acceptance

- [ ] Paper binding label is a short DUT id  
- [ ] Ops shell / WQ chip shows `IBKR DUT070450` (or the live nickname) not a fixture string  
