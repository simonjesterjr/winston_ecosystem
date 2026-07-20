# Ticket: Bulk risk actions (exit-all market, move-all pyramid stops)

**Status:** Done (2026-07-17)  
**Date:** 2026-07-17  
**Epic:** `2026-07-17-ops-daily-demo-epic.md`  

## Problem

Desk needs: close all lots for a market on an OP; move all pyramided stops for a market/OP. Today: single-position exit and single stop update only.

## Scope

1. `exit_all <portfolio> <symbol> price=P` — full lots open for symbol (human-gated, per-lot journals or one multi-lot policy — decide in impl).  
2. `stops <portfolio> <symbol> price=S` or `move_stops` — update all open lots for symbol.  
3. Wire shell + internal (+ MCP if thin).  
4. Specs: multi-lot paper OP.

## Acceptance

- [x] One command flattens multi-lot market on paper OP  
- [x] One command moves all stops for symbol on OP  

## Implementation decision

**Per-lot journals** for `exit_all` (not one multi-lot journal): each lot runs `AdHocExitService` so capital flow, fulfillment_details, and audit match single-lot exit. Batch is **all-or-nothing** (outer transaction). Same `price` + optional `reason` for every lot.

## Delivered

| Surface | Detail |
|---------|--------|
| `BulkMarketExitService` | All open lots for symbol → N× AdHocExitService |
| `BulkStopUpdateService` | All open lots → N× PositionStopUpdateService |
| Ops shell | `exit_all`, `stops` / `move_stops` (+ bare trailing price) |
| Internal API | `POST /internal/journals/exit_all`, `POST /internal/positions/stops_bulk` |
| MCP | `wv2_exit_all_trades`, `wv2_update_stops` + reply_text |
| Specs | multi-lot flatten, multi-lot stops, shell integration |
| Docs | MCP interface §6b2/6b3, ad-hoc-fill skill |

### Operator examples

```text
exit_all Blue MSFT price=420 reason=external_stop
stops Orange MSFT price=395
move_stops Orange MSFT 395
```

Telegram/MCP:
```text
wv2_exit_all_trades { portfolio_id_or_name: "12", symbol: "MSFT", price: 420, reason: "external_stop" }
wv2_update_stops { portfolio_id_or_name: "6", symbol: "MSFT", stop_price: 395 }
```

## Related

- PyramidStopAdjuster (confirm path partial)  
- Single exit: `2026-07-16-mcp-exit-trade-and-skill.md`  
- External stop reason: `2026-07-17-ops-daily-external-stop-exit.md`  
