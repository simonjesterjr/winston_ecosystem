---
id: ISSUE-20260822-friday-dar-hold-was-not-scored
title: Friday DAR published hold because session bars lagged; 15 recipe fires never tasked
status: in-progress
type: bug
priority: high
created: 2026-08-22
updated: 2026-08-22
labels: [dm, wv2, dar, eod, friday]
related:
  - 2026-08-18-dm-yesterday-window-misses-after-close-session
  - ADR-012
---

# Friday DAR published hold because session bars lagged; 15 recipe fires never tasked

**Status banner:** In progress — ADR-012 + session gate in tree; Friday 2026-08-21 catch-up minted 13 tasks onto Saturday desk (fill 2026-08-24), Friday DAR not replaced

## Summary

Friday 2026-08-21 Daily Analysis at 16:31 Mountain skipped all 7 Active paper Operational Portfolios as `missing_data`. The Daily Activity Report (DAR) said hold / 0 next actions and Telegram posted it. Saturday 08:00 weekend sync wrote Friday bars. A read-only re-scan fired 15 recipe signals. Desk pending remained 0.

## Problem statement

A clock-fired DAR presented an unscored Friday as a quiet day.

## Current behavior (before fix)

- DM 15:30 Friday did not leave exact 2026-08-21 bars
- Wv2 16:30 evaluated anyway, skipped every TF OP, wrote hold
- Weekend sync Saturday 08:00 filled Friday parquet; no catch-up analysis
- Ops shell Saturday: 0 pending, 0 drafts

## Expected behavior

ADR-012: wait for a Scored Session (until ~17:00 MT); never publish Hold for Not Scored; catch-up mints current-desk tasks without a replacement Friday DAR.

## Evidence

| Evidence | Source | What it establishes |
|---|---|---|
| generated_at 2026-08-21T22:31:01Z | `wv2-20260821.manifest.json` | EOD 4:31 PM MT, not 6:00 AM |
| All 7 OPs skipped missing_data | `wv2_20260821.json` | Nothing evaluated |
| WeekendDataSyncJob 2026-08-22T14:05Z | DM sidekiq | Friday bars landed Saturday ~8:05 AM MT |
| Dry SignalEvaluation 15 fires | rails runner 2026-08-22 | False hold |
| 0 pending / 0 drafts | Wv2 DB + `/operations/panels.json` | Desk empty |

## Resolution

- ADR-012 + business-context
- DM session-coverage retry; Wv2 session gate; not-scored copy; data_ready catch-up `mint_only`
- This session: Friday analysis mint-only, Telegram off, no new Friday DAR
