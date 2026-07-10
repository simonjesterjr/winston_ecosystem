# Ticket: Confirm first Portfolio Red pending action as paper

**Status:** Proposed  
**Date:** 2026-07-10  
**Context:** Session [`2026-07-09-1655-wv2-strategy-registry-daily-smoke`](../session-reports/2026-07-09-1655-wv2-strategy-registry-daily-smoke.md). Red is **Active** and evaluates cleanly; 2026-07-09 had zero signals. Paper loop is unproven end-to-end until a real task is confirmed.

## Problem

Daily analysis can create draft journals + `OperationsTask`s, but principals have not yet confirmed a Red action as paper. Without confirmation, tasks expire → `action_window_expired` passed signals (seen on old demo data).

## Scope

1. Wait for (or re-eval a historical date that produces) Red enter/exit `pending_actions`.
2. Confirm via MCP: `wv2_list_pending_actions` → `wv2_confirm_journal` / `wv2_mark_task_done` (paper execution mode).
3. Verify next analysis respects position/capital from confirmation.
4. Optional: exercise Cromwell `winston-confirmation-loop` skill when available.

## Acceptance

- At least one Red journal confirmed as paper (not real capital)
- Linked task status done/confirmed
- Subsequent daily analysis sees open position or updated capital_base as designed

## Related

- MCP: `wv2_confirm_journal`, `wv2_mark_task_done`, `wv2_list_pending_actions`
- Plan: `plans/cromwell-ai-skills-part2.md` Phase 2A
- Capital activation: `2026-07-09-capital-activation-mcp-telegram.md`
- Session: `2026-07-09-1655-wv2-strategy-registry-daily-smoke.md`
