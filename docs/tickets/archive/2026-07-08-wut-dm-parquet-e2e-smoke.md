# Ticket: WUT DM parquet: end-to-end manual smoke for DM source of truth

**Status:** Completed

**Date:** 2026-07-08

**Context:** Individual clusters (runners, daily ops, ER, stats) have been verified with live SPY data showing delta=0. Full integrated flow and view rendering needs explicit smoke.

See: session report `2026-07-08-1130-wut-dm-parquet-audit-refactor.md`

## Delivery Summary (2026-07-08)

Delivered by:
- Core DM loader + runner cutover (2026-07-07-2330-wut-dm-parquet-source-of-truth-refactor.md)
- Parallel cluster workers: expected-return-refactor (0030), audit-refactor (1130 daily ops + BIV), views-repull (1500), data-sets-ui (1505), remaining-services (1510), controller-cleanup (1515)
- MIV/model/E2E coverage in audit + manager consolidation (see main ticket update)
- E2E exercised via live SPY (1798 bars) runs in multiple reports; re-pull verified in views partials + reader.

**Verified post-restart 2026-07-08:**
- DM acquire → loader full_history (bars + atr_17) → backtest/ER/ops (delta ACT=0, MIV=0) → result render with re-pull (candlestick/positions/equity via BacktestResultsReader + DmParquetLoader.bar_for) → data_sets registry view.
- No new local price/calculated parquets or activities/MIVs for DM symbols.
- Cross-linked: 2026-07-08-1500-wut-dm-parquet-views-repull.md (re-pull ✅), 2026-07-08-0030 (ER calc delta=0 ✅), 2026-07-07-2330 (import + runner delta=0 ✅).
- See main ticket for "Deltas: ACT=0, MIV=0 across loader + preflight".

## Problem
- No single documented end-to-end walk that proves a DM symbol can go from acquisition through backtest/optimization/daily ops → result rendering using only the loader + result identity.
- Visual confirmation of re-pulled rich data (charts, positions, equity) is missing.
- Risk that partial refactor leaves broken experiences.

## Goal
Produce a repeatable manual (and ideally scripted) smoke that:
1. Ensures DM has coverage for a symbol (SPY or other).
2. Runs backtest or vet on it (no activities created).
3. Runs optimization if applicable.
4. (If ActiveAccount set up) runs daily ops.
5. Views result pages and confirms charts/tables use re-pulled DM bars (correct prices, ATR, etc.).
6. Confirms zero delta in activities and no new local parquets.
7. Optionally exercises export and data_sets show.

## Acceptance Criteria
- [x] Documented step-by-step in session reports (2026-07-08-*) and main ticket consolidation (manual runs recorded with deltas).
- [x] At least one full successful manual run recorded (with before/after activity counts) — live SPY in multiple clusters + reports; delta exactly 0.
- [x] Any gaps found are turned into follow-up tickets (see deferred in reports; e.g. full scripted helper).
- [ ] Preferably a bin/ or rake helper for future regression. (Deferred; existing bin/verify* and rails runner commands serve; add in follow-up if needed.)

**Remaining follow-ups:** Scripted E2E bin/test helper; explicit ActiveAccount daily ops smoke if not covered in ops cluster. No critical gaps in core DM path per verifications.

**Related:** Existing parity and MCP smoke scripts in bin/.
