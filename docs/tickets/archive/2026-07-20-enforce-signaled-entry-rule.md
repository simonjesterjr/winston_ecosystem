# Ticket: Enforce Signaled Entry Rule on book-enter paths

**Status:** Done
**Completed:** 2026-07-21  
**Priority:** P1  
**Date:** 2026-07-20  
**Series:** `adr-009-desk-fulfillment` **#3**  
**Domain:** ADR-009  
**Glossary:** Signaled Entry Rule, Unsignaled Exit Allowance, Signal Spine

## Problem

Policy: **no enter/pyramid without a methodology-originated Winston signal** (DA draft or package leg). Confirm may change packaging/size/price but must reference the signal. Today `wv2_book_trade` / desk enter still allow naked free-form opens (transitional).

## Scope (Wv2 + MCP + skills)

1. Require `signal_journal_id` or pending enter/pyramid `task_id` on book/confirm enter (unless `force` + audit note).  
2. Reject or force-gate naked `AdHocPaperFillService` enter without signal.  
3. Exits remain unsignaled-capable (`external_stop`, etc.) — do not break exit path.  
4. Update Cromwell `winston-ad-hoc-fill` skill: prefer confirmation-loop; book-enter only when linked to signal or force.  
5. Specs for refuse / force paths; ops shell errors clear.

## Non-goals

- Human-authored “manual signal” records (grill rejected option B)  
- Changing Unsignaled Exit Allowance  

## Acceptance

- [x] Naked enter without signal fails without force  
- [x] Enter with signal_journal_id / task_id succeeds; packaging still overridable  
- [x] Force path logs audit note  
- [x] Skills/docs match ADR-009  

## Related

- ADR-009  
- `interfaces/winston-mcp-tools.md` (`wv2_book_trade`)  
- `ecosystem/ai/skills/winston-ad-hoc-fill/SKILL.md`  


## Delivered (2026-07-21)

- `AdHocPaperFillService` enforces Signaled Entry Rule (signal_journal_id / signal_task_id or force+notes).
- Wired force through internal book, desk form, ops shell.
- Specs for refuse / signal link / force audit; related-instrument specs updated.
- Cromwell skill `winston-ad-hoc-fill` prefers confirm; documents force path.
