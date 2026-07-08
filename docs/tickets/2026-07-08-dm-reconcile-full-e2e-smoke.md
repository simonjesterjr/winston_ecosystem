---
Status: Completed
---

# Ticket: Run full E2E smoke for DM reconcile + PBR after source-of-truth cutover

**Related to:** ecosystem/docs/session-reports/2026-07-08-1430-dm-reconcile-container-cleanup.md

## Context
The core WUT DM-parquet source-of-truth work is marked complete, but the plan closeout and the dedicated E2E smoke ticket call for a documented manual end-to-end smoke:

- Fresh DM-only PortfolioBacktestRun on a DM-covered symbol
- `data:reconcile` run
- Reconcile updates DataCoverage correctly
- Backtest + portfolio backtest execute with DM loader (no activities/MIV growth)
- Result views (positions table, candlestick, etc.) render using bar_date + DmParquetLoader re-pull
- Original reported crash (portfolio_backtest_runs/25 style) does not recur

## Acceptance Criteria
- [x] Bring up clean stack (`bin/compose up -d`)
- [x] `bin/compose build data_manager` (or bind-mount dev) — **not needed**; reconcile rake present and succeeded on running image
- [x] `bin/rails data:reconcile` (or symbol) succeeds with 0 errors on target symbols
- [x] Create a new DM-only PBR (no legacy activities dependency for execution path)
- [x] Execute backtest + portfolio backtest — **PBR 29 completed**; single-market **BR4 completed** after follow-up nil-activity fixes
- [x] Verify:
  - No new rows in `activities` or `market_indicator_values` for DM symbols
  - `bar_date` + `market_id` populated on Position/Journal where applicable
  - Views use `DmParquetLoader` / `BacktestResultsReader.load_bars...`
  - PBR/25-style page renders cleanly
- [x] Document the exact commands + observed counts/deltas in the e2e-smoke ticket
- [ ] Update plan closeout if any gaps found — gaps noted below; plan closeout not rewritten this pass

## Links
- Plan closeout: `ecosystem/plans/wut-dm-parquet-source-of-truth.md`
- Existing smoke ticket: `2026-07-08-wut-dm-parquet-e2e-smoke.md`
- Session report: `ecosystem/docs/session-reports/2026-07-08-1430-dm-reconcile-container-cleanup.md`
- ReconciliationService: `data_manager/app/services/reconciliation_service.rb`
- Rake: `data_manager/lib/tasks/data.rake`

**Owner:** human / worker-1 E2E  
**Due:** soon (before moving to portfolio-overlap work)

---

## Evidence (2026-07-08 ~21:03–21:07 UTC)

### Environment
- Workspace: `/home/johnkoisch/Documents/com/sawtooth`
- Stack already up via `bin/compose` (DM :3001, WUT :3000, Redis, Postgres). Brief WUT exit after Redis recreate during session; recovered with `podman start winston_unit_test`.
- HTTP: `http://localhost:3001/` → 200; `http://localhost:3000/` → 302.
- No DM image rebuild required (rake `data:reconcile` / `data:reconcile_symbol` present and functional).

### 1) DM reconcile

```bash
# Timestamp: 2026-07-08 21:03:45 UTC
bin/compose exec -T data_manager bin/rails data:reconcile_symbol[SPY]
# => {:symbol=>"SPY", :status=>"reconciled", :bar_count=>1797, coverage earliest 2019-05-13 latest 2026-07-07}

# Timestamp: 2026-07-08 21:03:56 UTC
bin/compose exec -T data_manager bin/rails data:reconcile
# => Done: {:reconciled=>632, :skipped=>0, :errors=>0, :symbols=>[... includes SPY ...]}
```

**Result:** 0 errors on full set (632 symbols reconciled). SPY coverage bar_count=1797.

### 2) WUT preflight (SPY + loader)

```bash
bin/compose exec -T winston_unit_test bin/rails runner '...'
```

| Check | Value |
|-------|-------|
| SPY market_id | 224 |
| DmCoverage bar_count / path | 1797 / `/dm_data/markets/SPY/bars.parquet` |
| `DmParquetPaths.exists_for?("SPY")` | true |
| `DmParquetLoader.full_history` | **1797** bars, `id=nil` |
| Legacy ACT/MIV (pre-existing, not grown) | act_spy=**1799**, miv_spy=**3558** |
| Global ACT/MIV | act_all=**77486**, miv_all=**149584** |

### 3) Create DM-only portfolio + PBR + single BacktestRun

Timestamp: **2026-07-08 21:04:21 UTC**

| Artifact | Id | Notes |
|----------|-----|-------|
| Portfolio | **32** `E2E DM Smoke SPY` | Book: SPY only |
| PortfolioBacktestRun | **29** | Factory: entry TSS#4 `Breakout50DayNoHistoryStrategy`, exit TSS#15 `VolatilityExitStrategy`; capital 20_000; status pending→completed |
| BacktestRun | **4** | Same strategies; status later **failed** (see Gaps) |

Before counts (SPY / all): ACT 1799 / 77486; MIV 3558 / 149584.

### 4) Execute PortfolioBacktestRun 29

Timestamp: **2026-07-08 21:06:15 UTC**

```bash
bin/compose exec -T winston_unit_test bin/rails runner '
  dr = { start_date: Date.new(2025,1,2), end_date: Date.new(2025,6,30),
         total_overlapping_days: 180, markets_data: [...] }
  PortfolioBacktestRunner.new(29, date_range: dr).execute
'
```

| Metric | Value |
|--------|-------|
| Status | **completed** |
| Window | 2025-01-02 .. 2025-06-30 (injected; 180 calendar days) |
| Elapsed | **32.3s** |
| final_equity | 20459.58 |
| total_return | ~2.30% |
| total_trades / positions | 8 |
| journals | 265 |
| run_id | `23bd4a70-0720-4b55-827c-16118f7cee7b` |
| Position `bar_date` nil | **0** |
| Position `market_id` nil | **0** |
| Position `activity_id` | blank/nil on samples |
| Journal `market_id` nil | **0** |
| Sample pos bar_dates | 2025-01-24, 2025-02-14, 2025-03-11, … market_id=224 |

**After PBR deltas:**

| Counter | Before | After | Δ |
|---------|--------|-------|---|
| act_spy | 1799 | 1799 | **0** |
| miv_spy | 3558 | 3558 | **0** |
| act_all | 77486 | 77486 | **0** |
| miv_all | 149584 | 149584 | **0** |

### 5) Single-market BacktestRun 4

**First attempt** (2026-07-08 21:07 UTC): failed with `signal.activity.date` nil (DM path).

**Follow-up fix + re-run** (2026-07-08 21:10–21:12 UTC):

Nil-activity guards added in:
- `backtest_runner.rb` — `signal.date`, `position.bar_date || position.activity&.date`
- `pyramid_group_tracker.rb` — `position_entry_date` helper

```bash
BacktestRunner.new(4).execute
# status=completed
# equity≈35580.64 return≈77.90% trades=24
# ACT delta=0 MIV delta=0
```

| Metric | Value |
|--------|-------|
| Status | **completed** |
| final_equity | ~35580.64 |
| total_return | ~77.90% |
| total_trades | 24 |
| ACT/MIV Δ | **0** / **0** |

### 6) Reader / re-pull / page smoke

Timestamp: **2026-07-08 21:07:02–21:07:33 UTC**

```bash
# Rails
ParquetData::Readers::BacktestResultsReader.load_bars_for_result_rows(...)  # => Hash size=1
DmParquetLoader.bar_for("SPY", bar_date, market_id: 224)
# 2025-01-24 close=607.97 atr_17≈6.69 id=nil
# 2025-02-14 close=609.70 atr_17≈6.38 id=nil
# 2025-03-11 close=555.92 atr_17≈9.65 id=nil

# HTTP
curl -s -o /tmp/pbr29.html -w "%{http_code}" http://localhost:3000/portfolio_backtest_runs/29  # 200
curl -s -o /tmp/pbr25.html -w "%{http_code}" http://localhost:3000/portfolio_backtest_runs/25  # 200
```

| Check | Result |
|-------|--------|
| PBR 29 HTML | **200**, contains Positions / Total Return / completed / SPY; **no** `PG::UndefinedTable` |
| PBR 25 HTML | **200** (original crash path does not recur) |
| `is_dm` controller-style load | Position.order COALESCE(bar_date,…) without activities include — OK |
| Final ACT/MIV | act_spy=1799 miv_spy=3558 act_all=77486 miv_all=149584 (**unchanged**) |

`BacktestResultsReader.read_portfolio_backtest_run(run)` returned `nil` in this environment (result parquet may not be written for this path or path not found under `/app/data/backtest`); show page still renders from DB positions/journals + live loader re-pull.

### Commands summary (copy/paste)

```bash
# Stack
bin/compose up -d
# Reconcile
bin/compose exec -T data_manager bin/rails data:reconcile_symbol[SPY]
bin/compose exec -T data_manager bin/rails data:reconcile
# Create + execute PBR (see runner script used above; PBR id=29 portfolio id=32)
bin/compose exec -T winston_unit_test bin/rails runner 'PortfolioBacktestRunner.new(29, date_range: {...}).execute'
# Pages
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:3000/portfolio_backtest_runs/29
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:3000/portfolio_backtest_runs/25
```

---

## Gaps remaining (non-blocking)

1. **`PortfolioBacktestRunner#find_overlapping_date_range` still reads `market.activities`** — works for SPY because of legacy ACT rows; a pure DM symbol with **0** activities would fail date-range discovery unless date_range is injected (as in this smoke). Should use DmCoverage / DmParquetLoader for DM markets.
2. **Full multi-year PBR not re-run** this pass — used 2025-H1 injected window after WUT container instability. Core DM path still exercised over ~6 months with trades; full-history single BR4 completed.
3. **`read_portfolio_backtest_run` returned nil** — page render OK via DB + loader; confirm result parquet write path for PBRs if consumers depend on it.
4. Deeper dual-path edges (LEAP/options, some expected-return job args with nil activity_id) may still need hardening under load — not observed as blockers in this smoke.

## Unblocks "move to portfolio creation"?

**Yes.** Reconcile solid (632/0). Fresh DM-only PBR (29) + single BR (4) complete with ACT/MIV Δ=0, composite identity, loader re-pull, PBR pages 200. Scheduled no-dup paths audited separately. Resume portfolio-overlap work.
