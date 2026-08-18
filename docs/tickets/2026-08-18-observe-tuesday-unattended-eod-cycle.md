# Ticket: Observe Tuesday unattended EOD cycle (DM 15:30 MT → DAR 16:30 MT)

**Status:** Proposed  
**Priority:** P1  
**Date:** 2026-08-18  
**Related:** [`2026-08-18-after-close-eod-session-contract.md`](2026-08-18-after-close-eod-session-contract.md); session [`docs/session-reports/2026-08-18-1000-after-close-eod-session-contract.md`](../session-reports/2026-08-18-1000-after-close-eod-session-contract.md)

## Problem

The after-close session contract is coded and Monday was catch-up scored by hand. The unattended Tuesday 2026-08-18 chain has not been observed. If `CompletedNySession` or exact-bar readiness fails in cron, tonight’s Daily Analysis Report (DAR) will skip Active books or look empty again.

## Acceptance

- [ ] After 15:30 America/Denver: Active parquet / `DataCoverage.latest` = **2026-08-18** (sample NVDA, OIH, ROKU, RSPN)
- [ ] After 16:30 America/Denver: `DailyAnalysisJob` evaluates 2026-08-18; appendix OHLCV ≠ Monday 08/17
- [ ] New tasks (if any) have `session_bar_date=2026-08-18`
- [ ] If latest is still 2026-08-17 after 15:30, open the EODHD lag ticket instead of re-using yesterday’s window

## Related

- Issue: [`docs/issues/2026-08-18-dm-yesterday-window-misses-after-close-session.md`](../issues/2026-08-18-dm-yesterday-window-misses-after-close-session.md)
- Sibling: [`2026-08-18-eodhd-lag-retry-after-close.md`](2026-08-18-eodhd-lag-retry-after-close.md)
