# Ticket: Eventual schema cleanup for activity_id columns (post DM SoT)

**Status:** Proposed (Phase B/C deferred; planning done)  
**Priority:** P3  

**Related to:** ecosystem/docs/session-reports/2026-07-08-1430-dm-reconcile-container-cleanup.md  
**Plan:** ecosystem/plans/wut-dm-parquet-source-of-truth.md (open items)  
**Monolith:** `winston_unit_test`  
**Owner:** follow plan (non-blocking for DM SoT close)  
**Due:** when legacy activity paths are fully abandoned or a major schema cleanup release

## Context

After the DM cutover, `activity_id` is optional on result-bearing tables (Position, TradingSignal, BacktestIndicatorValue, PassedSignal). DM paths use `(market_id, bar_date)` (+ result parquet / `DmParquetLoader` re-pull) instead of Activity rows. Many tables still carry the column, indexes, and FKs. Journals **never** had `activity_id` (always `market_id` + `trade_date`).

We do not want to drop historical data or break remaining non-DM loaders immediately. This ticket inventories current state and defines a phased cleanup plan. **No columns are dropped in this planning pass.**

## Status of this deliverable

| Item | State |
|------|--------|
| Inventory | Done (2026-07-08) |
| Migration strategy decision | Done — **phased**, no new `source` column |
| Migration + rollback plan | Documented below (draft SQL shape; **not applied**) |
| Models / factories / specs updates | Documented impact; **not applied** (Phase B/C) |
| Cutover conditions for purging activities | Documented below |
| Code/migration applied this session | **None** (by design — evidence does not support dropping yet) |

---

## Inventory (as of schema.rb / models 2026-07-08)

### A. Tables with `activity_id` column

| Table | `activity_id` nullability | Indexes involving `activity_id` | FK → `activities` | Model association | DM path behavior |
|-------|---------------------------|----------------------------------|-------------------|-------------------|------------------|
| `positions` | **nullable** | `index_positions_on_activity_id` | yes | `belongs_to :activity, optional: true` | Writes `nil` + sets `market_id`/`bar_date` when `bar_context` present |
| `trading_signals` | **nullable** | `index_trading_signals_on_activity_id` | yes | `belongs_to :activity, optional: true` | `activity_id` nil; `market_id`/`bar_date` columns exist |
| `backtest_indicator_values` | **nullable** | `index_backtest_indicator_values_on_activity_id`; **unique** `index_indicator_values_on_run_activity_indicator` on `[backtest_run_id, activity_id, indicator_name]` | yes | `belongs_to :activity, optional: true` + uniqueness validation on same scope | **Skipped entirely** when bar `id` is nil (`BacktestRunner`) |
| `passed_signals` | **nullable** | `index_passed_signals_on_activity_id` | yes | `belongs_to :activity, optional: true` | Hash `activity_id: nil` for DM; has own `market_id` + `date` |
| `market_indicator_values` | **NOT NULL** | **unique** `index_market_indicator_values_unique` on `[activity_id, indicator_name, indicator_config]`; `index_market_indicator_values_on_activity_id` | yes | `belongs_to :activity` (**required**) | Not written for DM (`DatasetLoader` / `BacktestActivitiesLoader.sync_to_activities!` skip MIV for DM symbols) |
| `market_moving_averages` | **NOT NULL** | `index_market_moving_averages_on_activity_id` | yes | `belongs_to :activity` (**required**) | Essentially **legacy/dormant** (only destroy paths; no active writers found outside historical data) |

### B. Related tables **without** `activity_id`

| Table | Identity used | Notes |
|-------|---------------|--------|
| `journals` | `market_id` (NOT NULL) + `trade_date` + optional `position_id` | Never had `activity_id`. Relax migration guarded with `column_exists?(:journals, :activity_id)` — no-op. Model already DM-aware via position’s activity/bar. |
| `paper_orders` / `paper_runs` | `market_id` / dates | No activity FK |
| `activities` | parent bar table | Still created by non-DM loaders (Yahoo/CSV/`DatasetLoader`, non-DM parquet sync). Unique `(market_id, date)`. |

### C. Foreign keys to `activities` (schema.rb)

```
backtest_indicator_values → activities
market_indicator_values   → activities
market_moving_averages    → activities
passed_signals            → activities
positions                 → activities
trading_signals           → activities
```

### D. Prior migration (Phase A partially done)

`db/migrate/20260707150000_relax_activity_fks_for_dm_source_of_truth.rb`:

- Made nullable: `positions`, `trading_signals`, `backtest_indicator_values`, `passed_signals`, `journals` (journals column never existed).
- Added optional identity columns: `positions.market_id` + `bar_date`, `trading_signals.market_id` + `bar_date` (journals branch no-op for activity_id).
- Did **not** touch `market_indicator_values` or `market_moving_averages` (still NOT NULL) — intentional; those rows are activity-carrier indicator storage for legacy bars.

### E. Models with `belongs_to :activity`

| Model | optional? | Notes |
|-------|-----------|--------|
| `Position` | yes | Also `belongs_to :market, optional: true` |
| `TradingSignal` | yes | Compat `#market`, `#date` via activity or `market_id`/`bar_date` |
| `BacktestIndicatorValue` | yes | Uniqueness still scoped to `activity_id` (PostgreSQL UNIQUE treats NULLs as distinct) |
| `PassedSignal` | yes | Identity via `market_id` + `date` |
| `MarketIndicatorValue` | **no** | DB NOT NULL + unique on activity_id scope |
| `MarketMovingAverage` | **no** | DB NOT NULL |
| `Journal` | n/a | No association |

`Activity` still declares `has_many :positions, :market_moving_averages, :trading_signals, :market_indicator_values`.

### F. Notable write / read sites (not exhaustive)

**Still write `activity_id` (legacy / dual-path):**

- `Position.manage_position` — sets `activity_id` from signal when not DM-only; DM uses `bar_context`
- `PositionManager` — LEAP path hard-codes `activity_id: activity.id` (legacy assumption)
- `BacktestRunner` — BIV create only when `activity.id` present
- `Operations::SignalEvaluation` — passes `activity_id` (nil for DM bars)
- `DatasetLoader` / `DataDownloader` / `ParquetData::BacktestActivitiesLoader.sync_to_activities!` — create Activity + MIV for **non-DM** only
- `ActiveAccountsBackupJob` — slices `activity_id` from position attributes

**Still read `activity_id` / `Activity` for identity or ATR:**

- `ExpectedReturnCalculator` — dual path (bar_date vs activity_id ordering)
- `PyramidIndicatorCorrelator` — indexes BIVs by `activity_id`; entry via `position.activity_id`
- `Operations::TaskGenerator` — fallback price via `Activity.find_by(id: signal[:activity_id])`
- Controllers/views: `portfolio_backtest_runs_controller`, `backtest_runs_controller`, `_positions_table` — mixed DM guards + legacy joins
- `Market#risk` / `Activity#atr` — MIV lookup by `activity_id` (legacy ATR store)

### G. Factories / specs

- No `spec/factories` tree found; no FactoryBot `activity` factory inventory.
- Specs that construct activities: e.g. `spec/services/portfolio_backtest/position_swap_evaluator_spec.rb`, `entry_requirement_calculator_spec.rb`, `entry_decision_maker_spec.rb` (Structs / local lets — not schema-bound factories).
- Impact of later column drop: update dual-path specs, any fixture hashes including `activity_id`, backup job attribute lists, and correlator tests if BIVs lose activity keys.

---

## Decision: migration strategy

### Recommendation: **Phased cleanup; do not add a `source` column**

**Why no `source` column on results:**

- Identity for DM is already `(market_id, bar_date)` on positions/signals (and journals always used market + trade_date).
- Result durability is intended to live in **result parquet** (BACKTEST schema) + re-pull via `DmParquetLoader`, not a second provenance flag on every row.
- A `source` enum would be redundant bookkeeping and another migration surface.

**Why phased (not one-shot drop):**

1. Phase A nullability is largely done for result tables; MIV/MMA remaining NOT NULL is correct while legacy Activity loaders exist.
2. Many dual-path readers still use `activity_id` for legacy runs and some correlators/views.
3. Dropping FKs/columns while dual-path code remains is high-risk and not required for DM SoT close.
4. Historical Activity + MIV rows may still back old non-DM backtests and UI “data sets” legacy views.

### Phase map

| Phase | Goal | When | Blocking for DM SoT? |
|-------|------|------|----------------------|
| **A** (done / residual) | Nullable result FKs + model `optional: true` + identity columns | Already shipped via `20260707150000_…` | No |
| **A′ residual (optional, low risk)** | Document-only or tiny model comments; **do not** nullify MIV/MMA yet | Anytime | No |
| **B** | Stop **writing** `activity_id` on new result rows for all paths (or only when DM); verify zero new non-null `activity_id` on positions/signals/BIV/passed for DM runs | After dual-path call sites audited | No |
| **C** | Drop indexes → drop FKs → drop columns on **result** tables; leave or separately retire `activities` / MIV / MMA | After B + observation window | No |
| **D (optional)** | Purge legacy `activities` (+ cascade MIV/MMA) when no product path needs historical Activity bars | Only if product agrees historical non-DM data is disposable | No |

---

## Migration + rollback plan (document only — not applied)

### Phase A residual (already applied)

- Migration: `20260707150000_relax_activity_fks_for_dm_source_of_truth.rb`
- Rollback: reverse nullability + remove added `market_id`/`bar_date` only if no DM rows depend on them (unsafe once DM production data exists). Treat as **forward-only** in practice.

### Phase B — application only (no schema)

1. Grep/CI guard: no new writes of non-null `activity_id` on DM bars (`id.nil?` / `DmParquetPaths`).
2. Align remaining hard-coded writers:
   - `PositionManager` LEAP create path (`activity_id: activity.id`)
   - Any portfolio runner paths still attaching Activity for identity
   - Backup job: include `market_id`/`bar_date` in slice
3. Fix dual-path readers that **require** `activity_id` for DM-era rows:
   - `PyramidIndicatorCorrelator` (prefer BIV identity by date/market when activity_id nil — or accept BIV skip for DM as BacktestRunner already does)
4. Observation: N days (recommend **≥ 14 calendar days** of normal ops + at least one full portfolio backtest cycle) with metrics:
   - `positions.activity_id IS NOT NULL` count stable or only on known legacy runs
   - New DM runs: `activity_id` all NULL on positions/trading_signals/passed_signals
   - No regressions in ER, daily ops tasks, result views

**Rollback B:** revert application commits; columns remain.

### Phase C — schema drop (result tables only)

**Order matters (PostgreSQL):**

1. **Pre-check queries** (must pass before migrate):

```sql
-- New DM-era runs should not need activity_id; optional: flag any recent non-null
SELECT COUNT(*) FROM positions WHERE activity_id IS NOT NULL AND bar_date IS NOT NULL;
SELECT COUNT(*) FROM trading_signals WHERE activity_id IS NOT NULL AND bar_date IS NOT NULL;
SELECT COUNT(*) FROM passed_signals WHERE activity_id IS NOT NULL;
SELECT COUNT(*) FROM backtest_indicator_values WHERE activity_id IS NULL; -- expected large if any DM BIVs ever written (today DM skips BIV)

-- Code deploy must not reference columns after drop
```

2. **Migration sketch** (one migration or split per table; prefer one reverseable migration with `safety_assured`/strong_migrations if used):

```ruby
# Draft only — DO NOT apply until Phase B gates pass
class DropActivityIdFromResultTables < ActiveRecord::Migration[7.0]
  TABLES = {
    positions: {
      indexes: %w[index_positions_on_activity_id],
      fk: true
    },
    trading_signals: {
      indexes: %w[index_trading_signals_on_activity_id],
      fk: true
    },
    passed_signals: {
      indexes: %w[index_passed_signals_on_activity_id],
      fk: true
    },
    backtest_indicator_values: {
      indexes: %w[
        index_backtest_indicator_values_on_activity_id
        index_indicator_values_on_run_activity_indicator
      ],
      fk: true,
      note: "unique index must be replaced if BIV retained without activity_id — e.g. [backtest_run_id, bar identity] or drop BIV table for DM-only world"
    }
  }

  def up
    # For each table: remove_foreign_key :table, :activities (if exists)
    # remove_index ...
    # remove_column :table, :activity_id
  end

  def down
    # add_reference :table, :activity, foreign_key: true, null: true, index: true
    # restore unique index on BIV if needed
    # NOTE: historical activity_id values are NOT restored
  end
end
```

3. **BIV special case:** unique index includes `activity_id`. Options:
   - **C1 (preferred if BIV unused for DM):** stop using BIV entirely; drop table later; for Phase C just drop `activity_id` and unique index after confirming no writers.
   - **C2:** replace unique key with `[backtest_run_id, market_id, bar_date, indicator_name]` only if BIV is reintroduced for DM with those columns (would need new columns first — out of scope unless product wants BIV again).

4. **Do not drop in same PR without model updates:**
   - Remove `belongs_to :activity` from Position, TradingSignal, PassedSignal, BacktestIndicatorValue
   - Remove `Activity` `has_many` for those associations
   - Clean attribute slices, correlators, jobs, views

**Rollback C:** `down` re-adds nullable columns + FKs + indexes; **data in `activity_id` is lost** unless a pre-drop backup table is taken:

```sql
-- Optional safety before Phase C
CREATE TABLE _backup_positions_activity_id AS SELECT id, activity_id FROM positions WHERE activity_id IS NOT NULL;
-- similar for trading_signals, passed_signals, backtest_indicator_values
```

### Phase C′ — indicator carrier tables (`market_indicator_values`, `market_moving_averages`)

**Separate from result-table cleanup.** These are 1:1 with Activity bars for legacy ATR/MA storage.

- Only after legacy loaders no longer create Activities, **or** after MIV is fully replaced by parquet ATR for all markets.
- Strategy options:
  1. **Retire tables entirely** when `Activity#atr` and non-DM risk paths are gone (delete MIV/MMA + drop tables).
  2. **Re-key to `(market_id, date, indicator_…)`** if product wants DB-side indicators without Activity — larger redesign; not recommended while parquet is SoT.

**Do not nullify `market_indicator_values.activity_id` “just because”** without a replacement identity: uniqueness and `Activity#atr` depend on it.

### Phase D — purge legacy `activities` rows

**Not required for DM SoT.** Conditions under which purge is acceptable:

1. **Product:** Explicit decision that non-DM (Yahoo/CSV) historical bars and any backtests that only lived as Activity-linked positions are disposable or have been exported.
2. **Code:** No production code path calls `Activity.create` / `find_or_create_by` / `sync_to_activities!` / `DatasetLoader` Activity insert for any active market. Grep clean for writers.
3. **Data dependency:** Zero remaining FKs from result tables to `activities` (Phase C done) **or** purge only activities with no remaining children:

```sql
-- Safe-ish orphan purge after Phase C (no child FKs left)
-- Before Phase C, only purge activities with no referencing rows:
DELETE FROM market_indicator_values WHERE activity_id IN (...);
DELETE FROM market_moving_averages WHERE activity_id IN (...);
-- Only if positions/signals/etc. already null or dropped
DELETE FROM activities WHERE id IN (...);
```

4. **Ops:** Backup DB; run during maintenance; verify portfolio/backtest result UIs for both old DM runs and any retained legacy runs.
5. **Cutover date:** Set only when (1)–(4) pass; **no fixed calendar date today**. Suggested gate: “Phase C merged + 30 days with DM-only production use + stakeholder sign-off.”

If activities table is retained long-term as an empty/legacy husk, that is acceptable; column cleanup on **results** is the higher-value cleanup.

---

## Model / factory / spec impact (Phase B–C checklist)

| Area | Impact |
|------|--------|
| Models | Remove or keep `optional: true` until drop; on drop remove associations; BIV uniqueness validation |
| `Activity` | Remove has_manys as children lose FK; eventual deprecation of model |
| Jobs | `ActiveAccountsBackupJob` attribute list; `CalculateExpectedReturnJob` already nil-safe |
| Services | PositionManager LEAP; PyramidIndicatorCorrelator; TaskGenerator Activity fallback; DatasetLoader only if retiring non-DM |
| Controllers/views | Remove remaining `includes(:activity)` / activity date fallbacks after bar_date ubiquitous |
| Factories | None found; create DM-oriented fixtures with `market_id`/`bar_date` if needed later |
| Specs | Dual-path portfolio specs using Activity structs; no mass factory rewrite expected |

---

## Acceptance criteria

- [x] Inventory all tables/columns/indexes that still reference `activity_id` (or `belongs_to :activity`).
- [x] Decide on migration strategy (phased; **no** new `source` column on results).
- [x] Produce a migration + rollback plan (documented; draft not applied).
- [ ] Update models, factories, and specs accordingly. **→ Phase B/C implementation tickets**
- [x] Document cutover conditions under which legacy activity rows can be purged (if ever).

## Implementation this session

- **Code changes:** none  
- **Migrations applied:** none  
- **Draft migration committed:** no (plan only; drop not safe yet)  
- **Blocking dependency on portfolio work?** **No** — non-blocking cleanup; portfolio dual-path may still *read* activity_id until Phase B, but portfolio delivery does not block planning or later phased cleanup.

## Suggested follow-up tickets (when ready)

1. **Phase B:** Zero-write audit for `activity_id` on DM result rows + LEAP/PositionManager dual-path fix.  
2. **Phase C:** Drop `activity_id` from positions / trading_signals / passed_signals / BIV (+ model/view cleanup).  
3. **Phase D (optional):** Activities + MIV + MMA retirement / purge after stakeholder approval.

## Links

- Plan: `ecosystem/plans/wut-dm-parquet-source-of-truth.md`
- Relax migration: `winston_unit_test/db/migrate/20260707150000_relax_activity_fks_for_dm_source_of_truth.rb`
- Schema: `winston_unit_test/db/schema.rb`
- Related tickets: DM SoT cluster; activities compatibility shim
