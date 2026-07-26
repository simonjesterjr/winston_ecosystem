# Ticket: Strategy bake-off V1 — Phase 1 (cross-portfolio TS selection)

**Status:** Phase 1 scored — promote S4; S1 optional second family  
**Priority:** P1  
**Date:** 2026-07-25 (scored 2026-07-26)  
**Monolith:** winston_unit_test  
**Experiment key:** `strategy_bakeoff_v1`  
**Session reference (use this in a new Grok chat):** `2026-07-25-strategy-bakeoff-v1-phase1`

---

## Goal

Pick **2–3 winning TradingStrategies** from a controlled cross-portfolio sample of trend-following methodologies.  
**Do not** tune pyramid ATR, OWD ladders, max/symbol, or heat in this phase.

Phase 2 (tactics) only after promotion.

---

## Frozen chassis (all 55 cells)

| Knob | Value |
|------|--------|
| Fill | `next_bar_open` (T+1 queue) |
| Risk | `one_way_dynamic` |
| Stop | `move_to_last_entry` |
| ATR mult | 2.0 |
| Pyramid ATR | 1.0 |
| Max pyramid / max per symbol | 5 |
| Max positions per portfolio | 12 |
| Ladder long | `[0.02, 0.03, 0.04, 0.06, 0.06]` |
| Ladder short | `[0.02, 0.02, 0.02, 0.03, 0.03]` |
| Capital | $10,000 |
| Ignore first signal | true |

---

## Strategies (TS names)

| Key | Name | Primary | Confirm | Exits |
|-----|------|---------|---------|-------|
| S1 | BakeoffV1 S1 Elephant | Swing5 HL | EMA20 | 20BO + Vol |
| S2 | BakeoffV1 S2 Donchian20+EMA55 | Breakout20 | **EMA55** | 20BO + Vol |
| S3 | BakeoffV1 S3 SlowBO50NH | BO50 NoHistory | — | Vol |
| S4 | BakeoffV1 S4 FastBO5 | Breakout5 | — | Vol |
| S5 | BakeoffV1 S5 StructureExit | Swing5 HL | EMA20 | **EMA20 + Vol** |

---

## Portfolios (11 × 5 = 55 PBRs)

| Tier | Portfolios |
|------|------------|
| **Core** (rank on these) | Blue, Orange, Red, Green, Mango, Rust |
| **Stress** (consistency) | White, Pink, Gray |
| **Exclusive** (consistency) | Mint, Yellow |

---

## Ranking rules

1. **Median practical Sharpe** on Core completed cells  
2. **Median total return** (tie-break)  
3. **Viable count:** Core cells with return > 0, max DD < 55%, trades ≥ 80  
4. **Hard reject signal:** DD > 80% and return < 0, or too few trades  

Promote **top 2**; add **3rd** only if a different family (e.g. slow vs swing).

Stress/exclusive: report pass/fail; do not dominate median unless Core is tied.

---

## Operator workflow

1. **Setup** (already runnable; idempotent):

```bash
bin/compose exec -T winston_unit_test bin/rails runner lib/scripts/strategy_bakeoff_v1_setup.rb
```

2. **Manual Run** each pending PBR in UI:  
   `/wut/portfolio_backtest_runs/:id` → Execute  
   (results_json already seeds `fill_cadence=next_bar_open` + ladder + experiment tags)

3. **Score anytime** (partial OK):

```bash
bin/compose exec -T winston_unit_test bin/rails runner lib/scripts/strategy_bakeoff_v1_scorecard.rb
# optional markdown/json dump:
bin/compose exec -T winston_unit_test bin/rails runner lib/scripts/strategy_bakeoff_v1_scorecard.rb WRITE=1
```

4. **Hand off to Grok** (new chat paste):

```
Read ecosystem/docs/tickets/2026-07-25-strategy-bakeoff-v1-phase1.md and score strategy_bakeoff_v1.

1. Run scorecard WRITE=1
2. Promote 2–3 TS by Core median Sharpe + viable count
3. No tactic tuning yet
4. Summarize S1–S5 + Phase-2 sparse plan
```

---

## Scripts

| File | Role |
|------|------|
| `winston_unit_test/lib/scripts/strategy_bakeoff_v1_setup.rb` | Create 5 TS + 55 pending PBRs |
| `winston_unit_test/lib/scripts/strategy_bakeoff_v1_scorecard.rb` | Progress + rank + handoff prompt |
| `winston_unit_test/tmp/strategy_bakeoff_v1_matrix.json` | Cell map after setup |
| `winston_unit_test/tmp/strategy_bakeoff_v1_scorecard.{json,md}` | After `WRITE=1` |

---

## Out of scope (Phase 1)

- Pyramid ATR / ladder / max-symbol / heat sweeps  
- Close-primary variants  
- Full Maverick triple exits  
- OWDC / strength risk  
- Restoring same_bar_open for “better” numbers  

---

## Runtime IDs (created 2026-07-25)

| Key | TS id |
|-----|-------|
| S1 | 45 |
| S2 | 46 |
| S3 | 47 |
| S4 | 48 |
| S5 | 49 |

PBR range: **198–252** (55 cells). Map: `ecosystem/docs/analysis/2026-07-25-strategy-bakeoff-v1-pbr-map.md`

## Acceptance

- [x] 55 PBRs exist with `experiment=strategy_bakeoff_v1`  
- [x] All Core cells completed under `next_bar_open` (all 55 completed)  
- [x] Scorecard run; promote **S4 (TS#48)** primary; **S1 (TS#45)** optional second family only  
- [ ] Phase 2 tactic plan executed (sparse knobs on S4 first)

---

## Phase 1 score (2026-07-26)

All **55/55 completed**. Chassis frozen (`next_bar_open` + OWD ladder A).

### Core summary (rank metrics)

| Key | Med Sharpe | Med return% | Med DD% | Viable | Hard reject | Verdict |
|-----|------------|-------------|---------|--------|-------------|---------|
| **S4 FastBO5** | **0.52** | **+79.5** | **45.5** | **3/6** | 3 | **PROMOTE #1** |
| S3 SlowBO50NH | 0.40 | −101.1 | 101.1 | 1/6 | 4 | **Do not promote** (Sharpe trap) |
| S1 Elephant | 0.22 | −29.0 | 68.1 | 0/6 | 2 | Optional 2nd family only |
| S2 Donchian20+EMA55 | 0.12 | −60.8 | 93.7 | 0/6 | 5 | Reject |
| S5 StructureExit | 0.02 | −108.3 | 109.3 | 0/6 | 4 | Reject |

Naive scorecard rank put S3 #2 on median Sharpe alone — **override**: median wealth path is catastrophic; only Green is decent on Core.

### Core matrix (return% / DD% / Sharpe)

| Port | S1 | S2 | S3 | **S4** | S5 |
|------|----|----|----|--------|-----|
| Blue | −40/64 | −8/46 | −127/126 | **+187/53** | −43/62 |
| Orange | −98/101 | −96/108 | −144/143 | **+37/32** | −108/108 |
| Red | +24/67 | −73/95 | −103/102 | **+122/23**† | −131/127 |
| Green | −18/49 | −34/83 | +38/47 | −2/88 | −32/78 |
| Mango | +162/70 | −103/125 | +31/75 | **+186/38** | −111/113 |
| Rust | −103/106 | −48/92 | −100/100 | −30/89 | −108/111 |

† Red S4: only 60 trades (below MIN_TRADES=80) so scorecard marks REJECT despite excellent DD/return.

### Consistency (stress + exclusive) — S4

| Port | Ret% | DD% | Note |
|------|------|-----|------|
| Mint | **+229** | 43 | Strong |
| Yellow | **+166** | 57 | Strong |
| White / Pink / Gray | −65 to −93 | 75–97 | **Fails large/fragile books** |

S1 shows some exclusive/stress positives (Pink, Mint, Yellow) but Core median still negative under this chassis.

### Promotion decision

1. **Primary: S4 — BakeoffV1 S4 FastBO5 (TS #48)** — only methodology that is positive on Core median wealth + best Sharpe/viable.  
2. **Optional second family: S1 Elephant (TS #45)** — different entry family; do **not** treat as co-equal winner; use only if Phase 2 needs a swing-style contrast.  
3. **Do not promote S2, S3, S5** under this chassis.  
4. **Do not restore same_bar** to “save” Elephant — Phase 1 question was next_open truth.

### Phase 1.5 (scored 2026-07-26) — Elephant risk sensitivity

**Experiment:** `elephant_risk_1pct_v1` · PBRs **253–268** · **16/16 completed**  
**Scripts:** `elephant_risk_1pct_setup.rb` / `elephant_risk_1pct_scorecard.rb`

| Pack | Ladder | Base % |
|------|--------|--------|
| `half_ladder` | long 1/1.5/2/3/3 · short 1/1/1/1.5/1.5 | 1% |
| `flat_1pct` | all levels 1% | 1% |

**Finding:** half_ladder and flat_1pct produced **identical** results on every cell (same ret/DD/trades). Stamps differ; path identity implies higher pyramid levels did not change outcomes materially at this unit size, or sizing path is dominated by level-1 1% risk. Treat as **one** “~1% unit risk” treatment, not two distinct ladders.

#### S1 @ ~1% vs bakeoff @ ladder A / 2%

| Port | Bakeoff ret/DD | @1% ret/DD | Δ ret | Δ DD |
|------|----------------|------------|-------|------|
| Blue | −40 / 64 | −8.5 / 34 | **+31** | **−30** |
| Orange | −98 / 101 | **+37 / 30** | **+135** | **−70** |
| Mango | +162 / 70 | +48 / 42 | −114 | **−28** |
| Green | −18 / 49 | −50 / 65 | −32 | +16 |
| Rust | −103 / 106 | −47 / 67 | **+55** | **−39** |

S1@1% panel: med_ret **−8.5%**, med_dd **41.6%**, **2/5 positive** (Orange, Mango). Survivability **recovered on blowups** (Orange, Rust); hero Mango **delevered**.

#### Equal-risk head-to-head (Blue / Orange / Mango)

| Port | S1@1% | S4@1% | Winner |
|------|-------|-------|--------|
| Blue | −8.5 / 34 | **+61 / 23** | S4 |
| Orange | +37 / 30 | **+53 / 49** | S4 (ret); S1 better DD |
| Mango | +48 / 42 | **+76 / 25** | S4 |
| Mean Δ ret (S1−S4) | | | **−38 pts** |

**Promotion update:** S1 is a credible **second-place / alternate family** at **1% unit risk** (not at bakeoff 2%/ladder A). S4 remains primary. Phase 2: tactics on S4 first; carry S1 as B-book candidate with default risk pack ≈ flat 1% (or half-ladder — equivalent here).

### Phase 2 step 1 (pending runs) — S4 pyramid ATR only

**Experiment:** `s4_phase2_pyr_atr_v1`  
**Scripts:** `s4_phase2_pyr_atr_setup.rb` / `s4_phase2_pyr_atr_scorecard.rb`  
**Map:** `ecosystem/docs/analysis/2026-07-26-s4-phase2-pyr-atr-pbr-map.md`

| Freeze | Value |
|--------|--------|
| TS | S4 FastBO5 (#48) |
| Fill | `next_bar_open` |
| Risk | OWD **ladder A** / base **2%** (Phase 1 chassis — not the 1% side panel) |
| Caps | max pyramid 5 · max/symbol 5 · max port 12 |

| Vary | Levels |
|------|--------|
| `pyramid_atr_multiplier` | **0.5 · 0.75 · 1.0** |

| Portfolios | Role |
|------------|------|
| Blue, Orange, Mango | S4 winners |
| Green | S4 weak |

**Cells: 3 × 4 = 12** — completed; **freeze pyr_atr = 1.0**.

### Phase 2 step 2 (scored) — S4 max per symbol

**Experiment:** `s4_phase2_max_symbol_v1` · PBRs **281–292** · **12/12 completed**  
**Map:** `ecosystem/docs/analysis/2026-07-26-s4-phase2-max-symbol-pbr-map.md`

| Freeze after step 2 | **max_positions_per_symbol = 4** (max_pyramid 4); pyr ATR **1.0** |
| Reject | max_sym **3** (Blue DD ~80%; Mango return tax) |
| Note | max **4** beats max **5** on Blue; Mango 4≈5; Orange/Green non-binding |

### Phase 2 step 3 (scored) — S4 max portfolio lots (heat)

**Experiment:** `s4_phase2_max_port_v1` · PBRs **293–304** · **12/12 completed**  
**Map:** `ecosystem/docs/analysis/2026-07-26-s4-phase2-max-port-pbr-map.md`

| Result | max **8** bad (med ret −21%); max **16** portfolio-specific (Orange↑ Blue/Mango↓); max **12** best panel medians |
| Freeze | **max_positions_per_portfolio = 12** (default); do not promote 16 from Orange alone |
| Insight | Lot heat under next-bar-open is **path selection**, non-monotonic — “inconclusive” for a universal law, conclusive enough to reject 8 and keep 12 |

S4 tactics pack: pyr ATR **1.0** · max_sym **4** · max_port **12** · ladder A / 2% · next_bar_open.

Later: optional ladder mildness (3b); hybrid fill ticket; correlation heat BA; optional S1@1% thin retest.

### Phase 2 / lab add-on — hybrid fill (design; blocked on code)

**Ticket:** `2026-07-26-hybrid-fill-entry-next-pyramid-same-day.md`  

Doctrine under test: **initial entry = next_bar_open**, **pyramid = same-day close fill** (not global same_bar).  

Why: (1) Elephant survivability books (Orange/Rust/Blue); (2) S4 winners (Blue/Mango/Mint) for Compound Annual Growth Rate (CAGR) / Sharpe sensitivity; (3) prioritizes live broker same-day scale-in automation if material.

**Blocked:** WUT today uses one fill flag for entry and pyramid — hybrid must ship before PBRs.

---

## Related

- Heat BA: `2026-07-25-ts-portfolio-heat-unit-limits.md` (after promotion)  
- T+1 fill ADR: `ecosystem/docs/adr/2026-07-25-lab-t1-fill-queue.md`  
- Mint 121 vs Maverick discussion: same-day analysis (exit stack + chassis, not bakeoff cells)  
- Score dump: `winston_unit_test/tmp/strategy_bakeoff_v1_scorecard.{json,md}` (after WRITE=1)
