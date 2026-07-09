# Ticket: Wv2 import lineage (fingerprint / adopt / fork / engaged refuse)

**Status:** Proposed

**Date:** 2026-07-09

**Context:** Session [`2026-07-09-1649-trading-strategy-fingerprint-wv2-lifecycle-grill`](../session-reports/2026-07-09-1649-trading-strategy-fingerprint-wv2-lifecycle-grill.md). **ADR-006**. Current `wv2:portfolios:import` uses name-only upsert.

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

- Re-import new fingerprint does not overwrite prior OP journals
- Same fingerprint re-import is idempotent pre-engagement
- Engaged OP rejects methodology/Books overwrite via import
- Conforms to ADR-006 and `wut-to-wv2-handoff.md`

## Related

- ADR-006, `wv2-operational-portfolio-lifecycle.md`
- Schema ticket: `2026-07-09-wv2-op-lifecycle-schema.md`
- `winston_v2/lib/tasks/wv2.rake` import task
