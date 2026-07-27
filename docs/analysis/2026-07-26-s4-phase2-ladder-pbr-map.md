# S4 Phase 2 step 3b — One-Way Dynamic (OWD) ladder mildness PBR map

**Experiment:** `s4_phase2_ladder_v1`  
**Ticket:** `2026-07-26-s4-phase2-ladder-mildness`  
**Trading Strategy (TS):** #48 BakeoffV1 S4 FastBO5  
**Status:** **12/12 completed** (scored 2026-07-26)

## Freeze (from steps 1–3)

| Knob | Value |
|------|--------|
| Fill | `next_bar_open` |
| Pyramid Average True Range (ATR) mult | **1.0** |
| Max per symbol / max pyramid | **4** |
| Max portfolio lots | **12** |
| Stop | `move_to_last_entry` |
| ATR mult (stop distance) | 2.0 |

## Vary — ladder packs

| Pack | Long ladder | Short ladder | Base `risk_percentage` |
|------|-------------|--------------|------------------------|
| **A** (control) | 2 / 3 / 4 / 6 / 6 | 2 / 2 / 2 / 3 / 3 | 2% |
| **B** moderate | 2 / 2 / 3 / 3 / 4 | 2 / 2 / 2 / 2 / 3 | 2% |
| **C** flat | 2% × 5 | 2% × 5 | 2% |
| **D** (optional, not run) | 1 / 1.5 / 2 / 3 / 3 | 1 / 1 / 1 / 1.5 / 1.5 | 1% |

## Grid — PBRs 305–316

| Portfolio | Pack **A** | **B** | **C** | Step3 max_port=12 (prior A) |
|-----------|------------|-------|-------|------------------------------|
| Blue | 305 | 306 | 307 | 294 |
| Orange | 308 | 309 | 310 | 297 |
| Mango | 311 | 312 | 313 | 300 |
| Green | 314 | 315 | 316 | 303 |

## Results (return% / max DD% / Sharpe / CAGR% / Calmar / trades)

| Portfolio | Pack **A** | **B** | **C** |
|-----------|------------|-------|-------|
| Blue | **204 / 53 / 0.72 / 20.7 / 0.39 / 203** | **identical** | **identical** |
| Orange | **37 / 32 / 0.35 / 6.2 / 0.19 / 111** | **identical** | **identical** |
| Mango | **182 / 38 / 0.69 / 19.0 / 0.50 / 161** | **identical** | **identical** |
| Green | **−2 / 88 / 0.35 / −0.4 / 0.00 / 175** | **identical** | **identical** |

### Medians across 4 portfolios

| Pack | Med return% | Med max DD% | Med Sharpe | Med CAGR% | Med Calmar | Positive books |
|------|-------------|-------------|------------|-----------|------------|----------------|
| **A** | **109.3** | **45.5** | **0.52** | **12.6** | **0.29** | 3/4 |
| **B** | **109.3** | **45.5** | **0.52** | **12.6** | **0.29** | 3/4 |
| **C** | **109.3** | **45.5** | **0.52** | **12.6** | **0.29** | 3/4 |

### Path identity (not a scoring glitch)

| Check | Result |
|-------|--------|
| Pack A vs step3 max_port=12 (294/297/300/303) | **Δret=0, Δdd=0** on all four books |
| Packs A vs B vs C equity curve SHA (Blue, Orange) | **identical** within portfolio |
| Position unit series SHA (Blue 305/306/307) | **identical** (203 fills, same units) |
| Stamped ladders in `results_json` | **Differ correctly** (A 2/3/4/6 vs B 2/2/3/3/4 vs C flat 2%) |

**Interpretation:** Under frozen heat (`max_port=12`, next-bar-open queue), capacity is spent on **breadth** (many names, mostly first lots) not **depth** (pyramid rungs 2–5). All three packs share **level-1 risk = 2%**. Higher OWD rungs barely (or never) change sizing, so ladder *shape* is a **null lever** here — same class of finding as Elephant `half_ladder` ≡ `flat_1pct` (level-1 unit risk dominates).

Milder mid-ladder shape will **not** reduce maximum drawdown or Compound Annual Growth Rate (CAGR) on this chassis. To change risk economics at frozen heat, change **level-1 / base** risk (e.g. optional pack D @1%), not packs B/C.

## Product freeze

| Decision | Value |
|----------|--------|
| Ladder pack | **Keep A** (long 2/3/4/6 · short 2/2/2/3/3 · base 2%) |
| Packs B / C | **No adopt** — identical paths; no DD/CAGR benefit |
| Pack D | **Not run** — would test unit risk, not ladder mildness; only if operator wants a 1% sleeve |

**S4 working pack (unchanged):** next_bar_open · OWD ladder **A** / 2% · pyr ATR **1.0** · max_sym **4** · max_port **12** · TS #48

## Operator commands

```bash
bin/compose exec -T winston_unit_test bin/rails runner lib/scripts/s4_phase2_ladder_scorecard.rb
# optional dump:
bin/compose exec -T winston_unit_test bin/rails runner lib/scripts/s4_phase2_ladder_scorecard.rb WRITE=1
```
