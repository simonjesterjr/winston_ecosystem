---
id: ISSUE-20260921-option-enter-working-stop-from-premium
title: Option Plan B confirm books Working Stop from premium − 2N, not 2N under the underlying
status: triage
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

**Status banner:** Open — two Mode C paper lots already booked with through-the-market stops (2026-09-21 wrap).

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
- Wrap [`../session-reports/2026-09-21-1457-mode-c-furthest-call-desk-uat.md`](../session-reports/2026-09-21-1457-mode-c-furthest-call-desk-uat.md) §7 / §11
- Live: Journal 1943 `stop_price=0.78`; Journal 1946 / Position 889 `updated_stop=2.33`

## Related

Ticket [`../tickets/2026-09-21-option-enter-working-stop-underlying.md`](../tickets/2026-09-21-option-enter-working-stop-underlying.md). Distinct from exit-at-stop fill mark ([`../tickets/2026-09-20-mode-c-leap-exit-at-stop-option-mark.md`](../tickets/2026-09-20-mode-c-leap-exit-at-stop-option-mark.md)): that ticket is **exit fill = option mark**; this issue is **enter Working Stop = underlying**.
