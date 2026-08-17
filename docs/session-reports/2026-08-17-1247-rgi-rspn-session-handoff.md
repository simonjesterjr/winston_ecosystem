# Session Report — RGI→RSPN remap and DAR session handoff

**Date:** 2026-08-17
**Time:** ~09:50–12:47 MDT
**Duration:** ~3h
**Project:** sawtooth Winston ecosystem — data_manager (DM), winston_v2 (Wv2), live WUT/Wv2 DBs, `portfolio_configs/`
**Working directory:** `/home/johnkoisch/Documents/com/sawtooth`
**Branch:** `main` on `data_manager`, `winston_v2`, `ecosystem`
**Model:** Grok 4.6
**Operator:** johnkoisch

---

## 1. Goal & Outcome

**Stated goal:** Portfolio Rust listed market **RGI**, which is neither in DM search nor Schwab research. Figure out why, fix Rust, and update human-confirm pendings if the operator had a next action.

**Outcome:** Delivered. Live books remapped. Stale RGI pendings resolved. Ops-shell fill-date hole fixed. Weekend Daily Analysis Report (DAR) clones no longer mint, and Confirm/Pass supersedes siblings. Skip-vs-replay ticket closed.

**One-line summary:** RGI is the retired ticker for the same Invesco equal-weight industrials ETF now trading as RSPN; Rust was remapped in place, three fake RGI longs were passed, and DAR task identity is now the session bar — not the calendar date.

---

## 2. Work Completed

- Confirmed Schwab/OCC: **RGI → RSPN** (2023-06-07), same fund
- DM had stale RGI parquet through **2026-07-24** (last bar high **64.025**); RSPN registry row existed but was never acquired
- Acquired RSPN (1,798 bars through **2026-08-14**); remapped Market rows in Wv2 (#59) and Winston Unit Test (WUT) (#1119) in place (same `market_id`, not a successor Operational Portfolio)
- Updated `portfolio_configs/portfolio-rust.json`, sidecar, and `registry.json`
- Passed three stale RGI drafts (journals 630/639/666); live Friday eval did **not** want RSPN
- Tasked the real Friday winner **RXT short** (#614 / journal #845); operator later confirmed it
- Ops shell hid Friday/Saturday tasks (`report_date > today−2`); fixed `OperationsTask.actionable_on` to honor `fill_date`
- Unhide dumped 16 clones of Sunday desk work; operator had already filled ROKU / XOP / EEM and Passed NVDA / VXX / TSLA / PG / OIH
- Passed 15 siblings as `superseded` (not process-miss expire)
- Implemented light path: skip tasking when `bar.date ≠ report_date`; session-key idempotency; auto-supersede on Confirm/Pass
- Closed `winston_v2/docs/tickets/2026-07-28-dar-skip-when-no-session-bar.md`

---

## 3. Code Delivered

### Files changed

#### data_manager

| File | Change | Notes |
|------|--------|-------|
| `app/services/ticker_remap.rb` | added | Canonical storage RGI→RSPN; EODHD aliases include TSMC→TSM |
| `app/services/data_acquisition_service.rb` | modified | Acquire via remap; mark predecessor registry |
| `app/services/symbol_registry_acquirer.rb` | modified | Uses `TickerRemap` |
| `app/controllers/api/v1/triggers_controller.rb` | modified | Consumer-sync symbols remapped |
| `spec/services/ticker_remap_spec.rb` | added | 5 examples |

#### winston_v2

| File | Change | Notes |
|------|--------|-------|
| `app/models/operations_task.rb` | modified | `actionable_on` honors fill_date |
| `app/models/passed_signal.rb` | modified | `superseded` reason |
| `app/services/operations/session_handoff.rb` | added | Session-bar / fill-window identity |
| `app/services/operations/supersede_sibling_tasks.rb` | added | Auto-pass pending twins |
| `app/services/operations/task_generator.rb` | modified | Skip non-session mint; session duplicate check |
| `app/services/operations/pass_signal_service.rb` | modified | `superseded` + sibling hook |
| `app/services/operations/journal_confirmation_service.rb` | modified | Confirm supersedes siblings |
| `spec/services/action_item_window_spec.rb` | modified | Fri signal / Mon fill visible |
| `spec/services/operations/task_generator_eod_cadence_spec.rb` | modified | Skip + stamp + duplicate |
| `spec/services/operations/pass_signal_service_spec.rb` | modified | Supersede on pass |
| `spec/services/operations/journal_confirmation_service_spec.rb` | modified | Supersede on confirm |
| `docs/tickets/2026-07-28-dar-skip-when-no-session-bar.md` | modified | **Closed** — skip tasking |
| `docs/session-reports/2026-07-28-0954-…breakout-window.md` | modified | Checkbox closed |

#### Live / volume (not in git)

| Artifact | Change |
|----------|--------|
| Wv2 Market 59 | `RGI` → `RSPN` |
| WUT Market 1119 | `RGI` → `RSPN` |
| DM Market + parquet | `/app/data/markets/RSPN/` acquired; RGI registry `renamed_to` RSPN |
| `portfolio_configs/` rust JSON + registry | RGI → RSPN (folder is not a git repo) |

**Not staged (pre-existing dirty, other sessions):** Wv2 `exit_at_stop_service*`, desk `_actions.html.erb`; all WUT dirty files; unrelated ecosystem ticket edits.

### Commits

- `data_manager` `c436bbd` — feat(dm): remap retired RGI ticker onto live RSPN
- `winston_v2` `9f56a35` — feat(ops): skip non-session DAR tasks and supersede siblings
- `ecosystem` — this report (SHA filled after push)

### Branch / PR state at sign-off

- Branch: `main` on DM / Wv2 / ecosystem — pushed
- PR: not opened (work is on `main`)

---

## 4. Decisions Made

### Decision 1: In-place ticker remap, not successor
- **Choice:** Rename `Market.trading_symbol` RGI→RSPN on the same row; books/journals stay.
- **Why:** Same instrument (CUSIP continuity). Architecture Decision Record (ADR) 006 successor is for membership/methodology shape change.
- **Alternatives considered:** Successor OP A′; keep RGI and add RSPN as a second book.
- **Reversibility:** easy (rename back) but live parquet path is now RSPN.
- **Promote to ADR?** no — `TickerRemap` is enough.

### Decision 2: Pass stale RGI drafts; do not enter RSPN
- **Choice:** Pass journals 630/639/666 (`other` / dead-ticker notes). Live Friday tape had no RSPN 5-day breakout.
- **Why:** Signals used the July 24 high (64.025) replayed Fri/Sat/Sun.
- **Alternatives considered:** Relabel pendings to RSPN and let the operator fill.
- **Reversibility:** easy (new DAR can mint a real RSPN signal later).
- **Promote to ADR?** no.

### Decision 3: Skip tasking when no session bar
- **Choice:** DAR may inspect a reused bar; it must not mint tasks. Handoff identity is the session bar. Confirm/Pass auto-`superseded` remaining twins.
- **Why:** Calendar `report_date` minted Fri/Sat/Sun clones of one Monday fill. Hide ≠ resolve; expire-as-miss is the wrong ledger.
- **Alternatives considered:** Parent Activity + Sat/Sun children (too heavy; legitimizes clones); auto-supersede only (siblings still appear all weekend).
- **Reversibility:** easy.
- **Promote to ADR?** no — closes existing ticket; ADR-009 already names one handoff.

### Decision 4: `actionable_on` uses fill_date
- **Choice:** Pending shell / DAR next-steps include `fill_date >= as_of`.
- **Why:** Friday signal / Monday fill was invisible on Monday.
- **Alternatives considered:** Leave legacy `report_date > as_of-2`.
- **Reversibility:** easy.
- **Promote to ADR?** no.

---

## 5. Insights Surfaced

- DM still listed RGI as acquired and `not_suitable_for_winston` (ATR-17/close ~1.3% vs floor ~5.2%). RSPN fails the same rule — expected; suitability is for random draws, not kicking an engaged book.
- DAR `on-or-before` + weekend cron turned a **3-week-stale** last bar into three “today” entries.
- `already_evaluated?` / `duplicate_task?` keyed on calendar `report_date`, so each weekend day was a “new” evaluation.
- Completing Sunday’s twin left Fri/Sat `pending`. The shell hid them; expire would have called that a process miss.
- Rust free cash was already about **−$2,615** (DBA / AAAU / BIS) before the RXT short.
- `portfolio_configs/` is a compose bind-mount, not a git repo.

---

## 6. Issues & Tickets

### Resolved this session
- Rust dead ticker RGI — remapped to RSPN
- Ops-shell pending invisible on fill day — `actionable_on` fill-date aware
- 15 weekend sibling pendings — Passed `superseded`
- `winston_v2/docs/tickets/2026-07-28-dar-skip-when-no-session-bar.md` — **Closed** (skip tasking)

### Deferred
- No Active-book “last bar N sessions behind the rest of the book” detector (would have caught RGI in late July)
- Rust still **observation** / failed max-drawdown — `ecosystem/docs/tickets/2026-07-12-re-vet-mango-rust-trade-ready.md`
- RSPN remains `not_suitable_for_winston` on S3 volatility floor (do not use for random universe draws)
- DM development `EMFILE` / inotify — rails runner in `development` often cannot boot; `RAILS_ENV=test` rspec works
- Unrelated dirty trees in WUT, ecosystem, and Wv2 `exit_at_stop` left untouched

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| `TickerRemap` | `RAILS_ENV=test bundle exec rspec spec/services/ticker_remap_spec.rb` | ✅ 5 examples |
| RSPN acquire | DM `request_consumer_sync` | ✅ 1798 bars, latest 2026-08-14 |
| Wv2/WUT books | rails runner | ✅ Rust symbols include RSPN, no RGI |
| Live Friday eval | `SignalEvaluation` 2026-08-14 | ✅ no RSPN; RXT/BFIX/SCHD |
| `actionable_on` + expire + panels | rspec `action_item_window_spec`, expire, ops_shell_panels | ✅ |
| Skip / session dup / supersede | rspec generator + pass + confirm + daily_tasks + window | ✅ 30 examples, 0 failures |
| Ops shell after unhide | live `OpsShellPanels` | ✅ then 15 passed; operator confirmed RXT #845 |

**Test command(s):**

```
./bin/compose exec -T data_manager sh -c 'RAILS_ENV=test bundle exec rspec spec/services/ticker_remap_spec.rb'
./bin/compose exec -T winston_v2 bundle exec rspec spec/services/operations/task_generator_eod_cadence_spec.rb spec/services/operations/task_generator_heat_spec.rb spec/services/operations/pass_signal_service_spec.rb spec/services/operations/journal_confirmation_service_spec.rb spec/services/operations/daily_tasks_service_spec.rb spec/services/action_item_window_spec.rb
```

---

## 8. Environment, Dependencies, Data

- **Dependencies:** None
- **Services:** Existing compose stack. Restarted `data_manager`, `data_manager_sidekiq`, `winston_v2` (twice)
- **Migrations:** None
- **Live DB:** Wv2 postgres (5434), WUT, DM `data_manager_development`

---

## 9. Risks & Technical Debt

- Historical RGI parquet left in place under `/app/data/markets/RGI/` (archaeology). Consumers now read RSPN.
- Session-handoff sibling match uses fill-date OR session-bar. Two genuine different session bars that somehow share a fill date would collapse — unlikely under EOD T→T+1.
- Rust remains over-deployed after the RXT short.
- `portfolio_configs` remap is only on disk, not versioned.

---

## 10. Open Questions

- **Should Active books get a stale/renamed-ticker health check?** — operator; does not block desk
- **Re-vet Rust membership now that RSPN fails S3?** — lab; existing observation ticket

---

## 11. Handoff & Resume Notes

- **Where I left off:** Light path live; ticket closed; operator confirmed RXT; 15 siblings superseded; wrap in progress
- **Next concrete step:** Tonight’s DAR should not mint Sat/Sun clones. Watch Pending after the next weekend or holiday.
- **Files to read first:**
  1. `winston_v2/app/services/operations/session_handoff.rb`
  2. `winston_v2/app/services/operations/task_generator.rb`
  3. `winston_v2/app/services/operations/supersede_sibling_tasks.rb`
  4. `data_manager/app/services/ticker_remap.rb`
  5. `winston_v2/docs/tickets/2026-07-28-dar-skip-when-no-session-bar.md`

---

## 12. Stakeholder Communications

- Operator-only. No Telegram, no real-capital action. Paper desk: do not buy RGI/RSPN from those old drafts (already passed). RXT short was confirmed by the operator.

---

## 13. Tools & Workflow Notes

- **Skills used:** `operator-prose`, `wrap`, `session-report`
- **What worked well:** Live rails runner + Schwab/OCC confirmation; fill-date vs report-date diagnosis from one query
- **Friction points:** DM `development` inotify EMFILE blocks `rails runner` / rspec unless `RAILS_ENV=test`
- **Subagent usage:** none

---

## 14. Follow-up Actions

- [ ] Watch next weekend/holiday DAR — no new Fri-bar clones — owner: operator — due: next non-session DAR
- [ ] Optional: Active-book stale-ticker detector — owner: eng — due: backlog
- [ ] Optional: version `portfolio_configs` or copy remaps into a git-tracked export — owner: eng — due: backlog

---

## 15. Appendix (optional)

Sunday AM desk (what the operator actually worked):

| Task | OP | Action |
|------|-----|--------|
| 446 / j672 | Mango ROKU long 9 | executed |
| 447 / j673 | Mint · 85730621 XOP long 10 | executed |
| 448 / j674 | Yellow EEM long 37 | executed |
| 441–445 | NVDA, VXX, TSLA, PG, OIH | operator_decline |

Rust #614 / journal #845 RXT short 166 — operator desk-confirm executed 2026-08-17 15:49 UTC.
```
