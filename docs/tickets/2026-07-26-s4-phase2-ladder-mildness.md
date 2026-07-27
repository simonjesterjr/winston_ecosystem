# Ticket: Phase 2 step 3b — S4 milder One-Way Dynamic ladder at frozen heat

**Status:** Scored — freeze **keep ladder A** (B/C path-identical null)  
**Priority:** P2  
**Date:** 2026-07-26  
**Monolith:** winston_unit_test  
**Experiment key:** `s4_phase2_ladder_v1`  
**Related:** `2026-07-25-strategy-bakeoff-v1-phase1.md`; session `2026-07-26-1103-strategy-bakeoff-phase2.md`; elephant risk panel `elephant_risk_1pct_v1`  
**Map:** `docs/analysis/2026-07-26-s4-phase2-ladder-pbr-map.md`

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

## Scripts

| File | Role |
|------|------|
| `winston_unit_test/lib/scripts/s4_phase2_ladder_setup.rb` | Create 12 pending PBRs (packs A/B/C); `INCLUDE_D=1` adds pack D |
| `winston_unit_test/lib/scripts/s4_phase2_ladder_scorecard.rb` | Progress + medians + CAGR/Calmar vs step3 max_port=12 control |

```bash
# setup (already run 2026-07-26 → PBRs 305–316)
bin/compose exec -T winston_unit_test bin/rails runner lib/scripts/s4_phase2_ladder_setup.rb

# after Execute:
bin/compose exec -T winston_unit_test bin/rails runner lib/scripts/s4_phase2_ladder_scorecard.rb
```

## Acceptance

- [x] Setup: 12 PBRs under next_bar_open (305–316)  
- [x] 12 PBRs **completed**  
- [x] Written freeze: **keep A** (B/C identical; D not needed for mildness question)  
- [x] Map under `ecosystem/docs/analysis/2026-07-26-s4-phase2-ladder-pbr-map.md`  
- [x] Bake-off master ticket freezes updated after score  

## Score summary (2026-07-26)

| Pack | Med ret% | Med DD% | Med Sharpe | Med CAGR% | Path vs A |
|------|----------|---------|------------|-----------|-----------|
| A | 109.3 | 45.5 | 0.52 | 12.6 | control |
| B | 109.3 | 45.5 | 0.52 | 12.6 | **identical** |
| C | 109.3 | 45.5 | 0.52 | 12.6 | **identical** |

Pack A matched step3 max_port=12 cells exactly. Equity + position unit series SHA-identical across A/B/C per book. Stamped ladders differed correctly — higher rungs do not engage under `max_port=12` breadth regime (all packs level-1 = 2%).

**Freeze: keep ladder A.** Milder shape is not a de-risk lever on this chassis; change base/level-1 risk if unit risk is the goal (optional pack D / 1% sleeve).

## Out of scope

- Hybrid fill (separate ticket)  
- Correlation unit heat (heat ticket)  
- Changing max_sym / max_port / pyr ATR  

---

## Notes

Pack D (1%) was not run: it confounds **unit risk** with ladder shape. Prior Elephant panel already showed ~1% unit risk changes survivability; this step only asked whether mid-ladder mildness at 2% base helps — answer **no**.
