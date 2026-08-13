# Ticket: Live DAR render — free cash + risk equity + over-deployed

**Status:** In progress — smoke regenerate done 2026-08-12 (no Telegram)  
**Priority:** P2  
**Date:** 2026-08-12  
**Monolith:** winston_v2  
**Domain:** Daily Activity Report, PositionSizer, Turtle capital  
**See:** [`2026-08-12-1541-dar-risk-equity-desk-stop.md`](../session-reports/2026-08-12-1541-dar-risk-equity-desk-stop.md)  
**Program:** [`2026-08-12-turtle-systems-eval-and-ops-alignment.md`](2026-08-12-turtle-systems-eval-and-ops-alignment.md) workstream E (code landed)

## Problem

Workstream E shipped: units size on **risk equity**; DAR payload / markdown / PDF include free cash, risk equity, and an over-deployed flag. Specs are green. The channel has not yet seen a regenerated report, so operator review of column density and the 25% flag is still pending.

## Scope

1. Run Daily Analysis for a current report date (or re-render existing payload) **without** Telegram unless the operator asks.
2. Confirm summary + chapter pages show **Free cash** and **Risk equity**.
3. If any Active OP has free cash / risk equity < 0.25 (or negative cash with positive equity), the over-deployed callout is visible.
4. Spot-check that unit proposals on that DAR still look sane vs prior cash-only sizing (open lots should size off equity, not free cash).

## Progress (2026-08-12 evening)

- [x] Smoke: `DailyReportPayloadBuilder.build` + `DailyActivityReportMarkdownRenderer.render!` for 2026-08-12 → `storage/reports/wv2_20260812.md`
- [x] Dual Free cash / Risk equity columns present; over-deployed callouts for Rust / Yellow / Mango (negative free cash + positive risk equity)
- [x] Chapter `free_cash` aligned to `RiskEquity` snapshot (no longer display-snap disagreeing with flag)
- [ ] Operator visual review of MD/PDF density (open file under `/wv2` reports or container `storage/reports/`)
- [ ] Full `DailyAnalysisJob` path (tasks + Telegram) not required for close

## Non-goals

- Changing `OVER_DEPLOYED_RATIO` (0.25) unless the live PDF makes the flag too noisy
- Re-opening heat L1–L4 or Turtle matrix cells

## Acceptance

- [x] Regenerated markdown shows dual metrics + over-deployed (agent smoke)
- [ ] Operator has opened the new PDF or markdown
- [ ] Telegram redelivery only if explicitly requested

## Related

- `Operations::RiskEquity`
- `DailyReportPayloadBuilder` chapter fields
- `daily_activity_report_{markdown,pdf}_renderer.rb`
