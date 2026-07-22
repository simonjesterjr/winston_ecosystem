# Ticket: DAR attention for Active real process-miss Passed Signals

**Status:** Proposed  
**Priority:** P1  
**Date:** 2026-07-20  
**Series:** `adr-009-desk-fulfillment` **#6**  
**Domain:** ADR-009, attention bands  
**Glossary:** Passed Signal, Daily Activity Report, Active, Execution Mode

## Problem

Unconfirmed drafts past the action window become **Passed Signals**. On **Active real** OPs this is a **process miss** (stakeholder or market/clearing), not a strategy choice — must be unmistakable in DAR / ops attention. Today expire→passed exists; real-band process-miss surfacing is thin.

## Scope (Wv2)

1. Classify Passed Signals: `algorithmic` vs `process_miss` (e.g. `action_window_expired`).  
2. DAR summary + real band chapters: high-visibility section for process-miss on Active real.  
3. Desk Handoffs / next_steps include remediation (re-open? book late with force note? acknowledge?).  
4. Soft: Active paper process-miss lower urgency than real.  
5. PDF + markdown + payload fields for Cromwell.

## Non-goals

- Auto-retry fills  
- Treating process miss as algorithmic capacity pass  

## Acceptance

- [ ] Active real process-miss appears above routine paper noise in DAR  
- [ ] Reason and original signal/task ids retained  
- [ ] Attention band ordering still real → paper → inactive (ADR-006 / attention bands)  

## Related

- ADR-009, series #1 (window alignment)  
- `2026-07-16-attention-bands-dar-ops.md` (Done — foundation)  
- `ExpireStaleActionItemsService`  
