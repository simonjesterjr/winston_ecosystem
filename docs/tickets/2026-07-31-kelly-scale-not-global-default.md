# Ticket: Kelly scale — host-specific policy (not global default)

**Status:** Done (doctrine locked; host allowlist remains optional lab follow-on)  
**Priority:** P2  
**Date:** 2026-07-31 (closed 2026-08-09)  
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

- [x] Written rule in ADR or business-context — **ADR-010 §C**, CONTEXT **Risk Scale Policy**  
- [x] No silent Kelly default in TS/PBR forms (already `none`)  

Optional host allowlist / multi-portfolio confirmation remains a lab promotion checklist item, not a code default.

## Related

- PBRs 348, 352, 356  
- ADR-010 · ticket `2026-07-31-adr-risk-scale-orthogonality.md`  
