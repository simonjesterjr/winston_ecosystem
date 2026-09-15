# Orange #678 & Blue #679 OA twins vs parents & Red — book impact

**Date:** 2026-09-14 (PT)  
**Chassis:** sticky **20D_BO** Working Stop · TS#77 TurtleV1 S2 · $30k · turtle heat · risk 1% · `resting_stop_touch` · `leap_fulfillment=all` · atr_offset 0 · exp 730d · experiment `strategy77_rst_parity_v1`  
**Cells:** `orange_rst_turtle_r01_leap30k_oa` (#678 ← #667) · `blue_rst_turtle_r01_leap30k_oa` (#679 ← #668) · Red reference `#676` ← `#672`  
**Banner:** report only — option-aware equity dual curve (no pack promotion)  
**UI:** https://sawtooth-ai.tail944ffb.ts.net/wut/portfolio_backtest_runs/{678,679,667,668,676,672}

> Sticky **20D_BO** is locked; doctrine A stayed reverted.  
> † LEAP Edge/PF are **not** share-R-comparable — rank within LEAP panel only.

## 0. Headlines (verified)

| Metric | #667 Orange | #678 Orange OA | #668 Blue | #679 Blue OA | #672 Red | #676 Red OA |
|--------|-------------|----------------|-----------|--------------|----------|-------------|
| status | completed | completed | completed | completed | completed | completed |
| edge_r† | **117.35** | **150.97** | **137.58** | **137.58** | 59.43 | 62.40 |
| profit_factor† | 4.22 | 4.53 | 4.15 | 4.15 | 2.33 | 2.41 |
| edge_n / total_trades | 283 / 284 | 281 / 281 | 207 / 211 | 207 / 211 | 215 / 220 | 213 / 217 |
| win_rate | 41.7% | 43.4% | 30.0% | 30.0% | 38.6% | 39.0% |
| total_return (classic) | +364% | +378% | +318% | +318% | +134% | +133% |
| max_dd (classic field) | 89.0% | **102.9%** | 81.9% | 81.9% | 81.8% | 81.8% |
| final equity (classic) | $139,089 | $143,548 | $125,509 | $125,265 | $70,106 | $70,039 |
| OA final equity | — | **$143,548** | — | **$110,434** | — | **$65,187** |
| OA history pts | — | 1350 | — | 1534 | — | 1486 |
| window end | 2026-09-11 | **2026-09-14** | 2026-09-11 | **2026-09-14** | 2026-09-11 | 2026-09-14 |
| open at end | 1 | 0 (flat) | 4 | 4 | 5 | 4 |

Known headlines match (minor rounding). Blue classic return on #679 is +317.5% vs parent +318.4% solely from the extra calendar day / open MTM — **closed-lot edge identical**.

---

## 1. LEAP fidelity (#678 / #679)

| Check | #678 Orange OA | #679 Blue OA |
|-------|----------------|--------------|
| `is_option` / premium > 0 | **PASS** — **281/281** | **PASS** — **211/211** |
| Under-max 20-Day Breakout closes | **PASS** — **0** | **PASS** — **0** |
| Exit mix | Stop **276** / LEAP expired **5** / 20d **0** | Stop **206** / LEAP expired **1** / park **4** / 20d **0** |
| Direction | long 219 / short 62 | long 211 / short 0 |
| Premiums (min · med · max) | 0.05 · 6.46 · 19.98 | 1.48 · 6.64 · 25.81 |
| Top markets | XLF 35, FPA 35, WMT 34, MSOS 33, BITQ 31, GLTR 26, XLK 22, COPR 19, NVDA 19 | XLE 67, AAL 56, WMT 49, RXT 27, PG 9 |

**Overall LEAP acceptance: PASS** for both OA twins — faithful LEAP+RST S2 tape; no under-max 20d closes. (Red #676 previously PASS stop-only; Orange/Blue allow a few true LEAP expiries / Blue parks, still not under-max 20d.)

`extra_modal` is not a Position column here; LEAP intent is evidenced by `is_option=true` + positive premiums on every lot.

---

## 2. Classic vs OA path

### #678 Orange OA

| Path statistic | Classic `equity_history` | `option_aware_equity_history` |
|----------------|--------------------------|-------------------------------|
| points | 1350 | 1350 |
| end equity | $143,548 | **$143,548** (flat book) |
| max / min | $214,734 / **−$3,137** | $154,407 / $27,181 |
| max DD (curve) | **102.9%** (2023-09-20 → 2023-10-06) | **~14.6%** (2025-03-12 → 2025-04-08) |
| day-drops ≥ $15k | **34** | **0** |
| day-drops ≥ $5k | 75 | **3** |
| level correlation | — | **0.896** |
| daily Δ correlation | — | ~0.28 |

- Artifact cliffs (classic drop ≥ $15k **and** OA drop < 50% of classic): **34 / 34**.  
  Sum classic drops ≈ **−$943k** vs OA ≈ **−$20k** → ~**$923k** of chart cliff is share-MTM, not cash.
- Sample worst classic cliffs: 2025-04-07 (−48k classic / +$0.3k OA), 2024-06-11 (−43k / −$0.9k), 2021-08-11 (−42k / −$0.3k).
- Classic curve went **through zero** (min −$3.1k); OA never left the ~$27k–$154k band. Classic 102.9% DD is therefore **not** an economic LEAP DD.

### #679 Blue OA

| Path statistic | Classic | OA |
|----------------|---------|-----|
| points | 1534 | 1534 |
| end equity | $125,265 | **$110,434** |
| max / min | $135,489 / $17,533 | $110,700 / $17,383 |
| max DD (curve) | **81.9%** | **~44.1%** |
| day-drops ≥ $15k | **18** | **0** |
| day-drops ≥ $5k | 53 | **0** |
| level correlation | — | **0.859** |
| daily Δ correlation | — | ~0.20 |

- Artifact cliffs: **18 / 18**; sum classic ≈ **−$438k** vs OA ≈ **−$6k** (~**$432k** mark).
- Classic ≥ OA on **all** days (367 equal = flat-book / cash≈equity days). End gap (~$15k) is open LEAP share-notional vs BS mark (4 opens remain).
- Sample cliffs: 2021-07-22 (−43k classic / −$0.2k OA), 2023-11-16 (−40k / −$2.0k), 2023-09-29 (−37k / −$1.0k).

### Red reference (#676 vs #672)

Already reported: classic cliffs **33** vs OA **0**; OA DD ~35% vs classic 82%; OA trustworthiness **PASS** for path/DD. OA final **$65.2k** vs classic ~$70k.

**Path verdict:** OA dual curve is **trustworthy** for Orange and Blue equity-path / DD interpretation (same conclusion as Red). Do **not** rank LEAP books on classic DD alone — especially Orange’s 103% classic DD.

---

## 3. Why Orange #678 edge 151 vs #667 117?

**Not an “OA upgraded edge.”** Closed-lot Edge/PF methodology is unchanged by the OA curve; OA only marks open inventory on the dual equity series.

| Factor | Evidence |
|--------|----------|
| Window | #678 ends **2026-09-14** vs #667 **2026-09-11** (+1 trading day only on equity history). **Zero** positions with `bar_date ≥ 2026-09-11` on #678 — the extra day did **not** add a closed lot. |
| Path lockstep | Classic equity **identical through 2021-08-11**; first diverge **2021-08-12** (Δ ~$6k). Far earlier than Red’s Dec-2023 drift. |
| Close-set drift | Soft fingerprints: **230** shared; **54** only-on-667; **51** only-on-678. Engagements: 124 shared; 36 only-667; 30 only-678. |
| Unique engagement edge | Sum edge_r only-on-667 ≈ **+938R**; only-on-678 ≈ **+1088R**; unique-set Δ ≈ **+150R** — order-of-magnitude matches total edge gap. |
| Shared engagement blow-up | `COPR:long:2025-12-05`: **−1784R → +863R** (Δ **+2647R**) on n=2→3 lots — dominant path-sensitivity, not OA accounting. Also NVDA:long:2024-01-08 +576R, etc. |
| Avg loss / win | avg_loss_r 94 → 72; avg_win_r 413 → 441; win_rate 41.7% → 43.4% — consistent with a different loser/winner mix, not a marking change. |

**Aug 12 seed:** same-day XLF+FPA stops on both; #678 also stops two XLK lots (prem 12.51 / 11.58) that #667 does not — capital/inventory fork from there.

**Read:** Treat **+33.6 edge_r** as **lab re-run / fill-path drift + mid-sample COPR sensitivity**, amplified by a trivial window bump that adds no closes. Citing #678 as “OA made Orange better” is **FAIL**. For sticky Orange edge ranking prefer **#667 (~117)** unless a deliberate re-stamp with frozen DM as-of is accepted as the new baseline.

---

## 4. Blue twinship — good control

| Check | Result |
|-------|--------|
| Close fingerprints | **211 / 211 shared**; 0 only-on either side |
| Engagements + edge_r | **83 / 83** identical; **0** shared edge deltas |
| Classic equity | Common days **1533**; max abs Δ ~ **1e−8**; days with Δ>$1: **0** |
| Extra day | Only `2026-09-14` on #679; classic end $125,265 vs $125,509 (−$244 open MTM) |
| edge_r / PF / n | **137.58 / 4.15 / 207** — exact match |

**Blue is a pure OA instrumentation twin.** Use #679 for OA path/DD; use either for Edge. This is the control the Orange pair failed to be.

---

## 5. Book ranking (sticky 20D_BO · same knobs · OA-aware path)

† Within-LEAP only.

| Rank | Book | Edge cite† | OA end eq | OA curve DD | Classic ≥$15k cliffs → OA | Twin quality |
|------|------|------------|-----------|-------------|---------------------------|--------------|
| **1** | **Orange** | **#667 ~117** (not #678’s 151) | **$143.5k** (#678, flat) | **~14.6%** | 34 → **0** | Drifted twin — path PASS, edge cite parent |
| **2** | **Blue** | **137.58** (#668=#679) | **$110.4k** | **~44%** | 18 → **0** | **Clean twin** |
| **3** | **Red** | **~59–62** (#672 / #676) | **$65.2k** | **~35%** | 33 → **0** | Soft twin (prior note) |

**Ranking logic**

1. **OA path / DD:** all three PASS (cliffs gone). Orange’s OA DD (~15%) is best; Blue ~44%; Red ~35%.  
2. **OA terminal wealth:** Orange ≫ Blue ≫ Red.  
3. **Closed-lot edge (within LEAP):** Blue 137.6 slightly above Orange **parent** 117; Orange **OA twin** 151 is **not** eligible as an OA upgrade. Red clearly last (~60).  
4. **Practical pack read:** Orange still leads the sticky LEAP panel on OA equity path + terminal OA wealth; Blue is the honest Edge co-leader / best control; Red is the weaker third. If Edge-primary with clean twinship required, **Blue edges Orange’s verified 117** until Orange is re-stamped cleanly.

Do not compare any of these edge_r/PF figures to share Turtle R.

---

## 6. Verdict bullets

1. **LEAP tape PASS** on #678 and #679 (`is_option` + premiums; **0** under-max 20d).  
2. **OA path trustworthiness PASS** for Orange & Blue (and Red): classic ≥$15k cliffs **34 / 18 / 33** → OA **0 / 0 / 0**; OA DDs **~15% / ~44% / ~35%** vs classic **103% / 82% / 82%**.  
3. **Orange edge 151 ≠ OA upgrade** — diverge from **2021-08-12**; large close-set / COPR engagement drift; window +1 day adds **no** closes. Cite **#667 ~117** for Edge.  
4. **Blue twinship is exact** — identical edge 137.58; ideal OA control.  
5. **Within-LEAP sticky book rank:** **Orange (OA path/wealth) ≥ Blue (clean Edge) ≫ Red**; Edge-primary with twin purity → **Blue slightly over Orange-parent**.

---

## 7. Next steps

- **Cite #667 (~117), not #678 (151), for Orange Edge** in pack tables until a frozen-as-of Orange OA re-stamp locks closes through Aug 2021.  
- **Prefer OA equity + OA DD** for LEAP risk/wealth ranking across Orange/Blue/Red; keep classic equity only as a share-MTM diagnostic.  
- **Investigate `COPR:long:2025-12-05`** (−1784R → +863R) and the 2021-08-12 XLK fork before promoting Orange as an Edge winner over Blue.  
- **No new pack promotion / doctrine change** from these OA twins — instrumentation confirmation only; sticky 20D_BO remains locked.

## Blockers / caveats

- Orange `cash_vs_journal_delta` ≈ **$129k** on **both** #667 and #678 (pre-existing journal quirk, not OA-specific). Blue cash recon **~0**. Red ≈ **$4.4k** on both.  
- #672 Position rows were empty in DB at query time (metrics still on PBR); Red fidelity cited from prior `#676` analysis.  
- Mid-run fill drift on Orange (and mild on Red) is unexplained by OA marking — OA should not change fills.
