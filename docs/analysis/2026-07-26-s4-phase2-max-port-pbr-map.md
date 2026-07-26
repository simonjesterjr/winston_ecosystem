# S4 Phase 2 step 3 — max portfolio lots (heat) PBR map

**Experiment:** `s4_phase2_max_port_v1`  
**Ticket:** `2026-07-25-strategy-bakeoff-v1-phase1`  
**Trading Strategy (TS):** #48 BakeoffV1 S4 FastBO5  
**Status:** **12/12 completed** (scored 2026-07-26)

## Freeze (from steps 1–2)

| Knob | Value |
|------|--------|
| Fill | `next_bar_open` |
| Risk | One-Way Dynamic (OWD) ladder A / base 2% |
| Pyramid Average True Range (ATR) mult | **1.0** |
| Max per symbol / max pyramid | **4** |

## Vary

| Knob | Levels |
|------|--------|
| `max_positions_per_portfolio` (open lots heat) | **8 · 12 · 16** |

## Grid — PBRs 293–304

| Portfolio | max_port **8** | **12** | **16** | Step2 @12 max_sym4 |
|-----------|----------------|--------|--------|---------------------|
| Blue | 293 | 294 | 295 | 282 |
| Orange | 296 | 297 | 298 | 285 |
| Mango | 299 | 300 | 301 | 288 |
| Green | 302 | 303 | 304 | 291 |

## Results (return% / max drawdown% / Sharpe / trades)

| Portfolio | max **8** | max **12** | max **16** |
|-----------|-----------|------------|------------|
| Blue | −39 / **80** / 0.06 / 167 | **204 / 53 / 0.72 / 203** | 81 / 42 / 0.47 / 211 |
| Orange | −33 / **103** / 0.36 / 94 | 37 / **32** / 0.35 / 111 | **123 / 61 / 0.57 / 256** |
| Mango | 38 / 42 / 0.35 / 84 | **182 / 38 / 0.69 / 161** | 93 / 62 / 0.47 / 278 |
| Green | −9 / 56 / 0.12 / 107 | **−2 / 88 / 0.35 / 175** | −11 / **100** / −0.44 / 216 |

### Medians across 4 portfolios

| max_port | Med return% | Med max DD% | Med Sharpe | Positive books |
|----------|-------------|-------------|------------|----------------|
| **8** | **−21** | **68** | 0.24 | 1/4 |
| **12** | **109** | **46** | **0.52** | 3/4 |
| **16** | 87 | 62 | 0.47 | 3/4 |

### Path / capacity notes (not noise)

All three heat levels produce **distinct** paths (no accidental identical runs).

| Observation | Meaning |
|-------------|---------|
| **max 8** loses on Blue, Orange, Mango medians | Too tight: many `portfolio_limit` passes; under-deployed |
| **max 12** best **panel medians** | Best robust default for this four-book lab |
| **max 16** helps **Orange** a lot | More concurrent lots → Orange +123% but DD 61% |
| **max 16** **hurts Blue & Mango** vs 12 | Extra capacity changes **which** tickets fill under next-bar queue — not free alpha |
| **Green** stays weak everywhere | Heat does not fix a bad book/recipe fit |
| Final open lots often **&lt; cap** at 16 (e.g. Blue open=10, Mango open=8) | Cap is an upper bound on path, not “always run at N lots” |

`expired_unfilled` dominates passed counts under next-bar-open — heat interacts with **T+1 path selection**, which is why results are **non-monotonic and portfolio-specific**.

## Why it feels inconclusive (and what still freezes)

You are right that this is **not** a clean “higher heat = higher Compound Annual Growth Rate (CAGR)” story.

| Question | Answer |
|----------|--------|
| Is there a universal best heat for every book? | **No** — Orange “wants” 16; Blue/Mango “want” 12; Green wants a different recipe |
| Is max 8 defensible for S4 on this panel? | **No** — median return negative; Blue/Orange survivability bad |
| Is max 16 a free upgrade? | **No** — ruins Blue/Mango edge vs 12 |
| Is max 12 a robust freeze? | **Yes, as default** — best med return, DD, Sharpe; matches step2 baseline |

**Product freeze:** keep **`max_positions_per_portfolio = 12`** for S4 lab defaults on multi-book color portfolios of this size.  
Do **not** promote 16 from Orange alone. Do **not** tighten to 8.

Per-portfolio overrides later (e.g. Orange paper at 16) are optional ops policy, not Phase 2 science winners.

## Score command

```bash
bin/compose exec -T winston_unit_test bin/rails runner lib/scripts/s4_phase2_max_port_scorecard.rb
```

## S4 tactics freeze (Phase 2 complete enough to pause)

| Knob | Freeze |
|------|--------|
| Pyramid ATR mult | **1.0** |
| Max per symbol / pyramid | **4** |
| Max portfolio lots | **12** |
| Fill | `next_bar_open` |
| Risk ladder | A / 2% (not swept; optional 3b) |

## Next (pick deliberately)

1. **Stop tactics** — promote S4 @ 1.0 / 4 / 12 as working next-open recipe; move to hybrid fill code or ops transfer.  
2. **Step 3b** — milder OWD ladder at frozen heat (expect return/DD tradeoff, not a heat redo).  
3. **Hybrid fill** — entry next-bar / pyramid same-day close (architecture ticket; needs code).  
4. **True multi-level heat** (correlation units) — heat ticket; flat lot cap is what we just measured and it is path-noisy.
