# Ticket: Port WUT daily analysis pipeline to Wv2 (Phase 1)

**Status:** Done (Phase 1 tasks 1–4)
**Plan:** `plans/winston-mcp-next-steps.md` tasks 1–4
**Design:** `docs/business-context/daily-analysis-phase1-design.md`

## Scope

Replace `DemoSignalCreator` with ported `Operations::SignalEvaluation`, `ReportBuilder`, `TaskGenerator` adapted for Wv2.

## Acceptance criteria

- [x] `ParquetLookbackLoader` reads OHLCV + `atr_17` from DM parquet
- [x] Lazy DM fetch on missing parquet; portfolio skip with `missing_data` if any Book incomplete
- [x] Portfolio skip with `no_strategy`, `unsupported_strategy` per design doc
- [x] Idempotent per (portfolio, report_date)
- [x] Cromwell payload includes explicit `skipped` portfolios with reason + symbols
- [x] Strategy classes ported for parity test config (Breakout20 + VolatilityExit minimum)
- [x] CI fixture test: WUT vs Wv2 signal parity on pinned parquet (`bin/verify-daily-analysis-parity`)
- [x] Compose smoke: `bin/verify-daily-analysis-parity --compose` (wraps `bin/test-daily-pipeline --offline`)

## Out of scope (Phase 1)

- WUT migration off Yahoo DataSync
- DM auto-requeue on `data_ready`
- Full Cromwell webhook schema (Phase 2)