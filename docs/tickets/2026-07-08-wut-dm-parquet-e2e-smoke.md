# Ticket: WUT DM parquet: end-to-end manual smoke for DM source of truth

**Status:** Proposed

**Date:** 2026-07-08

**Context:** Individual clusters (runners, daily ops, ER, stats) have been verified with live SPY data showing delta=0. Full integrated flow and view rendering needs explicit smoke.

See: session report `2026-07-08-1130-wut-dm-parquet-audit-refactor.md`

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
- [ ] Documented step-by-step in a ticket comment or a TESTING_*.md update.
- [ ] At least one full successful manual run recorded (with before/after activity counts).
- [ ] Any gaps found are turned into follow-up tickets.
- [ ] Preferably a bin/ or rake helper for future regression.

**Related:** Existing parity and MCP smoke scripts in bin/.
