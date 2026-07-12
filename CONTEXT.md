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
The backtesting and laboratory monolith — candidate selection for markets, strategies, **TradingStrategy**, portfolios, risk, and signals before operational engagement. Mature reference for data sync, portfolios, strategies, and Sidekiq patterns.
_Avoid_: unit test (misleading — it is a full trading app), test env, production ops (that is **Wv2**)

**winston_v2 (Wv2)**:
The operational trading monolith — **Daily Analysis**, journals, human tasking (paper or real), MCP agent surface. Past theory: hygiene of engaged portfolios protects risk and performance evaluation.
_Avoid_: production (environment-specific), v2 alone (ambiguous without WUT context), lab (that is **WUT**)

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
Reusable methodology — entry/exit strategy names, risk evaluation, ATR multipliers, pyramid rules, and (in WUT) the full validation-run config window and constraints. Can be shared across Portfolios. Strategy class names must exist in the monolith's StrategyRegistry; unknown classes skip the portfolio (`unsupported_strategy`). **Identity is dual:** in **WUT** lab, content **fingerprint** is the canonical identity (portfolio name/membership/capital excluded); at handoff/**Wv2**, **name** is the human label and default lookup, while fingerprint/WUT TS id are **provenance** that must not be silently discarded. A **different fingerprint is a different methodology** — not an in-place edit of the prior recipe. In WUT, auto-captured after **Portfolio Signal Optimization** validation backtests; each win is a **TradingStrategy Selection**.
_Avoid_: strategy alone (too generic), config (implementation term)

**TradingStrategy Selection**:
A record that a fingerprinted **TradingStrategy** was the validation winner for a **Portfolio** (links portfolio, validation run, optimization, outcome metrics, `export_kind`). Used for frequency/regime insight (“won on N portfolios”), not as a separate export entity. **WUT-only** — does not cross the handoff as its own artifact.
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
A **Portfolio** hosted in Wv2 used for **Daily Analysis** and human tasking — past lab theory and into **execution** (paper or real). Not end-to-end automated broker fills. One lab seed may yield multiple operational implementations (different **TradingStrategy** fingerprints); each keeps its own journals/performance. When fingerprint is present, display name includes a short fingerprint suffix on first import. **WUT** is the candidate-selection lab; **Wv2** is the operational component.
_Avoid_: live portfolio (implies real money only), production portfolio (environment-specific)

**Active** (portfolio):
Operator-selected attention priority: included in **Daily Analysis** and the human task surface (paper or real trade prompts). Not “automated live trading.” Many inactive OPs per seed are normal (regime archive). Second **Active** without force is blocked when (1) same **seed_name** or (2) identical **Books** set as another Active OP. Short dual-active experiments use force.
_Avoid_: live (money), enabled (vague), running (sounds like a job)

**Engaged Operational Portfolio**:
An **Operational Portfolio** that has any **Journal** (paper or real intent). Methodology (**TradingStrategy**) and **Books** are immutable until **Closed** or successor **Rebalance**; capital may still change via **CashEvent**. Re-import must not mutate an engaged portfolio.
_Avoid_: active alone (Active is attention; Engaged is journal lock), in use (vague)

**Closed Operational Portfolio**:
An **Operational Portfolio** deliberately ended so it no longer participates in signal evaluation; prior journals/performance remain for regime history. Closing means signals on that OP+TS combo are no longer meaningful going forward. **Close preconditions split by intent:** **Paper Trading** may soft-close (mark closed, stop signals, leave historical open residue for human cleanup). **Real-intent** trading requires flat (no open positions; pending journals resolved) before close, unless an explicit force-flatten path is used.
_Avoid_: deleted (history should remain), deactivated alone (inactive ≠ closed)

**Rebalance** (operational):
A deliberate change to an **Operational Portfolio** while operating in **Wv2** (not lab re-vet in **WUT**). **Policy split:** capital adjustments are **CashEvents** on the same OP (in-place series). **Shape changes** (Books membership and/or **TradingStrategy** / fingerprint) take the **successor path**: close or end A for signals, open A′ linked as successor — journals stay on A. Never silent re-import mutation of an **Engaged** OP.
_Avoid_: re-import (file handoff), optimize (WUT lab), treating capital top-up as a full rebalance

**Execution Mode**:
Explicit intent on an **Operational Portfolio**: `paper` or `real`. Default **paper** on import. Independent of `export_kind` (economic promotion) and **Active** (attention). Branches close preconditions and human task framing; does not by itself automate broker fills. Moving to real capital is always a **new OP series** (successor A′): new initial **CashEvent** for committed capital — never paper terminal equity. Paper A is **not auto-closed** (should close for hygiene; humans may leave it running). Dual **Active** same seed still needs force.
_Avoid_: deriving mode from Active or export_kind alone; promoting paper→real in place on the same capital series

**Capital Activation**:
Operator command (e.g. Telegram: “Activate Portfolio Red + TS… with initial capital $X”) that opens a **new** **Operational Portfolio** series for a chosen seed+TS fingerprint with a stated initial **CashEvent**, default **Execution Mode** `real` and **Active** true. Requires **Trade-Ready** provenance (or explicit force override) — observation-only paper series cannot open real capital by default. Distinct from only flipping the **Active** flag. Does not rewrite the paper series’ journals or capital_base; does not auto-close or auto-deactivate paper A. If paper A (or any same **seed_name** / identical **Books**) is already **Active**, requires explicit force to keep dual attention.
_Avoid_: Activate alone (ambiguous with Active flag), promote in place

**Paper Trading**:
Simulated execution and signal tracking without broker fills — **Execution Mode** `paper`. Still **execution** for hygiene: journals lock OP+TS shape. Import never implies evaluation: land inactive until explicit **Active**. Soft-close allowed. Wv2 tasks a human; it does not automate fills end-to-end.
_Avoid_: backtest alone (historical replay in WUT), demo (too informal), theory (paper in Wv2 is post-theory)

**CashEvent**:
Capital injection or adjustment on a Wv2 Portfolio (e.g. initial_capital on import). Feeds risk sizing in daily analysis.
_Avoid_: deposit (broker term), funding event

**Journal**:
A proposed or confirmed trade action record in Wv2 daily analysis — entry, exit, pyramid, with flow/mtm/risk sizing. Any journal (paper or not) **engages** the **Operational Portfolio** and freezes its tradeable shape until **Closed**.
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

**Portfolio Correlation Score (PCS)**:
A versioned 0–100 composite summarizing diversification quality of a **Portfolio**’s **Books**. Primary driver is worst pairwise absolute correlation (max \|r\|) and high-pair count; mean pairwise \|r\| is secondary. Used for lab build acceptance, handoff provenance, and operational time-series monitoring — not a **TradingStrategy** performance metric. **WUT** is the system of record that computes and stores the score time series; **Wv2** consumes snapshots via a WUT client when operator surfaces need them (e.g. **Daily Activity Report**).
_Avoid_: correlation alone (ambiguous with pairwise r or audit Correlation ID), diversification rating alone (UI label without time series), mean correlation alone (can be diluted by junk series), recomputing divergent formulas in Wv2 without WUT

**Correlation Snapshot**:
A point-in-time record of a **Portfolio Correlation Score** plus transparent components (max \|r\|, mean \|r\|, high pairs, date window, methodology version) for a **Portfolio** on an as-of date. Produced by **WUT**; may be embedded at handoff and fetched again by **Wv2**.
_Avoid_: sidecar alone (build artifact; snapshot is the durable observation), heatmap alone (visual, not the stored score)

**Correlation Methodology Version**:
An immutable recipe identifier for how **Portfolio Correlation Score** and build constraints are computed (windows, quality gates, max-pairwise cap, weights). Changing the recipe requires a new version; historical snapshots keep their original version.
_Avoid_: strategy fingerprint (that is **TradingStrategy** identity), algorithm alone (too vague)

**Daily Activity Report (DAR)**:
The operator-facing Wv2 daily narrative (markdown/PDF) summarizing **Active** **Operational Portfolios** after **Daily Analysis** — status, next steps, equity context, and (when present) **Portfolio Correlation Score** time series.
_Avoid_: daily analysis alone (the job; DAR is the report), Cromwell notification alone (transport payload; DAR is the human document)

## Relationships

- A **Portfolio** has many **Books** (one per **Market**)
- A **Portfolio** applies one **TradingStrategy** (loose coupling — strategy is a separate entity)
- **DM** produces **Winston EOD Standard** parquet per **Market**; **Consumers** (WUT, Wv2) read it
- **DM** maintains **DataCoverage** metadata that reflects parquet reality after **Reconciliation**
- **WUT** runs **Portfolio Signal Optimization** → **Optimization Candidate** → validation backtest → fingerprinted **TradingStrategy** + **TradingStrategy Selection** → (viability gates) → **Trade-Ready Portfolio** JSON *or* **Observation Portfolio** JSON → **Wv2** imports an **Operational Portfolio** + **CashEvent** + linked **TradingStrategy**
- Handoff JSON may carry fingerprint / WUT TS id as **provenance**. When fingerprint is present, **Operational Portfolio** and **TradingStrategy** display names always include a **short fingerprint suffix** (e.g. `Portfolio Red · a1b2c3d4`) — including the first import. **Lineage match key** is the full fingerprint (stored on both OP and TS), not reconstructed display name. Import resolution: (1) same fingerprint → update that pair; (2) no fingerprint match, bare seed-name OP exists **and** Books symbols match → **adopt** (attach fingerprint, rename to suffix form, update); (3) else → **auto-fork** new OP+TS. Legacy JSON with no fingerprint may still update by bare seed name
- Performance of an **Operational Portfolio** under **Paper Trading** is a **regime heuristic** for that **TradingStrategy** fingerprint, not a property of the lab seed name alone
- Import always lands **Operational Portfolios** inactive regardless of `export_kind`; missing `export_kind` is treated as **Observation Portfolio**. Explicit **Active** selects which OPs enter **Daily Analysis** and the human attention queue. Hygiene mutex (unless force): at most one **Active** OP per **seed_name**, and at most one **Active** OP per identical **Books** symbol set. Many inactive regime variants may coexist. Import does not imply real-money trading or automated execution
- First **Journal** on an OP **engages** it: Books + TS immutable until **Closed** or successor **Rebalance**; capital may still move via **CashEvent**. Lifecycle sketch: imported/inactive → **Active** (not engaged) → **Engaged** (any Journal) → **Closed** (optional successor A′). Shape rebalance = close A + open A′ (link successor); capital-only = CashEvent on A. **Close:** paper may soft-close; real-intent requires flat first (optional force-flatten). Same-fingerprint re-import may update only **pre-engagement** OPs. **WUT** proposes candidates; **Wv2** executes and preserves evaluation integrity
- **Cromwell** receives webhooks/notifications from **DM** and **Wv2**; invokes **MCP Tools** for actions
- Each **MCP Tool** invocation has a **Correlation ID**; chained calls in one turn may share a **Parent Correlation ID**
- **Integration Log** entries land in the **Ecosystem Audit Log**; **Cromwell** and agents read them to trace coordination failures
- **DownloadRun** belongs to **DM**; tracks acquisition orchestration
- Human UI routes across monoliths are **Responsive Pages** (ADR-005): snappy shell first; progressive/async data second
- A **Portfolio**’s **Books** yield a **Correlation Snapshot** under a **Correlation Methodology Version**; **WUT** is source of truth for the **Portfolio Correlation Score** time series (scheduled after DM data readiness)
- Handoff JSON may carry a baseline **Correlation Snapshot**; **Wv2** pulls latest/history from **WUT** via client when **Daily Activity Report** or other tasking needs PCS; may **flag** degradation for operator review (shape change still follows **Rebalance** / successor rules — score does not auto-mutate **Books** or auto-open a successor)

## Example dialogue

> **Dev:** "When a **Trade-Ready Portfolio** moves from **WUT** to **Wv2**, does the **TradingStrategy** come with it?"
> **Domain expert:** "Yes — methodology travels in the JSON. **Wv2** creates an **Operational Portfolio** + **TradingStrategy** (fingerprinted names when provenance is present), Books from markets, and initial **CashEvent**. Import stays inactive until you mark it **Active**."

> **Dev:** "Can I keep two Portfolio Red fingerprints both **Active**?"
> **Domain expert:** "Only with force — hygiene first. Archive variants stay inactive; dual-active is a short experiment, not the default. Wv2 is an observation post that tasks humans, not an autotrader."

> **Dev:** "We re-vet and re-import while Portfolio Red already has paper journals. Update the strategy params?"
> **Domain expert:** "No — any **Journal** **engages** the OP. Shape is frozen until **Closed**. Close the old series (signals no longer meaningful), then import/activate a new OP+TS for the new candidate. Otherwise risk and performance series are corrupted."

> **Dev:** "Is paper trading still 'lab'?"
> **Domain expert:** "No — lab is **WUT**. Paper in **Wv2** is operational execution without broker fills. Hygiene rules still apply."

> **Dev:** "We need to drop ROKU from an engaged Red and change the exit strategy."
> **Domain expert:** "That's a shape **Rebalance** — successor path. Close A (signals on A stop), open A′ without ROKU and with the new TS. Journals stay on A so performance isn't rewritten. Capital top-ups alone are just **CashEvents** on A. Soft-close vs flat-required follows **Execution Mode** (`paper` vs `real`), not export_kind."

> **Dev:** "Paper Red ran $20K → $45K. We want to go real with the same TS."
> **Domain expert:** "**Capital Activation**: open real A′ with a new initial **CashEvent** for committed capital (e.g. $13,986) — not paper terminal equity. A′ defaults **Active** + `real`. Requires trade-ready provenance or force. Paper A is not auto-closed or auto-deactivated; dual **Active** on the same seed needs force. Journals on A and A′ stay separate series."

> **Dev:** "Can a losing backtest still reach **Wv2**?"
> **Domain expert:** "Yes — as an **Observation Portfolio** for **Paper Trading** and regime watching. **Trade-Ready Portfolio** is the breakeven+ export path for promoted configs. Either way, import leaves the **Operational Portfolio** inactive until you explicitly activate it."

> **Dev:** "If two portfolios win the same methodology fingerprint in **WUT**, do we get two strategies in **Wv2**?"
> **Domain expert:** "In **WUT**, one fingerprinted **TradingStrategy** and two **TradingStrategy Selections**. In **Wv2**, each import still carries a display name; same fingerprint/provenance can share methodology, but two lab seeds usually still create two **Operational Portfolios** because Books/capital differ."

> **Dev:** "We re-vet Portfolio Red and get a new fingerprint. Do we overwrite the Wv2 portfolio?"
> **Domain expert:** "No — that would erase the prior regime sample. Default import **auto-forks**: new **TradingStrategy** + new **Operational Portfolio** named with a short fingerprint suffix (e.g. `Portfolio Red · a1b2c3d4`). Prior paper lineage stays. Overwrite/update-by-name only when provenance is the same fingerprint (or legacy import with no fingerprint)."

> **Dev:** "Who calculates **ATR-17**?"
> **Domain expert:** "**DM** — always. Consumers read it from **Winston EOD Standard** parquet. **WUT** used to calculate locally; that path is legacy for new work."

## Flagged ambiguities

- "account" can mean broker account, Portfolio, or Cromwell principal — resolved: use **Portfolio** for trading config, **Cromwell principal** for the human operator.
- "sync" is overloaded — resolved: **Data Acquisition** (DM←EODHD); **Reconciliation** (parquet→PG metadata); **Symbol Demand** (consumers→DM discovery). WUT `Operations::DataSync` (Yahoo→activities) is legacy, not the target model.
- "audit log" is overloaded — resolved: **Ecosystem Audit Log** = integration/coordination events only; monolith application errors and request logs remain local per monolith.
- "strategy" alone is overloaded — resolved: **TradingStrategy** for the reusable methodology entity; strategy class names (e.g. `Breakout20DayStrategy`) are implementation identifiers.
- "vetted" / "export" overloaded — resolved: optimization complete → **Optimization Candidate**; breakeven+ gates → **Trade-Ready Portfolio**; sub-breakeven observation → **Observation Portfolio**; Wv2 hosting → **Operational Portfolio** (may be paper-only).
- "Configured Portfolio" — resolved: legacy term; canonical name is **Trade-Ready Portfolio** (or **Observation Portfolio** when gates fail). Prefer those over “configured portfolio” in new docs.
- "ready for Wv2" vs "ready for live money" — resolved: Wv2 import elevates observation (**Paper Trading**, **Daily Analysis**); live broker execution is a later, explicit step.
- "TradingStrategy identity" across monoliths — resolved: **WUT** = content fingerprint (lab). **Handoff/Wv2** = seed label + short fingerprint suffix on display names when fingerprint is present; **full fingerprint on OP + TS** is the lineage match key (short suffix is display-only). Import: same fingerprint → update; bare seed + matching Books → adopt/rename; else auto-fork. No fingerprint (legacy) ⇒ bare-name update path.
- "Active" vs "observation" vs "live money" — resolved: **Active** = attention priority for **Daily Analysis** + human tasking. **Execution Mode** (`paper` \| `real`) is capital intent (default paper). `export_kind` is WUT economic promotion (observation vs trade_ready). All three are independent. Second **Active** requires force if same **seed_name** or identical **Books** set. Wv2 tasks humans; not an end-to-end autotrader.
- "paper vs theory" / mutate-after-import — resolved: **WUT** = candidate selection lab; **Wv2** = operations. Any **Journal** **engages** an OP (immutable TS/Books/risk until **Closed**, pending explicit **Rebalance** rules). Paper journals count. Re-import must not rewrite an engaged series.
- **Rebalance** — resolved: capital → **CashEvent** in place; Books/TS shape change → successor path (close A, open A′, journals stay on A). Silent re-import must not reshape an **Engaged** OP.
- **Close preconditions** — resolved: **Execution Mode** `paper` = soft-close allowed; `real` = flat-required (force-flatten optional). Engagement lock still applies to both (any journal freezes shape).
- **Execution Mode** — resolved: explicit `paper` \| `real` on OP (default paper); not derived from Active or export_kind. Real capital starts via **Capital Activation**: new OP + new initial **CashEvent**; paper series is not auto-closed (recommended close). Never in-place capital rewrite of the paper series.
- "**Activate**" (Telegram/operator speech) — resolved: often means **Capital Activation** (new series + capital $X), not merely setting the **Active** attention flag. Prefer the term **Capital Activation** in docs; UI/Telegram may still say “activate … with capital”.
- **Capital Activation** defaults — resolved: new OP `real` + **Active**; paper A untouched; dual **Active** same seed/Books requires force (“keep paper running”). Real mode requires **Trade-Ready** provenance unless force override; observation-only stays paper by default.
- "DmCoverage" (and variants: dm_coverage, DmCoverage model/association) was used in WUT and Wv2 for the local consumer mirror of DM's metadata — resolved: converge on the canonical **DataCoverage** term everywhere. Deprecate and remove consumer-specific naming variants (DmCoverage, etc.). Consumers maintain a local **DataCoverage** (as their view of available DM parquet via Reconciliation). Glossary definition of **DataCoverage** is authoritative for the concept (DM-owned metadata describing parquet reality).
- "`activities` table" / `market.activities` (and `Activity` records) in WUT was the carrier for market time-series (OHLCV + indicators) — resolved: for DM-sourced **Market** data this is **very temporary** and deprecated. DM parquet (via **Winston EOD Standard** + **DataCoverage**) is the authoritative source. All references (positions, trading_signals, backtest_indicator_values, passed_signals, market_indicator_values, etc.) must be refactored to use composite `(market_id, date)` keys + **Bar** objects from the DM loader. No DB table row for bar identity (use composite or non-persisted derivative). No long-lived shim. Call sites for creation (e.g. Position/TradingSignal/BIV construction) and usage (risk, expected return, charts, views) updated to loader + composite. "Just use DM to pull the data again" at render time using stored (market, date). Backtest result views pull via loader from stored (market, date); backtest runs have dedicated result parquet storage. All legacy non-DM records are defunct and deprecated; there is no historical or legacy relationship that we need to curate. The `activities` table itself is deprecated for market time-series and can eventually be removed or emptied for DM symbols (and legacy paths as they are cleaned).
- The `belongs_to :activity` on Position, TradingSignal, PassedSignal, BacktestIndicatorValue, MarketIndicatorValue, MarketMovingAverage, etc. is to be removed or fully deprecated for DM-sourced data. Refactor creation and usage sites to use the composite key + Bar (from the DM loader). The association remains only for truly legacy non-DM records. However, with the integration of DM all legacy non-DM records are defunct and can be considered deprecated. There is no historical or legacy relationship that we need to curate.
- For obtaining time-series data for a **Market** (DM-sourced), the primary mechanism is direct from **Winston EOD Standard** parquet via a loader (returning Bar/ParquetBar-like objects, e.g. with market_id). The expression `market.activities` (and the `activities` table) is not supported for DM-sourced Markets. The Data Sets page becomes a pure registry view of DM's **DataCoverage**; it no longer materializes or "loads" time-series into WUT.
