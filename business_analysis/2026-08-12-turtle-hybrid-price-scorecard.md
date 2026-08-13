# Turtle Systems V1 — hybrid price-level scorecard

**Date:** 2026-08-12  
**Status:** Scored — promote list frozen for paper observation  
**Experiment:** `turtle_systems_v1`  
**Fill chassis:** `hybrid_entry_next_pyramid_price_level`  
(entry **T+1 open** · pyramid **price_level_touch** at last entry ± N×ATR)  
**Program ticket:** `docs/tickets/2026-08-12-turtle-systems-eval-and-ops-alignment.md`  
**Chassis BA:** `business_analysis/2026-08-12-turtle-systems-and-heat.md`  
**PBR map:** #424–#447 (24 cells, all completed)  
**TradingStrategies:**  
- **TS #75** `TurtleV1 S1 Breakout20/10` (cell A1)  
- **TS #76** `TurtleV1 S1 Breakout20/10 SkipWinner` (cell A2)  
- **TS #77** `TurtleV1 S2 Breakout55/20` (cell B1)  

---

## Chassis (all cells)

| Knob | Value |
|------|--------|
| Risk | Static **1%** of capital base (lab); target ops sizing = **risk_equity** (see chassis BA) |
| Stop | ATR×**2**, `move_to_last_entry` |
| Pyramid | **0.5N**, max **4** / market, max **12** portfolio lots |
| Vol exit | **None** |
| Fill | Hybrid price-level (not pure next_bar_open) |

---

## Panel medians (8 books)

| Cell | Recipe | Median return | Median max DD | Viable* |
|------|--------|---------------|---------------|---------|
| **A1** | S1 20/10, no skip | **−3.7%** | 55.6% | 3/8 |
| **A2** | S1 20/10 + skip-after-winner | **+21.9%** | 50.6% | ~3/8 |
| **B1** | S2 55/20 | **+16.0%** | 58.2% | 4/8 |

\*Viable heuristic: return &gt; 0, max DD &lt; 55%, trades ≥ 40.

---

## Window fit — Blue & Mango first

| Portfolio | Best S1 | S2 (B1) | Decision |
|-----------|---------|---------|----------|
| **Blue** | A1 −45.9% / DD 52% | B1 −72.8% / DD 79% | **Reject both** under this chassis |
| **Mango** | A1/A2 wipeouts (~−100%+) | **B1 +45.7% / DD 51%** | **S2 only** |

**Hypothesis result:** Window length **does** re-rank some prior strong books (Mango → S2). Blue is **not** rescued by Faith S1 or S2 under hybrid price + 0.5N.

---

## Cell detail (hybrid price)

| PBR | Portfolio | Cell | Return % | Max DD % | Trades | Flag |
|-----|-----------|------|----------|----------|--------|------|
| 424 | Blue | A1 | −45.9 | 52.1 | 800 | |
| 425 | Blue | A2 | −77.3 | 84.3 | 749 | hard reject |
| 426 | Blue | B1 | −72.8 | 79.3 | 418 | |
| 427 | Mango | A1 | −99.4 | 101.1 | 842 | hard reject |
| 428 | Mango | A2 | −115.4 | 122.6 | 713 | hard reject |
| 429 | Mango | B1 | **+45.7** | 51.4 | 610 | **viable** |
| 430 | Mint | A1 | **+103.5** | 50.2 | 1127 | **viable** |
| 431 | Mint | A2 | +21.9 | 57.1 | 1117 | |
| 432 | Mint | B1 | **+537.0** | 53.8 | 767 | **viable — best overall** |
| 433 | Yellow | A1 | **+328.1** | **20.9** | 1270 | **viable — best DD** |
| 434 | Yellow | A2 | +132.0 | 37.4 | 1211 | viable |
| 435 | Yellow | B1 | +74.2 | 34.5 | 761 | viable |
| 436 | Orange | A1 | −11.5 | 59.2 | 808 | |
| 437 | Orange | A2 | **+62.7** | 48.7 | 865 | viable |
| 438 | Orange | B1 | −92.9 | 100.6 | 454 | hard reject |
| 439 | Red | A1 | −102.6 | 106.5 | 689 | hard reject |
| 440 | Red | A2 | −12.8 | 50.6 | 819 | |
| 441 | Red | B1 | **+96.5** | 50.4 | 495 | viable |
| 442 | Green | A1 | +4.0 | 36.9 | 637 | viable |
| 443 | Green | A2 | +34.7 | 33.1 | 656 | viable |
| 444 | Green | B1 | −13.7 | 62.7 | 391 | |
| 445 | Rust | A1 | +18.1 | 67.9 | 588 | |
| 446 | Rust | A2 | +19.6 | 63.0 | 535 | |
| 447 | Rust | B1 | −71.2 | 82.1 | 300 | hard reject |

---

## Skip-after-winner (A2 − A1 return)

| Portfolio | Δ return (pts) | Call |
|-----------|----------------|------|
| Orange | **+74** | Skip helps |
| Red | **+90** | Skip helps |
| Green | **+31** | Skip helps |
| Rust | +1 | Neutral |
| Blue | −31 | Skip hurts |
| Mango | −16 | Skip hurts |
| Mint | **−82** | Skip hurts |
| Yellow | **−196** | Skip hurts hard |

**Decision:** Skip-after-winner is **not** a global S1 default. Prefer **A1 (no skip)** for exclusive books (Mint/Yellow). Optional paper on Orange/Green only if re-tested.

---

## Promote list (paper / observation)

| Priority | TS | Books | Why |
|----------|-----|-------|-----|
| **1** | **#77 TurtleV1 S2 Breakout55/20** | **Mint** (primary); optional Mango / Red later | Mint B1 +537% / 54% DD; Mango only viable on S2 |
| **2** | **#75 TurtleV1 S1 Breakout20/10** | **Yellow** (primary); Mint secondary | Yellow A1 +328% / **21%** DD; no skip |

**Do not promote under this chassis:**

- Blue (any cell)  
- S1 on Mango  
- Global skip-after-winner (TS #76) as default  

---

## Insights for heat / portfolio construction

1. **Exclusive / Mint-class books dominate** — same pattern as S4 bake-off; membership still beats window tuning for diversifiers.  
2. **Correlated cores (Orange/Blue)** need heat L2/L3 sooner — reinforces multi-level unit heat work.  
3. **Next discovery:** another exclusive book (**Walnut**, target PCS ~ Mint ~90+) to diversify beyond Mint/Yellow.  
4. **Ops:** size units on **risk_equity**, not free cash alone (chassis BA); required before real capital on these fingerprints.

---

## Follow-ons

| Track | Action |
|-------|--------|
| Handoff | Export Mint+TS#77 and Yellow+TS#75 as observation / trade-ready when gates pass |
| Heat | Implement L1–L4 on TS + PBR (`2026-07-25-ts-portfolio-heat-unit-limits`) |
| Discovery | Portfolio Walnut — exclusive Mint-class cohort |
| Capital | Wv2 `PositionSizer` + DAR dual free_cash / risk_equity |

---

## Score command

```bash
bin/compose exec -T winston_unit_test bin/rails runner lib/scripts/turtle_systems_v1_scorecard.rb WRITE=1
```
