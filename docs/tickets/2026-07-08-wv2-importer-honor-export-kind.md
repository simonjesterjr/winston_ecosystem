# Ticket: Wv2 importer honor export_kind (trade_ready vs observation)

**Status:** Proposed

**Date:** 2026-07-08

**Context:** Session [`2026-07-08-1744-portfolio-overlap-orange-white-eval-gates`](../session-reports/2026-07-08-1744-portfolio-overlap-orange-white-eval-gates.md). WUT now writes `export_kind` on portfolio JSON. Importer can still treat all configs as operational without distinguishing observation vs trade-ready.

## Problem

Observation exports (e.g. Red DD 64%, Blue −98%) can be imported without a hard gate, risking accidental live promotion.

## Scope

1. Parse `export_kind` on `wv2:portfolios:import`.
2. Default observation → inactive / paper-only flag if available.
3. Refuse or require explicit `FORCE_TRADE_READY=1` to activate `trade_ready` only when gates passed.
4. Document in `portfolio_configs/README.md` + handoff doc.

## Acceptance

- Import of `observation` cannot activate live capital without explicit override
- Import of missing `export_kind` treated as observation (safe default)

## Related

- `TradeReadyViabilityGates`, `trade-ready-viability-gates.md`
- Red/Blue sample exports in `portfolio_configs/`
