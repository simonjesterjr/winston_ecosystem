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

Authoritative detail: **`wv2-operational-portfolio-lifecycle.md`** and **ADR-006**.

```
[imported/inactive] → Active (attention) → Engaged (any Journal) → Closed
                         │                      │
                         │                 shape change → successor A′
                         │                 capital → CashEvent
                         └─ Capital Activation ($X real) → new OP series
```

- **Inactive:** exists in PG, excluded from Daily Analysis
- **Active:** attention priority — Daily Analysis + human task surface (mutex by seed_name / Books)
- **Engaged:** any Journal; Books/TS frozen until close or successor rebalance
- **Closed:** signals stop; history kept
- **Execution Mode** `paper` | `real` independent of Active and export_kind

## TradingStrategy lifecycle

```
[WUT fingerprint capture] → export JSON → [Wv2 import: lineage by fingerprint]
                                    ↓
              same fingerprint (pre-engagement) update | new fingerprint auto-fork
```

Lab identity = fingerprint; ops display names use seed + short suffix. See `wut-to-wv2-handoff.md`.

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
5. Hand off to Wv2 (see `wut-to-wv2-handoff.md`); ops lifecycle after import: `wv2-operational-portfolio-lifecycle.md`

Backfill existing validation runs: `bin/rails trading_strategies:capture_validation_runs` (optional `PBR_IDS=`, `PORTFOLIO=`, `DRY_RUN=1`).

WUT remains the **mature reference** for lab services (`winston_unit_test/docs/architecture.md`). Wv2 owns operational engagement hygiene (ADR-006).