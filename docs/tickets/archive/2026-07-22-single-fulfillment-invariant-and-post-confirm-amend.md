# Ticket: Single-fulfillment invariant + post-confirm amend

**Status:** Done  
**Priority:** P1  
**Date:** 2026-07-22  
**Domain:** ADR-009 Fulfillment, Desk Workflow, Booked Capital Spine  
**Glossary:** Journal, Desk Action, Signaled Entry Rule, Fulfillment  
**Monoliths:** **Wv2** (ops); MCP/desk UX  

## Problem

Orange WMT (2026-07-22): signal task **84** was confirmed via desk workflow (journal **105** @ 109.89). Operator then used desk **enter** intending to correct price → ad-hoc journal **119** @ 109.53 opened a **second** short lot. Product treated “re-enter” as a new fulfillment.

Winston should own **one fulfillment per signal leg**. Confirm ends the draft phase, not the identity of the work item. Post-confirm price/qty corrections must **amend** the same journal/lot (or explicit reverse), never silent double open.

## Scope

### A — Guards (shipped)

1. If `signal_task_id` / linked journal already `draft` or `executed` / task `completed`, refuse default ad-hoc enter (`force` + notes only).  
2. Desk Workflow / desk form deep link for executed open-lot journal → **correct_fill**, not confirm-as-new.  
3. Specs for double-book refusal.

### B — Post-confirm amend (shipped; corrective semantics)

1. `JournalExecutedAmendService` — amend executed enter/pyramid journal + open position (price, units, stop, notes) with `fulfillment_details.amendments` audit.  
2. Recomputes `flow` / capital impact.  
3. Desk Workflow + classic desk `correct_fill`; internal `POST /internal/journals/amend`; MCP `wv2_amend_journal`.  
4. Specs + live smoke on Orange WMT.

### C — Ops cleanup

- Accidental WMT pos #50 / journal #119 **deleted** 2026-07-22 (kept A: pos #48 / j#105 @ 109.89).

## Acceptance

- [x] Cannot open a second lot against a completed signal task without force  
- [x] Completed task UI does not look like a fresh confirm (correct-fill form)  
- [x] (B) Executed fill price/qty correctable without second Position  
- [x] Specs green (28 examples); no DA auto-fill introduced  

## Implementation notes

| Piece | Path |
|-------|------|
| Guard | `winston_v2/app/services/operations/single_fulfillment_guard.rb` |
| Amend service | `winston_v2/app/services/operations/journal_executed_amend_service.rb` |
| Ad-hoc book | `ad_hoc_paper_fill_service.rb` — calls guard |
| Desk | `desk_workflows_controller`, `desk_actions_controller`, views |
| Internal API | `POST /internal/journals/amend` |
| MCP | `wv2_amend_journal` in `ecosystem/ai/mcp/mcp_winston/server.py` (**rebuild winston_mcp** to pick up) |
| Specs | `single_fulfillment_guard_spec`, `journal_executed_amend_service_spec`, ad-hoc + workflow request specs |

**Error codes:** `signal_draft_exists`, `signal_already_fulfilled`, `force_requires_notes`

**Amend semantics locked (pre-grill pragmatic choice):** corrective rewrite same lot; superseding append-only journals deferred.

## Related

- Analysis: `docs/analysis/2026-07-22-winston-fulfillment-ownership-and-broker-intake.md`  
- Broker intake: `docs/tickets/2026-07-21-broker-confirmation-email-api-intake.md`  
- ADR-009 / human-gated desk business-context  
- Journal draft edit (pre-confirm) already partial  
