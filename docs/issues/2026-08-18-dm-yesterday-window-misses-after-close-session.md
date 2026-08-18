---
id: ISSUE-20260818-dm-yesterday-window-misses-after-close-session
title: After-close DM pull used Date.current-1 so Monday EOD never landed; DAR looked empty
status: resolved
type: bug
priority: high
created: 2026-08-18
updated: 2026-08-18
labels: [dm, wv2, dar, eod, session-bar]
related:
  - 2026-07-28-dar-skip-when-no-session-bar
---

# After-close DM pull used Date.current-1 so Monday EOD never landed; DAR looked empty

**Status banner:** Fixed — `CompletedNySession` + exact session-bar readiness; Monday 2026-08-17 re-scored (12 tasks, Telegram off)

## Summary

The session-bar skip (do not mint when `bar_date ≠ report_date`) was correct. Combined with data_manager (DM) requesting **through yesterday**, the Monday 15:30 Mountain sync stored Friday 2026-08-14, Winston v2 (Wv2) reused that bar via on-or-before, then refused to mint. The Daily Analysis Report (DAR) said “evaluated, 0 actions, hold.”

## Current behavior (before fix)

- `EcosystemDataSyncService` / `SymbolRegistryAcquirer`: `to = Date.current - 1`
- `ParquetLookbackLoader.data_ready?` / eval bar: on-or-before
- Monday DAR: 0 tasks, 0 skipped

## Expected behavior

- After NY close on a trading day, DM `to` = that Eastern session date
- Before close / weekend: last completed weekday
- Eval and readiness require an **exact** session row; missing row is `missing_data`, not a quiet hold

## Evidence

| Evidence | Source | What it establishes |
|---|---|---|
| Parquet latest 2026-08-14 after Monday 15:30 MT sync | DM coverage + bars.json | Window ended Sunday |
| Re-eval 2026-08-17 emitted 15 signals all `bar_date=2026-08-14` | SignalEvaluation runner | On-or-before reuse |
| 0 tasks report_date 2026-08-17 | Wv2 DB + DAR | Session skip hid the reuse |
| After pull `to=2026-08-17`, 12 Monday tasks | Catch-up DAR | Real Monday session had setups |

## Resolution

- DM `CompletedNySession` (America/New_York, 16:00 ET close)
- Wv2 `session_bar_for` + `data_ready?` exact date
- SignalEvaluation uses exact session bar
- Catch-up DAR 2026-08-17: 12 pending, `session_bar_date=2026-08-17`, Telegram skipped
