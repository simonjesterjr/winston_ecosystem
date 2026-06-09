# Majestic Monoliths & Ecosystem Vision

We fully believe in majestic monoliths, but we are deliberately building (and having work together) four focused ones:

- **data_manager (DM)**: The data download / acquisition / standardization service. Owns EODHD (initial single upstream), guarantees ≥3 years + latest data, calculates running derivatives (ATR + supported MAs), writes canonical "Winston EOD Standard" parquet files, maintains lightweight PG metadata + coverage, reconciles on-disk data with PG, notifies Cromwell, serves data to consumers (WUT today, Wv2 later).
- **winston_unit_test (WUT)**: Backtesting + Winston Operations (daily trading support). Already mature (beta). Reuses its own excellent patterns for portfolios, markets (via Books), activities, DataSync/Reconciler, DatasetLoader, indicators, Sidekiq jobs, daily ops orchestration. Will consume DM's parquet (via adapter or volume mount) for clean data + precomputed derivatives.
- **winston (v1)**: Legacy. Will be abandoned. Do not model new work after it or reuse its code for data/portfolio logic.
- **Cromwell**: Agentic AI component that manages communications, reporting, to-do lists, and daily coordination between Winston's principals. Will (eventually) tell DM to start daily downloads via API and receive structured step/status/error/completion webhooks from DM (and other components).

## Composition Model (Service-Oriented but Monolithic Apps)
- Majestic = each is a complete, powerful, independently deployable Rails app with its own DB (PG for metadata/state), Sidekiq, UI/CLI where useful.
- They work together via:
  - REST/JSON internal APIs (authenticated by token/secret for now).
  - Sidekiq jobs (within a monolith).
  - Webhooks / notifications (especially DM → Cromwell for status; Cromwell → DM for triggers ITMT).
  - File-based where it makes sense (DM's `data/` parquet tree can be volume-mounted in podman for direct high-perf access by consumers).
- Podman (compose at root) is the local (and target) runtime.

## Key Invariants
- Data durability: DM ensures at least ~3 years of contiguous recent EOD data (incl. latest trading data) for every market that any consumer (WUT portfolio, future Wv2) cares about.
- Derivatives: DM (not consumers) calculates and bakes in the running values (ATR period 17, the MAs currently supported by the ecosystem) into the parquet files.
- Parquet is the portable "Winston standard" for moving market data + derived around the ecosystem. PG in DM (and other monoliths) is for application metadata, runs, status, registry — not the time-series.
- Reconciliation: DM can always scan its parquet `data/` tree and bring PG metadata into sync. This enables git portability of data sets, "drop in old/updated files", shipping samples with the repo, etc.
- Reuse: WUT is the solid reference for Portfolio/Market/Book shapes, data services (DataSync, DatasetLoader, IndicatorCalculator, calculate_atr), Sidekiq patterns, operations orchestration. Winston v1 is legacy — ignore for modeling and code reuse.
- Single upstream first: EODHD only while we build the core (parquet standard, reconciliation, 3y logic, Cromwell notifications, WUT consumption). Pluggable adapters are kept in the design but not exercised until the single-source foundation is solid. User supplies the EODHD key once the ecosystem/deployment config location exists.
- Knowledge: All of the above (and evolving principles, plans, interfaces, deployment) lives in `ecosystem/`. Always read it first.

This vision comes directly from the original user query + the approved data download service plan.
