# Ticket: Operator click-through — TSMC → TSM storage remap

**Status:** Proposed  
**Priority:** P2  
**Date:** 2026-08-19  
**Related:** session [`docs/session-reports/2026-08-19-1304-tsmc-to-tsm-storage-remap.md`](../session-reports/2026-08-19-1304-tsmc-to-tsm-storage-remap.md)

## Problem

TSMC is now stored as NYSE ADR **TSM**. Code and live rows were remapped; Tailscale / Schwab / Winston Unit Test (WUT) UI were **not** click-verified this session. Cached CSS or a leftover TSMC label would hide a miss.

## Scope

Operator observation only — no code unless a screen still says TSMC on a live book.

1. Hard-refresh `https://sawtooth-ai.tail944ffb.ts.net/wv2/operations` (`Ctrl+Shift+R`).
2. Schwab research: TSMC empty / not a US listing; **TSM** is Taiwan Semiconductor.
3. Paper Operational Portfolio Blue `#381`: open short **TSM** 6 @ 418.13 (lot **#587**). Shell `journals 381` — journal **940** executed on TSM.
4. Signal inspect: `/wv2/operations/signal_inspect?portfolio_id=381&symbol=TSM&as_of=2026-08-18` — Tuesday close ~413.41. `symbol=TSMC` should not resolve a live book.
5. WUT `https://sawtooth-ai.tail944ffb.ts.net/wut/portfolios/7` Books show **TSM**.

## Acceptance

- [ ] Blue `#381` blotter and journal 940 say **TSM**, not TSMC
- [ ] Inspect 2026-08-18 loads TSM NYSE-dollar bars
- [ ] WUT lab Blue seed/book is TSM
- [ ] If any live surface still says TSMC, file/update an issue — do not restyle blindly

## Non-goals

- Confirming a second TSM enter to “test”
- Deleting the predecessor TSMC parquet folder (separate ticket)
