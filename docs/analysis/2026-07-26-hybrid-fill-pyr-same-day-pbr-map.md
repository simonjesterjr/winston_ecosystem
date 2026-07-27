# Hybrid fill matrix v1 — S4 frozen pack (side-by-side)

**Experiment:** `hybrid_fill_pyr_same_day_v1`  
**Ticket:** `2026-07-26-hybrid-fill-entry-next-pyramid-same-day`  
**Trading Strategy (TS):** #48 BakeoffV1 S4 FastBO5  
**Status:** **6/6 hybrid + 2/2 Mint·Yellow next_bar completed** (scored 2026-07-26)

## Call (freeze)

| Decision | Value |
|----------|--------|
| Adopt hybrid as lab default? | **No** |
| Prioritize broker same-day scale-in automation from this panel? | **No** |
| Keep pure `next_bar_open` for entry **and** pyramid | **Yes** |
| Wave 2 (S1 / heat under hybrid)? | **Not indicated** |

**Hybrid is path-destructive on the frozen S4 pack**, not a null and not a winner-panel upgrade. Median Δ vs next_bar: **return −73 pts**, **max DD +17 pts**, **CAGR −8 pts**, **pyramid fills −2**, trades −62.

Only **Mint** improved return/CAGR under hybrid — with **worse** max DD (+18 pts). Blue hero path collapsed (−268 pts return).

---

## Question

At the **frozen S4 pack**, does `hybrid_entry_next_pyramid_same_day` (entry T+1 open · pyramid same-day close) change path quality vs pure `next_bar_open`?

## Chassis (both arms)

| Knob | Value |
|------|--------|
| TS | #48 FastBO5 |
| Risk | OWD ladder A / base 2% |
| Pyramid ATR | **1.0** |
| Max / symbol · max pyramid | **4** |
| Max portfolio lots | **12** |
| Capital | **$10,000** |

| Arm | `fill_cadence` | Entry | Pyramid |
|-----|----------------|-------|---------|
| **next_bar** | `next_bar_open` | T+1 open queue | T+1 open queue |
| **hybrid** | `hybrid_entry_next_pyramid_same_day` | T+1 open queue | **same-day close (B1)** |

## Grid

| Portfolio | Role | Hybrid | Next_bar |
|-----------|------|--------|----------|
| Blue | winner | **325** | **305** |
| Orange | path-sensitive | **326** | **308** |
| Mango | winner | **327** | **311** |
| Green | weak | **328** | **314** |
| Mint | exclusive | **329** | **323** (clean max_sym 4) |
| Yellow | exclusive | **330** | **324** (clean max_sym 4) |

## Results (side-by-side)

| Portfolio | Hybrid ret / DD / CAGR / Sharpe / trades / pyr | Next_bar ret / DD / CAGR / trades / pyr | Δret | Δdd | Δcagr | Δpyr |
|-----------|-----------------------------------------------|------------------------------------------|------|-----|-------|------|
| Blue | **−64 / 70 / −16 / −0.28 / 117 / 0** | **+204 / 53 / 21 / 203 / 3** | **−268** | **+16** | **−37** | −3 |
| Orange | +17 / 52 / 3 / 0.31 / 133 / 2 | +37 / 32 / 6 / 111 / 3 | −20 | **+20** | −3 | −1 |
| Mango | +55 / 59 / 8 / 0.38 / 201 / 1 | +182 / 38 / 19 / 161 / 4 | **−127** | **+21** | −11 | −3 |
| Green | −87 / 94 / −37 / 0.14 / 131 / 0 | −2 / 88 / −0 / 175 / 4 | −85 | +6 | −36 | −4 |
| Mint | **+298 / 71 / 23 / 0.61 / 426 / 4** | +163 / 54 / 15 / 604 / 3 | **+136** | +18 | **+7** | +1 |
| Yellow | +106 / 63 / 11 / 0.46 / 238 / 2 | +166 / 57 / 15 / 319 / 2 | −61 | +6 | −4 | 0 |

### Paired medians (n=6)

| Metric | Hybrid − next_bar |
|--------|-------------------|
| Med Δ return% | **−72.9** |
| Med Δ max DD% | **+16.9** |
| Med Δ CAGR% | **−7.7** |
| Med Δ pyramid fills | **−2** |
| Med Δ trades | **−62** |
| Equity-identical pairs | **0/6** |

### S4 “winners” subset (Blue / Mango / Mint)

| Metric | Med Δ |
|--------|-------|
| Δ return | **−127** |
| Δ max DD | **+18** |
| Δ CAGR | **−11** |

Mint alone is hybrid-positive on wealth; Blue and Mango are large losses. **Do not promote hybrid from Mint alone.**

## Interpretation

1. **Not scale-invariant null** — every pair has a distinct equity path (0/6 identical).  
2. **Pyramid engagement stayed tiny** (0–4 hybrid fills); hybrid still rewrote **entry path selection** via same-day cash/slot competition with the T+1 queue (fewer trades on most books; Blue −86 trades).  
3. Same-day pyramid close **does not** fix Orange survivability (DD **worse** +20 pts).  
4. Clean Mint next_bar @ max_sym **4** (323, +163% / 54% DD) is the transfer-honest baseline — not bake-off 246 (max_sym 5, +229%).

**Product:** Keep **pure `next_bar_open`** for both entry and pyramid on the S4 working pack. Hybrid remains a supported lab switch for future experiments, not the pack default. Broker work should not prioritize same-day scale-in automation **on the strength of this panel**.

## Working S4 pack (unchanged fill)

next_bar_open · OWD ladder A / 2% · pyr ATR **1.0** · max_sym **4** · max_port **12** · capital **$10k** · TS #48

## Score command

```bash
bin/compose exec -T winston_unit_test bin/rails runner lib/scripts/hybrid_fill_pyr_same_day_scorecard.rb
```
