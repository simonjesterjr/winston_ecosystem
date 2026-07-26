# S4 Phase 2 step 2 — max per symbol PBR map

**Experiment:** `s4_phase2_max_symbol_v1`  
**Ticket:** `2026-07-25-strategy-bakeoff-v1-phase1`  
**Trading Strategy (TS):** #48 BakeoffV1 S4 FastBO5  
**Freeze:** `next_bar_open` · One-Way Dynamic (OWD) ladder A · base 2% · max_port 12 · **pyramid Average True Range (ATR) mult = 1.0** (step 1)  
**Vary:** `max_positions_per_symbol` / `max_pyramid` ∈ {3, 4, 5}  
**Status:** **12/12 completed** (scored 2026-07-26)

## Grid — PBRs 281–292

| Portfolio | max_sym **3** | **4** | **5** | Bakeoff @5 |
|-----------|---------------|-------|-------|------------|
| Blue | 281 | 282 | 283 | 201 |
| Orange | 284 | 285 | 286 | 206 |
| Mango | 287 | 288 | 289 | 221 |
| Green | 290 | 291 | 292 | 216 |

## Results (return% / max drawdown% / Sharpe / trades)

| Portfolio | max **3** | max **4** | max **5** | Bakeoff @5 |
|-----------|-----------|-----------|-----------|------------|
| Blue | 76.6 / **79.9** / 0.44 / 201 | **203.8 / 53.4 / 0.72 / 203** | 186.6 / 53.4 / 0.69 / 222 | 186.6 / 53.4 |
| Orange | 36.8 / 32.2 / 0.35 / 111 | 36.8 / 32.2 / 0.35 / 111 | 36.8 / 32.2 / 0.35 / 111 | 36.8 / 32.2 |
| Mango | 48.7 / 37.6 / 0.37 / 152 | 181.8 / 37.6 / 0.69 / 161 | **186.3 / 37.6 / 0.69 / 188** | 186.3 / 37.6 |
| Green | −1.9 / 87.6 / 0.35 / 175 | −1.9 / 87.6 / 0.35 / 175 | −1.9 / 87.6 / 0.35 / 175 | −1.9 / 87.6 |

### Medians across 4 portfolios

| max_sym | Med return% | Med max DD% | Med Sharpe | Positive books |
|---------|-------------|-------------|------------|----------------|
| **3** | 42.8 | **58.7** | 0.36 | 3/4 |
| **4** | 109.3 | **45.5** | **0.52** | 3/4 |
| **5** | **111.6** | **45.5** | **0.52** | 3/4 |

### Notes

- **max_sym 5 ≡ bakeoff** on all four books (reproducibility OK).
- **Orange & Green:** 3/4/5 **identical** — path never used more than 3 lots per name (cap non-binding).
- **Blue:** max **3** is bad (return down, drawdown ~80%). Max **4** **beats** max 5 on return and Sharpe with **same** max drawdown (~53%).
- **Mango:** max 3 taxes return hard (~49% vs ~186%). Max **4 ≈ 5** (182% vs 186%, same drawdown and Sharpe).

## Decision (freeze for step 3)

**Freeze `max_positions_per_symbol` = 4** (and `max_pyramid` = 4) for S4 Phase 2 onward.

| Level | Call |
|-------|------|
| **3** | Reject — Blue drawdown spike; Mango return collapse |
| **4** | **Prefer** — best Blue; Mango nearly full; medians ≈ 5 |
| **5** | Acceptable bakeoff default; slightly higher median return, worse Blue than 4 |

Do not keep max 5 only because bakeoff used it — step 2 evidence favors **4** on the important Blue path.

## Score command

```bash
bin/compose exec -T winston_unit_test bin/rails runner lib/scripts/s4_phase2_max_symbol_scorecard.rb
```

## S4 tactics freeze so far

| Knob | Freeze |
|------|--------|
| Pyramid ATR mult | **1.0** (step 1) |
| Max per symbol / max pyramid | **4** (step 2) |
| Fill | `next_bar_open` |
| Risk | OWD ladder A / 2% base (until step 3) |

## Next

**Phase 2 step 3:** ladder and/or portfolio heat (`max_positions_per_portfolio`) at **pyr ATR 1.0 + max_sym 4**.  
**Hybrid fill** (entry next-bar / pyramid same-day): still blocked on code — see `2026-07-26-hybrid-fill-entry-next-pyramid-same-day.md`.
