# Ticket: Wv2 importer honor export_kind (trade_ready vs observation)

**Status:** Proposed

**Date:** 2026-07-08

**Context:** Session [`2026-07-08-1744-portfolio-overlap-orange-white-eval-gates`](../session-reports/2026-07-08-1744-portfolio-overlap-orange-white-eval-gates.md). WUT now writes `export_kind` on portfolio JSON. Importer can still treat all configs as operational without distinguishing observation vs trade-ready. Extended by **ADR-006** / grill [`2026-07-09-1649`](../session-reports/2026-07-09-1649-trading-strategy-fingerprint-wv2-lifecycle-grill.md): `export_kind` is independent of **Active** and **Execution Mode**; **Capital Activation** to `real` requires trade_ready or force.

## Problem

Observation exports (e.g. Red DD 64%, Blue −98%) can be imported without a hard gate, risking accidental live promotion / Capital Activation.

## Scope

1. Parse `export_kind` on `wv2:portfolios:import`; store on OP.
2. Default observation (and missing kind) → inactive, **Execution Mode** paper.
3. Import never sets Active true from JSON alone.
4. **Capital Activation** to real requires trade_ready provenance or `FORCE_REAL` (see capital activation ticket).
5. Document in `portfolio_configs/README.md` + handoff + lifecycle docs.

## Acceptance

- Import of `observation` cannot open real capital without explicit force
- Import of missing `export_kind` treated as observation (safe default)
- Aligns with ADR-006 three axes (export_kind / Active / Execution Mode)

## Related

- `TradeReadyViabilityGates`, `trade-ready-viability-gates.md`, ADR-006
- Red/Blue sample exports in `portfolio_configs/`
- `2026-07-09-capital-activation-mcp-telegram.md`
