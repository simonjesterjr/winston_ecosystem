# Ticket: WUT consume DM parquet directly (eliminate activities/MIV duplication for DM markets); refactor to composite (market_id, date) + DM Bar loader; result rows carry identity; data_sets is pure DM registry

**Status:** Proposed — plan written; awaiting adversary verification + approval before implementation

**Date:** 2026-07-07

**Context:** Follow-up to DM registry metadata sync work and explicit user requirement that WUT align with Wv2 and ecosystem principles: DM is the single manager and source of truth for time-series data (Winston EOD Standard parquet on shared volume). WUT must stop duplicating bars into local parquets + `activities` + `MarketIndicatorValue`.

The previous bridge (DataSetDmImporter + sync_to_activities! + local writes) created duplication and tied everything to activity_id. All paths now refactored to direct DM loader + composite keys. No preservation of old expressions for DM data.

Wv2 already does this cleanly: no Activity table, direct DuckDB via ParquetLookbackLoader/ParquetBar on /dm_data, missing_data skips in PortfolioReadiness, DmCoverage as metadata pointer only.

User at /wut/data_sets sees "Load Full Data from DM" / "Sync" buttons (cosmetic; same code path) that trigger duplication. Columns/stats mix local vs DM.

See:
- Plan: `ecosystem/plans/wut-dm-parquet-source-of-truth.md` (authoritative; detailed working copy was in the Grok session dir during planning)
- Wv2 pattern: winston_v2/app/services/{parquet_lookback_loader.rb,parquet_bar.rb,dm_parquet_paths.rb,dm_parquet_ingester.rb,operations/portfolio_readiness.rb}
- WUT duplication: winston_unit_test/app/services/{data_set_dm_importer.rb,data_set_dm_sync_runner.rb}, lib/parquet_data/backtest_activities_loader.rb (sync_to_activities!), runners, data_sets_controller + views, MarketActivityStats, etc.
- Principles: ecosystem/principles/02_data_storage_and_reconciliation.md ("No heavy OHLCV... in PG tables"), CONTEXT.md, interfaces/winston-eod-parquet-standard.md
- Related: ecosystem/docs/tickets/2026-07-06-dm-wut-registry-metadata-sync-followups.md
- Plan: ecosystem/plans/wut-dm-parquet-source-of-truth.md (now authoritative for no-shim, composite+Bar, result identity, direct runner refactor)

## Problem

- Data duplication violates architecture (DM owns, consumers read).
- "Load full / Sync" UX lies about "loading into WUT" while principles say DM manages.
- Backtests/daily ops / paper still rely on `market.activities` (AR queries + objects with .id for FKs in Position/Journal/TradingSignal) and Activity#atr (via MIV).
- WUT data_sets + freshness + stats show local view instead of DM metadata as pointer.
- Two copies (DM parquet + WUT local + PG rows) for same bars; maintenance, drift, storage, inconsistency risk.
- Daily ops (Operations::*) and some portfolio code not yet on DM path.

## Goal

- DM parquet (Winston EOD Standard) + DataCoverage are the sole source of truth. WUT reads via direct loader (Bar objects) using composite `(market_id, date)` keys. No duplication into local parquets or `activities` table for DM data.
- `belongs_to :activity` and `market.activities` are removed/deprecated for DM-sourced data. All creation sites (Positions, signals, BIVs, journals...) and usage sites refactored to composite key + DM Bar loader. Legacy non-DM records are defunct; no curation of the association.
- Backtest result parquets are minimal (P&L/risk/journal data + stable `(market_id, date)` identity per row — logical key, concat, or reversible hash). Rich bar data (full OHLCV + indicators) for views is re-pulled from DM loader at render time using the keys. DM callback for holes (missing dates or derived values such as ATRs).
- DM owns all required indicators (ATR-17 + future ones). New indicators are DM responsibility + added to the parquet standard.
- data_sets UI is a pure DM registry view (DataCoverage as truth). No hydration/"load into WUT" buttons or language.
- Runners and daily ops use DM loader + composites directly during execution. No Activity rows or local parquets created for DM symbols.
- Implementation follows the authoritative plan in `ecosystem/plans/wut-dm-parquet-source-of-truth.md`. No transitional shims.

## Acceptance Criteria

- [ ] Loaders: Full DM Bar loader (full history + lookback, DuckDB on /dm_data) returning Bar objects with ohlcv + indicators (atr_17 etc.). Primary path for all DM data. BacktestActivitiesLoader limited to legacy non-DM.
- [ ] Result identity: BACKTEST schema + BacktestWriter/BacktestResultsReader guarantee every row is identifiable by `(market_id, date)` (add column(s) or composite key). Reader exposes the key. No activity_id reliance in results.
- [ ] Result rendering: Backtest result views (candlestick, positions table, etc.) and expected-return post-processing use keys from result parquet + DM loader re-pull for rich bar data. Treat captured result data as sufficient; call DM for holes.
- [ ] No Activity for DM: During backtest execution and daily ops, no Activity rows, no MIVs, no find_or_create_by activity for DM symbols. Creation of Position/TradingSignal/BIV/Journal etc. uses composite + transient Bar only. Refactor all such sites.
- [ ] Refactor usage sites: Remove Activity.where, joins, .activity access, Market#risk activity paths, Activity#atr, etc. for DM-backed data. All go through loader keyed by (market, date).
- [ ] Ingestion cutover: DataSetDmImporter, DataSetDmSyncRunner etc. request DM + ingest metadata (DataCoverage) only. No Pipeline.save, no sync_to_activities!, no local parquets for DM symbols.
- [ ] Runners: backtest_runner, portfolio_backtest_runner, optimization_context use DM loader + composites directly. Produce only minimal result output with identity keys. Add missing_data readiness gates.
- [ ] Daily ops & stats: Use loader. Freshness/stats from DataCoverage. Rename/converge DmCoverage references to DataCoverage.
- [ ] data_sets UI: No hydration buttons. Pure registry from DataCoverage. "Request refresh" only.
- [ ] No duplication: Post-change, no new activity rows or local price/calculated parquets generated by DM flows.
- [ ] Indicators: DM provides required indicators (atr_17 + any added). Loader surfaces them. Adding new indicator is DM + interface change.
- [ ] Tests + verification: Specs updated. Manual end-to-end: DM data → backtest run (no activities created) → result view (re-pull works) → hole fill via DM. Legacy non-DM isolated.
- [ ] Docs + plan alignment: Update parquet docs, architecture, AGENTS. Tickets and plan reflect "direct refactor, no shims".

## Related

- Plan file (detailed files, reuse list, verification commands)
- 2026-07-06-dm-wut-registry-metadata-sync-followups.md
- ecosystem/principles/02_*.md , CONTEXT.md , interfaces/winston-eod-parquet-standard.md
- Wv2 implementation (reference)
- WUT: DmParquetIngester (the "do NOT replicate" comment), internal data_ready, DmRegistrySynchronizer
- Models: Activity (FKs, atr via MIV), Market (has_many activities, risk), DmCoverage, Position, Journal
- Call sites: backtest_*, portfolio_*_runner, signal_optimization_context, operations/*, strategies/* (consume arrays), data_sets views/controller, MarketActivityStats, etc.
- compose.yml (sawtooth_dm_data mount :ro for WUT)

## Suggested Commands / Next (after approval)

```bash
# Explore / verify current state
bin/compose up -d
bin/compose exec winston_unit_test bin/rails runner "puts Market.find_by(trading_symbol:'SPY')&.activities&.count; puts Market.find_by(trading_symbol:'SPY')&.dm_coverage&.attributes"
bin/compose exec winston_unit_test bin/rails dm:sync_dm_registry
# After changes
bin/compose exec winston_unit_test bin/rails dm:sync_dm_registry
# Test backtest + daily for DM symbol
# Check no duplication post-run
```

See full plan for phased steps, exact files, reused code.

**Do not implement until plan + adversary + tickets verified and user says proceed.**
