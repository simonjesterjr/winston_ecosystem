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
The data acquisition monolith. Owns EODHD download, parquet production, derivative calculation, reconciliation, Cromwell download notifications, and **Alt Filing** acquisition.
_Avoid_: data service, downloader (too narrow)

**Alt Filing**:
A sparse alternative-data event (Congress or insider trade, contract, etc.) acquired by **DM** and stored as a filing row — not a daily bar and not a **Daily Analysis** signal.
_Avoid_: Quiver bar, alt candle, baking Congress into Winston EOD Standard

**Quiver Skim**:
A named Winston reconstruction of a Quiver Quantitative strategy’s **current holdings** (Congress Buys, Congress Long-Short, Nancy Pelosi, Insider Purchases, House Long-Short). **DM** builds the book from Alt Filings (file date only). **WUT** stores versioned skim books and diffs (opened / liquidated / rebalanced). Not EODHD bars, not Trend Following, not a Daily Analysis signal, not the vendor’s unpublished live holdings page. Price bars for skim tickers still come from EODHD parquet.
_Avoid_: scraping quiverquant.com/strategies, calling a skim book an EODHD data set, treating a skim book as an Operational Portfolio

**Winston Quiver (WQ)**:
The operator name for the **Quiver Tracking Desk** plus its one **WQ Shadow Portfolio**. Not a new majestic monolith. Not Trend Following Daily Analysis.
_Avoid_: a fourth Rails app; treating WQ as Mint/Orange/Yellow

**WQ Shadow Portfolio**:
The single paper **Operational Portfolio** on the **Quiver Tracking Desk** whose target is an uploaded published Quiver book (PDF or TXT). Daily Analysis skips it. Funding the Quiver tracking Schwab account is **Capital Activation** of a new real series of the same recipe on a separate Broker Gateway binding from Wv2 Ops.
_Avoid_: a second Turtle OP from the same PDF; mixing this series with Mint

**Monday Rebalance Plan**:
One human-readable package built after a Quiver book ingest (Monday is the live cadence; TXT uploads anytime are test mode): exits with profit/loss, rebalances as ±% per name, and enters. Exclusive alternate: a flatten-all plan on a chosen weekday.
_Avoid_: firing flatten and rebalance in the same week; treating gap tasks as a second Approve path (tasks execute an already-approved plan)

**Plan Approve**:
The Human-Gated verb for a **Monday Rebalance Plan**: Approve or Reject the whole package (optional skip-line with reason). After Approve, the plan is **locked** (Approve disabled). Remaining ready legs execute **one at a time** via tracking tasks (Confirm books that lot). A name that cannot resolve a fill is a per-leg **HITL** flag — the rest of the plan stays approved. Live WQ Schwab write is after test cycles.
_Avoid_: silent book-from-PDF; auto-booking the whole package on Approve; treating missing fill as a plan-wide fail; auto-execute on Mint or Execution Mode real

**Quiver Tracking Portfolio**:
Synonym for the **WQ Shadow Portfolio**. Target book comes from an operator-uploaded **Quiver Snapshot PDF** or TXT, not from Daily Analysis and not from the WUT Skim reconstruction. **Daily Analysis** skips it.
_Avoid_: treating it as a TF paper OP, minting DA signals from the PDF, using the Quiver API as the holdings source, mixing fingerprints with the old 15/10 copy-book reconstruction

**Quiver Tracking Desk**:
The Wv2 page `/quiver_tracking` (public: Tailscale Serve `/wv2/quiver_tracking`) — ops-shell styling, separate route from `/operations`. PDF/TXT archive, **Monday Rebalance Plan**, Plan Approve, test blow-away, tracking blotter.
_Avoid_: stuffing tracking pending into the TF ops-shell 25-row cap

**Quiver Snapshot PDF**:
A human-downloaded (or later bot-fetched) PDF — or a test-mode TXT/CSV/JSON holdings table — of a Quiver Strategies book. Stored like a **Daily Activity Report** under Wv2 `storage/reports/quiver_tracking/`. v1 source of truth for **published** weights. Parser failures become HITL tasks, not filing reconstructions.
_Avoid_: calling DM Alt Filings a snapshot PDF; treating an unreadable PDF as an empty strategy

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
A named trading account configuration: capital, risk params, linked markets (Books), and an applied TradingStrategy. Optional **preferred color** / chart color is a presentation attribute (CSS hex, e.g. `#16a34a`) for multi-series charts and handoff JSON — not part of methodology fingerprint.
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
Risk-evaluation mode that assigns a **risk % per concurrent pyramid level** (and direction) from a configured ladder (e.g. long 2%→3%→4%→6%). Intent: scale risk into a sustained trend after ATR adds confirm continuation. Orthogonal to **Confirmational Entry** and to **Risk Scale Policy** (meta money-management). Base `risk_percentage` on a PBR is not the full story when a ladder is present. ADR-008 (ladder); do not call the ladder `risk_scale_policy`. Remains a valid Winston Unit Test mode; operator preference is **not** to use it as the live Trend Following default (lab found higher drawdown without benefit).
_Avoid_: static risk, “dynamic” alone (ambiguous with equity-curve risk), conflating OWD ladder with Kelly/meta scale, treating the ladder as required live default

**Risk Scale Policy** (meta layer):
Portfolio money-management overlay orthogonal to base risk geometry: `none` · `anti_martingale` · `martingale` · `kelly`. Applied as `scaled_pct = Engine.scale_fraction(base_pct)` where base is static or OWD/OWDC rung. Config knobs live in `risk_scale_config` (fractional Kelly, lookback, calendar recompute, Winston vs classic Kelly sizing). Default **`none`**. Methodology fingerprint includes policy+config when ≠ none; runtime mult/`n_steps` are path state only. ADR-010. Kelly is not a global trade-ready default; Martingale scale is research/paper only for real capital.
_Avoid_: treating Kelly as a peer-only `risk_evaluation_strategy` in new recipes, calling the OWD ladder “risk_scale_policy”, embedding live Kelly mult in fingerprint

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
A **Portfolio** hosted in Wv2 used for **Daily Analysis** and human tasking — past lab theory and into **execution** (paper or real). Broker fills are not end-to-end automated unless **Slate Automation** is on for that OP + **TradingStrategy** fingerprint (policy **Desk Send** of the **Session Order Slate**; **Positions** still book via **Desk Confirm** until a later accept-fill lock). One lab seed may yield multiple operational implementations (different fingerprints); each keeps its own journals/performance. When fingerprint is present, display name includes a short fingerprint suffix on first import. **WUT** is the candidate-selection lab; **Wv2** is the operational component.
_Avoid_: live portfolio (implies real money only), production portfolio (environment-specific), treating paper or an Interactive Brokers bind as automation

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
Capital injection or adjustment on the **Notional Capital** ledger of an **Operational Portfolio**. **Initial** CashEvent may land on import or **Capital Activation**. **Top-up** is for **Notional Capital** OPs that are **Active** + **Execution Mode** `real`; paper **Notional Capital** lives on initial lab/ops capital. Paper with **Broker Account Capital** (Interactive Brokers paper bound) does not use CashEvent to mimic broker net liquidation — poll the broker instead.
_Avoid_: deposit (broker term), funding event, “make real” for a top-up, CashEvent to fake DUT/Schwab balances

**Capital Authority**:
Which figure **Risk Capital** uses on an **Operational Portfolio**: **Notional Capital** (WUT-like scorekeeping) or **Broker Account Capital** (bound broker balances). Defaults: Wv2 paper + dummy_sim or Schwab-as-fulfillment-only → notional; paper bound to Interactive Brokers paper → broker; **Execution Mode** `real` → broker.
_Avoid_: deriving this from Execution Mode alone (paper can be either); putting the SoT in Broker Gateway

**Notional Capital**:
The journal ledger — CashEvents plus executed journal flows (`capital_base`). How **WUT** keeps score and how default Wv2 paper (and Schwab-backed paper) evaluates drawdown and size.
_Avoid_: treating Schwab account equity as this pile; calling it “fake” because it is not a broker print

**Broker Account Capital**:
Bound-account balances reported by a fulfillment adapter and copied into Wv2 for risk. Authoritative for **real** OPs and for IBKR **paper** when that binding is the OP’s broker; Schwab on paper is fulfillment-only, not this.
_Avoid_: Broker Gateway owning equity; silent overwrite of Signal Spine units

**Risk Capital**:
The number Winston v2 uses to size risk and judge drawdown: **Notional Capital**, or — when **Capital Authority** is **Broker Account Capital** — the bound account’s **net liquidation value**.
_Avoid_: using journal `capital_base` as a synonym when authority is broker; using net liquidation as the Daily Analysis share-count story; using settled cash as drawdown capital

**Broker Buying Power**:
The bound broker’s margin-inclusive capacity to put on more risk (Interactive Brokers field `buyingPower`). Settled cash may be negative while buying power remains; this is how a twenty-two thousand dollar equity account with minus three thousand cash can still open a position.
_Avoid_: treating settled cash as the enter gate; using the broker’s full buying power without **Leverage Guardrail**

**Leverage Guardrail**:
Winston’s cap on **gross exposure** (long market value plus short market value) versus **Risk Capital** (default two times), configured per **Operational Portfolio** with an optional **Trading Strategy** default. May be stricter than the broker. Exceeding it needs a human per-transaction override; the override still cannot spend more than **Broker Buying Power**.
_Avoid_: net long-minus-short as the ratio; assuming broker buying power is the Winston cap; baking two-times into Daily Analysis as methodology

**Spending Capacity**:
What Winston will actually allow for the next enter or pyramid: the lesser of remaining **Broker Buying Power** and remaining room under the **Leverage Guardrail**, unless a human override is on that ticket. Used after exits, then pyramids, then entries. The broker’s buying-power number is always a hard ceiling.
_Avoid_: using Spending Capacity as the drawdown denominator (that is **Risk Capital**); human override that ignores a broker reject

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
Position open/close (and free-form desk fills) require an explicit operator desk action — ops form, ops shell, or Cromwell/MCP on a human instruction — not silent mutation by **Daily Analysis** or by inbound broker confirmation evidence alone. **Execution Mode** `real` is always human-gated for **booking entries and pyramids**. **Slate Automation** may policy-**Desk Send** the **Session Order Slate** and, in discovery, **Accept-Fill** a matched protective **Working Stop** print. L1 evidence (API poll / email) may prefill or surface mismatch; other booking still requires **Desk Confirm** or **Corrective Amend**.
_Avoid_: treating draft creation as a fill, silent book-from-email or book-from-API, equating policy Send with auto-open Position, accept-fill of entries while still in discovery

**Desk Action**:
An operator-facing verb that may change lots, amend a draft, or (later) place a broker order: **Desk Confirm**, **Corrective Amend**, book ad-hoc trade, exit, stop update, and (when L3 is authorized) **Desk Send**. Surfaces: desk form, ops shell, MCP/Telegram. Confirm for the EOD path is expected by **Fill Date** (next session after **Signal Date**); unconfirmed drafts become **Passed Signals** and remain visible as attention items (especially on **Active** **real** OPs).
_Avoid_: Daily Analysis (proposes only), task alone (the reminder; Desk Action is the mutation), treating casual ignore as normal strategy, conflating Confirm with Send

**Desk Confirm**:
Book on the **Booked Capital Spine** for a **Single Fulfillment Identity** (draft → executed **Journal** / open or closed lot). Human already has a fill story (traded outside Winston, accepted a prefilled **Trade Notification**, or paper path). Does **not** place a broker order. Near-term only path when adapter bindings lack `order_write`.
_Avoid_: “confirm” meaning place-order, silent book-from-API, treating Confirm as Send under a write-capable adapter

**Desk Send**:
Explicit operator (or later policy) instruction to place an **Order Intent** via a write-capable fulfillment adapter (`order_write`). Does **not** by itself open a **Position**; booking still requires **Desk Confirm** (or a later explicit accept-fill policy). Verb stays distinct from Confirm in speech, MCP, and DAR. Not shipped until L3; absent/disabled on Manual and L1-only bindings. Parking a **Session Order Slate** is Send of that package. When **Slate Automation** is on, that Send is **policy-automatic** each session (mechanical Turtle slate); a human may halt or **Desk Pass** before the session; turning the flag off reverts to per-leg Send.
_Avoid_: overloaded Confirm-that-sends, DA place_order, auto-send pyramids on a non-enabled fingerprint, treating Active or paper as automation, equating policy Send with Desk Confirm

**Session Order Slate**:
The stop-market **Order Intents** parked before the session for one **Active** **Operational Portfolio** — initial entry, pyramid scale-in, and protective **Working Stop**. Unfilled entries and pyramids cancel at the close; protective stops stay overnight and are **replaced**, never cancel-all. Live Trend Following target once write exists; next-open remains the lab default until a **TradingStrategy** is fingerprinted on resting-touch.
_Avoid_: mixing next-open fills with a fill-relative stop from the unfilled breakout; cancel-all of live protective stops; treating the slate as Daily Analysis opening Positions

**Moment of Truth**:
The instant a parked order is eligible to fill (touch or gap). Unit size, remaining **Spending Capacity**, and **Risk Modality** are evaluated from that instant’s **Risk Capital** and **N** / Average True Range — not from the prior session’s close.
_Avoid_: sizing the live fill from last night’s close; carrying a counterfactual stop from an unfilled breakout into a next-open fill

**Unit Heat**:
Faith-style occupancy caps on open lots — per market, closely correlated, loosely correlated, single direction — that refuse a proposed enter or pyramid which would overflow. Reads the pairwise map from **Portfolio Correlation Score**; is not itself the score.
_Avoid_: using PCS as a nightly contest ranker; treating heat as expected-return ranking; silent waiver of a cap

**Slate Contest**:
How a **Session Order Slate** chooses among competing parks: **Unit Heat** refuses correlated overflow; remaining ties use Turtle buy-strength / sell-weakness (strongest long or weakest short in a group) and first-to-touch (the resting order that fills consumes remaining **Spending Capacity**). Not expected-return ranking and not a human menu.
_Avoid_: Daily Activity Report pick-lists; live expected-return swap of an open winner; ranking two parks by 4 ATR reward minus 1 ATR risk

**Slate Automation**:
An explicit flag on an **Operational Portfolio** together with its **TradingStrategy** fingerprint that opts that pair into mechanical **Session Order Slate** instructions (Turtle **Slate Contest**, **Moment of Truth** sizing) and **policy-automatic Desk Send** of that slate each session. Distinct from **Active**, **Execution Mode**, and from Daily Analysis opening **Positions**. A human may halt or **Desk Pass** before the session; the Daily Activity Report is a review, not a send click. Non-enabled OPs stay per-leg Human-Gated Send/Confirm. Winston Quiver stays **Plan Approve**. Discovery/learning: **Accept-Fill** protective Working Stop prints only; entries and pyramids still **Desk Confirm**. Whole-slate accept-fill is glossary aspiration only — not a scheduled promotion; it waits for a later grill.
_Avoid_: implying automation from paper, Interactive Brokers binding, or Active; autotrader as a second monolith; silent Send on a fingerprint that is not enabled; policy Send as auto-open Position; jumping to whole-slate accept-fill because “soon”

**Accept-Fill**:
Policy that books a matched **Trade Notification** onto the **Booked Capital Spine** without a human Confirm click. Discovery/learning under **Slate Automation**: filled protective **Working Stops** only (**Stop-Out Reconciliation**, warn on gap). Entries, pyramids, orphans, mismatches, and extra-modal packaging surprises stay Confirm. Whole-slate accept-fill is not scheduled and is not implied by paper rehearsal — it waits for a later grill.
_Avoid_: silent invent of unmatched prints; accept-fill of entries in discovery; treating broker NLV movement as a booked lot; promoting to whole-slate accept-fill on a calendar

**Desk Handoff**:
A deterministic next-step package from **Daily Analysis** / **DAR** for one **Operational Portfolio**: what to do, why (signal + **Slate Contest** / **Unit Heat** reason), and a deep link into a **Desk Workflow** (Wv2 page) plus Telegram/shell phrases. Multi-leg packages (e.g. exit ABC then enter XYZ) are **one logical handoff** with **N linked Journals/tasks**, ordered; confirming out of order **warns** (and may refuse enter while capacity still full). Human may ignore links; ignoring past the action window is a **process miss**, not a strategy choice. **Slate Contest** is Turtle-mechanical; human supplies confirmation and **Fulfillment** details Winston may not fully know.
_Avoid_: open-ended alternative menus as the default, next step without a confirm path, silent out-of-order multi-leg confirms, expected-return menus as the handoff

**Desk Workflow**:
The guided Wv2 UI path that walks a human through one **Desk Handoff** / **Journal** (review signal, next-open prefill, units/price/stop, packaging, **Desk Confirm**; optional evidence match; later optional **Desk Send** when `order_write` is live). Target product surface; today only partially supported (`/operations/desk` prefill, ops panels, Telegram/MCP phrases) — not a full journal workflow app yet.
_Avoid_: assuming Telegram alone is the complete desk, dead `resources :journals` without controller, one button that means Confirm-or-Send by mode alone

**Fulfillment**:
How humans (or a future separate automation component) actually realize a Winston signal in the market — broker fills, LEAPs, partial size, delays, clearing failures. **Winston** is the **signal and prioritization system** (trend/methodology evaluation, deterministic desk work queue) — analogous to a warehouse management system prioritizing picks for human workers — not the assumption of complete fulfillment truth. Journals bridge signal → reported fill; they do not claim OMS completeness.
_Avoid_: equating Winston with a broker OMS, assuming DA state equals market state, baking autotrader into DA

**Trade Notification**:
Normalized inbound evidence of a broker trade or order outcome (fill, partial, cancel, reject) from an adapter poll or later stream — not Signal Spine truth. Used to prefill, match, or surface mismatch against a **Single Fulfillment Identity**; booking still requires **Human-Gated** **Desk Action**. Missing expected notifications after the action window is **attention** (DAR / Telegram), resolved via human attach/link workflow — not silent invent and not email-as-primary SoT.
_Avoid_: treating broker email alone as capital SoT, auto-executing Positions from notifications, equating notification with DA signal

**Confirmation Intake**:
L1 product workflow: authenticate adapter → poll/read order and transaction evidence → normalize/store **Trade Notifications** → match to **Single Fulfillment Identity** → prefill or attention → human **Desk Confirm** or **Corrective Amend**. First-ship adapter capabilities: `auth` + `txn_read` + `order_read` only (no `order_write`). L2 `position_read` / `balance_read` feed **Risk Capital** when **Capital Authority** is **Broker Account Capital**; they remain hints when authority is **Notional Capital**. Transport/poll lives in **Broker Gateway**; match/prefill/book and **Risk Capital** persistence stay in Winston v2 (Wv2).
_Avoid_: naming a capability `order_confirm` (collides with Desk Confirm); silent book-from-intake; treating broker balances as Signal Spine units

**Broker Gateway**:
Majestic monolith that owns external fulfillment **transport** and the durable **Winston Broker Evidence Standard**: OAuth/session, adapter registry keys and **CapabilityProfile**, poll/refresh jobs, append-only evidence events (orders/fills/status), optional rebuildable snapshots, raw payload refs, and a **minimal ops UI** (bindings, registry, auth health, ingest logs). Same composition pattern as **data_manager (DM)**: API commands to do work, files as evidence truth, PG as registry/cursors/status. May store broker activity **Winston never initiated** (orphans) for later match. Does **not** own journals, stack-rank, **Risk Capital** policy, or **Desk Confirm** / **Desk Send** policy. Secrets isolated from the Wv2 process. Repo: `broker_gateway/` (compose `broker_gateway` host **:3003**).
_Avoid_: putting broker OAuth in Wv2 as primary home; gateway as desk/OMS; equating gateway with Cromwell; shared PG with Wv2; BG as the OP equity ledger

**Fulfillment adapter keys (L1):**
- **`manual`** — zero-IO escape hatch inside **Wv2** only (no BG call); human types fill.  
- **`dummy_sim`** — **default for paper OPs** and always-on L1 rehearsal: BG synthesizes order/txn evidence; Wv2 still runs Confirmation Intake (match → prefill → human **Desk Confirm**). Never live broker credentials; never `order_write`.  
- **`schwab_trader_api`** — live (or fixture) **read** for real OPs; write only under a fulfillment-write ADR.  
- **`interactive_broker_trader_api`** — Interactive Brokers Web API / Client Portal Gateway **read**; fixtures by default; live GET gated by `BG_IBKR_LIVE_READ`; CPGW **tickle** keep-alive; write off at L1. Paper vs live are **bindings** (`env=sandbox` DUT paper vs `env=live`), same adapter class. WQ talks only to Broker Gateway. Dummy_sim remains Winston-internal paper.  
Paper may still choose `manual` explicitly; product default for paper intake practice is **`dummy_sim` through BG**.

**Winston Broker Evidence Standard**:
Versioned, human-readable file contract owned by **Broker Gateway** for broker order/fill lifecycle truth (primary: append-only JSONL events with idempotency keys; optional per-entity snapshots rebuildable from the log). Consumers (Wv2 **Confirmation Intake**) read via API and/or mount; they do not write the evidence store. Orthogonal to **Winston EOD Standard** (market bars). Interface: `interfaces/winston-broker-evidence-standard.md`.
_Avoid_: proprietary binary blobs; mutable status-only files with no event log; requiring a Winston journal id before an event may be stored

**Single Fulfillment Identity**:
For one signal leg (draft **Journal** + task / package leg) there is exactly one fulfillment work item humans open for that work. Confirm ends the **draft** phase, not the identity of the row. Later price/qty/stop corrections use **Corrective Amend** on that same journal/lot — never a silent second open against the same signal.
_Avoid_: re-enter to “fix price”, treating each Desk Action as a new lot, second book as the normal correction path

**Corrective Amend**:
A **Desk Action** that rewrites price, units, stop, and/or notes on an **already executed** enter/pyramid **Journal** and its open **Position** (same lot), with an amendment audit trail. Used for fill corrections (e.g. asked open 109.89, got 109.53). Distinct from draft edit pre-confirm, from **CashEvent** capital-only adjustment, and from close+reopen (reserved for true cancel/re-trade or accidental duplicate cleanup).
_Avoid_: second ad-hoc enter, superseding correction journals as the default, CashEvent as a silent second book

**Signal Spine**:
What the fingerprint / **Daily Analysis** recommended for an OP (signal side, direction, methodology sizing, expected-return story, algorithmic pass/swap reasons) — retained for methodology and process audit even when **Fulfillment** differs.
_Avoid_: discarding signal size story when packaging differs

**Signal-Path Operational Lot**:
While a position is open, Winston v2 tracks the methodology path **as operational truth** in signal units (e.g. long 210 IBM through entrance → stop → pyramid → exit): journals, Working Stop story, and capacity occupancy follow that path. Daily Analysis **drafts** the next pyramid in those units; other **Risk Modalities** are evaluated in parallel; how the add is filled is **Fulfillment Packaging Policy**. Extra-modal packaging is **linked**, not a continuous rewrite of this path.
_Avoid_: retargeting DA/Books to LEAP symbols; treating packaging as a different signal; sizing the draft pyramid from option premium alone

**Fulfillment Link**:
Attachment of real-world packaging or broker evidence to a signal / **Single Fulfillment Identity** (“fulfillment A is for signal S”), optionally with an **indicated capital adjustment** ±$D. Does not by itself rewrite mid-life signal-path sizing; application of ±$D is via **Exit Capital Reconcile** (or explicit later apply).
_Avoid_: silent capital rewrite from packaging; unlinked substitute trades

**Exit Capital Reconcile**:
At position exit (or explicit reconcile gate), compare **Signal-Path Operational Lot** economics to linked fulfillments and apply a **CashEvent** adjustment so household cash honesty lands on **actual fulfillment profit**, not the signal-path proxy. Human-Gated propose/confirm for v1. Worked shape: signal long 210 IBM @ 287.33 (notional −$60,339.30) vs 2 LEAP calls @ $2,700 ($5,400 out); exit IBM $300 → signal-path profit ~+$2,661, LEAPs sold @ $3,400 ($6,800 in) → actual profit +$1,400; CashEvent shifts capital from the ~+$2,661 path result to +$1,400 (delta ≈ −$1,261). Mid-life only **indicates** the packaging gap; application waits for this gate.
_Avoid_: continuous LEAP mark-to-market as capital_base every bar (unless later product), using CashEvent as a second book, leaving capital on signal-path profit after exit when packaging differed

**Booked Capital Spine**:
Executed **Journals** / **Positions** / **CashEvents** as fulfillment identity; when **Capital Authority** is **Notional Capital**, also the OP equity ledger. When authority is **Broker Account Capital**, **Risk Capital** follows polled broker balances and this spine stays the journal/lot story (plus **Exit Capital Reconcile** for extra-modal honesty).
_Avoid_: rewriting Signal Spine; using this spine as Risk Capital under broker authority; using broker NLV as DA share counts

**Working Stop**:
The stop price Winston treats as current on an open **Position** on the **Booked Capital Spine** (`updated_stop` / desk-updated). May start from methodology ATR default (signal/default stop) and then diverge via **Desk Action**. Winston does not assume the broker’s resting order matches this value.
_Avoid_: broker stop alone as SoT, assuming DA knows live exchange stops

**Stop-Out Reconciliation**:
Desk workflow when real-world **Fulfillment** exits a lot because a stop was hit (or should have been): book an exit **Journal** **required-linked** to the open **Position**, storing a snapshot (working_stop_at_exit, fill_price, gap) with reason (e.g. external_stop). **Warn** (do not hard-block by default) when fill diverges from **Working Stop**. No Winston exit signal is invented. Under **Slate Automation** in discovery, a matched protective-stop **Trade Notification** **Accept-Fills** this path so **Unit Heat** is not left holding a ghost lot; without that flag, a human Confirm books it.
_Avoid_: ad-hoc exit with no position/stop provenance, treating external stop as unrelated to the Winston lot, silent large gaps, leaving the lot open after a parked stop printed

**Signaled Entry Rule**:
No **Position** open (enter/pyramid) on an **Operational Portfolio** without a **methodology-originated** Winston signal on the **Signal Spine** — primarily a **Daily Analysis** draft enter/pyramid **Journal** + task (or a leg of an algorithm **Desk Handoff** package) for that OP and underlying. Confirm/book may change **Fulfillment Packaging**, size, and price but must reference the signal (`signal_journal_id` / task). Naked free-form enter is out of policy; force + audit is the only exception path. (Today’s ad-hoc book-enter tools are transitional and should converge on this rule.)
_Avoid_: ad-hoc enter as the normal path, inventing fills with no signal provenance, treating any enter journal as self-authorizing signal

**Unsignaled Exit Allowance**:
Exits **may** occur without a Winston exit signal — stops, clearing/broker errors, downstream misses, discretionary flatten — booked on the **Booked Capital Spine** with reason codes and, when closing a known lot, position linkage (**Stop-Out Reconciliation** when stop-related). Asymmetry is intentional: entries are methodology-gated; exits must reflect market reality Winston may not have seen.
_Avoid_: requiring a DA exit signal before any close, inventing fake exit signals to “make the ledger tidy”

**Passed Signal**:
A signal that did not become an executed fill. Kinds: **algorithmic** (capacity/rules: e.g. max markets, no valid swap); **process miss** (human did not confirm by the action window / **Fill Date** — stakeholder/process error, high attention on **Active** real); **Desk Pass** (`human_pass` / desk_pass — intentional human skip of a ranked handoff among **current** desk work, with **required reason** + audit, e.g. pass pyramid A to act on entry D). Desk Pass is not free-form enter-any-market and never waives capacity. Casual ignore without reason remains process miss, not Desk Pass.
_Avoid_: cancel as silent success, unlabeled skip, treating Desk Pass as naked enter permission, capacity waiver

**Fulfillment Packaging**:
How a signal is realized in the market under **Extra-Modal Fulfillment**: the real instrument and size may differ from the **Signal Spine** / **Signal-Path Operational Lot** share story. Examples: equity signal → stock shares, LEAP/option contracts, or option-chain structure; commodity / futures-theme signal → futures, options on futures, or commodity/levered ETFs (e.g. CLETF-class products). The **Journal** (and OP **Books**) still track the **signal Market** for DA, capacity, and mid-life path; packaging is recorded via **Fulfillment Link** with optional indicated ±$D; **Exit Capital Reconcile** applies cash honesty. Does not waive the **Signaled Entry Rule**; does not invent a second signal for the fill instrument.
_Avoid_: requiring the fill instrument to equal the signal share count or symbol; rewriting Signal Spine to match broker prints; equating broker symbol match with signal identity; continuous mid-life capital = LEAP premium unless reconciled

**Fulfillment Packaging Policy**:
Winston v2 rules, stored on the **Operational Portfolio**, for how a desk may realize a signal (shares as-printed, round to a round lot, long-dated calls or puts, ask the human for a per-share price, and so on). Edited in Winston v2 operations. Rule-based now; later an LLM may propose among allowed shapes and compare them (for example a long-dated-call entrance versus a calendar option spread) without a new **TradingStrategy** fingerprint. A desk (Quiver Tracking versus Trend Following operations) only supplies the default when the portfolio is created. **Broker Gateway** only classifies evidence. Packaging may differ by **Desk Action** on the same lot (entrance in long-dated calls, pyramid in shares). Split broker executions still sum to one command.
_Avoid_: putting packaging choice in the gateway; one packaging frozen for the whole life of the lot; a second Daily Analysis signal for the fill symbol; treating a later packaging bakeoff as a different Trading Strategy fingerprint

**Risk Modality**:
One measurement of risk on an open lot — share-equivalent **Signal-Path Operational Lot**, cash-at-risk of the packaged instrument, per-share price of the underlying, or an option structure — so the same position can be evaluated in more than one way at once. Daily Analysis still drafts pyramid size from the signal-path share units; the human or **Fulfillment Packaging Policy** chooses the fill shape of that add.
_Avoid_: collapsing extra-modal packaging into a single share count; treating a later pyramid’s shares as if the entrance were also shares; using only option premium or only signal units as the whole risk picture; hiding cash-at-risk when the draft is in shares

**Extra-Modal Fulfillment**:
Realizing a Winston **signal** with one or more market instruments that are **not** the same modality as the signal’s **Market** (or not a 1:1 share print of that market) — asynchronously and often with different size, timing, and Greek/notional risk. Signal↔fulfillment linkage is mandatory for enter/pyramid (**Signaled Entry Rule**); DA continues to evaluate the signal Market on the OP. Matching a **Trade Notification** to a signal must not require `broker.symbol == Book.symbol` — prefer explicit link, underlying-aware soft match, or human pick. Orthogonal to process miss and to broker choice.
_Avoid_: “substitute trade” without signal link; replacing the Book with the fill symbol for DA; symbol-equality-only match; treating LEAP/OCC as a different methodology signal

**Daily Analysis**:
Wv2's scheduled or triggered evaluation of **Active** Portfolios — signals, **draft** journals, tasks, **Passed Signals**, Cromwell/**DAR** notification. May create draft enter/exit **Journals** for paper and real as convenience; never opens or closes **Positions** (ADR-009). Capacity and rank rules (**Unit Heat**, **Slate Contest**) should yield **deterministic** recommendations or algorithmic passes — not open-ended “human pick among expected returns” menus from Winston. Live ops do not rank contests by expected return (Winston Unit Test expected-return cycles remain lab/audit). Requires a linked **TradingStrategy**; portfolios without one are skipped (`no_strategy`). Requires DM parquet for all Books; any missing symbol skips the whole Portfolio (`missing_data`). Unknown strategy class names skip with `unsupported_strategy`. Idempotent per (portfolio, date). DM fetch is lazy (triggered when analysis finds missing parquet).
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
A versioned 0–100 composite summarizing diversification quality of a **Portfolio**’s **Books**. Primary driver is worst pairwise absolute correlation (max \|r\|) and high-pair count; mean pairwise \|r\| is secondary. Used for lab build acceptance, handoff provenance, operational time-series monitoring, and as the source of the pairwise map that **unit heat** (L2/L3) reads. **Not** a **TradingStrategy** performance metric and **not** keyed by fingerprint. **WUT** is the system of record that computes and stores the score time series; **Wv2** stores a durable copy of every evaluation (keyed by Books membership / seed name) and must not recompute a parallel formula.
_Avoid_: correlation alone (ambiguous with pairwise r or audit Correlation ID), diversification rating alone (UI label without time series), mean correlation alone (can be diluted by junk series), recomputing divergent formulas in Wv2 without WUT, tying PCS to a TradingStrategy or Operational Portfolio id, using PCS as the nightly contest ranker (that is **Unit Heat** + **Slate Contest**)

**Correlation Snapshot**:
A point-in-time record of a **Portfolio Correlation Score** plus transparent components (max \|r\|, mean \|r\|, high pairs, date window, methodology version) and the compact pairwise map used by heat L2/L3. Produced by **WUT**; copied into **Wv2** on every evaluation (push + Daily Analysis pull) and at handoff import. Ops identity is **Books** (sorted symbol key) plus seed name — one Mint book set shares one series across every OP/TS on those names.
_Avoid_: sidecar alone (build artifact; snapshot is the durable observation), heatmap alone (visual, not the stored score), storing the pair map only on a TradingStrategy row

**Correlation Methodology Version**:
An immutable recipe identifier for how **Portfolio Correlation Score** and build constraints are computed (windows, quality gates, max-pairwise cap, weights). Changing the recipe requires a new version; historical snapshots keep their original version.
_Avoid_: strategy fingerprint (that is **TradingStrategy** identity), algorithm alone (too vague)

**Daily Activity Report (DAR)**:
The operator-facing Wv2 daily narrative (markdown/PDF) of a **Scored Session** after **Daily Analysis**. Primary job: make human attention unmistakable by **attention band** — **Active** + **Execution Mode** `real` first (capital at risk), **Active** + `paper` next (strategy/market learning), inactive only as a short hygiene/noise appendix when useful. Carries status, next steps, desk handoffs, equity context, and (when present) **Portfolio Correlation Score** time series. For an OP with **Slate Automation**, the DAR is a **review** of the session — which Working Stops / levels moved, what Turtle **Slate Contest** priorities come next — so a human may halt or Desk Pass if necessary; it is not a nightly approve-to-park menu. Preferred publish ~16:30 America/Denver; lateness until ~17:00 is acceptable. Must not be written as a quiet **Hold** when the session is **Not Scored**.
_Avoid_: daily analysis alone (the job; DAR is the report), treating a clock-fired skip as a DAR, flat “all Active” list with no paper/real split, Cromwell notification alone (transport payload; DAR is the human document), using the DAR as an expected-return pick-list

**Scored Session**:
A New York equity session whose Active Trend Following Operational Portfolios were actually evaluated against that session’s exact bars. A DAR **Hold** is valid only after a Scored Session.
_Avoid_: calling a missing_data skip a scored day; using calendar Saturday/Sunday as a session date

**Not Scored**:
Daily Analysis did not evaluate Active Trend Following books for that session (typical cause: no exact session bar). Must not be presented as “no next actions.” Catch-up evaluation when bars arrive mints desk tasks; it does not require a replacement DAR.
_Avoid_: Hold, quiet day, skipped-as-success

**Hold** (DAR):
A Scored Session that produced no actionable next steps after recipes and heat/capacity. Operator may treat the desk as quiet for that session.
_Avoid_: using Hold for Not Scored / missing_data skips

**Mid-month Scoreboard (MMS)**:
The operator-facing Wv2 **monthly business review** (markdown/PDF + `mid_month_scoreboards` publication row) of paper/real **Operational Portfolios**: take vs **Passed Signals**, entries/exits, Portfolio Correlation Score, period return / drawdown / Sharpe, and a scored operating grade. Generated by Wv2 Sidekiq at beginning of day (06:00 America/Denver) on the **third Wednesday**. Not a Daily Analysis; not a lab Portfolio Backtest Run. Paper results remain a **regime heuristic** for a fingerprint.
_Avoid_: treating MMS as a promotion stamp; mixing smoke/test books into the score; using one-month Sharpe as if it were a multi-year PBR; Cromwell generating the numbers (Cromwell may fetch/attach the PDF only)

## Relationships

- A **Portfolio** has many **Books** (one per **Market**)
- A **Portfolio** applies one **TradingStrategy** (loose coupling — strategy is a separate entity)
- **DM** produces **Winston EOD Standard** parquet per **Market**; **Consumers** (WUT, Wv2) read it
- **DM** owns **Alt Filings** (Quiver and later vendors); WUT/Wv2 read them via DM and never hold the vendor API key
- A **WQ Shadow Portfolio** in **Wv2** tracks a **Quiver Snapshot PDF** or TXT. **DM** supplies parquet. **Quiver Skim** in **WUT** remains lab-only. Tracking is skipped by **Daily Analysis**. Ingest builds a **Monday Rebalance Plan**; **Plan Approve** then auto-executes at-market on dummy_sim (test) or, later, the WQ Schwab binding. Broker Gateway dummy_sim sandbox fills are the test path; live Schwab write is after test cycles.
- **DM** maintains **DataCoverage** metadata that reflects parquet reality after **Reconciliation**
- **Broker Gateway** owns adapter transport and the **Winston Broker Evidence Standard** (files + API); **Wv2** owns **Confirmation Intake** match/prefill, **Desk Confirm** / later **Desk Send**, journals, **Capital Authority**, and **Risk Capital** — same split pattern as **DM** (parquet + API) vs consumers
- **WUT** runs **Portfolio Signal Optimization** → **Optimization Candidate** → validation backtest → fingerprinted **TradingStrategy** + **TradingStrategy Selection** → (viability gates) → **Trade-Ready Portfolio** JSON *or* **Observation Portfolio** JSON → **Wv2** imports an **Operational Portfolio** + **CashEvent** + linked **TradingStrategy**
- Handoff JSON may carry fingerprint / WUT TS id as **provenance**. When fingerprint is present, **Operational Portfolio** and **TradingStrategy** display names always include a **short fingerprint suffix** (e.g. `Portfolio Red · a1b2c3d4`) — including the first import. **Lineage match key** is the full fingerprint (stored on both OP and TS), not reconstructed display name. Import resolution: (1) same fingerprint → update that pair; (2) no fingerprint match, bare seed-name OP exists **and** Books symbols match → **adopt** (attach fingerprint, rename to suffix form, update); (3) else → **auto-fork** new OP+TS. Legacy JSON with no fingerprint may still update by bare seed name
- Performance of an **Operational Portfolio** under **Paper Trading** is a **regime heuristic** for that **TradingStrategy** fingerprint, not a property of the lab seed name alone
- Import always lands **Operational Portfolios** inactive regardless of `export_kind`; missing `export_kind` is treated as **Observation Portfolio**. Explicit **Active** selects which OPs enter **Daily Analysis** and the human attention queue. **Multi-Active is product intent:** run several **Active** paper OPs and a smaller set of **Active** real OPs in parallel; soft planning norms ~1–7 Active paper and ~1–3 Active real over the near term (advisory only — not hard caps; not a “sole focus OP” rule). Hygiene mutex (unless force): at most one **Active** OP per **seed_name**, and at most one **Active** OP per identical **Books** symbol set — that mutex prevents duplicate attention on the same recipe/membership, not multi-portfolio operation. Inactive OPs are archive/noise. Import does not imply real-money trading or automated execution
- Operator attention priority (for **DAR** and Wv2 surfaces): (1) **Active** + **Execution Mode** `real` — capital path, non-correlated books, way forward; (2) **Active** + `paper` — keep eyes on risky or under-researched strategies/markets; (3) inactive — random noise / regime archive; human may clean, remove, or activate later
- First **Journal** on an OP **engages** it: Books + TS immutable until **Closed** or successor **Rebalance**; capital may still move via **CashEvent**. Lifecycle sketch: imported/inactive → **Active** (not engaged) → **Engaged** (any Journal) → **Closed** (optional successor A′). Shape rebalance = close A + open A′ (link successor); capital-only = CashEvent on A. **Close:** paper may soft-close; real-intent requires flat first (optional force-flatten). Same-fingerprint re-import may update only **pre-engagement** OPs. **WUT** proposes candidates; **Wv2** executes and preserves evaluation integrity
- **Daily Analysis** proposes only (**Human-Gated** fills): draft **Journals** + tasks on **Signal Date** T; **Positions** change only via **Desk Action** or discovery **Accept-Fill** of a matched protective stop. Lab / paper default cadence remains signal T → next session **open** on **Fill Date** T+1 (ADR-009). Live Trend Following target (Grill 2026-09-01 Q7–Q10): after the bar is final, park a **Session Order Slate** of stop-market orders before the session; evaluate risk at the **Moment of Truth**; unfilled entries/pyramids cancel at the close; protective **Working Stops** replace overnight. Do not run that live loop against a **TradingStrategy** scored on next-open. Parking the slate is **Desk Send** of the package; **Slate Automation** (opt-in per OP + fingerprint) makes that Send policy-automatic. v1 / L1 stays Confirm + evidence until write exists. Unconfirmed by the action window → **Passed Signal** (process miss) with DAR attention — especially **Active** real. **Daily Analysis** runs only after Active Trend Following books have that session’s exact bars (**Scored Session**); a DAR **Hold** is invalid if the session is **Not Scored** (ADR-012). Preferred times yield to that gate; catch-up mints tasks onto the current desk without requiring a new DAR
- Confirm may change **Fulfillment Packaging** under **Extra-Modal Fulfillment** while still honoring the same signal **Market** and direction; mid-life **Signal-Path Operational Lot** keeps signal units for Daily Analysis market identity, capacity occupancy, and the **draft** pyramid size; **Risk Modality** evaluation also shows cash-at-risk of the packaging, per-share price, and option structure; the human or **Fulfillment Packaging Policy** chooses how that add is filled (shares, more calls, a spread); **Fulfillment Link** records packaging + indicated ±$D; **Exit Capital Reconcile** applies CashEvent honesty. Journals are not a broker lot mirror.
- **Single Fulfillment Identity** per signal leg: one draft → confirm → optional **Corrective Amend** on the same lot. Re-enter against a completed signal is refused by default (force + notes only)
- Capacity contests are resolved by **Unit Heat** (refuse correlated overflow) and **Slate Contest** (buy-strength / sell-weakness, first-to-touch) into a single **Desk Handoff** package (or algorithmic **Passed Signal**). Live ops do not rank by expected return; Winston Unit Test expected-return cycles stay lab/audit. Human does not pick from an expected-return menu. Human may **Desk Pass** a ranked handoff (required reason) to act on another **current** handoff only — not free-form markets. **Slate Automation** is opt-in per Operational Portfolio + TradingStrategy fingerprint and **policy-automatic Desk Send** of the mechanical slate; the Daily Activity Report for those pairs is a review (moved stops/levels, Turtle priorities), not a rank gate or a send click. Each handoff carries a **Desk Workflow** link (and Telegram/shell) for confirm + extra fields. Multi-leg packages are ordered; out-of-order confirm warns. Discovery **Accept-Fill** books matched protective Working Stop prints only; entries and pyramids stay Confirm; whole-slate accept-fill waits for a later grill (not a scheduled promotion).
- **Winston (Wv2 ops)** prioritizes signal-driven work for **Fulfillment** by humans (or later a separate autotrader component). It does not assume full market/OMS truth; **Human-Gated** desk is the intentional gap between signal and lot state
- Analytics: **Signal Spine** (methodology / process); **Signal-Path Operational Lot** (mid-life ops truth in signal units); **Booked Capital Spine** after reconcile (cash honesty). Gaps are first-class, not errors to hide
- Stops: methodology may propose default ATR stop; **Working Stop** on the **Position** is desk-current. Real-world stop-out is booked via **Stop-Out Reconciliation** (required position link + working-stop snapshot + fill; warn on gap). Under **Slate Automation** in discovery, a matched parked protective-stop print **Accept-Fills** that path so Unit Heat is not a ghost lot. Winston never assumes broker sync without that match.
- **Signaled Entry Rule** vs **Unsignaled Exit Allowance**: opens/pyramids need a Winston signal; closes may be unsignaled with reasons (stop, error, discretionary) so the booked spine stays honest about downstream fulfillment. Desk default: **intent-first** for signaled enters; **trade-first** (life/broker then book) for stop-outs and other unsignaled exits
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

> **Dev:** "The DAR says hold, 0 next actions. Quiet day?"
> **Domain expert:** "Only after a **Scored Session**. If Active books skipped for missing session bars, that is **Not Scored** — wait or catch-up; do not treat it as no trades."

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
> **Domain expert:** "No — same signal; **Extra-Modal Fulfillment** / different **Fulfillment Packaging**. Confirm/book with type=leap, strike, expiry, contract units and premium. Journal still anchors ABC and the signal for Daily Analysis; cash and booked returns use option premium × multiplier. **Fulfillment Packaging Policy** in Winston v2 chose (or allowed) that shape; Broker Gateway only reported option prints."

> **Dev:** "Commodity Book is on a futures-theme Market but I filled with a CLETF and later rolled into options. Does DA switch to the ETF symbol?"
> **Domain expert:** "No. DA keeps evaluating the signal **Market** on the **Book**. Link each booked fill to the signal; equity and cash follow the ETF/options packaging on the **Booked Capital Spine**. Do not re-book the OP’s Books to chase fill symbols."

> **Dev:** "I ignored a real Active enter through T+1. Is that a strategy pass?"
> **Domain expert:** "No — **Passed Signal** as **process miss**. DAR must flag attention. Algorithmic pass is only when rules already declined (capacity, no swap). Casual ignore is stakeholder/process error to correct, not fingerprint design."

> **Dev:** "At max markets, new XYZ beats ABC — what does the desk see?"
> **Domain expert:** "One **Desk Handoff** package from the algorithm (e.g. exit ABC + enter XYZ), each step with a **Desk Workflow** link — not a menu of six ER options. Confirm enter before exit **warns**. Human confirms fills and packaging; force/ad-hoc is the only discretionary path."

> **Dev:** "Is Winston an autotrader?"
> **Domain expert:** "No. It is a programmatic trend/methodology engine that prioritizes **Desk Handoffs** for **Fulfillment** — like a WMS for human picks. Fills are human (or a future separate automation component). Winston never assumes it has the full fulfillment picture."

> **Dev:** "Winston Quiver paper on Interactive Brokers dummy DUT — is the two thousand dollar CashEvent still Risk Capital?"
> **Domain expert:** "No. That Operational Portfolio’s **Capital Authority** is **Broker Account Capital**. **Risk Capital** is polled **net liquidation value**. Dummy-sim or Schwab-backed paper stays **Notional Capital** (Winston Unit Test–like). Live is broker."

> **Dev:** "Equity twenty-two thousand, cash minus three thousand — can we still enter?"
> **Domain expert:** "Yes if **Broker Buying Power** and the **Leverage Guardrail** still have room. Settled cash is not the gate. Gross long-plus-short counts toward two times **Risk Capital**. A human may override the Winston cap on that ticket; they cannot override a broker buying-power reject."

> **Dev:** "We sized 206 shares but filled 2 LEAPs — which equity curve mid-life?"
> **Domain expert:** "**Signal-Path Operational Lot** still tracks the 206-share path for Daily Analysis market identity and capacity. **Risk Modality** also shows cash-at-risk of the calls (and later a calendar-spread alternative). **Fulfillment Link** the calls with indicated cash gap. On exit, **Exit Capital Reconcile** applies CashEvent honesty. Do not retarget Books to the option symbol. A later pyramid on that lot may be shares under the same **Fulfillment Packaging Policy**."

> **Dev:** "Where do I set ‘round to a round lot, else ask me the per-share price’?"
> **Domain expert:** "On the **Operational Portfolio** in Winston v2 operations — that is the **Fulfillment Packaging Policy**. Rule-based now; later an LLM may compare allowed shapes. Broker Gateway does not own this."

> **Dev:** "Entrance was 2 LEAPs; a pyramid fires. How many shares does Daily Analysis write?"
> **Domain expert:** "The draft add is in **Signal-Path Operational Lot** share units. Show cash-at-risk of the calls (and other **Risk Modalities**) on the same ticket. Fill as shares or more calls per **Fulfillment Packaging Policy**. Do not size the draft from option premium alone, and do not assume One-Way Dynamic Risk is the live ladder."

> **Dev:** "Signal last night at 110, 2 ATR stop 102, next open 100 — buy the open and keep stop 102?"
> **Domain expert:** "No. Lab next-open would enter at 100 with a fill-relative stop. Live Trend Following parks a **Session Order Slate** (buy-stop 110) and evaluates risk at the **Moment of Truth**. Mixing the two is rejected."

> **Dev:** "One unit left, crude and gold both want a pyramid — which expected return wins?"
> **Domain expert:** "Neither. **Unit Heat** refuses if they are correlated overflow. If both still fit, **Slate Contest** is buy-strength / sell-weakness and first-to-touch. Expected return stays lab/audit, not the picker."

> **Dev:** "Mint is paper on Interactive Brokers — is it an autotrader now?"
> **Domain expert:** "Only if **Slate Automation** is on for that Operational Portfolio + TradingStrategy fingerprint. Then the **Session Order Slate** is mechanical Turtle instructions and **Desk Send** is policy-automatic. The Daily Activity Report is a review of moved stops/levels and priorities so a human may halt or Desk Pass. Daily Analysis still does not open Positions. Booking fills is still **Desk Confirm** until accept-fill is locked. Winston Quiver stays Plan Approve."

> **Dev:** "Broker stopped me out of AMZN — how do I book it?"
> **Domain expert:** "**Stop-Out Reconciliation**: exit the open **Position** on that OP with reason external_stop, fill price, and required lot link + **Working Stop** snapshot on the **Booked Capital Spine**. Warn if fill diverges from working stop. Don’t invent a Winston exit signal — **Unsignaled Exit Allowance**. If **Slate Automation** is on and the parked protective stop matched, **Accept-Fill** books that path so tomorrow’s slate does not pyramid a ghost. Entries and pyramids still Confirm in discovery."

> **Dev:** "I bought GGG with no DAR signal — book it?"
> **Domain expert:** "No under **Signaled Entry Rule**. Enter/pyramid only against a methodology-originated signal (DA draft journal/task or package leg), referenced on confirm. Packaging can be LEAPs. Unsignaled **exits** are allowed; unsignaled **entries** are not — force+audit only if you must break policy."

> **Dev:** "I confirmed WMT @ 109.89 then got 109.53 — book a second short?"
> **Domain expert:** "No — **Single Fulfillment Identity**. Use **Corrective Amend** on the same journal/lot. Second enter against that signal is refuse-by-default (force+notes only). Close+reopen only for true cancel/re-trade or accidental duplicate cleanup."

> **Dev:** "I want to skip the pyramid on A and take the entry on D instead."
> **Domain expert:** "**Desk Pass** the pyramid handoff with a **required reason**, then open the entry D workflow. That is a third **Passed Signal** kind — not process miss and not free-form enter. Capacity still never waived."

> **Dev:** "I downloaded the Congress Long-Short PDF from Quiver. Do we hit the API and run Daily Analysis?"
> **Domain expert:** "No. Upload the **Quiver Snapshot PDF** (or a test TXT) on the **Quiver Tracking Desk**. That builds a **Monday Rebalance Plan**. You **Plan Approve**; legs auto-execute at next open on dummy_sim. The **Quiver API** stays on DM for **Alt Filings** only. This **WQ Shadow Portfolio** is not TF — no Daily Analysis signals."

## Flagged ambiguities

- "account" can mean broker account, Portfolio, or Cromwell principal — resolved: use **Portfolio** for trading config, **Cromwell principal** for the human operator.
- "sync" is overloaded — resolved: **Data Acquisition** (DM←EODHD); **Reconciliation** (parquet→PG metadata); **Symbol Demand** (consumers→DM discovery); **Alt Filing** sync (DM←Quiver/events). WUT `Operations::DataSync` (Yahoo→activities) is legacy, not the target model.
- Quiver / Congress / insider prints are not EOD bars and not desk signals — resolved: **Alt Filing**.
- Quiver “strategy book” is three things — resolved: **Alt Filings** (events, DM+API); **Quiver Skim** (WUT/DM reconstruction from file dates, not published CAGR); **WQ Shadow Portfolio** / **Quiver Tracking Portfolio** (Wv2 paper OP whose target is a **Quiver Snapshot PDF** or TXT). Do not use the API as the tracking holdings source. Website scrape is a later HITL-removal plan, not v1.
- WQ “auto-execute” — resolved: **Plan Approve** is Human-Gated; execution of an **approved** Monday package may be automatic on the shadow paper OP (dummy_sim). Not DA fills. Not Mint. Not Execution Mode real until Capital Activation after test cycles.
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
- **CashEvent top-up** — resolved: notional-ledger top-up on **Active real** **Notional Capital** OPs; paper notional lives on initial capital. Paper **Broker Account Capital** (IBKR paper bound) does not CashEvent-mimic NLV. Distinct from Capital Activation.
- **Capital Authority / Risk Capital** — resolved (Grill 2026-09-01 D): pivot is what is authoritative for risk. Winston Unit Test and default Winston v2 paper (including Schwab-as-fulfillment-only) = **Notional Capital**. Winston v2 paper plus Interactive Brokers paper binding, and Winston v2 live = **Broker Account Capital**. When broker is authoritative, Winston v2 persists polled balances for risk; Broker Gateway remains evidence and transport, not the desk ledger.
- **Broker metric pair** — resolved (Grill 2026-09-01 Q2): **Risk Capital** = net liquidation value. Enter/pyramid room uses **Broker Buying Power** (margin-inclusive), then **Spending Capacity** = lesser of buying power and room under **Leverage Guardrail**. Default guardrail two times Risk Capital on **gross** (long plus short market value); configurable per Operational Portfolio / Trading Strategy; exceed only with per-transaction human override; broker buying power remains a hard ceiling. Settled cash may be negative.
- **Packaging owner** — resolved (Grill 2026-09-01 Q4–Q5): **Winston v2** owns **Fulfillment Packaging Policy** on the **Operational Portfolio** (desk supplies create-time default; Trading Strategy may suggest). Set in Winston v2 operations. Rule-based now (including a rule that asks the human for a per-share price). Later an LLM may evaluate and compare allowed shapes (long-dated calls versus a calendar spread) without a new fingerprint. Packaging may change by Desk Action on the same lot (entrance calls, pyramid shares). Same position is evaluated in more than one **Risk Modality**. Broker Gateway classifies evidence only.
- **Pyramid size after extra-modal entrance** — resolved (Grill 2026-09-01 Q6): **C** plus Q5 fill choice. Daily Analysis drafts the next pyramid in **Signal-Path Operational Lot** share units. Every **Risk Modality** is evaluated in parallel (share-equivalent, cash-at-risk of the packaging, per-share price, later a calendar-spread alternative). How the add is filled is **Fulfillment Packaging Policy** / human (entrance may be long-dated calls, pyramid shares). Do not size the draft from option premium alone.
- **One-Way Dynamic as live default** — operator note (Grill 2026-09-01 Q6), not a fingerprint ban: live Trend Following ops are not expected to use One-Way Dynamic Risk ladders; lab found higher drawdown without benefit. The mode remains valid in Winston Unit Test. Pyramids still exist under other risk geometries (static unit risk, Average True Range adds). Not re-locked as a new default here.
- **Live TF session cycle** — resolved (Grill 2026-09-01 Q7): **B**. Resting **Session Order Slate** is the live Trend Following loop; next-open stays the lab default until a fingerprint exists on resting-touch. Risk is evaluated at the **Moment of Truth**. Unfilled entries/pyramids cancel at the close; protective **Working Stops** replace overnight. Parking the slate is **Desk Send** of the package. v1 / L1 stays Confirm + evidence until write exists. ADR-009 point 3 (next-open as default EOD story) now needs a later addendum — not rewritten this turn.
- **Contest rank** — resolved (Grill 2026-09-01 Q8): **B**, Turtle mechanical. **Unit Heat** refuses correlated overflow (Faith caps; pairwise map from **Portfolio Correlation Score**). Remaining ties: buy-strength / sell-weakness and first-to-touch (**Slate Contest**). No expected-return ranking in live ops; WUT expected-return cycles stay lab/audit. No Daily Activity Report pick-list. No extra priority-approve check-in.
- **Automated park vs Desk Send** — resolved in part (Grill 2026-09-01 Q9): **A** scoped to **Slate Automation** on an **Operational Portfolio** + **TradingStrategy** fingerprint. Ranking stays Turtle; the verb remains **Desk Send** of the package (not Daily Analysis placing orders; not a global autotrader). DAR for those pairs is a **review** (moved Working Stops / levels, Turtle priorities) so a human may evaluate if necessary — not a nightly approve-to-park. Non-enabled OPs stay per-leg Human-Gated. Winston Quiver stays Plan Approve. After WQ paper setup, intent is to reset Interactive Brokers paper and bind it to a paper TF OP (probably Mint) for mechanical slate rehearsal — not locked as the bind itself this turn.
- **Nightly Send click once Slate Automation is on** — resolved (Grill 2026-09-01 Q10): **A**. Policy-automatic **Desk Send** of the mechanical slate once the flag is on. DAR is review; a human may halt or Desk Pass before the session. Disable the flag and it reverts to per-leg Send.
- **Accept-fill of slate prints** — resolved (Grill 2026-09-01 Q11–Q12): **B** now. Discovery/learning: **Accept-Fill** matched protective **Working Stop** prints (**Stop-Out Reconciliation**, warn on gap) so Unit Heat is not a ghost lot. Entries and pyramids stay **Desk Confirm** (packaging still human). **Risk Capital** already follows broker net liquidation when authority is broker. Whole-slate accept-fill (Q11-C) stays glossary aspiration only — **D**: no implied successor date; do not promote because the week went well; wait for a later grill.
- **Discovery / learning mode** — operator note (Grill 2026-09-01 Q11–Q12): still paper rehearsal and product law, not live capital and not L3 write this session. Winston Quiver paper setup first; then reset Interactive Brokers paper and bind a paper TF OP (probably Mint) for mechanical slate learning.
- "DmCoverage" (and variants: dm_coverage, DmCoverage model/association) was used in WUT and Wv2 for the local consumer mirror of DM's metadata — resolved: converge on the canonical **DataCoverage** term everywhere. Deprecate and remove consumer-specific naming variants (DmCoverage, etc.). Consumers maintain a local **DataCoverage** (as their view of available DM parquet via Reconciliation). Glossary definition of **DataCoverage** is authoritative for the concept (DM-owned metadata describing parquet reality).
- "`activities` table" / `market.activities` (and `Activity` records) in WUT was the carrier for market time-series (OHLCV + indicators) — resolved: for DM-sourced **Market** data this is **very temporary** and deprecated. DM parquet (via **Winston EOD Standard** + **DataCoverage**) is the authoritative source. All references (positions, trading_signals, backtest_indicator_values, passed_signals, market_indicator_values, etc.) must be refactored to use composite `(market_id, date)` keys + **Bar** objects from the DM loader. No DB table row for bar identity (use composite or non-persisted derivative). No long-lived shim. Call sites for creation (e.g. Position/TradingSignal/BIV construction) and usage (risk, expected return, charts, views) updated to loader + composite. "Just use DM to pull the data again" at render time using stored (market, date). Backtest result views pull via loader from stored (market, date); backtest runs have dedicated result parquet storage. All legacy non-DM records are defunct and deprecated; there is no historical or legacy relationship that we need to curate. The `activities` table itself is deprecated for market time-series and can eventually be removed or emptied for DM symbols (and legacy paths as they are cleaned).
- The `belongs_to :activity` on Position, TradingSignal, PassedSignal, BacktestIndicatorValue, MarketIndicatorValue, MarketMovingAverage, etc. is to be removed or fully deprecated for DM-sourced data. Refactor creation and usage sites to use the composite key + Bar (from the DM loader). The association remains only for truly legacy non-DM records. However, with the integration of DM all legacy non-DM records are defunct and can be considered deprecated. There is no historical or legacy relationship that we need to curate.
- For obtaining time-series data for a **Market** (DM-sourced), the primary mechanism is direct from **Winston EOD Standard** parquet via a loader (returning Bar/ParquetBar-like objects, e.g. with market_id). The expression `market.activities` (and the `activities` table) is not supported for DM-sourced Markets. The Data Sets page becomes a pure registry view of DM's **DataCoverage**; it no longer materializes or "loads" time-series into WUT.
- "trade_date" on **Journal** — resolved conceptually as two ideas: **Signal Date** (T) vs **Fill Date** (T+1 next-session open for EOD path). Schema may still use one column until the dual-date machinery lands; do not treat a single stamp as both signal and fill without saying which.
- "DA fills / autotrader" — resolved (Grill 2026-09-01 Q9–Q12): **Daily Analysis** still never opens **Positions**. **Slate Automation** (opt-in per OP + fingerprint) is the explicit product path for mechanical **Session Order Slate** **policy Desk Send** plus discovery **Accept-Fill** of protective stops only. Not implied by paper, Active, or an Interactive Brokers bind. Whole-slate accept-fill waits for a later grill.
- DAR "hold" vs empty skip — resolved (ADR-012): **Hold** only after a **Scored Session**. `missing_data` / no exact session bar is **Not Scored**. Clock-fired DAR at 16:30 MT must wait (until ~17:00) rather than publish hold. Catch-up mints current-desk tasks; no replacement DAR required.
- **Engaged** — confirmed **A**: any **Journal** (draft or executed) locks OP shape (Books + TS fingerprint). Unlock only **Close** or successor **Rebalance**. Same seed+fingerprint is one series (no second import of identical fingerprint as a parallel OP). Different fingerprints of the same lab seed are separate OPs and separate journal series. Independent of **Active**, paper, and real.
- Confirm window — **A**: from signal evening through **Fill Date**; next-open prefill when known; unconfirmed → **Passed Signal**. Real process misses are high-attention, not discretionary strategy.
- Signal vs fill instrument — **Fulfillment Packaging** may differ (shares vs LEAPs); journal tracks signal/returns spine.
- Capital contests — **A**: algorithm emits one deterministic package or algorithmic pass; human confirms fills/packaging. Multi-choice ER menus are non-default (force/ad-hoc discretionary).
- **Desk Workflow** — product requirement: every DAR next step links to a guided Wv2 journal/confirm path; partial today (desk form + Telegram/ops); full workflow not built.
- Multi-leg **Desk Handoff** — one logical package, N linked journals/tasks, ordered; out-of-order confirm **warns** (A).
- Winston vs fulfillment — signal/prioritization system for human (or future separate auto) **Fulfillment**; not full OMS truth; tidy end-to-end automation is not assumed.
- Equity / regime measurement — dual **Signal Spine** + **Booked Capital Spine**; **Risk Capital** follows **Capital Authority** (notional ledger vs polled broker). Gaps stay visible.
- Stops — **A**: signal/default ATR + **Working Stop** on Position; human update allowed; external stop-out via **Stop-Out Reconciliation** (required position link + snapshot; warn on gap). Order lifecycle still deferred.
- Stop-Out binding — **A**: required lot link + working_stop snapshot + warn on gap (not hard-block by default).
- Enter vs exit asymmetry — entries require methodology-originated Winston **signal** (DA draft / package leg); exits may be unsignaled (stop/error/downstream miss) with reason + linkage. Free-form enter deprecated as normal ops (force+audit only).
- **Confirm vs Send** — resolved (Grill B Q1): **Desk Confirm** = book only; **Desk Send** = place **Order Intent** only (no auto-open Position). Both verbs when binding has `order_write`; near-term ship is Confirm + L1 evidence (read/match/prefill) only — no `order_write` until ADR-010.
- **L1 first-ship capabilities** — resolved (Grill B Q2): **Confirmation Intake** = `auth` + `txn_read` + `order_read`; L2 `position_read` + `balance_read` are hints under **Notional Capital**, and feed **Risk Capital** under **Broker Account Capital**; `order_write` needs a fulfillment-write ADR (not current ADR-010 / Risk Scale).
- **Adapter home** — resolved (Grill B Q3 / H22): new monolith **Broker Gateway** (`broker_gateway`); transport + registry + minimal UI + evidence store; Manual in Wv2; match/book in Wv2.
- **BG durability & coordination** — resolved (Grill B Q4): DM-shaped — API commands (refresh/poll) + append-only JSONL **Winston Broker Evidence Standard** (idempotent events; optional rebuildable snapshots; PG metadata); orphans first-class; Wv2 pulls by cursor; no shared PG; not capital SoT.
- **Exit Capital Reconcile gate** — resolved (Grill B Q5): **A** — indicated ±$D on **Fulfillment Link** mid-life only; apply CashEvent on exit/explicit reconcile so capital lands on actual fulfillment profit (e.g. signal ~+$2,661 → LEAP actual +$1,400).
- **ADR-010 scope** — resolved (Grill B Q6): ADR-010 = L3 **Desk Send** / `order_write` law only; L1 Confirmation Intake does not wait on it. Optional thin ADR for Broker Gateway charter only if formal accept is needed before code.
- **L1 test strategy** — resolved (Grill B Q7): contract + fixtures first; live read after green; do not assume Schwab paperMoney is API sandbox — re-verify vendor sandbox in a spike.
