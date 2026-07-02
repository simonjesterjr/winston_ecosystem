# ADR-003: DM Owns Derivative Calculation

**Status:** Accepted
**Date:** 2026-06-12
**Deciders:** Architecture (seeded from principles/01_core_principles.md §5, principles/02)
**Builds on:** ADR-002
**Domain context:** `docs/business-context/data-invariant-and-derivatives.md`

## Context

Trading strategies require running indicators (ATR-17, SMA/EMA/WMA at supported periods) computed over the full price history. Both DM and WUT have indicator calculation capability. We needed a single owner to prevent drift between monoliths.

Alternatives:

- **Approach A: Each consumer calculates** — WUT and Wv2 compute indicators locally from raw OHLCV
- **Approach B: DM calculates and bakes in** — derivatives are columns in Winston EOD Standard parquet
- **Approach C: Shared calculation library** — extract IndicatorCalculator to a gem both use

## Decision

We chose **Approach B: DM owns derivatives**.

DM calculates and writes into parquet on every acquire/update:

- **atr_17** — simple method, period 17, matching WUT's `calculate_atr` semantics
- **Moving averages** — the exact SMA/EMA/WMA periods currently used by WUT strategies (authoritative list from WUT `app/strategies/` and `indicator_calculator.rb`)

Consumers read precomputed columns. They do not recalculate ATR or MAs from raw OHLCV for ecosystem-standard data paths.

## Rationale

### Why not per-consumer calculation?

WUT and Wv2 would drift on edge cases (adjustments, partial history, period boundaries). Signal comparison between backtest (WUT) and live (Wv2) requires identical indicator values on identical data.

### Why not a shared gem?

Adds versioning and deployment coupling without solving the "who refreshes on new bars" question. DM already owns freshness; baking derivatives at write time is simpler.

### Why DM at write time?

- **Single source of truth** — one calculation per symbol update
- **Consumer simplicity** — load parquet, trust columns
- **Reconciliation visibility** — DataCoverage.indicators_present reflects what is in the file

## Consequences

### Positive

- WUT→Wv2 signal parity depends on shared parquet, not shared code paths
- DM reconciliation can verify indicator columns exist

### Negative

- Adding a new indicator period requires DM standardizer update + parquet schema bump
- WUT legacy local calculation paths must be deprecated for new work

### Risks mitigated

- Indicator drift → single writer (DM)
- Stale indicators → DM recomputes on every standardize run over full/trailing history