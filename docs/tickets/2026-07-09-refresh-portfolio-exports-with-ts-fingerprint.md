# Ticket: Refresh portfolio JSON exports with TradingStrategy id/fingerprint

**Status:** Proposed

**Date:** 2026-07-09

**Context:** Session [`2026-07-09-0833-trading-strategy-fingerprint-capture`](../session-reports/2026-07-09-0833-trading-strategy-fingerprint-capture.md). Capture now sets `wut_trading_strategy_id` and `fingerprint` on new vet exports; historical files (`portfolio-red.json`, etc.) still lack them.

## Scope

1. Re-export or patch `portfolio_configs/portfolio-*.json` after capture/backfill so nested `trading_strategy` includes `wut_trading_strategy_id`, `fingerprint`, and TS name/description.
2. Prefer re-run of export path from existing validation PBR over full re-vet when possible.
3. Document one-shot rake or script if useful.

## Acceptance

- Red (and other completed vets) JSON reference the lab TS row used for that validation
- Wv2 import still works (backward-compatible fields)

## Related

- `portfolio_configs/portfolio-red.json`
- `PortfolioTrendVetter#export_run!`
