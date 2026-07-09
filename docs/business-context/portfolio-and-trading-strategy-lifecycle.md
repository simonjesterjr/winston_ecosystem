# Portfolio and TradingStrategy Lifecycle

**Type:** Domain explainer
**Glossary:** `CONTEXT.md` — Portfolio, TradingStrategy, Book, Journal

## Separation of concerns

| Entity | Owns | Does not own |
|--------|------|--------------|
| **Portfolio** | Capital (CashEvents), market list (Books), active/inactive state, live positions | Methodology rules (those live in TradingStrategy) |
| **TradingStrategy** | Entry/exit strategy names, risk evaluation, ATR multipliers, pyramid rules | Capital, which markets are traded |
| **Book** | Portfolio's exposure slot for one Market | Strategy logic |

This **loose coupling** lets one TradingStrategy apply to multiple Portfolios and lets Portfolios swap strategies without recreating market allocations.

## Lifecycle states (Wv2)

```
[imported/inactive] → activate → [active, evaluated daily] → deactivate → [inactive]
```

- **Inactive:** exists in PG, excluded from Daily Analysis cron
- **Active:** included in `DailyAnalysisJob` and Cromwell notifications
- **Evaluate:** one-shot analysis (may auto-activate if configured)

## TradingStrategy lifecycle

```
[WUT vetted] → export JSON → [Wv2 imported] → apply to Portfolio(s)
                                    ↓
                            update-by-name on re-import
```

Strategies can be activated/deactivated independently of Portfolios (see `wv2:trading_strategies:*` rake tasks).

## Daily analysis outputs (active Portfolio)

When Daily Analysis runs for an active Portfolio:

1. **Signals** — entry, exit, pyramid opportunities evaluated against DM parquet data
2. **Journals** — proposed trade actions with flow/mtm/risk sizing (capital_base from CashEvents)
3. **Operations tasks** — human action items
4. **Cromwell notification** — structured JSON with portfolios, actions, journals summary

Confirmation flow (future MCP tools): principal confirms journals → capital_base updates → next analysis respects new positions.

## WUT lab lifecycle (reference)

1. Create backtest run with strategy params and markets **or** run **Portfolio Signal Optimization** / `portfolios:vet_trend`
2. After the **validation** PortfolioBacktestRun completes, WUT auto-upserts a fingerprinted first-class **TradingStrategy** and a **TradingStrategy Selection** (outcomes + portfolio link). Manual promote from completed runs still works.
3. Fingerprint = full run methodology + date range + constraints; excludes portfolio name, membership (Books), and initial capital. Same fingerprint across portfolios increments selection counts for regime insight.
4. Export JSON when satisfied (`/trading_strategies`, `wut:strategies:export_config`, or portfolio export from vet)
5. Hand off to Wv2 (see `wut-to-wv2-handoff.md`)

Backfill existing validation runs: `bin/rails trading_strategies:capture_validation_runs` (optional `PBR_IDS=`, `PORTFOLIO=`, `DRY_RUN=1`).

WUT remains the **mature reference** for how these services work (`winston_unit_test/docs/architecture.md`).