# Ticket: Phase 2 step 3b — S4 milder One-Way Dynamic ladder at frozen heat

**Status:** Proposed  
**Priority:** P2  
**Date:** 2026-07-26  
**Monolith:** winston_unit_test  
**Related:** `2026-07-25-strategy-bakeoff-v1-phase1.md`; session `2026-07-26-1103-strategy-bakeoff-phase2.md`; elephant risk panel `elephant_risk_1pct_v1`

---

## Problem

S4 FastBO5 tactics freezes after Phase 2 steps 1–3:

| Knob | Freeze |
|------|--------|
| Pyramid Average True Range (ATR) mult | 1.0 |
| Max per symbol / pyramid | 4 |
| Max portfolio lots | 12 |
| Fill | `next_bar_open` |
| Risk | One-Way Dynamic (OWD) **ladder A** / base **2%** |

Ladder A (long 2→3→4→6%, short milder) was **never swept** while heat/pyr/max_sym were. Operator goal is higher Compound Annual Growth Rate (CAGR) with lower max drawdown — unit risk / ladder shape is the remaining sparse tactic after lot heat proved path-noisy.

Elephant @1% showed unit risk **changes survivability** without changing entry DNA. Same question for **S4 at frozen capacity**.

---

## Scope

1. Freeze everything above except OWD ladder (+ base `risk_percentage` if tied to first rung).  
2. Sparse packs only (not full factorial):

| Pack | Long ladder | Short ladder | Base % |
|------|-------------|--------------|--------|
| **A** (control) | 2/3/4/6/6 | 2/2/2/3/3 | 2% |
| **B** moderate | 2/2/3/3/4 | 2/2/2/2/3 | 2% |
| **C** flat | 2% × 5 | 2% × 5 | 2% |
| **D** optional half | 1/1.5/2/3/3 | 1/1/1/1.5/1.5 | 1% |

3. Portfolios: Blue, Orange, Mango, Green (same Phase 2 panel).  
4. Cells: 3 packs × 4 ports = **12** (+4 if D).  
5. Score: return, max DD, Sharpe, **CAGR**, Calmar vs pack A control (reuse bake-off / max_port PBR 294/297/300/303 shape where applicable).  
6. Scripts: mirror `s4_phase2_max_port_*` pattern; experiment key `s4_phase2_ladder_v1`.

---

## Acceptance

- [ ] 12 (+optional) PBRs completed under next_bar_open  
- [ ] Written freeze: keep A / adopt B / adopt C / adopt D  
- [ ] Map under `ecosystem/docs/analysis/`  
- [ ] Bake-off master ticket updated  

## Out of scope

- Hybrid fill (separate ticket)  
- Correlation unit heat (heat ticket)  
- Changing max_sym / max_port / pyr ATR  

---

## Notes

If pack D (1%) wins on DD but loses too much CAGR on Blue/Mango, document the tradeoff; do not auto-promote half risk without operator goal bar.
