# Ticket: S4 — does 2× initial capital ($20k) improve survivability?

**Status:** Scored — **keep $10k**; $20k does **not** improve survivability  
**Priority:** P2  
**Date:** 2026-07-26  
**Monolith:** winston_unit_test  
**Experiment key:** `s4_capital_20k_v1`  
**Map:** `docs/analysis/2026-07-26-s4-capital-20k-pbr-map.md`  
**Related:** Phase 2 freezes; bake-off V1; operator question (not a 1% risk sleeve)

---

## Problem

Lab Portfolio Backtest Runs (PBRs) used **$10,000** initial capital. Operator asks whether **$20,000** improves survivability on the frozen S4 FastBO5 pack (return%, maximum drawdown, trade viability), not by cutting unit risk to 1%.

Risk is **percent of capital**, so continuous sizing is scale-invariant. Discrete **share floors** (`floor(risk$ / ATR stop distance)`), cash reserves on the next-bar queue, and high-priced names can make $10k under-size or skip fills that $20k would take.

## Scope

1. Frozen S4 pack: next_bar_open · OWD ladder A / 2% · pyr ATR 1.0 · max_sym 4 · max_port 12 · TS #48  
2. Candidate capital **$20k** on Blue, Orange, Mango, Green, Mint, Yellow  
3. Score vs $10k baselines (ladder A 305/308/311/314; bake-off S4 Mint 246 / Yellow 251)  
4. Report Δ return, Δ max DD, Δ CAGR, Δ trades — freeze whether capital level is material for ops paper sizing

## Acceptance

- [x] Setup scripts + map  
- [x] 6 PBRs completed (317–322)  
- [x] Written call: **not** scale-invariant; **$20k hurts panel medians** — keep **$10k**  
- [x] Recommended paper/lab default capital: **$10,000** for this pack  

## Score summary (2026-07-26)

| Portfolio | $20k ret / DD | $10k ret / DD | Δret | Δdd |
|-----------|---------------|---------------|------|-----|
| Blue | −5.5 / 66 | +204 / 53 | **−209** | +12 |
| Orange | −4.8 / 46 | +37 / 32 | −42 | +14 |
| Mango | **+224 / 40** | +182 / 38 | **+43** | +2 |
| Green | −33 / 78 | −2 / 88 | −31 | −10 |
| Mint† | −101 / 100 | +229 / 43 | **−330** | +57 |
| Yellow† | +12 / 58 | +166 / 57 | −155 | +1 |

† Mint/Yellow $10k = bake-off max_sym **5** vs $20k max_sym **4** (confounded). Phase 2 four (Blue–Green) are pure capital isolation.

**Panel $20k:** med ret **−5%**, med DD **62%**, 2/6 positive.  
**Paired med Δ:** ret **−98 pts**, DD **+7 pts**, CAGR **−8 pts**.

**Mechanism:** Trade counts and equity SHAs differ — extra cash changes next-bar fill sets (path selection), not a 2× clone of the $10k path.

## Scripts

```bash
bin/compose exec -T winston_unit_test bin/rails runner lib/scripts/s4_capital_20k_setup.rb
bin/compose exec -T winston_unit_test bin/rails runner lib/scripts/s4_capital_20k_scorecard.rb
```

## Out of scope

- 1% unit-risk sleeve  
- Hybrid fill  
- Changing heat / pyramid ATR  
