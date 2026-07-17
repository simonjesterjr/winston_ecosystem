# Ticket: Bulk risk actions (exit-all market, move-all pyramid stops)

**Status:** Proposed  
**Date:** 2026-07-17  
**Epic:** `2026-07-17-ops-daily-demo-epic.md`  

## Problem

Desk needs: close all lots for a market on an OP; move all pyramided stops for a market/OP. Today: single-position exit and single stop update only.

## Scope

1. `exit_all <portfolio> <symbol> price=P` — full lots open for symbol (human-gated, per-lot journals or one multi-lot policy — decide in impl).  
2. `stops <portfolio> <symbol> price=S` or `move_stops` — update all open lots for symbol.  
3. Wire shell + internal (+ MCP if thin).  
4. Specs: multi-lot paper OP.

## Acceptance

- [ ] One command flattens multi-lot market on paper OP  
- [ ] One command moves all stops for symbol on OP  

## Related

- PyramidStopAdjuster (confirm path partial)  
