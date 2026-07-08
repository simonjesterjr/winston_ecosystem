---
Status: Proposed
---

# Ticket: Run full E2E smoke for DM reconcile + PBR after source-of-truth cutover

**Related to:** ecosystem/docs/session-reports/2026-07-08-1430-dm-reconcile-container-cleanup.md

## Context
The core WUT DM-parquet source-of-truth work is marked complete, but the plan closeout and the dedicated E2E smoke ticket call for a documented manual end-to-end smoke:

- Fresh DM-only PortfolioBacktestRun on a DM-covered symbol
- `data:reconcile` run
- Reconcile updates DataCoverage correctly
- Backtest + portfolio backtest execute with DM loader (no activities/MIV growth)
- Result views (positions table, candlestick, etc.) render using bar_date + DmParquetLoader re-pull
- Original reported crash (portfolio_backtest_runs/25 style) does not recur

## Acceptance Criteria
- [ ] Bring up clean stack (`bin/compose up -d`)
- [ ] `bin/compose build data_manager` (or bind-mount dev)
- [ ] `bin/rails data:reconcile` (or symbol) succeeds with 0 errors on target symbols
- [ ] Create a new DM-only PBR (no legacy activities)
- [ ] Execute backtest + portfolio backtest
- [ ] Verify:
  - No new rows in `activities` or `market_indicator_values` for DM symbols
  - `bar_date` + `market_id` populated on Position/Journal
  - Views use `DmParquetLoader` / `BacktestResultsReader.load_bars...`
  - PBR/25-style page renders cleanly
- [ ] Document the exact commands + observed counts/deltas in the e2e-smoke ticket
- [ ] Update plan closeout if any gaps found

## Links
- Plan closeout: `ecosystem/plans/wut-dm-parquet-source-of-truth.md`
- Existing smoke ticket: `2026-07-08-wut-dm-parquet-e2e-smoke.md`
- Session report: `ecosystem/docs/session-reports/2026-07-08-1430-dm-reconcile-container-cleanup.md`
- ReconciliationService: `data_manager/app/services/reconciliation_service.rb`
- Rake: `data_manager/lib/tasks/data.rake`

**Owner:** human  
**Due:** soon (before moving to portfolio-overlap work)