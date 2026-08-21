# Ticket: Native PDF parser for Quiver Tracking Premium print-PDF

**Status:** Proposed  
**Priority:** P2  
**Date:** 2026-08-21  
**Monoliths:** winston_v2 (Wv2)  
**See:** [`plans/quiver-tracking-desk.md`](../../plans/quiver-tracking-desk.md); `winston_v2/spec/fixtures/quiver_tracking/FORMAT.txt`; session [`docs/session-reports/2026-08-21-1629-quiver-tracking-wrap.md`](../session-reports/2026-08-21-1629-quiver-tracking-wrap.md)

## Problem

v1 ingest **stores** the uploaded PDF but parses **JSON / CSV / HTML table** sidecars. A Premium Quiver Strategies print-to-PDF will not mint gap tasks unless the operator extracts the holdings table first.

## Scope

1. Decide: add a lightweight PDF text extractor **or** keep sidecar-only and document the extract step on the tracking desk.
2. If extractor: fixture a real (redacted) holdings PDF; map Ticker / side / `% of NAV`; unreadable rows stay HITL (no guessing).
3. Do not use the Quiver API or DM catalog as the target book.

## Acceptance

- [ ] Operator can upload a print-PDF **or** the desk tells them exactly how to extract
- [ ] Spec with a fixture PDF or an explicit non-goal + UI copy
- [ ] Unreadable rows still mint HITL, never a reconstructed filing book

## Non-goals

- Login scrape (`2026-08-21-quiver-pdf-bot-scrape.md`)
- Matching published CAGR
