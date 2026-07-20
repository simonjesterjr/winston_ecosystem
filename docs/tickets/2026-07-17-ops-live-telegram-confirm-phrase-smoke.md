# Ticket: Live Telegram confirm-phrase smoke (when draft exists)

**Status:** Proposed  
**Date:** 2026-07-17  
**Source:** Session `2026-07-17-1257-mcp-smoke-shell-cash-parity.md`  
**Epic:** `2026-07-17-ops-daily-demo-epic.md`  
**Priority:** P2

## Problem

Demo smoke checklist skipped “Telegram: confirm phrase + one MCP mutation” for live **confirm** because no draft journals existed at smoke time. MCP mutations (cash/close/successor) were verified via tool handlers; the human Telegram confirm phrase path still needs one live pass when DA produces a draft.

## Scope

1. Wait for or trigger a paper DAR that creates a **draft** journal + operations task on an Active OP.  
2. From DAR / desk handoff / ops panel: copy Telegram phrase (`@sawtooth_nanobot confirm …`).  
3. Send in Telegram (or paste shell phrase without @mention into Ops UI).  
4. Confirm journal executes; capital/position update; record pass/fail on smoke checklist or this ticket.  
5. Out of scope: greenfield confirm service work (already exists).

## Acceptance

- [ ] One live confirm via Telegram phrase (or documented shell equivalent if bot busy)  
- [ ] Results table row added to `2026-07-17-ops-daily-demo-smoke-checklist.md` or this ticket  
- [ ] Failures open or update gap tickets  

## Related

- Smoke: `docs/tickets/2026-07-17-ops-daily-demo-smoke-checklist.md`  
- Session: `docs/session-reports/2026-07-17-1257-mcp-smoke-shell-cash-parity.md`  
- Human-gated desk: `docs/tickets/2026-07-16-human-gated-desk-actions.md`  
