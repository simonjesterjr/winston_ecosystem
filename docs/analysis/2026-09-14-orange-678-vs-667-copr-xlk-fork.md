# Orange #678 vs parent #667 — COPR flip & XLK Aug-2021 fork

**Date:** 2026-09-14 (PT)  
**Chassis:** sticky **20D_BO** Working Stop · TS#77 TurtleV1 S2 · $30k · turtle heat · risk 1% · `resting_stop_touch` · `leap_fulfillment=all` · atr_offset 0 · exp 730d · experiment `strategy77_rst_parity_v1`  
**Cells:** `#667` `orange_rst_turtle_r01_leap30k` (Edge cite) · `#678` `orange_rst_turtle_r01_leap30k_oa` (OA twin, drifted)  
**Prior:** `ecosystem/docs/analysis/2026-09-14-orange-blue-oa-book-impact.md`  
**Banner:** report only — no new PBR stamps / no pack promotion  
**UI:** https://sawtooth-ai.tail944ffb.ts.net/wut/portfolio_backtest_runs/{667,678}

> Sticky **20D_BO** locked. Cite Orange Edge from **#667 (~117.35)**, **not** #678’s 150.97 — the 151 figure is close-set / fill-path drift, not an OA upgrade.

---

## 0. Headlines

| Metric | #667 parent | #678 OA twin | Δ |
|--------|-------------|--------------|---|
| edge_r† | **117.35** | **150.97** | **+33.61** |
| edge_n / closes | 283 / 283 | 281 / 281 | −2 lots |
| profit_factor† | 4.22 | 4.53 | +0.31 |
| engagements | 160 | 154 | — |
| soft close fp shared / only | — | **211 / 72 / 70** | large drift |
| eng shared / only667 / only678 | — | **124 / 36 / 30** | matches prior |
| first equity diverge | — | **2021-08-12** | Δ ~+$6.2k classic |
| first cash diverge | — | **2021-08-12** | #678 cash −$1.25k (XLK prem outlay) |
| first close-set diverge | — | **2021-08-19** | WMT stop only on #667 |

† Within-LEAP only — not share-R-comparable.

**Knobs match** (fingerprint, RST, turtle heat, 1%, leap_fulfillment=all, sticky 20D_BO). Window end #678 = 2026-09-14 vs #667 = 2026-09-11; **zero** closes with `bar_date ≥ 2026-09-11` — the extra day adds no closed lots.

---

## 1. Close / cash / engagement diff

### Soft fingerprints & engagements

| Grain | Shared | Only #667 | Only #678 |
|-------|--------|-----------|-----------|
| Soft close fp (`mkt\|dir\|date\|u\|entry\|exit`) | 211 | 72 | 70 |
| Engagements (`by_engagement` keys) | **124** | **36** | **30** |
| Unique-eng Σ edge_r (mean-space) | — | +938R | +1088R | unique Δ ≈ **+150R** (order-of-magnitude of edge gap) |

### Weighted lot-R (truth for attribution)

Engagement `edge_r` is mean lot-R within the eng; `sum_R = edge_r × n`:

| | #667 | #678 | Δ |
|--|------|------|---|
| Σ lot-R | 33,211 | 42,422 | **+9,211** |
| mean (= edge_r) | 117.35 | 150.97 | **+33.61** |

- **Shared eng** drive **98.8%** of ΣR gap (+9,104).  
- **Unique eng** only **1.2%** (+108) — the headline “unique Δ +150R” is mean-space; cash-path damage is mostly **shared engagements that blow up differently**.

### Markets in the Aug–Sep 2021 seed window (asymmetric closes)

| Market | #667 | #678 |
|--------|------|------|
| **XLK** | (still open; exit 2021-10-04) | **4 lots stop 2021-09-20** (incl. Aug 12/13 pyramids) |
| **WMT** | stop 2021-08-19 (−$77) | no Aug-19 close |
| **FPA** | 3 short closes 2021-08-24 | 2 short closes (missing mid pyramid) |
| **MSOS** | — | 3 short closes 2021-09-22 |

---

## 2. Deep-dive — `COPR:long:2025-12-05` (−1784R → +863R)

| | #667 | #678 |
|--|------|------|
| eng n / edge_r | **2 / −1784.13** | **3 / +863.35** |
| ΣR (edge×n) | **−3,568** | **+2,590** |
| **d ΣR** | — | **+6,158 (66.9% of total ΣR gap)** |
| Net cash PnL | **−$814** | **+$3,126** |

### Lots

| Run | Entry | Units | Prem | Strike | `original_stop` | Exit | Exit prem | Trail at exit | PnL | Lot R≈ |
|-----|-------|------:|-----:|-------:|----------------:|------|----------:|--------------:|----:|-------:|
| 667 | 2025-12-05 | 5 | 3.4233 | 3.6 | 2.9918 | **2026-01-28** | **4.4629** | 7.060 | +520 | **+241R** |
| 667 | 2026-01-14 | 5 | 7.1301 | 8.0 | 7.0601 | **2026-01-28** | **4.4629** | 7.060 | **−1,334** | **−3,809R** |
| 667 | *(no 3rd unit)* | — | — | — | — | — | — | — | — | — |
| 678 | 2025-12-05 | 5 | 3.4233 | 3.6 | 2.9918 | **2026-01-26** | **8.1143** | **8.476** | +2,346 | **+1,087R** |
| 678 | 2026-01-14 | 5 | 7.1301 | 8.0 | 7.0601 | **2026-01-26** | **8.1143** | **8.476** | +492 | **+1,406R** |
| 678 | **2026-01-21** | **6** | 7.6341 | 9.0 | 8.476† | **2026-01-26** | **8.1143** | **8.476** | +288 | ATR-1R‡ |

† Pyramid entered with engagement trail already **above** entry (stop_strategy=`move_to_last_entry` inheritance).  
‡ Live Edge snapshot counts n=3; stop-distance 1R is non-positive so 1R falls back to ATR×mult×units at persist time. Reconstructing without ATR excludes the lot (`n_excluded_no_1r`).

### Mechanism (not OA marking)

1. Same seed entry (2025-12-05 @ 3.4233 ×5) and same first pyramid (2026-01-14 @ 7.1301 ×5).  
2. Path capital / inventory after the **2021-08-12 fork** lets #678 **trail higher** (8.48 vs 7.06) and print a **third pyramid** (2026-01-21).  
3. #678 stops **two sessions earlier** (Jan 26) into an **8.11** premium; #667 holds to Jan 28 and dumps into **4.46** — the Jan-14 unit alone flips from +492 to −1,334.  
4. LEAP R uses `one_r = |prem − original_stop| × units` **without** the ×100 cash multiplier while PnL is ×100 → **tight pyramid stops produce four-digit R**. The −1784 eng mean is dominated by the −3809R pyramid loser, not by cash economics (−$814 net).

**Read:** Dominant **path-sensitivity** episode. Explains ~⅔ of the ΣR gap and ~**+22R** of the **+33.6R** mean-edge gap if taken alone (counterfactual #678 with #667’s COPR ΣR → mean ≈ **129** vs parent 117 / actual 151).

---

## 3. Deep-dive — XLK ~2021-08-12 fork

### What actually differed

Prior note said “#678 also **stops** two XLK lots (prem 12.51 / 11.58).” **Correction:** those are **pyramid entries** on #678, not stops.

| | #667 | #678 |
|--|------|------|
| Open into Aug 12 | Identical: XLK×2, NVDA×4, COPR short×2 (8 lots, 871 units, 11 long units) | Same |
| Aug 12 fills | XLF long u2 @5.938 · FPA short u4 @2.089 | **Same XLF+FPA** **+ XLK long u1 @12.5136** |
| Aug 13 fills | — | **XLK long u1 @11.5821** |
| XLK wave exit | **2021-10-04** @ ~10.1–10.5 (3 lots, net **−$280**) | **2021-09-20** @ trail 74.15 (4 lots, net **−$62**) |
| Eng `XLK:long:2021-06-17` | n=3 · **−47.56R** | n=4 · **−13.76R** |

### Why #667 missed the XLK pyramids — heat, not missing bar

`PassedSignal` on **2021-08-12**:

| Only on #667 | Only on #678 |
|--------------|--------------|
| **`XLK pyramid long` → `heat_close_corr`** (would-have u=159 share-units) | `XLF pyramid long` → `heat_direction` |
| WMT entry long → `no_price_level_touch` | WMT entry long → `heat_direction` |

So with **byte-identical open inventory** after Aug 11 ZROZ stops, turtle **close-correlation heat** blocked XLK on #667 and allowed it on #678. Downstream heat then blocked #678’s XLF pyramid / WMT long. Knobs (`heat_mode=turtle`, PCS thresholds, max units) are identical — this is **re-run heat / PCS non-determinism** (eval order or correlation snapshot drift), **not** a sticky-20D_BO or OA-curve change.

### Cash & equity on the fork day

- **Cash** first diverge **2021-08-12**: #678 **−$1,251** vs #667 (XLK premium outlay).  
- **Classic equity** first diverge same day: #667 $52.9k vs #678 $59.1k (share-MTM of the new XLK inventory + path). Curves were lockstep through **2021-08-11**.

### Cascade (not just +88 ΣR on the 2021 XLK eng)

Direct `XLK:long:2021-06-17` d ΣR is only **+88 (1.0%)**. The fork matters as the **seed**:

- Different XLK trail/exit → different free cash & heat into autumn 2021.  
- Later shared eng re-prices: `XLK:long:2023-03-17` **+413 ΣR (4.5%)**; `NVDA:long:2021-10-22` **+557 (6.1%)**; `NVDA:long:2024-01-08` **+1,727 (18.8%)**; and eventually the COPR blow-up.  
- First **closed-lot** asymmetry surfaces **2021-08-19** (WMT), then XLK Sep-20 vs Oct-04.

No evidence of missing bars, park bugs unique to one run, or stop-strategy knob drift — stop_strategy=`move_to_last_entry` on both.

---

## 4. How much of 117 → 151 do these episodes explain?

| Episode | d ΣR | % of +9,211 | Approx mean-edge impact† |
|---------|-----:|------------:|--------------------------|
| **COPR:long:2025-12-05** | **+6,158** | **66.9%** | **~+21.9R** |
| NVDA:long:2024-01-08 | +1,727 | 18.8% | ~+6.1R |
| NVDA:long:2021-10-22 | +557 | 6.1% | ~+2.0R |
| XLK:long:2023-03-17 | +413 | 4.5% | ~+1.5R |
| XLK:long:2021-06-17 (fork eng) | +88 | 1.0% | ~+0.3R |
| XLK:long:2021-10-26 | +22 | 0.2% | ~+0.1R |
| **Listed total** | **+8,966** | **97.3%** | — |
| Residual (other shared + unique) | +245 | 2.7% | — |

† `d ΣR / n_678` — illustrative; true edge is expectancy over the full lot set.

**Counterfactual:** replace #678’s COPR ΣR with #667’s → mean ≈ **129R** (still **+12R** above parent from NVDA/XLK/other path drift).

**Causal stack:**

1. **Seed:** Aug 12 `heat_close_corr` coin-flip on XLK pyramid.  
2. **Amplifier:** inventory/cash/heat diverge for the rest of the book.  
3. **Headline R:** COPR Dec-2025 engagement sign-flip (⅔ of ΣR gap), with LEAP tight-stop R inflation.  
4. **Not OA:** Blue #679 twin is exact on edge; Orange edge moved because **closes moved**.

Window +1 trading day explains **0** of the edge gap.

---

## 5. Findings (bullets)

1. **#678 edge 151 ≠ OA upgrade.** Closed-lot methodology unchanged; cite **#667 ~117.35**. Blue OA twin remains the clean control (edge identical).  
2. **First diverge = 2021-08-12** (cash & classic equity); first close-set diverge **2021-08-19** (WMT). Lockstep through 2021-08-11.  
3. **XLK fork = heat non-determinism:** identical open book, yet #667 `PassedSignal` **`heat_close_corr`** on XLK pyramid while #678 **fills** prem **12.51 / 11.58** (entries, not stops). Wave exits Sep-20 vs Oct-04.  
4. **COPR:long:2025-12-05** is the R monster: **−1784 → +863** (n=2→3), **+6,158 ΣR = 66.9%** of the edge gap; cash PnL **−$814 → +$3,126** via higher trail, earlier exit, extra Jan-21 pyramid.  
5. **LEAP R inflation:** pyramid `original_stop` ≈ prem → tiny 1R denominator vs ×100 PnL → four-digit lot R; eng means are path-fragile, not “OA got smarter.”  
6. **Shared eng re-pricing** (esp. NVDA 2024 +18.8% ΣR) — not unique-lot turnover — carries almost all of the remaining gap; unique eng only ~1% of ΣR.  
7. **OA path/wealth on #678 still usable** for dual-curve DD (~14.6%) and terminal OA equity ($143.5k flat); do **not** promote that wealth edge as a verified Edge win over Blue’s clean **137.58**.  
8. **Sticky 20D_BO** and LEAP knobs are not implicated — twin impurity is fill/heat path drift on re-stamp.

---

## 6. Recommendation — promote or hold?

### **HOLD Edge promotion of Orange over Blue. Frozen-as-of re-stamp Orange first.**

| Question | Answer |
|----------|--------|
| Promote Orange over Blue on **closed-lot Edge** using #678’s 151? | **No.** Drifted twin; cite **#667 ~117** (Blue **137.58** still leads verified Edge). |
| Promote Orange on **OA terminal wealth / OA DD**? | **Conditional yes for path ranking only** — #678 OA end **$143.5k** / DD ~**15%** still leads Blue OA **$110.4k** / ~**44%**, with the caveat that the **close tape is not a clean twin** of #667. Prefer a clean OA re-stamp before pack language. |
| Must we frozen-as-of re-stamp Orange? | **Yes**, before any Edge-primary pack claim or “Orange beats Blue on Edge.” Freeze DM as-of / PCS correlation inputs (or pin heat eval order) through at least **2021-08-12**, confirm XLK pyramid parity with #667, then OA-instrument. |
| Stamp new PBRs now? | **No** (per brief). This note is diagnostic only. |

**Pack line until re-stamp:** *Orange sticky-20D_BO Edge = **#667 ~117**; OA wealth/path illustrative from #678; Blue = clean Edge co-leader at **137.58** with exact OA twin #679.*

---

## Blockers / caveats

- Root cause of `heat_close_corr` disagreement with identical inventory not fully isolated (PCS snapshot time vs market-processing order). Treat as **lab re-run hazard**, not strategy alpha.  
- COPR lot-3 1R uses ATR fallback in the live snapshot; stop-distance 1R is invalid when inherited trail > entry.  
- `cash_vs_journal_delta` ≈ $129k remains on both Orange runs (pre-existing; not OA-specific).  
- No new PBRs stamped in this investigation.
