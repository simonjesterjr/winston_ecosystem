# Ticket: Quiver Tracking paper population / weighting forms

**Status:** Done  
**Priority:** P1  
**Date:** 2026-08-21  
**Monoliths:** winston_v2 (Wv2)  
**Depends on:** tracking page + PDF gap tasks  
**See:** plan [`quiver-tracking-desk.md`](../../../plans/quiver-tracking-desk.md); ADR-009 (Human-Gated)

## Problem

Gap tasks must be completable on `/quiver_tracking` with paper forms: add a market, drop a market, change weight/units. Same journal/confirm flow as the desk, **limited to tracking portfolios**. Not TF Daily Analysis drafts. Not Broker Gateway.

## Scope

1. Tracking-scoped pending list with confirm / skip (HITL reason required on skip).
2. Enter (add name + weight/units), exit (flatten name), reweight (same name, new weight). Fractional units.
3. Equity curve + positions + journals panels for the tracking OP only (reuse ops-shell patterns).
4. Manual “adjust population” when there is no PDF task (ad-hoc HITL), still tagged `quiver_tracking`.
5. Confirm does not place broker orders.

## Acceptance

- [x] Confirm add on empty OP creates Book + draft→executed journal + position
- [x] Confirm drop closes the lot
- [x] Reweight writes an audit/journal, does not mint a TF signal
- [x] `/operations` TF pending unchanged
- [x] Request specs for the three verbs

## Non-goals

- Desk Send / BG
- In-place mutation of TF OPs
