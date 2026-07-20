# Ticket: Cash inflow via internal API + MCP

**Status:** Done (2026-07-17)  
**Date:** 2026-07-14  
**Source:** Paper Telegram roadmap Phase 4; session `2026-07-14-1112-paper-telegram-phase0-1.md`

## Problem

Speech like “add $5600 cash to Portfolio White” is domain-legal (`CashEvent` inflow) but not operable: model exists; nested REST route has no controller; no MCP tool.

## Scope

1. Internal `POST` create CashEvent (`inflow` / `adjustment`) with portfolio resolve, amount, date, notes.  
2. MCP `wv2_add_cash_event` (name TBD).  
3. Document in lifecycle / MCP contract.  
4. Spec: capital_base updates; paper focus safe.

## Acceptance

- [x] Inflow via MCP updates capital_base  
- [x] Auditable notes/source  
- [x] No secrets or arbitrary mutation  

## Implemented

- `Operations::CashEventService` — inflow/adjustment only; closed refuse; notes `source=…`
- `POST /internal/cash_events` on `InternalController`
- MCP `wv2_add_cash_event` + `summary`/`reply_text`
- Interface: `ecosystem/interfaces/winston-mcp-tools.md` §6c
- Specs: `spec/services/operations/cash_event_service_spec.rb` (6 ex)
- Live smoke: Orange +$100, Rust +$50 capital_base updates

## Related

- ADR-006 CashEvent capital-only rebalance  
- `InternalPortfolioStatus` already lists cash_events  
