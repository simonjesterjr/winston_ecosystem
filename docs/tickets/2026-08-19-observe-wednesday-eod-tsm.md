# Ticket: Observe Wednesday unattended EOD — DAR must say TSM

**Status:** Proposed  
**Priority:** P1  
**Date:** 2026-08-19  
**Related:** session [`docs/session-reports/2026-08-19-1304-tsmc-to-tsm-storage-remap.md`](../session-reports/2026-08-19-1304-tsmc-to-tsm-storage-remap.md); Tuesday observe (Done) [`archive/2026-08-18-observe-tuesday-unattended-eod-cycle.md`](archive/2026-08-18-observe-tuesday-unattended-eod-cycle.md)

## Problem

TSMC → TSM storage remap landed mid-day 2026-08-19. Tuesday’s unattended cycle was still labeled TSMC when it minted. Tonight’s data_manager (DM) 15:30 Mountain → Daily Analysis Report (DAR) 16:30 Mountain chain is the first unattended run on the new ticker. If consumer Markets or coverage paths still point at TSMC, Blue will skip as `missing_data` or the desk will see the nickname again.

## Acceptance

- [ ] After 15:30 America/Denver: TSM `DataCoverage.latest` = **2026-08-19** (not TSMC)
- [ ] After 16:30 America/Denver: Daily Analysis evaluates 2026-08-19; Blue `#381` books include **TSM**
- [ ] New Blue tasks (if any) name **TSM**, never TSMC
- [ ] Signal inspect / ops shell for any Wednesday Blue setup uses TSM
- [ ] If TSM latest is still 2026-08-18 after 15:30, open the EODHD lag ticket — do not fetch under TSMC

## Related

- Remap walkthrough: [`2026-08-19-tsm-remap-operator-clickthrough.md`](2026-08-19-tsm-remap-operator-clickthrough.md)
- Lag sibling: [`2026-08-18-eodhd-lag-retry-after-close.md`](2026-08-18-eodhd-lag-retry-after-close.md)
