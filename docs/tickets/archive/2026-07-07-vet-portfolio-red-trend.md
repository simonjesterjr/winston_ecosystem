# Ticket: Vet Portfolio Red trend strategies

**Status:** Done (2026-07-07 vet; 2026-07-08 viability labeling)

**Date:** 2026-07-07

**Context:** [`2026-07-06-2020-portfolio-overlap-pipeline`](../session-reports/2026-07-06-2020-portfolio-overlap-pipeline.md). Portfolio Red rebuilt under overlap rules.

**Current Red membership (9):** AMAT, CDE, MSFT, MSOS, PHYMF, ROKU, URA, VXX, XLV

## Result (PBR 25 / winner validation)

| Field | Value |
|-------|-------|
| Winner entry | `Breakout50DayNoHistoryStrategy` |
| Winner exit | `VolatilityExitStrategy` |
| Total return | **+636.3%** |
| Max drawdown | **64.0%** |
| Trades | 1051 |
| Sharpe | null |
| `export_kind` | **observation** (failed max_drawdown ≤ 50%) |
| Export | `portfolio_configs/portfolio-red.json` |
| Log | `portfolio_configs/portfolio-red-vet.log` |

## Acceptance

- [x] Optimization completed (screening + finals + winner PBR)
- [x] Export exists with Red markets
- [x] Economics recorded; not trade-ready — observation only for Wv2 paper

## Related

- Plan task #2 (completed)
- WUT: `lib/tasks/portfolio_trend_vet.rake`, `PortfolioTrendVetter`, `TradeReadyViabilityGates`