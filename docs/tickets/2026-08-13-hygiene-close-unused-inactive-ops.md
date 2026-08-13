# Ticket: Hygiene-close unused inactive Mint/Yellow/Blue leftovers

**Status:** Proposed  
**Priority:** P3  
**Date:** 2026-08-13  
**Monolith:** winston_v2  
**See:** session [`2026-08-13-1528-turtle-paper-handoff.md`](../session-reports/2026-08-13-1528-turtle-paper-handoff.md); ADR-006; issue `docs/issues/2026-07-28-wv2-portfolio-name-resolution-prefers-inactive-and-mutex-recovery-misguide.md`

## Problem

Unused **inactive, never-engaged** (or leftover successor) rows still sit in Wv2 and confuse name resolution:

| OP | Name | Notes |
|----|------|--------|
| #311 | Mint · 3749c990 | Elephant-era; 0 journals |
| #382 | Mint · 91608a22 | S4 pack unused; 0 journals |
| #330 | Yellow · 92776cfd | Elephant-era; 0 journals |
| #241 | Blue · 9cf64e64 | Duplicate successor leftover |

Not required for the Turtle handoff. Soft-close (paper) is enough — do **not** delete engaged history.

## Scope

1. Confirm each is inactive, not Active, and operator still wants them retired.  
2. Paper soft-close (`PortfolioCloseService`).  
3. Do **not** close #384, #797, #798, #308, #381, #385, #11.

## Acceptance

- [ ] Listed leftovers `closed_at` set, `active=false`  
- [ ] Vague `"Portfolio Mint"` / `"Portfolio Yellow"` still resolve to the intended Active series  

## Non-goals

- Hard delete  
- Touching engaged Active OPs  
