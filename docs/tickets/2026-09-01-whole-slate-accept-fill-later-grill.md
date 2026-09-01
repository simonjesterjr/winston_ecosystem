# Ticket: Whole-slate accept-fill waits for a later grill

**Status:** Proposed  
**Priority:** P3  
**Date:** 2026-09-01  
**Mode:** contractor  
**Graph nodes:** ecosystem, winston_v2  
**Human gates:** Grill 2026-09-01 Q12 **D** — no implied successor date  
**DoD:** This ticket is not started until a new grill locks Q11-C  
**Related:** [`2026-09-01-slate-automation-accept-fill-adr.md`](2026-09-01-slate-automation-accept-fill-adr.md)  
**Origin:** [`docs/session-reports/2026-09-01-1601-ibkr-paper-and-slate-grill.md`](../session-reports/2026-09-01-1601-ibkr-paper-and-slate-grill.md)

## Problem

Discovery Accept-Fill books **matched protective Working Stop prints only**. Whole-slate accept-fill (entries and pyramids auto-book from Trade Notifications) is glossary aspiration. Operator forbade promoting it because a paper week went well or because someone said “soon.”

## Scope

Do **not** implement. Keep this ticket as the reminder:

1. Reopen only via `/grill-with-docs`.  
2. Required before C: resting-touch fingerprint (Q7) is still recommended in CONTEXT; Q12-D means even that is not a calendar.  
3. Packaging surprises stay Confirm until C is locked.

## Non-goals

- Any accept-fill of entries/pyramids in discovery  
- A scheduled promotion date  

## Acceptance

- [ ] Later grill locks Q11-C **or** this ticket is cancelled/superseded in writing  
- [ ] No code path auto-books slate entries while this ticket is Proposed
