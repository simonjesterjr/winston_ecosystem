# Ticket: Persist Fulfillment Label nickname on the Operational Portfolio

**Status:** Proposed  
**Priority:** P3  
**Date:** 2026-09-06  
**Mode:** contractor  
**Graph nodes:** winston_v2  
**Human gates:** none (display cache, not capital)  
**DoD:** If Broker Gateway is down, a bound OP still shows `IBKR DUT070450` (last known nickname), not `IBKR bound`  
**Origin:** Grill 2026-09-06 — [`docs/session-reports/2026-09-06-2149-fulfillment-label-and-desk.md`](../session-reports/2026-09-06-2149-fulfillment-label-and-desk.md)

## Problem

v1 resolves `{Vendor} {Nickname}` from a live Broker Gateway `list_bindings` call. If the gateway is unreachable, Winston v2 falls back to vendor + `bound` / env. The operator still wants `IBKR DUT070450` on the ops shell.

## Scope

1. Cache the display nickname (and vendor) on the Operational Portfolio when a binding is associated or when catalog loads successfully.  
2. Glance uses the cache when Broker Gateway fails.  
3. Do not store full live account numbers. Last-4 / DUT id / operator nickname only.

## Non-goals

- Rebind UI  
- Making Broker Gateway optional for Confirm-Send  

## Acceptance

- [ ] Spec: injected catalog then simulated BG down still shows the cached nickname  
- [ ] Never persist a `hash:` vendor_account_ref or a long numeric live account  
