# Ticket: Link validation PortfolioBacktestRun to PortfolioSignalOptimization

**Status:** Proposed

**Date:** 2026-07-09

**Context:** Session [`2026-07-09-0833-trading-strategy-fingerprint-capture`](../session-reports/2026-07-09-0833-trading-strategy-fingerprint-capture.md). Backfill uses heuristic match (portfolio + entry + time window).

## Problem

No durable FK from validation PBR → optimization. Selection ledger can store `portfolio_signal_optimization_id` only when known at capture time; historical and future ad-hoc links remain fragile.

## Scope

1. Store `portfolio_signal_optimization_id` on PBR at `PortfolioBacktestRunFactory.create_from_optimization!` or in `results_json` from `PortfolioTrendVetter`.
2. Prefer column + index if query paths need it; else documented results_json key.
3. Update `TradingStrategyFingerprintCapture` / backfill to use the link.

## Acceptance

- Every vet-created validation run can resolve its optimization without heuristics
- Selections for new vets always populate `portfolio_signal_optimization_id`

## Related

- `PortfolioBacktestRunFactory`
- `trading_strategies:capture_validation_runs`
