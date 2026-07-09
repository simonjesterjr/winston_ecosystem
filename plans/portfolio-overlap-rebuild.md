# Portfolio Overlap Controls and Rebuild Plan

**Status:** Active  
**Updated:** 2026-07-08 (Orange + White membership complete)

## Goal

Build four trend-following portfolios from four seed markets, with enforced exclusivity and overlap limits, expanded historical data via DM random acquisition, and paginated WUT Data Sets UI.

## Seed → Portfolio mapping

| Seed | Portfolio | Target size |
|------|-----------|-------------|
| AMAT | Portfolio Red | 7–9 markets |
| TSMC | Portfolio Blue | 9–11 markets |
| GLTR | Portfolio Orange | 12–15 markets |
| CPER | Portfolio White | 16–20 markets |

Each seed anchors **exactly one** portfolio. A seed must not appear as a member of any other portfolio.

## Overlap rules

1. **Seed exclusivity** — `AMAT`, `TSMC`, `GLTR`, `CPER` each belong only to their named portfolio.
2. **Bilateral 25% cap** — for any two finalized portfolios A and B:
   - `|A ∩ B| / |A| ≤ 0.25`
   - `|A ∩ B| / |B| ≤ 0.25`

Enforced in WUT via `PortfolioOverlapPolicy`, wired into `PortfolioCorrelationBuilder` and `portfolios:build_correlation`.

**Effective membership:** overlap counts strip *alien seeds* (seeds that belong to another portfolio) from each side before computing fractions. Seed exclusivity is enforced separately. This prevents a stale peer (e.g. Red still holding TSMC) from blocking all diversifier picks.

## Status (2026-07-08)

| Phase | Status |
|-------|--------|
| 1 — Overlap controls | Done (`PortfolioOverlapPolicy`, `PortfolioRegistry`, builder + rake) |
| 2 — Data Sets pagination | Done (15/page) |
| 3 — DM random acquisition | **Done for ≥50 gate** — suitable **51** (3×300 batches 2026-07-08); acquired 1532 |
| 4 — Rebuild Red | **Done** |
| 5 — Rebuild Blue | **Done** |
| 6 — Vet + export | Red **Done** (PBR 25, observation); Blue **Done** (run 23, observation); Orange **Done** (opt#33 / PBR 41, observation); White **Done** (opt#36 / PBR 40, observation) |
| 7 — Strategy evaluation doctrine | **~90%** — gates + export_kind + null-Sharpe fallback + RANKING_METRIC env |
| 8 — Orange + White membership | **Done** — both registered; all bilateral ≤25%; seeds exclusive |

**Unblocked:** DM parquet is source of truth for portfolio path; scheduled jobs will not re-duplicate DM data (2026-07-08 SOT closeout).

### Portfolio Red (rebuilt + vetted)

- **Seed:** AMAT only (no TSMC, GLTR, CPER)
- **Markets (9):** AMAT, CDE, MSFT, MSOS, PHYMF, ROKU, URA, VXX, XLV
- **Overlap vs Blue:** 0 shared (0% bilateral)
- **Diversification:** Strong (mean \|r\| ≈ 0.21)
- **Sidecar:** `portfolio_configs/portfolio-red-sidecar.json`
- **Vet winner (PBR 25):** `Breakout50DayNoHistoryStrategy` + `VolatilityExitStrategy`
- **Economics:** Return **+636%**, max DD **64%**, trades 1051, Sharpe null
- **Export:** `portfolio_configs/portfolio-red.json` — **`export_kind: observation`** (failed drawdown gate ≤50%)
- **Wv2:** Paper/regime only — not trade-ready

### Portfolio Blue (rebuilt + vetted)

- **Seed:** TSMC only (no AMAT, GLTR, CPER)
- **Markets (11):** AAL, AMZN, GLD, GOOGL, JNJ, PG, RXT, TSLA, TSMC, WMT, XLE
- **Overlap vs Red:** 0 shared (0% bilateral)
- **Diversification:** Strong (mean \|r\| ≈ 0.12)
- **Sidecar:** `portfolio_configs/portfolio-blue-sidecar.json`
- **Registry:** `portfolio_configs/registry.json`
- **Vet winner (run 23):** `SwingBreakout5DayStrategy` + `VolatilityExitStrategy`
- **Economics:** Return **−98%**, max DD **100%** — catastrophic
- **Export:** `portfolio_configs/portfolio-blue.json` — **`export_kind: observation`**
- **Follow-up:** membership/strategy revisit ticket still open

### Portfolio Orange (built 2026-07-08)

- **Seed:** GLTR only
- **Markets (15):** AAPL, BITQ, COPR, FPA, GLTR, IBM, MSOS, NVDA, RXT, SMH, VXX, WMT, XLF, XLK, ZROZ
- **Diversification:** Strong (mean \|r\| ≈ 0.171)
- **Sidecar:** `portfolio_configs/portfolio-orange-sidecar.json`
- **Vet winner (opt#33 / PBR 41, 2026-07-09):** `Breakout5DayStrategy` + paired opposite `Breakout5DayStrategy`
- **Economics (validation):** Return **+7.2%**, max DD **96%**, trades 1912, Sharpe null
- **Export:** `portfolio_configs/portfolio-orange.json` — **`export_kind: observation`** (failed drawdown gate ≤50%)

### Portfolio White (built 2026-07-08)

- **Seed:** CPER only
- **Markets (20):** CIZ, CMDT, COPR, CPER, DBE, GOOGL, IWF, OILK, PHYMF, PPLT, PTF, ROKU, SOXX, TAGS, TESL, TILL, WMT, XLB, YOLO, ZROZ
- **Diversification:** mean \|r\| ≈ 0.105 (low pairwise correlation)
- **Sidecar:** `portfolio_configs/portfolio-white-sidecar.json`
- **Vet winner (opt#36 / PBR 40, 2026-07-09):** `Breakout50DayStrategy` + `VolatilityExitStrategy`
- **Economics (validation):** Return **+7.3%**, max DD **94%**, trades 738, Sharpe null
- **Export:** `portfolio_configs/portfolio-white.json` — **`export_kind: observation`** (failed drawdown gate ≤50%)

### Bilateral overlaps (all ≤25%)

| Pair | Shared | Fractions |
|------|--------|-----------|
| Red ∩ Blue | ∅ | 0% / 0% |
| Red ∩ Orange | MSOS, VXX | 22.2% / 13.3% |
| Red ∩ White | PHYMF, ROKU | 22.2% / 10.0% |
| Blue ∩ Orange | RXT, WMT | 18.2% / 13.3% |
| Blue ∩ White | GOOGL, WMT | 18.2% / 10.0% |
| Orange ∩ White | COPR, WMT, ZROZ | 20.0% / 15.0% |

Candidate pool expanded beyond DM-suitable-only (WUT markets with `DmCoverage` ≥1000 bars) because suitable-only pools cap builds under overlap rules.

## Next steps

Tracked in `portfolio-overlap-rebuild.md.tasks.json` and `docs/tickets/2026-07-07-*.md`.

| # | Item | Ticket | Priority |
|---|------|--------|----------|
| 1 | Recreate compose `data_manager` on latest image | [recreate-data-manager](../docs/tickets/2026-07-07-recreate-data-manager-compose-container.md) | **Done** |
| 5 | **Portfolio trading-strategy evaluation framework** | [evaluation-framework](../docs/tickets/2026-07-07-portfolio-trading-strategy-evaluation-framework.md) | **P0 ~90%** |
| 2 | Vet Portfolio Red | [vet-red](../docs/tickets/2026-07-07-vet-portfolio-red-trend.md) | **Done** (PBR 25, observation) |
| 3 | Revisit Blue membership/strategy | [revisit-blue](../docs/tickets/2026-07-07-revisit-portfolio-blue-membership-strategy.md) | open |
| 4 | Build Orange + White | [orange-white](../docs/tickets/2026-07-07-build-portfolio-orange-white.md) | **Done** (membership); vet pending |
| 6 | Vet Orange + White (`portfolios:vet_trend`) | orange-white ticket Phase D | **Done** (both observation) |

### Completed

1. ~~Rebuild Red~~ — done
2. ~~DM random batch~~ — suitable 51 ≥50 gate
3. ~~Blue vetting~~ — done (observation only)
4. ~~Red vetting~~ — done (PBR 25; observation — DD gate)
5. ~~DM compose recreate~~ — symbol registry rakes work via compose
6. ~~Eval framework core~~ — gates, export_kind, null-Sharpe fallback, RANKING_METRIC
7. ~~Orange + White membership~~ — done 2026-07-08
8. ~~Orange + White vet_trend~~ — done 2026-07-09 (both observation; DD gate)

## Phase 1 — Controls (WUT)

- `PortfolioOverlapPolicy` — seed exclusivity + bilateral overlap math
- `PortfolioRegistry` — reads/writes `portfolio_configs/registry.json` for finalized portfolios
- Extend `PortfolioCorrelationBuilder` to filter candidates during greedy selection
- Extend rake env: `PEERS` (comma-separated portfolio names to check overlap against)

## Phase 2 — Data Sets UI pagination

- Paginate `DataSetsController#index` at **15 markets per page** (same pattern as `PortfolioBuilderController#paginate_collection`)
- Update `data_sets/index.html.erb` with page controls
- Preserve `q`, `market_tab`, and `page` in link params

## Phase 3 — Expand historical data (DM)

- Run `dm:symbol_registry:acquire_random_batch[300]` via compose (never one-off podman volumes)
- Target ≥30 suitable symbols before Red/Blue rebuild; ≥50 before Orange/White (aspirational — builds may use expanded WUT coverage pool)
- Suitability evaluated post-acquire per `ecosystem/docs/business-context/winston-market-suitability.md`

## Phase 4 — Rebuild Portfolio Red

```bash
env NAME="Portfolio Red" SEED=AMAT MIN=7 MAX=9 \
  CANDIDATES="..." PEERS="" \
  SIDECAR_PATH=/portfolio_configs/portfolio-red-sidecar.json \
  bin/rails portfolios:build_correlation
```

- AMAT seed only; exclude TSMC, GLTR, CPER from candidates
- Register in `portfolio_configs/registry.json`

## Phase 5 — Rebuild Portfolio Blue

```bash
env NAME="Portfolio Blue" SEED=TSMC MIN=9 MAX=11 \
  CANDIDATES="..." PEERS="Portfolio Red" \
  SIDECAR_PATH=/portfolio_configs/portfolio-blue-sidecar.json \
  bin/rails portfolios:build_correlation
```

- TSMC seed only; exclude AMAT, GLTR, CPER
- ≤25% bilateral overlap vs finalized Red

## Phase 6 — Vet + export

- Re-run `portfolios:vet_trend` for Red and Blue
- Export configured portfolios to `portfolio_configs/` and Wv2 when ready
- **Gate:** `export_kind` must be `trade_ready` before live capital; `observation` allowed for paper

## Phase 7 — Strategy evaluation doctrine

Canonical docs:

- `docs/analysis/portfolio-trading-strategy-evaluation.md`
- `docs/business-context/trade-ready-viability-gates.md`

WUT implementation:

| Piece | Status |
|-------|--------|
| `FIRST_PASS_BASE_CONFIG` + 6×2 exit grid | Done |
| Screening defaults (25% / top 5) | Done |
| `TradeReadyViabilityGates` | Done |
| `export_kind` on JSON export | Done |
| Null-Sharpe → total_return ranking fallback | Done |
| `RANKING_METRIC` env on `vet_trend` | Done |
| Blue membership post-mortem | Open (ticket #3) |

## Phase 8 — Orange + White

```bash
env NAME="Portfolio Orange" SEED=GLTR MIN=12 MAX=15 \
  PEERS="Portfolio Red,Portfolio Blue" \
  CANDIDATES="..." SIDECAR_PATH=/portfolio_configs/portfolio-orange-sidecar.json \
  bin/rails portfolios:build_correlation

env NAME="Portfolio White" SEED=CPER MIN=16 MAX=20 \
  PEERS="Portfolio Red,Portfolio Blue,Portfolio Orange" \
  CANDIDATES="..." SIDECAR_PATH=/portfolio_configs/portfolio-white-sidecar.json \
  bin/rails portfolios:build_correlation
```

Vet with `portfolios:vet_trend` after membership locked; label exports via viability gates.

## Deferred

- Wv2 paper-trading gaps (auto-execute, pyramid, etc.)
- Wv2 import for Red/Blue — observation only until gates pass (or membership/strategy revisit)
- Parallel combo optimization (Phase 3 of accelerate ticket)

## Commands reference

```bash
# DM — ALWAYS use compose (never one-off `podman run` with custom volumes)
# Recreate on latest image after any DM code changes (e.g. symbol registry):
#   (stop ai dependents first if they block container removal)
podman stop winston_mcp nanobot_cromwell || true
podman rm -f data_manager data_manager_sidekiq
./bin/compose build data_manager data_manager_sidekiq
./bin/compose up -d data_manager data_manager_sidekiq
./bin/compose exec -T data_manager bin/rails db:migrate
./bin/compose exec -T data_manager bin/rails dm:symbol_registry:summary

# Normal ops
./bin/compose exec -T data_manager bin/rails dm:symbol_registry:acquire_random_batch[300]
./bin/compose exec -T data_manager bin/rails dm:symbol_registry:summary

# Verify volume is the correct one (sawtooth_sawtooth_dm_data) after recreate:
#   podman inspect data_manager --format '{{range .Mounts}}{{.Name}} -> {{.Destination}}{{end}}'

# WUT — build + vet
./bin/compose exec -T winston_unit_test env NAME="Portfolio Blue" SEED=TSMC ... bin/rails portfolios:build_correlation
./bin/compose exec -T winston_unit_test env PORTFOLIO="Portfolio Red" \
  EXPORT=/portfolio_configs/portfolio-red.json RANKING_METRIC=practical_sharpe_ratio \
  bin/rails portfolios:vet_trend
```
