# Ticket: DM parquet pull for Quiver Tracking names

**Status:** Done  

**Priority:** P1  
**Date:** 2026-08-21  
**Monoliths:** winston_v2 (Wv2), data_manager (DM)  
**Depends on:** [`2026-08-21-wv2-quiver-pdf-ingest-and-gap-tasks.md`](2026-08-21-wv2-quiver-pdf-ingest-and-gap-tasks.md)  
**See:** analysis [`2026-08-21-quiver-quant-vs-api-vs-dm.md`](../../analysis/2026-08-21-quiver-quant-vs-api-vs-dm.md)

## Problem

Tracking prices and equity must come from **Winston EOD Standard parquet** (EODHD via DM), not from Quiver. Gap task `dm_pull` should reuse consumer Symbol Demand (`POST /api/v1/triggers/request_consumer_sync`), same idea as WUT `QuiverLab::Snapshot#enqueue_symbol_pull`.

Do **not** add a Quiver API call for this.

## Scope

1. From a tracking ingest (or explicit “pull missing”), collect target tickers.
2. Wv2 requests DM sync for those symbols (`consumer: wv2`).
3. Tracking desk shows DataCoverage / missing-bar per name (ready / pending / failed).
4. Daily Analysis parquet-missing path must still **exclude** tracking OPs so Congress names cannot stall TF.
5. Optional footnote only: `GET /internal/alt/quiver/books/quiver_congress_long_short` vs PDF — never blocks `dm_pull`.

## Acceptance

- [x] Spec: tracking ingest enqueues DM sync for new tickers
- [x] Spec: DA `symbols_for_daily_analysis` still excludes tracking fingerprints
- [x] Desk shows coverage after DM notify / refresh
- [x] `QUIVER_API_KEY` remains DM-only

## Non-goals

- Baking holdings into parquet
- Insider API upgrade
- Mount `quiver.env` (separate P2 ticket)
