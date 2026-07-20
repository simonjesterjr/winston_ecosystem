# Ticket: Portfolio trading-strategy evaluation framework (priority)

**Status:** In progress (~90% — gates + export_kind + ranking fallback done; Blue post-mortem open)

**Priority:** P0 — blocks Wv2 trade-ready handoff for trend portfolios

**Date:** 2026-07-07

**Last updated:** 2026-07-08 (viability gates + export_kind + null-Sharpe fallback)

**Context:** Blue vet (`portfolios:vet_trend`) completed with catastrophic metrics across all six entry strategies. The current “evaluate TS for a portfolio” path is too narrow and undocumented for production decisions.

Session: [`2026-07-06-2020-portfolio-overlap-pipeline`](../session-reports/2026-07-06-2020-portfolio-overlap-pipeline.md)

## Problem

We do not have an ecosystem-approved answer to:

1. **What comprises a TradingStrategy** for trend portfolios (entry, confirmational, exit, risk evaluation, pyramid, stops).
2. **What defaults** should `PortfolioTrendVetter` / `PortfolioSignalOptimizer` use (capital, risk %, ranking metric, screening, date range).
3. **How to optimize** — which dimensions are swept vs fixed; exit strategy grid; confirmational entries; per-market overrides.
4. **What “viable” means** — minimum return, max drawdown, Sharpe, trade count, before export to Wv2.
5. **Why Blue vet failed** — e.g. `practical_sharpe_ratio` winner with all `null` Sharpes; only breakout entries; single `VolatilityExitStrategy`; no regime filter.

## Existing references (incomplete for this use case)

| Doc / code | What it covers | Gap |
|------------|----------------|-----|
| `docs/business-context/portfolio-and-trading-strategy-lifecycle.md` | Portfolio vs TradingStrategy separation, WUT→Wv2 lifecycle | No optimization defaults or viability thresholds |
| `docs/business-context/wut-to-wv2-handoff.md` | JSON export/import path | Assumes vet already satisfied |
| `portfolio_configs/README.md` | JSON shape, rake commands | No strategy selection doctrine |
| `PortfolioTrendVetter` | 6 hardcoded entry classes + `VolatilityExitStrategy`, full 5yr, `default_base_config` | Not configurable via rake; no exit grid |
| `PortfolioSignalOptimization` UI | `ranking_metric`, screening %, strategy multi-select | Not wired into `vet_trend` rake |
| `ecosystem/CONTEXT.md` | Daily analysis requires linked TradingStrategy | No lab vetting contract |

### First-pass `PortfolioTrendVetter` defaults (implemented — see analysis doc)

- `initial_capital`: **10_000** (`FIRST_PASS_BASE_CONFIG`)
- `risk_percentage`: 0.02 (static)
- `ranking_metric`: `practical_sharpe_ratio`
- Entry grid: 6 breakout classes (unchanged list)
- Exit grid: **paired opposite breakout** + **VolatilityExitStrategy** (12 combos via `paired_opposite_exit`)
- Position rules: 5 pyramid/market, 12 positions/portfolio, 4 markets, 13th-signal swap (`PositionSwapEvaluator`)
- Stops: ATR (`atr_multiplier: 2`), trail `move_to_last_entry`
- Screening: 100% date range (no subset) in vet rake

Canonical reference: [`docs/analysis/portfolio-trading-strategy-evaluation.md`](../analysis/portfolio-trading-strategy-evaluation.md)

## Progress (2026-07-08)

| Deliverable | Status |
|-------------|--------|
| Analysis doc (first-pass grid + fixed components) | **Done** |
| Viability gates doc (placeholders) | **Done** (`trade-ready-viability-gates.md`) |
| CONTEXT.md glossary (Trade-Ready / Observation / etc.) | **Done** |
| WUT: 6×2 exit grid (`paired_opposite_exit`) | **Done** |
| WUT: first-pass base config in `PortfolioTrendVetter` | **Done** |
| WUT: max 4 markets + 12-position swap logic | **Done** |
| WUT: specs for vetter / optimizer / swap / gates | **Done** (gates + null-Sharpe specs green 2026-07-08) |
| WUT: `export_kind` enforcement (trade_ready vs observation) | **Done** (`TradeReadyViabilityGates` + export JSON) |
| WUT: viability gate check on export | **Done** |
| WUT: ranking fallback when Sharpe is null | **Done** (falls back to `total_return`) |
| WUT: `vet_trend` `RANKING_METRIC` env | **Done** |
| Re-vet Red with new doctrine | **Done** (PBR 25 → observation; DD 64% > 50%) |
| Plan Phase 7 write-up | **Done** |
| Blue vet post-mortem template | **Not done** (ticket revisit-blue) |
| Apply `export_kind` to existing Red/Blue JSON | **Done** (both observation) |

## Proposed deliverables

### 1. Analysis doc (ecosystem)

`docs/analysis/portfolio-trading-strategy-evaluation.md` — canonical reference:

- Strategy composition checklist (aligned with Wv2 `TradingStrategy` model and `StrategyRegistry`).
- Default base config with rationale (capital, risk, position limits, ATR multipliers).
- Optimization dimensions matrix: what `PortfolioSignalOptimizer` already supports vs gaps.
- Viability gates for export (numeric thresholds + “must beat X benchmark” optional).
- Blue vet post-mortem template (membership vs strategy vs data).

### 2. WUT implementation (follow-on PRs)

- Extend `portfolios:vet_trend` to accept env/config file for strategy grid, ranking metric, screening.
- Fix ranking when `practical_sharpe_ratio` is null (fallback metric or compute fix).
- Optional: exit strategy grid; confirmational entries per `PortfolioSignalOptimization` UI.
- Document rake + UI paths in `winston_unit_test/docs/` or `portfolio_configs/README.md`.

### 3. Plan update

Add Phase 7 to `portfolio-overlap-rebuild.md`: “Strategy evaluation doctrine” — blocks Wv2 import for Red/Blue/Orange/White until passed.

## Acceptance

- Analysis doc reviewed and linked from plan + handoff doc.
- Agreed viability thresholds written (even if conservative placeholders).
- At least one re-vet of Blue (or Red) using revised doctrine shows whether membership or strategy was the dominant failure mode.
- `portfolios:vet_trend` documents env vars for ranking metric and strategy selection.

## Out of scope (separate tickets)

- Wv2 paper-trading execution gaps
- LLM-suggested strategy tweaks (`winston-plus-llm.md`)

## Related

- Plan task #5 (priority)
- Tickets: Blue revisit, Red vet, Orange/White build