# Ticket: Build Portfolio Orange and White

**Status:** Proposed

**Date:** 2026-07-07

**Context:** [`portfolio-overlap-rebuild`](../../plans/portfolio-overlap-rebuild.md). Red and Blue finalized in registry. Orange (GLTR, 12–15 markets) and White (CPER, 16–20 markets) not started.

**Gate:** Plan requires **≥50 suitable** symbols in DM registry before Orange/White builds. Current suitable count: **18** (after 300-symbol batch).

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

### Phase D — Vet (after trading-strategy framework)

Run `portfolios:vet_trend` for Orange and White only after viability criteria are defined.

## Acceptance

- Orange and White in WUT with seed exclusivity and ≤25% bilateral overlap vs all peers.
- Sidecars + registry updated.
- Suitable count logged when gate is met.

## Blocked by

- Suitable pool < 50 (Phase A)
- Trading-strategy evaluation framework (vetting economics)

## Related

- Plan task #4