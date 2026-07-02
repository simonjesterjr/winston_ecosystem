# Reconciliation Semantics

**Type:** Domain explainer
**Related ADR:** ADR-002
**Related principle:** `principles/02_data_storage_and_reconciliation.md`

## What reconciliation is

**Reconciliation** is DM scanning its on-disk parquet tree and updating PG metadata (`Market`, **DataCoverage**) to match reality. It is not downloading data and not syncing to consumers.

Think: "the filesystem is truth; PG catches up."

## When it runs

1. **DM app boot** — cheap guard job ensures PG knows what is on disk
2. **After every successful download/standardize** for a market
3. **Explicitly** via rake: `data:reconcile` or `data:reconcile[SYMBOL]`

## What it extracts per symbol

From each `data/markets/{SYMBOL}/bars.parquet`:

- `earliest_date`, `latest_date`, `bar_count`
- `indicators_present` — which derived columns exist (atr_17, sma_20, etc.)
- `source` (eodhd), `standard_version`

Then upserts Market (if needed) and DataCoverage.

## Why it matters (three scenarios)

### Scenario 1: Git clone + drop in data files

You clone `data_manager`, copy real parquet files into `data/markets/`, run reconcile. PG now knows AAPL has data through 2026-06-27. DM will not re-download the entire 3-year history.

### Scenario 2: Someone updated a file in place

A colleague adds newer bars to `AAPL/bars.parquet` manually. Reconcile detects the new `latest_date` without treating it as a brand-new dataset.

### Scenario 3: Sample data for CI

Small reference parquets for 1–3 symbols ship with the repo. Reconcile registers them; smoke tests run against known data.

## What reconciliation is NOT

| Operation | What it does | Not reconciliation |
|-----------|--------------|-------------------|
| EODHD download | Fetches new bars | Acquisition |
| WUT DataSync | Loads parquet → activities | Consumer ingest |
| `dm:sync_from_wv2` | Ensures DM has markets Wv2 needs | Consumer-driven acquisition |
| PG → parquet | Never happens | Reconciliation is parquet → PG only |