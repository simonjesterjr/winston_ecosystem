# Ticket: Revisit Portfolio Blue membership and strategy viability

**Status:** In progress (membership still open; **strategy/risk rescue evidence strong**)

**Date:** 2026-07-07

**Last updated:** 2026-07-13 — PBR business analysis + Level 2 C0/P1 runs

**Context:** Blue vet completed in [`2026-07-06-2020-portfolio-overlap-pipeline`](../session-reports/2026-07-06-2020-portfolio-overlap-pipeline.md). All six entry strategies lost heavily under **static/isomorphic**; winner `SwingBreakout5DayStrategy` still **-98.3%** return, **100%** max drawdown (run 23) at that time.

**2026-07-09 update:** Orange and White also finished first-pass vet as **observation** — see [`2026-07-09-1308-orange-white-vet-trend`](../session-reports/2026-07-09-1308-orange-white-vet-trend.md).

**2026-07-13 update (business analysis):** Membership alone was **not** the only failure mode. Same Blue books + Swing entry under **`one_way_dynamic` accelerating pyramid + `move_to_last_entry`** produces lab standouts:

| PBR | Config sketch | Ret | Max DD | Gates |
|-----|---------------|-----|--------|-------|
| 23 | static + isomorphic | −137% | 134% | fail |
| 48 | dynamic R1, max_mkt nil | +2073% | 21% | trade_ready |
| 62 | dynamic R1, **max_mkt=4** | +1415% | 42% | trade_ready |
| 63 | 48 + position_swap on | +975% | 31% | trade_ready (worse than 48) |

Canonical write-up: [`business_analysis/2026-07-13-pbr-return-dd-pcs-evaluation.md`](../../business_analysis/2026-07-13-pbr-return-dd-pcs-evaluation.md).  
**Recommendation shift:** prioritize **risk-regime + capacity policy** over rebuilding Blue membership first; membership revisit remains optional (corr_v2 quality) not the blocker for paper exploration of Blue 62.

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