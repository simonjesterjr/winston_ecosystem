# Ticket: Observe shuffled hourly snapshot on Telegram

**Status:** Proposed
**Priority:** P2
**Date:** 2026-08-13
**Monoliths:** winston_v2, Cromwell
**See:** [`docs/session-reports/2026-08-13-1248-hourly-snapshot-shuffle-movers.md`](../session-reports/2026-08-13-1248-hourly-snapshot-shuffle-movers.md); older observe log [`2026-07-13-observe-cromwell-market-snapshot-hourlies.md`](2026-07-13-observe-cromwell-market-snapshot-hourlies.md)

## Problem

Wv2 now shuffles Active Operational Portfolio books and returns at most 3 non-quiet movers. Compose smoke (2026-08-13 18:12Z) returned SHY / SOYB / AXON — not AAAU / AAL / AAPL. The next **natural** `market-snapshot-hourly` Telegram post has not been observed.

## Scope

Watch one open + one hourly (or the next NYSE-session hourly) on Sawtooth Main:

1. Confirm `mcp_winston_wv2_market_snapshot` ran this turn (nanobot logs).
2. Confirm Telegram is **not** the A-head dump (AAAU / AAL / AAPL quiet table).
3. If `movers` non-empty: at most 3 names, live prev → current + ATR + status.
4. If all quiet: one line (`All markets quiet.`), no symbol table.

## Acceptance

- [ ] One natural hourly logged (time, MCP call yes/no, Telegram quality)
- [ ] Names differ from a strict A-sort prefix **or** payload `summary.stopped_early` / `scanned` shows a shuffle scan
- [ ] No quiet-symbol dump

## Non-goals

- Rebuilding MCP (separate ticket)
- Changing Cromwell prompt/runtime rewrite
