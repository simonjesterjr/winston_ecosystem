# ADR-010: Risk Scale Meta-Layer (orthogonal to base risk geometry)

**Status:** Accepted  
**Date:** 2026-08-09  
**Deciders:** Operator + lab (risk-scale matrix 2026-07-31; Kelly hybrid campaign 2026-08-03)  
**Builds on:** ADR-006 (lineage), ADR-008 (confirm ⊥ OWD ladder)  
**Evidence:**  
- `docs/analysis/2026-07-31-risk-scale-meta-layer.md`  
- `docs/analysis/2026-07-30-sizing-kelly-martingale-pbr-map.md`  
- `docs/session-reports/2026-07-31-1556-risk-scale-matrix-findings.md`  
**Tickets:** `2026-07-30-kelly-martingale-sizing-portfolio-management.md`, `2026-07-31-adr-risk-scale-orthogonality.md`, `2026-07-31-kelly-scale-not-global-default.md`

---

## Context

Winston sizes positions with **base risk geometry** (static percentage or One-Way Dynamic (OWD) / One-Way Dynamic Close (OWDC) ladders) plus portfolio/market heat caps. Lab work introduced a second money-management axis: **risk scale policies** (none, anti-martingale, martingale, Kelly) that multiply or replace the base risk fraction from closed-trade and equity-curve evidence.

Two naming collisions needed a hard product lock:

1. ADR-008 “risk scale into trends” means the **OWD pyramid ladder** (geometry).  
2. `risk_scale_policy` means the **meta money-management overlay** (Kelly / AM / M / none).

Peer packaging of Kelly or Martingale as sole `risk_evaluation_strategy` is deprecated: geometry and meta must remain separable so OWD + Kelly can coexist without inventing ladder×Kelly hybrids as new base classes.

## Decision

### A. Two orthogonal fields

| Layer | Field | Values (canonical) |
|-------|-------|--------------------|
| **Base geometry** | `risk_evaluation_strategy` | `static` · `one_way_dynamic` · `one_way_dynamic_close` (lab) |
| **Meta scale** | `risk_scale_policy` | `none` · `anti_martingale` · `martingale` · `kelly` |

```
base_pct  = static | OWD/OWDC ladder[level, direction]
scaled_pct = RiskScale::Engine.scale_fraction(base_pct)   # identity when policy = none
```

Optional knobs live in `risk_scale_config` (fractional Kelly, lookback, calendar recompute, floor/ceiling mult, `kelly_sizing` winston|classic, etc.). Blank config ⇒ safe class defaults.

### B. Fingerprint vs runtime state

1. **Methodology identity (fingerprint)** includes `risk_scale_policy` and `risk_scale_config` when policy is not `none` (same rule as OWD ladder under ADR-008).  
2. **Path state** — `n_steps`, `kelly_multiplier`, `kelly_risk_fraction`, streaks, last review date, diagnostics — is **runtime only**. It is not part of fingerprint and may update freely on an Operational Portfolio (OP) without succession.  
3. Changing policy or config on an **Engaged** OP requires successor rebalance (ADR-006), not silent import mutation.

### C. Defaults and promotion doctrine

1. Default `risk_scale_policy` is **`none`** — current static/OWD behavior.  
2. **Kelly is not a global trade-ready default.** Promote only with host-specific multi-panel evidence; path dependence is large (static rescue vs OWDC regression on Yellow matrix).  
3. **Martingale scale policy is research / paper only** for real capital — ruin-class drawdowns observed (Yellow S/M/K panel).  
4. Legacy PBR/TS rows with peer `risk_evaluation_strategy` ∈ {`kelly`,`martingale`} map to **static base + that scale policy** at run time (WUT runner already does this).

### D. Handoff and ops

1. Trade-Ready / Observation portfolio JSON **must** carry `risk_scale_policy` and `risk_scale_config` at top level and under nested `trading_strategy` when policy ≠ `none` (and may emit `none` explicitly for clarity).  
2. Wv2 import **must not drop** these fields — store on `TradingStrategy.parameters` (and any OP runtime state store separately).  
3. Wv2 Daily Analysis / PositionSizer apply the same `base × scale` math as WUT for task and journal draft quantities.  
4. Until min history / first calendar review, Kelly mult stays **1.0×** (static-safe).

### E. Terminology

| Prefer | Avoid |
|--------|--------|
| **OWD ladder** / base geometry | Calling the ladder “risk_scale_policy” |
| **Risk scale policy** / meta layer / Kelly scale | Calling Kelly a `risk_evaluation_strategy` in new recipes |
| **Winston Kelly** (`kelly_sizing: winston`) | Assuming textbook f\* always flattens rungs |
| **Classic Kelly** (`kelly_sizing: classic`) | Using classic as silent default |

## Consequences

- Lab forms and Trading Strategy (TS) UI show **two** controls: base risk + meta scale.  
- Fingerprint capture and portfolio export include scale when active.  
- Wv2 must port `RiskScale::{Config,State,Engine}` (or equivalent) — majestic monoliths, not a shared gem in this ADR.  
- Operator-facing DAR / tasks should surface current mult when policy ≠ none (transparency).  
- Promotion of Kelly recipes remains evidence-gated (WS6 lab scorecard), independent of plumbing.

## Rejected

- Replacing OWD ladders with classic Kelly as the only sizing model.  
- Shipping Martingale as real-capital default.  
- Embedding live `kelly_multiplier` in fingerprint (would churn identity every review).  
- Joint re-grid of entry × exit × ladder × Kelly on full sample in one pass (anti-overfit).

## Related

- ADR-008 (confirmational entry ⊥ OWD ladder — different “scale”)  
- ADR-006 (OP lineage / Engaged immutability)  
- Analysis: `docs/analysis/2026-07-31-risk-scale-meta-layer.md`  
- Handoff: `docs/business-context/wut-to-wv2-handoff.md`  
- Gap plan: Kelly / risk scale → Wv2 portfolio management (2026-08-09)
