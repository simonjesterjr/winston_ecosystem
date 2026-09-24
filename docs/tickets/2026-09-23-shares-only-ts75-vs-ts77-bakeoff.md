# Ticket: Shares-only TS75 vs TS77 bakeoff (IBKR Level 2 path)

**Status:** Proposed  
**Priority:** P1  
**Date:** 2026-09-23  
**Lane:** B (matrix design + stamp script; Ops stamps — CoS does not enqueue)  
**Owner:** PBR Ops / Sawtooth Ops (stamp); CoS (ticket + morning readout)  
**Human gates:** Operator go before live stamp; morning winner call with John before any Wv2 promote  
**DoD:** 16 shares-only cells completed (not failed); Jev harness green; morning readout names TS75 or TS77 under winner rule, or “no clear winner” if split

## Goal

Pick a **shares-only** (no LEAP, no option packaging) book for the paper IBKR account while it is Level 1 options (covered only). Build a trade record toward **Level 2 options**. Compare **TS75** vs **TS77** under hard position caps the desk will actually trade.

## Evidence summary (Part 1 — read-only)

**Clear winner today? No.**

Comparable shares-only evidence is incomplete:

| Cohort | What exists | Gap |
|--------|-------------|-----|
| `strategy77_rst_parity_v1` / heat-risk | Many completed **TS77 shares** RST cells (heat legacy/turtle, risk 1%/2%, caps 4/12) across Blue/Orange/Mint/Yellow/… | **No TS75 twin** in the same modern RST + Edge_R panel |
| `turtle_systems_v1` (~#424–#447) | Shares TS75 / TS76 / TS77 @ 1%, caps 4/12, hybrid fill | Old panel; **no Edge_R**; fill ≠ resting_stop_touch; head-to-head **split** (TS75 6 books, TS77 4) — not a clear winner |
| Mode C Indigo/Teal/Copper/Slate evolved | Strong TS75 LEAP numbers (e.g. Teal #743 Edge_R ~17, OA ~20k%) | **LEAP fulfillment = all** — not valid for Level 1 shares path |
| Teal heat-ON #763–#770 / Orange #771 | LEAP + heat; #767–#770 RangeError; #771 Edge_R −0.1458 | Wrong instrument for this ask |

### Head-to-head shares (turtle_systems_v1, r01, caps 4/12, no Edge_R)

| Portfolio | TS75 | TS77 | Local winner (total return) |
|-----------|------|------|-----------------------------|
| Blue p7 | #424 TR −45.9% | #426 TR −72.8% | TS75 |
| Mango p65 | #427 TR −99.4% | #429 TR +45.7% | TS77 |
| Mint p110 | #430 TR +103.5% | #432 TR +537.0% | TS77 |
| Yellow p111 | #433 TR +328.1% / DD 20.9% | #435 TR +74.2% | TS75 |
| Orange p35 | #436 TR −11.5% | #438 TR −92.9% | TS75 |
| Red p6 | #439 TR −102.6% | #441 TR +96.5% | TS77 |
| Green p63 | #442 TR +4.0% | #444 TR −13.7% | TS75 |
| Rust p66 | #445 TR +18.1% | #447 TR −71.2% | TS75 |

Split board + missing Edge_R + wrong fill arm ⇒ **not** a promotion-grade winner.

Best modern **shares** single cell (TS77 only): Orange #649 legacy r02 — TR ~989%, DD ~36%, Edge_R ~0.69, MAR ~27 — still no TS75 control at same DNA.

## Heat-ON bug status

- Ticket [`2026-09-21-wut-heat-on-rst-portfolio-limit-bypass.md`](2026-09-21-wut-heat-on-rst-portfolio-limit-bypass.md) still **P0 In progress**.
- WUT **PR #55 is merged** on host (`0902707`) and runner now comments that combined `portfolio_limit` is always enforced.
- Post-#55 Teal heat-ON restamps **#767–#770 failed** with ActiveModel::RangeError before we could verify open ≤ cap; related P1 RangeError ticket still open.
- **Matrix decision: heat OFF** (hard caps only). Do not include heat-ON cells until RangeError is fixed and a probe shows peak open ≤ `max_positions_per_portfolio`.

## Matrix (Part 2)

| Dim | Value |
|-----|-------|
| Instrument | **Shares-only** (`leap_fulfillment` omitted) |
| Strategies | TS75 vs TS77 |
| Risk | 1% and 2% per unit |
| Heat | **OFF** (no heat hash; `heat_mode=legacy` label only) |
| Caps | `max_positions_per_symbol=3`, `max_positions_per_portfolio=10` |
| Fill | `resting_stop_touch` / resting arm |
| Stop | `move_to_last_entry`, `atr_multiplier=2` (desk law for TS75; same stop column for fair TS77 compare — exit *signal* still 10d vs 20d per TS) |
| Capital | $30,000 |
| Date range | Per-portfolio natural bar overlap (within-book TS75/TS77 share the same window). Observed anchors: Blue ~2020-08-05→2026-09-14; Indigo ~2021-05-10→2026-09-18; Teal/Copper ~2019-07-22→2026-09-18 |

### Portfolios (verified WUT ids)

| Seed | Id | Name | n markets | Sample tickers |
|------|----|------|-----------|----------------|
| blue | **7** | Portfolio Blue | 11 | AAL,AMZN,GLD,GOOGL,JNJ,PG,RXT,TSLA,TSM,WMT,XLE |
| indigo | **411** | Indigo_WUT_evolved | 10 | AMAT,BITQ,DBA,FPA,IBM,MSFT,TLT,URA,USDU,XLV |
| teal | **412** | Teal_WUT_evolved | 11 | COPR,DBA,FPA,GLD,JNJ,PG,TLT,USDU,XLE,XLI,XLU |
| copper | **413** | Portfolio Copper | 11 | AMZN,GLD,GOOGL,JNJ,MSFT,PG,TSLA,TSM,WMT,XLE,XLV |

Optional follow-on (not overnight): Slate p414.

### Cells (16)

`{blue,indigo,teal,copper}` × `{ts75,ts77}` × `{r01,r02}`  
cell_key pattern: `{seed}_rst_legacy_{r01|r02}_shares_ts{75|77}_caps3x10_20260923`

### Runtime / queue (host checked 2026-09-23 ~22:45 MT)

- GPU 3090 ~0% util (ollama idle resident only); Sidekiq default queue **0**; busy **0**; concurrency **5**.
- Prior shares RST wall times ~0.5–2.3h/cell; LEAP Mode C ~2–6h (N/A here).
- **16 cells @ concurrency 5** ⇒ ~4 waves. At ~1–1.5h/cell median ⇒ **~4–6h wall** — fits finish-by-~06:00 MT if stamped tonight. Priority enqueue order: all **r02** first, then r01.

## Stamp procedure (PBR Ops)

Schema fields: **`max_positions_per_symbol`** (units per market), **`max_positions_per_portfolio`**.

Script (same clone/DNA pattern as #763–#770 teal stamps):

[`../analysis/2026-09-23-stamp-shares-only-ts75-vs-ts77-bakeoff.rb`](../analysis/2026-09-23-stamp-shares-only-ts75-vs-ts77-bakeoff.rb)

```bash
cd /home/johnkoisch/Documents/com/sawtooth
# Dry-run (no rows):
DRY_RUN=1 ./bin/compose exec -T -e DRY_RUN=1 winston_unit_test bin/rails runner \
  /ecosystem/docs/analysis/2026-09-23-stamp-shares-only-ts75-vs-ts77-bakeoff.rb
# Live stamp + enqueue:
./bin/compose exec -T winston_unit_test bin/rails runner \
  /ecosystem/docs/analysis/2026-09-23-stamp-shares-only-ts75-vs-ts77-bakeoff.rb
```

Dry-run already verified on host: 16 planned cell_keys, factory methods present, no rows written.

**Do not** set `leap_fulfillment`. **Do not** write a `heat` hash. Confirm after stamp: caps 3/10, `leap_fulfillment` blank, status pending→running.

## Jev System One harness

**State**

1. All 16 cells share caps 3/10, heat OFF, leap omitted, fill resting_stop_touch, stop move_to_last_entry×2, initial $30k.
2. Within each portfolio, TS75 and TS77 cells share the same overlap window.
3. Every cell `status=completed` (not failed / not operator_stopped).
4. Edge_R present on each completed cell (or documented null with cause).

**Checkpoints (yes/no)**

1. Did any cell stamp with `leap_fulfillment` set? → **must be no**
2. Did any cell carry a non-empty `heat` hash? → **must be no**
3. Did any completed cell show peak concurrent positions > 10? → **must be no**
4. Are all 16 completed before readout? → **must be yes** (else readout = partial + list missing)
5. Winner rule (below) applied on completed set? → **must be yes**

**Winner rule**

Across the 4 portfolios, at each risk (1% and 2% scored separately, then agree):

- Prefer the TS with **better return/DD (MAR)** and **Edge_R not worse** (Edge_R_candidate ≥ Edge_R_other − 0.05).
- **Clear winner** = same TS wins on **≥3 of 4** portfolios at **both** risks, or wins ≥3/4 at one risk and not worse at the other.
- Else: **no clear winner** — keep both as paper candidates or extend matrix (Slate / Red).

## Morning readout criteria

1. Table: PBR id, portfolio, TS, risk, status, TR%, DD%, MAR, Edge_R, trades, peak_open.
2. Per-portfolio winner at r01 and r02.
3. Harness pass/fail list.
4. Promote language: **shares-only paper candidate** only — no LEAP, no live size-up.
5. If RangeError or cap breach appears on any cell: stop promote talk; file/append issue.

## CLI seed (for Ops)

```
cwd: /home/johnkoisch/Documents/com/sawtooth
monolith: winston_unit_test
action: dry-run then stamp shares bakeoff script; do not edit Wv2; push not required for stamp
acceptance: 16 pending/running PBRs; report JSON under ecosystem/docs/analysis/; leap blank; heat blank; caps 3/10
System One: checkpoints 1–3 above before walking away overnight
```

## Related

- Desk stop law: [`../business-context/exit-and-protective-stop-desk-law.md`](../business-context/exit-and-protective-stop-desk-law.md)
- Heat bypass P0: [`2026-09-21-wut-heat-on-rst-portfolio-limit-bypass.md`](2026-09-21-wut-heat-on-rst-portfolio-limit-bypass.md)
- RangeError P1: [`2026-09-22-wut-teal-heat-on-rangeerror-4byte-int.md`](2026-09-22-wut-teal-heat-on-rangeerror-4byte-int.md)
- TS77 shares RST panel: [`../analysis/2026-09-13-strategy77-rst-heat-risk-matrix.md`](../analysis/2026-09-13-strategy77-rst-heat-risk-matrix.md)
