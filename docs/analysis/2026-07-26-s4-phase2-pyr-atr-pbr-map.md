# S4 Phase 2 step 1 — pyramid ATR PBR map

**Experiment:** `s4_phase2_pyr_atr_v1`  
**Ticket:** `2026-07-25-strategy-bakeoff-v1-phase1`  
**TS:** #48 BakeoffV1 S4 FastBO5  
**Freeze:** `next_bar_open` · OWD ladder A (2/3/4/6) · base 2% · max 5/12 · ATR×2  
**Vary:** `pyramid_atr_multiplier` ∈ {0.5, 0.75, 1.0}  
**Status:** **12/12 completed** (scored 2026-07-26)

## Grid — PBRs 269–280

| Portfolio | pyr 0.5 | pyr 0.75 | pyr 1.0 | Bakeoff baseline |
|-----------|---------|----------|---------|------------------|
| Blue | 269 | 270 | 271 | 201 |
| Orange | 272 | 273 | 274 | 206 |
| Mango | 275 | 276 | 277 | 221 |
| Green | 278 | 279 | 280 | 216 |

## Results (ret% / DD% / Sharpe / trades)

| Portfolio | pyr **0.5** | pyr **0.75** | pyr **1.0** | Bakeoff @1.0 |
|-----------|-------------|--------------|-------------|--------------|
| Blue | 66.5 / **80.3** / 0.44 / 72 | 28.7 / 60.5 / 0.29 / 252 | **186.6 / 53.4 / 0.69 / 222** | 186.6 / 53.4 |
| Orange | −22.1 / 83.9 / 0.26 / 179 | **36.8 / 32.2 / 0.35 / 111** | **36.8 / 32.2 / 0.35 / 111** | 36.8 / 32.2 |
| Mango | 113.1 / 49.1 / 0.57 / 127 | **277.2 / 34.9 / 0.91 / 260** | 186.3 / 37.6 / 0.69 / 188 | 186.3 / 37.6 |
| Green | −25.9 / 84.2 / 0.24 / 170 | −59.1 / 83.5 / −0.03 / 109 | **−1.9 / 87.6 / 0.35 / 175** | −1.9 / 87.6 |

### Medians across 4 portfolios

| pyr_atr | Med ret% | Med DD% | Med Sharpe | Positive |
|---------|----------|---------|------------|----------|
| 0.5 | 22.2 | **82.1** | 0.35 | 2/4 |
| 0.75 | 32.8 | 47.7 | 0.32 | 3/4 |
| **1.0** | **111.6** | **45.5** | **0.52** | **3/4** |

### Notes

- **pyr 1.0 ≡ bakeoff** on all four books (reproducibility OK).
- **Orange:** 0.75 and 1.0 identical path (spacing past ~0.75 doesn’t change that book).
- **Mango** is the only book that clearly prefers **0.75** (best ret + DD + Sharpe).
- **Blue** is destroyed by denser adds: 0.5 → DD 80%; 0.75 → weak return; **1.0 wins hard**.
- **Green** stays broken at all three; 1.0 is least bad.

## Decision (freeze for step 2)

**Freeze `pyramid_atr_multiplier = 1.0`** for S4 Phase 2 onward.

| Why not 0.75? | Mango-local win; Blue/Green worse or flat; lower median return/Sharpe. |
| Why not 0.5? | Median DD ~82%; Orange/Green losses; Blue DD spike. |

Do **not** curve-fit to Mango’s 0.75 cell.

## Score command

```bash
bin/compose exec -T winston_unit_test bin/rails runner lib/scripts/s4_phase2_pyr_atr_scorecard.rb
```

## Next

**Phase 2 step 2:** max per symbol `3 · 4 · 5` at **pyr_atr = 1.0**, same four portfolios (or Blue/Orange/Mango/Green).
