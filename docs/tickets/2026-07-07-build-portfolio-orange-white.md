# Ticket: Build Portfolio Orange and White

**Status:** Membership done (2026-07-08); Phase D vet pending

**Date:** 2026-07-07

**Last updated:** 2026-07-08

**Context:** [`portfolio-overlap-rebuild`](../../plans/portfolio-overlap-rebuild.md). All four seed portfolios in registry.

**Gate:** ≥50 suitable **met** (suitable **51** after 3×300 acquire batches).

## Problem

Cannot assemble Orange/White with overlap controls and sufficient candidate diversity at current suitable pool size.

## Scope

### Phase A — Grow suitable pool

1. Ensure compose `data_manager` on latest image (see recreate ticket).
2. Run 1–2 more `dm:symbol_registry:acquire_random_batch[300]` via compose.
3. Target ≥50 suitable before Orange build; reassess for White (16–20 markets needs broader pool).

### Phase B — Build Orange (GLTR)

```bash
env NAME="Portfolio Orange" SEED=GLTR MIN=12 MAX=15 \
  PEERS="Portfolio Red,Portfolio Blue" \
  CANDIDATES="..." SIDECAR_PATH=/portfolio_configs/portfolio-orange-sidecar.json \
  bin/rails portfolios:build_correlation
```

- Exclude AMAT, TSMC, CPER from candidates.
- Register in `portfolio_configs/registry.json`.

### Phase C — Build White (CPER)

```bash
env NAME="Portfolio White" SEED=CPER MIN=16 MAX=20 \
  PEERS="Portfolio Red,Portfolio Blue,Portfolio Orange" \
  ...
```

### Phase D — Vet (pending)

```bash
env PORTFOLIO="Portfolio Orange" EXPORT=/portfolio_configs/portfolio-orange.json \
  bin/rails portfolios:vet_trend
env PORTFOLIO="Portfolio White" EXPORT=/portfolio_configs/portfolio-white.json \
  bin/rails portfolios:vet_trend
```

## Results (membership)

| Portfolio | Markets | Seed | mean \|r\| | Sidecar |
|-----------|---------|------|-----------|---------|
| Orange | 15 | GLTR | 0.171 | `portfolio-orange-sidecar.json` |
| White | 20 | CPER | 0.105 | `portfolio-white-sidecar.json` |

All bilateral overlaps ≤25%; seeds exclusive. See plan status table.

## Acceptance

- [x] Orange and White in WUT with seed exclusivity and ≤25% bilateral overlap vs all peers
- [x] Sidecars + registry updated
- [x] Suitable count ≥50 (51)
- [ ] Phase D vet + export_kind labeling

## Related

- Plan task #4 (membership completed), task #6 (vet)
- Perf fix this session: `MarketCorrelationCalculator` DmCoverage date bounds + process-level close series cache (greedy builds no longer multi-hour reloads)