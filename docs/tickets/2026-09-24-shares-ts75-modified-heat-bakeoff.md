# Ticket: Shares-only TS75 modified-heat bakeoff (caps 3/10)

**Status:** Done — readout 2026-09-24 (no clear heat-knob win)  
**Priority:** P1  
**Date:** 2026-09-24  
**Lane:** B (matrix design + stamp script; Ops stamps — CoS does not enqueue)  
**Owner:** PBR Ops / Sawtooth Ops (stamp); CoS (ticket + readout)  
**Human gates:** Operator go before live stamp; morning Edge_R / heat+caps readout with John before any Wv2 promote  
**DoD:** 8 shares-only TS75 cells completed (not failed / not operator_stopped); Jev harness green; readout names best Edge_R under modified heat+caps, or “no clear winner”

## Goal

Find **good Edge_R under heat + hard caps** on the shares-only (IBKR Level 1) path. Prior overnight bakeoff (#772–#787) was heat-absent (legacy label only) and crowned **TS75** on Edge_R across all four books — that panel is the **heat-absent control**. This panel keeps **TS75 only**, same books and caps, and adds **modified Turtle heat knobs** (heat is knobs, never blank/omitted).

## Heat knob interpretation (Operator correction)

Classic `TURTLE_HEAT` from [`../analysis/2026-09-21-stamp-teal-ts75-heat-on-r01.rb`](../analysis/2026-09-21-stamp-teal-ts75-heat-on-r01.rb):

| Knob | Classic |
|------|---------|
| `max_units_per_market` | 4 |
| `max_units_closely_correlated_same_direction` | 6 |
| `max_units_loosely_correlated_same_direction` | 10 |
| `max_units_single_direction` | 12 |

Operator modified heat **(3, 6, _, 10 max per portfolio)**. I interpret that as:

| Knob | Modified |
|------|----------|
| `max_units_per_market` | **3** |
| `max_units_closely_correlated_same_direction` | **6** |
| `max_units_loosely_correlated_same_direction` | **10** (`_` = no separate mid band; align loose to direction/portfolio max) |
| `max_units_single_direction` | **10** |
| `unit_risk_fraction` | cell risk (0.01 or 0.02) |
| `correlation` | same `pcs_pairwise` block as classic (close 0.7, loose 0.4, window methodology) |

Plus hard lot caps `max_positions_per_symbol=3`, `max_positions_per_portfolio=10`.

**Host check (2026-09-24):** `PortfolioBacktestRun#heat_enabled?` ⇒ `heat_config.present?`; Mode-C / `PortfolioHeatConfig.normalize` expect the full heat hash keys above. Sample heat-ON #765/#766 match that shape. WUT heat capacity gate compares L3/L4 independently — **loose == direction (10/10) is accepted**; no rejector found. If a future WUT build rejects loose==direction, note it and stop — do not invent a different loose without evidence.

## Baseline control

| Panel | PBRs | Heat | Caps | Result |
|-------|------|------|------|--------|
| Shares TS75 vs TS77 | **772–787** | OFF (no heat hash; `heat_mode=legacy`) | 3/10 | TS75 won Edge_R on all 4 books; Teal Return/DD split + #783 TR anomaly ⇒ no clear promote without Operator review — ticket [`2026-09-23-shares-only-ts75-vs-ts77-bakeoff.md`](2026-09-23-shares-only-ts75-vs-ts77-bakeoff.md) |

This panel **adds modified heat knobs** on the TS75 / caps 3/10 / shares DNA.

## Related host fixes (do not restamp)

- WUT **#55** portfolio_limit fix is on host (`0902707` — combined `portfolio_limit` always enforced on RST + heat-ON).
- RangeError fail-closed landed (`a30e228`); ticket [`2026-09-22-wut-teal-heat-on-rangeerror-4byte-int.md`](2026-09-22-wut-teal-heat-on-rangeerror-4byte-int.md) status: **Fixed in code — operator restamp pending**. **Do not restamp Teal LEAP #767–#770** (or Orange #771) in this work.
- This panel is **shares** so LEAP unit overflow is lower risk — still **fail-closed harness**: any `RangeError` / `operator_stop` ⇒ **no promote**.

## DNA table

| Dim | Value |
|-----|-------|
| Instrument | **Shares-only** (`leap_fulfillment` key **omitted**) |
| Strategy | **TS75 only** (20-day entry / 10-day exit) |
| Risk | 1% and 2% (`unit_risk_fraction` matches) |
| Heat | **ON** — full `heat` hash + `heat_mode=turtle` (never blank) |
| Heat knobs | 3 / 6 / 10 / 10 (market / close / loose / direction) |
| Caps | `max_positions_per_symbol=3`, `max_positions_per_portfolio=10` |
| Fill | `resting_stop_touch` / resting arm |
| Stop | `move_to_last_entry`, `atr_multiplier=2` |
| Capital | $30,000 |
| Date range | Per-portfolio natural bar overlap (same windows as #772–#787 within each book) |

### Portfolios

| Seed | Id | Name |
|------|----|------|
| blue | **7** | Portfolio Blue |
| indigo | **411** | Indigo_WUT_evolved |
| teal | **412** | Teal_WUT_evolved |
| copper | **413** | Portfolio Copper |

### Cells (8)

`{blue,indigo,teal,copper}` × `{r01,r02}` × TS75  

cell_key pattern: `{seed}_rst_turtle_{r01|r02}_shares_ts75_heat3_6_10_caps3x10_20260924`  

experiment: `shares_ts75_mod_heat_bakeoff_20260924`

Exact heat hash written every cell (r01 example; r02 swaps `unit_risk_fraction` → `0.02`):

```ruby
{
  "unit_risk_fraction" => 0.01,  # or 0.02
  "max_units_per_market" => 3,
  "max_units_closely_correlated_same_direction" => 6,
  "max_units_loosely_correlated_same_direction" => 10,
  "max_units_single_direction" => 10,
  "correlation" => {
    "source" => "pcs_pairwise",
    "close_threshold" => 0.7,
    "loose_threshold" => 0.4,
    "window" => "methodology",
  },
}
```

## Stamp procedure (PBR Ops — CoS does not stamp)

Script: [`../analysis/2026-09-24-stamp-shares-ts75-modified-heat-bakeoff.rb`](../analysis/2026-09-24-stamp-shares-ts75-modified-heat-bakeoff.rb)

```bash
cd /home/johnkoisch/Documents/com/sawtooth
# Dry-run (no rows):
DRY_RUN=1 ./bin/compose exec -T -e DRY_RUN=1 winston_unit_test bin/rails runner \
  /ecosystem/docs/analysis/2026-09-24-stamp-shares-ts75-modified-heat-bakeoff.rb
# Live stamp + enqueue:
./bin/compose exec -T winston_unit_test bin/rails runner \
  /ecosystem/docs/analysis/2026-09-24-stamp-shares-ts75-modified-heat-bakeoff.rb
```

**Always** write full `heat` hash; set `heat_mode=turtle`. **Omit** `leap_fulfillment`. Idempotent on `cell_key`. New rows only. Enqueues `PortfolioBacktestJob`.

## Jev System One harness

**State**

1. Heat hash present + enabled on every cell (`heat_enabled?` true; knobs 3/6/10/10).
2. Heat never blank/omitted; `heat_mode=turtle`.
3. Caps 3/10; `leap_fulfillment` omitted.
4. All 8 cells `status=completed` (not failed / not operator_stopped).
5. Peak concurrent open positions ≤ 10 on every completed cell.

**Checkpoints (yes/no)**

1. Did any cell stamp without a non-empty `heat` hash? → **must be no**
2. Do heat knobs match 3/6/10/10 (+ `unit_risk_fraction` = risk)? → **must be yes**
3. Did any cell carry `leap_fulfillment`? → **must be no**
4. Caps 3/10 on every cell? → **must be yes**
5. All 8 completed before readout? → **must be yes** (else partial + list missing)
6. Any RangeError / operator_stop? → **must be no** (else fail-closed: no promote)
7. Peak open ≤ 10 on every completed cell? → **must be yes**

**Winner / Edge_R readout criteria**

- Primary: **Edge_R** (stored `edge_r`, post WUT PR #37) under heat+caps — prefer cells with Edge_R ≥ heat-absent TS75 twin at same book/risk (#772/#773/#776/#777/#780/#781/#784/#785) without peak_open breach.
- Secondary: Return/DD = `total_return / |max_drawdown|` (computed).
- Score r01 and r02 separately across the 4 books.
- **Clear heat-knob win** = modified-heat Edge_R ≥ control on ≥3/4 books at both risks (or ≥3/4 at one risk and not worse at the other), with harness green.
- Else: **no clear winner** — report best book/risk cells; do not invent promote language.
- Fail-closed: RangeError, operator_stop, or peak_open > 10 ⇒ **no promote**.

## Morning readout criteria

1. Table: PBR id, portfolio, risk, status, TR%, DD%, MAR/Return-DD, Edge_R, trades, peak_open, heat knobs verified.
2. Side-by-side vs heat-absent control (#772–#787 TS75 rows).
3. Harness pass/fail list.
4. Promote language: **shares-only paper candidate under modified heat** only — no LEAP, no live size-up.
5. If RangeError or cap/heat breach: stop promote talk; append issue.

## CLI seed (for Ops)

```
cwd: /home/johnkoisch/Documents/com/sawtooth
monolith: winston_unit_test
action: dry-run then stamp shares TS75 modified-heat bakeoff; do not edit Wv2; do not restamp Teal LEAP 767–770
acceptance: 8 pending/running PBRs; report JSON under ecosystem/docs/analysis/; leap omitted; heat hash present+enabled knobs 3/6/10/10; heat_mode=turtle; caps 3/10
System One: checkpoints 1–4 and 6–7 above before walking away overnight
```

## Related

- Prior shares bakeoff (heat-absent control): [`2026-09-23-shares-only-ts75-vs-ts77-bakeoff.md`](2026-09-23-shares-only-ts75-vs-ts77-bakeoff.md)
- Classic heat writer: [`../analysis/2026-09-21-stamp-teal-ts75-heat-on-r01.rb`](../analysis/2026-09-21-stamp-teal-ts75-heat-on-r01.rb)
- Evolve `heat_for`: [`../analysis/2026-09-18-evolve_indigo_teal_matrix.rb`](../analysis/2026-09-18-evolve_indigo_teal_matrix.rb)
- Heat bypass P0 / WUT #55: [`2026-09-21-wut-heat-on-rst-portfolio-limit-bypass.md`](2026-09-21-wut-heat-on-rst-portfolio-limit-bypass.md)
- RangeError P1: [`2026-09-22-wut-teal-heat-on-rangeerror-4byte-int.md`](2026-09-22-wut-teal-heat-on-rangeerror-4byte-int.md)
- Desk stop law: [`../business-context/exit-and-protective-stop-desk-law.md`](../business-context/exit-and-protective-stop-desk-law.md)


## Results (2026-09-24 CoS watch — PBRs 788–795)

All 8 cells `completed`. Experiment `shares_ts75_mod_heat_bakeoff_20260924`. No RangeError / operator_stop.

### Jev System One harness

| # | Checkpoint | Result |
|---|------------|--------|
| 1 | Heat hash non-empty | **pass** (`heat_enabled?` true; knobs present) |
| 2 | Knobs 3/6/10/10 + unit_risk_fraction = risk | **pass** |
| 3 | `leap_fulfillment` omitted | **pass** |
| 4 | Caps 3/10 | **pass** |
| 5 | All 8 completed | **pass** |
| 6 | No RangeError / operator_stop | **pass** |
| 7 | Peak open ≤ 10 | **pass** (max observed 9) |

### Scoreboard

| PBR | Book | Risk | TR% | DD% | Ret/DD | Edge_R | PF | Trades | peak_open | Heat | vs control |
|-----|------|------|-----|-----|--------|--------|----|--------|-----------|------|------------|
| 788 | Blue | 1% | 51.73 | 22.95 | 2.254 | **0.0879** | 1.22 | 468 | 9 | 3/6/10/10 turtle | = #772 |
| 789 | Blue | 2% | 96.99 | 26.97 | 3.596 | **0.0981** | 1.29 | 394 | 8 | 3/6/10/10 turtle | = #773 |
| 790 | Indigo | 1% | 45.91 | 23.97 | 1.916 | **0.0919** | 1.35 | 316 | 9 | 3/6/10/10 turtle | = #776 |
| 791 | Indigo | 2% | 82.82 | 24.86 | 3.331 | **0.1138** | 1.53 | 256 | 8 | 3/6/10/10 turtle | = #777 |
| 792 | Teal | 1% | −53.08 | 56.44 | −0.941 | **−0.1676** | 0.65 | 406 | 9 | 3/6/10/10 turtle | = #780 |
| 793 | Teal | 2% | −3.33 | 42.06 | −0.079 | **0.0769** | 0.97 | 336 | 7 | 3/6/10/10 turtle | = #781 |
| 794 | Copper | 1% | 168.55 | 16.32 | 10.327 | **0.311** | 1.73 | 550 | 9 | 3/6/10/10 turtle | = #784 |
| 795 | Copper | 2% | 215.98 | 22.70 | 9.514 | **0.2697** | 1.69 | 435 | 9 | 3/6/10/10 turtle | = #785 |

DNA verified in `results_json`: `heat_mode=turtle`, full heat hash, `instrument_mode=shares`, leap key omitted, caps 3/10.

### Verdict

- **Best Edge_R under modified heat:** Copper **#794** (r01) Edge_R **0.311** / TR 168.5% / DD 16.3% — same as heat-absent Copper #784.
- **Heat-knob effect:** Edge_R, TR%, and DD% are **byte-identical** to the heat-absent TS75 twins (#772/#773/#776/#777/#780/#781/#784/#785) on every book/risk. Modified heat did not move the scoreboard vs caps-only control.
- **Clear heat-knob win?** **No** (criterion ≥3/4 books improved or at least not worse with a real delta — here delta = 0 everywhere).
- **Promote:** **No** — shares-only paper candidate language stays with the prior heat-absent TS75 panel; this panel adds no new Edge_R evidence. No Wv2 promote.

## Follow-up (Operator 2026-09-24)

Mode D paper bind plan: [`2026-09-24-copper-794-mode-d-paper-bind.md`](2026-09-24-copper-794-mode-d-paper-bind.md) · [`../../plans/copper-794-mode-d-paper-bind.md`](../../plans/copper-794-mode-d-paper-bind.md).
