# Session Report — Portfolio Backtest First-Pass Doctrine & WUT Implementation

**Date:** 2026-07-06
**Time:** ~18:00–21:06 local (estimated)
**Duration:** ~3h (spans grill + implementation; includes prior context in thread)
**Project:** Sawtooth — ecosystem + winston_unit_test
**Working directory:** `/home/johnkoisch/Documents/com/sawtooth`
**Branch:** `main` (both repos)
**Model:** Grok
**Operator:** johnkoisch

---

## 1. Goal & Outcome

**Stated goal:** Revisit portfolio backtesting for portfolio creation/export (P0 task #5) — define first-pass trend vetting doctrine and implement it in WUT so Red/Blue re-vets use a credible 6×2 grid with fixed risk/position rules.

**Outcome:** Partially delivered (~60% of P0 ticket)

**One-line summary:** First-pass backtest spec is documented and coded (6 entries × 2 exits, $10K, 12 positions / 4 markets, swap-on-13th); export viability gates and an actual re-vet are still pending.

---

## 2. Work Completed

- Agreed **Option A** first-pass grid: 6 breakout entries × 2 exits (paired opposite breakout + VolatilityExit)
- Fixed pass-1 components: ATR stops, pyramid each ATR, 2% static risk, 5 pyramid/market, 12 positions, 4 markets, 13th-signal swap, $10K capital, `move_to_last_entry` stop trail
- Confirmed **opposite exit** = same entry class / lookback, evaluated in reverse direction via `TestingStrategy`
- Wrote canonical analysis doc: `docs/analysis/portfolio-trading-strategy-evaluation.md`
- Updated P0 ticket with progress table; plan task #5 → `in_progress`
- Implemented WUT: `FIRST_PASS_BASE_CONFIG`, `paired_opposite_exit` optimizer combos, `max_markets_per_portfolio`, `PositionSwapEvaluator`, specs
- Clarified task #5 status for user: doctrine done, export enforcement + re-vet not done

---

## 3. Code Delivered

### Files changed

| File | Change | Notes |
|------|--------|-------|
| `ecosystem/docs/analysis/portfolio-trading-strategy-evaluation.md` | added | First-pass grid + fixed components |
| `ecosystem/docs/business-context/trade-ready-viability-gates.md` | added | Grill session — placeholder gates |
| `ecosystem/CONTEXT.md` | modified | Trade-Ready / Observation / Optimization Candidate glossary |
| `ecosystem/docs/tickets/2026-07-07-portfolio-trading-strategy-evaluation-framework.md` | modified | Status in progress + progress table |
| `ecosystem/plans/portfolio-overlap-rebuild.md.tasks.json` | modified | Task #5 → in_progress with note |
| `winston_unit_test/app/services/portfolio_trend_vetter.rb` | modified | `FIRST_PASS_BASE_CONFIG`, 6×2 vet |
| `winston_unit_test/app/services/portfolio_signal_optimizer.rb` | modified | `paired_opposite_exit` combo builder |
| `winston_unit_test/app/models/portfolio_signal_optimization.rb` | modified | `paired_opposite_exit?`, exit_combo_count |
| `winston_unit_test/app/services/portfolio_position_manager.rb` | modified | 4-market cap, open position helpers |
| `winston_unit_test/app/services/portfolio_backtest/position_swap_evaluator.rb` | added | 13th-signal swap (inline ATR ER) |
| `winston_unit_test/app/services/portfolio_backtest_runner.rb` | modified | Swap integration in `process_entries` |
| `winston_unit_test/app/services/portfolio_backtest_run_factory.rb` | modified | `max_markets_per_portfolio`, config JSON |
| `winston_unit_test/app/services/portfolio_backtest/entry_pass_reason.rb` | modified | `market_limit` reason |
| `winston_unit_test/app/models/portfolio_backtest_transient_run.rb` | modified | `max_markets_per_portfolio` attr |
| `winston_unit_test/db/migrate/20260707120000_...rb` | added | `max_markets_per_portfolio` column |
| `winston_unit_test/db/schema.rb` | modified | Schema bump |
| `winston_unit_test/lib/tasks/portfolio_trend_vet.rake` | modified | Desc reflects 6×2 grid |
| `winston_unit_test/spec/services/portfolio_trend_vetter_spec.rb` | added | Config + optimization shape |
| `winston_unit_test/spec/services/portfolio_backtest/position_swap_evaluator_spec.rb` | added | Swap approve/decline |
| `winston_unit_test/spec/services/portfolio_signal_optimizer_spec.rb` | modified | Paired opposite combos test |

### Commits

- _Pending this wrap — see §11_

### Branch / PR state at sign-off

- Branch: `main` (ecosystem + WUT) — dirty, uncommitted session work
- Pushed: no (this session's commits)
- PR: not opened

---

## 4. Decisions Made

### Decision 1: First-pass grid = 6×2 (opposite + volatility)
- **Choice:** Sweep 6 entries × 2 exit modes; fix risk/position rules
- **Why:** Fast credible trend test without full parameter explosion
- **Alternatives considered:** VolatilityExit only (rejected — too narrow, Blue vet failure)
- **Reversibility:** easy
- **Promote to ADR?** no — captured in analysis doc

### Decision 2: Opposite exit paired to entry class
- **Choice:** Same breakout strategy ID as exit; `TestingStrategy` evaluates opposite direction
- **Why:** Matches existing WUT behavior; user confirmed
- **Reversibility:** easy
- **Promote to ADR?** no

### Decision 3: Swap uses inline ATR ER (not full calculator)
- **Choice:** `PositionSwapEvaluator` uses `AtrBasedCalculator` + simple incoming proxy
- **Why:** Full multi-method ER is post-backtest async today
- **Alternatives considered:** Synchronous full ER — deferred to follow-on
- **Reversibility:** easy
- **Promote to ADR?** no

### Decision 4: Export paths (Trade-Ready vs Observation)
- **Choice:** Document gates; do not auto-enforce in export yet
- **Why:** Implementation scoped to lab path first
- **Reversibility:** easy
- **Promote to ADR?** no

---

## 5. Insights Surfaced

- Blue vet failure was partly **doctrine** (single exit, $20K, 10-position cap, no market limit) not only membership
- `PortfolioSignalOptimizer` already supports multi-exit combos; **paired opposite** needed a new `paired_opposite_exit` flag
- Expected-return jobs run **after** backtest — swap cannot use full ER without new synchronous path
- WUT `main` was ahead 1 commit before this session's uncommitted work; unrelated DM registry WIP exists untracked — do not commit with this session

---

## 6. Issues & Tickets

### Resolved this session
- P0 ticket and task #5 partially advanced — progress table + `in_progress` status

### Deferred
- **export_kind + viability gate enforcement in `PortfolioTrendVetter`** — documented only; see P0 ticket
- **Null Sharpe ranking fallback** — Blue vet winner issue; not fixed
- **`vet_trend` env/config overrides** — hardcoded first-pass defaults
- **db:migrate + WUT container deploy** — migration not run in compose
- **Re-vet Portfolio Red** — task #2, blocked until WUT deployed
- **Re-vet Portfolio Blue** — task #3
- **Full multi-method ER for swap** — follow-on pass
- **Plan Phase 7** in `portfolio-overlap-rebuild.md` — not written
- **Blue post-mortem template** — not written
- **Recreate DM compose container** — task #1 (separate ticket)
- **Orange/White build** — task #4 when suitable pool ≥50

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| First-pass config constants | RSpec (written) | ⚠️ not executed — `bundle install` failed locally |
| Paired opposite combos | RSpec (written) | ⚠️ not executed |
| Position swap evaluator | RSpec (written) | ⚠️ not executed |
| End-to-end `vet_trend` on Red | not run | ❌ |
| Migration in compose | not run | ❌ |

**Test command(s):** `cd winston_unit_test && bundle exec rspec spec/services/portfolio_trend_vetter_spec.rb spec/services/portfolio_signal_optimizer_spec.rb spec/services/portfolio_backtest/position_swap_evaluator_spec.rb`

---

## 8. Environment, Dependencies, Data

- **Dependencies:** Local `bundle install` failed (gem resolution); use WUT container for migrate/test
- **Services:** No compose changes this session
- **Migrations:** `20260707120000_add_max_markets_per_portfolio_to_portfolio_backtest_runs.rb` — pending run

---

## 9. Risks & Technical Debt

- Swap ER proxy may behave differently from post-backtest full ER — tune after first re-vet
- Export still allows catastrophic winners to write JSON without `export_kind`
- Uncommitted WUT files (`dm_registry_*`) from another effort — must not be swept into this commit

---

## 10. Open Questions

- **Does first-pass re-vet improve Red/Blue economics materially?** — needs answer from: re-vet runs; blocks: Wv2 handoff

---

## 11. Handoff & Resume Notes

- **Where I left off:** User asked for task #5 status clarity; `/wrap` invoked
- **Next concrete step:** `podman exec` WUT → `rails db:migrate` → re-vet Portfolio Red with `portfolios:vet_trend`
- **Files to read first:**
  1. `ecosystem/docs/analysis/portfolio-trading-strategy-evaluation.md`
  2. `winston_unit_test/app/services/portfolio_trend_vetter.rb`
  3. `ecosystem/docs/tickets/2026-07-07-portfolio-trading-strategy-evaluation-framework.md`

---

## 12. Stakeholder Communications

- Portfolio pipeline blocked on Wv2 import until task #5 completes export gates + at least one credible re-vet

---

## 13. Tools & Workflow Notes

- **Skills used:** session-report, wrap (invoked), grill-with-docs (prior in thread)
- **What worked well:** Codifying first-pass in `FIRST_PASS_BASE_CONFIG` + analysis doc keeps lab and docs aligned
- **Friction points:** Local bundle broken; long vets need `podman exec -d`
- **Subagent usage:** none this session

---

## 14. Follow-up Actions

- [ ] Migrate WUT + deploy first-pass code in compose container — owner: ops — due: before re-vet
- [ ] Re-vet Portfolio Red (`portfolios:vet_trend`) — owner: dev — due: after migrate — See: `plans/portfolio-overlap-rebuild.md.tasks.json#2`
- [ ] Implement `export_kind` + viability gates in `PortfolioTrendVetter#export_run!` — owner: dev — See: P0 ticket
- [ ] Fix null `practical_sharpe_ratio` ranking fallback — owner: dev — See: P0 ticket
- [ ] Add `vet_trend` env vars for ranking metric / config override — owner: dev — See: P0 ticket
- [ ] Re-vet Portfolio Blue and compare to prior -98% run — owner: dev — See: task #3
- [ ] Full multi-method ER for swap decisions (optional pass 2) — owner: dev
- [ ] Write Plan Phase 7 + Blue post-mortem template — owner: dev — See: P0 ticket

---

## 15. Appendix

**Excluded from this commit (other WIP in WUT tree):**
- `app/jobs/dm_registry_sync_job.rb`
- `app/services/dm_registry_synchronizer.rb`
- `config/initializers/dm_registry_on_boot.rb`

**Task #5 dependency chain:**
```
#5 framework (60%) → #2 Red vet → #3 Blue revisit → Wv2 import
```