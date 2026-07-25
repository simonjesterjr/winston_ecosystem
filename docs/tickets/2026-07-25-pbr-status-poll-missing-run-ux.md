# Ticket: PBR status-poll UX when run HTML is missing (404)

**Status:** Proposed  
**Priority:** P3  
**Date:** 2026-07-25  
**Monolith:** winston_unit_test  
**Related:** session `ecosystem/docs/session-reports/2026-07-25-1310-pbr-fill-queue-pyramid-cash.md`; PBR new/show Turbo status polling; conf button / status HTML issues from 2026-07-25 lab session

---

## Problem

During lab runs, the PBR **status poll** can request run HTML or status endpoints for a run that never persisted, was deleted, or 404s. Current behavior is easy to misread as “stuck” or a no-op confirm, rather than a clear empty/missing state.

Session notes: status HTML 404 and conf-button Turbo/click no-ops complicated operator trust when validating fill cadence and TS capture.

---

## Desired behavior

1. Poll detects 404 / missing run → stop spinning; show explicit **“run not found / not started”** (or last known error).
2. Confirm-entry path: if create failed, surface server error instead of silent no-op.
3. Prefer one durable status element (progress text + terminal reason) over raw fetch failures in console only.

---

## Acceptance

- [ ] Missing run: poll stops; user-visible terminal message
- [ ] Failed create/confirm: non-empty error path in UI
- [ ] Happy path unchanged (running → complete → redirect/refresh)
- [ ] No infinite poll on 404

---

## Out of scope

- Sidekiq job reliability (separate)
- Large `results_json` puma timeouts (existing ticket)
