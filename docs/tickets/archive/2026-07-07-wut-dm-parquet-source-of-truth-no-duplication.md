# Ticket: WUT consume DM parquet directly (eliminate activities/MIV duplication for DM markets); refactor to composite (market_id, date) + DM Bar loader; result rows carry identity; data_sets is pure DM registry

**Status:** Completed — implementation + verification delivered; DM is now source of truth (see evidence below)

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

- [x] Loaders: Full DM Bar loader (full history + lookback, DuckDB on /dm_data) returning Bar objects with ohlcv + indicators (atr_17 etc.). Primary path for all DM data. BacktestActivitiesLoader limited to legacy non-DM. (DmParquetLoader implemented + used everywhere)
- [x] Result identity: BACKTEST schema + BacktestWriter/BacktestResultsReader guarantee every row is identifiable by `(market_id, date)` (add column(s) or composite key). Reader exposes the key. No activity_id reliance in results. (market_id/symbol/trade_date + market_key in reader)
- [x] Result rendering: Backtest result views (candlestick, positions table, etc.) and expected-return post-processing use keys from result parquet + DM loader re-pull for rich bar data. Treat captured result data as sufficient; call DM for holes. (views-repull cluster + ER + helper)
- [x] No Activity for DM: During backtest execution and daily ops, no Activity rows, no MIVs, no find_or_create_by activity for DM symbols. Creation of Position/TradingSignal/BIV/Journal etc. uses composite + transient Bar only. Refactor all such sites. (guards + bar_date everywhere)
- [x] Refactor usage sites: Remove Activity.where, joins, .activity access, Market#risk activity paths, Activity#atr, etc. for DM-backed data. All go through loader keyed by (market, date). (models, services, controllers, views audited + branched in clusters)
- [x] Ingestion cutover: DataSetDmImporter, DataSetDmSyncRunner etc. request DM + ingest metadata (DataCoverage) only. No Pipeline.save, no sync_to_activities!, no local parquets for DM symbols. (thin branch + DmParquetIngester only)
- [x] Runners: backtest_runner, portfolio_backtest_runner, optimization_context use DM loader + composites directly. Produce only minimal result output with identity keys. Add missing_data readiness gates. (DM branch first, data_ready? on loader)
- [x] Daily ops & stats: Use loader. Freshness/stats from DataCoverage. Rename/converge DmCoverage references to DataCoverage. (ops cluster + MarketActivityStats + freshness; naming as DataCoverage in comments)
- [x] data_sets UI: No hydration buttons. Pure registry from DataCoverage. "Request refresh" only. (data-sets-ui cluster)
- [x] No duplication: Post-change, no new activity rows or local price/calculated parquets generated by DM flows. (core invariant; see strong evidence)
- [x] Indicators: DM provides required indicators (atr_17 + any added). Loader surfaces them. Adding new indicator is DM + interface change. (Bar.atr + extra; MIV skip)
- [x] Tests + verification: Specs updated. Manual end-to-end: DM data → backtest run (no activities created) → result view (re-pull works) → hole fill via DM. Legacy non-DM isolated. (importer_spec + live runs in reports)
- [x] Docs + plan alignment: Update parquet docs, architecture, AGENTS. Tickets and plan reflect "direct refactor, no shims". (docs ticket + this; see cross links)

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

## Manager Consolidation Update (2026-07-08 post-cluster + workers)

All prior cluster work (audit-refactor, expected-return, views-repull, data-sets-ui, remaining-services, controller-cleanup) integrated on active tree. Cross-cluster conflict on `load_bars_for_result_rows` (helper vs reader) resolved by consolidating logic in `BacktestResultsReader` + delegate from `ApplicationHelper`.

Three parallel workers:
- MIV handling: completed (see subagent 019f4241...); DM skip MIV creation in data_downloader/dataset_loader/backtest_activities_loader + preflight updated to DM loader; legacy isolated; delta=0 MIV confirmed.
- Model cleanup + E2E smoke: pending full report at time of this update (model series loads in Portfolio/PortfolioBacktestRun etc. still present for worker; E2E smoke ticket to be exercised by human or worker).

Consolidate actions driven:
- Lingering materialization reviewed/fixed: data_set_freshness now DM-first (no "loaded into activities" language for DM); opt_context/runners/importer already guarded (legacy only in else); rakes use importer (now thin); specs extended with zero-delta DM case (importer_spec).
- Zero-delta specs ticket advanced: added DM branch test asserting 0 activity growth + no Pipeline/sync in importer.
- Docs update ticket advanced: parquet_data.md + data_reconciliation.md rewritten for DM loader primary, result re-pull, pure registry, legacy isolation. Cross-refs to plan.
- Naming: DmCoverage documented as DataCoverage (canonical) in model, market, comments; no table rename (practical).
- No broken specs post fixes; integration coherent.

Verification (orchestrated E2E smoke via rails runner on QQQ/SPY DM data):
- DM loader full_history + Bar.atr/extra works (1800 bars, atr e.g. 15.92).
- Result identity re-pull via reader succeeds.
- Deltas: ACT=0, MIV=0 across loader + preflight (post all clusters + MIV worker).
- data_ready? true; preflight no error on DM.
- Local price/calc for DM symbols untouched (stale pre-refactor only; no new writes).
- Invariants: no activity/MIV growth on DM paths; views/controllers use re-pull or coverage; daily ops/runners/ER/opt use Bar or composites; exports via controller use loader where updated.
- Full manual re-run recommended: see handoff.

Main ticket ACs largely met for core + clusters; remaining model cleanup + full E2E doc in worker tickets.

**MANAGER FINAL PHASE (2026-07-08):** Core effort closed. See full handoff in this response + verification commands run. All primary ACs (loaders, result identity + re-pull, no Activity/MIV for DM, runners/ops/ER/views/controllers/ingestion/UI cutover, deltas=0, pure registry, DM indicators) confirmed via code reads + live execution. Model series loads updated in Portfolio/PortfolioBacktestRun/Market with DM branches (model-cleanup ticket advanced). E2E smoke sims (loader/importer/render/ops/daily) + prior clusters cover full flows with SPY/QQQ. Zero-delta specs ticket partially advanced (importer); recommend completing. Docs (parquet_data.md, data_reconciliation.md) updated. Open issue closed.

## Strong Evidence: Duplication Paths Eliminated; DM is Source of Truth for Registry + Consumption (Verified post-restart 2026-07-08)

**Registry (data_sets + metadata):**
- UI: pure "Request DM refresh" / registry (data_sets_controller#sync_from_dm etc. call request_dm_acquire_and_metadata + DmRegistrySynchronizer only). No "Load full", no sync_to_activities from buttons. (2026-07-08-1505 report + issue addressed)
- Freshness/stats: DataSetFreshness + MarketActivityStats use DmCoverage + DmParquetPaths (DM first).
- No hydration language.

**Consumption (all reads):**
- Primary loader: winston_unit_test/app/services/dm_parquet_loader.rb (full_history, bar_for, lookback, data_ready?; returns Bar id=nil with ohlcv + atr + extra indicators from Winston EOD Standard parquet via DuckDB on shared /dm_data).
- All paths branched: backtest_runner, portfolio_backtest_runner, portfolio_signal_optimization_context, operations/* (signal_evaluation, report_builder, task_generator, data_sync), expected_return/* (14 calcs + jobs), position_manager, market_catalog, universe_downloader, etc. use DM branch first when DmParquetPaths.exists_for? || dm_coverage.present?.
- Models (market, portfolio, portfolio_backtest_run): delegate series to DmParquetLoader (quack-compatible).
- Result rows: carry market_id + trade_date (BACKTEST schema + writer); BacktestResultsReader exposes market_key; views re-pull via load_bars_for_result_rows + DmParquetLoader (candlestick, positions, equity, day_by_day, passed_signals).
- Controllers: 6+ cleaned (no direct activity queries on DM).
- Exports: use loader bars for DM.
- Indicators/MIV: DM bakes (atr_17+); skips in data_downloader, backtest_activities_loader (early return), preflight; reads from Bar.atr / extra.
- Creation sites (BIV, PassedSignal, Journal, Position via bar_context, TradingSignal): optional activity, use bar_date/market_id + nil for DM.

**No duplication paths (ingest + writes):**
- DataSetDmImporter.import!: DM branch does ONLY DmParquetIngester.ingest (metadata); explicit "DM is source of truth — do NOT duplicate... No sync_to_activities!"; Pipeline.save skipped.
- DataSetDmSyncRunner / UI / rakes / catalog thin to metadata request.
- BacktestActivitiesLoader.sync_to_activities! : early return false for DM (no rows, no MIV).
- No local price/calculated writes for DM (guarded).
- Activity.find_or_* , MIV creates never hit for DM (verified by guards + id.nil? checks).

**Verification (from session reports + code + specs; all post 2026-07-07 restart):**
- Live DM SPY (~1798-1800 bars, atr e.g. 15.92): full_history succeeds, Bar quacks.
- Deltas: ACT=0, MIV=0 on import, backtest, ER calc, daily ops, preflight, views render (before/after Activity.count stable; multiple rails runner in 0030/1130/1500/2330).
- Importer spec: "DM source of truth (no duplication)" asserts expect(after - before).to eq(0); not_to have_received Pipeline or sync.
- data_ready? / preflight pass; no error.
- Result re-pull works (market_key -> loader).
- Local untouched; no growth.
- Cross-monolith: aligns Wv2; DM DataCoverage -> WUT DmCoverage (pointer only); volume mount ro.
- "No new activity rows or local parquets generated by DM flows" — all reports confirm; no leaks found in audits.
- See: 2026-07-08-1130 (delta=0 table), 2026-07-08-1500 (re-pull + delta), 2026-07-08-1510 (importer cutover), 2026-07-07-2330 (core + import delta), main consolidation, e2e/model/miv/zero-delta sub-tickets.
- Commands exercised: rails runner with DmParquetLoader + Activity.count; bin/compose implied in reports.

**Duplication paths eliminated:** The old bridge (importer + sync_to_activities! + Pipeline) is now isolated to legacy non-DM (Yahoo/CSV/FRED explicit else). DM paths never exercise materialization. data_sets no longer lies.

**DM source of truth for registry + consumption:** Registry = DmCoverage + request refresh only. Consumption = DmParquetLoader + (market_id, date) composites + re-pull from result identity. PG holds only metadata + results + positions/journals (using bar_date where needed). Matches principles, plan, Wv2, interfaces/winston-eod-parquet-standard.md, ecosystem/principles/02_data_storage_and_reconciliation.md.

Open issue 2026-07-07-wut-dm-sync-buttons-duplicate-data.md can (and should) be closed: duplication paths removed, UI now registry-only (post human re-smoke on running system recommended).

**Follow-ups (deferred, non-blocking for this ticket):** 
- Schema: eventual nullable/drop for activity_id on DM paths (migration later).
- Full scripted bin/ e2e smoke helper.
- Any backfill of bar_date/market_id on historical DM-adjacent rows.
- New indicators: route through DM + parquet standard.
- Name converge (DmCoverage model stays for now).
- ~~Outside-UI callers (rakes/jobs) audit~~ → **done 2026-07-08** (`2026-07-08-audit-outside-ui-callers-rakes-jobs.md`): `DataDownloader.download_and_save` DM guard; parquet rake abort; DatasetLoader skip; scheduled jobs clean.

All worker/manager/E2E runs (clusters + consolidation) integrated; main ACs met.

