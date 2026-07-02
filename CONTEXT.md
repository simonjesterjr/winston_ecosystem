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

**Book**:
The join between a Portfolio and a Market — the portfolio's exposure to that market.
_Avoid_: position (Book is the allocation slot; Position is the live holding)

**Portfolio**:
A named trading account configuration: capital, risk params, linked markets (Books), and an applied TradingStrategy.
_Avoid_: account (ambiguous with broker account), fund

**TradingStrategy**:
Reusable methodology — entry/exit strategy names, risk evaluation, ATR multipliers, pyramid rules. Can be shared across Portfolios. Strategy class names must exist in the monolith's StrategyRegistry; unknown classes skip the portfolio (`unsupported_strategy`).
_Avoid_: strategy alone (too generic), config (implementation term)

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

**Configured Portfolio**:
A portable JSON export from WUT representing a vetted backtest configuration ready for Wv2 import.
_Avoid_: portfolio config (acceptable alias), backtest result (the run is the source; the config is the export)

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

## Relationships

- A **Portfolio** has many **Books** (one per **Market**)
- A **Portfolio** applies one **TradingStrategy** (loose coupling — strategy is a separate entity)
- **DM** produces **Winston EOD Standard** parquet per **Market**; **Consumers** (WUT, Wv2) read it
- **DM** maintains **DataCoverage** metadata that reflects parquet reality after **Reconciliation**
- **WUT** exports **Configured Portfolio** JSON → **Wv2** imports and creates **Portfolio** + **CashEvent**
- **Cromwell** receives webhooks/notifications from **DM** and **Wv2**; invokes **MCP Tools** for actions
- **DownloadRun** belongs to **DM**; tracks acquisition orchestration

## Example dialogue

> **Dev:** "When a **Configured Portfolio** moves from **WUT** to **Wv2**, does the **TradingStrategy** come with it?"
> **Domain expert:** "Yes — the JSON includes strategy names and risk params. **Wv2** creates or updates a **TradingStrategy** by name, then links it to the new **Portfolio**. The **Markets** list becomes **Books**."

> **Dev:** "Who calculates **ATR-17**?"
> **Domain expert:** "**DM** — always. Consumers read it from **Winston EOD Standard** parquet. **WUT** used to calculate locally; that path is legacy for new work."

## Flagged ambiguities

- "account" can mean broker account, Portfolio, or Cromwell principal — resolved: use **Portfolio** for trading config, **Cromwell principal** for the human operator.
- "sync" is overloaded — resolved: **Data Acquisition** (DM←EODHD); **Reconciliation** (parquet→PG metadata); **Symbol Demand** (consumers→DM discovery). WUT `Operations::DataSync` (Yahoo→activities) is legacy, not the target model.
- "strategy" alone is overloaded — resolved: **TradingStrategy** for the reusable methodology entity; strategy class names (e.g. `Breakout20DayStrategy`) are implementation identifiers.