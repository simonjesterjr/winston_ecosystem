# Ticket: Bake-off / Phase 2 scorecards — CAGR and Calmar metrics

**Status:** Proposed  
**Priority:** P3  
**Date:** 2026-07-26  
**Monolith:** winston_unit_test  
**Related:** session `2026-07-26-1103-strategy-bakeoff-phase2.md`; operator goal framing (exceptional return vs low risk); scripts under `lib/scripts/*scorecard*.rb`

---

## Problem

Lab scorecards currently emphasize **total return %**, max drawdown, practical Sharpe, and trade count. Operator evaluation of multi-year Portfolio Backtest Runs (PBRs) needs:

| Metric | Why |
|--------|-----|
| **Compound Annual Growth Rate (CAGR)** | ~200% over ~7 years is not exceptional once annualized (~19%/yr on Mint S4) |
| **Calmar** (total return / max DD, or CAGR / max DD — **pick one and document**) | Compares wealth path to pain |

Without these, panels over-weight long-window total return and under-weight “is this good Trend Following (TF) for the time span?”

---

## Scope

1. Add helpers (shared module or copy-small) used by:
   - `strategy_bakeoff_v1_scorecard.rb`
   - `elephant_risk_1pct_scorecard.rb`
   - `s4_phase2_*_scorecard.rb` (all Phase 2)
2. CAGR from `overlapping_date_range` start/end + `total_return` (fractional years = day span / 365.25).  
3. Calmar: default **total_return_pct / max_drawdown_pct** when DD &gt; 0; optional second line CAGR/DD if useful.  
4. Print medians of CAGR and Calmar by strategy key / pack in summaries.  
5. Optional `WRITE=1` JSON fields: `cagr_pct`, `calmar`, `window_years`.  
6. One short comment or README line in each script header describing formulas.

## Acceptance

- [ ] Scorecards print CAGR and Calmar per completed cell  
- [ ] Medians include CAGR (and Calmar) where n≥1 completed  
- [ ] Formula documented in script header or shared module  
- [ ] Smoke: re-run scorecard on existing bake-off data (no new PBRs required)

## Out of scope

- UI PBR show page scorecard strip (separate cash-ledger ticket)  
- Changing ranking primary key away from Sharpe without product call  

---

## Notes

Mint S4 bake-off reference: ~6.73y window → ~19.4% CAGR, ~43% max DD (PBR 246) — scorecard should reproduce this class of number.
