# Ticket: Optional Wv2 import of Orange/White observation portfolios

**Status:** Proposed
**Priority:** P3

**Date:** 2026-07-09

**Context:** Session [`2026-07-09-1308-orange-white-vet-trend`](../session-reports/2026-07-09-1308-orange-white-vet-trend.md). Exports:

- `portfolio_configs/portfolio-orange.json` — `export_kind: observation`
- `portfolio_configs/portfolio-white.json` — `export_kind: observation`

Red/Blue already labeled observation. Importer must honor `export_kind` (see related ticket).

## Problem

Operator may want paper/regime observation in Wv2 for Orange/White without implying live capital.

## Scope

1. Confirm Wv2 import path refuses live promotion for `observation` (or documents paper-only).
2. Import Orange and/or White via shared volume / rake as paper Operational Portfolios.
3. Smoke daily analysis skip/safe path for observation portfolios.
4. Do **not** treat as trade-ready capital.

## Acceptance

- Portfolios visible in Wv2 as observation/paper
- No path to live capital without re-export as `trade_ready`
- Documented command + result in session note or plan

## Related

- Ticket: `2026-07-08-wv2-importer-honor-export-kind.md`
- Business-context: `docs/business-context/trade-ready-viability-gates.md`
- Session: `docs/session-reports/2026-07-09-1308-orange-white-vet-trend.md`
