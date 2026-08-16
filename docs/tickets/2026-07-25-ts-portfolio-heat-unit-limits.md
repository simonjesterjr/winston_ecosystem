# Ticket: TS creation — multi-level portfolio heat (Turtle unit limits + correlations)

**Status:** Done — Phases 0–4 landed 2026-08-14  
**Priority:** P1 (elevated with Turtle program)  
**Date:** 2026-07-25 (updated 2026-07-26 after S4 Phase 2 heat sweep; Phase 0 BA 2026-08-12)  
**Monoliths:** winston_unit_test (lab PBR + TS capture); winston_v2 (ops capacity later)  
**Related:** PCS / correlation work (`ecosystem/docs/tickets/archive/2026-07-12-wut-portfolio-correlation-dashboard.md`, portfolio cohorts, `max_markets_per_portfolio`); OWD ladder / TS capture (2026-07-25 session); scale-in ATR blocks ADR `2026-07-25-pyramid-scale-in-price-blocks.md`; bake-off session `2026-07-26-1103-strategy-bakeoff-phase2.md`; map `2026-07-26-s4-phase2-max-port-pbr-map.md`; program `2026-08-12-turtle-systems-eval-and-ops-alignment.md`; BA `ecosystem/business_analysis/2026-08-12-turtle-systems-and-heat.md`

---

## Lab evidence (2026-07-26) — flat lot heat is not enough

Phase 2 step 3 swept **max_positions_per_portfolio ∈ {8, 12, 16}** on S4 FastBO5 with pyr ATR 1.0 and max_sym 4 under `next_bar_open`:

| max_port | Panel median return | Median max DD | Notes |
|----------|---------------------|---------------|--------|
| 8 | **−21%** | 68% | Too tight |
| **12** | **+109%** | **46%** | Best robust default |
| 16 | +87% | 62% | Orange wins; **Blue/Mango lose** vs 12 |

**Insight:** Flat lot caps under next-bar-open are **path selection**, not a free CAGR dial — non-monotonic and portfolio-specific. Default freeze **12** for S4 multi-book lab. This **increases** the value of true multi-level / correlation **unit** heat (this ticket), rather than more integer lot sweeps.

S4 interim freezes while heat BA proceeds: pyr ATR **1.0**, max_sym **4**, max_port **12**, OWD ladder A / 2%.

---

## Problem

Today Winston’s portfolio risk “heat” is mostly a **single flat cap**:

| Current control | Typical value | What it measures |
|-----------------|---------------|------------------|
| `max_positions_per_portfolio` | 10–12 | **Open lots** (all markets, all directions) |
| `max_positions_per_symbol` / `max_pyramid` | 5 | Lots **per market** (includes pyramids) |
| `max_markets_per_portfolio` | 4 | Distinct markets with open risk |
| OWD ladder | R1 % of equity per lot | Risk **per add**, not portfolio heat |

That last line of defense (“all directions, all markets ≤ N lots”) is a crude stand-in for classic Turtle **portfolio heat**. It does **not** encode:

1. **Unit-normalized risk** (1 unit ≈ 1N adverse move ≈ fixed % equity) across lots  
2. **Correlated market clusters** (tight vs loose) in the same direction  
3. **Directional bias** (all longs vs all shorts as separate budgets)  
4. **TS identity** — heat rules should live on the Trading Strategy (methodology), not only as ad-hoc PBR columns

We now have **correlation / PCS** infrastructure and better TS capture (ladder, OWDC, scale-in). Heat should be revisited with that work, not reinvented as another opaque integer.

---

## Turtle baseline (reference, not dogma)

Units = risk-normalized building blocks (1 unit sized so 1N adverse ≈ ~1% equity in classic presentation). Caps (Faith et al.):

| Level | Type | Max units |
|-------|------|-----------|
| 1 | Single market | **4** |
| 2 | Closely correlated markets (same direction) | **6** |
| 3 | Loosely correlated markets (same direction) | **10** |
| 4 | Single direction (all longs **or** all shorts portfolio-wide) | **12** |

Longs and shorts can each approach L4 independently (e.g. up to 12 long units **and** 12 short units). Extra valid signals are **passed** when a cap binds — same spirit as lab `expired_unfilled` / capacity passes.

Winston defaults today: often **5** per market and **10–12** total lots — similar spirit at L1/L4, but **lot count ≠ unit count**, and **L2/L3 are missing**.

---

## Desired outcome

### A. TS contract (creation / export / fingerprint)

Extend TS `risk` (or sibling `heat`) so creation and export carry explicit multi-level caps, e.g.:

```json
"risk": {
  "percent": 0.02,
  "atr_multiplier": 2,
  "stop_strategy": "move_to_last_entry",
  "pyramiding": {
    "max_positions": 5,
    "atr_multiplier": 1.0,
    "confirming_signal": null
  },
  "heat": {
    "unit_risk_fraction": 0.01,
    "max_units_per_market": 4,
    "max_units_closely_correlated_same_direction": 6,
    "max_units_loosely_correlated_same_direction": 10,
    "max_units_single_direction": 12,
    "correlation": {
      "source": "pcs_or_pairwise",
      "close_threshold": 0.7,
      "loose_threshold": 0.4,
      "window": "methodology_or_portfolio_default"
    }
  }
}
```

- Defaults may mirror Turtle numbers or our current 5 / 12 practice — **decide in BA**, not silently.  
- `null` / omit heat → preserve **legacy** lot caps only (backward compatible).  
- Fingerprint must include heat config when set (methodology identity).

### B. Unit definition (lab + ops alignment)

Define **Winston unit** explicitly, preferably:

- `unit_size` such that stop distance (N = risk ATR mult × ATR) implies risk ≈ `unit_risk_fraction × equity` **or**  
- Map each open lot’s **risk fraction** (OWD ladder % × capital base) into **fractional units** so pyramids count as multiple units honestly.

Do **not** treat “one Position row = one unit” without stating that (our pyramids would overstate L1).

### C. Correlation clusters (reuse good work)

- Prefer existing **PCS / pairwise correlation** artifacts (portfolio correlation dashboard, cohort membership, parquet closes).  
- Define **closely** vs **loosely** correlated groups (threshold + optional static sector map as fallback).  
- Same-direction unit sum within a cluster vs L2/L3 caps.  
- Document when correlation is **frozen** (TS window / signal day / fill day).

### D. Lab enforcement (WUT PBR)

On entry / pyramid fill (including T+1 queue adjudication):

1. Size candidate lot → units (or risk-equivalent units)  
2. Check L1 → L2 → L3 → L4 (and legacy lot/market caps if still enabled)  
3. Fail → **passed** with reason taxonomy (`heat_market`, `heat_close_corr`, `heat_loose_corr`, `heat_direction`, …)  
4. Ranked fill order (ATR/ER) still applies **within** heat-feasible set  

### E. Ops (Wv2) — later phase

- Desk capacity / swap packages already talk markets and ER — heat should eventually gate drafts the same way.  
- Out of scope for first lab slice unless cheap.

### F. TS creation UX

- When creating/promoting a TS (manual or from PBR): **heat section** with Turtle defaults + “legacy lot caps only” mode.  
- OWDC/OWD ladder remains separate (per-lot risk %); heat is **portfolio aggregation** of units.  
- Show ladder + heat on TS show page (same confidence fix as ladder display).

---

## Non-goals (first pass)

- Auto-learning correlation thresholds from production P&L  
- Replacing PCS portfolio construction (heat is **runtime capacity**, not membership search)  
- Atomic reverse / SoS policy (separate ticket)  
- Intraday multi-N scaling beyond existing pyramid ATR step

---

## Work sequence (suggested)

| Phase | Work | Done when |
|-------|------|-----------|
| **0** | BA: unit definition + default heat table (Turtle vs Winston 5/12) | **Done** — `ecosystem/business_analysis/2026-08-12-turtle-systems-and-heat.md` (unit = full Faith unit; heat 4/6/10/12; size on risk_equity) |
| **1** | TS JSON + fingerprint + capture from PBR/TS form | **Done 2026-08-14** — `PortfolioHeatConfig`; export `risk.heat`; capture from PBR `results_json.heat` + TS form; omit = legacy lot caps (fingerprint stable) |
| **2** | Correlation group resolver (reuse PCS/pairwise) | **Done 2026-08-14** — `PortfolioHeatClusterResolver`; pairwise \|ρ\| (not PCS score); vintage = methodology window on PBR snapshot; specs with synthetic matrix |
| **3** | WUT PBR enforce L1–L4 on fill + pass reasons | **Done 2026-08-14** — `HeatCapacityGate` on fill (same-bar + T+1); pass `heat_market` / `heat_close_corr` / `heat_loose_corr` / `heat_direction`; same-signal cell heat on vs off |
| **4** | Optional Wv2 desk gate | **Done 2026-08-14** — `Operations::DeskHeatGate` on DA enter/pyramid drafts; PassedSignal `heat_*` codes match lab; exits not gated |

---

## Acceptance criteria

- [x] Written rule: what counts as **1 unit** under OWD ladder pyramids — Phase 0 BA: full Faith unit; each pyramid add is another full unit  
- [x] TS can store and display multi-level heat (or explicit “legacy only”) — Phase 1  
- [x] Lab rejects / passes adds that would breach L1–L4 when heat enabled — Phase 3  
- [x] Closely/loosely groups derived from correlation infrastructure (documented source + thresholds) — Phase 2: pairwise \|ρ\| ≥ 0.70 close / ≥ 0.40 loose; vintage = methodology window  
- [x] Fingerprint/export include heat when non-default — Phase 1  
- [x] No silent change to existing PBRs without `heat` key (backward compatible)

---

## Open questions

1. **Unit vs lot:** Do we count pyramid adds as separate full units (Turtle) or as ladder risk-fractional units?  
2. **Correlation vintage:** **Phase 2 lock** — methodology window on the PBR snapshot (not signal-day / fill-day recompute).  
3. **Short/long nets:** Can a market’s long and short ever both count (we generally forbid dual direction per market)? Resolver already direction-filters; still no dual-direction per market.  
4. **Default heat:** Turtle 4/6/10/12 vs Winston 5/—/—/12? — **Phase 0:** Turtle 4/6/10/12.  
5. **PCS score vs pairwise |ρ|:** **Phase 2 lock** — pairwise \|ρ\| is authoritative for L2/L3; PCS score is construction/monitoring only.

---

## Links / prior art in repo

- PBR: `max_positions_per_portfolio`, `max_markets_per_portfolio`, position swap by ER  
- Correlation dashboard / PCS snapshots  
- Capacity swap desk packages (Wv2 ticket history)  
- Session 2026-07-25: TS ladder capture, T+1 queue, last-entry pyramid ATR steps  

---

## Notes from operator

> Right now we capture this as the last line … all directions, all markets to total some value (10 or 12). We want to revisit this with all of the good work we have done with correlations.

Ticket captures that intent: **upgrade flat portfolio lot heat → multi-level unit heat informed by correlation clusters**, and make it a first-class part of **TS creation**, not only a PBR integer.
