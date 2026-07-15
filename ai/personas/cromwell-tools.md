# Tool Usage Notes

Tool signatures are provided automatically via function calling.
This file documents non-obvious constraints. Workflow playbooks are in `skills/`.

## Winston MCP (wv2_*)

All Wv2 state changes go through audited MCP tools — never `exec`, never direct DB access.
See `ecosystem/interfaces/winston-mcp-tools.md` for the contract.

| Tool family | Skill |
|-------------|-------|
| Daily analysis + report | `winston-daily-ops`, `winston-report-delivery` |
| Portfolio setup | `winston-portfolio-lifecycle` |
| WUT promotion / handoff | `winston-wut-to-wv2` |
| Integration failures / correlation trace | `winston-audit-trail` |

## After mutating tools — lead with that result

When any **mutating** MCP tool returns (`wv2_transfer_portfolio_from_wut`, `wv2_create_portfolio`, `wv2_activate_portfolio`, `wv2_deactivate_portfolio`, `wv2_add_market`, `wv2_confirm_journal`, `wv2_mark_task_done`, capital activation, close/successor, etc.):

1. **Lead the reply** with that tool’s outcome: `status`, key ids, `action` if present, name, active/mode flags, top warnings.
2. Do **not** bury the mutation under a later `wv2_list_portfolios` inventory or generic briefing.
3. Do **not** auto-chain follow-up mutators (activate → sync → report) unless the user already asked for them in this turn.
4. List dumps are optional verification only — never the only story of a successful mutation.

Handoff detail (success template, forbidden menus): skill `winston-wut-to-wv2`.

## message — Telegram PDF Delivery

When delivering daily reports, use `media=[telegram_media_path]` from the MCP response.
Never paste filenames or paths as clickable links.

## cron — Scheduled Reminders

See the `cron` skill (nanobot builtin) for syntax.
Use `tz: "America/Denver"` for market-close schedules.

## exec — Safety Limits

- Commands have a configurable timeout (default 60s)
- Dangerous commands are blocked
- Output truncated at 10,000 characters
- Use `grep` on `memory/HISTORY.md` to recall past events — not for state changes