# Plan: Winston v2 (Wv2) — Initial Rails Monolith Scaffold + Core Domain + Ecosystem Integration

**Status**: In progress. Core scaffold + domain + TradingStrategy loose coupling (updated WUT first-class TS model via JSON + names + rich export methods) + daily/Cromwell stub + explicit DM trigger paths for missing portfolio data (wv2:request_dm_sync + auto-detect in job/rake + symmetric consumer notifies in DM) done. Portfolio config exchange (WUT TS/run export → JSON shared volume → Wv2 import + apply + link), CLI edit (nano), activate/deactivate/evaluate, internal APIs, coverage ingest via DuckDB, capital_base with CashEvents + realized, seeds with linked TS per updated model. See portfolio_configs/README.md, ecosystem/, wv2:* rakes (portfolios + trading_strategies + request_dm), DmParquetIngester#missing/request, updated models for delegation + WUT TS methods, DailyAnalysisJob now triggers DM when data missing. (2026-06-12 updates per user query).

**Original plan date**: 2026 session (see below for the full initial plan).

**Date**: 2026 session

## Context

Winston v2 is the operational/live trading monolith in the Sawtooth "majestic monoliths" ecosystem (see `ecosystem/` for permanent source of truth). 

- WUT (`winston_unit_test/`) is the mature backtesting laboratory (refines trend-following strategies, uses Portfolio/Books/Markets/Journals/Positions + robust risk/entrance/exit strategies, daily ops services, Sidekiq, PassedSignal journaling of skips/fulfillment notes).
- DM (`data_manager/`) owns EODHD acquisition → canonical "Winston EOD Standard" parquet (raw + DM-computed derivatives like atr_17 + MAs) under shared volume + PG metadata/reconciliation + Cromwell notifications.
- `winston/` (v1) is legacy — ignore for modeling/reuse.
- Cromwell (future agentic coordinator) will drive daily flows via APIs/webhooks, aggregate reports/todos, chat (Telegram) with humans (e.g., Alex's weekly management turn), and link to Wv2-generated reports/summaries. Wv2 is explicitly designed as an MCP component with specific inputs/outputs/comms patterns; UIs are governance/config only and secondary to AI/chat interaction.
- The 11-point narrative (Telegram channel at 4pm MT, Cromwell announcing WUT then Wv2 portfolios, outstanding trades, Alex todos, new entrance signals, final reports with last-10 journals + equity graphs + cash/positions/action-items) defines the target interaction surface.

Wv2 reuses WUT's application model and compute (risk mgmt parallels, entrance/exit, pyramiding, journal robustness) but operationalizes for live: real cash (initial + periodic inflows/exits as risk basis), live positions/journals, signal fulfillment notes (LEAPs instead of stock, options strategies), daily analysis producing actionable journal drafts + Cromwell notifications. It shares Redis (Sidekiq), mounts DM parquet volume for data (no time-series duplication in its PG), has its own PG + Sidekiq.

Principles (from `ecosystem/principles/*.md` and DM plan) must be followed: podman-native (root `compose.yml`), parquet as portable standard (DM writer, consumers read via DuckDB/mount or API), reconciliation/ingest metadata only in consumer PG, Sidekiq for work + webhooks/APIs for cross-monolith, WUT as reference for Portfolio/Market/Book/Journal/Position/risk/strategies/ops patterns, update `ecosystem/` on decisions.

**Additional implementation constraint** (user directive): New Ruby classes/scripts ≤65 lines (refactor; exceptions only for docs/migrations/rakes/schemas/READMEs). Plan and all future work must respect this.

This plan scopes the *start* of the workstream: a runnable podmanized Rails monolith with core domain, data integration, daily analysis skeleton, journal/action items, stub Cromwell integration, minimal governance UIs, and compose updates. Full MCP/telegram/Cromwell + advanced reports/graphs come in follow-on slices.

## Recommended Approach (Single Coherent Path)

1. **Standardization & Deployment Foundation (match DM/WUT exactly)**:
   - Ruby 3.3.6, Rails ~7.0.6, pg ~1.1, puma, importmap/turbo/stimulus/tailwind, slim-rails, pry, httparty, technical-analysis (git), async, redis ~5, sidekiq ~7 + sidekiq-cron, duckdb (for parquet reads), parquet (gem).
   - Containerfile: exact pattern from `winston_unit_test/Containerfile` (ruby:3.3.6-slim + system deps + DuckDB C lib install via curl/unzip/ldconfig before bundle + chmod +x bin/ + mkdirs).
   - database.yml: ERB/env-aware like WUT (DB_HOST/DB_NAME/DB_USER/DB_PASSWORD; defaults for local).
   - sidekiq.rb + sidekiq_schedule.yml: identical pattern (cron for daily analysis).
   - config: puma, environments, boot, application matching WUT (pool sizes, etc.).
   - Root compose updates (see Files section): dedicated `wv2_postgres` (postgres:16, port 5434:5432, sawtooth user/db=winston_v2_dev, volume), `winston_v2` service (build context ./winston_v2 + Containerfile, ports 3002:3000, env RAILS_ENV + REDIS + DB_* + DATA_MANAGER_URL=http://data_manager:3000, volumes: sawtooth_dm_data:/dm_data:ro + ./winston_v2:/app bind for dev, depends healthy on redis + wv2_postgres). Follow naming/container_name conventions already in compose.
   - bin/compose already generic (uses container_name); no change or minimal.
   - Update `ecosystem/deployment/README.md` + root compose comments with Wv2 commands (migrate, seed, exec console, etc.). Add Wv2 to eodhd.env notes if relevant (future consumer registration).
   - Add Wv2 as first-class consumer in DM: Wv2 exposes matching internal/active_markets; DM gets `dm:sync_from_wv2` rake (and notify path to Wv2) for full symmetry with WUT. Wv2 calls DM internals (e.g. for required_indicators if useful).

2. **Core Domain Models (WUT as direct reference; live-focused adaptations)**:
   - Reuse shapes from WUT `app/models/` (Portfolio, Book, Market, Journal, Position, PassedSignal, TradingSignal) but own DB so re-implement/adapt (no cross-DB).
   - Key Wv2-specific:
     - `Portfolio`: live trading portfolio (name, active, always_in_market: bool default false, max_positions_per_portfolio:10, max_positions_per_symbol:5). Has many Books, Journals, Positions, CashEvents.
     - `Book`: join Portfolio <-> Market (same as WUT).
     - `Market`: registry (trading_symbol, name, trading_market, tick_*, period). Populated for Wv2's portfolios (via DM active_markets or manual).
     - `CashEvent` (new, core to task reqs): date, amount (decimal), event_type (enum: initial, inflow, exit, adjustment), notes, recurring (bool + interval for $200/wk modeling). Journals/capital_base computation walks CashEvents + realized P&L.
     - `Position`: live (direction, units, execution_price, original/updated_stop, action_description, is_option, option_* fields for LEAP fulfillment, motivating_signal). Status via action_description containing "CLOSED".
     - `Journal` (start from WUT's robust one): portfolio/market/position, trade_date, flow (signed for cash impact), mark_to_market, debit_credit, run_capital (or equiv), notes, position_sizing_risk, position_action_initiation, expected_return_data (jsonb, for future), fulfillment_type (stock|leap|option_strategy|...), fulfillment_details (jsonb). "Passed signals" tracked via separate or embedded.
     - `PassedSignal`: adapt WUT (portfolio, market, activity/date, signal_type, direction, reason — e.g. portfolio_limit/symbol_limit/insufficient_cash/risk_limit). Used for journal + Cromwell reports of "why we didn't act".
   - Config on Portfolio (or dedicated `PortfolioConfig` / embedded jsonb for simplicity at start): risk_percentage (e.g. 0.02), risk_evaluation_strategy ('static'|'martingale'|'one_way_dynamic'|'equity_curve'), atr_multiplier, stop_strategy ('isomorphic'|'move_to_last_entry'|'move_to_stepped_entry'), pyramid_atr_multiplier, max_pyramid (per-symbol), primary_entry_strategy (string/class name or id), confirmational_entry_strategy_ids (array), exit_strategy_ids (array — any triggered exits the position), cashflow_policy (reference to CashEvents).
   - Enums/strings match WUT strategy names exactly for reuse of `StrategyRegistry` + instances.
   - No full backtest_run/ActiveAccount duplication initially (Wv2 is the "live active account").

3. **Data Integration & Compute (Parquet-first, DuckDB, reuse WUT services)**:
   - Mount `/dm_data:ro` (same volume as WUT). No local Activities table replication for price series (PG = metadata/state/journals only, per principles).
   - Adapt `DmParquetIngester` (from WUT `app/services/`) into Wv2 as `DmCoverage` + ingester (or lighter `DataCoverage` model). On boot/after notify, or via rake/job: discover markets for active Wv2 Portfolios, ingest coverage (earliest/latest, bar_count, indicators_present with populated stats) from parquet via DuckDB. Store in Wv2 PG.
   - Daily data needs: query parquet directly (DuckDB) for "activity on date" + lookback + atr_17 (and required MAs per IndicatorRequirements or hardcode initial set from WUT).
   - Adapt WUT `app/services/operations/{DataSync,SignalEvaluation,DailyTasksService,TaskGenerator,ReportBuilder}` + `position_manager.rb`, `portfolio_position_manager.rb`, `pyramid_service.rb`.
   - Copy (into `winston_v2/app/strategies/`) the strategy files needed: `strategy_registry.rb`, `testing_strategy.rb`, `trading_signal_strategy_base.rb`, entry_exit/* (at least breakout_20/55 etc.), exit/* (volatility, others), risk/* (all 4), stops/* (all 3). Register same names.
   - Capital base for risk: initial (from CashEvent) + cumulative realized P&L from closed journals (profits increase base, per WUT PositionManager logic). Inflows/Exits from CashEvents adjust base on/after their date. Support "e.g. start $10k + $200/wk".
   - Entrance: use TestingStrategy (primaries ALL + confirmations ALL). Exits: OR any exit_strategy (per WUT TestingStrategy + ops narrative).
   - Pyramiding: PyramidService + PositionManager logic (ATR multiplier, max, stepped stops).
   - "Always in market", max limits, risk % per trade, ATR mult, stop updates — all config-driven like WUT PortfolioBacktestRun + market configs.
   - Fulfillment: on journal/position create or confirm, allow noting "used LEAPs" or "option strategy X" (stored in journal; no full option chain valuation in v1 slice).

4. **Async, Orchestration, Notifications (Sidekiq + Cromwell hooks)**:
   - Sidekiq + cron schedule (daily at ~6am or market close logic; configurable).
   - `DailyAnalysisJob` (perform(date)): for each active Wv2 Portfolio → run adapted DailyTasksService (sync metadata/ingest if needed, evaluate signals via strategies on DM parquet "today", build reports, generate draft Journals + OperationsTask-like "action items").
   - Idempotent per (portfolio, date).
   - `CromwellNotifier` service (class methods or job): POST structured JSON to Cromwell webhook (stub: write file under storage/ + log + console for now, like DM's stub; include portfolio name, outstanding trades confirmations (pyramid #N at price, stopped at $x), new entrance signals (first for JKL), action items, summary cash/positions, links or embedded last-10 journals + equity series data for graphs). Payload shape to be documented in `ecosystem/interfaces/` on first cut.
   - Internal APIs (namespace or /internal): 
     - GET /internal/active_markets (for DM discovery of Wv2's needed symbols).
     - POST /internal/dm/data_ready (trigger ingest for symbols; like WUT).
     - Future: Cromwell-facing /api/v1/triggers/analyze_portfolios, /status, action confirmation endpoints (POST to mark journal "executed" + notes from chat).
   - Routes + controllers for above (skip CSRF for internal).
   - On complete: CromwellNotifier fires with the narrative elements (2 active portfolios, markets updated, outstanding trades, analysis complete + follow-on actions, final report link/summary).

5. **Governance UIs (Secondary, Minimal but Functional)**:
   - Resources: portfolios (index/new/edit with nested cash_events, strategy selects, limits, entrance/exit config forms — simple selects + multi for confirms/exits).
   - Journals (index with filters by portfolio/date/type, show fulfillment notes).
   - Current positions / open equity view.
   - Operations-like dashboard (inspired by WUT `operations/home`): pending action items (from draft journals/tasks), latest reports per portfolio, "run analysis now" button (enqueues job).
   - Use ERB or slim (WUT uses ERB for complex ops; DM uses slim). Tailwind for quick forms.
   - No heavy JS; keep simple. Reports can render basic tables + data for future graphs (JSON endpoint for equity series).

6. **Scaffolding, Seeding, Tooling**:
   - Since `winston_v2/` exists empty: bootstrap by placing a complete Gemfile + Containerfile first, then `./bin/compose build winston_v2`, followed by iterative `bin/rails` inside the running container (or use `podman compose run --rm` for one-offs) to generate the rest of the Rails skeleton (`rails new . --force --skip` variants are risky in place; prefer manual + rails generators inside container for app/, config/, etc.). Copy/adapt files from WUT/DM into the mounted source.
   - Preferred practical: minimal files → build → exec container to `bin/rails db:....`, `rails g model ...`, edit, repeat. Bundle happens in image build.
   - Initial migration(s): create core tables (markets, portfolios, books, cash_events, positions, journals, passed_signals, dm_coverages or equivalent, operations_tasks or action_items).
   - Seeds: 1-2 sample live portfolios (e.g. "Trading Portfolio A" with $10k initial + weekly inflow CashEvent, static risk, breakout entry + confirm, volatility+atr exits, limits 10/5, 2-3 markets/books; "B" with different risk/always_in). Seeds should reference symbols that will have DM parquet data.
   - Rake (Wv2 side): `wv2:sync_markets` (or equivalent from DM), `wv2:ingest_dm`, `wv2:daily_analysis[date]`, `wv2:reconcile`.
   - Rake (DM side): new `dm:sync_from_wv2` (see DM modifications above).
   - lib/tasks, app/jobs/application_job, services base.
   - Update WUT/DM? Required for symmetry: 
  - Wv2 exposes `/internal/active_markets` (plan already includes).
  - Add `dm:sync_from_wv2` rake in data_manager (modeled 1:1 on existing `dm:sync_from_wut` / `lib/tasks/test_data.rake` or data_acquisition flow): it calls Wv2's internal endpoint to discover symbols, acquires the 3y+latest + derivatives, writes Winston-standard parquet, notifies Wv2 (data_ready), etc. Keep the WUT one working unchanged.
  - Optional polish (during impl): generalize the sync rake to a single `dm:sync_from_consumers` that hits both (or a small consumer registry) so one command covers the ecosystem. Document in the rake and ecosystem/deployment.
   - Update `ecosystem/`: 
     - Copy this plan (with any final session comments/notes) verbatim or lightly edited into `ecosystem/plans/winston-v2-initial.md` as the authoritative permanent record (matching how the DM plan lives there).
     - Add any new interface contracts (Cromwell Wv2 notification shape, Wv2 <-> DM); note decisions (e.g. cash events model, direct DuckDB for live vs WUT activities, 65-line rule application).
     - Update principles if material new invariants arise.

7. **Trade-offs & Scope Boundaries**:
   - Reuse WUT strategies/position logic by copy (monoliths independent; later possible shared gem or mount if elegant). Avoid shared code paths that couple deploys.
   - **Code length rule (ecosystem-wide for new Ruby)**: New classes and scripts must stay ≤65 lines unless absolutely necessary (refactor toward small, focused objects; obvious exceptions = docs, READMEs, schema.rb, migrations, rake tasks). When adapting long WUT files (e.g. position_manager.rb), split during the Wv2 port.
   - Parquet queries for eval (performant in podman) vs. loading local table: direct query wins for "no duplication" + simplicity in live (WUT keeps activities for backtest history).
   - Full equity graph generation + report PDF/links: stub data + JSON in first cut; visual in next.
   - Real Cromwell webhook + MCP tool defs: prepare endpoints/payloads + notifier; actual Cromwell + Telegram in parallel/future stream.
   - Cash inflows: model as dated events (supports retro + scheduled); risk calc uses time-aware capital base (sum events up to date + realized journals).
   - Start without full paper trading or LEAP valuation (notes only for journal; WUT has the services if needed later).
   - No auth on internal for compose net (same as current DM/WUT).

## Critical Files to Create/Modify

**New (winston_v2/ tree)**:
- `Gemfile` + `Gemfile.lock` (after bundle)
- `Containerfile`
- `config/database.yml`, `config/initializers/sidekiq.rb`, `config/sidekiq_schedule.yml`, `config/routes.rb`, `config/puma.rb`, `config/application.rb` etc. (standard + env)
- `db/migrate/XXXXXXXX_create_initial_wv2_tables.rb` (or split: markets/portfolios/books/journals/positions/cash_events/passed_signals/dm_coverages)
- `db/schema.rb`, `db/seeds.rb` (samples)
- `app/models/` : application_record, market.rb, portfolio.rb, book.rb, cash_event.rb, position.rb, journal.rb, passed_signal.rb, dm_coverage.rb (or data_coverage), operations_task.rb (or action_item)
- `app/services/` : dm_parquet_ingester.rb (or data_ingester), cash_base_calculator.rb, operations/ (daily_tasks_service.rb, signal_evaluation.rb, task_generator.rb, report_builder.rb), position_manager.rb, pyramid_service.rb, cromwell_notifier.rb, portfolio_position_manager.rb (adapted)
- `app/strategies/` (full subtree copied/adapted + registry + testing + base)
- `app/jobs/` : application_job.rb, daily_analysis_job.rb
- `app/controllers/` : application_controller.rb, portfolios_controller.rb, journals_controller.rb, operations/home_controller.rb + reports/tasks (minimal), internal_controller.rb, api/v1/ (triggers, status, actions)
- `app/views/` (minimal ERB/slim for governance + ops dashboard)
- `lib/tasks/wv2.rake` (or data.rake)
- `Rakefile`, `README.md` (ecosystem notes), `bin/rails` etc. (standard)

**Modify (ecosystem-wide)**:
- `compose.yml` (add wv2_postgres + winston_v2 services + volumes + comments)
- `ecosystem/principles/*.md` (if new invariants, e.g. cash events as first-class for risk)
- `ecosystem/plans/` : add `winston-v2-initial.md` (promote this or detailed session version)
- `ecosystem/interfaces/` : add `winston-v2-cromwell-notification.md` (payload examples matching narrative) + update parquet if needed
- `ecosystem/deployment/README.md` (Wv2 commands, env)
- `data_manager/` (add `dm:sync_from_wv2` rake + small supporting changes in acquisition/notify flow for Wv2 parity with WUT; Wv2 becomes a first-class discoverable consumer)
- `winston_unit_test/` (none required for this slice; WUT remains reference)

**Reuse (read/copy patterns, exact paths)**:
- WUT models: `winston_unit_test/app/models/{portfolio.rb, journal.rb, activity.rb (for to_analysis_hash/atr), book.rb, market.rb, position.rb, passed_signal.rb, active_account.rb (for max limits), portfolio_backtest_run.rb (for can_add + limits logic)}`
- WUT strategies: `winston_unit_test/app/strategies/{strategy_registry.rb, testing_strategy.rb, trading_signal_strategy_base.rb, risk/*.rb (all), stops/*.rb (all), entry_exit/breakout_*.rb + others as needed, exit/*.rb}`
- WUT services: `winston_unit_test/app/services/{pyramid_service.rb, position_manager.rb, portfolio_position_manager.rb, operations/{daily_tasks_service.rb, data_sync.rb, signal_evaluation.rb, task_generator.rb, report_builder.rb}}`, `dm_parquet_ingester.rb`, `indicator_requirements.rb` (for required columns/atr_17 etc. when Wv2 queries parquet)
- WUT jobs: `winston_unit_test/app/jobs/daily_operations_job.rb`
- WUT controllers/ops: `winston_unit_test/app/controllers/internal_controller.rb`, `app/controllers/operations/home_controller.rb` (and reports/tasks)
- WUT config: `winston_unit_test/config/{database.yml, initializers/sidekiq.rb, sidekiq_schedule.yml, routes.rb (internal + operations parts)}`
- WUT Containerfile + data patterns.
- DM: `data_manager/Containerfile`, `config/database.yml`, `config/initializers/sidekiq.rb`, `app/services/data_acquisition_service.rb` (notify pattern), `app/controllers/internal*` (no, the WUT side), routes for internal + triggers + status, models/download_run etc for status patterns.
- Root: `compose.yml` (service + volume + depends + env patterns), `bin/compose`
- ecosystem/ all of it (read first, update on decisions).

## Verification (End-to-End)

1. From sawtooth root (clean state):
   - `./bin/compose build data_manager winston_unit_test winston_v2` (or selective).
   - `./bin/compose up -d` (ensure DM/WUT running for data; create eodhd.env if needed).
   - `./bin/compose exec -T winston_v2 bin/rails db:create db:migrate RAILS_ENV=development`
   - `./bin/compose exec -T winston_v2 bin/rails db:seed`
   - Verify containers: podman ps shows winston_v2, wv2_postgres healthy, port 3002 mapped, /dm_data inside.

2. Prereq for data: ensure DM has parquet for seed symbols (e.g. run DM rake `dm:sync_from_wut` or test downloads for AAPL/IBM etc. via its endpoints while DM container is up). Inside or via exec: rails c → Portfolio.create!(name: "Trading Portfolio A", ...); add CashEvent initial 10000; add Books/markets (use symbols that have DM parquet); inspect CashEvent impact on base.

3. Trigger analysis:
   - `./bin/compose exec -T winston_v2 bin/rails runner "DailyAnalysisJob.perform_now(Date.current)"` (or rake).
   - Or enqueue via sidekiq.
   - Logs show: markets updated (ingest coverage), evaluation (using strategies on parquet data), journals created (drafts for entries/exits/pyramids), passed_signals, capital calc with cash events, "Cromwell" stub notification written/logged with narrative elements (portfolios, outstanding, new signals, summary).

4. Governance:
   - http://localhost:3002 (root → ops dashboard or portfolios).
   - View/edit portfolio config (cash events table renders), journals list shows fulfillment notes + passed reasons.
   - "Run daily" button works.

5. Data fidelity:
   - No price bars in wv2 PG (only coverage + state).
   - DuckDB queries inside container succeed against /dm_data (confirm atr_17 etc. present from prior DM run).
   - Cash example: $10k initial + simulated weekly inflow → risk sizing uses updated base; journals reflect flows.

6. Integration:
   - Wv2 internal/active_markets returns its portfolio symbols.
   - DM rake `dm:sync_from_wv2` (or generalized) discovers from Wv2 and populates parquet for Wv2's markets (symmetric to existing sync_from_wut).
   - (If DM running) DM notifies Wv2 via data_ready (or the new sync task does); Wv2 ingests coverage.
   - Sidekiq UI or logs confirm cron/job (if sidekiq running in container).
   - Restart stack, re-migrate, re-seed, re-run — idempotent.

7. Narrative simulation (manual steps 1-11):
   - Pretend Cromwell trigger → job runs → produces the exact outputs described (2 portfolios, outstanding trades confirm msg, Alex todo via "notification", new entrance for JKL, final report payload with last-10 journals per portfolio + summary cash/positions/actions + equity data).
   - Manual journal update (as if Alex replied) → status executed, capital adjusted.

8. Ecosystem:
   - `cat ecosystem/principles/*.md ...` still accurate.
   - New plan + interface docs present in ecosystem/.
   - `podman compose ps` clean names; no breakage to DM/WUT services.

9. (Stretch) Basic specs in `spec/` for CashEvent capital calc + SignalEvaluation produce expected signals from sample parquet rows.

Success = runnable monolith in the compose stack, core portfolio/risk/journal/cash functionality works, daily flow produces Cromwell-ready artifacts matching the provided narrative, follows all principles (incl. 65-line rule for new .rb files), WUT code reused/adapted (not reinvented; split where we touch long files), plan promoted to `ecosystem/plans/`, ready for MCP layer + Cromwell.

## Open Decisions / Follow-ups (for later slices or clarification)

- Exact initial set of required indicators for Wv2 eval (pull live from WUT IndicatorRequirements during impl).
- Precise Cromwell notification payload schema (document in interfaces/ during first notifier cut).
- Whether to introduce a thin "LiveRun" or "TradingSession" model (per date/portfolio) vs. purely date-scoped journals/positions.
- CashEvent recurrence expansion (job that materializes future events? or compute on-the-fly in base calc).
- Full report generation (graphs via view component or separate service; equity curve from journals + mtm).
- Auth for cross-monolith (tokens in ecosystem/deployment/ for prod-like).
- Option/LEAP fulfillment depth (notes sufficient for v1; full services copy from WUT later).
- MCP server exposure (tools for "list_portfolios", "get_pending_actions", "confirm_journal" — after Rails endpoints stable).

This plan is concrete, references exact reuse locations, scopes MVP to unblock the workstream while preserving long-term architecture. Execute slice-by-slice (scaffold/deploy first, then models+data, services+job, notifier+UI, docs/verification).

(End of plan)
