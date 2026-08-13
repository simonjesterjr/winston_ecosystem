# Ticket: First Daily Analysis on Turtle Mint S2 + Yellow S1

**Status:** Proposed  
**Priority:** P1  
**Date:** 2026-08-13  
**Monolith:** winston_v2  
**See:** handoff [`2026-08-13-handoff-mint-s2-yellow-s1-observation.md`](2026-08-13-handoff-mint-s2-yellow-s1-observation.md); session [`2026-08-13-1528-turtle-paper-handoff.md`](../session-reports/2026-08-13-1528-turtle-paper-handoff.md)

## Problem

#797 Mint · 85730621 (Turtle S2) and #798 Yellow · 7aa73357 (Turtle S1) are Active paper but have **not** been through Daily Analysis (DA). No drafts, tasks, or Daily Activity Report (DAR) rows yet.

## Scope

1. Run `wv2:portfolios:evaluate` (or wait for scheduled DA) covering the current Active set.  
2. Confirm #797 / #798 / #384 all appear (dual-Active Mint must stay distinct).  
3. Spot-check sizing is **1%** of risk equity on the Turtle OPs, **2%** on #384.  
4. Note any `missing_data` / `unsupported_strategy` skips (Breakout10 / Breakout55 must resolve).

## Acceptance

- [ ] DA result rows for #797 and #798 (evaluated or explicit skip reason)  
- [ ] DAR / ops shell lists both new OPs under paper band  
- [ ] No 100% unit-size on Turtle drafts  

## Non-goals

- Desk confirm / fills  
- Real capital  
