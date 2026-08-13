# Ticket: Human cleanup of open residue on closed paper OPs #6 and #383

**Status:** Proposed  
**Priority:** P3  
**Date:** 2026-08-13  
**Monolith:** winston_v2  
**See:** session [`2026-08-13-1528-turtle-paper-handoff.md`](../session-reports/2026-08-13-1528-turtle-paper-handoff.md); ADR-006 paper soft-close

## Problem

Path B paper soft-close left **open lots** on series that no longer receive signals:

| OP | Name | Open residue | Journals kept |
|----|------|--------------|---------------|
| #6 | Orange · 6622b2eb | **11** | 29 |
| #383 | Yellow · 2a97a043 | **9** | 28 |

Closed at 2026-08-13T21:17:24Z. History must stay. Residue can clutter blotter if closed OPs are not filtered.

## Scope

1. Confirm ops/DAR already hide closed-OP lots (if yes, document and close this ticket).  
2. If lots still appear as desk work: human flatten or mark residue-on-closed — **do not** invent Daily Analysis exit signals.  
3. Prefer Unsignaled Exit Allowance + reason `series_closed` (or equivalent) if booking exits.

## Acceptance

- [ ] Operator can scan Active blotter without #6 / #383 lots as current work  
- [ ] Journals/history on those OPs still queryable  

## Non-goals

- Deleting journals  
- Flattening as if the series were still in DA  
