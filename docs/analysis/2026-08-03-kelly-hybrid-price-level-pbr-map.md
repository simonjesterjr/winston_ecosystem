# PBR map — Kelly hybrid price-level matrix (`kelly_hybrid_price_level_v1`)

**Date:** 2026-08-03 (scorecard filled 2026-08-09)  
**Experiment key:** `kelly_hybrid_price_level_v1`  
**Ticket:** `docs/tickets/2026-08-03-kelly-hybrid-matrix.md`  
**Fill (all cells):** Hybrid · pyramid price-level  
(`hybrid_entry_next_pyramid_price_level` = entry `next_bar_open` · pyramid `price_level_touch`)  
**DNA:** S4 FastBO5 (TS #48) · OWD ladder A · 2% · max_sym 4 · max_port 12 · pyr ATR 1.0 · $10k · lev 3  
**Books:** Mint (110) · Mango (65) · Yellow (111)

---

## Phase 1 cells (per book)

| Cell key | Policy | Notes |
|----------|--------|--------|
| **ctrl** | `risk_scale_policy: none` | OWD control |
| **classic** | kelly + `kelly_sizing: classic` | risk% = clamp(½ f\*), recompute every close |
| **wk22** | kelly + winston + calendar **22** | mult form `1+f`, half-Kelly |
| **wk44** | kelly + winston + calendar **44** | default Winston cadence |
| **wk66** | kelly + winston + calendar **66** | |
| **wk88** | kelly + winston + calendar **88** | |

**Expected Phase 1 total:** 18 PBRs — **completed**.

Shared Winston defaults: `fractional_kelly: 0.5`, `kelly_min_trades: 20`, `kelly_lookback_trades: 40`, mult floor 0.5× / ceiling 2.0×, rung caps 0.5%–8%.

---

## Phase 2 — Yellow flat-edge band (hypothesis)

**Hypothesis:** Phase-1 Yellow Kelly failed because closed-trade full f\* ≈ 0 / slightly negative, so Winston mostly **shrunk** below 1.0×. If we treat |full_kelly| < ε as **noise** and **floor at 1.0×**, Kelly should track control more closely and only de-risk when edge is clearly bad.

Config: `kelly_flat_edge_eps` (on **full** f\* before fractional). Default 0 = disabled.

| Cell key | Config | Compare to |
|----------|--------|------------|
| **wk44_flat_eps02** | WK44 + ε=0.02 | wk44 (398), ctrl (395) |
| **wk44_flat_eps05** | WK44 + ε=0.05 | same |
| **wk44_flat_eps10** | WK44 + ε=0.10 | same (wide band) |
| **wk22_flat_eps05** | WK22 + ε=0.05 | wk22 (397) |
| **classic_flat_eps05** | classic + ε=0.05 | classic (396) |

| Cell | PBR | Status |
|------|-----|--------|
| wk44_flat_eps02 | **401** | completed |
| wk44_flat_eps05 | **402** | completed |
| wk44_flat_eps10 | **403** | completed |
| wk22_flat_eps05 | **404** | completed |
| classic_flat_eps05 | **405** | completed |

---

## PBR ID table (Phase 1)

| Book | ctrl | classic | wk22 | wk44 | wk66 | wk88 |
|------|------|---------|------|------|------|------|
| Mint | **383** | **384** | **385** | **386** | **387** | **388** |
| Mango | **389** | **390** | **391** | **392** | **393** | **394** |
| Yellow | **395** | **396** | **397** | **398** | **399** | **400** |

---

## Scorecard (completed 2026-08-09)

| Book | Cell | Ret % | Max DD % | Sharpe | Trades | Final $ | PBR |
|------|------|-------|----------|--------|--------|---------|-----|
| Mango | ctrl | **149.9** | 47.5 | 0.58 | 251 | 24,992 | 389 |
| Mango | classic | −37.6 | 75.3 | 0.05 | 231 | 6,244 | 390 |
| Mango | wk22 | **249.6** | 43.8 | 0.72 | 220 | 34,956 | 391 |
| Mango | wk44 | 128.8 | 46.8 | 0.56 | 148 | 22,875 | 392 |
| Mango | **wk66** | **262.7** | **36.9** | **0.75** | 260 | **36,267** | **393** |
| Mango | wk88 | 83.2 | 47.5 | 0.45 | 214 | 18,315 | 394 |
| Mint | ctrl | 109.7 | **113.5** | −0.32 | 484 | 20,969 | 383 |
| Mint | classic | 376.3 | **44.5** | **0.79** | 65 | 47,627 | 384 |
| Mint | wk22 | 376.6 | 70.3 | 0.63 | 427 | 47,662 | 385 |
| Mint | wk44 | 428.3 | 67.3 | 0.65 | 523 | 52,834 | 386 |
| Mint | **wk66** | **497.1** | 79.1 | 0.63 | 476 | **59,711** | **387** |
| Mint | wk88 | 334.3 | 69.1 | 0.59 | 521 | 43,430 | 388 |
| Yellow | **ctrl** | **81.7** | 40.4 | **0.43** | 166 | **18,168** | **395** |
| Yellow | classic | −5.3 | 31.6 | 0.04 | 231 | 9,472 | 396 |
| Yellow | wk22 | −17.5 | 39.6 | 0.0 | 154 | 8,253 | 397 |
| Yellow | wk44 | −5.7 | 44.1 | 0.09 | 132 | 9,429 | 398 |
| Yellow | wk66 | −17.5 | 39.6 | 0.0 | 158 | 8,248 | 399 |
| Yellow | wk88 | 32.3 | 45.3 | 0.28 | 140 | 13,232 | 400 |
| Yellow | wk44_flat_eps02 | −5.7 | 44.1 | 0.09 | 132 | 9,429 | 401 |
| Yellow | wk44_flat_eps05 | −5.2 | 44.1 | 0.09 | 132 | 9,481 | 402 |
| Yellow | wk44_flat_eps10 | −5.2 | 44.1 | 0.09 | 132 | 9,481 | 403 |
| Yellow | wk22_flat_eps05 | 1.0 | 39.6 | 0.12 | 136 | 10,099 | 404 |
| Yellow | **classic_flat_eps05** | **37.3** | **30.9** | **0.32** | 184 | **13,729** | **405** |

---

## Reading (promotion doctrine)

1. **Host-dependent (confirms ADR-010 — Kelly not global default).**  
   - **Mango / Mint:** Winston calendar Kelly **beats control** on return; **wk66** is the standout on Mango (best Sharpe + return); Mint return wins (wk66) but drawdowns stay high.  
   - **Yellow:** OWD **control wins** Phase 1; every Kelly arm underperforms ctrl on return (except partial recovery on wk88).  

2. **Classic vs Winston:** Classic flattens ladder — **hurt Mango hard** (−38% / 75% DD); **rescued Mint** on DD/Sharpe (few trades, 0.79 Sharpe). Not a universal mode.

3. **Flat-edge ε (Phase 2 Yellow):** Winston flat-edge barely moves wk44 (still ~−5%). **classic_flat_eps05** is the only Phase-2 arm that approaches ctrl quality (37% ret / 31% DD / 0.32 Sharpe) — still **below** Yellow ctrl return (82%).

4. **Promotion call (ops):**  
   - Do **not** auto-export Kelly on all trade-ready recipes.  
   - Candidate for **observation / host-specific** promotion: **Winston Kelly calendar 66** (`wk66`) on hosts that look like Mango/Mint under this DNA — fingerprint as new methodology.  
   - Yellow-like hosts: keep **`risk_scale_policy: none`** until a different edge proxy or DNA wins.

5. **Plumbing:** Wv2 now imports + sizes + recomputes meta scale (WS2–WS4). Lab evidence gates **whether** a given fingerprint should carry Kelly — not whether the code path works.

---

## Commands

```bash
bin/compose exec -T winston_unit_test bin/rails runner lib/scripts/kelly_hybrid_matrix_setup.rb
bin/compose exec -T winston_unit_test bin/rails runner lib/scripts/kelly_hybrid_matrix_scorecard.rb
```

Artifact: `winston_unit_test/tmp/kelly_hybrid_price_level_v1_scorecard.json`
