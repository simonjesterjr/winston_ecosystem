# Ticket: Kelly evaluation matrix under Hybrid · pyramid price-level

**Status:** Done — Phase 1 + Phase 2 Yellow scorecard complete (2026-08-09)  
**Priority:** P2  
**Date:** 2026-08-03 (closed 2026-08-09)  
**Scope:** Winston Unit Test (WUT) lab only  
**Experiment key:** `kelly_hybrid_price_level_v1`  
**Map:** `docs/analysis/2026-08-03-kelly-hybrid-price-level-pbr-map.md`

---

## Goal

Evaluate **three families** of Kelly bet sizing on **Mint / Mango / Yellow** under a **fixed honest fill**:

| Family | What it tests |
|--------|----------------|
| **Classic Kelly** | Risk budget = clamp(fractional × f\*) of equity (textbook bankroll fraction) |
| **Winston Kelly + calendar** | Existing mult form `base_rung × (1+f)` recomputed every **22 / 44 / 66 / 88** trading days |
| **Param shifts** | Fractional Kelly, lookback, mult caps (Phase 2, Yellow first) |

Always:

- **Fill:** `hybrid_entry_next_pyramid_price_level` (entry next-bar open · pyramid price-level touch)
- **DNA freeze:** S4 FastBO5 (Trading Strategy #48), One-Way Dynamic (OWD) ladder A, 2% base, max symbol 4, max portfolio 12, pyramid Average True Range (ATR) 1.0, $10k, leverage 3

---

## Edge estimate (all Kelly arms)

Same proxy for f\*:

- **p** = win rate of closed trades (PnL > 0)
- **b** = avg win $ / avg loss $
- **f\*** = p − (1−p)/b  
- **fractional** default **0.5** (half-Kelly)
- Lookback default **40** closes; min **20** before adapting

No signal-strength or vol-target Kelly in this matrix (those remain ticket follow-ons K1/K2).

---

## Classic vs Winston (code)

| Mode | `risk_scale_config.kelly_sizing` | Sizing |
|------|----------------------------------|--------|
| Winston (default) | `winston` | `risk% = base_rung% × clamp(1+f, floor_mult, ceil_mult)` — keeps OWD ladder shape |
| Classic | `classic` | `risk% = clamp(max(0,f), min_rung, max_rung)` — **flattens** OWD rungs to a single f\* budget |

Recompute:

| Arm | `kelly_recompute` |
|-----|-------------------|
| Classic Phase 1 | `every_close` |
| Winston WK22…88 | `calendar` + `review_every_trading_days` ∈ {22,44,66,88} |

---

## Matrix size

### Phase 1 — 18 cells (default setup)

3 books × {`ctrl`, `classic`, `wk22`, `wk44`, `wk66`, `wk88`}

### Phase 2 — Yellow flat-edge band (`PHASE=2`)

**Hypothesis:** do not de-risk when |full_kelly| < ε (closed-sample edge is noise / sub-Kelly).

| Cell | ε | Base |
|------|---|------|
| wk44_flat_eps02 / 05 / 10 | 0.02 / 0.05 / 0.10 | Winston calendar 44 |
| wk22_flat_eps05 | 0.05 | Winston calendar 22 |
| classic_flat_eps05 | 0.05 | Classic every_close |

Code: `risk_scale_config.kelly_flat_edge_eps` — when |full f\*| < ε → mult 1.0 / classic uses base OWD.

### Phase params — +8 on Yellow (`PHASE=params`)

Sparse param pack at WK44 + classic variants (quarter/full fractional, lookback 20/80, wide mult, classic calendar 44).

---

## Commands

```bash
# Phase 1 create pending PBRs
bin/compose exec -T winston_unit_test bin/rails runner lib/scripts/kelly_hybrid_matrix_setup.rb

# Optional Phase 2 (Yellow params)
bin/compose exec -T winston_unit_test bin/rails runner lib/scripts/kelly_hybrid_matrix_setup.rb
# with PHASE=2

# Score
bin/compose exec -T winston_unit_test bin/rails runner lib/scripts/kelly_hybrid_matrix_scorecard.rb
```

Enqueue / run pending Portfolio Backtest Runs (PBRs) via WUT UI or Sidekiq after setup.

---

## Scorecard metrics

Per cell: total return %, max drawdown %, practical Sharpe, trade count, final equity.  
Primary comparisons: each Kelly arm vs **ctrl** on the same book; Winston calendar cadence ranking; classic vs Winston.

---

## Notes / risks

1. Prior hybrid price-level panel (`hybrid_fill_price_level_v1`) was **path-destructive vs pure next_bar** on S4 — absolute returns will look worse than next_bar doctrine. This matrix ranks **sizing policies under that fill**, not re-litigating fill choice.
2. Classic Kelly can size **above** OWD later rungs when f\* is large (capped at `max_rung_pct` default 8%).
3. Fingerprint: any promotion candidate must mint a new Trading Strategy — never mutate engaged ops.

---

## Acceptance

- [x] Classic Kelly mode in `RiskScale::Engine` (`kelly_sizing: classic`)
- [x] Calendar recompute already supported; matrix stamps 22/44/66/88
- [x] Setup + scorecard scripts
- [ ] Phase 1 PBRs completed and scored
- [ ] Recommendation filed on map (keep ctrl / adopt classic / adopt Winston@N / reject)
