# Ticket: Re-bake remaining DM parquet for MACD 12/26/9

**Status:** Proposed
**Priority:** P2
**Date:** 2026-09-10
**Mode:** contractor
**Graph nodes:** data_manager
**Monolith:** data_manager
**Origin:** session `docs/session-reports/2026-09-10-1121-macd-and-walnut-slate.md`

## Problem

Winston EOD Standard v0.2 requires `macd_line`, `macd_signal`, `macd_histogram` (12/26/9). `ParquetStandardizer` always bakes them on acquire. Existing files stay v0.1 until re-baked.

Only **GOOGL** was run through `rake data:restandardize[GOOGL]` (1801 bars, 1768 with MACD). Other symbols still omit the columns. Signal Inspect can compute MACD from a 90-bar window as fallback (warm-up nils at the left of the pane). The bars table MACD column and any future consumer that trusts parquet will be empty.

## Work

1. Run `bin/rails data:restandardize[SYMBOL]` for Active Operational Portfolio Book symbols (or a full corpus pass if cheap — GOOGL 1801 bars was seconds).
2. Reconcile so `DataCoverage.indicators_present` lists `macd_*`.
3. Spot-check one non-GOOGL inspect (e.g. Walnut `DBC`) that `macd_*` is on the payload bars, not only computed overlay.

Service: `ParquetRestandardizeService` / `rake data:restandardize[SYMBOL]`. Split-adjust is idempotent on already-adjusted files.

## Acceptance

- [ ] Active OP Book symbols have `macd_line` / `macd_signal` / `macd_histogram` in parquet (nil only in warm-up).
- [ ] Reconciliation `indicators_present` includes `macd_*`.
- [ ] Inspect table shows MACD hist from parquet on a non-GOOGL name.

## Out of scope

- HMM states in parquet
- RSI as a required Standard column
- Changing `Macd1269Strategy` recipes

## Related

- `ecosystem/interfaces/winston-eod-parquet-standard.md` (v0.2)
- `data_manager/app/services/parquet_restandardize_service.rb`
- Inspect fallback: `winston_v2/app/services/operations/signal_inspect_overlay_builder.rb`
