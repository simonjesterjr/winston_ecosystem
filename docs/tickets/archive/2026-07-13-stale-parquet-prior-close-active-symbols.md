# Ticket: Stale DM parquet last-dates for some Active symbols

**Status:** Done  
**Priority:** P1  
**Date:** 2026-07-13  
**Closed:** 2026-09-08  
**Context:** Session `docs/session-reports/2026-07-13-1307-intraday-market-radar.md`. Live radar uses DM parquet for prior close + `atr_17`; smoke showed mixed last bars (`2026-07-02` vs `2026-07-10`) on Active Books.

## Problem

Intraday Average True Range (ATR) multiples are only as good as the end-of-day (EOD) boundary. If parquet for a symbol stops updating, live price vs a week-old close produces false breaches and misdirected attention.

## Acceptance criteria

- [x] Inventory Active Book symbols where parquet max(date) is older than last expected trading day
- [x] Root-cause: demand discovery, DM sync skip, symbol rename, or coverage gap
- [x] Repair path (re-acquire / reconcile) for lagging symbols
- [x] Optional: radar response includes `previous_close_date` age warning when bar is >1 session old

## Inventory (2026-09-08, after NY close)

Completed New York session = **2026-09-08**. Nine Active Operational Portfolios, **94** unique Active Book symbols.

| Bucket | Count | Last bar |
|--------|------:|----------|
| Active Book parquet on disk | 93 | 2026-09-08 |
| Missing parquet folder | 1 | `BRK.B` (alias of `BRK-B`, which is 2026-09-08) |
| data_manager (DM) demand (Winston Unit Test (WUT) + Winston v2 (Wv2) `/internal/active_markets`) | 113 | 2026-09-08 |
| Demand with no coverage | 3 | `SMOKE1`, `SMOKE2`, `SMOKE3` (inactive smoke-test books, not EODHD names) |
| PostgreSQL `DataCoverage.latest` vs on-disk parquet | 0 mismatches | — |

No Active Book parquet was older than the completed session. The July 13 mixed-date failure is gone on the live tree.

## Root cause

**July 13 mixed last bars (`2026-07-02` vs `2026-07-10`)** were the same family as the later after-close miss: DM requested through `Date.current - 1`, some symbols skipped when End of Day Historical Data (EODHD) had no new print, and there was no session-coverage retry. Closed by:

- Architecture Decision Record (ADR) 012 — `CompletedNySession` + exact-bar readiness (`2026-08-18-after-close-eod-session-contract.md`)
- `SessionCoverageRetryJob` — probe EODHD for the print, then rewrite (`2026-08-18-eodhd-lag-retry-after-close.md`)
- `TickerRemap` — `RGI`→`RSPN`, `TSMC`→`TSM`, `BRK.B`→`BRK-B` (storage folder identity)

**2026-09-08 leftovers (not stale bars):**

1. **Symbol alias on an Active book.** Winston Quiver (WQ) OP#1372 still has both `BRK.B` (executed journal #1331) and `BRK-B`. Parquet is stored only as `BRK-B`. Radar used to treat them as two symbols; Yahoo fetch on `BRK.B` could miss. Do **not** delete the `BRK.B` book — it owns a live journal. Radar now canonicalizes via `TickerRemap`.
2. **Demand includes inactive smoke books.** `SMOKE1/2/3` on inactive test Operational Portfolios are advertised on `/internal/active_markets` (all portfolios, not Active-only). DM tries to acquire them, EODHD returns nothing. Not an Active Book freshness bug; leave as residual demand noise.

## Repair path

Lagging **real** demand symbols (not smoke aliases):

```bash
# Status vs completed NY session
./bin/compose exec -T data_manager bin/rails runner '
session = CompletedNySession.date
stale = SessionCoverage.stale_among(EcosystemDataSyncService.demand_symbols, session)
puts "session=#{session} stale=#{stale.size} #{stale.join(",")}"
'

# Re-acquire + reconcile one or more
./bin/compose exec -T data_manager bin/rails dm:symbol_registry:acquire_symbols
# or SYMBOLS=NVDA,OIH
./bin/compose exec -T data_manager bin/rails data:reconcile
```

Automatic path after 15:30 America/Denver: `DailyDataOrchestratorJob` → `SessionCoverageRetryJob` (stops at 17:00 MT; probes the print before rewrite).

Wv2 consumers can also `DmParquetIngester.request_dm_data(symbols)` (used by the Daily Analysis session gate).

## Radar warning (landed 2026-09-08)

`MarketSnapshotService`:

- Canonicalizes Active Book symbols (`BRK.B` → `BRK-B`) before parquet lookup and live quote
- Each row: `previous_close_date`, `previous_close_sessions_behind`, `previous_close_stale` (true when weekday sessions behind > 1)
- Summary: `expected_previous_close_date`, `stale_previous_close`, `stale_previous_close_symbols`
- Cromwell skill annotates stale movers so a week-old close is not treated as a real ATR breach

Live smoke: `evaluate_one("BRK.B")` → `BRK-B`, `previous_close_date=2026-09-08`, `previous_close_stale=false`. Specs: 12 examples, 0 failures.

## Related

- Session: [`docs/session-reports/2026-07-13-1307-intraday-market-radar.md`](../../session-reports/2026-07-13-1307-intraday-market-radar.md)
- DM principles: `ecosystem/principles/02_data_storage_and_reconciliation.md`
- Code: `winston_v2/app/services/market_snapshot_service.rb` (`eod_bar`)
- Cousin: [`../2026-08-18-eodhd-lag-retry-after-close.md`](../2026-08-18-eodhd-lag-retry-after-close.md)
