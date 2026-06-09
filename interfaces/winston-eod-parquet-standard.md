# Winston EOD Parquet Standard (v0.1 — Initial)

This is the canonical format that DM produces and that consumers (WUT today, Wv2 later) are expected to understand.

**Location convention (DM)**: `data/markets/{UPPER_SYMBOL}/bars.parquet` (or partitioned sub-structure under it).

**Required columns (minimum for v1)**:
- date (date)
- open, high, low, close (float)
- volume (bigint or int)
- atr_17 (float, simple method, period 17 — exactly as WUT calculates it)
- Plus the moving average columns currently supported and used by WUT strategies for entry/exit (to be confirmed exactly during implementation by inspecting WUT `app/strategies/` and `app/services/indicator_calculator.rb` + `market_moving_average.rb` usage):
  - Examples from existing WUT: sma_20, ema_20, wma_20, sma_55, ema_55, wma_55, etc.
- Any other derived columns agreed for the "running" set that DM will keep fresh.

**Conventions**:
- Rows sorted ascending by date.
- No duplicate (symbol, date) — the file for a symbol is the single source for that symbol's history.
- Adjusted prices where the upstream (EODHD) provides them; note the source.
- Embedded or sidecar metadata: symbol, asof (the "as of" date of the last update), source="eodhd", standard_version="0.1", indicators (list of derived columns present).
- DuckDB-friendly (excellent predicate pushdown, window functions used by DM during standardization).

**Versioning**: Start with 0.1. When we add columns or change semantics, bump and document here + in principles. Old files should still be readable (DM reconciliation + consumers should be tolerant or have a migration path).

**Consumer expectations**:
- WUT (initial) will load via its new DM/Parquet adapter (reusing DatasetLoader bulk patterns) into its local structures (activities + market_indicator_values or equivalent) for evaluation.
- Direct DuckDB queries against the parquet are also valid (especially in podman with volume mount).

**DM responsibilities**:
- On every acquire/update for a symbol: produce a file that conforms to the current standard, with all required derived columns correctly calculated over the full (or trailing relevant) history.
- Reconciliation reflects exactly what columns and date range are present in the file(s).

This document will grow as we implement and decide the exact initial column list (pull the authoritative list from current WUT during the build of the standardizer).

See principles/02_data_storage_and_reconciliation.md and the approved data-manager plan in plans/.
