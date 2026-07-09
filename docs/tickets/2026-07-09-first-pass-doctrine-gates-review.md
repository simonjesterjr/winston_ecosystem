# Ticket: First-pass trend doctrine and viability gates review

**Status:** Proposed

**Date:** 2026-07-09

**Context:** Session [`2026-07-09-1308-orange-white-vet-trend`](../session-reports/2026-07-09-1308-orange-white-vet-trend.md). All four seed portfolios (Red, Blue, Orange, White) completed first-pass `vet_trend` and exported as **`observation` only**.

## Problem

First-pass grid + risk rules produce high max drawdown across every seed portfolio:

| Portfolio | Return | Max DD | export_kind |
|-----------|--------|--------|-------------|
| Red | +636% | 64% | observation |
| Blue | −98% | 100% | observation |
| Orange | +7.2% | 96% | observation |
| White | +7.3% | 94% | observation |

Gates (return ≥0%, DD ≤50%, trades ≥20) work as labels but the **doctrine** may be too aggressive (risk %, pyramid, market limits, swap, exit grid) for trade-ready handoff.

## Scope

1. Review `FIRST_PASS_BASE_CONFIG` and screening defaults against four observation outcomes.
2. Decide whether to tighten risk/position rules, expand strategy set, or change ranking/gates.
3. Document recommendation in analysis or business-context (update `portfolio-trading-strategy-evaluation.md` / `trade-ready-viability-gates.md` if thresholds change).
4. Optionally re-vet one portfolio under revised doctrine as smoke test.

## Acceptance

- Written recommendation with explicit keep / change decisions for risk, exits, ranking, gates
- If gates or defaults change: WUT code + docs updated; at least one portfolio re-export path verified

## Related

- Plan: `plans/portfolio-overlap-rebuild.md` (Phase 7 residual)
- Ticket: `2026-07-07-portfolio-trading-strategy-evaluation-framework.md`
- Session: `docs/session-reports/2026-07-09-1308-orange-white-vet-trend.md`
