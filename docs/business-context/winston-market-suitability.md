# Winston Market Suitability

**Type:** Domain business rules  
**Glossary:** `CONTEXT.md` — Market, Winston EOD Standard, DataCoverage  
**Implementation:** `data_manager/app/services/winston_market_suitability.rb`

## Purpose

Define which symbols are **suitable for Winston** trend-following portfolios. DM evaluates suitability after acquiring and standardizing EODHD data. Results are stored on `symbol_registry_entries` in DM PostgreSQL.

## Suitability states

| Status | Meaning |
|--------|---------|
| `pending` | Listed or acquired; not yet evaluated, or awaiting re-evaluation |
| `suitable` | Passes all rules S1–S7 |
| `not_suitable_for_winston` | Failed one or more rules; excluded from random portfolio draws |

## Rules (S1–S7)

| ID | Rule | Threshold |
|----|------|-----------|
| **S1** | History depth | `bar_count >= 1260` (~5 trading years) |
| **S2** | Winston EOD Standard | `atr_17` present in standardized parquet |
| **S3** | Volatility floor | `atr_17 / close` ≥ 25th percentile of acquired suitable pool, or ≥ 1.5% absolute floor |
| **S4** | Liquidity | US equities: EODHD `avgvol_1d > 700,000`; ETFs: `avgvol_1d > 100,000` when metadata present |
| **S5** | Price floor | `adjusted_close > 5` when screener metadata present |
| **S6** | Instrument type | Not option symbols; not leveraged/inverse ETFs (name filter) |
| **S7** | Data integrity | No gap > 5 consecutive calendar days in the most recent 252 sessions |

## DM registry

`symbol_registry_entries` is the symbol list manager:

- Populated by `dm:symbol_registry:import_eodhd_lists` and catalog/seed imports
- `dm_data_status` tracks acquisition: `unknown` → `requested` → `acquired` | `failed`
- Updated automatically on every `DataAcquisitionService.acquire`
- Query via `GET /api/v1/markets?suitability=suitable&dm_data_status=acquired`

## Relationship to consumers

WUT and Wv2 read parquet from DM; they do **not** re-run suitability. Portfolio Builder and correlation tools consume symbols DM has marked `suitable` with `dm_data_status: acquired`.

## Manual override

Register or re-evaluate via:

```bash
bin/rails dm:symbol_registry:import_seeds[AMAT,TSMC,GLTR,CPER]
bin/rails dm:symbol_registry:evaluate[AMAT]
```

Rejection is sticky for random draws unless suitability is reset manually.