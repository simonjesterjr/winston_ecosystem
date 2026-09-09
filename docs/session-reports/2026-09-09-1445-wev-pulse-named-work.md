# Session Report — WEV Pulse named work + landing redesign

**Date:** 2026-09-09
**Time:** ~09:00–14:45 MDT
**Duration:** ~5h 45m
**Project:** sawtooth Winston ecosystem — `ecosystem/`, `winston_v2`, `winston_unit_test`, `data_manager`, `broker_gateway`
**Working directory:** `/home/johnkoisch/Documents/com/sawtooth`
**Branch:** `main` on each touched repo (from `origin/main`)
**Model:** Grok 4.6
**Operator:** johnkoisch

---

## 1. Goal & Outcome

**Stated goal:** Next Winston Ecosystem View (WEV) Pulse product work — name live jobs so the Work tablet can say “Daily Analysis on Mint” / “Portfolio Backtest Run 550” instead of `busy: 1`. Then make Pulse the landing glance for estate health (Impeccable pass: full-width map, tabbed tablets, redesigned log/heartbeat, container metadata).

**Outcome:** Delivered. Named Pulse Work emit across all four monoliths; Pulse is the default plane with a health strip, full-width isometric map, container metadata dock, heartbeat (named work only), and Work / Queues / Cron tabs. Transport stays 3s poll; Action Cable not built.

**One-line summary:** Pulse now names real work on each owner’s Redis HASH and opens as the ecosystem landing page; queue dumps and empty broker polls no longer pretend to be a live ticker.

---

## 2. Work Completed

- Catalogued nameable work per monolith (by category). Silence policy: tickle, health, expected_returns graveyard, Turbo broadcasts, empty Confirmation Intake / WQ fill / coverage retry.
- Contract: Pulse Work Record on `winston-ecosystem-view-pulse/v1`. Redis `wev:pulse:work` HASH + `wev:pulse:recent` LIST + `PUBLISH wev:pulse` on each owner DB (`/0..3`). Poll and a later Cable subscriber are both readers of the same JSON.
- `PulseWork` / `PulseWork::Store` copied into data_manager (DM), Winston Unit Test (WUT), Winston v2 (Wv2), Broker Gateway (BG). Opt-in `around_perform` plus `PulseWork.wrap` for request-path services. MCP `perform_now` is visible.
- Wv2 projector prefers named HASH for `owners.*.jobs[]`. Sidekiq `:work` is fallback only and **excludes** `ExpectedReturn` / tickle / health / Cable broadcast. Queued args are **not** Work rows.
- Pulse UI: landing plane; health chips; full-width map; click cuboid → container metadata (what / for / helps Winston / listen / this sample / queues / last named work); Heartbeat = sample clock + named start/finish; tablets on tabs.
- Noise fix after operator screenshot: empty BG `RefreshService` polls no longer emit; ticker no longer dumps `CalculateExpectedReturnJob` args.
- Restarted `winston_v2_sidekiq`, `winston_unit_test_sidekiq`, `data_manager_sidekiq`, `broker_gateway_sidekiq`.

---

## 3. Code Delivered

### Files changed (this session only — do not stage the rest of the dirty trees)

#### ecosystem

| File | Change | Notes |
|------|--------|-------|
| `interfaces/winston-ecosystem-view-v1.md` | modified | Pulse Work Record, Redis keys, kind enum, silence rules |
| `plans/winston-ecosystem-view.md` | modified | Key decision 7: named work on owner Redis |
| `docs/tickets/2026-09-08-wev-pulse-other-monolith-emits.md` | modified | P2 In progress; checklist of emits |
| `docs/tickets/2026-09-07-winston-ecosystem-view.md` | modified | Named emit in progress; Cable still later |
| `docs/tickets/INDEX.md` | modified | Emit ticket P2 In progress |
| `docs/session-reports/2026-09-09-1445-wev-pulse-named-work.md` | added | this report |

**Do not stage this session:** `AGENTS.md`, `CONTEXT.md`, `docs/README.md`, ADR-013, desk business-context, unrelated tickets, `hints/`, `plans/cromwell-staff-roster.md`, `vendor/`.

#### winston_v2

| File | Change | Notes |
|------|--------|-------|
| `app/services/pulse_work.rb` | added | opt-in emit + `wrap` |
| `app/services/pulse_work/store.rb` | added | HASH / recent / PUBLISH; memory mode for specs |
| `app/jobs/daily_analysis_job.rb` | modified | named Daily Analysis |
| `app/jobs/mid_month_scoreboard_job.rb` | modified | wrap only when due |
| `app/jobs/confirmation_intake_job.rb` | modified | emit only when worth it or explicit binding |
| `app/jobs/quiver_tracking/working_fill_job.rb` | modified | emit only with working legs |
| `app/jobs/quiver_tracking_ingest_job.rb` | modified | WQ ingest |
| `app/jobs/quiver_congress_long_short_digest_job.rb` | modified | digest + subject progress |
| `app/jobs/quiver_congress_long_short_rebalance_job.rb` | modified | weekly package |
| `app/services/operations/daily_analysis_runner.rb` | modified | `progress!` current Operational Portfolio |
| `app/services/market_snapshot_service.rb` | modified | one hourly-radar row, not per-symbol |
| `app/services/operations/ecosystem_pulse.rb` | modified | named HASH; silent-class fallback; no queued dump |
| `app/views/operations/ecosystem/show.html.erb` | modified | Pulse landing, map, dock, tabs |
| `public/ecosystem/wev-live.js` | modified | health chips, metadata, heartbeat, tabs, noise filter |
| `public/ecosystem/wev-live.css` | modified | full-width map, dock, tablets |
| `spec/services/pulse_work/store_spec.rb` | added | |
| `spec/services/operations/ecosystem_pulse_named_work_spec.rb` | added | titles + no ExpectedReturn |
| `spec/jobs/daily_analysis_job_spec.rb` | modified | perform_now emit |
| `spec/jobs/mid_month_scoreboard_job_spec.rb` | modified | skip is silent |
| `spec/jobs/quiver_tracking/working_fill_job_spec.rb` | modified | idle is silent |
| `spec/requests/operations_ecosystem_spec.rb` | modified | Pulse landing markup |

**Do not stage:** WQ / Fulfillment Desk / Session Order Slate / ops-shell / `db/schema.rb` / other dirty files.

#### winston_unit_test

| File | Change | Notes |
|------|--------|-------|
| `app/services/pulse_work.rb` + `store.rb` | added | copy of Store |
| `app/jobs/portfolio_backtest_job.rb` | modified | hero title `PBR {id} · {name}` |
| `app/jobs/backtest_job.rb` | modified | single-market |
| `app/jobs/portfolio_signal_optimization_job.rb` | modified | |
| `app/jobs/daily_operations_job.rb` | modified | |
| `app/jobs/daily_paper_trading_job.rb` | modified | |
| `app/jobs/refresh_portfolio_data_job.rb` | modified | subject walks symbols |
| `app/jobs/portfolio_correlation_daily_score_job.rb` | modified | |
| `app/jobs/quiver_lab_snapshot_job.rb` | modified | |
| `app/jobs/quiver_lab_backtest_job.rb` | modified | |
| `app/jobs/dm_registry_sync_job.rb` | modified | |
| `app/jobs/data_set_dm_sync_job.rb` | modified | |
| `app/jobs/active_accounts_backup_job.rb` | modified | |
| `spec/services/pulse_work/store_spec.rb` | added | |
| `spec/jobs/portfolio_backtest_job_pulse_spec.rb` | added | |

Silent (unchanged): `CalculateExpectedReturnJob`, `PostBacktestExpectedReturnJob`, `BroadcastBacktestUpdateJob`.

**Do not stage:** `docs/tickets/INDEX.md` or untracked ponytail / expected_returns tickets.

#### data_manager

| File | Change | Notes |
|------|--------|-------|
| `app/services/pulse_work.rb` + `store.rb` | added | |
| `app/services/dm_pulse_progress.rb` | modified | Redis acquire row beside DownloadTask |
| `app/jobs/daily_data_orchestrator_job.rb` | modified | Daily EOD sync |
| `app/jobs/weekend_data_sync_job.rb` | modified | |
| `app/jobs/ecosystem_sync_request_job.rb` | modified | |
| `app/jobs/consumer_sync_job.rb` | modified | |
| `app/jobs/quiver_sync_job.rb` | modified | Alt Filing sync |
| `app/jobs/session_coverage_retry_job.rb` | modified | only when stale |
| `spec/services/pulse_work/store_spec.rb` | added | |
| `spec/services/ecosystem_data_sync_service_spec.rb` | modified | IBM acquire named row |

Silent: `EcosystemHealthCheckJob`.

#### broker_gateway

| File | Change | Notes |
|------|--------|-------|
| `app/services/pulse_work.rb` + `store.rb` | added | |
| `app/services/evidence/refresh_service.rb` | modified | emit on desk/force/scenario or `events_appended > 0`; empty poll silent |
| `app/services/evidence/place_order_service.rb` | modified | after policy gate |
| `app/services/evidence/sandbox_fills_service.rb` | modified | dummy_sim only |
| `spec/services/pulse_work/store_spec.rb` | added | |
| `spec/jobs/adapters/ibkr/tickle_job_spec.rb` | modified | tickle does not write |
| `spec/services/evidence/refresh_service_spec.rb` | modified | emit vs duplicate poll |

Silent: `Adapters::Ibkr::TickleJob`.

**Do not stage:** IBKR adapter/session/account_snapshot, `config/sidekiq_schedule.yml`, `tmp/`, `vendor/`.

### Commits

- _None yet — wrap Step 2 (follow-up promotion) runs before commit._

### Branch / PR state at sign-off

- Branch: `main` on five repos — dirty (this session + unrelated work)
- Pushed: no
- PR: not opened (commit to `main` is the house pattern)

---

## 4. Decisions Made

### Decision 1: Pulse Work Record is the contract; poll is a reader
- **Choice:** Owner Redis HASH `wev:pulse:work` + `PUBLISH wev:pulse`. Wv2 GET still polls 3s while the Pulse tab is open.
- **Why:** Action Cable without a write-path is a server poller. MCP `perform_now` is invisible to Sidekiq `:work`.
- **Alternatives considered:** Improve args_hint parsing; `/internal/pulse` on every monolith; Turbo Frame timer; Cable first.
- **Reversibility:** easy
- **Promote to ADR?** no — interface + WEV plan key decision 7

### Decision 2: Silence is the product
- **Choice:** Do not emit tickle, health, expected_returns, Cable broadcast, or empty cron polls.
- **Why:** Operator screenshot showed Work/ticker drowned in `CalculateExpectedReturnJob` and 5‑minute BG refresh.
- **Alternatives considered:** Show everything Sidekiq knows.
- **Reversibility:** easy (add `pulse_record`)
- **Promote to ADR?** no

### Decision 3: Pulse is the WEV landing plane
- **Choice:** Default tab Pulse. Map full width. Tablets on tabs. Container metadata + heartbeat dock (not a competing column of poll lines).
- **Why:** Operator asked for estate-health glance; Poster is intended topology, not live.
- **Alternatives considered:** Keep Poster first; keep three tables side by side.
- **Reversibility:** easy (swap `class="on"`)
- **Promote to ADR?** no

### Decision 4: Four copies of Store, no gem
- **Choice:** Identical `PulseWork::Store` in each monolith. Schema owned by the interface.
- **Why:** No shared lib load path; no fifth compose service.
- **Alternatives considered:** ecosystem gem; Redis `/4` “for WEV”.
- **Reversibility:** easy
- **Promote to ADR?** no — drift is the risk (see §9)

---

## 5. Insights Surfaced

- Wv2 already peeked sibling Redis `/0..3`. Named work did not need new HTTP endpoints on WUT/BG.
- Sidekiq queued-args fallback is how 227k `expected_returns` became the ticker. Queue **depth** belongs on Queues; job **identity** belongs on Work.
- BG tickle is the only BG Sidekiq class. Named BG work is request-path (`RefreshService`, `PlaceOrderService`). Confirmation Intake’s 5‑minute refresh is not “work” unless it appended events.
- Pulse Work `PUBLISH` is unused today; Cable can subscribe later without changing job instrumentation.
- Compose healthchecks stay `starting` forever for several services; Pulse must not invent container liveness from that. No `docker.sock`.

---

## 6. Issues & Tickets

### Resolved this session
- Named Pulse Work emit — ticket `docs/tickets/2026-09-08-wev-pulse-other-monolith-emits.md` implemented (leave In progress until operator visual QA).
- Pulse landing layout + noise — no separate ticket; parent WEV ticket.

### Deferred
- Action Cable / Turbo Frame — already filed: `2026-09-08-wev-pulse-action-cable.md`, `2026-09-08-wev-pulse-turbo-frame.md`. Skip until a desk needs ≪3s **and** Tailscale WebSocket works.
- Operator visual QA of Pulse landing (hard-refresh; click cuboids; confirm Work is quiet when idle).
- WUT `expected_returns` drain (~227k, no worker `-q`) — Pulse finding from 2026-09-07; still a graveyard. Untracked WUT ticket `winston_unit_test/docs/tickets/2026-09-09-wut-expected-returns-queue-graveyard.md` exists from another session — do not duplicate blindly.
- Host/container live status (podman) remains UNKNOWN on Tailscale — no docker.sock; `last.json` still absent.
- Four-copy `PulseWork::Store` drift.
- Impeccable `detect.mjs` / finish-reviewer not run (no host `node`; no browser MCP).
- Code plane visual QA — already filed `2026-09-09-wev-code-plane-visual-qa.md`.

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| Wv2 Pulse Work + landing markup | `bundle exec rspec` (compose, `TEST_DB_HOST=wv2_postgres`) store, named-work, DA, MMS, working-fill, ecosystem request | ✅ 13 then 7 examples, 0 failures |
| WUT Store + PBR title | compose `TEST_DB_HOST=wut_postgres` | ✅ 2 examples, 0 failures |
| DM Store + IBM acquire row | compose `TEST_DB_HOST=postgres` | ✅ 10 examples, 0 failures |
| BG Store, tickle silent, refresh emit/duplicate | compose `TEST_DB_HOST=bg_postgres` | ✅ new examples pass; one pre-existing IBKR fixture `auth_failed` (env) |
| Live Pulse JSON | `curl /wv2/operations/ecosystem/pulse` | ✅ jobs[] empty (quiet); `ExpectedReturn` absent; queues still show expected_returns depth |
| Live Pulse HTML | curl WEV page | ✅ Pulse default plane, tabs, map, meta, heartbeat |
| Browser clickthrough | operator + Impeccable | ⚠️ no browser MCP this session |
| Sidekiq restart | `bin/compose restart` four workers | ✅ Up ~10s after restart |

**Test command(s):**

```bash
./bin/compose exec -T -e RAILS_ENV=test -e TEST_DB_HOST=wv2_postgres -e TEST_DB_USER=sawtooth -e TEST_DB_PASSWORD=sawtooth winston_v2 \
  bundle exec rspec spec/services/pulse_work/store_spec.rb spec/services/operations/ecosystem_pulse_named_work_spec.rb \
  spec/jobs/daily_analysis_job_spec.rb spec/jobs/mid_month_scoreboard_job_spec.rb \
  spec/jobs/quiver_tracking/working_fill_job_spec.rb spec/requests/operations_ecosystem_spec.rb

./bin/compose exec -T -e RAILS_ENV=test -e TEST_DB_HOST=wut_postgres -e TEST_DB_USER=sawtooth -e TEST_DB_PASSWORD=sawtooth winston_unit_test \
  bundle exec rspec spec/services/pulse_work/store_spec.rb spec/jobs/portfolio_backtest_job_pulse_spec.rb

./bin/compose exec -T -e RAILS_ENV=test -e TEST_DB_HOST=postgres -e TEST_DB_USER=postgres -e TEST_DB_PASSWORD=password data_manager \
  bundle exec rspec spec/services/pulse_work/store_spec.rb spec/services/ecosystem_data_sync_service_spec.rb \
  spec/requests/internal_pulse_spec.rb spec/jobs/consumer_sync_job_spec.rb

./bin/compose exec -T -e RAILS_ENV=test -e TEST_DB_HOST=bg_postgres broker_gateway \
  bundle exec rspec spec/services/pulse_work/store_spec.rb spec/jobs/adapters/ibkr/tickle_job_spec.rb \
  spec/services/evidence/refresh_service_spec.rb spec/services/evidence/place_order_service_spec.rb \
  spec/services/evidence/sandbox_fills_service_spec.rb
```

---

## 8. Environment, Dependencies, Data

- **Dependencies:** None new. `turbo-rails` still unused on ops-shell. Action Cable still commented out in Wv2 `application.rb`.
- **Services:** Four Sidekiq workers restarted. No compose rebuild. Bind-mounted source.
- **Migrations:** None this session. Unrelated Wv2 `session_order_slates` migration is **not** this wrap.

---

## 9. Risks & Technical Debt

- Four identical Store copies will drift if someone “improves” one.
- `expected_returns` depth still 227000 — honest on Queues / WUT chip; do not “fix” by hiding the number.
- Heartbeat still can show BG refresh when a poll **does** append events (intended).
- Container metadata is a JS catalog in `wev-live.js`, not generated from `runtime.yaml` — can drift from compose.
- Unrelated dirty trees (WQ, slates, ponytail tickets) are large; wrap must stage **only** Pulse files.

---

## 10. Open Questions

- **Is Pulse the permanent landing plane?** — operator; blocks nav order only.
- **Should empty Pulse Work HASH hide the Work tab empty-state copy about expected_returns?** — copy; not blocking.
- **When does Cable become worth Tailscale WebSocket risk?** — operator; already ticketed.

---

## 11. Handoff & Resume Notes

- **Where I left off:** Pulse landing shipped in bind-mount; operator should hard-refresh (`wev-live.js?v=20260909q`). Wrap not yet committed.
- **Next concrete step:** Visual QA on Pulse (idle = Quiet; click `data_manager` / `winston_v2` / `redis`; Work tab empty; Queues shows expected_returns depth). Then commit Pulse files only.
- **Files to read first:**
  1. `ecosystem/interfaces/winston-ecosystem-view-v1.md` (Pulse Work Record)
  2. `winston_v2/app/services/pulse_work.rb` + `operations/ecosystem_pulse.rb`
  3. `winston_v2/app/views/operations/ecosystem/show.html.erb` Pulse section
  4. `ecosystem/docs/tickets/2026-09-08-wev-pulse-other-monolith-emits.md`

---

## 12. Stakeholder Communications

- Operator: Pulse is the estate-health door. Quiet means no **named** work, not “Redis is empty.” WUT expected_returns is a known graveyard, not a live backtest.

---

## 13. Tools & Workflow Notes

- **Skills used:** operator-prose, wrap, session-report, impeccable (Operate / distill / layout; `context.mjs` failed — no host `node`)
- **What worked well:** Contract-first Redis HASH; silence policy after a real screenshot; compose exec rspec with `TEST_DB_HOST`.
- **Friction points:** Host has no `node` for Impeccable scripts. Dirty trees from other sessions dwarf this slice. `bin/compose ps --format` failed (podman template).
- **Subagent usage:** none

---

## 14. Follow-up Actions

- [ ] Operator Pulse visual QA (hard-refresh, cuboid click, idle Quiet) — owner: johnkoisch — due: this desk session. See: `plans/winston-ecosystem-view.md.tasks.json#1`
- [ ] Mark emit ticket Done after QA — owner: agent after QA — due: same day. See: `docs/tickets/2026-09-08-wev-pulse-other-monolith-emits.md` (already In progress; flip to Done after task 1)
- [ ] Action Cable / Turbo — skip until ≪3s + Tailscale WS. See: `docs/tickets/2026-09-08-wev-pulse-action-cable.md`, `docs/tickets/2026-09-08-wev-pulse-turbo-frame.md` (no new artifact)
- [ ] Pulse container metadata source of truth — **grill, do not implement YAML yet**. See: `docs/tickets/2026-09-09-wev-pulse-container-catalog-sot.md`
- [ ] PulseWork::Store one component (import first; single deploy only if import fails). See: `docs/tickets/2026-09-09-wev-pulse-work-store-single-component.md`
- [ ] WUT `expected_returns` stop-producing (or add worker). See: `winston_unit_test/docs/tickets/2026-09-09-wut-expected-returns-queue-graveyard.md` (**P2**; WUT INDEX + ecosystem INDEX). Drain 2026-09-09 does not stop refill.

---

## 15. Appendix (optional)

Live Pulse JSON at wrap (`GET /wv2/operations/ecosystem/pulse`): all four owners `status=ok`, `jobs=[]`, WUT `queues.expected_returns=227000`. Headline should be **Quiet**, not a job dump.

Sidekiq restart (session): `data_manager_sidekiq`, `winston_unit_test_sidekiq`, `winston_v2_sidekiq`, `broker_gateway_sidekiq`.
