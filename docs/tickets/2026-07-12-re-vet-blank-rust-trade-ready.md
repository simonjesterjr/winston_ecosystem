# Ticket: Re-vet Portfolio Blank and Rust for trade-ready gates

**Status:** Proposed  

**Date:** 2026-07-12  

**Context:** Phase 6 cohort vet_trend (2026-07-12). Green and Pink passed viability gates; Blank and Rust failed **max drawdown ≤ 50%**.

## Results (validation winners)

| Portfolio | Strategy | Return | Max DD | Trades | export_kind |
|-----------|----------|--------|--------|--------|-------------|
| Blank | Breakout5Day + VolExit | +671% | **55.0%** | 814 | observation |
| Rust | Breakout5Day + VolExit | +685% | **77.4%** | 496 | observation |

## Problem

Observation-only paper is fine short-term, but Blank/Rust cannot open real capital by default without trade-ready provenance. High returns with extreme DD suggest membership and/or strategy grid need another pass.

## Scope

1. Diagnose DD drivers (membership concentration, short breakout + vol exit, capital/risk base config)  
2. Options: re-membership under corr_v2; expand strategy grid; ranking metric experiment; risk/capital params  
3. Re-run `portfolios:vet_trend` with EXPORT; aim `export_kind: trade_ready`  
4. Re-import Wv2 only if fingerprint/export changes (successor hygiene if engaged)

## Acceptance

- [ ] Root-cause note in analysis or session report  
- [ ] New export labeled trade_ready **or** documented decision to keep observation  
- [ ] Wv2 OP updated without silent mutate of engaged series  

## Related

- Exports: `portfolio_configs/portfolio-blank.json`, `portfolio-rust.json`  
- Gates: `docs/business-context/trade-ready-viability-gates.md`  
- Open Blue revisit ticket remains separate  
