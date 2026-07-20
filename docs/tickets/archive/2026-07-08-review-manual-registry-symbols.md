# Ticket: Review the 8 "manual" symbols registered via reconcile (CDE, IBM, JNJ, PG, ROKU, RXT, WMT, WTI)

**Status:** Done  
**Priority:** P3  
_Archived 2026-07-20: completed work; no further action._


**Related to:** ecosystem/docs/session-reports/2026-07-08-1430-dm-reconcile-container-cleanup.md

## Context
During the first successful `data:reconcile` run, these 8 symbols had no prior `SymbolRegistryEntry` (or one without `list_source`). The reconcile path now defaults them to `list_source: "manual"`.

They are common / well-known symbols (big caps + a few others). They may have been acquired via direct EODHD calls, manual parquet drops, or older non-registry paths.

## Acceptance Criteria
- [x] Inspect each symbol's history (how its parquet was originally created, any prior registry attempts).
- [x] Decide for each whether `manual` is correct, or whether it should be re-classified (e.g. `eodhd_screener`, `catalog`, `seed`).
- [x] Update the entries (and any related suitability / list_metadata) as needed.
- [x] Add a note or small correction approach if a batch fix is warranted.
- [x] Confirm they now appear correctly in `awaiting_evaluation` / suitable scopes after reconcile.

## Links
- Session report (error log section): `ecosystem/docs/session-reports/2026-07-08-1430-dm-reconcile-container-cleanup.md`
- SymbolRegistryEntry model and LIST_SOURCES: `data_manager/app/models/symbol_registry_entry.rb`
- ReconciliationService registry sync: `data_manager/app/services/reconciliation_service.rb`
- Catalog source of truth: `winston_unit_test/config/market_catalog.json`
- Portfolio memberships: `portfolio_configs/registry.json`

**Owner:** Worker 4 (DM-as-source-of-truth closeout)  
**Completed:** 2026-07-08

---

## Investigation summary

### Why they became `manual`
1. On-disk parquets existed under `data/markets/<SYM>/bars.parquet` (all 8 present; mtimes June 15 – July 7 2026).
2. Reconcile created `Market` + `DataCoverage` + `SymbolRegistryEntry` with `entry.list_source ||= "manual"` when no prior registry row existed (`ReconciliationService` + same pattern in `MarketMetadataRecorder`).
3. Registry rows for these 8 were created **2026-07-08 ~20:52 UTC** during reconcile — not via importer.
4. No `DownloadTask` rows for these symbols in current PG (acquisition history not retained / predated task table usage).
5. **Catalog was never imported into DM:** `SymbolRegistryImporter.catalog_path` is `nil` in the container (WUT path and `/app/catalog/...` not mounted). Pre-fix: `list_source=catalog` count was **0**.

### LIST_SOURCES available
`eodhd_etf_list | eodhd_screener | catalog | manual | seed`

### Pre-fix distribution (context)
| source | count | notes |
|--------|------:|-------|
| eodhd_etf_list | 5786 | ETF universe import |
| eodhd_screener | 4 | Only T, INTC, AAL, NVDA currently |
| seed | 4 | AMAT, TSMC, GLTR, CPER only |
| catalog | 0 | Catalog file not reachable in DM container |
| manual | 15 | Included the 8 ticket symbols + AAPL/AMZN/GOOGL/MSFT/TSLA/COPR/CLETF |

### Parquet / coverage at review time
| Symbol | Parquet | Bars | Range | Coverage source |
|--------|---------|-----:|-------|-----------------|
| CDE | yes (~224KB, 2026-07-02) | 1799 | 2019-05-06..2026-07-01 | eodhd |
| IBM | yes (~248KB, 2026-07-07) | 1797 | 2019-05-10..2026-07-06 | eodhd |
| JNJ | yes (~238KB, 2026-06-15) | 1799 | 2019-04-18..2026-06-15 | eodhd |
| PG | yes (~239KB, 2026-06-15) | 1799 | 2019-04-18..2026-06-15 | eodhd |
| ROKU | yes (~245KB, 2026-07-01) | 1799 | 2019-05-06..2026-07-01 | eodhd |
| RXT | yes (~195KB, 2026-07-02) | 1483 | 2020-08-05..2026-07-01 | eodhd |
| WMT | yes (~264KB, 2026-06-15) | 1799 | 2019-04-18..2026-06-15 | eodhd |
| WTI | yes (~224KB, 2026-07-02) | 1799 | 2019-05-06..2026-07-01 | eodhd |

### Provenance evidence (not seed / not screener import)
| Symbol | In WUT `market_catalog.json`? | Portfolio / other |
|--------|-------------------------------|-------------------|
| CDE | yes — Coeur Mining Inc, US stocks | Portfolio Red |
| IBM | yes — IBM, US stocks | DM test-download default (`/api/v1/test/download/IBM`); docs example symbol |
| JNJ | yes — Johnson & Johnson, US stocks | Portfolio Blue; WUT seeds fallback list |
| PG | yes — Procter & Gamble Co., US stocks | Portfolio Blue; WUT seeds fallback list |
| ROKU | yes — ROKU, US stocks | Portfolio Red |
| RXT | yes — Rackspace Technology Inc, US stocks | Portfolio Blue |
| WMT | yes — Walmart Inc., US stocks | Portfolio Blue; WUT seeds fallback list |
| WTI | yes — **Crude Oil WTI**, trading_market=`FRED Commodity`, asset_class=`commodities` | Commodity path (not equity screener) |

**Not** reclassified as:
- `seed` — reserved for intentional core seeds (AMAT/TSMC/GLTR/CPER)
- `eodhd_screener` — never imported via screener job for these symbols (and WTI is not a US equity screener hit)
- `eodhd_etf_list` — none are ETFs from that list
- leave `manual` — incorrect once catalog membership is known

---

## Decision table (final)

| Symbol | Before | After | name | trading_market | asset_class | Rationale |
|--------|--------|-------|------|----------------|-------------|-----------|
| CDE | manual | **catalog** | Coeur Mining Inc | US | stocks | In WUT catalog; Portfolio Red member |
| IBM | manual | **catalog** | IBM | US | stocks | In WUT catalog; also historic test-download symbol |
| JNJ | manual | **catalog** | Johnson & Johnson | US | stocks | In WUT catalog; Portfolio Blue + WUT seed fallback |
| PG | manual | **catalog** | Procter & Gamble Co. | US | stocks | In WUT catalog; Portfolio Blue + WUT seed fallback |
| ROKU | manual | **catalog** | ROKU | US | stocks | In WUT catalog; Portfolio Red member |
| RXT | manual | **catalog** | Rackspace Technology Inc | US | stocks | In WUT catalog; Portfolio Blue member |
| WMT | manual | **catalog** | Walmart Inc. | US | stocks | In WUT catalog; Portfolio Blue + WUT seed fallback |
| WTI | manual | **catalog** | Crude Oil WTI | FRED Commodity | commodities | In WUT catalog as commodity (not equity) |

Unchanged fields (intentional):
- `dm_data_status = acquired` (parquet present)
- `suitability_status = pending` (not yet evaluated → correctly in `awaiting_evaluation`)
- No suitability auto-apply in this ticket (out of scope; use `dm:symbol_registry:evaluate_pending` later)

`list_metadata` written on each row:
- `reclassified_from`, `reclassified_at`, `reclassified_reason`, `provenance_notes`, `catalog_symbol: true`

Market rows also backfilled `name` / `trading_market` where blank (reconcile had created bare Markets).

---

## DB updates performed

One-off `bin/compose exec data_manager bin/rails runner` (2026-07-08 ~21:05 UTC):

- Set `list_source` **manual → catalog** for all 8
- Filled `name`, `trading_market`, `asset_class` from catalog metadata
- Merged reclassification audit fields into `list_metadata`
- Backfilled related `Market` name/trading_market when blank

**No migration, no commit.** Data-only correction.

### Post-update distribution
| source | count |
|--------|------:|
| catalog | 8 |
| eodhd_etf_list | 5786 |
| eodhd_screener | 4 |
| seed | 4 |
| manual | 7 (remaining: AAPL, AMZN, GOOGL, MSFT, TSLA, COPR, CLETF) |

---

## Scope checks (post-update + re-check after container restart)

| Scope | Expected | Observed |
|-------|----------|----------|
| `SymbolRegistryEntry.awaiting_evaluation` for the 8 | all 8 present (`acquired` + `pending`) | **all 8** with `list_source=catalog` |
| `SymbolRegistryEntry.suitable` for the 8 | empty until evaluate | **0** |
| `SymbolRegistryEntry.acquired` for the 8 | all 8 | **all 8** |
| Re-reconcile does not clobber `catalog` | stays catalog (`||= "manual"` only fills blank) | confirmed after restart |

---

## Batch correction note (residual manuals + importer quirks)

### Residual manuals also in catalog (out of this ticket’s 8)
These remain `list_source=manual` but **are** in `market_catalog.json` and could get the same treatment later:

| Symbol | Notes |
|--------|-------|
| AAPL | catalog; suitability already evaluated (`not_suitable_for_winston`) |
| AMZN | catalog; `suitable` |
| GOOGL | catalog; `not_suitable_for_winston` |
| MSFT | catalog; `suitable` |
| TSLA | catalog; `suitable` |

True orphans / non-catalog manuals:
| Symbol | Notes |
|--------|-------|
| COPR | not in catalog; keep manual (or seed-like copper instrument) |
| CLETF | not in catalog; `failed` / not_suitable — keep manual |

### Why `import_catalog!` alone would not have fixed these
`SymbolRegistryEntry.upsert_symbol!` only assigns `list_source` when:

```ruby
entry.new_record? || list_source == "manual" || list_source == "seed"
```

So calling upsert with `list_source: "catalog"` on an **existing manual** row does **not** promote it. A proper batch fix needs either:

1. **Direct assign** (what this ticket did), or
2. A small code change so stronger sources can overwrite `manual`/`seed`, e.g. allow update when existing is `manual`/`seed` and incoming is catalog/screener/etf, **and**
3. Mount or copy `winston_unit_test/config/market_catalog.json` into DM (`MARKET_CATALOG_PATH` / `/app/catalog/market_catalog.json`) then run `dm:symbol_registry:import_catalog` for future symbols.

Suggested one-liner for residual catalog-known manuals (operator-run later):

```bash
bin/compose exec data_manager bin/rails runner '
# after mounting MARKET_CATALOG_PATH, or hardcode catalog hits:
%w[AAPL AMZN GOOGL MSFT TSLA].each do |sym|
  e = SymbolRegistryEntry.find_by!(trading_symbol: sym)
  next unless e.list_source == "manual"
  e.update!(list_source: "catalog",
            list_metadata: e.list_metadata.merge(
              "reclassified_from" => "manual",
              "reclassified_reason" => "present in WUT market_catalog.json"))
end
'
```

Optional follow-ups (not done here):
- Mount catalog into DM compose service; run full import
- Fix `upsert_symbol!` promotion rules so catalog/screener can reclaim manuals
- Run `dm:symbol_registry:evaluate_pending` so these 8 leave `awaiting_evaluation`

---

## Status

**Completed** — all 8 reclassified to `catalog` with catalog metadata; scopes verified; residual manuals + importer quirk documented for a later batch pass.
