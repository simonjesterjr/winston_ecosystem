# Ticket: Yellow OWDC + scale=none as paper candidate (from matrix)

**Status:** Proposed  
**Priority:** P2  
**Date:** 2026-07-31  
**Monolith:** WUT lab → Wv2 paper path  
**Session:** `docs/session-reports/2026-07-31-1556-risk-scale-matrix-findings.md`

---

## Problem

Among scale=none cells on Yellow 17-book pack:

| Base | PBR | Ret | Max DD | Sharpe |
|------|-----|-----|--------|--------|
| OWDC | **353** | **+176%** | **39%** | **0.64** |
| OWD | 345 | +143% | 49% | 0.56 |
| static | 349 | −0.8% | 41% | 0.12 |

OWDC-none is the standout **base** recipe from the matrix. Not auto-promoted to capital.

## Desired outcome

1. Capture/promote TradingStrategy from PBR 353 (or re-export clean fingerprint).  
2. Run viability / paper hygiene per existing ops (observation vs trade_ready).  
3. Do **not** attach Kelly/Martingale scale for first paper band.  

## Acceptance

- [ ] TS captured with base OWDC + scale none  
- [ ] Paper OP path decided (import / activate paper)  
- [ ] Link PBR 353 in provenance  

## Related

- Close-trigger / OWDC prior science  
- Matrix findings session report  
