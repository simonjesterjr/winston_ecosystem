# Ticket: Snapshot shuffle universe — Active books vs full parquet population

**Status:** Proposed
**Priority:** P2
**Date:** 2026-08-13
**Monoliths:** winston_v2
**See:** [`docs/session-reports/2026-08-13-1248-hourly-snapshot-shuffle-movers.md`](../session-reports/2026-08-13-1248-hourly-snapshot-shuffle-movers.md); related [`2026-07-13-market-radar-core-portfolio-scope.md`](2026-07-13-market-radar-core-portfolio-scope.md)

## Problem

Operator asked to randomize “our population of markets.” This session kept the existing source: **Books on Active Operational Portfolios** (70 names on 2026-08-13 smoke). That fixed the alphanumeric AAAU/AAL/AAPL bug without widening the universe.

Still undecided: should the hourly radar shuffle

- Active OP books (shipped),
- all portfolio books,
- a tagged “core” subset, or
- every market with data_manager (DM) parquet?

Widening to the full parquet set makes Sidekiq early-stop more important and can surface names the desk does not trade.

## Scope

1. Operator product call on the four options above.
2. If not Active books: change `MarketSnapshotService#resolved_symbols` only; keep shuffle + stop-at-3 + movers-only payload.
3. Smoke: one `/internal/market_snapshot` and note `summary.population`.

## Acceptance

- [ ] Written product rule in this ticket (or radar-scope ticket)
- [ ] Code matches the rule
- [ ] Skill / MCP one-liner updated if the universe changes

## Non-goals

- Changing ATR classify thresholds
- Rebuilding Cromwell formatting
