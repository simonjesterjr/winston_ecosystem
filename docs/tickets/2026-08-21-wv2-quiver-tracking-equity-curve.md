# Ticket: Real equity curve on Quiver Tracking desk

**Status:** Proposed  
**Priority:** P2  
**Date:** 2026-08-21  
**Monoliths:** winston_v2 (Wv2)  
**See:** `app/views/quiver_tracking/home/index.html.erb` (placeholder); plan [`quiver-tracking-desk.md`](../../plans/quiver-tracking-desk.md); session [`docs/session-reports/2026-08-21-1629-quiver-tracking-wrap.md`](../session-reports/2026-08-21-1629-quiver-tracking-wrap.md)

## Problem

The tracking desk shows an equity **placeholder**. After paper confirms, operators need the same booked-capital / risk-equity story as ops shell (scoped to the tracking OP only), using DM parquet marks — not Quiver.

## Scope

1. Reuse Wv2 equity helpers (`PortfolioEquitySeries` / risk equity) for the tracking fingerprint only.
2. Panel: cash, risk equity, open lots; spark/series if cheap (ADR-005: do not block first paint).
3. Missing parquet → coverage panel / `dm_pull`, not a fake curve.

## Acceptance

- [ ] After a confirmed enter, equity is not the placeholder string
- [ ] TF ops-shell equity unchanged
- [ ] Request or service spec

## Non-goals

- Matching Quiver published CAGR
- Daily Analysis on the tracking OP
