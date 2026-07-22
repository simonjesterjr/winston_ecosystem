# PBR Return / Drawdown / PCS Evaluation + What Made Blue Work

**Date:** 2026-07-13  
**Bucket:** `ecosystem/business_analysis/` (business / operator evaluation — not technical `docs/analysis/`)  
**Status:** Level 1 complete. Level 2 Phase 2.1 **C0 (PBR 62) + P1 (PBR 63) done**. Further R/X/E paths pending (see tickets).  
**Scope:** WUT lab PBRs for color cohorts (Red/Blue/Orange/White) + corr_v2 cohorts (Green/Pink/Mango/Rust).  
**Anti-overfit stance:** Describe what *already happened*; do not jointly re-search entry×exit×risk on the full sample. Pre-registered experiment paths only.

---

## 1. Executive snapshot

| Question | Short answer |
|----------|----------------|
| Best lab PBR overall? | **PBR 48 — Portfolio Blue**, `one_way_dynamic` + SwingBreakout5Day + VolExit only |
| Best already-gated “boring” cohort? | **PBR 55 Green** / **PBR 56 Pink** (trade_ready under static first-pass) |
| Was 48 jointly optimized? | **No** — entry won under static vet (and lost money); risk transferred from TS3 experiment; caps differ from vet |
| Biggest success component (hypothesis)? | **Risk regime + stop trail** (`one_way_dynamic` accelerating pyramid + `move_to_last_entry`), not multi-exit or confirm |
| Money left on the table? | **Yes on Blue/Orange** — large `portfolio_limit` / `market_limit` / cash passed-signal piles; Green is capacity-clean |
| First paper candidate? | **Blue 62 exploration** (§15, locked 2026-07-14); policies: max_markets=4, paper leverage 1×; **no real-money** until paper hygiene proves out |

### Headline metrics (WUT DB, 2026-07-13, post cash-equity re-run)

| Rank axis | Leader | Value |
|-----------|--------|-------|
| Total return | PBR 48 Blue | **+2073.5%** |
| Max drawdown (best) | PBR 48 Blue | **20.9%** |
| Practical Sharpe | PBR 48 Blue | **1.52** |
| Runner-up | PBR 44 Blue | +1532%, DD 34.7%, Sharpe 1.49 |
| Best PCS | Green | **83.39** (corr_v2) |
| Blue PCS | Blue | **76.15** |

**Viability gates** (`TradeReadyViabilityGates`: return ≥ 0, max DD ≤ 50%, trades ≥ 20) on current rows:

| PBR | export_kind | failures |
|-----|-------------|---------|
| 48 Blue | **trade_ready** | — |
| 44 Blue | **trade_ready** | — |
| 45 Orange | **trade_ready** | — |
| 40 White | **trade_ready** | — |
| 47 White | **trade_ready** | — |
| 55 Green | **trade_ready** | — |
| 56 Pink | **trade_ready** | — |
| 25 Red | observation | max_drawdown (52.1%) |
| 41 Orange | observation | max_drawdown (59.7%) |
| 23 Blue static | observation | return + DD |
| 57/58 Mango/Rust | observation | max_drawdown |

> Historical selections still show Blue/Red/White/Orange as observation from *original* vet metrics. Live re-run numbers on 44/48 now pass gates — treat that as **new evidence**, not as “the vet already blessed them.”

---

## 2. Full cohort table (Level 1 freeze)

| PBR | Port | Risk | Stop | max_mkt | max_port | Ret % | Max DD % | Sharpe | Trades | Cap | Equity | Cash | Notes |
|-----|------|------|------|---------|----------|-------|----------|--------|--------|-----|--------|------|-------|
| **48** | Blue | one_way_dynamic | move_to_last | nil | 10 | **2073.5** | **20.9** | **1.52** | 767 | 10k | 217k | 490k | Winner entry + TS3 risk ladder |
| **44** | Blue | one_way_dynamic | move_to_last | nil | 10 | 1532.1 | 34.7 | 1.49 | 582 | 10k | 163k | 335k | Full TS3 entry 20d + dual exit |
| 41 | Orange | static | move_to_last | 4 | 12 | 839.8 | 59.7 | 1.05 | 1697 | 10k | 94k | 88k | High activity; DD fail |
| 58 | Rust | static | move_to_last | 4 | 12 | 684.6 | 77.4 | 0.83 | 496 | 10k | 78k | 182k | observation |
| 57 | Mango | static | move_to_last | 4 | 12 | 671.5 | 55.0 | 0.84 | 814 | 10k | 77k | 114k | observation |
| 46 | Red | one_way_dynamic | move_to_last | nil | 10 | 398.4 | 68.6 | 0.70 | 626 | 10k | 50k | 20k | Winner+TS3 risk |
| 45 | Orange | one_way_dynamic | move_to_last | nil | 10 | 383.1 | 39.0 | 0.92 | 825 | 10k | 48k | 85k | Dynamic improved DD vs 41 |
| 25 | Red | static | move_to_last | 4 | 12 | 340.4 | 52.1 | 0.74 | 716 | 10k | 44k | 10k | Classic vet winner |
| 42 | Red | one_way_dynamic | move_to_last | nil | 10 | 300.0 | 65.2 | 0.69 | 776 | 10k | 40k | −1.5k | Full TS3 |
| **55** | Green | static | move_to_last | 4 | 12 | 292.4 | 48.3 | 0.95 | 323 | 10k | 39k | 45k | trade_ready + best PCS |
| 47 | White | one_way_dynamic | move_to_last | nil | 10 | 222.8 | 46.9 | 0.67 | 434 | 10k | 32k | 19k | |
| 40 | White | static | move_to_last | 4 | 12 | 207.1 | 35.3 | 0.69 | 509 | 10k | 31k | 21k | Best static DD (old colors) |
| 56 | Pink | static | move_to_last | 4 | 12 | 136.6 | 49.5 | 0.49 | 514 | 10k | 24k | 3k | trade_ready |
| 49 | Orange | one_way_dynamic | move_to_last | nil | 10 | 1.2 | 90.3 | 0.60 | 1232 | 10k | 10k | −2k | Winner+risk **failed** |
| 43 | White | one_way_dynamic | move_to_last | nil | 10 | 0.5 | 86.7 | 0.47 | 486 | 10k | 10k | 78k | Full TS3 weak |
| 23 | Blue | static | **isomorphic** | nil | 10 | −136.8 | 133.8 | −0.49 | 79 | 20k | −7k | −7k | Original vet disaster |
| 10 | Red | static | **isomorphic** | nil | 10 | −138.3 | 140.4 | 0.11 | 94 | 20k | −8k | −20k | Isomorphic death |

**Excluded from ranking trust:** PBR 50 (cash↔journal Δ ~$57k).

**Accounting flag:** Blue dynamic runs show **final_cash ≫ final_equity** with `max_leverage=3`. Treat as leverage/short mark-to-market residue until proven otherwise — do not read free cash as withdrawable P&L.

---

## 3. Composition / PCS overlay

| Portfolio | n | PCS (corr_v2) | as_of | Membership (abbrev) | PBR story |
|-----------|---|---------------|-------|---------------------|-----------|
| Green | 12 | **83.39** | 2026-07-12 | AMZA, BERZ, BFIX, CORN, ICLN, JNJ, PHYMF, SCHD, SH, SPTI, VXX, WMT | Best diversification; trade_ready static |
| Rust | 12 | 77.25 | 2026-07-12 | AAAU, AFIF, BFIX, BIS, DBA, DBE, GOOGL, RGI, RXT, SCHD, USDU, XLI | High ret / fail DD |
| Pink | 12 | 76.29 | 2026-07-12 | AFIF, AGZ, COM, DBA, FXI, IYH, JNJ, MSFT, PINK, UUP, WMT, WTI | trade_ready static |
| **Blue** | 11 | **76.15** | 2026-07-13 | AAL, AMZN, GLD, GOOGL, JNJ, PG, RXT, TSLA, TSMC, WMT, XLE | Good PCS; static fail → dynamic rescue |
| Red | 9 | 73.01 | 2026-07-12 | AMAT, CDE, MSFT, MSOS, PHYMF, ROKU, URA, VXX, XLV | Strong static; dynamic mixed DD |
| Mango | 12 | 71.30 | 2026-07-12 | AAAU, BIB, BWX, COMB, MSFT, PPLT, ROKU, RXT, SEF, SVXY, WTI, ZROZ | High ret / fail DD |
| Orange | 15 | 68.34 | 2026-07-12 | AAPL, BITQ, COPR, … XLK, ZROZ | High ret / high DD; COPR quality risk |
| White | 20 | **41.76** | 2026-07-12 | twins DBE/OILK; quality fails | Low PCS; capacity + junk |

### Hypotheses (Level 1)

1. **PCS ≈ survivability under static risk** more than max return — Green/Pink pass; White weak; Blue is the exception (good PCS, terrible static economics until risk regime change).
2. **Risk regime can dominate entry class on Blue** — SwingBreakout5Day that blew up under static becomes the best portfolio under accelerating pyramid risk.
3. **`move_to_last_entry` is necessary, not sufficient** — isomorphic 10/23 are non-survivors; many move_to_last runs still have bad DD.
4. **Capacity confounds return** — TS3 buckets (44/48) have **no max_markets**; vet winners use max_markets=4.
5. **Dynamic risk is not free alpha on every book** — Orange winner+dynamic (49) collapses; Red dynamic worsens DD vs static 25.

---

## 4. Was PBR 48 optimized?

**No — not jointly.** Provenance:

| Layer | What | Optimized? |
|-------|------|------------|
| Membership | Blue corr_v1 / overlap | For low mean \|r\|, not return |
| Entry/exit | Vet winner SwingBreakout5Day / **VolExit only** (`exit_ids [15]`) | Grid under **static** risk; 6×2 first-pass |
| Confirmational | **None** (`[]`) | Never used |
| Risk | TS3 `one_way_dynamic` ladder long `[2,3,4,6,6]%` / short `[2,2,2,3,3]%` | **Transferred** from TS3 experiment (PBR 42–49), not searched with Blue entry |
| Stops | `move_to_last_entry` | From TS3 / vet finals, not isomorphic |
| Caps | max_sym=5, max_port=**10**, max_markets=**nil** | Differs from vet (12 / 4) |
| Accounting | 2026-07-10 cash-equity re-run | Metrics rewritten; pre-fix ~+72% / DD ~118% |

**TS #13 Accelerating Risk** uses a *nearby* ladder `[2,3,3,4,4]` long — a small R2 A/B vs PBR 48’s R1, **not** a new regime.

---

## 5. Component attribution — what about 44/48 is repeatable?

### 5.1 Config contrast (fact)

| Component | PBR 48 (best) | PBR 44 (runner-up) | PBR 23 (static fail) |
|-----------|---------------|--------------------|----------------------|
| Entry | SwingBreakout5Day (TSS13) | Breakout20Day (TSS1) | SwingBreakout5Day |
| Exits | **VolExit only [15]** | **Dual [1, 15]** (20d breakout + Vol) | VolExit |
| Confirm | none | none | none |
| Risk | one_way_dynamic R1 ladder | same R1 ladder | **static** |
| Stop | move_to_last_entry | move_to_last_entry | **isomorphic** |
| max_markets | nil | nil | nil |
| max_port | 10 | 10 | 10 |
| Result | +2073% / DD 21% | +1532% / DD 35% | −137% / DD 134% |

### 5.2 Ranked contribution hypotheses (to be falsified in Level 2)

| Rank | Component | Evidence for | Evidence against | Repeatability |
|------|-----------|--------------|------------------|---------------|
| **1** | **Risk regime (`one_way_dynamic` + accelerating pyramid)** | 23→48 same entry family, economics invert; 41→45 Orange DD improves with dynamic | 49 Orange winner+dynamic fails; Red 25→46 return ok but DD worse | **Transfer test required** (Green/Red under same R1) |
| **2** | **Stop = `move_to_last_entry`** | Isomorphic 10/23 dead; all top runs use move_to_last | Many move_to_last still fail DD | Necessary condition |
| **3** | **Capacity (no max_markets)** | 44/48 uncapped markets; Orange 41 has 2.4k market_limit passes | Green thrives *with* max_mkt=4 | Confound — **C0 re-run of 48 is mandatory** |
| **4** | **Pyramid structure (levels + ATR step)** | Both 44/48 use max_pyr=5, pyr_atr=1.0, accelerating % | Flat/static 2% is the vet baseline that killed Blue | De-risk ladder R3 tests “acceleration vs any dynamic” |
| **5** | **Entry class** | 48 > 44, so Swing5 helps *given* R1 | 44 still excellent with 20d — entry not unique | Cross-apply entries across books |
| **6** | **Multi-exit (vol OR opposite breakout)** | 44 has dual exits | **48 is better with single VolExit** | Dual exit is **not** what made 48 win; X1 A/B on Swing entry still useful |
| **7** | **Confirmational entry** | — | **Unused on all top PBRs** | Open Path X3 — may reduce bad entries / change pass mix |
| **8** | **PCS / membership** | Blue PCS 76; not junk-filled | Static still failed — membership alone insufficient | PCS necessary for static trade_ready cohorts |

### 5.3 “If we add exit ABC / confirm XYZ?”

| Idea | Prior from data | How to test without curve-fit |
|------|-----------------|-------------------------------|
| Extra exit (ATR, max-hold, profit target) | Unknown; dual exit on 44 did **not** beat single Vol on 48 | One-at-a-time on **frozen** Blue R1 entry (Path X) |
| Confirmational entrance | Zero usage on winners | Add one approved confirm (e.g. Penetration25Day); measure **Sharpe/DD/pass reasons**, not max return |
| More exits “because TS3 has [1,15]” | TS3 dual-exit underperforms 48’s single exit on Blue | Do not assume dual is better |

### 5.4 Candidate repeatable recipe

> **PCS ≳ 70 membership** + **enough trade activity** + **`one_way_dynamic` accelerating pyramid** + **`move_to_last_entry`** + **VolExit (or dual)** + **honest capacity caps**.

Not yet proven: SwingBreakout5Day as universal entry; uncapped markets; leverage 3.

---

## 6. Passed-signal capacity audit (operator request)

### 6.1 Why this matters

Passed signals record entries/pyramids the engine **wanted** but **did not take**. If we are full of mediocre pyramids while high-ER new markets are `market_limit` / `portfolio_limit` blocked, we leave money on the table — or, conversely, capacity blocks are *protecting* us from overtrading.

### 6.2 Reason histograms (selected PBRs)

| PBR | Port | # passed | Top reasons | Capacity story |
|-----|------|----------|-------------|----------------|
| **48** | Blue | **12,078** | no_units 6764, insufficient_cash 2628, **portfolio_limit 2078**, margin 582 | Extremely signal-heavy; hard portfolio full; huge reject pile |
| **44** | Blue | 3,486 | no_units 1939, cash 1103, portfolio_limit 306 | Same regime, quieter entry |
| **41** | Orange | 6,007 | **market_limit 2456**, no_units 1725, cash 884, portfolio_limit 414 | **max_markets=4 is the main throttle** |
| 25 | Red | 1,293 | cash 877, margin 265, market_limit 80, portfolio_limit 40 | Moderate; vet caps binding lightly |
| **55** | Green | 725 | cash 583, margin 137 | **No market/portfolio limit blocks** — capacity clean |
| 56 | Pink | 1,832 | cash 1376, margin 426 | Cash-bound, not slot-bound |
| 23 | Blue static | 7,058 | no_units 3849, cash, margin, portfolio_limit | Many signals, capital destroyed |

`lower_atr_priority` counts are small everywhere (priority ranking among same-day signals works; not the main loss channel).

### 6.3 Notional proxy (price × units on capacity-ish reasons)

Rough sum of `would_have_price * would_have_units` for cash/margin/portfolio/market blocks (not expected P&L — scale of blocked intent only):

| PBR | Notional proxy | Interpretation |
|-----|----------------|----------------|
| 48 | ~$15.2M | Enormous blocked intent; many rows have 0 units (price-only / no_units mix) |
| 41 | ~$8.4M | Market-limit dominated |
| 56 | ~$10.8M | Cash/margin |
| 25 | ~$6.3M | Cash-heavy |
| 44 | ~$5.7M | |
| 55 | ~$5.7M | Fewer events, still cash notionals |

**Caveat:** `would_have_units=0` on many market_limit rows → notional understates pure “slot” blocks. Prefer **counts by reason** + sampling for decisions.

### 6.4 Interpretive conclusions

1. **Blue 48 success is not “we took every good signal.”** It is “we took a capacity-constrained subset under aggressive risk sizing and still compounded.” Optimization may mean **better selection among signals** (position swap / ER rank), not only more slots.
2. **Orange leaves the most *obvious* slot alpha on the table** via `market_limit` — first place to test swap (P1) or slightly higher max_markets (P2) under DD guardrails.
3. **Green/Pink trade_ready runs are not capacity-starved on slots** — confirm/extra exit experiments there are about *signal quality*, not queue overflow.
4. **Position swap** exists (`PortfolioBacktest::PositionSwapEvaluator` for portfolio_limit / market_limit). **Confirmed:** vet-style runs **25/55 have `enable_position_swap: true`**; **44/48 have the key missing → swap off**. So Blue’s best runs ran with **dumb capacity** (no ER-based replacement of weak open risk). Path P1 (swap on) is high value for “money left on the table.”

### 6.5 Analysis we are *not* doing yet (tedious but valuable)

True “distressing money left on table” needs counterfactual paths: for a sample of `portfolio_limit` days, compare ER of blocked signal vs weakest open position’s subsequent contribution. That is a research script (P3), not a single backtest. Defer until P0/P1 results say the pile is economically meaningful.

---

## 7. Paired deltas (static ↔ dynamic / stop)

| Pair | Change | Δ Return | Δ Max DD | Lesson |
|------|--------|----------|----------|--------|
| Blue 23 → 48 | static+iso → dynamic+trail, same entry family | −137% → +2073% | 134% → 21% | **Risk+stop rescue** |
| Blue 23 → 44 | + 20d entry + dual exit + dynamic | −137% → +1532% | 134% → 35% | Risk family works with other entries |
| Red 25 → 46 | static → dynamic, same winner entry | 340% → 398% | 52% → 69% | Dynamic **hurts DD** on Red |
| White 40 → 47 | static → dynamic | 207% → 223% | 35% → 47% | Mild return, worse DD |
| Orange 41 → 45 | static → full TS3 dynamic | 840% → 383% | 60% → 39% | Lower return, **better DD** (trade_ready) |
| Orange 41 → 49 | static → winner+dynamic | 840% → 1% | 60% → 90% | Dynamic + short entry **fails** |

**Repeatability takeaway:** Accelerating risk is **not** a universal booster. It is a **Blue-shaped** (and sometimes Orange DD) tool. Transfer experiments (Phase 2.2) are mandatory before “use TS13 everywhere.”

---

## 8. Top 5 for Level 2 optimization review

| # | PBR | Why |
|---|-----|-----|
| 1 | **48 Blue** | Best return + DD + Sharpe; capacity stress case |
| 2 | **44 Blue** | Isolates entry + multi-exit vs 48 |
| 3 | **41 Orange** | Static return leader; market_limit stress case |
| 4 | **55 Green** | Best PCS + trade_ready; optimize without breaking gates |
| 5 | **25 Red** | Classic vet winner; dynamic transfer already mixed |

---

## 9. Pre-registered Level 2 paths (summary)

See session plan for full catalog. Paths: **R** risk, **S** stop, **C** capacity, **K** risk%/leverage, **E** entry transfer, **P** passed-signal/swap, **X** exit/confirm, **M** membership.

### Phase 2.1 priority (confounds before promotion)

1. Blue 48 config @ **C0** (max_markets=4, max_port=12) + R1 — does excellence survive vet caps?  
2. Blue 48 @ **R2** TS13 ladder — small A/B  
3. Blue 48 @ **R3** conservative ladder — is acceleration necessary?  
4. Blue Swing + R1 + **X1** dual exit `[1,15]` — multi-exit on best entry  
5. Blue R1 + **P1** position_swap on (if off)  

**Stop rule:** If C0 destroys Blue 48 economics, do **not** paper-trade uncapped 48 as “strategy skill”; prefer Green/Pink as first paper.

### Phase 2.2 transfer

- Red winner entry + R1 (vs 46)  
- Green 55 entry + R1  
- Orange 41 entry + R1 under C0  

### Exit / confirm (operator questions)

- X1–X3 as above; success metric = **Sharpe + DD + pass-reason mix**, not max return alone.

---

## 10. Paper-first recommendation (provisional)

| Priority | Candidate | Why | Caveats |
|----------|-----------|-----|---------|
| **A — disciplined** | **Green PBR 55** (static, trade_ready, PCS 83) | Clean capacity, gates honest, corr_v2 membership | Lower lab return than Blue |
| **B — explore** | **Blue PBR 62 (C0)** or 48 family paper after cash/leverage sanity | 62 keeps trade_ready under honest max_markets=4; 48 is lab upper bound | cash≫equity; swap-on (63) did **not** help; not jointly optimized |
| **Avoid for now** | White (PCS 42), Orange static 41 (DD), isomorphic anything | Structural / DD / dead stops | |

**Real capital:** not recommended from this analysis alone.

---

## 11. Open questions for operator

1. First paper OP: **Green discipline** vs **Blue exploration**? — **Blue 62 exploration** (locked 2026-07-14; see §15)  
2. Ops max_markets: force **4** or allow nil? — **decided: force 4**  
3. Allow `max_leverage=3` on paper? — **decided: force 1×** on paper focus  
4. Invest in P3 counterfactual pass-signal study this cycle or only after C0/P1?

---

## 12. Experiment log (Level 2 — fill as runs complete)

| New PBR | Path | Parent | Config delta | Ret | DD | Sharpe | Pass # | Notes |
|---------|------|--------|--------------|-----|----|--------|--------|-------|
| **62** | C0 | 48 | max_mkt=**4**, max_port=**12**, R1, swap **off**, VolExit only | **1415.4** | **41.6** | **1.11** | 5766 | Still **trade_ready**; ~31 min. vs 48: −658pp ret, +21pp DD |
| _pending_ | R2 | 48 | TS13 ladder | | | | | |
| _pending_ | R3 | 48 | conservative ladder | | | | | |
| _pending_ | X1 | 48 | exits [1,15] | | | | | |
| **63** | P1 | 48 | same as 48 + **position_swap on** | **974.6** | **31.5** | **1.22** | 4990 | trade_ready but **worse** than 48; swap ≠ free alpha |

### Phase 2.1 C0 interpretation (PBR 62 vs 48)

| | PBR 48 (C1 uncapped) | PBR 62 (C0 vet caps) |
|--|----------------------|----------------------|
| max_markets | nil | **4** |
| max_port | 10 | 12 |
| Return | 2073.5% | **1415.4%** |
| Max DD | 20.9% | **41.6%** |
| Sharpe | 1.52 | **1.11** |
| Trades | 767 | **1443** (more churn under tighter markets?) |
| Gates | trade_ready | trade_ready |
| Pass mix | no_units + cash + portfolio_limit | cash + **market_limit 1746** + margin |

**Stop-rule result:** Blue excellence does **not** disappear under vet caps — still excellent and trade_ready — but **uncapped markets were a large free lunch** (much better DD and Sharpe). Do not paper-trade nil max_markets as if it were pure signal skill; prefer documenting **max_markets=4** as the honest ops config, or explicitly accept higher concurrency as a policy choice.

**Capacity under C0:** `market_limit` becomes the dominant slot block (as with Orange 41). Path P1 (position swap) under C0 is the natural next lever for “better slots, not more slots.”

### Phase 2.1 P1 interpretation (PBR 63 vs 48)

| | PBR 48 (swap **off**) | PBR 63 (swap **on**) |
|--|----------------------|----------------------|
| Return | 2073.5% | **974.6%** |
| Max DD | 20.9% | **31.5%** |
| Sharpe | 1.52 | **1.22** |
| Trades | 767 | 1240 |
| portfolio_limit passes | 2078 | **530** |
| cash/margin passes | high | still dominant |

**Finding:** Enabling position swap **reduced** portfolio_limit rejects (capacity “worked”) but **hurt** return and DD vs leaving swap off. So “money left on the table” is **not** automatically recoverable by ER-based swaps on this Blue recipe — swaps may eject winners mid-pyramid or prefer noisy short-horizon ER. Still trade_ready; not an improvement over 48.

**Implication for operator concern:** Large pass piles ≠ proven left-behind alpha. Need P3 counterfactual (blocked signal’s subsequent path vs kept position) before optimizing for fewer passes. Prefer C0 honesty + R-path de-risk over “take more signals.”

---

## 13. References

- Plan: session plan (PBR performance × composition)  
- Gates: `ecosystem/docs/business-context/trade-ready-viability-gates.md`  
- First-pass doctrine: `ecosystem/docs/analysis/portfolio-trading-strategy-evaluation.md`  
- PCS ADR: `ecosystem/docs/adr/ADR-007-portfolio-correlation-score-sot.md`  
- TS3 experiment: `winston_unit_test/docs/session-reports/2026-07-09-1614-ts3-portfolio-backtest-reruns.md`  
- Cash re-run batch: `winston_unit_test/docs/session-reports/2026-07-10-1649-pbr-batch-rerun-sticky-headers.md`  
- Blue membership ticket: `ecosystem/docs/tickets/2026-07-07-revisit-portfolio-blue-membership-strategy.md`  
- Code: `PortfolioBacktest::EntryPassReason`, `PositionSwapEvaluator`, `TradeReadyViabilityGates`, `PortfolioBacktestRunner` pyramid_risks load  

---

## 14. Next actions (tickets)

| Action | Ticket |
|--------|--------|
| Remaining Level 2 runs (R2/R3, X1/X3, transfer E, optional P3/K) | `docs/tickets/2026-07-13-pbr-level2-remaining-experiments.md` |
| Paper-first cohort decision (Green 55 vs Blue 62) | `docs/tickets/2026-07-13-paper-first-cohort-decision.md` |
| Expose this library in WUT UI | `docs/tickets/2026-07-13-wut-expose-business-analysis-link.md` |
| Blue membership ticket (risk-rescue evidence noted) | `docs/tickets/2026-07-07-revisit-portfolio-blue-membership-strategy.md` |

**Done this cycle:** C0 (62), P1 (63), swap flag confirmed off on 44/48, experiment log updated, paper recommendation provisional.

---

## 15. Operator decision addendum — paper-first policies + cohort

**Ticket:** `docs/tickets/2026-07-13-paper-first-cohort-decision.md`  
**Status:** **Done** — capacity, leverage, cohort (**Blue 62**). Phase 1 (2026-07-14): OP `#12 Portfolio Blue · PBR62` sole Active; first paper journal confirmed (AMZN).

| Decision | Choice | When | Rationale (operator) |
|----------|--------|------|----------------------|
| First paper OP seed | **Blue 62 (exploration)** | 2026-07-14 | C0 honest-cap Blue family for first paper journals; higher-return explore path under locked caps |
| Ops `max_markets` | **Force 4** | 2026-07-13 | Matches C0 honesty; uncapped 48 is lab free lunch, not ops default |
| Paper `max_leverage` | **Force 1×** on paper focus | 2026-07-13 | De-risk cash≫equity mark-to-market residue before trusting paper capital narrative |
| Active hygiene timing | **Deferred** (record only) | 2026-07-14 | Six color Actives unchanged until Phase 1 hygiene session |
| Real capital | **Out of scope** | locked | Until paper hygiene (journals / confirm loop) proves out |

### Implications for lab and ops

1. **Do not paper-trade nil `max_markets`** as the primary ops story. Further Blue research may still run uncapped in WUT for science, but exports intended for paper must document **max_markets=4**.  
2. **Paper focus sizing is 1× leverage** until K-path (or accounting proof) reopens 3×.  
3. **Live Wv2 Portfolio Blue is still the static isomorphic vet export**, not PBR 62. Phase 1 must **export C0 / PBR 62 recipe from WUT → import lineage-correct OP** (auto-fork if needed), then focus Active on that OP. Do **not** treat current Blue id=7 as the paper-focus methodology.  
4. **Green 55** remains the best discipline/PCS alternate archive; demote when hygiene runs unless operator force-keeps a secondary.  
5. **First paper journal confirm** targets the Blue 62 focus OP only (`2026-07-13-confirm-first-paper-journal-focus-cohort.md`).

### Still open (execution, not decision)

- Phase 1: Blue 62 export/import + Active hygiene (`2026-07-13-paper-focus-active-hygiene-and-recipe.md`)  
- Phase 1: first paper journal confirm on that OP  
- Optional lab: Level 2 transfer/R paths (do not block paper ops)  
