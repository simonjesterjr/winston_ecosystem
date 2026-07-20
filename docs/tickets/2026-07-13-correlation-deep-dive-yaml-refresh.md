# Ticket: Refresh process for correlation deep-dive YAML

**Status:** Proposed  
**Priority:** P3

**Date:** 2026-07-13  

**Session:** [`docs/session-reports/2026-07-13-1034-wut-portfolio-correlation-dashboard.md`](../session-reports/2026-07-13-1034-wut-portfolio-correlation-dashboard.md)

## Problem

Curated deep dives (`winston_unit_test/config/correlation_deep_dives/*.yml`) embed reference PCS, max|r|, rating rationale, and seed narrative. After a membership rebuild, daily score regime shift, or methodology_version bump, narratives can go stale relative to the live dashboard.

## Scope

1. Define when to re-author (checklist): membership change, methodology_version change, rating class change, archive/unarchive.  
2. Optional: short note in deep-dive partial or primer pointing operators at refresh ownership.  
3. After next color rebuild, update affected YAML (especially Orange/White if ever rebuilt; new cohorts after vet).  
4. Keep as-of dates and “curated not live” labeling honest.

## Acceptance

- [ ] Refresh checklist documented (ticket body or short analysis note is enough)  
- [ ] Next membership/methodology change updates corresponding YAML in the same PR or a linked follow-up  
- [ ] No silent contradiction with live rating (e.g. sidecar “strong” vs live “Good”) without narrative callout  

## Related

- Loader: `PortfolioCorrelationDeepDive`  
- Content: `config/correlation_deep_dives/`  
- Session report §9 risks on sidecar vs live rating  
