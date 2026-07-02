---
name: winston-daily-ops
description: Run the Winston daily trading flow and produce the 11-point narrative for active portfolios.
---

# Winston Daily Ops

## Triggers

- "run the daily", "do analysis", "run the numbers"
- Heartbeat after 4:30 PM MT on trading days
- Explicit analysis for a named portfolio

## MCP Tools

- `wv2_list_portfolios`
- `wv2_sync_data`
- `wv2_perform_daily_analysis` (explicit analysis only — see below)
- `wv2_get_daily_activity_report` (preferred for report + narrative)
- `wv2_list_pending_actions`

## Playbook

1. **List state** — `wv2_list_portfolios`. Note active portfolios, capital_base, markets.
2. **Sync if needed** — If data may be stale or analysis failed for missing coverage, call `wv2_sync_data` per active portfolio (or with explicit symbols). Wait for result; do not loop sync calls.
3. **Resolve date** — Reports for date D require 4:30 PM MT on D to have passed. Before cutoff, "the daily" means yesterday. Never trigger analysis for a future date.
4. **Get report** — For full narrative, use `wv2_get_daily_activity_report` (see skill `winston-report-delivery`). Use `wv2_perform_daily_analysis` only when the user explicitly wants analysis without report formatting, and only after the cutoff.
5. **Pending actions** — `wv2_list_pending_actions` if confirmations are relevant.
6. **Format output** — Post a concise 11-point-style summary:

   - Active portfolios and markets
   - Data sync status (if relevant)
   - New entrance signals
   - Exit signals
   - Pyramiding opportunities
   - Passed signals with reasons
   - Outstanding confirmations / operations_tasks
   - Capital base and position summary
   - Action items for principals

## Error Handling

| Code | Action |
|------|--------|
| `sync_failed` | Report error; offer one retry after checking symbols |
| `analysis_failed` | Check data coverage; sync then retry once |
| `not_found` | Verify portfolio name via `wv2_list_portfolios` |

## Never Do

- Call `wv2_get_daily_activity_report` on simple greetings
- Loop the same tool with minor arg changes
- Invent signals not returned by tools
- Mutate positions or capital outside MCP confirmation tools (Part 2)