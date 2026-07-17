# Ticket: Ops shell cash parity (`cash` command)

**Status:** Proposed  
**Date:** 2026-07-17  
**Epic:** `2026-07-17-ops-daily-demo-epic.md`  

## Problem

Capital add/remove works via `wv2_add_cash_event` / internal API but Ops shell HELP does not expose a `cash` verb — demo path requires Telegram or curl.

## Scope

1. Ops shell: `cash <portfolio> amount=N [type=inflow|adjustment] [notes=…]` → `CashEventService`.  
2. HELP + panels refresh on success.  
3. Spec for parse + service call.

## Acceptance

- [ ] Ops UI can top-up and reverse capital without MCP  
- [ ] Same service as MCP (no parallel accounting)  

## Related

- Done: `2026-07-14-wv2-cash-inflow-mcp.md`  
