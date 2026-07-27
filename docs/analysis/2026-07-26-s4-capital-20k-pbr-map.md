# S4 — 2× initial capital ($20k vs $10k) survivability panel

**Experiment:** `s4_capital_20k_v1`  
**Status:** **6/6 completed** (scored 2026-07-26)  
**Trading Strategy (TS):** #48 BakeoffV1 S4 FastBO5  
**Question:** Does $20k starting capital improve return%, maximum drawdown (max DD), or trade count vs the Phase 2 / bake-off **$10k** path under integer share floors?

## Call (freeze)

| Decision | Value |
|----------|--------|
| Does $20k improve survivability? | **No** — panel medians **worse** |
| Lab / bake-off default capital | **Keep $10,000** |
| Promote $20k as ops paper default for this pack? | **No** |

**Not scale-invariant.** Under `next_bar_open` + cash/ticket reserves, more starting cash changes **which** fills win the queue — not a free 2× unit scale of the same path.

## Theory (pre-run)

Position units = `floor(risk_dollars / stop_distance)` with `risk_dollars = capital_base × ladder_level_%`.  
If sizing were continuous and cash never bound, **percent return and max DD% would be scale-invariant**.

Discrete effects that *could* help $20k: zero-unit floors, one-share coarseness, cash residual, leverage headroom.  
Lot heat (`max_port=12`) is **count-based** — capital does not buy more concurrent names.

## Frozen chassis (candidate $20k cells)

| Knob | Value |
|------|--------|
| Fill | `next_bar_open` |
| Risk | OWD ladder A / base 2% |
| Pyramid ATR | 1.0 |
| Max / symbol | 4 |
| Max portfolio lots | 12 |
| Initial capital | **$20,000** |

## Grid

| Portfolio | Role | $20k PBR | $10k baseline | Baseline note |
|-----------|------|----------|---------------|---------------|
| Blue | Phase 2 winner | **317** | 305 | ladder A, max_sym 4 — **apples** |
| Orange | Phase 2 winner | **318** | 308 | apples |
| Mango | Phase 2 winner | **319** | 311 | apples |
| Green | Phase 2 weak | **320** | 314 | apples |
| Mint | exclusive / transfer | **321** | 246 | bake-off S4; **max_sym 5** (confound) |
| Yellow | exclusive / transfer | **322** | 251 | bake-off S4; **max_sym 5** (confound) |

## Results

### Return% / max DD% / Sharpe / CAGR% / trades

| Portfolio | $20k | $10k | Δret | Δdd | Δcagr | Δtrades |
|-----------|------|------|------|-----|-------|---------|
| Blue | **−5.5 / 65.8 / 0.19 / −0.9 / 214** | **203.8 / 53.4 / 0.72 / 20.7 / 203** | **−209** | **+12** | **−22** | +11 |
| Orange | −4.8 / 45.9 / 0.17 / −0.9 / 216 | 36.8 / 32.2 / 0.35 / 6.2 / 111 | −42 | +14 | −7 | **+105** |
| Mango | **224.3 / 39.9 / 0.75 / 21.8 / 226** | 181.8 / 37.6 / 0.69 / 19.0 / 161 | **+43** | +2 | +3 | +65 |
| Green | −32.9 / 77.7 / 0.20 / −8.6 / 234 | −1.9 / 87.6 / 0.35 / −0.4 / 175 | −31 | **−10** | −8 | +59 |
| Mint† | **−100.6 / 100.4 / −0.19 / — / 281** | 229.1 / 43.3 / ~0.76 / 19.4 / 423 | **−330** | **+57** | — | −142 |
| Yellow† | 11.7 / 57.5 / 0.21 / 1.6 / 284 | 166.2 / 56.8 / ~0.55 / 14.7 / 319 | −155 | +1 | −13 | −35 |

† Mint/Yellow $10k baselines are bake-off chassis (max_sym **5** vs candidate **4**) — directionally severe, but not pure capital isolation.

### Medians

| Set | Med ret% | Med max DD% | Med Sharpe | Med CAGR% | Positive books |
|-----|----------|-------------|------------|-----------|----------------|
| **$20k (n=6)** | **−5.1** | **61.7** | **0.19** | **−0.9** | **2/6** (Mango, Yellow) |
| Paired Δ vs $10k | **−98** | **+7.4** | — | **−8.2** | — |

### Path evidence (not a scoring glitch)

| Check | Finding |
|-------|---------|
| Chassis stamps (Blue–Green) | Same ladder A, max_port 12, max_sym 4, pyr 1.0, next_bar_open — **only capital differs** |
| Equity curve SHA | Distinct $20k vs $10k on every book |
| Trade counts | Material change (Orange +105 trades; Mint −142) → **different fill sets** |
| Unit sizes | Mean units up ~1.5–2×, but **not** a scaled clone of the $10k series |

## Interpretation

1. **More cash ≠ better survivability** for this S4 pack under next-bar-open.  
2. Extra cash lets larger notionals / more tickets clear the T+1 queue → **different path selection** (same class of effect as max_port heat).  
3. Only **Mango** improved return/CAGR modestly; **Blue** hero path collapsed; **Mint** wiped (with max_sym confound).  
4. Green’s max DD improved slightly but return worsened — not a survivability win.

**Ops implication:** Do not “top up” lab capital to $20k hoping for cleaner $10k economics. Paper/lab comparison capital for this recipe stays **$10k** unless a dedicated capital-ladder study is designed (e.g. $10k / $25k / $50k with fixed random seed / same ticket order — not free-form cash scale).

## Operator commands

```bash
bin/compose exec -T winston_unit_test bin/rails runner lib/scripts/s4_capital_20k_scorecard.rb
```
