# Winston Ecosystem — Domain Glossary

Canonical terms for the sawtooth Winston trading ecosystem. Glossary only — no implementation details. For architecture decisions see `docs/adr/`; for domain rules see `docs/business-context/`.

## Language

**Majestic Monolith**:
A complete, independently deployable Rails application that owns a focused domain (DM, WUT, Wv2). Not a microservice — a full app with its own DB, Sidekiq, and UI where useful.
_Avoid_: service, microservice, module (when meaning a deployable app)

**Monolith**:
Synonym for majestic monolith in this ecosystem. Each monolith has its own git repo and `AGENTS.md`.
_Avoid_: app (ambiguous), component (too vague)

**Ecosystem**:
The cross-monolith knowledge base in `ecosystem/` — principles, plans, interfaces, ADRs, business-context. The general contractor, not a deployable service.
_Avoid_: platform (overloaded), framework

**data_manager (DM)**:
The data acquisition monolith. Owns EODHD download, parquet production, derivative calculation, reconciliation, and Cromwell download notifications.
_Avoid_: data service, downloader (too narrow)

**winston_unit_test (WUT)**:
The backtesting and daily-operations lab monolith. Mature reference for data sync, portfolios, strategies, and Sidekiq patterns.
_Avoid_: unit test (misleading — it is a full trading app), test env

**winston_v2 (Wv2)**:
The live operational trading monolith. Portfolios, daily analysis, journals, MCP agent surface.
_Avoid_: production (environment-specific), v2 alone (ambiguous without WUT context)

**Cromwell**:
The agentic coordinator — todos, reports, daily orchestration, Telegram/MCP interface. Not a monolith today; runtime lives in `ai/` with nanobot + MCP.
_Avoid_: bot alone (Cromwell is the persona, not just the transport)

**Market**:
A tradable symbol (e.g. AAPL) with metadata in PG. The time-series lives in parquet, not in Market rows.
_Avoid_: symbol alone (symbol is the identifier; Market is the entity), ticker (informal)

**DataCoverage**:
DM metadata row describing what parquet data actually exists for a **Market** — date range, bar count, indicators present. Consumers (WUT, Wv2) may maintain a local mirror of **DataCoverage** for quick availability checks, but the source of truth remains DM's parquet + reconciliation. (Previously sometimes called DmCoverage in consumer code — now standardized.)
_Avoid_: coverage alone (ambiguous)

**Book**:
The join between a Portfolio and a Market — the portfolio's exposure to that market.
_Avoid_: position (Book is the allocation slot; Position is the live holding)

**Portfolio**:
A named trading account configuration: capital, risk params, linked markets (Books), and an applied TradingStrategy.
_Avoid_: account (ambiguous with broker account), fund

**TradingStrategy**:
Reusable methodology — entry/exit strategy names, risk evaluation, ATR multipliers, pyramid rules, and (in WUT lab fingerprints) the full validation-run config window and constraints. Can be shared across Portfolios. Strategy class names must exist in the monolith's StrategyRegistry; unknown classes skip the portfolio (`unsupported_strategy`). In WUT, auto-captured after **Portfolio Signal Optimization** validation backtests via a content **fingerprint** (portfolio membership/name/capital excluded); each win is a **TradingStrategy Selection**.
_Avoid_: strategy alone (too generic), config (implementation term)

**TradingStrategy Selection**:
A record that a fingerprinted **TradingStrategy** was the validation winner for a **Portfolio** (links portfolio, validation run, optimization, outcome metrics, `export_kind`). Used for frequency/regime insight (“won on N portfolios”), not as a separate export entity.
_Avoid_: Optimization Candidate (candidate is pre-capture draft), win alone

**Winston EOD Standard**:
The canonical parquet format DM produces and consumers read. OHLCV + baked-in derivatives (ATR-17, supported MAs). Consumers must read `atr_17` from parquet; missing column triggers portfolio skip (`missing_data`).
_Avoid_: parquet file (the file is an artifact; the Standard is the contract)

**DataCoverage**:
DM metadata row describing what parquet data actually exists for a Market — date range, bar count, indicators present.
_Avoid_: coverage alone (ambiguous)

**Reconciliation**:
DM scanning on-disk parquet and syncing PG metadata to match reality. Enables git-portable data and in-place file updates.
_Avoid_: sync (sync implies fetching; reconciliation implies metadata alignment)

**Symbol Demand**:
The deduplicated set of market symbols required by all consumer portfolios (WUT + Wv2). DM discovers demand by querying each consumer's internal API, fetches each symbol once from EODHD, writes one parquet file per symbol, and notifies all consumers.
_Avoid_: per-portfolio download (DM dedupes across portfolios and monoliths)

**Data Acquisition**:
DM fetching and standardizing market data from EODHD into Winston EOD Standard parquet. Triggered by ecosystem sync, consumer-specific sync rakes, or Cromwell/API triggers.
_Avoid_: DataSync (WUT's `Operations::DataSync` is a legacy Yahoo path — not the ecosystem model)

**DownloadRun**:
A DM orchestration record tracking a download batch — steps, status, errors, timings. Visible to Cromwell.
_Avoid_: job alone (Sidekiq job is different), batch (too generic)

**Consumer**:
A monolith that reads DM parquet (WUT, Wv2). Registered in DM with base URL and verification status.
_Avoid_: client (ambiguous), subscriber

**Portfolio Signal Optimization**:
WUT lab process that compares **TradingStrategy** combinations on a **Portfolio**'s **Books** and ranks winners (e.g. `PortfolioSignalOptimization`, `portfolios:vet_trend`).
_Avoid_: vet alone (ambiguous with viability approval), backtest (single run is one trial inside optimization)

**Optimization Candidate**:
The winning strategy-and-params from **Portfolio Signal Optimization** on a **Portfolio**; a draft result, not yet approved for handoff.
_Avoid_: Trade-Ready Portfolio (that label requires viability gates), vetted (implies economic approval)

**Viability Gates**:
Minimum backtest criteria an **Optimization Candidate** must pass before WUT may export it as a **Trade-Ready Portfolio**.
_Avoid_: vet (optimization completion is not gate passage), profitable (gates are thresholds, not a guarantee in live markets)

**Trade-Ready Portfolio**:
A portable JSON export from WUT that passed **viability gates** and is ready for Wv2 import as a promoted configuration.
_Avoid_: Configured Portfolio (legacy alias — use **Trade-Ready Portfolio**), portfolio config alone (too vague), optimization export (that is an **Optimization Candidate** until gates pass)

**Observation Portfolio**:
A portable JSON export from WUT for an **Optimization Candidate** that did not pass trade-ready gates — imported to Wv2 for **Paper Trading** and regime observation only, not promotion to live capital.
_Avoid_: Trade-Ready Portfolio (requires breakeven gates), live portfolio (no real-money implication)

**Operational Portfolio**:
A **Portfolio** hosted in Wv2 (imported, inactive or active) used for **Daily Analysis** and market observation — not synonymous with live broker capital.
_Avoid_: live portfolio (implies real money), production portfolio (environment-specific)

**Paper Trading**:
Simulated trading and signal tracking without broker execution — journals and positions for observation and regime testing, not real-money fills.
_Avoid_: backtest alone (historical replay in WUT), demo (too informal)

**CashEvent**:
Capital injection or adjustment on a Wv2 Portfolio (e.g. initial_capital on import). Feeds risk sizing in daily analysis.
_Avoid_: deposit (broker term), funding event

**Journal**:
A proposed or confirmed trade action record in Wv2 daily analysis — entry, exit, pyramid, with flow/mtm/risk sizing.
_Avoid_: log (too generic), trade (Journal is the draft; confirmed execution is separate)

**Daily Analysis**:
Wv2's scheduled or triggered evaluation of active Portfolios — signals, journals, tasks, Cromwell notification. Requires a linked **TradingStrategy**; portfolios without one are skipped (`no_strategy`). Requires DM parquet for all Books; any missing symbol skips the whole Portfolio (`missing_data`). Unknown strategy class names skip with `unsupported_strategy`. Idempotent per (portfolio, date). DM fetch is lazy (triggered when analysis finds missing parquet).
_Avoid_: daily run (ambiguous with DM download run), evaluation alone

**MCP Tool**:
An agent-callable operation exposed by `winston_mcp` — narrow, auditable surface for Cromwell to act on Wv2/DM.
_Avoid_: API alone (internal APIs exist separately; MCP is the agent surface)

**Correlation ID**:
A unique identifier for one **MCP Tool** invocation, used to trace that call through monolith internals, **Cromwell** notifications, and operator-facing replies.
_Avoid_: request_id alone (Rails HTTP tag; not the cross-layer trace), trace_id (too generic)

**Parent Correlation ID**:
An optional identifier linking a child **MCP Tool** invocation to an earlier call in the same **Cromwell** turn or workflow (e.g. evaluate → confirm journal).
_Avoid_: session_id (implies nanobot session scope; parent is invocation-level chaining)

**Ecosystem Audit Log**:
The cross-monolith integration audit trail under `ecosystem/logs/audit/` — **Integration Log** entries only (MCP invocations, webhook delivery, internal API access at coordination boundaries). Not monolith application logs; Rails, Sidekiq, and app runtime errors stay in each monolith with local log rolling.
_Avoid_: audit log alone (ambiguous with Rails request logs), container stdout (ephemeral), dumping all app errors centrally

**Integration Log**:
A single append-only record in the **Ecosystem Audit Log** describing one cross-boundary action (e.g. one **MCP Tool** call, one Cromwell webhook POST, one DM→consumer notify).
_Avoid_: application log (monolith-internal debug), journal (trading domain record)

**Responsive Page**:
A human UI route that returns a usable first response quickly; heavy data is progressive (Hotwire frames/streams) or asynchronous (Sidekiq / ActiveJob), not loaded fully inside the original request. Summary cells prefer **DataCoverage** and aggregates over full history loads.
_Avoid_: blocking page (request waits for complete analytical load), full_history on index

## Relationships

- A **Portfolio** has many **Books** (one per **Market**)
- A **Portfolio** applies one **TradingStrategy** (loose coupling — strategy is a separate entity)
- **DM** produces **Winston EOD Standard** parquet per **Market**; **Consumers** (WUT, Wv2) read it
- **DM** maintains **DataCoverage** metadata that reflects parquet reality after **Reconciliation**
- **WUT** runs **Portfolio Signal Optimization** → **Optimization Candidate** → validation backtest → fingerprinted **TradingStrategy** + **TradingStrategy Selection** → (viability gates) → **Trade-Ready Portfolio** JSON *or* **Observation Portfolio** JSON → **Wv2** imports an **Operational Portfolio** + **CashEvent** + linked **TradingStrategy**
- An **Operational Portfolio** in Wv2 may be inactive, paper-observed, or live — import does not imply real-money trading
- **Cromwell** receives webhooks/notifications from **DM** and **Wv2**; invokes **MCP Tools** for actions
- Each **MCP Tool** invocation has a **Correlation ID**; chained calls in one turn may share a **Parent Correlation ID**
- **Integration Log** entries land in the **Ecosystem Audit Log**; **Cromwell** and agents read them to trace coordination failures
- **DownloadRun** belongs to **DM**; tracks acquisition orchestration
- Human UI routes across monoliths are **Responsive Pages** (ADR-005): snappy shell first; progressive/async data second

## Example dialogue

> **Dev:** "When a **Trade-Ready Portfolio** moves from **WUT** to **Wv2**, does the **TradingStrategy** come with it?"
> **Domain expert:** "Yes — the JSON includes strategy names and risk params. **Wv2** creates or updates a **TradingStrategy** by name, then links it to the new **Portfolio**. The **Markets** list becomes **Books**."

> **Dev:** "Can a losing backtest still reach **Wv2**?"
> **Domain expert:** "Yes — as an **Observation Portfolio** for **Paper Trading** and regime watching. **Trade-Ready Portfolio** is the breakeven+ export path for promoted configs."

> **Dev:** "Who calculates **ATR-17**?"
> **Domain expert:** "**DM** — always. Consumers read it from **Winston EOD Standard** parquet. **WUT** used to calculate locally; that path is legacy for new work."

## Flagged ambiguities

- "account" can mean broker account, Portfolio, or Cromwell principal — resolved: use **Portfolio** for trading config, **Cromwell principal** for the human operator.
- "sync" is overloaded — resolved: **Data Acquisition** (DM←EODHD); **Reconciliation** (parquet→PG metadata); **Symbol Demand** (consumers→DM discovery). WUT `Operations::DataSync` (Yahoo→activities) is legacy, not the target model.
- "audit log" is overloaded — resolved: **Ecosystem Audit Log** = integration/coordination events only; monolith application errors and request logs remain local per monolith.
- "strategy" alone is overloaded — resolved: **TradingStrategy** for the reusable methodology entity; strategy class names (e.g. `Breakout20DayStrategy`) are implementation identifiers.
- "vetted" / "export" overloaded — resolved: optimization complete → **Optimization Candidate**; breakeven+ gates → **Trade-Ready Portfolio**; sub-breakeven observation → **Observation Portfolio**; Wv2 hosting → **Operational Portfolio** (may be paper-only).
- "Configured Portfolio" — resolved: legacy term; canonical name is **Trade-Ready Portfolio**.
- "ready for Wv2" vs "ready for live money" — resolved: Wv2 import elevates observation (**Paper Trading**, **Daily Analysis**); live broker execution is a later, explicit step.
- "DmCoverage" (and variants: dm_coverage, DmCoverage model/association) was used in WUT and Wv2 for the local consumer mirror of DM's metadata — resolved: converge on the canonical **DataCoverage** term everywhere. Deprecate and remove consumer-specific naming variants (DmCoverage, etc.). Consumers maintain a local **DataCoverage** (as their view of available DM parquet via Reconciliation). Glossary definition of **DataCoverage** is authoritative for the concept (DM-owned metadata describing parquet reality).
- "`activities` table" / `market.activities` (and `Activity` records) in WUT was the carrier for market time-series (OHLCV + indicators) — resolved: for DM-sourced **Market** data this is **very temporary** and deprecated. DM parquet (via **Winston EOD Standard** + **DataCoverage**) is the authoritative source. All references (positions, trading_signals, backtest_indicator_values, passed_signals, market_indicator_values, etc.) must be refactored to use composite `(market_id, date)` keys + **Bar** objects from the DM loader. No DB table row for bar identity (use composite or non-persisted derivative). No long-lived shim. Call sites for creation (e.g. Position/TradingSignal/BIV construction) and usage (risk, expected return, charts, views) updated to loader + composite. "Just use DM to pull the data again" at render time using stored (market, date). Backtest result views pull via loader from stored (market, date); backtest runs have dedicated result parquet storage. All legacy non-DM records are defunct and deprecated; there is no historical or legacy relationship that we need to curate. The `activities` table itself is deprecated for market time-series and can eventually be removed or emptied for DM symbols (and legacy paths as they are cleaned).
- The `belongs_to :activity` on Position, TradingSignal, PassedSignal, BacktestIndicatorValue, MarketIndicatorValue, MarketMovingAverage, etc. is to be removed or fully deprecated for DM-sourced data. Refactor creation and usage sites to use the composite key + Bar (from the DM loader). The association remains only for truly legacy non-DM records. However, with the integration of DM all legacy non-DM records are defunct and can be considered deprecated. There is no historical or legacy relationship that we need to curate.
- For obtaining time-series data for a **Market** (DM-sourced), the primary mechanism is direct from **Winston EOD Standard** parquet via a loader (returning Bar/ParquetBar-like objects, e.g. with market_id). The expression `market.activities` (and the `activities` table) is not supported for DM-sourced Markets. The Data Sets page becomes a pure registry view of DM's **DataCoverage**; it no longer materializes or "loads" time-series into WUT.
