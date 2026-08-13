# Ticket: Handoff Mint+TS#77 and Yellow+TS#75 as observation OPs

**Status:** Done — imported + activated 2026-08-13  
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

- [x] Two OP rows in Wv2 with distinct fingerprints  
- [x] Landed inactive paper (ADR-006); activated after audit (Yellow no force; Mint `FORCE` vs #384)  
- [x] strategy audit ok (ladder N/A for static 1%)  
- [x] Document export paths under `portfolio_configs/`  

**Landed 2026-08-13 (path B):**

| Seed | WUT | Export | Wv2 OP | TS | Fingerprint |
|------|-----|--------|--------|----|-------------|
| Mint S2 | PBR 432 / WUT TS#77 | `portfolio_configs/portfolio-mint-turtle-s2-ts77.json` | **#797** | Wv2 #266 | `85730621` |
| Yellow S1 | PBR 433 / WUT TS#75 | `portfolio_configs/portfolio-yellow-turtle-s1-ts75.json` | **#798** | Wv2 #267 | `7aa73357` |

Both `export_kind=observation`, `execution_mode=paper`, `force_lab_uncapped` (Mint 10 / Yellow 17 books). Existing Mint **#384** kept Active (dual-seed force). Yellow S4 **#383** already closed.

Importer trap: export `risk_percentage: 1.0` became stored 100 (1.0 treated as fraction). Patched OPs to stored `1.0` = 1%. PositionSizer now treats `>= 1.0` as percent. JSON files use `0.01` so re-import stores 1.0.

## Non-goals

- Real capital activation  
- Blue under this chassis  
