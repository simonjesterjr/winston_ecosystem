---
name: winston-wut-to-wv2
description: Transfer a vetted WUT backtest or TradingStrategy configuration into Wv2 as an Operational Portfolio (handoff confirmation only).
---

# Winston WUT to Wv2 Transfer

## Triggers

- "transfer portfolio from WUT", "promote the backtest", "move run X to live"
- "transfer the latest good one", "promote trading strategy"

## MCP Tools

| Tool | When |
|------|------|
| `wv2_transfer_portfolio_from_wut` | **Primary** — always for this skill |
| `wv2_list_portfolios` | Optional verify only if transfer payload omits `portfolio.id` / name; do not lead with this dump |
| `wv2_activate_portfolio` | **Only if user explicitly asks** to activate after transfer |
| `wv2_sync_data` | **Only if user explicitly asks** to sync |
| `wv2_list_trading_strategies` | Rare; only if user asks about strategy linkage |

## Inputs (one of)

- `{ "run_id": 42 }` — WUT backtest run
- `{ "ts_id": 7 }` — first-class TradingStrategy
- `{ "config_name": "my-trend.json" }` — file under shared `/portfolio_configs` volume

## Playbook

1. Clarify which source if ambiguous (run_id vs ts_id vs config name).
2. Confirm with the user when capital or real-intent markets are involved (paper import is the default).
3. Call **only** `wv2_transfer_portfolio_from_wut` with the resolved input.
4. **Stop and report** using the success template below. Do **not** chain activate, sync, or daily ops unless the user just asked for those.

Optional: one `wv2_list_portfolios` call **after** transfer only to fill missing fields or name the sole Active OP — never as the main story of the reply.

## Success reply contract (mandatory)

After a successful transfer, the **first two lines** of the user-facing reply must come from the transfer tool result — not from a portfolio list briefing.

### Lead fields (use tool JSON)

| Field | Source | Required |
|-------|--------|----------|
| status | top-level `status` | yes |
| action | top-level `action` | yes |
| portfolio.id | `portfolio.id` | yes |
| name | `portfolio.name` | yes |
| active | `portfolio.active` | yes |
| execution_mode | `portfolio.execution_mode` (default `paper` if absent) | yes |
| warnings | top-level `warnings` — at most top 2–3, one short line each | if present |

If the tool later includes a top-level `summary` string (MCP ticket C), you may use that as line 1 and still expand id/action on line 2.

### Action → plain English

| `action` | Say |
|----------|-----|
| `created` | New Operational Portfolio created |
| `legacy_updated` | Updated existing OP (legacy bare-name path; no fingerprint) |
| `forked` | New OP forked (different methodology / fingerprint) |
| `adopted` | Adopted fingerprint onto existing OP |
| `engaged_refuse` | Refused — OP is engaged (journals exist); shape not mutated |
| `closed_refuse` | Refused — OP is closed; import not applied in place |

Treat `engaged_refuse` / `closed_refuse` as **failed handoffs for the user’s goal** even if HTTP status is structured: lead with the refuse reason, do not claim success.

### Template (copy structure)

```
Transfer OK — {plain-English action}: OP #{id} “{name}”
active={true|false}, execution_mode={paper|real}
{one warning line if any}
Sole Active OP unchanged: #{id} “{name}”   ← only if you know it; omit if unknown
```

**Example (legacy_updated):**

```
Transfer OK — Updated existing OP (legacy path): #157 “Portfolio Blank (WUT run 57)”
active=false, execution_mode=paper
Warning: legacy_no_fingerprint (re-export with fingerprint when possible)
Sole Active OP unchanged: #12 “…”
```

Keep the whole reply short (≤ ~8 lines). One optional sentence of context is fine; no inventory tables.

## Forbidden after transfer (unless user already asked)

Do **not**:

- Call or offer `wv2_activate_portfolio`
- Call or offer `wv2_sync_data`
- Run or offer daily analysis / daily report (`winston-daily-ops`, `winston-report-delivery`)
- Numbered menus: “Would you like to: 1) activate 2) sync 3) report…”
- “Would you like to proceed?” / “Next steps” option lists
- Lead with a full portfolio inventory or “briefing” that buries the transfer result

If the user later asks to activate, sync, or run daily ops, use skill `winston-portfolio-lifecycle` or `winston-daily-ops` **in a new turn**.

## Error Handling

| Code / outcome | Action |
|----------------|--------|
| `not_found` | Ask for run_id, ts_id, or config_name; check WUT exported the config |
| `invalid_input` | Specify exactly one of run_id, ts_id, config_name |
| `engaged_refuse` / `closed_refuse` | Report refuse plainly; suggest close/successor or different seed — no activate menu |
| Tool `status: error` | Lead with `code` + `message`; ignore unrelated `retry_guidance` (e.g. EOD fetch_only text on non-report tools) |

## Future (Part 2)

When `wut_list_vetted_runs` MCP tool exists, use it to resolve "transfer the best vetted trend run from last month" before calling transfer.

## Never Do

- Transfer without user confirmation when capital or live/real markets are involved
- Auto-activate or auto-sync after transfer
- Modify WUT state from this skill — transfer is WUT export → Wv2 import only
- Narrate only a subsequent `wv2_list_portfolios` dump and skip the transfer `action` / `#id`
