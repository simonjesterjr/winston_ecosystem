# Ticket: Confirm first Portfolio Red pending action as paper

**Status:** Superseded (2026-07-14) — paper focus is Blue 62 (`Portfolio Blue · PBR62` #12); first paper journal confirmed there (`2026-07-13-confirm-first-paper-journal-focus-cohort.md`).  
**Date:** 2026-07-10  
**Context:** Session [`2026-07-09-1655-wv2-strategy-registry-daily-smoke`](../session-reports/2026-07-09-1655-wv2-strategy-registry-daily-smoke.md). Red was the original candidate; Phase 0 chose Blue 62 instead.

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

- Prefer if paper focus is not Red: `2026-07-13-confirm-first-paper-journal-focus-cohort.md` (generalized; close this ticket together if Red remains focus and one confirm satisfies both)
- MCP: `wv2_confirm_journal`, `wv2_mark_task_done`, `wv2_list_pending_actions`
- Plan: `plans/cromwell-ai-skills-part2.md` Phase 2A
- Capital activation: `2026-07-09-capital-activation-mcp-telegram.md`
- Session: `2026-07-09-1655-wv2-strategy-registry-daily-smoke.md`
