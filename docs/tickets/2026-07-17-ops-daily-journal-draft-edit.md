# Ticket: Edit draft journal before confirm

**Status:** Proposed  
**Date:** 2026-07-17  
**Epic:** `2026-07-17-ops-daily-demo-epic.md`  

## Problem

Operators can view and confirm drafts but cannot amend draft units/price/notes/stop without console. Executed journals must remain immutable.

## Scope

1. Service: edit **draft only** fields (units, suggested price, notes, stop override in details).  
2. Internal API + ops shell `edit_journal <id> …`.  
3. Refuse executed/cancelled/passed.  
4. Specs.

## Acceptance

- [ ] Draft amendable from Ops UI  
- [ ] Executed journal edit refused  

## Related

- Journal confirmation path  
