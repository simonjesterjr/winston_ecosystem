# Stack ARR / MER defaults and engagement grouping (locked)

**Date:** 2026-08-04  
**Code:** `PortfolioBacktest::StackArrCalculator`, `TradeTimelineBuilder`  
**Ticket:** `docs/tickets/2026-08-04-stack-arr-mer-risk-scale-chart.md`

---

## ARR (unchanged)

| Rule | Value |
|------|--------|
| Lot \(r_i\) | Signed \((P_{exit}-P_{entry})/\mathrm{ATR}_i\) |
| \(\mathrm{ATR}_i\) | Per-lot entry ATR |
| Stack ARR | **Unweighted** \(\sum r_i\) — OWD risk % does not weight |
| Engagement | Market + direction, continuous open book → flat |

---

## MER defaults (locked)

Trend Following thesis: a **trend engagement** targets ~**4 ATR** capture with ~**1 ATR** stop risk — not “+4 ATR per pyramid lot.”

| Field | Default | Meaning |
|-------|---------|---------|
| `thesis_win_atr` | **4.0** | Full-trend opportunity on the **seed (L1)** lot only |
| `thesis_loss_atr` | **actual stop distance in ATR**, else **1.0** | Risk side of expectancy |
| `prior_win_rate` | **0.30** | Used for expectancy when closed-lot sample &lt; `min_win_rate_sample` |
| `min_win_rate_sample` | **20** | Below this, do not trust empirical \(p\) |

### Per-lot MER

| Lot role | MER opportunity (primary) | MER expectancy (secondary) |
|----------|---------------------------|----------------------------|
| **L1** (pyramid_level ≤ 1) | **+4.0 ATR** | \(p \cdot 4 + (1-p)\cdot(-s)\) |
| **Pyramid add** (level ≥ 2) | **0.0 ATR** | \(p \cdot 0 + (1-p)\cdot(-s) = -(1-p)\,s\) |

Scale-ins are the **same** trend thesis, not new +4 ATR markets. Primary stack MER for a 4-lot pyramid is therefore **~4 ATR**, not 16.

### Primary vs secondary comparison

| Metric | Use |
|--------|-----|
| **MER stack (primary)** | \(\sum\) lot opportunity MER → usually **4** for any multi-lot engagement |
| **MER expectancy stack** | \(\sum\) lot expectancy — honesty about win rate + stop |
| **ARR − MER** | `arr_stack − mer_stack` (primary opportunity) |

Win rate \(p\): empirical from closed-lot $ PnL when \(n \ge 20\); else prior **0.30**.

---

## Engagement grouping edge cases (locked)

Key: same `market_base` + `direction`.

| Case | Rule |
|------|------|
| Pyramid while book open | `entry_date < max_exit` of current eng → **same** engagement |
| Full flat then re-entry later | `entry_date > max_exit` → **new** engagement |
| Same-day re-entry after flat | `entry_date == max_exit` → **new** engagement (EOD: flat then re-enter is a new book) |
| Shared stop (all exit same day) | One engagement; all lots share max exit |
| Partial early exit, later add | Join if still open (`entry < max_exit` of remaining path) |
| Long then short | **Different** engagements (direction in key) |
| Missing `exit_date` | Treat exit = entry for span only |
| Missing `entry_date` | **Singleton** engagement (do not merge on garbage dates) |
| Orphan pyramid (no L1) | Still group by overlap; MER opportunity all 0 if no L1 |

Sort within market+direction: `entry_date`, then `pyramid_level`, then `entry_price`.

---

## Non-goals (still)

- Weighting ARR by OWD risk %  
- Remaining-trend MER decay by price path (optional later)  
- Feeding MER into live Kelly without a labeled experiment arm  
