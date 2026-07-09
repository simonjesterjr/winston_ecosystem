# Ticket: Use saved TradingStrategy in backtest workflow (slice B)

**Status:** Proposed

**Date:** 2026-07-09

**Context:** Session [`2026-07-09-0833-trading-strategy-fingerprint-capture`](../session-reports/2026-07-09-0833-trading-strategy-fingerprint-capture.md). Slice A delivered auto-capture + selection ledger on `/trading_strategies`.

## Problem

Backtest / optimization forms still only “build new” or “promote after.” Operators cannot pick a saved fingerprinted **TradingStrategy** as the recipe for a new PortfolioBacktestRun or fixed-strategy revalidation.

## Scope

1. New Portfolio Backtest form: **Use saved TS** (select active/fingerprinted TS) **or** build config manually.
2. Seed run + market configs from `TradingStrategy#to_run_config` / `fingerprint_payload` (date window optional override).
3. Optional: Portfolio Signal Optimization UI — pin to one TS (no grid) for validation-only re-run.
4. Docs: portfolio lifecycle + `portfolio_configs/README.md` workflow section.

## Acceptance

- Operator can start a PBR from an existing TS without re-entering entry/exit/risk fields
- Selected TS id recorded on run (results_json or FK) for provenance
- Manual / grid path unchanged

## Related

- `winston_unit_test/app/services/trading_strategy_fingerprint_capture.rb`
- `winston_unit_test/app/views/portfolio_backtest_runs/new.html.erb`
