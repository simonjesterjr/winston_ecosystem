# Ticket: Revisit Portfolio Blue membership and strategy viability

**Status:** Proposed

**Date:** 2026-07-07

**Context:** Blue vet completed in [`2026-07-06-2020-portfolio-overlap-pipeline`](../session-reports/2026-07-06-2020-portfolio-overlap-pipeline.md). All six entry strategies lost heavily; winner `SwingBreakout5DayStrategy` still **-98.3%** return, **100%** max drawdown (run 23). Export exists at `portfolio_configs/portfolio-blue.json` but is **not Wv2-ready**.

**Current Blue membership (11):** AAL, AMZN, GLD, GOOGL, JNJ, PG, RXT, TSLA, TSMC, WMT, XLE

## Problem

Strong correlation diversification (mean |r| ≈ 0.12) did not translate to trend-following profitability under current vet defaults. Unclear whether root cause is membership (too equity-heavy, wrong sectors), strategy set (breakout-only, fixed exit), or base config (capital, risk %, ranking metric).

## Scope

Investigate and decide (document decision in plan or analysis):

1. **Membership hypothesis** — rebuild Blue with DM-suitable-heavy pool once registry compose works; compare vet metrics.
2. **Strategy hypothesis** — see priority ticket `2026-07-07-portfolio-trading-strategy-evaluation-framework.md`.
3. **Ranking metric** — Blue vet used `practical_sharpe_ratio` but all Sharpe values were `null`; confirm optimizer ranking behavior.
4. Do **not** import to Wv2 until a strategy passes agreed viability thresholds.

## Acceptance

- Written recommendation: keep membership / revise membership / revise strategy defaults (with evidence from at least one re-vet or controlled backtest).
- Updated `portfolio-blue-sidecar.json` or new sidecar if membership changes.

## Related

- Plan task #3
- Priority: `docs/tickets/2026-07-07-portfolio-trading-strategy-evaluation-framework.md`