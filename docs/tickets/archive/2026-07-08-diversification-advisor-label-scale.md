# Ticket: Diversification advisor labels (clarified)

**Status:** Done (clarified; transparency shipped in Phase 2–3)  
**Date:** 2026-07-08  
**Clarified:** 2026-07-11  
**Closed:** 2026-07-12  

**Context:** Session and plan [`portfolio-correlation-methodology-and-score`](../../plans/portfolio-correlation-methodology-and-score.md).

## Original problem statement

Portfolio White mean |r| ≈ 0.105 was labeled **Weak Diversification**; Orange mean |r| ≈ 0.171 was **Strong Diversification**. Suspected inverted labels.

## Clarification (2026-07-11 audit)

Labels are **not** inverted. Rating rules:

- **weak** if any pair |r| > 0.70 **or** mean |r| > 0.50  
- **strong** if mean |r| < 0.25 and no high pairs  

White is weak because **DBE/OILK ≈ 0.93**, not because mean is low. Low mean was **diluted** by near-zero junk pairs (e.g. COPR).

## Revised scope

1. ~~Fix inverted scale~~ — N/A  
2. Surface **why** weak in sidecar/UI (high pairs list, max |r|, quality flags) — still valid  
3. Prefer **max |r|** and high-pair count as primary operator metrics; mean secondary  
4. Implement under **Portfolio Correlation Score (PCS)** work in the methodology plan  

## Acceptance (revised)

- Operator can see high pairs when rating is weak  
- Mean |r| alone never sold as “strong” without max |r| context  
- Ticket closed when Phase 2–3 of correlation plan lands transparency  

## Related

- `winston_unit_test/app/services/portfolio_diversification_advisor.rb`
- White/Orange sidecars under `portfolio_configs/`
