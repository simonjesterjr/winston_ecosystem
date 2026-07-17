# Ticket: Signal → related instrument fill (e.g. equity signal, LEAP fill)

**Status:** Proposed  
**Date:** 2026-07-17  
**Epic:** `2026-07-17-ops-daily-demo-epic.md`  

## Problem

IBM may signal a 20-day breakout; operator buys 2028 LEAPs (or other related instrument) to honor the signal without the stock. Schema has `fulfillment_type` / `fulfillment_details` but product path is stock-centric.

## Scope

1. Confirm or book fill with `fulfillment_type=leap|option|proxy` + details (underlying, expiry, strike).  
2. Link to motivating signal/journal/task id when present.  
3. Position representation rules (units, stops) for non-stock — minimum viable.  
4. Non-goal: full options pricing engine.

## Acceptance

- [ ] Journal can record LEAP fill tied to equity signal context  
- [ ] capital_base / flow rules documented for that path  

## Related

- Journal vs trading ledger analysis  
