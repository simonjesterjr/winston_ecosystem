# Ticket: Wire standard_call flatten / roll DTE to desk tasks

**Status:** Done  
**Priority:** P1  
**Date:** 2026-09-20  
**Mode:** contractor  
**Graph nodes:** winston_v2 (`CallLifecycle`, Daily Analysis / task generator, desk workflow)  
**Human gates:** Human-in-the-loop sell-to-close / roll; no auto-exercise; do not say “assignment” for long calls  
**DoD:** Open `standard_call` overlay legs emit flatten (DTE < `flatten_below_dte`) or roll-window desk tasks. Operator confirms. Default: do not auto-exercise; HITL if intrinsic near expiry.  
**Origin:** Wrap [`../session-reports/2026-09-20-1140-standard-call-packaging-rung.md`](../session-reports/2026-09-20-1140-standard-call-packaging-rung.md); helper already `winston_v2/app/services/operations/call_lifecycle.rb`  
**Related:** [`2026-09-19-standard-call-fulfillment-packaging-rung.md`](2026-09-19-standard-call-fulfillment-packaging-rung.md) (selector first deliverable); ADR-018 addendum

## Problem

Selector stamps `lifecycle_action` / exercise policy. Nothing in Daily Analysis or the desk mints flatten/roll work. Standard calls decay faster than LEAPs. Promote to **P0** the day any live/paper OP holds `standard_call` inside the flatten window.

## Scope

1. DA (or EOD cadence) walks open option-packaged lots; `CallLifecycle.action` → enter/flatten/roll task.  
2. Confirm is HITL sell-to-close (or roll pick) of the packaged call. Working Stop still on underlying.  
3. Earnings avoid remains a flag only (no fake data).

## Non-goals

- Auto-exercise  
- Silent option STP  
- Changing TF exit signals

## Acceptance

- [x] Lot with DTE < flatten_below_dte gets a flatten task (`task_type=exit`, HITL sell-to-close at option mark; not ExitAtStopService)
- [x] DTE in roll_window gets a roll task (`task_type=hitl` attention; no roll picker in v1)
- [x] Confirm does not auto-exercise (copy + `exercise_policy.auto_exercise=false`; no “assignment”)

Mode C dummy_sim only. LEAP knobs keep `flatten_below_dte: nil` so long-dated lots are not flattened at 7 DTE. Idempotent. Bound books skipped until Lane 2 OPT Send exists.
