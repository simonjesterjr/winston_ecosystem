---
name: winston-decision-verifier
description: Advisory TAKE|SIZE_DOWN|SKIP|HOLD on pending DAR drafts. Never confirms. Separate from EOD narrator.
---

# Winston Decision Verifier (checker)

Maker is deterministic DAR + PositionSizer. This skill is the **checker** only. Human remains the fill gate (`winston-confirmation-loop`).

## Triggers

- EOD daily-loop when pending drafts exist
- "verify pending", "should we take this draft?", "checker on journal N"

## Inputs (facts only)

From `wv2_get_daily_activity_report` pending / `wv2_list_pending_actions` / `wv2_get_journal`:

- journal_id, task_id, OP id/name, execution_mode, symbol
- task_type (enter/exit/pyramid), direction
- proposed units/price/stop when present
- signal_date / fill_date, reason codes from payload
- LEAP/option fields if present (premium, expiry) — do not recompute Edge (R)

Do **not** use narrator prose, MEMORY essays, or similar-day stories you cannot cite from this turn's tools.

## Output (one line per journal)

```
J#<id> <SYMBOL> <TAKE|SIZE_DOWN|SKIP|HOLD> — <≤12 words, grounded>
```

| Verdict | When |
|---------|------|
| `TAKE` | Facts look internally consistent; still **not** a fill |
| `SIZE_DOWN` | Size/cash/LEAP premium looks tight vs payload — suggest human edit, do not edit |
| `SKIP` | Payload says passed / duplicate / missing price / not a draft |
| `HOLD` | Awaiting next open, missing field, or Mode C packaging question — wait for human |

Also copy the same lines into `state/STATE-YYYY-MM-DD.md` when the daily loop is running.

## Never

- `wv2_confirm_journal` / `wv2_mark_task_done` / `wv2_edit_journal`
- Invent execution_price or units
- Recompute Edge, stops, or LEAP packaging
- Telegram menus or "would you like me to confirm"
- Quiet-day essays when pending_count is 0 (say nothing extra)
