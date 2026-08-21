# Ticket: Cromwell Telegram document → Quiver Tracking ingest

**Status:** Proposed  
**Priority:** P2  
**Date:** 2026-08-21  
**Monoliths:** winston_v2 (Wv2), ecosystem Cromwell / MCP  
**See:** `POST /internal/quiver_tracking/ingest` (already fail-closed); plan [`quiver-tracking-desk.md`](../../plans/quiver-tracking-desk.md); session [`docs/session-reports/2026-08-21-1629-quiver-tracking-wrap.md`](../session-reports/2026-08-21-1629-quiver-tracking-wrap.md)

## Problem

Tracking v1 web upload works. Telegram is specified as an **alternate** path. Wv2 already has `POST /internal/quiver_tracking/ingest` (no file → fail closed). Cromwell / nanobot does not yet take an inbound Telegram document and POST it there.

## Scope

1. Skill or MCP tool: operator sends a document in Telegram → bytes + optional as_of/operator → ingest POST.
2. Fail closed if no document; never invent holdings from Alt Filings.
3. Reply with tracking-desk URL and parse/task counts.
4. Do not put Quiver site credentials in Cromwell.

## Acceptance

- [ ] One Telegram document reaches the same ingest as web upload
- [ ] No file → error, no empty book
- [ ] Web upload remains the primary path

## Non-goals

- Scraping Quiver
- Auto-confirm gap tasks
