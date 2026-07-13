# Ticket: Decide first paper Operational Portfolio (Green 55 vs Blue 62 family)

**Status:** Proposed  
**Date:** 2026-07-13  

## Context

From [`business_analysis/2026-07-13-pbr-return-dd-pcs-evaluation.md`](../../business_analysis/2026-07-13-pbr-return-dd-pcs-evaluation.md):

| Candidate | Case |
|-----------|------|
| **A — Green PBR 55** | trade_ready static, best PCS (83), capacity-clean, lower lab return |
| **B — Blue PBR 62** | C0 honest caps, still trade_ready (+1415% / DD 41.6%), risk-regime dependent; cash≫equity / leverage flag |
| Lab upper bound | Blue 48 uncapped — **not** preferred ops default without explicit policy |

## Decision needed

1. First **paper** OP seed: Green discipline vs Blue exploration (or both with dual-active force)?
2. Ops `max_markets`: force **4** vs allow nil?
3. Paper `max_leverage`: allow 3 vs force 1×?

## Acceptance

- [ ] Written operator decision recorded in business analysis (short addendum) or this ticket
- [ ] Wv2 paper import / Active set updated only after decision
- [ ] Real capital activation explicitly out of scope until paper hygiene proves out

## Related

- Level 2 experiments ticket: `2026-07-13-pbr-level2-remaining-experiments.md`
- Capital activation domain: ADR-006 / business-context OP lifecycle
