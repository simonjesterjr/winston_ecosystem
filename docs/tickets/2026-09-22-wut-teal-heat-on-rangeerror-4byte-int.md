# Ticket: WUT Teal/Orange heat-ON PBRs hit ActiveModel::RangeError (4-byte integer)

**Status:** Fixed in code — operator restamp pending (do not requeue 767–771)  
**Priority:** P1  
**Date:** 2026-09-22 (scope expanded 2026-09-23)  
**Mode:** contractor  
**Lane:** B  
**Implementer:** Grok CLI (default) — **not** Winston Dev  
**Graph nodes:** winston_unit_test (`PortfolioBacktestJob`, edge/persist integer columns; likely `units` / `quantity`)  
**Human gates:** Operator stopped retries — do **not** requeue Teal #767–#770 or Orange #771 until fixed  
**DoD:** Heat-ON Teal Resting Stop Touch (RST) and Orange RST Portfolio Backtest Runs (PBRs) complete without `ActiveModel::RangeError` on a 4-byte integer; Sidekiq does not infinite-retry the same cell; column(s) that overflow are identified and widened **or** guarded with a fail-closed write (note: Teal 2% value exceeds signed 64-bit max ≈9.22e18, so bigint alone may be insufficient).  
**Origin:** Operator stop 2026-09-22 (cycles burning on Teal post–Winston Unit Test (WUT) #55 requeue); overnight Loop B 2026-09-22 ~22:15 MT saw Orange #771 fail same class.  
**Evidence:** [`../analysis/2026-09-22-teal-pbr-767-770-rangeerror-stop.json`](../analysis/2026-09-22-teal-pbr-767-770-rangeerror-stop.json); [`../analysis/2026-09-23-orange-pbr-771-rangeerror-glance.json`](../analysis/2026-09-23-orange-pbr-771-rangeerror-glance.json); requeue map [`../analysis/2026-09-21-requeue-heat-on-post55.md`](../analysis/2026-09-21-requeue-heat-on-post55.md); heat DD autopsy [`../analysis/2026-09-21-teal-heat-on-dd-autopsy-763-764.md`](../analysis/2026-09-21-teal-heat-on-dd-autopsy-763-764.md); overnight [`../analysis/2026-09-23-loop-b-overnight-pcs-depth-midband.md`](../analysis/2026-09-23-loop-b-overnight-pcs-depth-midband.md)  
**Related:** [`2026-09-21-wut-heat-on-rst-portfolio-limit-bypass.md`](2026-09-21-wut-heat-on-rst-portfolio-limit-bypass.md) (WUT #55); edge persist path

## Goal

Teal Mode C heat-ON RST cells stamped after WUT #55, and Orange RST faithful-sim #771, can finish (or fail once with a durable non-retrying error). Today they die mid-window writing a value larger than a 4-byte signed integer column, then Sidekiq retries for hours.

## Specimens (stopped / failed)

| PBR | Book | Risk | Cell (abbrev) | Overflow value | Notes |
|-----|------|------|---------------|----------------|-------|
| **#767** | Teal (#412) | 2% | `…_r02_…_p727_…` | `11484179049794764800` | operator_stop; replaces #763 |
| **#768** | Teal (#412) | 2% | `…_r02_…_p743_…` | `11484179049794764800` | operator_stop; replaces #764 |
| **#769** | Teal (#412) | 1% | `…_r01_…_p727_…` | `5742089524897382400` | operator_stop; replaces #765 |
| **#770** | Teal (#412) | 1% | `…_r01_…_p743_…` | `5742089524897382400` | operator_stop; replaces #766 |
| **#771** | Orange (#35) | 1% | `orange_rst_turtle_r01_leap30k_20260922` | `5742089524897382400` | failed ~2026-09-22 17:53 MT; **no** operator_stop; experiment `strategy77_rst_parity_v1` |

Teal four: `$30k`, TurtleV1 S1 / TS75, `leap_fulfillment=all`, `heat_mode=turtle`, experiment `mode_c_teal_heat_on_post55`. Progress before fail (examples): #769 ~1270/1808 days (`current_date` ~2024-08-08); #770 ~1225/1808 (`~2024-06-04`); #767/#768 `current_date` ~2025-05-21. Orange #771 `current_date` ~2025-05-23.

**Value relationship:** `11484179049794764800 == 2 × 5742089524897382400` (exact). Matches 2% vs 1% risk — strong smell that the overflowing attribute is **risk-scaled sizing** (`units` / `quantity` / `would_have_units`), not a random id.

**Ops action taken:** Teal #767–#770 status `failed`; `operator_stop` stamped on `results_json`; Sidekiq `PortfolioBacktestJob` retries for #767/#768 deleted (retry_count had reached 12). #769/#770 had no remaining retry rows when scrubbed. Orange #771 left running on 2026-09-22 stop pass; overnight glance found it **failed** same class — **still do not requeue**.

## Overflow column hypothesis (seed for implementer)

- **Not confirmed** which ActiveRecord attribute — Sidekiq dead/retry sets empty at seed time; #771 `results_json` backtrace truncates inside ActiveRecord `_create_record` (INSERT path) before app frames.
- **Best hypothesis:** 4-byte `integer` **units-like** column written on create during day advance:
  - `positions.units`
  - `paper_orders.quantity` (often copied from `position.units`)
  - `passed_signals.would_have_units`
  - less likely: `trading_signals.units` (runner often creates with `units: 0`), `journals.debit_credit`, `lab_fill_signal_evals.same_units` / `next_units`
- **Why:** risk-proportional exact 2× between r01 and r02 specimens; values are absurd as share counts → likely `risk_dollars / near-zero stop_distance` (or similar) then cast to Integer(4).
- **Fix shape:** identify column via reproducing insert / full backtrace; prefer **fail-closed clamp or reject** before save (Teal 2% value **does not fit signed bigint** ~9.22e18); widen alone is incomplete for #767/#768. Stop Sidekiq retry storms.

## Work items

- [x] Identify which ActiveRecord attribute receives ~5.7e18 / ~1.1e19 (probe hypothesis above; get app frames)
- [x] Fix: fail-closed before save and/or widen where safe; job must not retry forever
- [x] Spec reproducing RangeError on heat-ON Teal-class **and** Orange-class persist
- [x] Do not auto-requeue #767–#770 or #771; Operator decides after fix
- [x] In-band wrap + push WUT main

## Result (2026-09-23, Grok CLI)

**Column:** `passed_signals.would_have_units` (postgres `integer`, 4 bytes). The specimen is the uncapped share count `floor(risk_dollars / (atr × atr_multiplier))`, written by `PortfolioBacktestRunner#record_passed_signal` on arm-refuse / cash-skip before a LEAP save. LEAP `positions.units` stores contracts (`shares / 100`); `floor(5742089524897382400 / 100)` is a different integer, so the stored error text is not that column. `paper_orders.quantity` was not in play (`paper_run_id` null). The 2% value exceeds signed bigint, so the column was not widened.

**Fix:** refuse the entry (`units: 0`, reason `units_out_of_range`) in `EntryRequirementCalculator`, `PositionManager` (shares and contracts), and the passed-signal / paper-order writes. `PortfolioBacktestJob` `discard_on ActiveModel::RangeError` so a residual overflow is marked failed and is not re-raised into the Sidekiq retry set.

**System One (jevctl `jev ask`, model jev-1.13.0):**
- `overflow_column` choice=`identified_bigint_or_units_candidate` confidence=1.0 (pass ≥ 0.7)
- `no_retry_storm` noul=0.92 (pass ≥ 0.85)
- `teal_or_orange_cell_completes_or_clean_fail` noul=0.33 after the insert spec (fail < 0.8). Specimens were not restamped. Operator decides after this fix is on main.

## System One harness

**State:** Evidence JSON paths above; Sidekiq error strings exact; Teal PBRs 767–770 status `failed` with `operator_stop`; Orange #771 status `failed` (no operator_stop); WUT main at Teal stop `a4565e2` (host).

**Checkpoints:**

| id | type | instructions | pass rule |
|----|------|--------------|-----------|
| overflow_column | Choice | options: identified_bigint_or_units_candidate, still_unknown | choice=identified_bigint_or_units_candidate ∧ confidence ≥ 0.7 |
| no_retry_storm | Noul | after fix, a forced overflow fails once and does not stay in RetrySet | noul ≥ 0.85 |
| teal_or_orange_cell_completes_or_clean_fail | Noul | restamped Teal heat-ON or Orange RST cell either completes or fails with non-RangeError durable reason | noul ≥ 0.8 |

**Runner:** deterministic schema/column probe first (`positions.units` / `paper_orders.quantity` / `passed_signals.would_have_units`); prefer `jevctl` (no TypeSafe Python Software Development Kit (SDK)); `jev ask` only on residual “which metric blew up” smell  
**Order:** code/schema before Jev  
**On fail:** stop; do not requeue Teal heat-ON or Orange #771

## CLI seed

```
cwd: /home/johnkoisch/Documents/com/sawtooth/winston_unit_test
Lane B hotfix. Ticket: /home/johnkoisch/Documents/com/sawtooth/ecosystem/docs/tickets/2026-09-22-wut-teal-heat-on-rangeerror-4byte-int.md
Implementer = Grok CLI only (not Winston Dev).

Problem: ActiveModel::RangeError on Integer limit 4 bytes during PortfolioBacktestRunner persist/create.
Specimens (do NOT requeue):
  Teal #767/#768 → 11484179049794764800 (r02 / 2%)
  Teal #769/#770 + Orange #771 → 5742089524897382400 (r01 / 1%)
Exact 2× relationship ⇒ risk-scaled units/quantity smell.
Orange #771 results_json has truncated INSERT backtrace (ensure_in_range → _create_record); column not yet named.

Do:
1. Read this ticket (hypothesis + System One harness) and evidence JSONs under ecosystem/docs/analysis/.
2. Identify overflowing attribute (start: positions.units, paper_orders.quantity, passed_signals.would_have_units; PositionManager sizing ÷ stop_distance).
3. Prefer fail-closed guard before save (Teal 2% value exceeds signed bigint). Widen only if still correct semantically.
4. Failing spec first; then minimal fix; stop Sidekiq retry storms.
5. Use jevctl for System One checks (no TypeSafe Python SDK). jev ask only for residual harness smell.
6. In-band wrap + push winston_unit_test main. Update ecosystem ticket status if you touch docs. Never commit graphify-out/.
7. Do not requeue 767–771; Operator decides after fix lands.

DoD: column identified; RangeError cannot infinite-retry; specs green; push main.
```

## Shared watchable session (Operator)

Preferred desk pattern ([`../business-context/winston-bot-cli-ai-dlc-contract.md`](../business-context/winston-bot-cli-ai-dlc-contract.md)): Operator opens a **visible** terminal on **sawtooth-ai** and starts Grok Build Terminal User Interface (TUI) with the seed as the initial prompt. Chief of Staff (CoS) / bots follow that TUI; do not start a second implementer on this ticket.

```bash
cd /home/johnkoisch/Documents/com/sawtooth/winston_unit_test
SEED=$(sed -n '/^## CLI seed$/,/^## /p' \
  /home/johnkoisch/Documents/com/sawtooth/ecosystem/docs/tickets/2026-09-22-wut-teal-heat-on-rangeerror-4byte-int.md \
  | sed '1d;$d' | sed '/^```/d')
grok --fullscreen "$SEED"
```

Fallback (paste-only): `cd` same cwd → `grok` → paste the ``` CLI seed ``` block once.

## Non-goals

- Re-running #767–#771 before the overflow is fixed
- Changing turtle heat doctrine or Mode C Teal book weights
- Orange faithful-sim doctrine changes beyond surviving the integer write
- Winston Dev parallel implement on this ticket

## Overnight observation (2026-09-22 ~22:15 MT) — incorporated

Read-only WUT glance during Loop B: **Orange PBR #771** (`orange_rst_turtle_r01_leap30k_20260922`, portfolio 35) is **`failed`** with the same `ActiveModel::RangeError` value class as Teal 1% cells (`5742089524897382400…`), updated ~2026-09-22 17:53 MT. No `operator_stop` on #771. **Did not requeue** Teal or Orange. **2026-09-23 Lane B seed:** scope expanded to include #771 in this ticket (no sibling).
