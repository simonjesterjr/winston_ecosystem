---
name: winston-wut-portfolio-lifecycle
description: Manage WUT lab portfolios via Telegram — add markets, sync DM data, run daily operations. Distinct from Wv2 live portfolio tools.
---

# Winston WUT Portfolio Lifecycle

## When to Use WUT vs Wv2

| Intent | Tools |
|--------|-------|
| Lab portfolio, backtests, signal tuning, WUT Operations reports | `wut_*` |
| Live trading, Wv2 Daily Activity PDF, capital/positions | `wv2_*` |
| Move vetted config from lab → live | `wv2_transfer_portfolio_from_wut` only; then skill `winston-wut-to-wv2` reply contract |

## Triggers

- "add GOLD to my WUT portfolio", "add CLETF to portfolio X"
- "sync WUT data", "run WUT daily ops"
- "what's in my lab portfolio", "WUT daily report"

## MCP Tools

- `wut_list_portfolios`
- `wut_list_portfolio_runs`
- `wut_add_market`
- `wut_sync_portfolio_data`
- `wut_run_daily_operations`
- `wut_get_daily_operations_report`

## Playbook — Add Market

1. `wut_list_portfolios` — resolve portfolio id/name.
2. `wut_add_market` with `portfolio_id_or_name` and `symbol`. Aliases resolve automatically (e.g. GOLD → CLETF).
3. `wut_sync_portfolio_data` if sync was skipped or user wants explicit refresh.
4. Report updated markets from tool response.

## Playbook — Daily Operations

1. `wut_list_portfolios` — confirm `active_account_id` is present. If missing, tell user to create ActiveAccount in WUT Operations UI first.
2. `wut_sync_portfolio_data` when data may be stale.
3. `wut_run_daily_operations` — runs signals/tasks for the ActiveAccount.
4. Format summary from `report` payload (equity, signals, warnings, passed opportunities).

To read without re-running: `wut_get_daily_operations_report`.

## Playbook — Transfer to Live

After lab work is vetted:

1. `wut_list_portfolio_runs` — pick `run_id`.
2. `wv2_transfer_portfolio_from_wut` with that `run_id`.
3. **Stop.** Report using skill `winston-wut-to-wv2` success template (`action`, OP `#id`, active, execution_mode). Do **not** auto-activate, sync, or open daily ops — only if the user asks next.

## Error Handling

| Error | Action |
|-------|--------|
| `portfolio not found` | `wut_list_portfolios` to clarify name |
| `no_active_account` | Direct user to WUT Operations UI |
| `not_ready` (report) | Run `wut_run_daily_operations` or wait for 6 AM Sidekiq job |

## Never Do

- Use `wv2_add_market` for WUT lab portfolios
- Use `wut_*` tools for Wv2 Daily Activity PDF delivery (use `wv2_get_daily_activity_report`)
- Assume GOLD is a ticker — it resolves to CLETF in WUT