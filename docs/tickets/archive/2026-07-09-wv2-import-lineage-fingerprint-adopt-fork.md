# Ticket: Wv2 import lineage (fingerprint / adopt / fork / engaged refuse)

**Status:** Done (2026-07-14 Phase 3 PR 2)

**Date:** 2026-07-09

**Context:** Session [`2026-07-09-1649-trading-strategy-fingerprint-wv2-lifecycle-grill`](../session-reports/2026-07-09-1649-trading-strategy-fingerprint-wv2-lifecycle-grill.md). **ADR-006**.  
**Plan:** [`plans/paper-telegram-phase3-adr006.md`](../../plans/paper-telegram-phase3-adr006.md) PR 2.

## Problem

Silent `find_or_initialize_by(name)` on Portfolio and TradingStrategy destroys regime samples and can reshape engaged series. ADR-006 requires fingerprint lineage.

## Scope

1. Store full fingerprint (+ WUT TS id) on OP and TS; display names `seed · shortFp` when fingerprint present.
2. Import resolution: same fingerprint → update (pre-engagement only); bare seed + matching Books → adopt/rename; else auto-fork.
3. Refuse shape mutation when OP is engaged (any Journal).
4. Store `seed_name` from JSON `name`; land always inactive; missing `export_kind` → observation.
5. Legacy no-fingerprint path remains bare-name (transition).
6. Specs + rewrite `wv2.rake` import (or extract service).

## Acceptance

- [x] Re-import new fingerprint does not overwrite prior OP journals
- [x] Same fingerprint re-import is idempotent pre-engagement
- [x] Engaged OP rejects methodology/Books overwrite via import
- [x] Conforms to ADR-006 and `wut-to-wv2-handoff.md`

## Delivered

- `Operations::PortfolioConfigImporter` — lineage service
- Wired: `wv2:portfolios:import` rake + `POST /internal/portfolios` (MCP transfer)
- Engaged bare-seed adopt target → auto-fork (does not reshape engaged OP)
- Specs: `spec/services/operations/portfolio_config_importer_spec.rb` (12 examples)
- Live smoke: legacy re-import of blue-pbr62 refused on engaged `#12` (journals + Active preserved)

## Related

- ADR-006, `wv2-operational-portfolio-lifecycle.md`
- Schema ticket: `2026-07-09-wv2-op-lifecycle-schema.md` (Done PR 1)
- export_kind ticket: `2026-07-08-wv2-importer-honor-export-kind.md` (folded into PR 2)
- Next: Active mutex PR 3 — `2026-07-09-wv2-active-mutex-seed-books.md`
