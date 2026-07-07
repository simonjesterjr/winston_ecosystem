# Plan: WUT — DM as Source of Truth for Market Data (Parquet Primary, Eliminate Duplication)

**Authoritative location for the plan.** A detailed working copy lived in the Grok session dir during planning (`~/.grok/sessions/.../plan.md`); this is the promoted version in the permanent ecosystem knowledge base.

**Status**: Proposed (plan written + adversary review completed). Adversary verdict: **BROKEN** on implementation details (see below). Goal and direction align with principles; approach requires significant corrections before execution. Tickets filed. Awaiting user approval / revised plan before implementation begins.

**Date**: 2026-07-07

## Context & Goal

WUT (`winston_unit_test/`) currently duplicates DM-managed market data:

- `DataSetDmImporter` reads DM parquet (from shared `/dm_data`) then writes local copies to WUT's `data/price_data/` + `data/calculated/`.
- It then calls `ParquetData::BacktestActivitiesLoader.sync_to_activities!`, which materializes full rows into the `activities` table + `market_indicator_values` (for ATR).
- Buttons on `/wut/data_sets` ("Load Full Data from DM", "Sync", "Update All Data") trigger this path (the label difference is only cosmetic: `needs_full_data = stats[:activity_count].to_i == 0`).
- Many downstream components still assume `market.activities.order(date: :asc).to_a` (backtest runners, portfolio backtests, signal optimization, daily ops, strategies, reports, charts, Position/Journal FKs via `activity_id`, `Market#risk`, `Activity#atr`, expected return calculators, etc.).

This violates the core principles:

- DM owns the time-series (Winston EOD Standard parquet + baked derivatives).
- Consumers (WUT, Wv2) **read** it. PG in consumers holds **metadata only** (`Market`, `DmCoverage`, Portfolios/Books, runs, journals, positions, etc.).
- "No heavy OHLCV or indicator time-series rows in PG tables."

Wv2 already follows the correct model:
- No `Activity` table at all.
- Mounts the same `sawtooth_dm_data` volume as `/dm_data:ro`.
- Uses `DmParquetPaths`, `ParquetLookbackLoader` (DuckDB direct), `ParquetBar` (struct with `.id = nil`).
- `PortfolioReadiness` skips with `missing_data` when `data_ready?` fails.
- Only `DmCoverage` metadata is ingested.

**Goal**: Make WUT match the principles and Wv2. DM parquet (Winston EOD Standard) is the single source of truth. Consumers read via direct loader returning Bar objects keyed by composite `(market_id, date)`. No duplication of bars into WUT local parquets or the `activities` table for DM-sourced data. The `activities` table and `belongs_to :activity` associations are removed/deprecated for DM data (legacy non-DM records are defunct; no curation of historical relationships needed). The data_sets UI is a pure DM registry (no "load into WUT" buttons or language). Backtest result parquets are minimal (P&L, journals, risk snapshots + stable `(market_id, date)` identity per row); any richer bar data (OHLCV + indicators) is re-pulled from the DM loader at render time using the stored keys. If holes exist (missing dates or derived values), WUT calls back to DM. Legacy Yahoo/CSV paths for non-DM data may remain temporarily but are also defunct.

DM owns calculation of all required indicators (ATR-17 and any future ones added to strategies). New indicators become part of the DM responsibility and the parquet standard going forward.

## Core Decisions

- **Storage truth**: The parquet files written by DM (under the shared volume) + DataCoverage metadata in WUT's PG. (Converge on canonical **DataCoverage** term; deprecate DmCoverage naming in consumer code.)
- **No duplication for DM symbols**: Stop `Pipeline.save_price` / `save_calculated` and `sync_to_activities!` entirely for DM-acquired data. `DmParquetIngester` + registry sync are metadata-only. DataSetDmImporter and related become thin request + metadata paths only.
- **Consumption**: Direct DM loader (adapt/port Wv2 `ParquetLookbackLoader` + full-series equivalent using DuckDB on `/dm_data`). Primary objects are Bar/ParquetBar (id = nil) or equivalent. All call sites (runners, daily ops, strategies, risk, charts, expected return, etc.) use composite `(market_id, date)` + loader. `market.activities` and Activity objects are not used for DM-sourced markets.
- **Refactor of creation and usage sites (no shim)**: Remove or fully deprecate `belongs_to :activity` for DM data. Refactor creation sites (Position, TradingSignal, BacktestIndicatorValue, PassedSignal, MarketIndicatorValue, Journal, etc.) and usage sites to carry/use `(market_id, date)` (or non-persisted composite) + Bar from the DM loader. Every result row in backtest parquets must be identifiable by `(market_id, date)` (logical key, concatenated value, or reversible 2-way hash). No transitional stubs or proxies.
- **Backtest results**: Result parquets (`data/backtest/*.parquet`) stay minimal — P&L, journals, positions, risk, notes + stable `(market_id, date)` identity. Rich bar data for visualization is re-pulled from DM loader at render time. If data holes (missing dates or indicators like ATR), call back to DM to fill.
- **UI (data_sets and related)**: Pure DM registry view. Remove hydration buttons/labels entirely ("Request DM refresh" or equivalent for trigger + metadata only). Columns, counts, ranges, freshness from DataCoverage. No language suggesting data is "loaded into WUT".
- **Readiness & skips**: Adopt `missing_data` style checks (like Wv2 `PortfolioReadiness`) before backtests or daily analysis.
- **Legacy non-DM**: All legacy non-DM records (Yahoo/CSV) are defunct. Paths may remain for a short time but receive no special curation of activity relationships.
- **Cross-monolith / indicators**: DM owns calculation of all required indicators (ATR-17 + any added to strategies). New indicators are added to the Winston EOD Standard and become DM's responsibility. Leverage `DataManagerClient#request_download`, registry, volume mounts.

## Adversary Review Outcome

An adversarial subagent was run against the initial plan (per user request "/adversary").

**Verdict: BROKEN** (on the details of the approach, not the goal).

**Major disconfirming evidence** (from direct code reads + greps on schema, runners, services, models, views):
- ~100 direct uses of `Activity.where`, joins on activities, `find_by(date)`, full history queries for BIVs/expected_return/calculators/charts (not just the post-sync `market.activities.to_a`).
- Schema requires real `activity_id` (NOT NULL) for positions, signals, backtest indicator values.
- `Activity#atr` early-returns 0 unless `id.present?`.
- `Market#risk` raises "No Activities loaded".
- Wv2's `ParquetBar` explicitly returns `nil` for id and its models never use activity_id.
- The duplication logic is executed in many places beyond just the importer (runners, optimization context, catalog, universe downloader, rakes, controller actions, views).
- "NO replicate" comment exists **only** in the metadata ingester; the actual running bridge (DataSetDmImporter + sync_to_activities!) does full replication.

**Corrections incorporated**:
- Direct DM loaders first; all consumption (runners, views, calcs) and creation sites refactored to composite `(market_id, date)` + Bar. No thin proxy/shim.
- Full audit and refactor of ~100 Activity usage sites (no preservation of `market.activities` expressions for DM data).
- Result parquets augmented with stable `(market_id, date)` identity per row; render paths re-pull via loader.
- Explicit: no stubs, no transitional materialization of activities for DM. Direct refactor.
- UI, ingestion, and runner changes are full cutover (not compatibility layers).
- Update ACs, phasing, and tickets to reflect "no more transitional". DM owns all indicators.
- Recommend verification pass before implementation.

The plan file in the session dir was updated with these findings. This ecosystem/plans version reflects the reviewed state.

## Phasing (Revised)

1. **Foundation (loaders + identity)**: Add/adapt DM Bar loader (full series + lookback, DuckDB on mounted `/dm_data`). Update BacktestResultsReader/Writer + BACKTEST schema to embed stable `(market_id, date)` identity (logical/concat/hash) per row. Make `sync_to_activities!`, Pipeline saves, and local parquets no-ops for DM symbols. Add DataCoverage-based readiness.
2. **Refactor runners & creation sites**: Update backtest_runner, portfolio_backtest_runner, optimization context, signal/position/journal creation, daily ops to use DM loader + composite keys directly. Produce only minimal result output + identity keys. No Activity rows created for DM data.
3. **Refactor usage sites**: Audit and update all Activity.where, joins, find_by, risk, atr, charts, expected-return calcs, views (result rendering included) to use stored `(market, date)` + DM loader re-pull. Result views treat captured data as sufficient and re-pull for rich bars/holes.
4. **Ingestion & callers cutover**: Thin out DataSetDmImporter, DataSetDmSyncRunner, market_catalog, universe_downloader, correlation_builder, rakes, controllers to request + metadata only (no materialization).
5. **UI overhaul**: data_sets and related become pure DM registry. Remove all hydration buttons/actions/language. Columns/metadata from DataCoverage.
6. **Stats, readiness, daily ops, tests, docs, model changes**: Update models to deprecate/remove activity associations for DM paths; schema work for activity_id columns (eventual removal or nullability for legacy).
7. **Verification**: DM data present, WUT has only metadata + result parquets with identities; no new activity rows or local parquets from DM paths; runners + views work via loader + composites; holes trigger DM fill; legacy paths isolated.

## Key Files (WUT unless noted)

- Models: `market.rb`, `activity.rb`, `dm_coverage.rb` (→ converge on DataCoverage), `position.rb`, `journal.rb`, `backtest_indicator_value.rb`, `market_indicator_value.rb`, `passed_signal.rb`
- Loaders/Services: DM Bar loader (new or extended from Wv2 `parquet_lookback_loader.rb` + full history), `lib/parquet_data/backtest_activities_loader.rb` (legacy path only), `dm_parquet_ingester.rb`, `data_set_dm_importer.rb` (thin to metadata/request), `data_set_dm_sync_runner.rb`
- Result storage: `lib/parquet_data/writers/backtest_writer.rb`, `lib/parquet_data/readers/backtest_results_reader.rb`, schemas.rb (add `(market_id, date)` identity)
- Runners + creation: `backtest_runner.rb`, `portfolio_backtest_runner.rb`, `portfolio_signal_optimization_context.rb`, `position_manager.rb`, `services/expected_return/*`
- Ops: `services/operations/*`
- Controller/Views: `data_sets_controller.rb` + `app/views/data_sets/*`, backtest result views (stop Activity queries for DM runs)
- Stats: `market_activity_stats.rb`, `data_set_freshness.rb`, `MarketDataUpdatePlanner`
- Other: `market_catalog.rb`, `universe_downloader.rb`, `portfolio_correlation_builder.rb`, rakes
- Wv2 reference: `winston_v2/app/services/{dm_parquet_paths.rb,parquet_lookback_loader.rb,parquet_bar.rb,dm_parquet_ingester.rb,operations/portfolio_readiness.rb}`
- DM side: request_consumer_sync, etc.
- Compose + ecosystem docs as before.

## Tickets

Tracking tickets (2026-07-07) updated to reflect final direction (no shims, direct composite + Bar refactor, result identity keys, DM indicator ownership):
- `wut-dm-parquet-source-of-truth-no-duplication.md` (main)
- `wut-dm-data-sets-ui-dm-truth-no-load-sync-buttons.md`
- `wut-activities-compatibility-shim-dm-stubs.md` (rewritten as refactor ticket: remove activity associations, use composite keys + loader for creation/usage + results)

See updated tickets for ACs.

## Verification (High Level)

- DM has parquets + DataCoverage for symbols; WUT has only metadata (DataCoverage), no local price/calculated parquets or activities rows created by DM paths.
- data_sets is pure registry; no hydration buttons.
- Backtests + daily ops + result views succeed using DM loader + `(market_id, date)` composites (correct OHLCV, ATR-17 and other indicators, risk, signals, charts).
- Result parquets contain minimal data + stable `(market_id, date)` identity per row; re-pull for rich visualization works.
- No growth in activity rows or local parquets from DM flows. Holes (if any) cause DM callback.
- `market.activities` / activity_id not used for DM-sourced data.
- Legacy paths isolated and not exercised for DM symbols.
- Specs + smoke tests pass. Manual: full backtest → result view cycle with DM as source.

See the detailed session plan for expanded verification commands and success metrics.

## Open Items / Decisions

- Exact representation for `(market_id, date)` identity in result parquets (add `market_id` column + dates, concatenated string key, or reversible hash) — decide and implement in BACKTEST schema + writer/reader.
- Full audit list of creation + usage sites that still reference activity (models, views, services, jobs).
- How result render paths invoke the DM loader for re-pull (new helper? extend existing lookback/full loader?).
- Handling for holes: on-demand DM request during view vs. pre-ensure before render.
- Convergence on DataCoverage naming (rename DmCoverage model/table/references).
- Loader sharing with Wv2.
- Treatment of FRED/special series (may keep limited local paths).
- Schema changes for activity_id columns (make nullable or drop for DM paths; migration strategy).
- No transitional paths — full cutover for DM symbols.

## Related

- `ecosystem/principles/02_data_storage_and_reconciliation.md`
- `ecosystem/CONTEXT.md` (glossary: Winston EOD Standard, DataCoverage, Reconciliation, Consumer)
- `ecosystem/interfaces/winston-eod-parquet-standard.md`
- `ecosystem/docs/tickets/2026-07-06-dm-wut-registry-metadata-sync-followups.md`
- WUT docs: `parquet_data.md`, `data_reconciliation.md`
- AGENTS.md files (read ecosystem/ first)

This plan supersedes the session copy as the permanent record. Implementation must follow a revised version that addresses the adversary findings.