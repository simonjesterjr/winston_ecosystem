# Session Report — DM pending migration Telegram spam

**Date:** 2026-08-19
**Time:** ~14:10–15:05 MDT
**Duration:** ~55m
**Project:** sawtooth Winston ecosystem — data_manager (DM) ops + ecosystem health watchdog
**Working directory:** `/home/johnkoisch/Documents/com/sawtooth`
**Branch:** `main` on `data_manager` and `ecosystem` (no product commits this session)
**Model:** Grok 4.6
**Operator:** johnkoisch

---

## 1. Goal & Outcome

**Stated goal:** Explain repeated Telegram messages:

`🚨 Ecosystem health DEGRADED (hourly) — FAIL data_manager: unexpected status 500` on `http://data_manager:3000/`.

**Outcome:** Delivered (ops fix on live compose DB; no product code change)

**One-line summary:** Hourly Telegram was the DM Sidekiq watchdog paging a real HTTP 500: last night’s Quiver/Alt Filing migration was in source but not applied, so Rails development blocked every request until we ran `db:migrate`.

---

## 2. Work Completed

- Traced the Telegram text to `data_manager/app/services/ecosystem_health_check_service.rb` (`EcosystemHealthCheckJob` at :10 hourly; posts only when degraded).
- Confirmed live `GET http://127.0.0.1:3001/` and `GET /up` were HTTP 500 with `ActiveRecord::PendingMigrationError` for `20260819000000_create_quiver_filings_and_sync_runs.rb`.
- Applied that additive migration in the running `data_manager` container (`quiver_sync_runs`, `quiver_filings` + indexes).
- Re-ran the live watchdog from `data_manager_sidekiq`: all six probes green (DM 200, WUT 302, Wv2 302, MCP 200, Ollama 200, nanobot 200). Host `GET /` on :3001 is 200.

---

## 3. Code Delivered

### Files changed

| File | Change | Notes |
|------|--------|-------|
| `ecosystem/docs/session-reports/2026-08-19-1505-dm-pending-migration-telegram.md` | added | This report |

**Not product code.** Live Postgres only: schema version `20260819000000`.

`data_manager/db/schema.rb` became dirty after `db:migrate` (table dump order: `symbol_registry_entries` moved below Quiver tables). Version was already `2026_08_19_000000` from the 2026-08-18 Quiver session. **Do not commit** that reorder as a schema change.

### Commits

- _None yet — wrap commit of this report only._

### Branch / PR state at sign-off

- Branch: `main` (ecosystem + data_manager) — leftover dirty trees from other sessions (see §15)
- Pushed: session report only (this wrap)
- PR: not opened (direct `main`)

---

## 4. Decisions Made

### Decision 1: Apply the pending Quiver migration on live compose
- **Choice:** Run `./bin/compose exec -T data_manager bin/rails db:migrate` immediately.
- **Why:** PendingMigrationError was taking down the entire DM HTTP surface (including `/` the watchdog probes). Additive `create_table` only. Prior session already dumped `schema.rb` and left apply as an operator question.
- **Alternatives considered:** Leave it and tell the operator to migrate; change the watchdog to probe `/up` or ignore 500s. Neither stops the 500s.
- **Reversibility:** easy (`db:rollback` drops the two new tables)
- **Promote to ADR?** no (ops apply of ADR-011 tables already decided)

---

## 5. Insights Surfaced

- Hourly Telegram “DEGRADED” is **not Cromwell**. It is DM Sidekiq `EcosystemHealthCheckJob`. Recovery hints always mention `nanobot_cromwell` / Ollama even when the only failure is DM — those lines are a generic footer.
- Rails development `PendingMigrationError` fires on **every** request. An unapplied migration after bind-mount is indistinguishable from “DM is down.”
- `schema.rb` can be committed ahead of the live DB. That is what happened 2026-08-18 (`Migrations: … not applied on sawtooth`).
- `GET /up` on DM is still **404** after migrate, despite `config/routes.rb` `get "up" => "rails/health#show"`. Watchdog uses `/` (now 200), so this did not page Telegram. Compose `ps` still shows `data_manager` as `(starting)`.

---

## 6. Issues & Tickets

### Resolved this session
- Live DM HTTP 500 / hourly Telegram DEGRADED caused by unapplied `20260819000000_create_quiver_filings_and_sync_runs` — migrated; live health check `ok=true`.

### Deferred
- Watchdog recovery hints are not probe-specific (always nanobot/ollama). See: [`docs/tickets/2026-08-20-health-watchdog-probe-specific-hints.md`](../tickets/2026-08-20-health-watchdog-probe-specific-hints.md)
- DM `GET /up` 404 vs registered `rails/health#show`. See: [`docs/tickets/2026-08-20-dm-rails-health-up-404.md`](../tickets/2026-08-20-dm-rails-health-up-404.md)
- Many compose services stuck in `(starting)` (WUT, Wv2, MCP, nanobot, BG, open-webui) — not diagnosed. See: [`docs/tickets/2026-08-20-compose-starting-healthcheck-inventory.md`](../tickets/2026-08-20-compose-starting-healthcheck-inventory.md)
- Live Alt Filing sync / `quiver.env` mount — already open in `docs/session-reports/2026-08-18-2032-git-free-cash-quiver.md` §10; tables now exist so that path is unblocked. See: [`docs/tickets/2026-08-20-mount-quiver-env-live-alt-filing-sync.md`](../tickets/2026-08-20-mount-quiver-env-live-alt-filing-sync.md)

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| Pending migration | `compose exec data_manager bin/rails db:migrate` | ✅ migrated 0.0132s |
| Schema version | `rails runner 'puts ActiveRecord::Migrator.current_version'` | ✅ `20260819000000` |
| Host DM `/` | `curl http://127.0.0.1:3001/` | ✅ 200 |
| Host DM `/up` | `curl http://127.0.0.1:3001/up` | ❌ 404 |
| Live watchdog | `EcosystemHealthCheckService.call(mode: :hourly)` from `data_manager_sidekiq` | ✅ `ok=true`, `failed=[]` |
| Next natural hourly Telegram | wait for :10 | ⚠️ not observed this session |

**Test command(s):**

```bash
./bin/compose exec -T data_manager_sidekiq bin/rails runner 'r = EcosystemHealthCheckService.call(mode: :hourly); puts({ok: r.ok, failed: r.failed}.inspect); r.checks.each { |c| puts [c[:name], c[:ok], c[:status], c[:ms], c[:error]].inspect }'
```

---

## 8. Environment, Dependencies, Data

- **Dependencies:** None
- **Services:** Existing compose stack (no restart required). DM web + Sidekiq were already up (~5h); web was 500ing.
- **Migrations:** Applied on live `data_manager_development`: `20260819000000 CreateQuiverFilingsAndSyncRuns` (create `quiver_sync_runs`, `quiver_filings`).

---

## 9. Risks & Technical Debt

- Next hourly at :10 might still send one stale DEGRADED if a job was already queued before migrate (unlikely; cron is time-based). After that, hourly should be silent while probes stay green.
- `schema.rb` dirty reorder on `data_manager` — leave uncommitted unless a later dump is intentional.
- Bind-mount + unapplied migration will 500 DM again the next time a migration is committed without `db:migrate` on this host.
- Compose `(starting)` zoo may hide real healthcheck failures unrelated to this page.

---

## 10. Open Questions

- **Why is DM `GET /up` 404?** — needs code/runtime look at `rails/health#show` vs Puma/route; blocks accurate compose healthchecks, not Telegram (watchdog uses `/`).
- **Mount quiver.env and run live Alt Filing sync?** — operator; unblocked now that tables exist. Already asked 2026-08-18.

---

## 11. Handoff & Resume Notes

- **Where I left off:** Live migrate done; watchdog green; Telegram should stop at the next :10.
- **Next concrete step:** If another DEGRADED arrives after 15:10 MDT, re-run the live `EcosystemHealthCheckService` call above. If `/up` or compose `(starting)` matters, investigate those separately.
- **Files to read first:**
  1. `data_manager/app/services/ecosystem_health_check_service.rb`
  2. `data_manager/app/jobs/ecosystem_health_check_job.rb`
  3. `data_manager/db/migrate/20260819000000_create_quiver_filings_and_sync_runs.rb`
  4. `ecosystem/docs/session-reports/2026-08-18-2032-git-free-cash-quiver.md` (migration left unapplied)

---

## 12. Stakeholder Communications

- Operator already has the live diagnosis in chat. No outward email needed.
- Telegram channel (Sawtooth Main) should go quiet on hourly DEGRADED unless a real probe fails.

---

## 13. Tools & Workflow Notes

- **Skills used:** `operator-prose`, `manage-issue-ticket` (read; no issue filed — ops miss, watchdog behaved), `session-report`, `wrap`
- **What worked well:** Hitting host :3001 and reading the Rails exception HTML (`PendingMigrationError`) instead of treating the Telegram footer as the diagnosis.
- **Friction points:** Generic recovery hints pointed at the AI profile; compose `ps` `(starting)` is noisy and not the same as the watchdog.
- **Subagent usage:** _None._

---

## 14. Follow-up Actions

- [ ] Probe-specific Telegram recovery hints in `EcosystemHealthCheckService#format_message` — owner: agent/operator — due: whenever the footer misleads again. See: [`docs/tickets/2026-08-20-health-watchdog-probe-specific-hints.md`](../tickets/2026-08-20-health-watchdog-probe-specific-hints.md)
- [ ] Diagnose DM `GET /up` 404 — owner: agent — due: if compose healthchecks matter. See: [`docs/tickets/2026-08-20-dm-rails-health-up-404.md`](../tickets/2026-08-20-dm-rails-health-up-404.md)
- [ ] Inventory why compose services sit in `(starting)` — owner: agent — due: ops hygiene. See: [`docs/tickets/2026-08-20-compose-starting-healthcheck-inventory.md`](../tickets/2026-08-20-compose-starting-healthcheck-inventory.md)
- [ ] Mount `quiver.env` and run live Alt Filing sync now that tables exist — owner: operator — due: already tracked 2026-08-18. See: [`docs/tickets/2026-08-20-mount-quiver-env-live-alt-filing-sync.md`](../tickets/2026-08-20-mount-quiver-env-live-alt-filing-sync.md)

---

## 15. Appendix (optional)

### Watchdog after migrate (from `data_manager_sidekiq`)

```text
{:ok=>true, :mode=>"hourly", :failed=>[]}
["data_manager", true, 200, 3, nil, "http://data_manager:3000/"]
["winston_unit_test", true, 302, 1, nil, "http://winston_unit_test:3000/"]
["winston_v2", true, 302, 1, nil, "http://winston_v2:3000/"]
["winston_mcp", true, 200, 1, nil, "http://winston_mcp:8088/health"]
["ollama", true, 200, 0, nil, "http://ollama:11434/"]
["nanobot_cromwell", true, 200, 1, nil, "http://nanobot_cromwell:18790/health"]
```

### Dirty trees **not** this session — do not mix into wrap commit

**ecosystem** (`M` / `??`): `CONTEXT.md`, `ai/mcp/mcp_winston/server.py`, `ai/personas/cromwell-agents.md`, `ai/schedule/*`, L1/Confirmation Intake tickets, `interfaces/winston-broker-evidence-standard.md`, `interfaces/winston-mcp-tools.md`, `ai/skills/winston-mms/`, `interfaces/fixtures/`

**data_manager:** `db/schema.rb` table-order-only dump after migrate
