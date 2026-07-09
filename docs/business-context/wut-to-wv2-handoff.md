# WUT → Wv2 Handoff

**Type:** Domain workflow  
**Related ADR:** ADR-001, ADR-006  
**Operational guide:** `portfolio_configs/README.md` (sawtooth root)  
**Ops lifecycle after import:** `wv2-operational-portfolio-lifecycle.md`  
**Glossary:** Trade-Ready Portfolio, Observation Portfolio, Operational Portfolio, fingerprint, seed_name

## Purpose

Move a lab candidate from **WUT** to **Wv2** without re-entering methodology parameters. Handoff is file-based JSON through the shared `portfolio_configs/` volume.

**WUT** = candidate selection lab. **Wv2** = operational execution (paper or real tasking). Import is not Capital Activation and not live broker automation.

## The happy path

```
WUT Portfolio Signal Optimization / validation backtest
  → fingerprinted TradingStrategy + Selection (WUT)
  → viability gates → export_kind trade_ready | observation
  → export portfolio JSON (seed name, markets, nested trading_strategy, fingerprint, capital)
  → human edits JSON if needed (nano/vim — explicit supported path)
  → Wv2 import → Operational Portfolio + Books + CashEvent + TradingStrategy (inactive)
  → set Active (attention) and/or paper Daily Analysis
  → journals engage the series
  → optional Capital Activation ($X real) → new OP series (see lifecycle doc)
```

## Two export types

### Portfolio export (whole account config)

Exports seed name, capital, risk %, markets, nested strategy, vetting/`export_kind`, and (when captured) fingerprint provenance.

```bash
./bin/compose exec -T winston_unit_test \
  bin/rails wut:portfolios:export_config[RUN_ID, /portfolio_configs/my-portfolio.json]
```

Also produced by vet path (`PortfolioTrendVetter#export_run!`) into `portfolio_configs/portfolio-*.json`.

Canonical kinds:

| `export_kind` | Meaning |
|---------------|---------|
| `trade_ready` | Passed **Viability Gates** — eligible for **Capital Activation** to real (default path) |
| `observation` | Failed or skipped gates — paper/regime observation; real Capital Activation needs force |
| missing | Treat as **observation** on import |

Avoid legacy phrase **Configured Portfolio** — use **Trade-Ready Portfolio** or **Observation Portfolio**.

### TradingStrategy export (methodology only)

```bash
./bin/compose exec -T winston_unit_test \
  bin/rails wut:strategies:export_config[TS_ID]
```

Reusable methodology; still subject to StrategyRegistry class names in Wv2.

## Provenance fields (target shape)

Nested `trading_strategy` (and/or top-level) should carry when available:

| Field | Role |
|-------|------|
| `fingerprint` | Full content hash — **lineage match key** in Wv2 |
| `wut_trading_strategy_id` | Lab row id |
| `name` | Human label (becomes seed-related display + suffix when fingerprinted) |
| methodology blocks | entry/exit/risk (rich + flat compat) |

Top-level: `name` (seed), `markets`, `initial_capital`, `export_kind`, `wut_backtest_run_id`, `vetting`.

Historical files may lack fingerprint — legacy bare-name path until re-export (ticket: refresh portfolio exports).

## What Wv2 creates on import

| JSON field | Wv2 entity |
|------------|------------|
| `name` (seed) | **seed_name** + display name (`seed · shortFp` when fingerprint present) |
| `markets[]` | Market find_or_create + Book per symbol |
| `initial_capital` | CashEvent (initial) once per new OP series |
| `trading_strategy` + fingerprint | TradingStrategy + provenance; linked to OP |
| `export_kind` | Stored for gates; missing → observation |
| — | **Execution Mode** default `paper`; **Active** false |

## Import lineage rules (ADR-006)

1. **Same full fingerprint** (on OP/TS) → update that lineage **if not engaged**.  
2. **No fingerprint match**, bare seed OP exists, **Books symbols match** → **adopt** (attach fingerprint, rename to suffix form).  
3. **Else** → **auto-fork** new OP + TS (new fingerprint or membership mismatch).  
4. **No fingerprint in JSON** → legacy bare-name update (transition).  
5. **Engaged** OP (any Journal) → refuse shape mutation via import; use close / successor / Capital Activation.

**Not** silent upsert-by-name for fingerprinted methodology (supersedes older “re-import same name always updates” language).

## Preconditions

1. Strategy **class names** in JSON must exist in Wv2 StrategyRegistry  
2. DM parquet for Books (or lazy fetch on Daily Analysis)  
3. OP inactive until explicit **Active**  
4. Real **Capital Activation** requires trade_ready (or force) — see lifecycle doc  

## Idempotency (summary)

| Situation | Result |
|-----------|--------|
| Re-import same fingerprint, pre-engagement | Update fields/provenance |
| Re-import new fingerprint | Auto-fork new OP+TS |
| Re-import, engaged OP | No shape overwrite |
| Initial CashEvent | Once per OP series |
| Capital Activation $X | Always new OP series + new initial CashEvent |

## Verification target

Backtest known config in WUT on DM parquet → export with fingerprint → import to Wv2 → Active paper → signals align with WUT expectations on same data. Regime re-vet with new fingerprint must **not** erase the prior OP’s journals.

## Related

- ADR-006 — lineage and lifecycle decision  
- `wv2-operational-portfolio-lifecycle.md` — Active, engage, close, rebalance, Capital Activation  
- `trade-ready-viability-gates.md`  
- `portfolio-and-trading-strategy-lifecycle.md`  
