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

**Confirmational Entry**:
Optional second entry filter on a **TradingStrategy**: primary entry strategies AND confirmational strategies must all fire before an **initial** entry is taken (hard mode). Soft mode may still enter at reduced risk size when confirms fail. **Does not gate pyramids** — see **One-Way Dynamic Risk**. ADR-008.
_Avoid_: confirmation alone (ambiguous with journal fill confirm), treating pyramid adds as confirmational entry

**One-Way Dynamic Risk**:
Risk-evaluation mode that assigns a **risk % per concurrent pyramid level** (and direction) from a configured ladder (e.g. long 2%→3%→4%→6%). Intent: scale risk into a sustained trend after ATR adds confirm continuation. Orthogonal to **Confirmational Entry**. Base `risk_percentage` on a PBR is not the full story when a ladder is present.
_Avoid_: static risk, “dynamic” alone (ambiguous with equity-curve risk)

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
Operator-selected attention: the OP is included in **Daily Analysis** and the human task surface. Not “automated live trading” and not “only one portfolio at a time.” Multiple **Active** OPs across different seeds are normal and desired — typically a **paper band** (observation / risky or under-researched recipes) and a **real band** (capital at risk). Mutex (unless force): at most one **Active** OP per **seed_name**, and at most one **Active** OP per identical **Books** set. Inactive OPs are the archive/noise queue (operator may clean, remove, or later activate).
_Avoid_: live (money), sole focus OP, enabled (vague), running (sounds like a job), treating multi-Active as a defect

**Engaged Operational Portfolio**:
An **Operational Portfolio** that has any **Journal** — including a **draft** on **Signal Date**, before any fill. That OP is one series of seed + **TradingStrategy** fingerprint + **Books**; its journals belong only to that series. Methodology and **Books** are immutable until **Closed** or successor **Rebalance**; capital may still change via **CashEvent**. Independent of **Active** and **Execution Mode** (paper or real). Re-import must not mutate an engaged portfolio; same fingerprint does not create a second OP.
_Avoid_: active alone (Active is attention; Engaged is journal lock), in use (vague), unlock by deactivating or switching paper/real

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
Operator command that opens a **new** **real** **Operational Portfolio** series with a stated initial **CashEvent** `$X` — not paper terminal equity. Preferred speech: “**Make** Portfolio Red + Ts10 **real** with initial capital $X” or “**make** \<fingerprint\> **real** with initial capital $X” (not “Activate …”, which collides with the **Active** flag). Source recipe must already exist in **Wv2** (seed OP for **Books**, **TradingStrategy** for methodology); missing either → error to import from WUT first, not a multi-step transfer workflow. New OP keeps the **same methodology fingerprint** as the source unit (fingerprint is recipe identity, not paper-vs-real). Defaults: **Execution Mode** `real`, **Active** true. **Trade-ready / observation provenance:** soft **warn** in reply when not trade-ready — do **not** hard-block; capital hygiene is human responsibility (warnings + confirmations ok). Does not rewrite paper journals/capital; does not auto-**Close** paper A. **Default hygiene:** auto-**deactivate** paper A (same seed/Books) when real A′ becomes Active; optional force keeps dual **Active**.
_Avoid_: Activate alone (ambiguous with Active flag), promote in place, minting a new fingerprint only because mode is real, auto-closing paper on capital activation, hard-refusing real on observation export_kind

**Paper Trading**:
Simulated execution and signal tracking without broker fills — **Execution Mode** `paper`. Still **execution** for hygiene: journals lock OP+TS shape. Import never implies evaluation: land inactive until explicit **Active**. Soft-close allowed. Wv2 tasks a human; it does not automate fills end-to-end.
_Avoid_: backtest alone (historical replay in WUT), demo (too informal), theory (paper in Wv2 is post-theory)

**CashEvent**:
Capital injection or adjustment on an **Operational Portfolio**. **Initial** CashEvent may land on import or **Capital Activation**. **Top-up** (“**add** $5000 **to** \<fingerprint or OP name\>”) is allowed **only** on **Active** + **Execution Mode** `real` OPs — paper series never receive added capital (they live and die on initial lab/ops capital as attention tests). Not Capital Activation (that opens a **new** real series). Resolve fingerprint among real Active matches; ask if multiple; refuse paper / inactive / closed.
_Avoid_: deposit (broker term), funding event, “make real” for a top-up, adding capital to paper

**Journal**:
A proposed or confirmed trade action record in Wv2 — entry, exit, pyramid, with flow/mtm/risk sizing. Carries a **Signal Date** (when the recommendation was born) and, once executed, a **Fill Date** (when the **Position** changes). Any journal (paper or not) **engages** the **Operational Portfolio** and freezes its tradeable shape until **Closed**.
_Avoid_: log (too generic), trade (Journal is the draft; confirmed execution is separate), conflating signal day with fill day

**Signal Date**:
The bar date on which **Daily Analysis** (or an explicit desk signal) generated an entry/exit recommendation for a **Market** on an **Operational Portfolio** (day T in the EOD cadence).
_Avoid_: trade_date alone (overloaded with fill), report_date alone (report packaging, not the signal concept)

**Fill Date**:
The session date when a confirmed **Journal** opens or closes a **Position** and books cash impact. For the canonical Winston EOD path, **Fill Date** is the **next session after Signal Date** (T+1); fill price defaults to that session’s **open**.
_Avoid_: trade_date alone without saying signal vs fill, same-bar close as the default EOD fill

**Human-Gated**:
Position open/close (and free-form desk fills) require an explicit operator desk action — ops form, ops shell, or Cromwell/MCP on a human instruction — not silent mutation by **Daily Analysis**. **Execution Mode** `real` is always human-gated; paper follows the same confirm step today (optional paper autofill is a later, explicit decision).
_Avoid_: autotrader (future product), treating draft creation as a fill

**Desk Action**:
An operator-facing verb that may change lots or amend a draft: confirm **Journal**, book ad-hoc trade, exit, stop update (and kin). Surfaces: desk form, ops shell, MCP/Telegram. Confirm for the EOD path is expected by **Fill Date** (next session after **Signal Date**); unconfirmed drafts become **Passed Signals** and remain visible as attention items (especially on **Active** **real** OPs).
_Avoid_: Daily Analysis (proposes only), task alone (the reminder; Desk Action is the mutation), treating casual ignore as normal strategy

**Desk Handoff**:
A deterministic next-step package from **Daily Analysis** / **DAR** for one **Operational Portfolio**: what to do, why (signal + capacity/swap reason), and a deep link into a **Desk Workflow** (Wv2 page) plus Telegram/shell phrases. Multi-leg packages (e.g. exit ABC then enter XYZ) are **one logical handoff** with **N linked Journals/tasks**, ordered; confirming out of order **warns** (and may refuse enter while capacity still full). Human may ignore links; ignoring past the action window is a **process miss**, not a strategy choice. Algorithm ranks contests; human supplies confirmation and **Fulfillment** details Winston may not fully know.
_Avoid_: open-ended alternative menus as the default, next step without a confirm path, silent out-of-order multi-leg confirms

**Desk Workflow**:
The guided Wv2 UI path that walks a human through one **Desk Handoff** / **Journal** (review signal, next-open prefill, units/price/stop, packaging, confirm). Target product surface; today only partially supported (`/operations/desk` prefill, ops panels, Telegram/MCP phrases) — not a full journal workflow app yet.
_Avoid_: assuming Telegram alone is the complete desk, dead `resources :journals` without controller

**Fulfillment**:
How humans (or a future separate automation component) actually realize a Winston signal in the market — broker fills, LEAPs, partial size, delays, clearing failures. **Winston** is the **signal and prioritization system** (trend/methodology evaluation, deterministic desk work queue) — analogous to a warehouse management system prioritizing picks for human workers — not the assumption of complete fulfillment truth. Journals bridge signal → reported fill; they do not claim OMS completeness.
_Avoid_: equating Winston with a broker OMS, assuming DA state equals market state, baking autotrader into DA

**Signal Spine**:
What the fingerprint / **Daily Analysis** recommended for an OP (signal side, direction, methodology sizing, expected-return story, algorithmic pass/swap reasons) — retained for methodology and process audit even when **Fulfillment** differs.
_Avoid_: using signal sizes as live cash when fills differ

**Booked Capital Spine**:
What the OP actually did via executed **Journals** / **Positions** / **CashEvents** — cash, risk sizing base, and DAR equity for the live series. Diverges from the **Signal Spine** when packaging, size, timing, or process miss differs.
_Avoid_: rewriting booked history to match ideal next-open stock fills

**Working Stop**:
The stop price Winston treats as current on an open **Position** on the **Booked Capital Spine** (`updated_stop` / desk-updated). May start from methodology ATR default (signal/default stop) and then diverge via **Desk Action**. Winston does not assume the broker’s resting order matches this value.
_Avoid_: broker stop alone as SoT, assuming DA knows live exchange stops

**Stop-Out Reconciliation**:
Desk workflow when real-world **Fulfillment** exits a lot because a stop was hit (or should have been): human books an exit **Journal** **required-linked** to the open **Position**, storing a snapshot (working_stop_at_exit, fill_price, gap) with reason (e.g. external_stop). **Warn** (do not hard-block by default) when fill diverges from **Working Stop**; allow confirm with note. No Winston exit signal is invented. Ties “what happened in life” to the **Booked Capital Spine**.
_Avoid_: ad-hoc exit with no position/stop provenance, treating external stop as unrelated to the Winston lot, silent large gaps

**Signaled Entry Rule**:
No **Position** open (enter/pyramid) on an **Operational Portfolio** without a **methodology-originated** Winston signal on the **Signal Spine** — primarily a **Daily Analysis** draft enter/pyramid **Journal** + task (or a leg of an algorithm **Desk Handoff** package) for that OP and underlying. Confirm/book may change **Fulfillment Packaging**, size, and price but must reference the signal (`signal_journal_id` / task). Naked free-form enter is out of policy; force + audit is the only exception path. (Today’s ad-hoc book-enter tools are transitional and should converge on this rule.)
_Avoid_: ad-hoc enter as the normal path, inventing fills with no signal provenance, treating any enter journal as self-authorizing signal

**Unsignaled Exit Allowance**:
Exits **may** occur without a Winston exit signal — stops, clearing/broker errors, downstream misses, discretionary flatten — booked on the **Booked Capital Spine** with reason codes and, when closing a known lot, position linkage (**Stop-Out Reconciliation** when stop-related). Asymmetry is intentional: entries are methodology-gated; exits must reflect market reality Winston may not have seen.
_Avoid_: requiring a DA exit signal before any close, inventing fake exit signals to “make the ledger tidy”

**Passed Signal**:
A signal that did not become an executed fill — either **algorithmic** (capacity/rules: e.g. max markets, no valid swap) or **process miss** (human did not confirm by the action window / **Fill Date**). On paper, primarily regime/theoretical. On **Active** real, a process miss is treated as possible stakeholder or market/clearing error and must surface for correction — not as a free “I chose to skip.”
_Avoid_: cancel as silent success, pass as discretionary strategy choice without an algorithm reason

**Fulfillment Packaging**:
How a confirmed signal is realized in the market: stock shares, LEAP/option contracts, proxy, etc. The **Journal** still tracks the **signal** (underlying **Market**, direction, methodology sizing story); the fill may use different units/instrument (e.g. signal sized as 206 shares of ABC → confirm 2× Jan 2028 LEAP calls). Cash impact follows packaging (e.g. contracts × premium × multiplier). Part of **Fulfillment** — Winston prioritizes the work; packaging details often come only from the human. Does not waive the **Signaled Entry Rule**.
_Avoid_: requiring the fill instrument to equal the signal share count; treating LEAP as a different signal

**Daily Analysis**:
Wv2's scheduled or triggered evaluation of **Active** Portfolios — signals, **draft** journals, tasks, **Passed Signals**, Cromwell/**DAR** notification. May create draft enter/exit **Journals** for paper and real as convenience; never opens or closes **Positions** (ADR-009). Capacity and rank rules (max markets, swaps, pyramid priority) should yield **deterministic** recommendations or algorithmic passes — not open-ended “human pick among expected returns” menus from Winston. Requires a linked **TradingStrategy**; portfolios without one are skipped (`no_strategy`). Requires DM parquet for all Books; any missing symbol skips the whole Portfolio (`missing_data`). Unknown strategy class names skip with `unsupported_strategy`. Idempotent per (portfolio, date). DM fetch is lazy (triggered when analysis finds missing parquet).
_Avoid_: daily run (ambiguous with DM download run), evaluation alone, auto-fill (DA does not fill)

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
The operator-facing Wv2 daily narrative (markdown/PDF) after **Daily Analysis**. Primary job: make human attention unmistakable by **attention band** — **Active** + **Execution Mode** `real` first (capital at risk), **Active** + `paper` next (strategy/market learning), inactive only as a short hygiene/noise appendix when useful. Carries status, next steps, desk handoffs, equity context, and (when present) **Portfolio Correlation Score** time series.
_Avoid_: daily analysis alone (the job; DAR is the report), flat “all Active” list with no paper/real split, Cromwell notification alone (transport payload; DAR is the human document)

## Relationships

- A **Portfolio** has many **Books** (one per **Market**)
- A **Portfolio** applies one **TradingStrategy** (loose coupling — strategy is a separate entity)
- **DM** produces **Winston EOD Standard** parquet per **Market**; **Consumers** (WUT, Wv2) read it
- **DM** maintains **DataCoverage** metadata that reflects parquet reality after **Reconciliation**
- **WUT** runs **Portfolio Signal Optimization** → **Optimization Candidate** → validation backtest → fingerprinted **TradingStrategy** + **TradingStrategy Selection** → (viability gates) → **Trade-Ready Portfolio** JSON *or* **Observation Portfolio** JSON → **Wv2** imports an **Operational Portfolio** + **CashEvent** + linked **TradingStrategy**
- Handoff JSON may carry fingerprint / WUT TS id as **provenance**. When fingerprint is present, **Operational Portfolio** and **TradingStrategy** display names always include a **short fingerprint suffix** (e.g. `Portfolio Red · a1b2c3d4`) — including the first import. **Lineage match key** is the full fingerprint (stored on both OP and TS), not reconstructed display name. Import resolution: (1) same fingerprint → update that pair; (2) no fingerprint match, bare seed-name OP exists **and** Books symbols match → **adopt** (attach fingerprint, rename to suffix form, update); (3) else → **auto-fork** new OP+TS. Legacy JSON with no fingerprint may still update by bare seed name
- Performance of an **Operational Portfolio** under **Paper Trading** is a **regime heuristic** for that **TradingStrategy** fingerprint, not a property of the lab seed name alone
- Import always lands **Operational Portfolios** inactive regardless of `export_kind`; missing `export_kind` is treated as **Observation Portfolio**. Explicit **Active** selects which OPs enter **Daily Analysis** and the human attention queue. **Multi-Active is product intent:** run several **Active** paper OPs and a smaller set of **Active** real OPs in parallel; soft planning norms ~1–7 Active paper and ~1–3 Active real over the near term (advisory only — not hard caps; not a “sole focus OP” rule). Hygiene mutex (unless force): at most one **Active** OP per **seed_name**, and at most one **Active** OP per identical **Books** symbol set — that mutex prevents duplicate attention on the same recipe/membership, not multi-portfolio operation. Inactive OPs are archive/noise. Import does not imply real-money trading or automated execution
- Operator attention priority (for **DAR** and Wv2 surfaces): (1) **Active** + **Execution Mode** `real` — capital path, non-correlated books, way forward; (2) **Active** + `paper` — keep eyes on risky or under-researched strategies/markets; (3) inactive — random noise / regime archive; human may clean, remove, or activate later
- First **Journal** on an OP **engages** it: Books + TS immutable until **Closed** or successor **Rebalance**; capital may still move via **CashEvent**. Lifecycle sketch: imported/inactive → **Active** (not engaged) → **Engaged** (any Journal) → **Closed** (optional successor A′). Shape rebalance = close A + open A′ (link successor); capital-only = CashEvent on A. **Close:** paper may soft-close; real-intent requires flat first (optional force-flatten). Same-fingerprint re-import may update only **pre-engagement** OPs. **WUT** proposes candidates; **Wv2** executes and preserves evaluation integrity
- **Daily Analysis** proposes only (**Human-Gated** fills): draft **Journals** + tasks on **Signal Date** T; **Positions** change only via **Desk Action**. Canonical EOD cadence: signal T → fill at next session open on **Fill Date** T+1 (paper path; real drafts are convenience — human supplies actual fill). Unconfirmed by the action window → **Passed Signal** (process miss) with DAR attention — especially **Active** real. Optional paper autofill and future autotrader are separate later decisions, not implied by draft creation
- Confirm may change **Fulfillment Packaging** (stock → LEAP/option/proxy) while still honoring the same signal underlying; journals remain the signal/return spine, not a broker lot mirror
- Capacity contests are resolved by the methodology/algorithm into a single **Desk Handoff** package (or algorithmic **Passed Signal**); human does not re-rank expected returns by default. Each handoff carries a **Desk Workflow** link (and Telegram/shell) for confirm + extra fields. Multi-leg packages are ordered; out-of-order confirm warns
- **Winston (Wv2 ops)** prioritizes signal-driven work for **Fulfillment** by humans (or later a separate autotrader component). It does not assume full market/OMS truth; **Human-Gated** desk is the intentional gap between signal and lot state
- Analytics are dual: **Signal Spine** (methodology / process audit) and **Booked Capital Spine** (live OP equity, risk, DAR cash). Live risk uses booked; signal-vs-fill gaps are first-class, not errors to hide
- Stops: methodology may propose default ATR stop; **Working Stop** on the **Position** is desk-current. Real-world stop-out is booked via **Stop-Out Reconciliation** (required position link + working-stop snapshot + fill; warn on gap) — Winston never assumes broker sync
- **Signaled Entry Rule** vs **Unsignaled Exit Allowance**: opens/pyramids need a Winston signal; closes may be unsignaled with reasons (stop, error, discretionary) so the booked spine stays honest about downstream fulfillment
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
> **Domain expert:** "Same **seed_name** (or identical **Books**) needs force — that mutex prevents duplicate recipe attention. Different seeds are fine: several **Active paper** and a few **Active real** OPs in parallel is the product. **DAR** should put real first, paper second, inactive as hygiene noise only."

> **Dev:** "We have five Active paper OPs and two Active real — should we deactivate down to one?"
> **Domain expert:** "No. Soft norms are ~1–7 paper and ~1–3 real. Deactivate only when attention is noise (wrong recipe, smoke residue, closed thesis) — not because multi-Active is 'dirty'."

> **Dev:** "We re-vet and re-import while Portfolio Red already has paper journals. Update the strategy params?"
> **Domain expert:** "No — any **Journal** **engages** the OP. Shape is frozen until **Closed**. Close the old series (signals no longer meaningful), then import/activate a new OP+TS for the new candidate. Otherwise risk and performance series are corrupted."

> **Dev:** "Is paper trading still 'lab'?"
> **Domain expert:** "No — lab is **WUT**. Paper in **Wv2** is operational execution without broker fills. Hygiene rules still apply."

> **Dev:** "We need to drop ROKU from an engaged Red and change the exit strategy."
> **Domain expert:** "That's a shape **Rebalance** — successor path. Close A (signals on A stop), open A′ without ROKU and with the new TS. Journals stay on A so performance isn't rewritten. Capital top-ups alone are just **CashEvents** on A. Soft-close vs flat-required follows **Execution Mode** (`paper` vs `real`), not export_kind."

> **Dev:** "Paper Red ran $20K → $45K. We want to go real with the same TS."
> **Domain expert:** "Speech: **make** Portfolio Red + that TS **real** with capital $13,986 (or make short-fp **real** …). **Capital Activation** opens real A′ with CashEvent $13,986 — not paper terminal equity. **Same fingerprint**. A′ defaults **Active** + `real`. Paper A **deactivated** by default (not Closed). If export was observation-only, **warn** in the reply — still allow; capital hygiene is the human’s job. Missing Red or TS in Wv2 → import error, not a wizard."

> **Dev:** "Add $5000 to dd653f33 — Capital Activation?"
> **Domain expert:** "No — **CashEvent** top-up on an **existing** series. **Make real** opens a new series; **add $X to** increases capital_base. Top-up is **only** for **Active real** OPs — never paper (paper lives and dies on its starting capital). Resolve fingerprint among Active real; ask if multiple; refuse paper/inactive."

> **Dev:** "Can a losing backtest still reach **Wv2**?"
> **Domain expert:** "Yes — as an **Observation Portfolio** for **Paper Trading** and regime watching. **Trade-Ready Portfolio** is the breakeven+ export path for promoted configs. Either way, import leaves the **Operational Portfolio** inactive until you explicitly activate it."

> **Dev:** "If two portfolios win the same methodology fingerprint in **WUT**, do we get two strategies in **Wv2**?"
> **Domain expert:** "In **WUT**, one fingerprinted **TradingStrategy** and two **TradingStrategy Selections**. In **Wv2**, each import still carries a display name; same fingerprint/provenance can share methodology, but two lab seeds usually still create two **Operational Portfolios** because Books/capital differ."

> **Dev:** "We re-vet Portfolio Red and get a new fingerprint. Do we overwrite the Wv2 portfolio?"
> **Domain expert:** "No — that would erase the prior regime sample. Default import **auto-forks**: new **TradingStrategy** + new **Operational Portfolio** named with a short fingerprint suffix (e.g. `Portfolio Red · a1b2c3d4`). Prior paper lineage stays. Overwrite/update-by-name only when provenance is the same fingerprint (or legacy import with no fingerprint)."

> **Dev:** "Who calculates **ATR-17**?"
> **Domain expert:** "**DM** — always. Consumers read it from **Winston EOD Standard** parquet. **WUT** used to calculate locally; that path is legacy for new work."

> **Dev:** "DA fired an IBM entrance on Jul 16 for paper Yellow. Did we buy IBM?"
> **Domain expert:** "No — **Human-Gated**. Jul 16 is **Signal Date**; you get a draft **Journal** + task. **Fill Date** is the next session (Jul 17); paper fill price is that open. Confirm (or later opt-in paper autofill) is a **Desk Action** — DA never opens the **Position**."

> **Dev:** "Same signal on a real OP — different?"
> **Domain expert:** "Still a draft for convenience. Real is always human-gated; the human states the actual fill (price/units/stop). Next-open is the EOD default story, not a forced broker print."

> **Dev:** "We import Portfolio Blue with TS fingerprint a, then again with fingerprint b. Two OPs?"
> **Domain expert:** "Yes — two **Operational Portfolios** (display e.g. `Portfolio Blue · a1b2c3d4` and `… · e5f6g7h8`). Journals for a stay on a; journals for b stay on b. Same fingerprint a again updates that series only if still pre-engagement; after any **Journal** (draft or executed) shape is locked until **Close**/successor. Engagement ignores **Active** and paper/real. Dual **Active** on the same **seed_name** still needs force — both series can exist; both Active is the special case."

> **Dev:** "Signal said long 206 ABC but I bought 2 Jan 2028 LEAP calls. Wrong journal?"
> **Domain expert:** "No — same signal; different **Fulfillment Packaging**. Confirm/book with type=leap, strike, expiry, contract units and premium. Journal still anchors ABC and the signal; cash uses multiplier."

> **Dev:** "I ignored a real Active enter through T+1. Is that a strategy pass?"
> **Domain expert:** "No — **Passed Signal** as **process miss**. DAR must flag attention. Algorithmic pass is only when rules already declined (capacity, no swap). Casual ignore is stakeholder/process error to correct, not fingerprint design."

> **Dev:** "At max markets, new XYZ beats ABC — what does the desk see?"
> **Domain expert:** "One **Desk Handoff** package from the algorithm (e.g. exit ABC + enter XYZ), each step with a **Desk Workflow** link — not a menu of six ER options. Confirm enter before exit **warns**. Human confirms fills and packaging; force/ad-hoc is the only discretionary path."

> **Dev:** "Is Winston an autotrader?"
> **Domain expert:** "No. It is a programmatic trend/methodology engine that prioritizes **Desk Handoffs** for **Fulfillment** — like a WMS for human picks. Fills are human (or a future separate automation component). Winston never assumes it has the full fulfillment picture."

> **Dev:** "We sized 206 shares but filled 2 LEAPs — which equity curve?"
> **Domain expert:** "**Booked Capital Spine** for the live OP (premium × multiplier × contracts). Keep the **Signal Spine** (206 @ next open story) for methodology/process comparison. Do not rewrite cash to synthetic stock."

> **Dev:** "Broker stopped me out of AMZN — how do I book it?"
> **Domain expert:** "**Stop-Out Reconciliation**: exit the open **Position** on that OP with reason external_stop, fill price, and required lot link + **Working Stop** snapshot on the **Booked Capital Spine**. Warn if fill diverges from working stop. Don’t invent a Winston exit signal — **Unsignaled Exit Allowance**."

> **Dev:** "I bought GGG with no DAR signal — book it?"
> **Domain expert:** "No under **Signaled Entry Rule**. Enter/pyramid only against a methodology-originated signal (DA draft journal/task or package leg), referenced on confirm. Packaging can be LEAPs. Unsignaled **exits** are allowed; unsignaled **entries** are not — force+audit only if you must break policy."

## Flagged ambiguities

- "account" can mean broker account, Portfolio, or Cromwell principal — resolved: use **Portfolio** for trading config, **Cromwell principal** for the human operator.
- "sync" is overloaded — resolved: **Data Acquisition** (DM←EODHD); **Reconciliation** (parquet→PG metadata); **Symbol Demand** (consumers→DM discovery). WUT `Operations::DataSync` (Yahoo→activities) is legacy, not the target model.
- "audit log" is overloaded — resolved: **Ecosystem Audit Log** = integration/coordination events only; monolith application errors and request logs remain local per monolith.
- "strategy" alone is overloaded — resolved: **TradingStrategy** for the reusable methodology entity; strategy class names (e.g. `Breakout20DayStrategy`) are implementation identifiers.
- "vetted" / "export" overloaded — resolved: optimization complete → **Optimization Candidate**; breakeven+ gates → **Trade-Ready Portfolio**; sub-breakeven observation → **Observation Portfolio**; Wv2 hosting → **Operational Portfolio** (may be paper-only).
- "Configured Portfolio" — resolved: legacy term; canonical name is **Trade-Ready Portfolio** (or **Observation Portfolio** when gates fail). Prefer those over “configured portfolio” in new docs.
- "ready for Wv2" vs "ready for live money" — resolved: Wv2 import elevates observation (**Paper Trading**, **Daily Analysis**); live broker execution is a later, explicit step.
- "TradingStrategy identity" across monoliths — resolved: **WUT** = content fingerprint (lab). **Handoff/Wv2** = seed label + short fingerprint suffix on display names when fingerprint is present; **full fingerprint on OP + TS** is the lineage match key (short suffix is display-only). Import: same fingerprint → update; bare seed + matching Books → adopt/rename; else auto-fork. No fingerprint (legacy) ⇒ bare-name update path.
- "Active" vs "observation" vs "live money" — resolved: **Active** = in **Daily Analysis** + human task surface. **Execution Mode** (`paper` \| `real`) is capital intent (default paper). `export_kind` is WUT economic promotion (observation vs trade_ready). All three are independent. Multi-Active across seeds is intentional (paper band + real band); force is only for same **seed_name** or identical **Books**. Sole-focus / “one Active OP” hygiene is incorrect. Wv2 tasks humans; not an end-to-end autotrader.
- "dual-Active hygiene" — resolved: not collapse to one OP. Differentiate **attention bands** (inactive / Active paper / Active real) in **DAR** and ops; soft planning norms ~1–7 paper, ~1–3 real (warn only; hard caps would need a new decision).
- "paper vs theory" / mutate-after-import — resolved: **WUT** = candidate selection lab; **Wv2** = operations. Any **Journal** **engages** an OP (immutable TS/Books/risk until **Closed**, pending explicit **Rebalance** rules). Paper journals count. Re-import must not rewrite an engaged series.
- **Rebalance** — resolved: capital → **CashEvent** in place; Books/TS shape change → successor path (close A, open A′, journals stay on A). Silent re-import must not reshape an **Engaged** OP.
- **Close preconditions** — resolved: **Execution Mode** `paper` = soft-close allowed; `real` = flat-required (force-flatten optional). Engagement lock still applies to both (any journal freezes shape).
- **Execution Mode** — resolved: explicit `paper` \| `real` on OP (default paper); not derived from Active or export_kind. Real capital starts via **Capital Activation**: new OP + new initial **CashEvent**; paper series is not auto-closed (recommended close). Never in-place capital rewrite of the paper series.
- "**Activate**" (Telegram/operator speech) — resolved: prefer “**make … real** with capital $X” for **Capital Activation**; “activate” alone often means only the **Active** attention flag. Docs use **Capital Activation**.
- **Capital Activation** defaults — resolved: new OP `real` + **Active**; same methodology **fingerprint**; paper not auto-**Closed**; default **deactivate** paper A (same seed/Books); force for dual **Active**. **export_kind** non-trade_ready → **warn**, do not hard-block (human hygiene). Source OP+TS must exist in Wv2 or hard error (import first).
- **CashEvent top-up** — resolved: “add $X to fingerprint” only on **Active real** OPs; paper never (live/die on initial capital). Distinct from Capital Activation.
- "DmCoverage" (and variants: dm_coverage, DmCoverage model/association) was used in WUT and Wv2 for the local consumer mirror of DM's metadata — resolved: converge on the canonical **DataCoverage** term everywhere. Deprecate and remove consumer-specific naming variants (DmCoverage, etc.). Consumers maintain a local **DataCoverage** (as their view of available DM parquet via Reconciliation). Glossary definition of **DataCoverage** is authoritative for the concept (DM-owned metadata describing parquet reality).
- "`activities` table" / `market.activities` (and `Activity` records) in WUT was the carrier for market time-series (OHLCV + indicators) — resolved: for DM-sourced **Market** data this is **very temporary** and deprecated. DM parquet (via **Winston EOD Standard** + **DataCoverage**) is the authoritative source. All references (positions, trading_signals, backtest_indicator_values, passed_signals, market_indicator_values, etc.) must be refactored to use composite `(market_id, date)` keys + **Bar** objects from the DM loader. No DB table row for bar identity (use composite or non-persisted derivative). No long-lived shim. Call sites for creation (e.g. Position/TradingSignal/BIV construction) and usage (risk, expected return, charts, views) updated to loader + composite. "Just use DM to pull the data again" at render time using stored (market, date). Backtest result views pull via loader from stored (market, date); backtest runs have dedicated result parquet storage. All legacy non-DM records are defunct and deprecated; there is no historical or legacy relationship that we need to curate. The `activities` table itself is deprecated for market time-series and can eventually be removed or emptied for DM symbols (and legacy paths as they are cleaned).
- The `belongs_to :activity` on Position, TradingSignal, PassedSignal, BacktestIndicatorValue, MarketIndicatorValue, MarketMovingAverage, etc. is to be removed or fully deprecated for DM-sourced data. Refactor creation and usage sites to use the composite key + Bar (from the DM loader). The association remains only for truly legacy non-DM records. However, with the integration of DM all legacy non-DM records are defunct and can be considered deprecated. There is no historical or legacy relationship that we need to curate.
- For obtaining time-series data for a **Market** (DM-sourced), the primary mechanism is direct from **Winston EOD Standard** parquet via a loader (returning Bar/ParquetBar-like objects, e.g. with market_id). The expression `market.activities` (and the `activities` table) is not supported for DM-sourced Markets. The Data Sets page becomes a pure registry view of DM's **DataCoverage**; it no longer materializes or "loads" time-series into WUT.
- "trade_date" on **Journal** — resolved conceptually as two ideas: **Signal Date** (T) vs **Fill Date** (T+1 next-session open for EOD path). Schema may still use one column until the dual-date machinery lands; do not treat a single stamp as both signal and fill without saying which.
- "DA fills / autotrader" — resolved for now: **Daily Analysis** drafts only; **Positions** change via **Desk Action** (**Human-Gated**). Real always. Paper still confirms today; next-open prefill + optional paper autofill are not built; full autotrader is a future explicit product decision, not implied by B/C roadmap talk.
- **Engaged** — confirmed **A**: any **Journal** (draft or executed) locks OP shape (Books + TS fingerprint). Unlock only **Close** or successor **Rebalance**. Same seed+fingerprint is one series (no second import of identical fingerprint as a parallel OP). Different fingerprints of the same lab seed are separate OPs and separate journal series. Independent of **Active**, paper, and real.
- Confirm window — **A**: from signal evening through **Fill Date**; next-open prefill when known; unconfirmed → **Passed Signal**. Real process misses are high-attention, not discretionary strategy.
- Signal vs fill instrument — **Fulfillment Packaging** may differ (shares vs LEAPs); journal tracks signal/returns spine.
- Capital contests — **A**: algorithm emits one deterministic package or algorithmic pass; human confirms fills/packaging. Multi-choice ER menus are non-default (force/ad-hoc discretionary).
- **Desk Workflow** — product requirement: every DAR next step links to a guided Wv2 journal/confirm path; partial today (desk form + Telegram/ops); full workflow not built.
- Multi-leg **Desk Handoff** — one logical package, N linked journals/tasks, ordered; out-of-order confirm **warns** (A).
- Winston vs fulfillment — signal/prioritization system for human (or future separate auto) **Fulfillment**; not full OMS truth; tidy end-to-end automation is not assumed.
- Equity / regime measurement — **A**: dual **Signal Spine** + **Booked Capital Spine**; live OP uses booked; gaps are visible.
- Stops — **A**: signal/default ATR + **Working Stop** on Position; human update allowed; external stop-out via **Stop-Out Reconciliation** (required position link + snapshot; warn on gap). Order lifecycle still deferred.
- Stop-Out binding — **A**: required lot link + working_stop snapshot + warn on gap (not hard-block by default).
- Enter vs exit asymmetry — entries require methodology-originated Winston **signal** (DA draft / package leg); exits may be unsignaled (stop/error/downstream miss) with reason + linkage. Free-form enter deprecated as normal ops (force+audit only).
