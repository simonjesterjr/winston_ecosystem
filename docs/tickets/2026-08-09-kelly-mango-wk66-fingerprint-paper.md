# Ticket: Capture Mango Winston Kelly calendar-66 fingerprint → paper OP

**Status:** Proposed  
**Priority:** P2  
**Date:** 2026-08-09  
**Monolith:** cross (WUT → Wv2)  
**Session:** `docs/session-reports/2026-08-09-2029-kelly-risk-scale-wv2-ops.md`

---

## Problem

Mango **wk66** (PBR **393**) was the hybrid standout (+262.7% / 36.9% DD / 0.75 Sharpe vs ctrl). Ops plumbing can size/recompute Kelly, but no fingerprinted TS was promoted to observation paper.

## Desired outcome

1. Capture fingerprint from PBR 393 (or re-run if needed) with `risk_scale_policy: kelly` + calendar 66 config  
2. Export portfolio JSON (PortfolioConfigExporter)  
3. Import to Wv2 inactive → Active paper  
4. Confirm Daily Analysis updates `risk_scale_state` and ProposedSize shows scale mult  

## Acceptance

- [ ] Fingerprinted TS in WUT with scale in full_config  
- [ ] OP in Wv2 with TS.parameters risk_scale_*  
- [ ] After N DA days or closes, mult ≠ only 1.0 when history sufficient  
- [ ] Not Capital Activation / real mode  

## Related

- PBR 393 · ADR-010 · ADR-006  
- `docs/analysis/2026-08-03-kelly-hybrid-price-level-pbr-map.md`  
