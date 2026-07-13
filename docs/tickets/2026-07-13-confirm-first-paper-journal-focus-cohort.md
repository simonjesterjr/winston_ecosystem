# Ticket: Confirm first paper journal on paper-focus cohort

**Status:** Proposed  
**Date:** 2026-07-13  
**Blocked by:** cohort choice + hygiene (`2026-07-13-paper-first-cohort-decision.md`, `2026-07-13-paper-focus-active-hygiene-and-recipe.md`)  

## Context

Paper execution loop is still unproven end-to-end (draft journals / tasks without principal confirm). Historical ticket targeted **Red** specifically ([`2026-07-10-confirm-first-red-paper-pending-action.md`](./2026-07-10-confirm-first-red-paper-pending-action.md)). Paper-first work may shift focus to **Green 55** or **Blue 62**; first confirm should follow the **chosen focus seed**, not necessarily Red.

## Scope

1. After focus OP is Active with correct recipe and paper intent: wait for or re-eval a date that yields enter/exit `pending_actions`.  
2. Confirm via MCP: `wv2_list_pending_actions` → `wv2_confirm_journal` / `wv2_mark_task_done` (**paper** execution mode only).  
3. Verify next daily analysis respects position / capital_base from confirmation.  
4. Optional: Cromwell `winston-confirmation-loop` when available.  
5. If focus remains Red, this ticket and the 2026-07-10 Red ticket may be closed together after one successful confirm.

## Acceptance

- [ ] At least one journal confirmed as **paper** on the **paper-focus** OP (not real capital)  
- [ ] Linked task done/confirmed  
- [ ] Subsequent analysis sees open position or updated capital as designed  
- [ ] Real capital still out of scope  

## Related

- Red-specific predecessor: `2026-07-10-confirm-first-red-paper-pending-action.md`  
- Paper-first policies: `2026-07-13-paper-first-cohort-decision.md`  
- Hygiene/import: `2026-07-13-paper-focus-active-hygiene-and-recipe.md`  
- MCP: `wv2_confirm_journal`, `wv2_mark_task_done`, `wv2_list_pending_actions`  
- Session: `docs/session-reports/2026-07-13-1741-paper-first-cohort-partial.md`  
