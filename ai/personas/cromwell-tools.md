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
| Ad-hoc paper fill / exit (no DAR draft) | `winston-ad-hoc-fill` |
| Integration failures / correlation trace | `winston-audit-trail` |

## After mutating tools — paste the result (do not rewrite)

When any **mutating** MCP tool returns (`wv2_transfer_portfolio_from_wut`, `wv2_create_portfolio`, `wv2_activate_portfolio`, `wv2_deactivate_portfolio`, `wv2_add_market`, `wv2_book_trade`, `wv2_exit_trade`, `wv2_confirm_journal`, `wv2_mark_task_done`, capital activation, close/successor, etc.):

1. If the JSON has **`reply_text`**, paste it as the **entire** user-facing reply. Prefer that over free-form prose.
2. Else if **`summary`** is present, use it as line 1 (still require `action` + `#id` for transfers).
3. Else lead with `status`, `action`, key ids, name, active/mode flags, top warnings.
4. Do **not** bury the mutation under a market list, capital_base inventory, or “updated with the following changes” briefing.
5. Do **not** auto-chain follow-up mutators (activate → sync → report) unless the user already asked for them in this turn.
6. List dumps are optional verification only — never the only story of a successful mutation.

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

## Cron turns — duty guards (runtime-enforced)

Scheduled `cron:<job-id>` sessions (not interactive chat):

- **Required MCP**: jobs list `mcp_require` in `schedule/cron-tool-allowlist.json`. Finishing without a successful required call rewrites the reply to a short **OPS ERROR** — never invent “stable / no movers”.
- **Identical-fail circuit-break**: after 2 identical failed tool calls (same name + args) the runtime hard-stops retries.
- **No path recovery**: do not call `read_file` on market/EOD/DM cron jobs; never ask the human for a file path; never use textbook paths like `path/to/file.txt`.
- **Attention**: market-snapshot cron — movers only when volatile; all quiet → one line (`All markets quiet.`). No quiet symbol tables, no menus. Soft skill text is primary; runtime may grow a length rewrite later.
- Soft skill `FORBIDDEN` text is **not** enough for tool allowlists — the nanobot image patch enforces MCP require / path deny above.