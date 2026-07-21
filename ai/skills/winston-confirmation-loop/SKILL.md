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
- `wv2_edit_journal` — amend draft units/price/notes/stop **without** executing
- `wv2_confirm_journal`
- `wv2_mark_task_done`
- `wv2_get_portfolio_status`
- `wv2_list_portfolios`

## Playbook — Inspect

1. `wv2_list_portfolios` — note Active OP(s). Paper focus is typically a single Active book.
2. `wv2_list_pending_actions` with optional `portfolio_id_or_name` and `as_of` (default today).
3. For each interesting task, `wv2_get_journal` with `journal_id` if present.
4. Report: task_id, journal_id, market, task_type, **signal_date / fill_date**, proposed price — **do not invent fills**.

## EOD cadence (ADR-009)

- **Signal Date T** — DA created the draft (`signal_date`).
- **Fill Date T+1** — intended next session (`fill_date`); next-open prefill when DM parquet has the bar (`next_open_available`).
- If awaiting next open, ask the human for fill price — do not invent open from signal close.

## Playbook — Edit draft (optional, before confirm)

1. When the human wants to **change size/price/stop/notes** but not fill yet: `wv2_edit_journal`.
2. Required: `journal_id` + at least one of units / price / stop_price / notes / …
3. Paste **`reply_text`**. Journal stays **draft** — do **not** auto-confirm.
4. Shell: `edit_journal 16 units=5 price=251.03 stop=245 notes=size-down`

## Playbook — Confirm

1. Confirm only when the human explicitly authorizes a fill (price/units if required).
2. Prefer `wv2_confirm_journal` with:
   - `journal_id` (required)
   - `execution_price` when overriding (or omit to use next-open / sticky draft price)
   - `units` when PositionSizer would return 0 or human specifies size (or sticky after edit)
   - `notes` short reason (e.g. "paper confirm Blue PBR62")
3. Alternative: `wv2_mark_task_done` with `task_id` (defaults `confirm_journal: true`).
4. Immediately `wv2_get_portfolio_status` on the OP — report capital_base and open positions.
5. Idempotent re-confirm of an already-executed journal is OK (tool returns `idempotent: true`).

## Example (paper)

```
wv2_list_pending_actions { portfolio_id_or_name: "12" }
wv2_edit_journal { journal_id: 16, units: 5, price: 251.03, stop_price: 245.0, notes: "size-down" }
wv2_confirm_journal { journal_id: 16, notes: "paper confirm" }
wv2_get_portfolio_status { portfolio_id_or_name: "12" }
```

## Error Handling

| Code / symptom | Action |
|----------------|--------|
| `not_found` | Re-list pending; journal may have been cleaned up |
| `invalid_state` | Journal not draft — report status; do not force (edit also refuses executed) |
| `confirmation_failed` / zero units | Ask for explicit `units=` or `wv2_edit_journal` first; ATR sizing may be broken for some symbols |
| Empty pending | Say so; do not invent tasks |

## Never Do

- Confirm without human authorization of the fill
- Edit an **executed** journal (immutable — use new ad-hoc enter/exit instead)
- Auto-confirm after edit unless the human asked to fill
- Mutate positions outside these MCP tools
- Bypass services with ad-hoc SQL or direct DB edits
- Loop confirm retries on permanent errors

## Desk shell

The Wv2 ops shell (`http://localhost:3002`) uses the same services (`edit_journal` / `confirm` / `pending` / `status` chat commands). Prefer MCP on Telegram; shell is for desk verification.
