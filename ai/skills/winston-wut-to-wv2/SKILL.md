---
name: winston-wut-to-wv2
description: Transfer a vetted WUT backtest or TradingStrategy configuration into live Wv2.
---

# Winston WUT to Wv2 Transfer

## Triggers

- "transfer portfolio from WUT", "promote the backtest", "move run X to live"
- "transfer the latest good one", "promote trading strategy"

## MCP Tools

- `wv2_transfer_portfolio_from_wut` (primary)
- `wv2_list_portfolios` (verify result)
- `wv2_activate_portfolio` (if not auto-active)
- `wv2_sync_data` (ensure data for new markets)
- `wv2_list_trading_strategies` (confirm linked strategy)

## Inputs (one of)

- `{ "run_id": 42 }` — WUT backtest run
- `{ "ts_id": 7 }` — first-class TradingStrategy
- `{ "config_name": "my-trend.json" }` — file under shared `/portfolio_configs` volume

## Playbook

1. Clarify which source if ambiguous (run_id vs ts_id vs config name).
2. `wv2_transfer_portfolio_from_wut` with the resolved input.
3. On success — note `portfolio.id`, `name`, `markets`, `capital_base`, `config_path`.
4. Chain lifecycle steps (read skill `winston-portfolio-lifecycle`):
   - `wv2_sync_data` for transferred markets
   - `wv2_activate_portfolio` if inactive
   - Optional: run daily ops (skill `winston-daily-ops`) if user wants immediate analysis
5. `wv2_list_portfolios` — confirm final state.

## Error Handling

| Code | Action |
|------|--------|
| `not_found` | Ask for run_id, ts_id, or config_name; check WUT has exported the config |
| `invalid_input` | Specify exactly one of run_id, ts_id, config_name |

## Future (Part 2)

When `wut_list_vetted_runs` MCP tool exists, use it to resolve "transfer the best vetted trend run from last month" before calling transfer.

## Never Do

- Transfer without user confirmation when capital or live markets are involved
- Skip sync after transfer — new symbols need DM parquet coverage
- Modify WUT state from this skill — transfer is WUT export → Wv2 import only