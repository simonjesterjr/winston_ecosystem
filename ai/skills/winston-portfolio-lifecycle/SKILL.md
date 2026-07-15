---
name: winston-portfolio-lifecycle
description: Create, configure, and activate Wv2 live portfolios — add markets, sync data, link strategies.
---

# Winston Portfolio Lifecycle

## Triggers

- "create a portfolio", "add NVDA to portfolio X", "activate portfolio"
- "set up a new live portfolio", "add market"

## MCP Tools

- `wv2_create_portfolio`
- `wv2_add_market`
- `wv2_activate_portfolio`
- `wv2_deactivate_portfolio`
- `wv2_list_trading_strategies`
- `wv2_list_portfolios`
- `wv2_sync_data`

## Playbook — New Portfolio

1. `wv2_list_trading_strategies` — confirm strategy name exists if user specified one.
2. `wv2_create_portfolio` with `name`, `initial_capital`, `markets[]`, optional `trading_strategy_name` and risk params.
3. For each additional symbol: `wv2_add_market` with `portfolio_id_or_name` and `symbol`.
4. `wv2_sync_data` for the portfolio — ensure DM parquet coverage.
5. `wv2_activate_portfolio` when ready for daily analysis.
6. Confirm via `wv2_list_portfolios` — report id, capital_base, markets, linked strategy.

## Playbook — Add Market to Existing

1. `wv2_list_portfolios` — resolve portfolio id/name.
2. `wv2_add_market` — add symbol to book.
3. `wv2_sync_data` — request DM acquisition for the new symbol.
4. Report updated markets list from tool response.

## Playbook — Activate / Deactivate

Triggers: "activate the portfolio", "activate #157", "make it Active", "deactivate …"

1. **Resolve `id_or_name` without re-asking when possible:**
   - Explicit id/name in the user message, else
   - **"the portfolio" / "it"** = the OP most recently transferred, created, or discussed in this conversation (e.g. transfer returned `#157`), else
   - One `wv2_list_portfolios` only if still ambiguous — then ask once.
2. Call **only** `wv2_activate_portfolio` or `wv2_deactivate_portfolio`.
3. Reply in ≤ 4 lines:
   - `Activated #{id} “{name}” — active=true` (or `already_active`)
   - On mutex/conflict: report conflicting Active OP ids; do not invent force unless user said force.
4. **Do not** follow with get_portfolio_status, sync, daily analysis, or menus unless asked.

## Idempotency

- Name-based upsert is acceptable for `wv2_create_portfolio`.
- Re-adding an existing market should return cleanly — do not retry in a loop.

## Error Handling

| Code | Action |
|------|--------|
| `not_found` | List portfolios or strategies to clarify names |
| `invalid_input` | Report missing required fields |
| `sync_failed` | Report symbols affected; one retry acceptable |

## Never Do

- Skip `wv2_sync_data` before first daily analysis on new symbols
- Invent strategy names not in `wv2_list_trading_strategies`
- Mutate positions directly — only portfolio/book setup via MCP
- Ask for portfolio id when the last transfer/create in-thread already named it
- After activate, offer sync/daily-report menus