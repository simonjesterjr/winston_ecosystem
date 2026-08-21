# Ticket: Quiver Tracking PDF ingest + gap tasks

**Status:** Done  
**Priority:** P1  
**Date:** 2026-08-21  
**Monoliths:** winston_v2 (Wv2); Cromwell/Telegram alternate  
**Depends on:** [`2026-08-21-wv2-quiver-tracking-page.md`](2026-08-21-wv2-quiver-tracking-page.md)  
**See:** plan [`quiver-tracking-desk.md`](../../../plans/quiver-tracking-desk.md)

## Problem

The operator downloads a Quiver Strategies PDF (HITL) and needs Wv2 to store it like a Daily Activity Report (DAR), parse holdings, and mint tasks that close the gap vs the (initially empty) tracking book.

## Scope

1. Store uploads at `winston_v2/storage/reports/quiver_tracking/` (`wv2_qtrack_YYYYMMDD[_n].pdf` + sidecar json: as_of, sha256, operator, parse status). List on the tracking desk like `/operations/dars`.
2. Web upload on `/quiver_tracking` (primary).
3. Telegram **alternate**: document → Cromwell/MCP or internal POST to the same ingest. Fail closed if no file. Do not block v1 on Telegram if web works.
4. Parser: fixture-driven. Extract ticker, side (long/short), weight (`% of NAV` preferred). Unreadable rows → HITL task, do not guess.
5. Diff vs current tracking OP: add / drop / reweight / `dm_pull` / HITL. First PDF vs empty OP = all adds.
6. Tasks tagged `source=quiver_tracking`. Sidekiq for parse (ADR-005). Idempotent per PDF checksum.

## Acceptance

- [x] Fixture PDF (or synthetic holdings table) → expected legs spec
- [x] Empty OP + fixture → N add tasks, 0 TF pending leak
- [x] Re-upload same checksum does not duplicate tasks
- [x] PDF appears in the tracking list and can be re-opened
- [x] Parse failure creates HITL task, not a reconstructed filing book

## Non-goals

- Login scrape (separate plan/ticket)
- Using DM catalog as the target book
- Auto-confirm
