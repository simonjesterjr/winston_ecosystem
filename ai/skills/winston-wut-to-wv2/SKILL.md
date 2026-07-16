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

After a successful transfer, paste the tool’s user-facing text — **do not rewrite** into a portfolio briefing.

### Priority order

1. **`reply_text`** present → paste **verbatim** as the entire reply. Done.
2. Else **`summary`** → use as line 1; still ensure `action` + `#id` appear on line 1.
3. Else build from fields below.

### Lead fields (use tool JSON)

| Field | Source | Required |
|-------|--------|----------|
| status | top-level `status` | yes |
| action | top-level `action` | yes — **must appear on line 1** |
| portfolio.id | `portfolio.id` | yes — **must appear as `#id` on line 1** |
| name | `portfolio.name` | yes |
| active | `portfolio.active` | yes |
| execution_mode | `portfolio.execution_mode` (default `paper` if absent) | yes |
| fingerprint | `portfolio.fingerprint` — short 8 hex optional on line 1 | if present |
| warnings | top-level `warnings` — at most top 2, one short line each | if present |

### Action → plain English

| `action` | Say |
|----------|-----|
| `created` | New Operational Portfolio created |
| `legacy_updated` | Updated existing OP (legacy bare-name path) |
| `forked` | New OP forked (different methodology / fingerprint) |
| `adopted` | Adopted fingerprint onto existing OP |
| `engaged_refuse` | Refused — OP is engaged (journals exist); shape not mutated |
| `closed_refuse` | Refused — OP is closed; import not applied in place |

Treat `engaged_refuse` / `closed_refuse` as **failed handoffs for the user’s goal** even if HTTP status is structured: lead with the refuse reason, do not claim success.

### Template (copy structure)

```
Transfer OK — {plain-English action}: #{id} “{name}” · {shortFp?}
active={true|false}, execution_mode={paper|real}
{one warning line if any}
```

**Example (adopted / fingerprinted):**

```
Transfer OK — Adopted fingerprint onto existing OP: #6 “Portfolio Orange · 6622b2eb” · 6622b2eb
active=false, execution_mode=paper
Warning: paper_caps:max_leverage normalized to 1.0 (was 3.0)
```

**Example (legacy_updated):**

```
Transfer OK — Updated existing OP (legacy bare-name path): #157 “Portfolio Blank (WUT run 57)”
active=false, execution_mode=paper
Warning: legacy_no_fingerprint: bare-name path (ADR-006 transition)
```

Keep the whole reply short (≤ ~6 lines). No inventory tables.

## Forbidden after transfer (unless user already asked)

Do **not**:

- Call or offer `wv2_activate_portfolio`
- Call or offer `wv2_sync_data`
- Run or offer daily analysis / daily report (`winston-daily-ops`, `winston-report-delivery`)
- Numbered menus: “Would you like to: 1) activate 2) sync 3) report…”
- Soft offers: “Would you like to check the portfolio's status, pending tasks, or market snapshots?”
- “Would you like to proceed?” / “Next steps” option lists
- **Rewrite patterns that bury `action` + `#id`:**
  - “The portfolio … has been updated with the following changes”
  - Bullet lists of markets / capital_base / Books
  - Long “No immediate actions are required…” footers (one short stop is enough; no question)

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
