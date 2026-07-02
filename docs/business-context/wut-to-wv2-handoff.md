# WUT → Wv2 Handoff

**Type:** Domain workflow
**Related ADR:** ADR-001
**Operational guide:** `portfolio_configs/README.md` (sawtooth root)

## Purpose

Move a **vetted** trading configuration from the lab (**WUT**) to live operations (**Wv2**) without re-entering parameters. The handoff is file-based JSON through the shared `portfolio_configs/` volume.

## The happy path

```
WUT backtest (vet results)
  → export Configured Portfolio JSON (or TradingStrategy JSON)
  → human edits JSON if needed (nano/vim — explicit supported path)
  → Wv2 import (creates Portfolio + Books + CashEvent + TradingStrategy)
  → activate Portfolio
  → daily analysis runs → Cromwell notification
```

## Two export types

### Configured Portfolio (whole account)

Exports portfolio-level settings: capital, risk %, markets, strategy names.

```bash
./bin/compose exec -T winston_unit_test \
  bin/rails wut:portfolios:export_config[RUN_ID, /portfolio_configs/my-portfolio.json]
```

### TradingStrategy (methodology only)

Exports reusable strategy definition. Can be applied to multiple Portfolios.

```bash
./bin/compose exec -T winston_unit_test \
  bin/rails wut:strategies:export_config[TS_ID]
```

Wv2 import supports **upsert-by-name** — re-importing with the same name updates the existing TradingStrategy.

## What Wv2 creates on import

| JSON field | Wv2 entity |
|------------|------------|
| `name`, risk params, strategy names | Portfolio |
| `markets[]` | Market (find_or_create) + Book per symbol |
| `initial_capital` | CashEvent (event_type=initial) |
| strategy block | TradingStrategy (linked to Portfolio) |

## Preconditions

1. **Strategy names** in JSON must exist in Wv2's StrategyRegistry (same class names as WUT seeds)
2. **Parquet data** must exist for imported markets — run `dm:sync_from_wv2` or equivalent after import
3. Portfolio is **inactive** until explicitly activated

## Idempotency rules

- Re-importing same portfolio name: mostly idempotent for Portfolio record
- Re-importing TradingStrategy with same name: updates existing record
- CashEvent initial: typically created once on first import

## Verification target

Backtest a known config in WUT on DM parquet data → export → import to Wv2 → run daily analysis → signals should match WUT expectations on the same data.