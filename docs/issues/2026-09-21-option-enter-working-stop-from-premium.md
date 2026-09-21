---
id: ISSUE-20260921-option-enter-working-stop-from-premium
title: Option Plan B confirm books Working Stop from premium − 2N, not 2N under the underlying
status: in-progress
type: bug
priority: p0
created: 2026-09-21
updated: 2026-09-21
labels: [p0, mode-c, desk, working-stop, standard_call]
related:
  - docs/tickets/2026-09-21-option-enter-working-stop-underlying.md
  - docs/tickets/2026-09-20-mode-c-leap-exit-at-stop-option-mark.md
  - docs/adr/ADR-018-mode-c-leap-plan-a-plan-b.md
  - docs/session-reports/2026-09-21-1457-mode-c-furthest-call-desk-uat.md
---

# Option Plan B confirm books Working Stop from premium − 2N

**Status banner:** Under investigation — candidate in winston_v2 working tree; journals 1943 / 1946 Working Stops restored on paper (29.95 / 24.85). Resolve when the code commit lands.

## Summary

Desk workflow fill-stop JS treats **Price** as the underlying fill. After option Plan B prefills Price with the listed-call mid, Confirm writes `updated_stop = premium − 2×ATR`. Working Stop law (ADR-018) keeps the stop on the **underlying**. Booked SEF 1943 `updated_stop=0.78` (spot ~30.54) and BITQ 1946 `updated_stop=2.33` (spot ~27.31).

## Problem statement

A long call enter must not move the pyramid / Working Stop onto option premium space. The stop is the signal-path stop on the stock or ETF. Anything that reads `Position#updated_stop` as an underlying GTC will treat these lots as already stopped.

## Current behavior

1. Overlay stamps option mid into the Price field (`1.375` SEF, `4.75` BITQ).
2. `_fill_stop_adjust_script.html.erb` `stopFromFill(fill, dist, direction)` runs on Price input/change and on load (`sync()`).
3. `fill` is the premium; `dist` is still 2×ATR of the underlying. Long stop = premium − dist.
4. Confirm persists that number on the journal details and `Position#original_stop` / `#updated_stop`.

| Journal | Underlying | Suggested (form, pre-premium) | Booked stop |
|---------|------------|-------------------------------|-------------|
| 1943 SEF / Mango pos (call 4× Feb 30) | ~30.54 | 29.95 | **0.78** |
| 1946 BITQ / Indigo #889 | ~27.31 | 24.89 | **2.33** |

## Expected behavior

- Working Stop stays 2N under (long) or over (short) the **underlying** reference (signal close / next open), not the option mid.
- Fill-stop JS must not rewrite stop when `fulfillment_type` is option-like (`leap`, `standard_call`, `option`).
- Confirm must not persist a premium-space stop onto `Position#updated_stop`.

## Reproduction

### Preconditions

Mode C paper OP, dummy_sim, CPGW up, draft enter that resolves Plan B `standard_call` with a live mid.

### Steps

1. Open desk workflow for a packaged call (Price = option mid, Stop originally ~2N under stock).
2. Do not touch Stop. Confirm.

### Observed result

`fulfillment_details["stop_price"]` and `Position#updated_stop` equal premium − 2×ATR.

### Reproducibility

Always, as long as fill-stop `sync()` runs after premium prefill.

## Evidence

- `winston_v2/app/views/operations/shared/_fill_stop_adjust_script.html.erb`
| Evidence | Source | What it establishes |
|---|---|---|
| `_fill_stop_adjust_script.html.erb` `stopFromFill` | winston_v2 | Client rewrites Stop from Price − 2×ATR |
| `DeskContext.apply_fill_adjusted_stop` | winston_v2 | Server re-anchors Stop onto fill when Price ≠ expected |
| `JournalConfirmationService#lot_working_stop_price` | winston_v2 | Enter/pyramid Working Stop uses `resolved_price` (option premium) as fill |
| Wrap §7 / §11 | [`../session-reports/2026-09-21-1457-mode-c-furthest-call-desk-uat.md`](../session-reports/2026-09-21-1457-mode-c-furthest-call-desk-uat.md) | Booked SEF 1943 stop 0.78; BITQ 1946 / pos 889 stop 2.33 |

## Impact and priority

Anything that treats `Position#updated_stop` as an underlying GTC will false-trigger stop-out on the two live Mode C paper lots. P0 because capital-path stop hygiene is already wrong on booked paper.

## Scope and preservation requirements

### In scope

- Skip fill-stop JS rewrite when fulfillment is option-like (`leap` / `standard_call` / `option` / `option_strategy`).
- Confirm must persist the underlying 2N Working Stop, not `premium − 2N`.
- Request spec lock for Plan B `standard_call` GET + confirm.

### Must preserve

- Stock enter fill-stop JS still retargets when the operator edits the **share** fill.
- Working Stop geometry (ATR multiple, pyramid) unchanged.
- Exit-at-stop fill remains option mark (separate P0 ticket) — Working Stop is not the fill.

### Out of scope

- Silent IBKR STP.
- Operator-gated correction of journals 1943 / 1946 (ticket DoD; not a silent flatten).

## Acceptance criteria

- [x] Given a Plan B `standard_call` desk GET, when Price is option mid, then Stop is ~2N under the underlying close (not premium − 2N).
- [x] Given Confirm of that draft, when Price is premium, then `Position#updated_stop` is the underlying Working Stop.
- [x] Stock enter fill-stop re-anchor spec still passes.
- [x] Journals 1943 and 1946 corrected or operator-noted.

## Investigation notes

Hypothesis confirmed in code: three stacked writers (JS `sync()`, `apply_fill_stop!`, `lot_working_stop_price`) all treat Price as an underlying fill. `StopSuggestion` already uses `signal_close` as reference for `standard_call` (not in its skip list), so GET HTML can be correct before JS runs.

## Unknowns and clarifying questions

- [x] None blocking. Booked-lot correction waits on operator go.

## Dependencies and risks

ADR-018 Working Stop on underlying. Distinct from [`../tickets/2026-09-20-mode-c-leap-exit-at-stop-option-mark.md`](../tickets/2026-09-20-mode-c-leap-exit-at-stop-option-mark.md).

## Verification plan

- `spec/requests/desk_workflow_plan_c_overlay_spec.rb` Plan B GET + confirm.
- `spec/services/operations/desk_context_fill_stop_spec.rb` option-like skip.
- `spec/services/operations/journal_confirmation_service_spec.rb` option enter stop.
- Existing stock fill-stop request spec.
- Compose `winston_v2` rspec for those files.

## History

- 2026-09-21 — Created from wrap 2026-09-21 Mode C furthest-call desk UAT.
- 2026-09-21 — Marked `ready`: acceptance, preservation, and persist-path notes (`lot_working_stop_price`) added.
- 2026-09-21 — Candidate in winston_v2: skip fill-stop rewrite for option-like; StopSuggestion uses underlying bar; confirm `lot_working_stop_price` uses signal close / bar, not premium. Request + unit specs pass. Live 1943 stop 0.78 vs intended 29.95; 1946 stop 2.33 vs intended 24.85. Correction operator-gated.
- 2026-09-21 — Operator go: journal 1943 / pos 887 `original_stop`/`updated_stop`/`stop_price` 0.78 → **29.95**; journal 1946 / pos 889 2.33 → **24.85**. No cash change, no flatten, no Desk-Send.
