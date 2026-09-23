# Ticket: WUT Teal heat-ON PBRs hit ActiveModel::RangeError (4-byte integer)

**Status:** Proposed  
**Priority:** P1  
**Date:** 2026-09-22  
**Mode:** contractor  
**Lane:** B  
**Implementer:** Grok CLI (default)  
**Graph nodes:** winston_unit_test (`PortfolioBacktestJob`, edge/persist integer columns)  
**Human gates:** Operator stopped retries — do not requeue Teal #767–#770 until fixed  
**DoD:** Heat-ON Teal Resting Stop Touch (RST) Portfolio Backtest Runs (PBRs) complete without `ActiveModel::RangeError` on a 4-byte integer; Sidekiq does not infinite-retry the same cell; column(s) that overflow are identified and widened or guarded with a fail-closed write.  
**Origin:** Operator stop 2026-09-22 (cycles burning on Teal post–Winston Unit Test (WUT) #55 requeue).  
**Evidence:** [`../analysis/2026-09-22-teal-pbr-767-770-rangeerror-stop.json`](../analysis/2026-09-22-teal-pbr-767-770-rangeerror-stop.json); requeue map [`../analysis/2026-09-21-requeue-heat-on-post55.md`](../analysis/2026-09-21-requeue-heat-on-post55.md); heat DD autopsy [`../analysis/2026-09-21-teal-heat-on-dd-autopsy-763-764.md`](../analysis/2026-09-21-teal-heat-on-dd-autopsy-763-764.md)  
**Related:** [`2026-09-21-wut-heat-on-rst-portfolio-limit-bypass.md`](2026-09-21-wut-heat-on-rst-portfolio-limit-bypass.md) (WUT #55); edge persist path

## Goal

Teal Mode C heat-ON RST cells stamped after WUT #55 can finish (or fail once with a durable non-retrying error). Today they die mid-window writing a value larger than a 4-byte signed integer column, then Sidekiq retries for hours.

## Specimens (stopped 2026-09-22)

| PBR | Risk | Cell (abbrev) | Replaces | Captured error |
|-----|------|---------------|----------|----------------|
| **#767** | 2% | `…_r02_…_p727_…` | #763 | `11484179049794764800 is out of range for ActiveModel::Type::Integer with limit 4 bytes` |
| **#768** | 2% | `…_r02_…_p743_…` | #764 | same as #767 |
| **#769** | 1% | `…_r01_…_p727_…` | #765 | `5742089524897382400 is out of range for ActiveModel::Type::Integer with limit 4 bytes` |
| **#770** | 1% | `…_r01_…_p743_…` | #766 | same as #769 |

All four: portfolio Teal (#412), `$30k`, TurtleV1 S1 / TS75, `leap_fulfillment=all`, `heat_mode=turtle`, experiment `mode_c_teal_heat_on_post55`. Progress before fail (examples): #769 ~1270/1808 days (`current_date` ~2024-08-08); #770 ~1225/1808 (`~2024-06-04`).

**Ops action taken:** status `failed`; `operator_stop` stamped on `results_json`; Sidekiq `PortfolioBacktestJob` retries for #767/#768 deleted (retry_count had reached 12). #769/#770 had no remaining retry rows when scrubbed. Orange #771 left running.

## Work items

- [ ] Identify which ActiveRecord attribute receives ~5.7e18 / ~1.1e19 (edge components, lot id, conid-sized field, or computed metric packed into `integer`)
- [ ] Fix: widen to `bigint`, or clamp/fail-closed before save so the job does not retry forever
- [ ] Spec reproducing RangeError on heat-ON Teal-class persist
- [ ] Do not auto-requeue #767–#770; Operator decides after fix
- [ ] In-band wrap + push WUT main

## System One harness

**State:** Evidence JSON path above; Sidekiq error strings exact; PBRs 767–770 status `failed` with `operator_stop`; WUT main at stop `a4565e2` (host).

**Checkpoints:**

| id | type | instructions | pass rule |
|----|------|--------------|-----------|
| overflow_column | Choice | options: identified_bigint_candidate, still_unknown | choice=identified_bigint_candidate ∧ confidence ≥ 0.7 |
| no_retry_storm | Noul | after fix, a forced overflow fails once and does not stay in RetrySet | noul ≥ 0.85 |
| teal_cell_completes_or_clean_fail | Noul | restamped Teal heat-ON cell either completes or fails with non-RangeError durable reason | noul ≥ 0.8 |

**Runner:** deterministic schema/column probe first; `jev ask` on residual “which metric blew up” smell  
**Order:** code/schema before Jev  
**On fail:** stop; do not requeue Teal heat-ON grid

## CLI seed

```
cwd: /home/johnkoisch/Documents/com/sawtooth/winston_unit_test
Lane B. Ticket: ecosystem/docs/tickets/2026-09-22-wut-teal-heat-on-rangeerror-4byte-int.md
Find which integer(4) column rejects 5742089524897382400 / 11484179049794764800 on Teal heat-ON PBR persist.
Widen or fail-closed; stop Sidekiq retry storms; specs green. Do not requeue 767–770 without Operator.
Push winston_unit_test main. Never commit graphify-out/.
```

## Non-goals

- Re-running #767–#770 before the overflow is fixed
- Changing turtle heat doctrine or Mode C Teal book weights
- Touching Orange #771 faithful-sim

## Overnight observation (2026-09-22 ~22:15 MT) — propose only

Read-only WUT glance during Loop B: **Orange PBR #771** (`orange_rst_turtle_r01_leap30k_20260922`, portfolio 35) is now **`failed`** with the same `ActiveModel::RangeError` value class as Teal 1% cells (`5742089524897382400…`), updated ~2026-09-22 17:53 MT. No `operator_stop` on #771. **I did not requeue** Teal or Orange. Morning: Operator may widen this ticket’s specimens to include #771 or file a sibling — still fail-closed until bigint/guard ships.

