# Session Report — EODHD lag retry: probe, 17:00 stop, Labor Day Not Scored

**Date:** 2026-09-07
**Time:** ~17:10–17:44 MDT (after Labor Day Daily Analysis)
**Duration:** ~35m implementation; earlier turn inventoried non–Winston Quiver leftovers
**Project:** sawtooth Winston ecosystem — data_manager (DM), winston_v2 (Wv2), ecosystem docs
**Working directory:** `/home/johnkoisch/Documents/com/sawtooth`
**Branch:** `main` on `data_manager`, `winston_v2`, `ecosystem` (started from each `origin/main`)
**Model:** Grok 4.6
**Operator:** johnkoisch

---

## 1. Goal & Outcome

**Stated goal:** Close the remaining Architecture Decision Record 012 (ADR-012) work: End of Day Historical Data (EODHD) lag retry before 17:00 Mountain, and the Friday unattended scored-session observe (due 2026-08-28).

**Outcome:** Delivered. Retry no longer rewrites 7-year parquet after the deadline; Fridays 08-28 / 09-04 scored; Labor Day 09-07 was the first live **Not Scored**.

**One-line summary:** Session-coverage retry now probes EODHD for today’s print and stops at 17:00 Mountain *before* work; Daily Analysis waited until 17:03 and wrote `daily_not_scored` instead of a false hold.

---

## 2. Work Completed

- Inventoried leftover non–Winston Quiver (WQ) work from the 2026-09-04 research sessions; operator chose the P0 EODHD lag ticket.
- Verified live artifacts: Friday 2026-08-28 and 2026-09-04 Daily Activity Reports (DARs) were `daily_complete` / `session_status=scored` at 16:30–16:31 MT (print present, lag path unused).
- Captured Labor Day 2026-09-07: Wv2 Daily Analysis 16:30–17:03 MT wrote `wv2_20260907.json` `type=daily_not_scored` (70 symbols; parquet latest 2026-09-04). Old `SessionCoverageRetryJob` then re-acquired 106 symbols through **17:05 MT** (~10 min 7-year rewrite). Wv2 `request_dm_data` hit `Net::ReadTimeout`.
- Changed retry to **probe** the session print (no parquet rewrite until EODHD has the bar); **abort at 17:00 MT before work**; re-enqueue only while stale.
- Made `request_consumer_sync` async (`ConsumerSyncJob`); skip rewrite when history exists but the print is absent.
- Wv2 `SessionDataGate` pokes DM once, then polls ingest.
- Specs: 18 DM + 5 Wv2 examples green in compose.
- Restarted `data_manager`, `data_manager_sidekiq`, `winston_v2`, `winston_v2_sidekiq`; confirmed new source paths loaded.
- Closed P0 retry ticket and P1 Friday observe; filed P2 holiday calendar; updated the Friday-hold issue.

---

## 3. Code Delivered

### Files changed

#### data_manager

| File | Change | Notes |
|------|--------|-------|
| `app/services/session_coverage.rb` | modified | `session_print_live?` probe; canary AAPL/MSFT/SPY/QQQ; fail closed |
| `app/jobs/session_coverage_retry_job.rb` | modified | deadline first; probe; full sync only if print live |
| `app/services/ecosystem_data_sync_service.rb` | modified | `demand_symbols` |
| `app/jobs/consumer_sync_job.rb` | added | async consumer acquire; skip absent print |
| `app/controllers/api/v1/triggers_controller.rb` | modified | enqueue `ConsumerSyncJob`; no sync 7-year loop on Puma |
| `spec/services/session_coverage_spec.rb` | modified | stale vs session; probe true/false/error |
| `spec/jobs/session_coverage_retry_job_spec.rb` | added | deadline / skip rewrite / pull when live |
| `spec/jobs/consumer_sync_job_spec.rb` | added | skip / live / no coverage |
| `spec/jobs/daily_data_orchestrator_job_spec.rb` | modified | no enqueue after 17:00 MT |

#### winston_v2

| File | Change | Notes |
|------|--------|-------|
| `app/services/operations/session_data_gate.rb` | modified | request DM once, then poll |
| `spec/services/operations/session_data_gate_spec.rb` | modified | one poke, two ingest polls |

#### ecosystem

| File | Change | Notes |
|------|--------|-------|
| `docs/tickets/2026-08-18-eodhd-lag-retry-after-close.md` | modified | Done + live table + 09-07 fix |
| `docs/tickets/2026-08-22-observe-friday-scored-session-dar.md` | modified | Done; 08-28 / 09-04 / 09-07 results |
| `docs/issues/2026-08-22-friday-dar-hold-was-not-scored.md` | modified | status done |
| `docs/tickets/2026-09-07-completed-ny-session-us-holiday-calendar.md` | added | P2 holiday calendar |
| `docs/tickets/INDEX.md` | modified | three rows |
| `docs/session-reports/2026-09-07-1744-eodhd-lag-retry-probe.md` | added | this report |

**Not this session (do not stage)**

- `ecosystem/AGENTS.md`, `docs/README.md` (ponytail skill lines)
- `ecosystem/plans/cromwell-staff-roster.md`, `ecosystem/vendor/`

### Commits

- _Pending wrap commit._

### Branch / PR state at sign-off

- Branch: `main` on all three — dirty with this session’s files
- Pushed: pending wrap
- PR: not opened (direct `main`)

---

## 4. Decisions Made

### Decision 1: Probe before rewrite
- **Choice:** Session-only EODHD historical for a canary; full 7-year acquire only if that print exists.
- **Why:** Labor Day retry rewrote 106 symbols after 17:00 and blocked Wv2. A missing print will never appear on a closed day; Friday lag still needs one full pull once EODHD publishes.
- **Alternatives considered:** Short-window acquire (would replace parquet with one bar); always full-sync stale names.
- **Reversibility:** easy
- **Promote to ADR?** no (implements ADR-012)

### Decision 2: Stop at 17:00 before work
- **Choice:** `before_deadline?` at the start of `SessionCoverageRetryJob#perform`.
- **Why:** Checking after a 10-minute pull overran the DAR wait budget.
- **Alternatives considered:** Kill in-flight jobs at 17:00 (harder).
- **Reversibility:** easy
- **Promote to ADR?** no

### Decision 3: Consumer sync async + skip absent print
- **Choice:** `request_consumer_sync` enqueues `ConsumerSyncJob`. Skip rewrite when coverage exists but the session print is absent.
- **Why:** Controller claimed `accepted` but acquired synchronously; 120s HTTP timeout on Daily Analysis.
- **Alternatives considered:** Leave Puma sync; drop Wv2 poke entirely.
- **Reversibility:** easy
- **Promote to ADR?** no

### Decision 4: Holiday calendar is a later ticket, not tonight
- **Choice:** Labor Day Not Scored stays ADR-012 v1. File P2; do not add a NYSE calendar in this patch.
- **Why:** Operator asked for lag retry. Holiday “prior session” changes report date and needs an ADR addendum.
- **Alternatives considered:** Hard-code Labor Day skip in `CompletedNySession`.
- **Reversibility:** easy
- **Promote to ADR?** later, with the P2 ticket

---

## 5. Insights Surfaced

- `DataAcquisitionService.acquire` **replaces** parquet with whatever EODHD returned. A session-only fetch cannot be written without wiping history.
- `request_consumer_sync` ran on Puma and acquired every symbol in the HTTP request; Daily Analysis `timeout: 120` cannot survive a 7-year 70-name pull.
- Friday lag did not fire on 08-28 or 09-04 — those DARs scored on time. The first live wait was a **holiday**, which looks identical to vendor lag until 17:00.
- Old retry cadence was ~15 minutes (10 min pull + 5 min wait), not 5 minutes.

---

## 6. Issues & Tickets

### Resolved this session
- EODHD lag retry / second pull before 17:00 — [`docs/tickets/2026-08-18-eodhd-lag-retry-after-close.md`](../tickets/2026-08-18-eodhd-lag-retry-after-close.md) **Done**
- Friday scored-session observe — [`docs/tickets/2026-08-22-observe-friday-scored-session-dar.md`](../tickets/2026-08-22-observe-friday-scored-session-dar.md) **Done**
- Issue [`docs/issues/2026-08-22-friday-dar-hold-was-not-scored.md`](../issues/2026-08-22-friday-dar-hold-was-not-scored.md) **done**

### Deferred
- US holiday calendar on `CompletedNySession` — already filed [`docs/tickets/2026-09-07-completed-ny-session-us-holiday-calendar.md`](../tickets/2026-09-07-completed-ny-session-us-holiday-calendar.md)

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| DM retry / coverage / consumer sync / orchestrator | compose `data_manager` rspec, 18 examples | ✅ |
| Wv2 session gate + Daily Analysis job | compose `winston_v2` rspec, 5 examples | ✅ |
| Live Labor Day Not Scored | `wv2_20260907.json` 17:03 MT | ✅ |
| Friday 08-28 / 09-04 scored | notification JSON + manifests 16:30 MT | ✅ |
| Sidekiq loaded new code | `rails runner` source_location after restart | ✅ |
| Next Friday lag (print late, then appears) | not yet a live Friday-lag day | ⚠️ |
| Browser / Telegram | not opened this session | ⚠️ |

**Test command(s):**

```
./bin/compose exec -T -e RAILS_ENV=test data_manager bundle exec rspec \
  spec/services/session_coverage_spec.rb \
  spec/jobs/session_coverage_retry_job_spec.rb \
  spec/jobs/consumer_sync_job_spec.rb \
  spec/jobs/daily_data_orchestrator_job_spec.rb \
  spec/services/ecosystem_data_sync_service_spec.rb

./bin/compose exec -T -e RAILS_ENV=test -e TEST_DB_HOST=wv2_postgres winston_v2 bundle exec rspec \
  spec/services/operations/session_data_gate_spec.rb \
  spec/jobs/daily_analysis_job_spec.rb
```

---

## 8. Environment, Dependencies, Data

- **Dependencies:** None new
- **Services:** restarted `data_manager`, `data_manager_sidekiq`, `winston_v2`, `winston_v2_sidekiq` (bind-mount; no image rebuild)
- **Migrations:** none
- **Secrets:** none

---

## 9. Risks & Technical Debt

- Holiday weekdays still wait until 17:00 for a print that will never exist (P2 ticket).
- `ConsumerSyncJob` still full-acquires when the print **is** live (correct for Friday lag; expensive once).
- Probe uses one canary; a single thin name lagging AAPL still needs the post-pull `stale_among` loop.
- `EcosystemDataSyncService.demand_symbols` uses `send(:discover_by_consumer)`.

---

## 10. Open Questions

- **Should Labor Day score Friday instead of Not Scored?** — operator; blocks: P2 holiday ticket / ADR-012 addendum
- **Watch Friday 2026-09-11 if EODHD lags?** — operator; not a code blocker

---

## 11. Handoff & Resume Notes

- **Where I left off:** Retry probe live on compose; tickets closed; holiday P2 filed; wrap.
- **Next concrete step:** Optional — `CompletedNySession` US holiday calendar (P2). Or leave it and watch the next lag Friday.
- **Files to read first:**
  1. `data_manager/app/jobs/session_coverage_retry_job.rb`
  2. `data_manager/app/services/session_coverage.rb`
  3. `ecosystem/docs/adr/ADR-012-scored-session-dar-gate.md`
  4. `ecosystem/docs/tickets/2026-09-07-completed-ny-session-us-holiday-calendar.md`

---

## 12. Stakeholder Communications

- _None._ Operator-facing; no outward email.

---

## 13. Tools & Workflow Notes

- **Skills used:** `operator-prose`, `session-report`, `wrap`
- **What worked well:** Live Labor Day artifact made the retry overrun undeniable; specs were cheap once the probe vs rewrite split was clear.
- **Friction points:** Host `rg` not on PATH; compose `ps` template `.Name` failed; Sidekiq code needs restart under bind-mount.
- **Subagent usage:** _None._

---

## 14. Follow-up Actions

- [ ] `CompletedNySession` US holiday calendar — already [`docs/tickets/2026-09-07-completed-ny-session-us-holiday-calendar.md`](../tickets/2026-09-07-completed-ny-session-us-holiday-calendar.md) — owner: next session
- [ ] Optional: observe Friday 2026-09-11 if EODHD lags (probe, then one full pull, DAR scored or Not Scored — not hold) — owner: operator

---

## 15. Appendix

Labor Day Not Scored: `winston_v2/storage/cromwell_notifications/wv2_20260907.json` `generated_at=2026-09-07T23:03:49Z`.

DM retry overrun: `SessionCoverageRetryJob` jid `a7277db7230f4671439d4c51` finished `2026-09-07T23:05:39Z` elapsed 597s, latest bars `2019-07-09..2026-09-04`.
