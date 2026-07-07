# Portfolio Overlap Controls and Rebuild Plan

**Status:** Active  
**Updated:** 2026-07-06

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

## Status (2026-07-06)

| Phase | Status |
|-------|--------|
| 1 — Overlap controls | Done (`PortfolioOverlapPolicy`, `PortfolioRegistry`, builder + rake) |
| 2 — Data Sets pagination | Done (15/page) |
| 3 — DM random acquisition | **Done** — 300 acquired via one-off `podman run` on latest image (2026-07-06) |
| 4 — Rebuild Red | **Done** — see below |
| 5 — Rebuild Blue | **Done** — see below |
| 6 — Vet + export | Blue vetted + exported (`portfolio-blue.json`, run 23) |

### Portfolio Red (rebuilt)

- **Seed:** AMAT only (no TSMC, GLTR, CPER)
- **Markets (9):** AMAT, CDE, MSFT, MSOS, PHYMF, ROKU, URA, VXX, XLV
- **Overlap vs Blue:** 0 shared (0% bilateral)
- **Diversification:** Strong (mean \|r\| ≈ 0.21)
- **Sidecar:** `portfolio_configs/portfolio-red-sidecar.json`

### Portfolio Blue (rebuilt)

- **Seed:** TSMC only (no AMAT, GLTR, CPER)
- **Markets (11):** AAL, AMZN, GLD, GOOGL, JNJ, PG, RXT, TSLA, TSMC, WMT, XLE
- **Overlap vs Red:** 0 shared (0% bilateral)
- **Diversification:** Strong (mean \|r\| ≈ 0.12)
- **Sidecar:** `portfolio_configs/portfolio-blue-sidecar.json`
- **Registry:** `portfolio_configs/registry.json`

Candidate pool had to expand beyond the 15 DM-suitable symbols (WUT markets with `DmCoverage` ≥1000 bars, excluding peer effective membership and alien seeds) because the suitable-only pool capped builds at 8 markets under overlap rules.

## Next steps

Tracked in `portfolio-overlap-rebuild.md.tasks.json` and `docs/tickets/2026-07-07-*.md`.

| # | Item | Ticket | Priority |
|---|------|--------|----------|
| 1 | Recreate compose `data_manager` on latest image | [recreate-data-manager](../docs/tickets/2026-07-07-recreate-data-manager-compose-container.md) | — |
| 5 | **Portfolio trading-strategy evaluation framework** | [evaluation-framework](../docs/tickets/2026-07-07-portfolio-trading-strategy-evaluation-framework.md) | **P0** |
| 2 | Vet Portfolio Red | [vet-red](../docs/tickets/2026-07-07-vet-portfolio-red-trend.md) | blocked by #5 |
| 3 | Revisit Blue membership/strategy | [revisit-blue](../docs/tickets/2026-07-07-revisit-portfolio-blue-membership-strategy.md) | blocked by #5 |
| 4 | Build Orange + White (suitable ≥50) | [orange-white](../docs/tickets/2026-07-07-build-portfolio-orange-white.md) | blocked by #1, #5 |

### Completed

1. ~~Rebuild Red~~ — done
2. ~~DM random batch~~ — done (300 ok, 0 failed; suitable 15→18)
3. ~~Blue vetting~~ — done (winner: `SwingBreakout5DayStrategy` + `VolatilityExitStrategy`, run 23; economics poor — do not import to Wv2 yet)

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
- Target ≥30 suitable symbols before Red/Blue rebuild; ≥50 before Orange/White
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

## Deferred

- Orange (GLTR) and White (CPER) builds — see ticket `2026-07-07-build-portfolio-orange-white.md`
- Wv2 paper-trading gaps (auto-execute, pyramid, etc.)
- Wv2 import for Red/Blue — blocked until trading-strategy evaluation framework (P0 ticket)

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

# WUT
./bin/compose exec -T winston_unit_test env NAME="Portfolio Blue" SEED=TSMC ... bin/rails portfolios:build_correlation
./bin/compose exec -T winston_unit_test env PORTFOLIO="Portfolio Blue" bin/rails portfolios:vet_trend
```