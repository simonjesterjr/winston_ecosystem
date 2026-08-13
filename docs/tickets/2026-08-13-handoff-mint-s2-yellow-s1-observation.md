# Ticket: Handoff Mint+TS#77 and Yellow+TS#75 as observation OPs

**Status:** Proposed  
**Priority:** P1  
**Date:** 2026-08-13  
**Monoliths:** winston_unit_test → winston_v2  
**See:** scorecard [`business_analysis/2026-08-12-turtle-hybrid-price-scorecard.md`](../../business_analysis/2026-08-12-turtle-hybrid-price-scorecard.md); session `2026-08-13-0850-turtle-walnut-risk-equity-wrap.md`

## Problem

Lab promote list is frozen (Mint **S2** TS#77; Yellow **S1** TS#75, no skip) but recipes are not yet **imported** to Wv2 as Operational Portfolios for paper observation.

## Scope

1. Export trade-ready or observation JSON from WUT (Mint+S2 fingerprint, Yellow+S1 fingerprint) with hybrid price-level fill + chassis knobs.  
2. Import to Wv2 **inactive** paper OPs (ADR-006).  
3. Recipe audit (entries/exits, pyramid 0.5N, no vol exit, fill cadence stamps).  
4. Optional: Activate paper only when operator ready — not auto.

## Acceptance

- [ ] Two OP rows in Wv2 with distinct fingerprints  
- [ ] inactive paper default  
- [ ] strategy audit ok (ladder N/A for static 1%)  
- [ ] Document export paths under `portfolio_configs/`  

## Non-goals

- Real capital activation  
- Blue under this chassis  
