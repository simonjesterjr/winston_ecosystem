# Risk scale meta-layer (Kelly · Martingale · Static · Anti-Martingale)

**Date:** 2026-07-31  
**Status:** Implemented in WUT lab (engine + UI seed); product rule locked in **ADR-010**  
**Supersedes product framing of:** peer S/M/K as `risk_evaluation_strategy`  
**Ticket:** `docs/tickets/2026-07-30-kelly-martingale-sizing-portfolio-management.md`  
**ADR:** `docs/adr/ADR-010-risk-scale-meta-layer.md`

---

## Model

| Layer | Field | Values |
|-------|-------|--------|
| Base geometry | `risk_evaluation_strategy` | `static` · `one_way_dynamic` · `one_way_dynamic_close` |
| Meta scale | `risk_scale_policy` | `none` · `anti_martingale` · `martingale` · `kelly` |

```
base_pct = OWD/OWDC/static(level, …)
scaled_pct = RiskScale::Engine.scale_fraction(base_pct)
```

Scale applies to **new** entries/pyramids only (not open lots). Default `none` = current behavior.

---

## Four test policies

| Policy | Behavior |
|--------|----------|
| **none** (Static scale) | No change to base schedule |
| **anti_martingale** | Good evidence → step up; bad → step down |
| **martingale** | Bad evidence → step up; good → step down |
| **kelly** | Multiplier from fractional Kelly on closed-trade window |

### Default knobs (blank config)

**AM / M:** hybrid trigger, calendar 44 trading days, equity ±16% vs period open, multiplicative step 0.10, floor 0.5×, ceiling 2.0×, max |steps| 5.

**Kelly:** half-Kelly (`fractional_kelly: 0.5`), min 20 closes, lookback 40, recompute every_close, same mult floor/ceiling.

**Kelly sizing modes** (`risk_scale_config.kelly_sizing`, 2026-08-03):

| Mode | Behavior |
|------|----------|
| `winston` (default) | `risk% = base × clamp(1+f, floor_mult, ceil_mult)` — preserves OWD ladder shape |
| `classic` | `risk% = clamp(max(0,f), min_rung, max_rung)` — textbook f\* of bankroll; flattens rungs |

Calendar recompute: `kelly_recompute: calendar` + `review_every_trading_days` (e.g. 22/44/66/88). See experiment `kelly_hybrid_price_level_v1`.

---

## Where to configure

### New PBR form
- **Base risk geometry** dropdown (static / OWD / OWDC)
- **Risk scale policy (meta)** dropdown (none / anti_martingale / martingale / kelly)
- Optional advanced scale JSON

Stored on `results_json`:
```json
{
  "risk_scale_policy": "kelly",
  "risk_scale_config": { "fractional_kelly": 0.5, "kelly_min_trades": 20 }
}
```

### Trading Strategy
- Show: **Base risk** + **Risk scale (meta)**
- Edit: scale policy select + optional config JSON → `full_config_json`

### Code
- `app/services/risk_scale/{config,state,engine}.rb`
- `Strategies::Risk::ScaleAwareRiskEvaluation` decorator
- `PortfolioBacktestRunner` init + day/close hooks

### Legacy
If `risk_evaluation_strategy` is `kelly` or `martingale` without `risk_scale_policy`, runner maps to **static base + that scale policy**.

---

## Lab matrix (recommended next)

Freeze OWD ladder A (or static 2%) + Yellow/Blue books:

| Cell | scale policy |
|------|----------------|
| S | none |
| AM | anti_martingale |
| M | martingale |
| K | kelly |

Score return, max DD, Sharpe, final equity; inspect `risk_history[].risk_scale` for step/Kelly mult path.
