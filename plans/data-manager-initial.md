# Plan: Data Download Service (data_manager / DM) — Initial Implementation

**Authoritative location for the plan.** A detailed working copy lived in the Grok session dir during planning; this is the promoted version in the permanent ecosystem knowledge base.

**Status**: Approved (user feedback incorporated — parquet primary, PG metadata only, reconciliation, single EODHD, podman root compose, ecosystem/ folder, WUT reuse only, v1 legacy abandoned).

**See the full revised plan text** in the session history if you need the exhaustive version, or the principles/ files for distilled rules. This file captures the essence + key decisions.

## Context & Goal (Summary)
Build the first of the four monoliths: data_manager. It is triggered (ITMT by API; later by Cromwell), discovers required markets from WUT (using WUT's Portfolio/Market/Book model via a small internal API), acquires from EODHD (single upstream for v1), guarantees 3+ years + latest, calculates derivatives (ATR + supported MAs), writes the canonical Winston EOD Standard as parquet files (raw + derived columns), maintains PG metadata + coverage, reconciles on-disk parquets with PG (for git portability and "data files present" bootstrap), makes the data available (parquet files + API), verifies consumers have it, and reports rich step-by-step + final status to Cromwell.

WUT (the mature reference) will consume via a new adapter (or volume mount) and continue to support its existing paths during transition.

## Core Technical Decisions (Approved)
- **Storage**: Parquet files under `data_manager/data/markets/{SYMBOL}/...` are the primary, portable artifact (Winston EOD Standard). PG holds only lightweight metadata (Market, DataCoverage, DownloadRun/Task, Consumer registry, etc.). No heavy time-series in the DB.
- **Derivatives**: DM calculates them (ATR 17 simple + the MAs currently used by WUT strategies) and bakes the columns into the parquet on every standardize/write. DM owns keeping running values fresh.
- **Reconciliation**: First-class service. Walks the parquet tree and syncs PG so that the on-disk reality is always reflected in the registry. Enables shipping data with the repo, updating files in place, clone + drop data, etc.
- **Upstream**: EODHD **only** for the initial build of the full pipeline (acquisition → parquet standard → derivatives → reconciliation → provisioning → Cromwell notifications → WUT consumption). Pluggable kept in design.
- **Provisioning/Availability**: The act of writing the canonical parquet (with derived) + updating metadata is the core "make available". Additional: HTTP endpoint to serve the parquet, notification to Cromwell with paths/URLs, optional direct file mount in podman. WUT gains a parquet loader/adapter. Verification step confirms consumers have the expected coverage.
- **Deployment**: Podman. Root `compose.yml` at `sawtooth/`. Volumes for the data tree. Minimal Containerfiles per monolith.
- **Knowledge**: Everything lives in / is referenced from `sawtooth/ecosystem/`. Always read first.
- **Reuse**: Exclusively WUT's mature code and patterns for Portfolio/Market/Book, data services (DataSync/Reconciler/DatasetLoader/IndicatorCalculator/calculate_atr), Sidekiq, jobs, orchestration, etc. Winston v1 is legacy — do not use.

## High-Level Phasing (from approved plan)
1. ecosystem/ folder + seeds + root podman compose skeleton.
2. Scaffold data_manager (WUT patterns + duckdb gem + data/ tree).
3. EODHD client/adapter (single source), parquet standardizer (DuckDB + derivatives from WUT logic), reconciliation, gap/3y policy.
4. Jobs, orchestrator, APIs (trigger + parquet export), CromwellNotifier.
5. WUT internal APIs + parquet adapter + DataSync updates (reuse WUT code).
6. Podman validation, EODHD key placement (user supplies), tests, verification per the detailed steps in the full plan, ecosystem doc updates.

## Key Artifacts to Produce
- `sawtooth/ecosystem/...` (this folder and its substructure).
- `sawtooth/data_manager/` (new monolith).
- Updates only to `winston_unit_test/` (never to winston/ v1 for this work).
- Root `compose.yml`.

See `principles/` for the distilled rules and `interfaces/` for the emerging parquet schema definition.

This plan (and the full session version it was promoted from) was created after thorough exploration of WUT (the reference) and the existing sawtooth layout.
