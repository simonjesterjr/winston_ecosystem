# Ticket: Vet Portfolio Red trend strategies

**Status:** Proposed

**Date:** 2026-07-07

**Context:** [`2026-07-06-2020-portfolio-overlap-pipeline`](../session-reports/2026-07-06-2020-portfolio-overlap-pipeline.md). Portfolio Red rebuilt under overlap rules; Blue vetting completed (run 23). Red vet not run.

**Current Red membership (9):** AMAT, CDE, MSFT, MSOS, PHYMF, ROKU, URA, VXX, XLV

## Problem

Red has no `portfolios:vet_trend` optimization or Wv2 export. Cannot compare Red vs Blue economics or proceed to handoff.

## Scope

1. Run vet detached (multi-hour): `podman exec -d winston_unit_test sh -c 'env PORTFOLIO="Portfolio Red" EXPORT=/portfolio_configs/portfolio-red.json bin/rails portfolios:vet_trend >> /portfolio_configs/portfolio-red-vet.log 2>&1'`
2. Monitor `PortfolioSignalOptimization` progress for portfolio id 6.
3. Export `portfolio_configs/portfolio-red.json` on success.
4. Record winner strategy, return, drawdown, trades in sidecar or session note.

## Acceptance

- Optimization completes 6/6 without stuck `running` state.
- `portfolio_configs/portfolio-red.json` exists with markets matching Red Books.
- Results summarized in plan or follow-on ticket if economics are poor (see trading-strategy evaluation ticket).

## Depends on

- Trading-strategy evaluation framework ticket if Red vet also shows catastrophic losses — may need revised defaults before treating export as Wv2-ready.

## Related

- Plan task #2
- WUT: `lib/tasks/portfolio_trend_vet.rake`, `PortfolioTrendVetter`