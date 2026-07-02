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
| WUT promotion | `winston-wut-to-wv2` |

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