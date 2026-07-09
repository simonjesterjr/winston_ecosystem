# ADR-005: Responsive User Pages (Progressive / Async Data)

**Status:** Accepted
**Date:** 2026-07-09
**Deciders:** Architecture (principal directive after WUT portfolios hang)
**Builds on:** ADR-001
**Applies to:** All majestic monoliths with a human UI — especially **WUT**; also DM and Wv2 wherever operators hit browser routes
**Incident seed:** WUT `GET /wut/portfolios` hung / timed out because the index path loaded full parquet histories and eager-loaded tens of thousands of `activities` rows inside the request

## Context

Monolith UIs (WUT portfolio lab, data sets, backtest results; DM ops pages; any future Wv2 human surfaces) must stay usable under real data volumes: hundreds of markets, multi-year parquet, large journals/positions.

We observed a concrete failure mode: a list page that only needs **summary** fields (name, market symbols, overlapping date range) blocked the entire Puma process for tens of seconds to minutes by:

- Eager-loading `markets: :activities` (~60k rows)
- Calling `DmParquetLoader.full_history` per market just to compute min/max dates
- Concurrent full-catalog `MarketCatalog.load!` re-upserts on other pages saturating the DB

Bare `localhost:3000` still answered with a cheap redirect; real app routes under `/wut/` hung. That is unacceptable for operator workflow.

Alternatives evaluated:

- **Approach A: Synchronous completeness** — every page renders only when all underlying data is fully loaded and computed in the request
- **Approach B: Precompute everything into PG at ingest** — no progressive UI; all summaries always denormalized
- **Approach C: Responsive shell + progressive / async data** — request returns a snappy usable page; heavy work via Sidekiq, metadata caches (e.g. DataCoverage), or Hotwire (Turbo/Stimulus) progressive hooks

## Decision

We choose **Approach C: Responsive user pages**.

### Principle

**User-facing HTTP responses must feel snappy.** A page that operators open repeatedly (indexes, dashboards, show headers) must return a usable shell in well under a second under normal dev/prod load. Completeness of heavy data is **not** a prerequisite for first paint.

### Rules (normative)

1. **Request path = metadata + light queries only**
   - Prefer **DataCoverage** / local coverage mirrors, counts, and SQL aggregates (`MIN`/`MAX`/`COUNT`) over materializing full time-series or full association graphs.
   - Do **not** call `DmParquetLoader.full_history` (or equivalent full-table loads) from index/list actions or from model methods invoked by those views solely to compute date ranges or “has data?” flags.
   - Do **not** `includes(...:activities)` (or load all journals/positions) for pages that only need summaries.

2. **Heavy work is async or progressive**
   - **Sidekiq / ActiveJob** for multi-symbol registry sync, DM acquisition triggers, backtests, optimizers, exports, bulk recompute.
   - **Hotwire (Turbo Frames / Streams, Stimulus)** to fill panels after first paint: charts, large tables, win/loss stats, coverage refresh status.
   - Polling or stream updates are preferred over holding the original request open.

3. **Idempotent “ensure” helpers must be cheap when already done**
   - Bootstraps such as `MarketCatalog.ensure_registry!` must insert **missing** rows only — never re-save the entire universe on every page hit.

4. **Applies to all monoliths**
   - WUT is the sharpest pain point today and the reference UI lab.
   - DM and Wv2 browser routes follow the same bar when they exist.
   - Agent/MCP and rake paths may run longer synchronous work; human page GETs may not.

### Acceptable patterns

| Need | Prefer |
|------|--------|
| Overlapping portfolio date range on index | Coverage `earliest`/`latest` / bar_count |
| “Has data?” badge | Coverage present, parquet exists check, or aggregate existence |
| Full chart / dense bars | Turbo frame or async job + stream |
| Registry / DM metadata sync | Sidekiq job; UI shows status + refresh |
| Backtest / optimization | Enqueue; show progress; never block list pages |

### Non-goals

- This ADR does **not** forbid full-history loads inside **backtest runners**, optimizers, or explicit “download / ensure data” actions the user intentionally starts.
- It does **not** require every legacy page to be rewritten immediately — new work and hang fixes must comply; known offenders get tickets.

## Rationale

### Why not synchronous completeness?

Operator UIs are navigational. Blocking first paint on analytical completeness couples page responsiveness to data volume growth and turns one bad includes into an app-wide hang (Puma thread / reloader / pool contention).

### Why not only denormalize into PG?

Coverage metadata (ADR-002 / ADR-003 world) already supplies the cheap summary layer for DM-sourced markets. Duplicating full OHLCV into PG for UI snappiness fights the parquet standard. Where denormalized **summaries** help (counts, ranges, status), use them; do not reintroduce time-series in PG for list pages.

### Why Hotwire + Sidekiq?

Both are already in the Rails stack across monoliths. Sidekiq owns multi-minute work; Hotwire owns progressive enhancement without a separate SPA. Together they match “majestic monolith” UI without micro-frontend complexity.

## Consequences

### Positive

- Indexes and dashboards stay usable as market universes and history grow
- Failures isolate to background jobs or partial frames instead of whole-process hangs
- Aligns with existing DM coverage metadata and async orchestration culture

### Negative

- Some pages show incomplete panels briefly (“loading…”) until jobs/frames finish
- Authors must design loading/empty/error states deliberately
- Reviewers must reject “just includes everything” as a convenience

### Risks mitigated

- Request-path full parquet / activities loads → explicit ban for summary UI
- Catalog thrash on every hit → ensure-helpers are incremental
- Cross-monolith UI regressions → same standard for DM/WUT/Wv2 human routes

### Conformance checklist (for PRs touching UI)

- [ ] Index/show first response avoids full-history and bulk activities/journals loads
- [ ] Any work expected to exceed ~1s is job- or frame-backed
- [ ] Status/progress is visible when data is progressive
- [ ] “Ensure/sync” paths are no-ops when already satisfied

## Related

- Incident fix (WUT): `Portfolio#test_data_date_range` uses coverage/SQL aggregates; `PortfoliosController#index` includes markets + coverage only; `MarketCatalog.ensure_registry!` inserts missing symbols only
- ADR-001 — majestic monoliths and coordination
- ADR-002 — parquet Winston EOD standard (metadata vs time-series)
- ADR-003 — DM owns derivatives (consumers read columns; do not recompute on page render)
- Plans: `plans/wut-dm-parquet-source-of-truth.md`
