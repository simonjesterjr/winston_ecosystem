# Ticket: Grill Quiver Tracking in-place membership vs ADR-006 successor

**Status:** Proposed  
**Priority:** P2  
**Date:** 2026-08-21  
**Monoliths:** ecosystem (CONTEXT / ADR-006), winston_v2 (Wv2)  
**See:** plan [`quiver-tracking-desk.md`](../../plans/quiver-tracking-desk.md) §7; ADR-006; session [`docs/session-reports/2026-08-21-1629-quiver-tracking-wrap.md`](../session-reports/2026-08-21-1629-quiver-tracking-wrap.md)

## Problem

v1 tracking **mutates membership in place** when a new PDF lands (add/drop/reweight). ADR-006 freezes Books on an **Engaged** Operational Portfolio until Close / successor. The plan flags this as a grill item before treating it as law.

## Scope

1. `/grill-with-docs` against ADR-006, CONTEXT **Rebalance** / **Engaged**, and the tracking plan.
2. Either: (A) explicit exception — tracking membership may mutate in place with PDF-ingest audit, or (B) each PDF is a successor OP.
3. Promote the choice to CONTEXT / ADR addendum. Align `QuiverTracking::Population` if code disagrees.

## Acceptance

- [ ] Written decision A or B
- [ ] CONTEXT (and ADR if irreversible) updated
- [ ] Code path matches the decision

## Non-goals

- Changing TF OP engagement rules
- Broker Gateway
