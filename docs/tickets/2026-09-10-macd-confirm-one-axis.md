# Ticket: One-axis MACD 12/26/9 confirm vs EMA-20

**Status:** Proposed — blocked
**Priority:** P2
**Date:** 2026-09-10
**Mode:** contractor
**Graph nodes:** winston_unit_test
**Monolith:** winston_unit_test (lab); handoff to winston_v2 only if a winner is promoted
**Origin:** session `docs/session-reports/2026-09-10-1121-macd-and-walnut-slate.md`
**Blocked on:** [`2026-09-04-tf-p1-residual-signal-and-oos.md`](2026-09-04-tf-p1-residual-signal-and-oos.md)

## Problem

`Macd1269Strategy` is in the WUT/Wv2 zoo (long when MACD line > signal; short when line < signal; lookback 34). It is **not** a live default. Semi-Markov trend-following theory says a MACD-like rule is the next confirm after Exponential Moving Average (EMA) 20 (ADR-008 Blue hard confirm).

Do not run this until the residual-signal / true walk-forward harness exists. A joint re-grid of entry × confirm × ladder × Kelly × MACD is forbidden.

## Work

1. One axis only: frozen parent (Blue C03 EMA-20 hard, and/or Turtle Mint System 2) **with** `Macd1269Strategy` as confirmational vs the parent’s current confirm (or none).
2. Causal bars only; same fill cadence as the parent.
3. Rank with the P1 measurement pack (walk-forward / embargo), not full-sample Sharpe fishing.
4. Do not promote to an Engaged Operational Portfolio without a new Observation series.

## Acceptance

- [ ] P1 residual-signal / walk-forward harness is in use on the frozen parent first.
- [ ] One-axis PBR: parent vs parent+MACD confirm. Deflated Sharpe / Bonferroni if the grid grows.
- [ ] Fingerprint includes `Macd1269Strategy` when selected. No silent mutation of an Engaged OP.

## Out of scope

- HMM regime overlay
- Making MACD the live default
- Joint search with One-Way Dynamic / Kelly
- Changing 12/26/9 periods

## Related

- ADR-008 (confirmational entry, initial only)
- `winston_unit_test/app/strategies/entry_exit/macd_1269_strategy.rb`
- TF competency: `docs/tickets/2026-09-04-tf-foundations-INDEX.md`
