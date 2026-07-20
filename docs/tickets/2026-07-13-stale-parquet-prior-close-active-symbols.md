# Ticket: Stale DM parquet last-dates for some Active symbols

**Status:** Proposed  
**Priority:** unset
**Context:** Session `docs/session-reports/2026-07-13-1307-intraday-market-radar.md`. Live radar uses DM parquet for prior close + `atr_17`; smoke showed mixed last bars (`2026-07-02` vs `2026-07-10`) on Active Books.

## Problem

Intraday ATR multiples are only as good as the EOD boundary. If parquet for a symbol stops updating, live price vs a week-old close produces false breaches and misdirected attention.

## Acceptance criteria

- [ ] Inventory Active Book symbols where parquet max(date) is older than last expected trading day
- [ ] Root-cause: demand discovery, DM sync skip, symbol rename, or coverage gap
- [ ] Repair path (re-acquire / reconcile) for lagging symbols
- [ ] Optional: radar response includes `previous_close_date` age warning when bar is >1 session old

## Related

- Session: [`docs/session-reports/2026-07-13-1307-intraday-market-radar.md`](../session-reports/2026-07-13-1307-intraday-market-radar.md)
- DM principles: `ecosystem/principles/02_data_storage_and_reconciliation.md`
- Code: `winston_v2/app/services/market_snapshot_service.rb` (`eod_bar`)
