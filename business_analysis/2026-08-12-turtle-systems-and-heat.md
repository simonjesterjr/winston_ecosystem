# Turtle systems chassis, heat units, and capital base

**Date:** 2026-08-12  
**Status:** Spec freeze (Phase 0) — lab matrix next  
**Program ticket:** `docs/tickets/2026-08-12-turtle-systems-eval-and-ops-alignment.md`  
**Heat ticket:** `docs/tickets/2026-07-25-ts-portfolio-heat-unit-limits.md`  
**Related:** Faith / Turtle Rules; S4 bake-off (pyr 0.5 rejected for FastBO5 only)

---

## Decisions (frozen for matrix)

### Unit definition

| Term | Definition |
|------|------------|
| **N** | ATR × stop ATR multiplier (chassis: **2.0**) |
| **1 unit** | Position size such that a 1N adverse move ≈ **`unit_risk_fraction` × risk_equity** (chassis: **1%**) |
| **Pyramid add** | Each add is **another full unit** for heat L1–L4 (Faith counting) |
| **Pyramid spacing** | **0.5N** from last fill (`pyramid_atr_multiplier = 0.5`) |
| **Max units / market** | **4** (L1) — map to `max_pyramid` / `max_positions_per_symbol` until heat engine ships |

### Heat table (defaults)

| Level | Scope | Max units |
|-------|--------|-----------|
| L1 | Single market | 4 |
| L2 | Closely correlated markets, same direction | 6 |
| L3 | Loosely correlated markets, same direction | 10 |
| L4 | Single direction (all long **or** all short) | 12 |

Long and short budgets are independent at L4.

**Implication:** Same TS heat config on every book. **Mint-class** (low pairwise \|r\|) rarely hits L2/L3; **Yellow / Orange / Mango** hit sooner. Prefer correlation-driven binding over hardcoding different unit tables per color.

Correlation thresholds (until BA revises): close \|r\| ≥ 0.70; loose \|r\| ≥ 0.40; source PCS pairwise on methodology window.

### Risk equity vs free cash

| Name | Formula | Use |
|------|---------|-----|
| **free_cash** | CashEvents + executed journal flows (`Portfolio#capital_base`) | Funding / margin / “can I pay for this notional?” |
| **risk_equity** | free_cash + long market value − short market value | **Unit sizing** (Turtle account value) |

**Decision:** Size units on **risk_equity**. Report both on DAR. Free cash ≪ risk_equity → over-deployed attention flag, not silent zero units when equity remains.

### System recipes

| Key | Entry | Exit | Skip next after winner | Vol exit | Pyramid |
|-----|-------|------|------------------------|----------|---------|
| **S1** | `Breakout20DayStrategy` | `Breakout10DayStrategy` | off (A1) / **on** (A2) | none | 0.5N |
| **S2** | `Breakout55DayStrategy` | `Breakout20DayStrategy` | off | none | 0.5N |

Chassis shared: static 1% risk, ATR×2 stop, `move_to_last_entry`, max 4/market, max 12 portfolio lots interim, `next_bar_open`, `ignore_first_signal: true`, `always_in_market: false`, **no** `VolatilityExitStrategy`.

**Skip rule (S1 A2):** After a market goes **flat** and **round-trip realized P&L > 0** (sum of all lots in that trade), ignore the **next** entry signal in **either** direction for that market only; then clear the skip.

### Portfolio panel for matrix

| Tier | Portfolios |
|------|------------|
| **strong_prior** | **Blue**, **Mango** (required every cell; window-fit table) |
| exclusive | Mint, Yellow |
| core_cluster | Orange, Red, Green, Rust |
| optional_stress | White, Pink, Gray (consistency only) |

Hypothesis: short window (S1) vs long window (S2) may re-rank Blue/Mango relative to S4 FastBO5.

### Explicit non-promotions

- Do **not** change S4 FastBO5 default pyramid to 0.5N from this freeze alone (prior Phase 2 evidence: median DD ~82% on FastBO5).
- OWD ladder / Kelly meta-layer stay **orthogonal**; Turtle baseline uses **static** unit risk.

---

## Open until heat engine ships

1. Correlation vintage — **locked for v1 (Phase 2):** freeze pairwise \|ρ\| to the **methodology window** on the PBR correlation snapshot (attach at start/complete). Do **not** recompute every bar. **Pairwise \|ρ\|** is authoritative for L2/L3 membership; the PCS 0–100 score is not. Close ≥ 0.70; loose ≥ 0.40. Missing matrix → unknown pair (do not invent); optional sector map fills unknown pairs only.
2. Wv2 desk hard-gate on heat — **Phase 4 landed:** DA enter/pyramid drafts that breach L1–L4 become PassedSignals (`heat_market` / `heat_close_corr` / `heat_loose_corr` / `heat_direction`). Exits are not heat-gated. L2/L3 need pairwise (`parameters.heat_pairs`); without a matrix only L1/L4 bind.

---

## Scorecard requirements

1. Panel medians on required tiers (exclude optional stress).
2. **Window fit table:** per portfolio best S1 (A1/A2) vs S2 (B1) — return, max DD, trades — **always include Blue and Mango**.
3. Skip A1 vs A2 trade-count and return delta on S1 only.
