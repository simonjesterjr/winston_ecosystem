# Ticket: Optional preferred color per Portfolio

**Status:** Done  
**Date:** 2026-08-03  
**Mode:** Ultrawork (parallel workstreams)  
**Scope:** WUT + Wv2 + `portfolio_configs` handoff  

## Verification (contractor 2026-08-03)

### Integrity
- Single `PortfolioColor` **service** per monolith (no model constant collision).
- WUT `Portfolio` validates + normalizes `color` column; `#preferred_color` / `#color_for_export` wired.
- WUT resolver uses `name` only (no `seed_name`) — acceptable for lab.
- Wv2 resolver supports `seed_name` for fingerprint-suffixed display names.
- Canonical token palette aligned; `portfolio_configs/portfolio-*.json` carry top-level `"color"`.

### Migrations (compose dev)
- `bin/compose exec -T winston_unit_test bin/rails db:migrate` — `portfolios.color` present.
- `bin/compose exec -T winston_v2 bin/rails db:migrate` — same.
- Named color portfolios already backfilled (WUT nulls = non-token names; Wv2 nulls = smoke/legacy non-token). No re-backfill required for registry names.

### Specs
| Suite | Result |
|-------|--------|
| WUT `portfolio_color` + `portfolio_correlation_dashboard` + `portfolio_config_exporter` | **29 examples, 0 failures** |
| Wv2 `portfolio_color` + importer + enricher + `report_pdf_chart_drawer` + equity_compare | **43 examples, 0 failures** |

### Smoke
- WUT Portfolio Green `preferred_color` = `#16a34a`; all registry color names resolve correctly.
- WUT `PortfolioCorrelationDashboard.history_series`: 10 series, all have hex `color` keys.
- Wv2 Portfolio Green `preferred_color` = `#16a34a`.
- Wv2 import of temp OP "Color Integration Smoke XYZ" stored `#16a34a`; destroyed safely (0 journals).
- `GET localhost:3000/wut/portfolios/correlation` → 200; HTML embeds per-series colors including `#16a34a`.

### Docs
- Glossary note added under **Portfolio** in `ecosystem/CONTEXT.md` (preferred color = presentation, not fingerprint).


## Goal

Operator charts (WUT PCS time series, Wv2 DAR / equity compare) must draw each portfolio’s line in a **preferred color** that matches the portfolio identity — e.g. Portfolio Green → green. Color is optional, defaulted from name when blank, and travels on the WUT→Wv2 JSON handoff.

## Contract (do not invent alternatives)

| Surface | Field | Rules |
|---------|-------|--------|
| DB (`portfolios.color`) | nullable `string` | CSS hex preferred: `#RRGGBB` (lowercase). Null = derive. |
| JSON handoff | top-level `"color"` | Optional. Omitted when blank after compact. Same hex form. |
| Not in fingerprint | — | Color is **display/presentation**, not methodology. Do **not** put it in TradingStrategy fingerprint. |

### Default resolution order

1. Explicit `portfolio.color` if present and valid hex (or known CSS color name → normalized hex).  
2. Token match on **name** / **seed_name** (case-insensitive word):  
   Red, Blue, Green, Pink, Mango, Rust, White, Orange, Yellow, Mint, Gray/Grey.  
3. Stable fallback hash from name → fixed palette index (never random per request).

### Canonical palette (hex)

| Token | Hex | Notes |
|-------|-----|--------|
| red | `#dc2626` | |
| blue | `#2563eb` | |
| green | `#16a34a` | |
| pink | `#db2777` | |
| mango | `#f97316` | Distinct from orange |
| orange | `#ea580c` | |
| rust | `#b45309` | |
| yellow | `#ca8a04` | Readable on white |
| mint | `#10b981` | Distinct from green |
| white | `#9ca3af` | Gray — pure white is invisible on white charts |
| gray / grey | `#6b7280` | |

### Helper API (each monolith, duplicated — no shared gem)

```ruby
# Portfolio#preferred_color  → hex string always (never nil for chart use)
# Portfolio#color_for_export → hex or nil (omit from JSON when nil and no name token? prefer always export resolved preferred when name matches; export explicit column if set, else name-derived if recognizable, else omit)
```

**Export rule:** Prefer exporting resolved preferred color when it can be derived from name or is stored — so configs are self-describing. Always export when `color` column set; when null but name matches a token, export the derived hex.

**Import rule:** If JSON has `color`, store it (normalize). If missing, leave null and resolve at read time via name/seed.

### Consumers

| Place | Behavior |
|-------|----------|
| WUT `/wut/portfolios/correlation` PCS multi-series Plotly | `line: { color: s.color }` per series |
| WUT `PortfolioCorrelationDashboard.history_series` | include `color` key |
| Wv2 `ReportPdfChartDrawer.equity_chart` | use `series[:color]` when present, else index palette |
| Wv2 DAR PDF PCS chart | pass color from enricher series |
| Wv2 `EquityCompareChartService` | pass portfolio preferred_color into chart series |
| Wv2 correlation enricher `series_entry` | include `color` from OP preferred_color |

### Backfill

After migration: set `color` on existing rows where name matches a color token (WUT + Wv2). Idempotent rake or `up` migration data step is fine.

## Workstreams (parallel)

1. **WUT core** — migration, model, resolver, backfill, PCS chart + dashboard series  
2. **WUT export** — `PortfolioConfigExporter` + specs; optional refresh of key `portfolio_configs/portfolio-*.json`  
3. **Wv2 import** — migration, model, `PortfolioConfigImporter` + specs  
4. **Wv2 impacts** — DAR enricher, PDF chart drawer, equity compare  

**Contractor** merges, runs specs in both monoliths, migrates compose DBs, smoke-checks correlation page + sample import.

## Out of scope

- Changing fingerprint / ADR-006 engagement rules  
- DM involvement  
- Requiring color on create UI (optional field ok if easy; not required for this ticket)  
- Recoloring non-portfolio chart series (market candles, etc.)
