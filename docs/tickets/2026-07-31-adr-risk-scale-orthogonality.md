# Ticket: ADR — risk_scale_policy orthogonal to base risk geometry

**Status:** Done  
**Priority:** P2  
**Date:** 2026-07-31 (closed 2026-08-09)  
**Scope:** ecosystem ADR  
**Session:** `docs/session-reports/2026-07-31-1556-risk-scale-matrix-findings.md`

---

## Problem

Risk scale (none / anti_martingale / martingale / kelly) is implemented as meta over static/OWD/OWDC, but no ADR locks the product rule. Peer S/M/K as sole `risk_evaluation_strategy` is deprecated.

## Desired outcome

ADR under `ecosystem/docs/adr/` covering:

- Base geometry enum vs `risk_scale_policy`  
- Fingerprint includes policy + config; runtime `n_steps`/Kelly mult is path state  
- Default `none`  
- Martingale research-only; Kelly not a global ops default without host evidence  

## Acceptance

- [x] ADR accepted and linked from CONTEXT or business-context risk notes  
- [x] Cross-link from `2026-07-31-risk-scale-meta-layer.md`  

**Delivered:** `docs/adr/ADR-010-risk-scale-meta-layer.md` · CONTEXT **Risk Scale Policy** · `wut-to-wv2-handoff.md` provenance fields.

## Related

- ADR-008 (confirm ⊥ ladder) as pattern  
- ADR-010 (this decision)  
- Ticket `2026-07-30-kelly-martingale-sizing-portfolio-management.md`  
