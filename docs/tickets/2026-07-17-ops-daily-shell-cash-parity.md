# Ticket: Ops shell cash parity (`cash` command)

**Status:** Done (2026-07-17)  
**Date:** 2026-07-17  
**Epic:** `2026-07-17-ops-daily-demo-epic.md`  

## Problem

Capital add/remove works via `wv2_add_cash_event` / internal API but Ops shell HELP does not expose a `cash` verb — demo path requires Telegram or curl.

## Scope

1. Ops shell: `cash <portfolio> amount=N [type=inflow|adjustment] [notes=…]` → `CashEventService`.  
2. HELP + panels refresh on success.  
3. Spec for parse + service call.

## Implementation

| Surface | Change |
|---------|--------|
| `ops_shell_chat.rb` | `cash` / `add_cash` / `cash_event` / `inflow` → `CashEventService` (`source=ops_shell`); HELP; `amount=` / `type=`; bare amount |
| Ops shell UI (`home/index`, `_panels`) | Placeholder + system copy list cash; Active OP **cash** fill + **cash form** links |
| Desk form (`desk_actions`) | `task_type=cash` → amount + event_type → `CashEventService` (`source=desk_form`) |
| `desk_action_handoff.rb` | Cash phrases/paths without symbol |
| Specs | shell cash (10) + handoff cash phrase (1) |

### Command forms

```
cash Blue amount=5600 notes=weekly
cash 12 500
cash 12 amount=-100 type=adjustment notes=correction
```

Desk form: `/operations/desk?portfolio_id=12&task_type=cash`  
Same service as MCP `wv2_add_cash_event` — no parallel accounting.

## Acceptance

- [x] Ops UI can top-up and reverse capital without MCP (shell chat + desk form)  
- [x] Same service as MCP (no parallel accounting)  
- [x] Specs green (11 cash-related)  
- [x] Live smoke: shell + handoff phrase + desk service path on Blue #12  
- [x] Console/UI surfaces advertise cash (not chat-backend-only)  

## Related

- Done: `2026-07-14-wv2-cash-inflow-mcp.md`  
- Smoke checklist: `2026-07-17-ops-daily-demo-smoke-checklist.md` (shell cash was GAP; closed here)  
