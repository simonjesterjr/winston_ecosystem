# Ticket: Wv2 importer honor export_kind (trade_ready vs observation)

**Status:** Done (2026-07-14 Phase 3 PR 2 — folded into import lineage)

**Date:** 2026-07-08

**Context:** Session [`2026-07-08-1744-portfolio-overlap-orange-white-eval-gates`](../session-reports/2026-07-08-1744-portfolio-overlap-orange-white-eval-gates.md). WUT now writes `export_kind` on portfolio JSON. Extended by **ADR-006** / grill [`2026-07-09-1649`](../session-reports/2026-07-09-1649-trading-strategy-fingerprint-wv2-lifecycle-grill.md).  
**Plan:** [`plans/paper-telegram-phase3-adr006.md`](../../plans/paper-telegram-phase3-adr006.md) PR 2.

## Problem

Observation exports (e.g. Red DD 64%, Blue −98%) can be imported without a hard gate, risking accidental live promotion / Capital Activation.

## Scope

1. Parse `export_kind` on `wv2:portfolios:import`; store on OP.
2. Default observation (and missing kind) → inactive, **Execution Mode** paper.
3. Import never sets Active true from JSON alone.
4. **Capital Activation** to real requires trade_ready provenance or `FORCE_REAL` (see capital activation ticket).
5. Document in `portfolio_configs/README.md` + handoff + lifecycle docs.

## Acceptance

- [x] Import of missing `export_kind` treated as observation (safe default)
- [x] Import never sets Active true from JSON (`active: true` in JSON ignored)
- [x] Aligns with ADR-006 three axes (export_kind / Active / Execution Mode stored independently)
- [ ] Capital Activation trade_ready gate — deferred to capital-activation ticket
- [ ] portfolio_configs README note — optional doc polish

## Delivered

- `Operations::PortfolioConfigImporter#normalized_export_kind` stores `observation` | `trade_ready`
- Always lands `execution_mode=paper` on create; `active=false` always on import

## Related

- `TradeReadyViabilityGates`, `trade-ready-viability-gates.md`, ADR-006
- Import lineage: `2026-07-09-wv2-import-lineage-fingerprint-adopt-fork.md`
- `2026-07-09-capital-activation-mcp-telegram.md` (trade_ready gate on real)
