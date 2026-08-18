# Ticket: After-close EOD session contract (DM to-date + Wv2 exact bar)

**Status:** Done  
**Priority:** P0  
**Date:** 2026-08-18  
**Issue:** [`docs/issues/2026-08-18-dm-yesterday-window-misses-after-close-session.md`](../issues/2026-08-18-dm-yesterday-window-misses-after-close-session.md)

## Problem

Monday 2026-08-17 DAR minted 0 tasks after the session-bar skip. Root cause: DM after-close sync used `Date.current - 1` (Sunday → Friday last bar). Wv2 on-or-before readiness hid the gap.

## Done

- [x] `CompletedNySession` (ET, 16:00 close) in DM sync / acquire / recent
- [x] Wv2 `session_bar_for` + exact `data_ready?`; eval uses exact bar
- [x] Specs (DM clocks, missing session ≠ ready, TaskGenerator skip stays)
- [x] Data-invariant: latest = completed NY session
- [x] Pull Active books through 2026-08-17; re-run DAR (Telegram off) → 12 Monday tasks

## Tonight

See: [`2026-08-18-observe-tuesday-unattended-eod-cycle.md`](2026-08-18-observe-tuesday-unattended-eod-cycle.md). If parquet still ends Monday after 15:30, [`2026-08-18-eodhd-lag-retry-after-close.md`](2026-08-18-eodhd-lag-retry-after-close.md).
