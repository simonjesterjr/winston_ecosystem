# TS75 LEAP Edge accounting audit (S1 vs S2)

**Banner:** report only — no pack promotion · no new stamps.  
**Date:** 2026-09-15 (PT)  
**Cells:** PBRs **#682–#697** (`strategy75_leap_risk_ab_v1`, Turtle **S1** Breakout20/**10**)  
**Refs:** TS77 LEAP $30k — Orange **#667**, Blue **#668**, Red **#672** (`strategy77_rst_parity_v1`)  
**Question:** Why do S1 LEAP RST $30k cells show absurd Edge (hundreds–thousands) and huge returns vs the S2 LEAP panel?

---
> **Fix direction locked (operator 2026-09-15):** Signal-path 1R (A) = `|order_price − original_stop| × contracts × 100`. Tracked in [`docs/tickets/2026-09-15-wut-leap-edge-signal-path-1r.md`](../tickets/2026-09-15-wut-leap-edge-signal-path-1r.md). WUT implementation in flight.


## Verdict (one line)

**Stored `edge_r` is broken for LEAP lots (S1 and S2)** — mis-scaled 1R (premium entry mixed with underlying 2N stop; longs fall through to `ATR×2×contracts` with no ×100). Cash PnL / PF / equity path can still be “real” in the sim, but **Edge is not share-R-comparable and must not drive today’s Wv2 paper selection.** Prefer PF + solvency-gated return/DD (+ optional recomputed signal-path or premium-at-risk Edge).

---

## How Edge is supposed to work vs what LEAP feeds it

Per `ecosystem/interfaces/winston-edge-v1.md` and `EdgeCalculator`:

```
one_r_dollars = |entry_price − original_stop| × units
                else ATR_entry × atr_multiplier × units
lot_r         = realized_pnl / one_r_dollars
edge_r        = (W × avg_win_r) − (L × avg_loss_r)
```

LEAP position booking (`PositionManager#add_leap_position`):

| Field | LEAP meaning |
|-------|----------------|
| `units` | **contracts** (not shares) |
| `execution_price` / `option_premium` | **premium per share** |
| `order_price` | underlying fill (pyramid / 1N reference) |
| `original_stop` / `updated_stop` | **underlying 2N** Working Stop |
| Cash PnL on close | `(exit_prem − entry_prem) × contracts × 100` |

`TradeTimelineBuilder` then passes **`entry_price = execution_price` (premium)** and **`original_stop` (underlying)** into `EdgeCalculator.one_r_dollars` — the share formula on option fields.

### What actually happens

1. **Long LEAP (dominant path):** `premium − underlying_stop` is **negative** (stop ≫ premium) → distance branch skipped → **ATR fallback** `one_r = ATR × 2 × contracts` (**no ×100**). Typical 1R ≈ **$2–$4** while cash PnL is thousands → winners print **hundreds–thousands of R**.
2. **Short LEAP:** `underlying_stop − premium` is positive → `one_r = mix_dist × contracts` still **missing ×100** and still mixing premium with underlying dollars → R inflated ~×100 vs cash risk.
3. **Penny / near-parity names (e.g. COPR):** when premium ≈ stop, mix distance collapses → **extreme |R|** on tiny denominators (seen on both S1 and S2).

Cash-side LEAP accounting (premium mark ×100, extra-modal stop pierce → option mark) is coherent; **only the Edge 1R denominator is wrong.**

---

## Panel snapshot (stored metrics)

| id | book | TS | risk | edge_r | n | PF | return | max_dd | final_eq | exit mix |
|----|------|----|------|--------|---|----|--------|--------|----------|----------|
| 667 † | Orange | 77 | 1% | **117.4** | 283 | 4.22 | +364% | 89% | 139k | stop 278 / exp 5 / **20d 0** |
| 668 † | Blue | 77 | 1% | **137.6** | 207 | 4.15 | +318% | 82% | 126k | stop 206 / exp 1 / **20d 0** |
| 672 † | Red | 77 | 1% | **59.4** | 215 | 2.33 | +134% | 82% | 70k | stop 215 / **20d 0** |
| **682** | Orange | **75** | 1% | **916** | 619 | 7.35 | **+4299%** | 47% | 1.32M | stop 293 / **10d 326** |
| 683 | Orange | 75 | 2% | 778 | 768 | 2.73 | +6680% | 69% | 2.03M | stop 367 / 10d 401 |
| **684** | Blue | **75** | 1% | **883** | 406 | 24.2 | **+2993%** | 34% | 928k | stop 202 / **10d 204** |
| 685 | Blue | 75 | 2% | 920 | 731 | 4.89 | +8931% | 45% | 2.71M | stop 360 / 10d 371 |
| 686 | Mango | 75 | 1% | 862 | 830 | 1.68 | +2838% | 78% | 881k | stop 449 / 10d 381 |
| 687 | Mango | 75 | 2% | 609 | 239 | 0.90 | −352% | 150% | **−76k** | stop 141 / 10d 98 |
| 688 | Mint | 75 | 1% | **4098** | 127 | 0.72 | −1828% | 134% | **−518k** | stop 61 / 10d 66 |
| 692 | Red | 75 | 1% | 887 | 422 | 27.7 | +3513% | 26% | 1.08M | stop 250 / 10d 172 |
| 693 | Red | 75 | 2% | 873 | 564 | 10.1 | +8183% | 53% | 2.48M | stop 323 / 10d 241 |
| 690–691, 694–697 | Y/G/Rust | 75 | 1–2% | 705–1483 | 46–375 | 0.47–0.91 | deeply negative | 174–331% | **insolvent** | 10d + stop |

† S2 LEAP refs. All listed cells: **100% `is_option` closes** (LEAP fidelity PASS).

---

## Sample lots — #682 (Orange S1 1%) and #684 (Blue S1 1%)

### 1R path split (#682)

- **458 / 619** lots → ATR-fallback 1R (almost all longs)  
- **161 / 619** lots → premium−stop mix distance (mostly shorts / odd parity)

Example long (ATR path): GLTR prem≈$17.9, und stop≈$99.8, `one_r = ATR×2×1 ≈ $2.43`, cash winner tens of thousands → **R in the thousands**.

Example COPR long (tiny mix dist): prem $3.17 → $7.30, und 2N dist $0.51, stored `1R_brk=$1.86` → **R_brk≈1112**; honest signal-path R ≈ **8.1**; premium-at-risk R ≈ **1.3**.

### Recomputed Edge (same closes, alternate 1R)

| PBR | stored edge_r | signal-path 1R† | premium-at-risk 1R‡ | PF (unchanged) |
|-----|---------------|-----------------|---------------------|----------------|
| 682 Orange S1 1% | 916 | **8.45** | **1.51** | 7.35 |
| 684 Blue S1 1% | 883 | **8.93** | **1.85** | 24.20 |
| 667 Orange S2 1% | 117 | **1.60** | **0.29** | 4.22 |
| 668 Blue S2 1% | 138 | **1.47** | **0.28** | 4.15 |

† `one_r = |order_price − original_stop| × contracts × 100` (underlying 2N × shares controlled).  
‡ `one_r = entry_premium × contracts × 100` (cash at risk to zero).

Stored S2 “117–138R” is the **same bug**, just fewer / stickier winners so the headline looks “merely large” instead of “absurd.”

---

## Why returns look enormous

1. **LEAP cash leverage is real in-sim:** unit heat sizes from underlying 2N risk, but outlay is premium×100×contracts ≪ share notional → more concurrent risk units and fatter cash winners when trends run.
2. **S1 harvests channel exits:** TS#75 exit = **`Breakout10DayStrategy`** (classic Turtle S1: entry 20 / exit **10**). On #682 ≈ **53% of closes are 10-day breakout exits** (326/619); on #684 ≈ **50%** (204/406). That is **by design**, not a bug — and it is **not** S2’s under-max **20d sticky suppression** (S2 refs: **0** channel exits).
3. **Compounding on a solvent book:** Orange/Blue/Red S1 1% never go cash-negative; equity compounds from $30k → ~$0.9–1.3M. Risk is % of capital → absolute unit size scales with the equity path.
4. **Edge does not require solvency:** Mint #688 `edge_r≈4098` with **final_equity −$518k**, PF 0.72 — proof that stored Edge is **not** a portfolio-selection score.

Returns on solvent S1 LEAP cells can be “real” *as cash-sim outcomes* and still be **non-comparable** to share Edge or to S2 sticky geometry without a fixed 1R definition.

---

## Exit mix clarification (S1 vs S2)

| System | TS | Channel exit | Observed on LEAP $30k |
|--------|-----|--------------|------------------------|
| **S1** | #75 Breakout20/**10** | **10-day** breakout (under-max closes **allowed**) | ~45–55% of closes are `10-Day Breakout exit` |
| **S2** | #77 Breakout55/**20** | 20-day under-max **suppressed** (sticky Working Stop) | **0** `20-Day` closes on #667/#668/#672 |

Operator note: “S1 exit is 20-day” is incorrect for TS#75 — fingerprint says **`Breakout10DayStrategy`**. The audit question’s “under-max 20d on S1” maps to **under-max 10d**, which **do** fire.

---

## Findings (8 bullets)

1. **Stored LEAP `edge_r` is accounting-broken**, not a mysterious S1 alpha: 1R mixes **premium entry** with **underlying stop** (or ATR×2×contracts without ×100).
2. **Long LEAP lots almost always take the ATR fallback** (`premium − stop < 0`), yielding ~$2–4 1R vs cash PnL ×100 → **avg_win_r in the 1500–6600R range** on S1 cells.
3. **S2 LEAP refs are broken the same way** (stored 59–138R → recomputed signal-path ~1.5R / premium-at-risk ~0.3R); S1 looks worse because more / larger premium winners hit the tiny denominator.
4. **Cash PnL, PF, and LEAP fidelity are trustworthy**; PF is identical under recomputed R (same numerator).
5. **S1 10-day exits are real and frequent** (~half of closes) — different geometry from S2 sticky suppression, not an Edge bug.
6. **Huge solvent returns** (Orange/Blue/Red) = LEAP outlay leverage + compounding + S1 channel harvest; do not read them as “916R Edge.”
7. **Insolvent books with huge positive Edge** (Mint/Yellow/Green/Rust) disqualify stored Edge for ranking.
8. **For Wv2 paper selection today:** do **not** rank on stored `edge_r` for any LEAP cell; rank within LEAP panels on **PF + solvency + return/DD**, optionally with a **recomputed** signal-path or premium-at-risk Edge — and treat S1 vs S2 as different exit doctrines.

---

## Recommended scoreboard metrics for S1 LEAP (today)

Use this glance set until EdgeCalculator grows an explicit LEAP 1R mode:

| Metric | Role |
|--------|------|
| **`final_equity > 0` (solvency gate)** | Hard filter — drop insolvent books |
| **`profit_factor`** | Primary skill score (cash wins/losses) |
| **`total_return` / `max_drawdown`** | Path quality; flag DD ≥ 80% |
| **`edge_n` + LEAP fidelity** (`is_option` closes / n) | Sample + packaging honesty |
| **Exit mix** (stop vs 10d vs exp) | Doctrine check for S1 |
| **Optional: recomputed `signal_path_edge_r`** | Comparable across LEAP cells if 1R = underlying 2N × shares_controlled |
| **Optional: `premium_at_risk_edge_r`** | Cash-risk view (1R = premium outlay) |
| **Do not use** stored `edge_r` / `avg_win_r` / `avg_loss_r` | Mis-scaled for LEAP |

**Wv2 paper pick heuristic (LEAP $30k lab):** among solvent S1 cells with PF ≫ 1 and acceptable DD, prefer **Blue #684** / **Red #692** / **Orange #682** (1% risk) on PF+DD — *not* on stored Edge. Do not promote packs from this audit; no restamps.

---

## Code pointers (no changes made)

- `PositionManager#add_leap_position` — premium in `execution_price`, underlying 2N in `original_stop`, `units` = contracts  
- `PortfolioBacktest::TradeTimelineBuilder` — feeds those fields into `EdgeCalculator.one_r_dollars`  
- `EdgeCalculator.one_r_dollars` — share formula; negative long distance → ATR×mult×units  
- Close PnL — correctly uses `× 100` for options (`PortfolioBacktestRunner` / `PositionManager#remove_positions`)

**Fix direction (future ticket, not this audit):** for `is_option` lots, define 1R explicitly as either (A) underlying `|order_price − original_stop| × units × 100` or (B) `premium × units × 100`, and never mix premium with underlying stop in the distance branch.

---

## Artifacts / probes

- This doc: `ecosystem/docs/analysis/2026-09-15-ts75-leap-edge-accounting-audit.md`  
- Probes (local, not stamps): `winston_unit_test/tmp/probes/audit_ts75_leap_edge.rb`, `audit_ts75_leap_edge_b.rb`  
- S2 panel context: `ecosystem/docs/analysis/2026-09-14-strategy77-leap30k-7book-panel.md`
