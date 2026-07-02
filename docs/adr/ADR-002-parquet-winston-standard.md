# ADR-002: Parquet as the Winston EOD Standard

**Status:** Accepted
**Date:** 2026-06-12
**Deciders:** Architecture (seeded from principles/02_data_storage_and_reconciliation.md)
**Builds on:** ADR-001
**Source design:** `interfaces/winston-eod-parquet-standard.md`
**Domain context:** `docs/business-context/parquet-winston-standard.md`

## Context

Market time-series data (OHLCV + derived indicators) must travel between DM, WUT, and Wv2. We needed a storage format that supports analytical queries, git-portable data sets, volume mounts in Podman, and clean separation from application metadata.

Alternatives evaluated:

- **Approach A: PostgreSQL time-series tables** — store OHLCV and indicators in PG across monoliths
- **Approach B: CSV files** — simple but slow, no schema enforcement, poor analytical performance
- **Approach C: Parquet (Winston EOD Standard)** — columnar, DuckDB-friendly, portable files with PG metadata only

## Decision

We chose **Approach C: Parquet as the Winston EOD Standard**.

- **Location (DM):** `data_manager/data/markets/{SYMBOL}/bars.parquet`
- **Contents:** date, OHLCV, atr_17, plus supported MA columns (exact list from WUT strategies)
- **PG role:** metadata only — Market, DataCoverage, DownloadRun, Consumer registry
- **Versioning:** standard_version in metadata; bump on semantic changes (currently v0.1)

Consumers read via volume mount (preferred in Podman dev) or HTTP from DM. WUT may still load into local activities during transition; DM parquet is the preferred source for new work.

## Rationale

### Why not PG time-series?

OHLCV history is large, append-heavy, and analytical. Storing it in PG duplicates data across monoliths, complicates git portability, and fights the "drop parquet files and reconcile" workflow explicitly requested.

### Why not CSV?

No column typing, poor compression, slow bulk reads, no DuckDB predicate pushdown. WUT already moved toward parquet locally.

### Why parquet?

- **Portability** — ship data with repo or mount volumes
- **Analytical** — DuckDB window functions for DM standardization
- **Separation** — PG holds orchestration state; parquet holds truth for time-series
- **Reconciliation** — scan files to update DataCoverage without re-downloading

## Consequences

### Positive

- Single canonical artifact per symbol
- Consumers avoid recalculating derivatives DM already baked in
- Git-friendly workflow with reconciliation (see ADR-003 companion business-context)

### Negative

- Binary files need `.gitignore` discipline for large datasets
- Schema evolution requires version bumps and consumer tolerance

### Conformance checklist

- [x] DM writes `bars.parquet` per symbol
- [x] Interface doc at `interfaces/winston-eod-parquet-standard.md`
- [~] WUT adapter to prefer DM parquet over local Yahoo/CSV (in progress)
- [~] Wv2 consumes DM parquet for daily analysis (in progress)