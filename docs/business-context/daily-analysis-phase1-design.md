# Daily Analysis Phase 1 — Design Decisions (Grill Session 2026-06-30)

**Type:** Domain + implementation design (precedes Phase 1 build)
**Plan:** `plans/winston-mcp-next-steps.md` Phase 1
**Tasks:** `plans/winston-mcp-next-steps.md.tasks.json` (tasks 1–4)
**Status:** Accepted via `/grill-with-docs`

## Summary

Replace Wv2 `DemoSignalCreator` with a full port of WUT's `SignalEvaluation` + `ReportBuilder` + `TaskGenerator`, adapted for DM-owned data and Wv2's Portfolio/TradingStrategy model.

## Data model

| Decision | Choice |
|----------|--------|
| Who acquires market data | **DM only** (EODHD). Symbol demand deduped across WUT + Wv2 portfolios. |
| Consumer read path | **DM parquet** (not WUT `Operations::DataSync` / Yahoo / activities) |
| When DM fetch triggers | **Lazy on analysis** — missing parquet → request DM, no eager sync on Book create |
| Missing symbol | **Skip entire portfolio** (`missing_data`) |
| Missing `atr_17` column | Same as missing data — **skip portfolio** (ADR-003) |
| Cromwell visibility | **Explicit skip entries** — never omit silently |

### Skip reasons (Cromwell payload)

```json
{
  "name": "My Trend Portfolio",
  "status": "skipped",
  "reason": "missing_data | no_strategy | unsupported_strategy",
  "symbols": ["MSFT"],
  "detail": "optional human-readable"
}
```

## Evaluation model

| Decision | Choice |
|----------|--------|
| Config source | **TradingStrategy only** (Phase 1). No linked TS → `no_strategy` skip. |
| Pipeline scope | **Full WUT pipeline** — SignalEvaluation + ReportBuilder + TaskGenerator |
| Idempotency | Per **(portfolio, report_date)** — re-run after data lands produces signals once |
| Unknown strategy class | **Skip portfolio** (`unsupported_strategy`); port classes needed for parity test |

## Strategy registry (Phase 1)

- Port WUT strategy files required for parity test config (e.g. `Breakout20DayStrategy`, `VolatilityExitStrategy`)
- Do not copy entire WUT tree in one PR
- Expand registry incrementally as imports demand

## Verification

| Tier | Method |
|------|--------|
| **CI** | Pinned parquet fixture + fixed date; assert WUT vs Wv2 signal/journal parity |
| **Smoke** | Compose E2E: WUT backtest → export → Wv2 import → DM sync → evaluate → compare |

## Implementation notes

- New service: `ParquetLookbackLoader` (symbol, date, N bars + `atr_17` from DM parquet)
- Replace `DemoSignalCreator` entirely — no second demo layer
- Split ported files to 65-line rule
- WUT `Operations::DataSync` remains legacy; do not port to Wv2

## Open (Phase 2+)

- Auto-requeue analysis when DM `data_ready` webhook fires
- Full Cromwell notification schema in `interfaces/`
- WUT daily ops migration off Yahoo DataSync to DM parquet read path