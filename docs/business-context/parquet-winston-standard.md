# Parquet Winston Standard — Domain View

**Type:** Domain explainer (technology contract in `interfaces/winston-eod-parquet-standard.md`)
**Related ADR:** ADR-002

## What it is

The **Winston EOD Standard** is the portable file format for market history in the ecosystem. One file per symbol, columnar parquet, readable by DuckDB, mountable in Podman volumes.

## File layout

```
data_manager/data/markets/{SYMBOL}/bars.parquet
```

Example: `data/markets/AAPL/bars.parquet`

## Required columns (v0.1 minimum)

| Column | Meaning |
|--------|---------|
| date | Trading day (ascending, no duplicates) |
| open, high, low, close | Adjusted where EODHD provides adjustments |
| volume | Share volume |
| atr_17 | 14-period ATR, simple method, period 17 (WUT-compatible) |
| sma_*, ema_*, wma_* | Supported MA periods from WUT strategies |

Embedded or sidecar metadata: `symbol`, `asof`, `source=eodhd`, `standard_version=0.1`, `indicators` list.

## Consumer read paths

| Consumer | Preferred path | Fallback |
|----------|----------------|----------|
| WUT | Volume mount → DuckDB/adapter → activities | Local Yahoo/CSV (legacy) |
| Wv2 | Volume mount → daily analysis services | — |
| Cromwell/MCP | Indirect via Wv2/DM tools | — |

## Versioning rules

- Bump `standard_version` when columns or semantics change
- Old files remain readable; DM reconciliation tolerates missing new columns
- Document changes in `interfaces/winston-eod-parquet-standard.md` and note in ADR if irreversible

## DM write contract

On every acquire/update for a symbol:

1. Combine fetched range with existing local data
2. Recompute all required derivatives over full/trailing history
3. Write atomically (temp + rename)
4. Update DataCoverage
5. Reconcile
6. Notify Cromwell