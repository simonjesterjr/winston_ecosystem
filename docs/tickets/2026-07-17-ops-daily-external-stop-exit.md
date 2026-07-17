# Ticket: External stop / discretionary exit packaging

**Status:** Proposed  
**Date:** 2026-07-17  
**Epic:** `2026-07-17-ops-daily-demo-epic.md`  

## Problem

Stops can hit outside Winston without a Winston exit signal. Ad-hoc `exit` covers fill, but lacks first-class reason packaging so DAR/journal hygiene doesn’t look like a miss.

## Scope

1. Ad-hoc exit accepts `reason=external_stop|discretionary|…` (notes + fulfillment_details).  
2. Optional ops shell / desk field.  
3. Document speech: “AMZN stopped out — book exit, no Winston signal.”  
4. Non-goal: broker stop sync.

## Acceptance

- [ ] Exit journals carry machine-readable external-stop reason  
- [ ] Operator path documented for Ops UI + Telegram  

## Related

- Ad-hoc exit Done: `2026-07-16-mcp-exit-trade-and-skill.md`  
