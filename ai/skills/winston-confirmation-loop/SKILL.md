---
name: winston-confirmation-loop
description: List pending paper/live action items and confirm journals via MCP — list pending → confirm → status.
---

# Winston Confirmation Loop

## Triggers

- "confirm the trade", "fill this", "any pending actions?"
- "mark task done", "execute the journal"
- After daily report when pending actions exist
- Telegram / ops shell confirm workflow

## MCP Tools

- `wv2_list_pending_actions`
- `wv2_get_journal`
- `wv2_confirm_journal`
- `wv2_mark_task_done`
- `wv2_get_portfolio_status`
- `wv2_list_portfolios`

## Playbook — Inspect

1. `wv2_list_portfolios` — note Active OP(s). Paper focus is typically a single Active book.
2. `wv2_list_pending_actions` with optional `portfolio_id_or_name` and `as_of` (default today).
3. For each interesting task, `wv2_get_journal` with `journal_id` if present.
4. Report: task_id, journal_id, market, task_type, report_date, suggested price — **do not invent fills**.

## Playbook — Confirm

1. Confirm only when the human explicitly authorizes a fill (price/units if required).
2. Prefer `wv2_confirm_journal` with:
   - `journal_id` (required)
   - `execution_price` when overriding signal price
   - `units` when PositionSizer would return 0 or human specifies size
   - `notes` short reason (e.g. "paper confirm Blue PBR62")
3. Alternative: `wv2_mark_task_done` with `task_id` (defaults `confirm_journal: true`).
4. Immediately `wv2_get_portfolio_status` on the OP — report capital_base and open positions.
5. Idempotent re-confirm of an already-executed journal is OK (tool returns `idempotent: true`).

## Example (paper)

```
wv2_list_pending_actions { portfolio_id_or_name: "12" }
wv2_confirm_journal { journal_id: 16, units: 5, execution_price: 251.03, notes: "paper confirm" }
wv2_get_portfolio_status { portfolio_id_or_name: "12" }
```

## Error Handling

| Code / symptom | Action |
|----------------|--------|
| `not_found` | Re-list pending; journal may have been cleaned up |
| `invalid_state` | Journal not draft — report status; do not force |
| `confirmation_failed` / zero units | Ask for explicit `units=`; ATR sizing may be broken for some symbols |
| Empty pending | Say so; do not invent tasks |

## Never Do

- Confirm without human authorization of the fill
- Mutate positions outside these MCP tools
- Bypass services with ad-hoc SQL or direct DB edits
- Loop confirm retries on permanent errors

## Desk shell

The Wv2 ops shell (`http://localhost:3002`) uses the same services (`confirm` / `pending` / `status` chat commands). Prefer MCP on Telegram; shell is for desk verification.
