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

1. **List state** — `wv2_list_portfolios`. Note active portfolios, capital_base, markets. Use **numeric ids** or full display names (`seed · shortFp`) for any later targeted call.
2. **Sync if needed** — If data may be stale or analysis failed for missing coverage, call `wv2_sync_data` per active portfolio (or with explicit symbols). Wait for result; do not loop sync calls.
3. **Resolve date** — Reports for date D require 4:30 PM MT on D to have passed. Before cutoff, "the daily" means yesterday. Never trigger analysis for a future date.
4. **Get report** — For full narrative, use `wv2_get_daily_activity_report` (see skill `winston-report-delivery`). Use `wv2_perform_daily_analysis` only when the user explicitly wants analysis without report formatting, and only after the cutoff.
   - **Full desk:** omit `portfolio_id_or_name` (analyzes Active OPs).
   - **One OP:** pass numeric id or full display name only — never bare seed like `"Portfolio Blue"` (can match closed lineage).
5. **Pending actions** — `wv2_list_pending_actions` if confirmations are relevant.
6. **Format output** — Focused operator summary (not a research essay): signals, exits, pyramids, pending confirms, capital-relevant deltas, action items. Link/PDF when available.

## Error Handling

| Code | Action |
|------|--------|
| `sync_failed` | Report error; one retry after checking symbols |
| `analysis_failed` | Check data coverage; sync then retry once |
| `not_found` | Verify via `wv2_list_portfolios`; use numeric id |
| `active_mutex` | Post tool `safe_next_step` (or: use Active conflict id / omit name). **Do not** deactivate live Active OP for desk analysis. **Do not** lead with force=true |
| `portfolio_closed` | Use `active_same_seed` id if present; do not revive closed OP |
| `ambiguous_portfolio` | Ask once with candidate ids or re-call with numeric id |

Telegram error shape: ≤ 5 lines OPS copy + optional `ref:` footer. No multi-option menus.

## Never Do

- Call `wv2_get_daily_activity_report` on simple greetings
- Loop the same tool with minor arg changes
- Invent signals not returned by tools
- Mutate positions or capital outside MCP confirmation tools (Part 2)
- Pass bare seed names for analysis when Active display names exist
- "Key Observations / Potential Next Steps" chatbot essays after tool results
