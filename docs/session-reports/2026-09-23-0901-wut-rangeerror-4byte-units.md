# Session Report — WUT RangeError 4-byte units

**Date:** 2026-09-23
**Time:** ~08:20–10:00 MDT
**Duration:** ~1h 40m
**Project:** winston_unit_test (ticket in ecosystem)
**Working directory:** /home/johnkoisch/Documents/com/sawtooth/winston_unit_test
**Branch:** main (started from `a4565e2`)
**Model:** Grok 4.7
**Operator:** lane B seed (Grok CLI only)

---

## 1. Goal & Outcome

**Stated goal:** Stop `ActiveModel::RangeError` (integer limit 4 bytes) on heat-ON Teal and Orange Portfolio Backtest Runs, identify the column, keep Sidekiq from retrying the same cell, and push WUT main. Do not requeue PBRs 767–771.

**Outcome:** Delivered for the code fix and the column. Live restamp of those cells was not run.

**One-line summary:** The crashing value is the uncapped share count written to `passed_signals.would_have_units`; the entry is now refused and a leftover RangeError is discarded instead of retried.

---

## 2. Work Completed

- Identified `passed_signals.would_have_units` as the column that receives `5742089524897382400` / `11484179049794764800`.
- Fail-closed the sizing and persist path. Did not widen the column (the 2% value exceeds signed bigint).
- `PortfolioBacktestJob` discards `ActiveModel::RangeError` after marking the run failed.
- Specs for the calculator, pass reason, position manager, job, and the specimen insert.
- System One via `jev ask`: column and retry checkpoints pass; live-cell checkpoint does not.
- Updated the ecosystem ticket. Did not requeue 767–771.
- Restarted `winston_unit_test` and `winston_unit_test_sidekiq` at 09:14 MDT so the running processes loaded the fix. PBR 771’s show page still renders the stored 2026-09-22 failure.

---

## 3. Code Delivered

### Files changed

| File | Change | Notes |
|------|--------|-------|
| `app/services/portfolio_backtest/persistable_integer.rb` | added | Signed 4-byte fit check. Out of range returns nil, no clamp. |
| `app/services/portfolio_backtest/entry_requirement_calculator.rb` | modified | `units_out_of_range` when risk/stop does not fit |
| `app/services/portfolio_backtest/entry_pass_reason.rb` | modified | Surfaces that reason ahead of `no_units` |
| `app/services/portfolio_backtest_runner.rb` | modified | Passed-signal and paper-order guards; RST arm reason |
| `app/services/position_manager.rb` | modified | Refuses share and LEAP contract counts that do not fit |
| `app/jobs/portfolio_backtest_job.rb` | modified | `discard_on ActiveModel::RangeError` |
| `app/models/passed_signal.rb` | modified | Reason label |
| `spec/services/portfolio/entry_requirement_calculator_spec.rb` | modified | 1% and 2% fail-closed examples |
| `spec/services/portfolio/entry_pass_reason_spec.rb` | modified | Reason example |
| `spec/services/position_manager_fill_relative_stop_spec.rb` | modified | Share and LEAP refusal |
| `spec/jobs/portfolio_backtest_job_range_error_spec.rb` | added | Job does not re-raise |
| `spec/models/passed_signal_integer_range_spec.rb` | added | Column identity and specimen insert |
| `ecosystem/docs/tickets/2026-09-22-wut-teal-heat-on-rangeerror-4byte-int.md` | modified | Status and result |

### Commits

- `a30e228` — Fix: refuse oversized backtest units before the 4-byte integer write (`winston_unit_test` main)
- Ecosystem ticket + this report committed in the wrap commit on ecosystem main.

### Branch / PR state at sign-off

- Branch: `main` — pushed after this report is committed
- Pushed: yes, as part of wrap
- PR: not opened (hotfix on main, matching the seed)

---

## 4. Decisions Made

### Decision 1: Refuse the entry instead of widening the column
- **Choice:** If `floor(risk_dollars / stop_distance)` does not fit a signed 4-byte integer, return 0 units and reason `units_out_of_range`. Do not clamp to 2,147,483,647 and do not migrate to bigint.
- **Why:** The Teal 2% specimen `11484179049794764800` is larger than signed bigint max `9223372036854775807`. A near-zero stop is not a real share count.
- **Alternatives considered:** Widen `would_have_units` to bigint. That still raises on the 2% value.
- **Reversibility:** easy
- **Promote to ADR?** no

### Decision 2: Do not requeue 767–771
- **Choice:** Leave those runs failed. Operator restamps after the fix is on main.
- **Why:** Ticket human gate and non-goal. Live-cell Jev noul stayed below 0.8 because no cell was restamped.
- **Alternatives considered:** Rerun Orange #771 to satisfy the harness checkpoint.
- **Reversibility:** easy (operator can requeue)
- **Promote to ADR?** no

---

## 5. Insights Surfaced

- The error text is the same for every 4-byte integer column. The specimen matches the uncapped share count, not LEAP contracts (`shares / 100`), which would have been `57420895248973824`.
- `EntryRequirementCalculator` returns share units even when cash is checked in contracts. Skipped LEAP entries therefore persist the share count on `passed_signals.would_have_units`.
- Leverage capping can hide the same number on `positions.units` when equity is positive. `equity <= 0` skips that cap and would have written the raw count. The position-manager guard covers that hole.
- Orange #771 and Teal 1% cells share the exact integer despite different mark-to-market equity. The written value scales with risk percent, not with the equity snapshot.

---

## 6. Issues & Tickets

### Resolved this session
- `ecosystem/docs/tickets/2026-09-22-wut-teal-heat-on-rangeerror-4byte-int.md` — code fix landed. Status left as operator-restamp pending, not fully closed.

### Deferred
- Operator restamp of Teal heat-ON and Orange #771. Jev `teal_or_orange_cell_completes_or_clean_fail` noul was 0.33. Do not requeue until the operator says so.
- `db/schema.rb` on main is still version `2026_08_21_180000` while migration `20260916120000_add_option_aware_metrics_to_portfolio_backtest_runs` is pending. Applying it to the test database rewrote `schema.rb`; that hunk was reverted and is not in this commit. Filed: [`../../../winston_unit_test/docs/tickets/2026-09-23-wut-schema-rb-option-aware-metrics.md`](../../../winston_unit_test/docs/tickets/2026-09-23-wut-schema-rb-option-aware-metrics.md).

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| Column | Schema sql type `integer` plus specimen `save(validate: false)` | ✅ raises limit 4 bytes |
| Sizing guard | EntryRequirementCalculator 1% and 2% examples | ✅ units 0, `units_out_of_range` |
| Persist | `record_passed_signal` with `5742089524897382400` | ✅ row saved, units nil, no RangeError |
| Retry | `PortfolioBacktestJob.perform_now` forced RangeError | ✅ no raise, run `failed` |
| Neighbors | LEAP journal, LEAP fulfillment, RST arm, next-open, fill-relative stop | ✅ 49 examples, 0 failures (`RUBYOPT=-rostruct`) |
| Live cell | Restamp of 767–771 | ❌ not run |
| Compose | Restart web + Sidekiq; `GET /wut/portfolio_backtest_runs/771` | ✅ 200. Page still shows stored `5742089524897382400` RangeError |
| Jev | `jev ask` jev-1.13.0 | column confidence 1.0; retry noul 0.92; cell noul 0.33 |

**Test command(s):** `podman exec -e RAILS_ENV=test -e TEST_DB_HOST=wut_postgres -w /app winston_unit_test bundle exec rspec` on the files above. Host `bundle exec rspec` cannot reach Postgres on port 5432 (WUT is on host port 5433 / container hostname `wut_postgres`).

---

## 8. Environment, Dependencies, Data

- **Dependencies:** none
- **Services:** existing compose (`winston_unit_test`, `wut_postgres`). Test database migrated `20260916120000` so specs could boot. `db/schema.rb` was not committed. Web and Sidekiq restarted 09:14 MDT; both running. Sidekiq boot enqueued the usual `DmRegistrySyncJob`. No `PortfolioBacktestJob` was in the retry set.
- **Migrations:** none added

---

## 9. Risks & Technical Debt

- A restamped cell can still hit some other 4-byte integer this guard does not cover. The job discard stops a retry storm if that happens, and the run stays failed.
- Refusing the entry changes the backtest versus booking a leverage-capped position on a near-zero stop. That cap was not a meaningful trade.
- Pre-existing: several runner specs use `OpenStruct` without `require "ostruct"` and fail when `entry_requirement_calculator.rb` has not been loaded. Pre-existing: `portfolio_backtest_edge_persist_spec` passes `initial_capital` to `Portfolio`.

---

## 10. Open Questions

- **When does the operator restamp 767–771?** — needs answer from the operator; blocks a live proof of checkpoint 3.

---

## 11. Handoff & Resume Notes

- **Where I left off:** Fix is on `winston_unit_test` `a30e228` and ecosystem `f6b0ceb`. Containers restarted. PBR 771 still displays the stored failure. Cells not requeued.
- **Next concrete step:** Operator restamps one Teal or Orange cell and confirms it finishes or fails once without `ActiveModel::RangeError`. Restart already happened, so a restamp will run the new code.
- **Files to read first:** `app/services/portfolio_backtest/persistable_integer.rb`, `app/services/portfolio_backtest_runner.rb` (`record_passed_signal`), the ecosystem ticket.

---

## 12. Stakeholder Communications

- Operator: fix is on main. Web and Sidekiq were restarted. [PBR 771](https://sawtooth-ai.tail944ffb.ts.net/wut/portfolio_backtest_runs/771) still shows the stored RangeError until that run is restamped. PBRs 767–771 were not requeued.

---

## 13. Tools & Workflow Notes

- **Skills used:** lightweight-bug-fix, graphify query (then file read), wrap / session-report, jevctl `jev ask` (no TypeSafe Python SDK).
- **Graphify Graph:** WUT code graph left at the earlier refresh this session (4528 nodes; no code change since `a30e228`). Ecosystem `graphify update` rebuilt 12576 nodes / 928 communities. Workspace merge wrote `sawtooth/graphify-out/graph.json` (18583 nodes, 22917 edges; 5 graphs, winston_v2 graph absent). Not committed.
- **Ponytail flags:** `PersistableInteger` is new. The WUT graph shows it only beside `.overflow?` / `.storable` under `PortfolioBacktest`. No existing units-range helper to collapse into. No new helper in the restart slice.
- **What worked well:** The 2× risk relationship plus LEAP `shares/100` distinguished `would_have_units` from `positions.units` without an app frame.
- **Friction points:** Host rspec hits port 5432; tests need the compose test database. `schema.rb` was one version behind a committed migration.
- **Subagent usage:** none

---

## 14. Follow-up Actions

- [ ] Operator restamp of Teal heat-ON or Orange #771 after this push — owner: Operator — due: when they choose. Already the human gate on [`../tickets/2026-09-22-wut-teal-heat-on-rangeerror-4byte-int.md`](../tickets/2026-09-22-wut-teal-heat-on-rangeerror-4byte-int.md). No second ticket.
- [ ] Commit the pending option-aware columns into `db/schema.rb` — owner: next WUT session. See [`../../../winston_unit_test/docs/tickets/2026-09-23-wut-schema-rb-option-aware-metrics.md`](../../../winston_unit_test/docs/tickets/2026-09-23-wut-schema-rb-option-aware-metrics.md).

---

## 15. Appendix (optional)

Jev (`jev-1.13.0`, typesafe), first ask: `overflow_column` = `identified_bigint_or_units_candidate` confidence 1; `no_retry_storm` noul 0.92; `teal_or_orange_cell_completes_or_clean_fail` noul 0.45. Second ask of the cell question after the insert spec: noul 0.33.

Specimen relationship: `11484179049794764800 == 2 * 5742089524897382400`. Both are `1275 * 2^52` and `2550 * 2^52`.
