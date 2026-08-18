# Session Report — After-close EOD session contract + Monday catch-up DAR

**Date:** 2026-08-18
**Time:** ~09:00–10:00 MDT
**Duration:** ~1h
**Project:** sawtooth Winston ecosystem — data_manager (DM), winston_v2 (Wv2), ecosystem docs
**Working directory:** `/home/johnkoisch/Documents/com/sawtooth`
**Branch:** `main` on `data_manager`, `winston_v2`, `ecosystem`
**Model:** Grok 4.6
**Operator:** johnkoisch

---

## 1. Goal & Outcome

**Stated goal:** Verify that no signals were generated on any Winston v2 (Wv2) Active paper Operational Portfolio (OP) from trading Monday 2026-08-17, after the session-bar skip made the evening Daily Analysis Report (DAR) / ops shell show zero. Then, after that proved to be a data-window bug rather than a quiet market, lock the after-close End of Day (EOD) date contract and score Monday’s actual close.

**Outcome:** Delivered. Pipeline contract fixed. Monday catch-up DAR minted 12 session-true tasks. Telegram not re-sent.

**One-line summary:** DM was pulling through yesterday, so Monday’s close never landed; after the session-bar skip the DAR looked empty. We now pull the completed New York session, require an exact session bar to evaluate, and Monday has 12 real desk actions.

---

## 2. Work Completed

- Verified live Wv2: 7 Active paper OPs, 0 real; **0** `OperationsTask` / passed-signal rows for 2026-08-17; 4 Monday journals were fills of earlier sessions (ROKU / XOP / EEM / RXT)
- Re-ran `SignalEvaluation` for 2026-08-17: **15** setups, all `bar_date=2026-08-14`; TaskGenerator correctly refused to mint
- Confirmed parquet / `DmCoverage` latest **2026-08-14** after Monday 15:30 Mountain DM sync; DAR appendix OHLCV matched Friday
- Root-caused `EcosystemDataSyncService` / `SymbolRegistryAcquirer` `to = Date.current - 1` vs Wv2 on-or-before `data_ready?`
- Implemented `CompletedNySession` (America/New_York, 16:00 ET close) and wired DM acquire paths
- Wv2: `session_bar_for` + exact `data_ready?`; `SignalEvaluation` uses the exact session bar; lookback / marks stay on-or-before
- Specs: DM clocks; missing session ≠ ready; eval does not score a reused prior bar; TaskGenerator skip still holds
- Updated `data-invariant-and-derivatives.md`
- Pulled all 70 Active book symbols through 2026-08-17 (EODHD); latest=2026-08-17 on every sample
- Re-ran `DailyAnalysisJob` for 2026-08-17 with `WV2_TELEGRAM_DELIVER=0`: **12** tasks, 0 skipped, all `session_bar_date=2026-08-17`
- Restarted `data_manager`, `data_manager_sidekiq`, `winston_v2_sidekiq` so tonight’s cron loads the new code

---

## 3. Code Delivered

### Files changed

#### data_manager

| File | Change | Notes |
|------|--------|-------|
| `app/services/completed_ny_session.rb` | added | Last completed NY session + 7y+60d `history_from` |
| `app/services/ecosystem_data_sync_service.rb` | modified | `to`/`from` via `CompletedNySession` |
| `app/services/symbol_registry_acquirer.rb` | modified | Same window |
| `app/services/data_acquisition_service.rb` | modified | Default acquire uses completed session, not `EodhdClient.recent`/`Date.current` |
| `app/services/eodhd_client.rb` | modified | `recent` also uses completed session |
| `spec/services/completed_ny_session_spec.rb` | added | Mon after close, Tue before close, Sat weekend, Fri 16:00 |
| `spec/services/ecosystem_data_sync_service_spec.rb` | added | Acquire `to=2026-08-17` not yesterday |

#### winston_v2

| File | Change | Notes |
|------|--------|-------|
| `app/services/parquet_lookback_loader.rb` | modified | `session_bar_for`; `data_ready?` exact date; `bar_for` still on-or-before |
| `app/services/operations/signal_evaluation.rb` | modified | Eval bar = `session_bar_for` |
| `spec/services/parquet_lookback_loader_spec.rb` | modified | Prior bar ≠ ready |
| `spec/services/portfolio_readiness_spec.rb` | modified | `missing_data` when exact bar absent |
| `spec/services/operations/signal_evaluation_open_position_spec.rb` | modified | Stubs + no-score-without-session-bar |

**Not this session (left unstaged on Wv2):** `app/views/operations/signal_inspect/show.html.erb`, `spec/requests/operations_signal_inspect_spec.rb`, `docs/session-reports/2026-08-18-0932-signal-inspect-legend-sheet.md`.

#### ecosystem

| File | Change | Notes |
|------|--------|-------|
| `docs/business-context/data-invariant-and-derivatives.md` | modified | `latest_date` = completed NY session |
| `docs/issues/2026-08-18-dm-yesterday-window-misses-after-close-session.md` | added | Resolved |
| `docs/tickets/2026-08-18-after-close-eod-session-contract.md` | added | Done |
| `docs/tickets/INDEX.md` | modified | P0 Done row |
| `docs/session-reports/2026-08-18-1000-after-close-eod-session-contract.md` | added | This report |

### Commits

- **data_manager** `00ecb55` — `fix(eod): pull completed NY session after close, not yesterday`
- **winston_v2** `2b9daf2` — `fix(ops): require exact session bar for DAR readiness and eval`
- **ecosystem** `e0560b0` — `docs: wrap after-close EOD session contract and Monday catch-up`

### Branch / PR state at sign-off

- Branch: `main` on all three
- Pushed: yes (wrap)
- PR: not opened (direct `main`)
- Wv2 leftover dirty (not this commit): signal-inspect legend sheet — See ticket `2026-08-18-commit-wv2-signal-inspect-legend-sheet`

---

## 4. Decisions Made

### Decision 1: After-close `to` is the completed NY session, not yesterday
- **Choice:** `CompletedNySession` at 16:00 America/New_York; weekday after close → that date; before close / weekend → prior weekday
- **Why:** M–F DM cron is 15:30 Mountain (17:30 Eastern), after NY close. `Date.current - 1` on Monday requested Sunday → Friday last bar
- **Alternatives considered:** Always `Date.current` (writes a partial bar during market hours); holiday calendar (out of scope — missing print stays not-ready)
- **Reversibility:** easy
- **Promote to ADR?** no — invariant doc updated

### Decision 2: Exact session bar for readiness/eval; on-or-before for marks
- **Choice:** `data_ready?` / `SignalEvaluation` use `session_bar_for`; `bar_for` stays on-or-before
- **Why:** Changing `bar_for` globally would break sizing, equity, next-open. Quiet “hold” on a missing session is the operator-visible defect
- **Alternatives considered:** Fail the whole DAR; keep on-or-before and only skip mint (status quo — hides the gap)
- **Reversibility:** easy
- **Promote to ADR?** no

### Decision 3: Catch-up DAR without Telegram
- **Choice:** `WV2_TELEGRAM_DELIVER=0`. Monday was still `default_report_date` Tuesday morning, so Telegram would have re-broadcast
- **Why:** Monday already posted 0 actions (msg 774). Operator can work the 12 pendings in the ops shell
- **Alternatives considered:** Wait until after 16:30 MT so Monday is historical
- **Reversibility:** easy (manual deliver if asked)
- **Promote to ADR?** no

---

## 5. Insights Surfaced

- Session-bar identity and the yesterday window were two bugs that cancelled into “empty DAR.” The skip was the right fix; it unmasked the data gap
- Consumer-sync / `EodhdClient.recent` already used `to=Date.current`; scheduled sync used yesterday. Two paths, two policies
- `data_ready?` on-or-before made `ensure_dm_data` a no-op (`missing=[]`) even when today’s print was absent
- `download_runs` / `download_tasks` tables are empty — Monday 15:30 left no DM run row
- Live catch-up: OIH Mon C=426.60 vs Fri 421.33; NVDA Mon C=225.01 vs Fri 225.16 — real Monday prints, not Friday reuse

---

## 6. Issues & Tickets

### Resolved this session
- `ecosystem/docs/issues/2026-08-18-dm-yesterday-window-misses-after-close-session.md` — yesterday window + on-or-before readiness
- `ecosystem/docs/tickets/2026-08-18-after-close-eod-session-contract.md` — Done

### Deferred
- Tonight’s unattended Tuesday path — See: [`docs/tickets/2026-08-18-observe-tuesday-unattended-eod-cycle.md`](../tickets/2026-08-18-observe-tuesday-unattended-eod-cycle.md)
- EODHD lag retry if 15:30 MT still lacks today’s print — See: [`docs/tickets/2026-08-18-eodhd-lag-retry-after-close.md`](../tickets/2026-08-18-eodhd-lag-retry-after-close.md)
- Empty `download_runs` / `download_tasks` — See: [`docs/tickets/2026-08-18-persist-dm-download-runs.md`](../tickets/2026-08-18-persist-dm-download-runs.md)
- `2026-07-13-stale-parquet-prior-close-active-symbols` — same family, radar age, not this session

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| DM `CompletedNySession` + sync `to` | `rspec spec/services/completed_ny_session_spec.rb spec/services/ecosystem_data_sync_service_spec.rb` | ✅ 8 examples, 0 failures |
| Wv2 exact bar + eval + skip | `rspec` parquet_lookback, portfolio_readiness, signal_evaluation_open_position, task_generator_eod_cadence, signal_evaluation_parity | ✅ 23 examples, 0 failures |
| Monday parquet | 70/70 Active symbols `latest=2026-08-17` | ✅ |
| Monday DAR catch-up | 12 tasks, 0 skipped, all `session_bar_date=2026-08-17`; Friday-only names absent; Telegram `skipped/disabled` | ✅ |
| Tonight Tuesday cycle | Not yet | ⚠️ |

**Test command(s):**

```
./bin/compose exec -T data_manager bundle exec rspec spec/services/completed_ny_session_spec.rb spec/services/ecosystem_data_sync_service_spec.rb
./bin/compose exec -T winston_v2 bundle exec rspec spec/services/parquet_lookback_loader_spec.rb spec/services/portfolio_readiness_spec.rb spec/services/operations/signal_evaluation_open_position_spec.rb spec/services/operations/task_generator_eod_cadence_spec.rb spec/services/signal_evaluation_parity_spec.rb
```

---

## 8. Environment, Dependencies, Data

- **Dependencies:** None
- **Services:** Restarted `data_manager`, `data_manager_sidekiq` (inotify EMFILE + load new code), `winston_v2_sidekiq`
- **Migrations:** None
- **Data:** Rewrote Active-book parquet through 2026-08-17; Wv2 `DmCoverage` ingested 88 / skipped 3; regenerated `wv2_20260817.{md,pdf,json}`

---

## 9. Risks & Technical Debt

- Holiday calendar not modeled — a weekday with no print stays `missing_data` (honest, may skip whole OPs)
- If EODHD has not published at 15:30 MT, exact-bar readiness will skip OPs instead of a false hold — better, still need a retry if it happens
- Wv2 leftover dirty tree (signal-inspect legend) is unrelated and was not committed
- Catch-up DAR overwrote Monday artifacts; Telegram still shows the old “0 actions” post

---

## 10. Open Questions

- **Did tonight’s 15:30 MT pull get Tuesday?** — needs answer from: parquet `latest_date` after 15:30 MT; blocks: confidence the unattended chain is fixed
- **Does the operator want Monday’s 12 actions on Telegram?** — needs answer from: operator; blocks: nothing (ops shell is live)

---

## 11. Handoff & Resume Notes

- **Where I left off:** Monday scored; 12 pendings in ops shell; tonight’s Tuesday cycle not observed
- **Next concrete step:** After 15:30 MT, confirm parquet `latest=2026-08-18`; after 16:30 MT, confirm DAR evaluates Tuesday bars (appendix OHLCV ≠ Monday)
- **Files to read first:**
  1. `data_manager/app/services/completed_ny_session.rb`
  2. `winston_v2/app/services/parquet_lookback_loader.rb` (`session_bar_for` / `data_ready?`)
  3. `ecosystem/docs/issues/2026-08-18-dm-yesterday-window-misses-after-close-session.md`

---

## 12. Stakeholder Communications

- Operator: 12 Monday paper desk actions are pending in the ops shell (not Telegram). Work those; do not treat last night’s empty DAR as “Monday was quiet.”

---

## 13. Tools & Workflow Notes

- **Skills used:** `operator-prose`, `session-report`, `wrap`
- **What worked well:** Live re-eval showing 15 Friday-stamped signals made the collision obvious; `WV2_TELEGRAM_DELIVER=0` already existed
- **Friction points:** DM container inotify EMFILE blocked first `rails runner` / rspec; restart cleared it. Host has no `psql` — used `compose exec postgres`
- **Subagent usage:** _None._

---

## 14. Follow-up Actions

- [ ] Confirm tonight’s unattended Tuesday DM pull + DAR — owner: operator / next agent — due: 2026-08-18 16:30 MT — See: [`docs/tickets/2026-08-18-observe-tuesday-unattended-eod-cycle.md`](../tickets/2026-08-18-observe-tuesday-unattended-eod-cycle.md)
- [ ] If 15:30 MT still lacks today’s print, implement EODHD lag retry — owner: next agent — due: if observed — See: [`docs/tickets/2026-08-18-eodhd-lag-retry-after-close.md`](../tickets/2026-08-18-eodhd-lag-retry-after-close.md)
- [ ] Persist DM `download_runs` / `download_tasks` — owner: next agent — due: unscheduled — See: [`docs/tickets/2026-08-18-persist-dm-download-runs.md`](../tickets/2026-08-18-persist-dm-download-runs.md)
- [ ] Work the 12 Monday pending desk tasks — owner: operator — due: now — See: [`docs/tickets/2026-08-18-work-monday-catchup-desk-tasks.md`](../tickets/2026-08-18-work-monday-catchup-desk-tasks.md)
- [ ] Commit leftover Wv2 signal-inspect legend sheet — owner: that UI session — due: unscheduled — See: [`docs/tickets/2026-08-18-commit-wv2-signal-inspect-legend-sheet.md`](../tickets/2026-08-18-commit-wv2-signal-inspect-legend-sheet.md)

---

## 15. Appendix (optional)

Monday catch-up tasks (all `session_bar_date=2026-08-17`, pending):

| Task | OP | Type | Market | Journal |
|------|-----|------|--------|---------|
| 677 | Rust `dd7e7c7a` | enter | DBE | 905 |
| 678 | Orange `7ea76741` | enter | SMH | 906 |
| 679 | Orange | pyramid | ZROZ | 907 |
| 680 | Orange | pyramid | VXX | 908 |
| 681 | Blue `f4dd31eb` | pyramid | TSLA | 909 |
| 682 | Blue | enter | PG | 910 |
| 683 | Blue | pyramid | XLE | 911 |
| 684 | Mint `0478e0ea` | enter | OIH | 912 |
| 685 | Mint | pyramid | VNQ | 913 |
| 686 | Mango `45c09e30` | enter | MSFT | 914 |
| 687 | Mango | pyramid | COMB | 915 |
| 688 | Yellow `7aa73357` | enter | REMX | 916 |

Friday-only names **not** cloned: BFIX, SCHD, USDU, FPA, NVDA, WMT, XOP, RXT, SVXY.

Telegram on catch-up JSON: `{ delivered: false, skipped: true, reason: "disabled" }`.
