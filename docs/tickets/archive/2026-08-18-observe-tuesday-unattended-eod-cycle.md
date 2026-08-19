# Ticket: Observe Tuesday unattended EOD cycle (DM 15:30 MT → DAR 16:30 MT)

**Status:** Done  
**Priority:** P1  
**Date:** 2026-08-18  
**Related:** [`2026-08-18-after-close-eod-session-contract.md`](../2026-08-18-after-close-eod-session-contract.md); session [`docs/session-reports/2026-08-18-1000-after-close-eod-session-contract.md`](../../session-reports/2026-08-18-1000-after-close-eod-session-contract.md); close-out [`docs/session-reports/2026-08-19-1304-tsmc-to-tsm-storage-remap.md`](../../session-reports/2026-08-19-1304-tsmc-to-tsm-storage-remap.md)

## Problem

The after-close session contract is coded and Monday was catch-up scored by hand. The unattended Tuesday 2026-08-18 chain has not been observed. If `CompletedNySession` or exact-bar readiness fails in cron, tonight’s Daily Analysis Report (DAR) will skip Active books or look empty again.

## Acceptance

- [x] After 15:30 America/Denver: Active parquet / `DataCoverage.latest` = **2026-08-18** (sample NVDA, OIH, ROKU, RSPN) — confirmed 2026-08-19 morning; GOOGL/RXT also 2026-08-18
- [x] After 16:30 America/Denver: `DailyAnalysisJob` evaluates 2026-08-18; not Friday/Monday reuse — five paper enters minted (`report_date` 2026-08-18)
- [x] New tasks keyed to session 2026-08-18 (tasks 709–712, 716; journals 939–942, 946). `OperationsTask` has no `session_bar_date` column; `report_date` + journal `trade_date` = 2026-08-18
- [x] Latest was **not** stuck on 2026-08-17 — EODHD lag ticket not opened

Operator confirmed the five drafts 2026-08-19 (including Blue TSMC, later remapped to TSM).

## Related

- Issue: [`docs/issues/2026-08-18-dm-yesterday-window-misses-after-close-session.md`](../../issues/2026-08-18-dm-yesterday-window-misses-after-close-session.md)
- Sibling: [`2026-08-18-eodhd-lag-retry-after-close.md`](../2026-08-18-eodhd-lag-retry-after-close.md)
- Next observe: [`2026-08-19-observe-wednesday-eod-tsm.md`](../2026-08-19-observe-wednesday-eod-tsm.md)
