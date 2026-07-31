# Ticket: Kelly scale — host-specific policy (not global default)

**Status:** Proposed  
**Priority:** P2  
**Date:** 2026-07-31  
**Monolith:** cross (WUT lab doctrine → eventual Wv2)  
**Session:** `docs/session-reports/2026-07-31-1556-risk-scale-matrix-findings.md`

---

## Problem

Kelly-as-meta changed Yellow paths:

| Base | none → Kelly | Verdict |
|------|----------------|---------|
| static | −0.8% → +35% | lift |
| OWD | +143% → +152%, DD better | mild lift |
| OWDC | +176% → +10%, DD worse | **regression** |

Shipping Kelly as a global portfolio toggle is unsafe.

## Desired outcome

Document and enforce lab doctrine:

1. Kelly not default on trade-ready exports.  
2. Optional: allowlist hosts where none-cell is weak, or require multi-portfolio confirmation.  
3. Capture in ADR or business-context once ADR ticket lands.  

## Acceptance

- [ ] Written rule in ADR or business-context  
- [ ] No silent Kelly default in TS/PBR forms (already `none`)  

## Related

- PBRs 348, 352, 356  
- ADR orthogonality ticket `2026-07-31-adr-risk-scale-orthogonality.md`  
