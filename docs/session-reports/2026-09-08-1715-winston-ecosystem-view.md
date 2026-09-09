# Session Report — Winston Ecosystem View (four planes + DM Pulse emit + Code polish)

**Date:** 2026-09-08
**Time:** ~09-07 tournament through 17:15 MDT (continued session; last slice = Code plane)
**Duration:** multi-hour, two calendar days, one wrap
**Project:** sawtooth Winston ecosystem — `ecosystem/`, `winston_v2`, `data_manager`
**Working directory:** `/home/johnkoisch/Documents/com/sawtooth`
**Branch:** `main` on `ecosystem`, `winston_v2`, `data_manager` (each from `origin/main`)
**Model:** Grok 4.6
**Operator:** johnkoisch

---

## 1. Goal & Outcome

**Stated goal:** Winston Ecosystem View (WEV) — a four-plane, non-game operator console (Poster / Codebase / Pulse / Book Board) of how Winston actually runs. Canonical monoliths: winston_v2 (Wv2), winston_unit_test (WUT), data_manager (DM), broker_gateway (BG). Later slices: real Isoflow poster; live Pulse (DM pulling IBM); Pulse/Book/Code UI revisions; Code sub-tabs + metadata + document reader.

**Outcome:** Delivered for v1 console + DM Pulse emit. WebSockets not built (tickets filed). Code plane v2 (tabs / metadata / reader) implemented this wrap slice. Uncommitted at sign-off pending follow-up promotion.

**One-line summary:** Ops-shell **Ecosystem** tab shows intended topology, live work (including DM acquire), Active Operational Portfolios as stacked cash/equity cubes, and a Code map that explains each cuboid and opens Architecture Decision Records (ADRs) / tickets / plans under the diagram.

---

## 2. Work Completed

- Tournament A/B/C judged. Synthesis: A ownership + B entry + C board math. Isolation via git worktrees **failed** (no `.git` at sawtooth root); candidates wrote the shared tree; kept as `plans/winston-ecosystem-view-candidate-{a,b,c}.md` (record, not source of truth).
- Plan + contracts: `ecosystem/plans/winston-ecosystem-view.md`, `ecosystem/interfaces/winston-ecosystem-view-v1.md`.
- Glossary in `ecosystem/CONTEXT.md`: WEV, Score Projection, Book Board slab ≠ Book row, execution_mode `paper`|`real` (not live).
- Isoflow-style poster SVG: `ecosystem/docs/poster/winston-topology.svg` copied to `winston_v2/public/ecosystem/`.
- Inventory CLI: `ecosystem/ecosystem_view/bin/inventory`.
- Wv2 door: `GET /operations/ecosystem` + `GET /operations/ecosystem/pulse` (3s poll). Linked from ops-shell header. First paint is Operational Portfolio SQL + local Sidekiq `/2`; sibling Redis peeks are Pulse, not scores. No `docker.sock`. No BookScore engine.
- Pulse UI: same isometric map; click cuboid → that owner’s log; queues/cron/work as **flat tables**.
- DM Pulse emit: `DmPulseProgress` writes `DownloadRun` + `DownloadTask status=running` **before** acquire and finishes after. Wired into `EcosystemDataSyncService` and `ConsumerSyncJob`. **Does not** Cromwell-emit per-symbol start (Telegram would flood). `GET /internal/pulse`.
- Live demo: IBM consumer sync (~4s); then six uncovered names (SHOP, MELI, SNOW, NET, TEAM, MDB) so the map stayed live longer.
- Book Board: graphic **Active only** (real vs paper pads); stacked cubes (blue deployed / green free cash) from `RiskEquity.snapshot` on Active OPs only; click slab → metadata pane; table lists Active + count of omitted inactive.
- Code plane v1: top-down cuboids ecosystem (general contractor) → dm / wut / wv2 / bg; wq under wv2 (Quiver Tracking desk, not a fifth monolith).
- Code plane v2: sub-tabs **ADRs | tickets / issues | plans**; click row opens markdown **under** the cuboids; metadata pane answers what / for / helps Winston / externals / in-estate peers. Catalog fetched from `/ecosystem/work.json` (285 items, ~1.1 MB) — not inlined in HTML.
- Tickets booked (not implemented): Turbo Frame Pulse (no Cable); Action Cable + Tailscale `/wv2/cable`; Pulse emit from WUT / Wv2 / BG jobs.

---

## 3. Code Delivered

### Files changed

#### ecosystem (this session — stage these)

| File | Change | Notes |
|------|--------|-------|
| `CONTEXT.md` | modified | WEV + Score Projection + Book Board glossary. **Also contains** a Quiver Tracking “Blow away” glossary tweak that was already dirty — review before commit. |
| `docs/tickets/INDEX.md` | modified | Three Pulse follow-on tickets + parent WEV |
| `docs/tickets/2026-09-07-winston-ecosystem-view.md` | added | Parent ticket (In progress) |
| `docs/tickets/2026-09-08-wev-pulse-turbo-frame.md` | added | P2 Proposed |
| `docs/tickets/2026-09-08-wev-pulse-action-cable.md` | added | P2 Proposed |
| `docs/tickets/2026-09-08-wev-pulse-other-monolith-emits.md` | added | P3 Proposed |
| `interfaces/winston-ecosystem-view-v1.md` | added | Pulse/board contracts |
| `plans/winston-ecosystem-view.md` | added | Applied synthesis |
| `plans/winston-ecosystem-view-candidate-{a,b,c}.md` | added | Tournament record |
| `docs/poster/*` | added | Isoflow SVG + FossFLOW JSON + dsl |
| `ecosystem_view/**` | added | inventory, render_poster, index_work, static app, catalog |
| `docs/session-reports/2026-09-08-1715-winston-ecosystem-view.md` | added | this report |

#### winston_v2 (this session — stage these)

| File | Change | Notes |
|------|--------|-------|
| `config/routes.rb` | modified | `operations/ecosystem` + pulse only (diff is clean) |
| `app/views/operations/home/index.html.erb` | modified | Ecosystem header link only (diff is clean) |
| `app/controllers/operations/ecosystem_controller.rb` | added | HTML + JSON board; pulse JSON; poster SVG; does **not** embed work.json |
| `app/services/operations/ecosystem_board.rb` | added | OP list + stack_for Active only |
| `app/services/operations/ecosystem_pulse.rb` | added | Redis DBs 0–3 + DM `/internal/pulse` |
| `app/views/operations/ecosystem/show.html.erb` | added | Four planes |
| `public/ecosystem/wev-live.js` | added | Poll, Pulse log, Book cubes, Code tabs/meta/reader |
| `public/ecosystem/wev-live.css` | added | Split panes, work tabs, doc pane |
| `public/ecosystem/winston-topology.svg` | added | Copy of poster |
| `public/ecosystem/work.json` | added | Generated catalog (nodes + clipped bodies) |
| `spec/requests/operations_ecosystem_spec.rb` | added | 5 examples, 0 failures |

#### data_manager (this session — stage these)

| File | Change | Notes |
|------|--------|-------|
| `app/services/dm_pulse_progress.rb` | added | DownloadRun/Task around acquire |
| `app/services/ecosystem_data_sync_service.rb` | modified | Wire progress |
| `app/jobs/consumer_sync_job.rb` | modified | Wire progress; `notify_cromwell: false` on this path as before |
| `app/controllers/internal_controller.rb` | modified | `GET /internal/pulse` |
| `config/routes.rb` | modified | pulse route |
| `spec/jobs/consumer_sync_job_spec.rb` | modified | running task during acquire |
| `spec/services/ecosystem_data_sync_service_spec.rb` | modified | same |
| `spec/requests/internal_pulse_spec.rb` | added | host! localhost |

**Not this session (do not stage)**

- `ecosystem/AGENTS.md`, `ecosystem/docs/README.md` — `/ponytail` skill line
- `ecosystem/hints/wq-blow-away-not-ops-reset.md`
- `ecosystem/plans/cromwell-staff-roster.md`
- `ecosystem/vendor/`
- Wv2 Quiver Tracking / Fulfillment dirty tree: `confirmation_intake/ingest_orchestrator.rb`, `fulfillment_catalog.rb`, `fulfillment_desk.rb`, `operations/quiver_tracking.rb`, `quiver_tracking/*`, `quiver_tracking` views, `config/sidekiq_schedule.yml`, `spec/requests/quiver_tracking_page_spec.rb`, untracked `app/jobs/quiver_tracking/`, `app/services/quiver_tracking/desk_fulfillment.rb` + specs

### Commits

- _None yet — wrap paused at follow-up promotion._

### Branch / PR state at sign-off

- Branch: `main` on three repos — dirty
- Pushed: no
- PR: not opened

---

## 4. Decisions Made

### Decision 1: Four planes, not a game
- **Choice:** Poster / Code / Pulse / Book Board. Pulse ≠ PnL. Book Board slabs are Operational Portfolios, not Book rows. Mode `paper`|`real`.
- **Why:** Operator asked for how Winston actually runs; ADR-001/006 language.
- **Alternatives considered:** Winston World / city / weather; DragonRuby (candidate C, dropped).
- **Reversibility:** easy (UI)
- **Promote to ADR?** no — CONTEXT glossary + interface is enough

### Decision 2: Wv2 hosts the human door; ecosystem owns contracts/poster
- **Choice:** `GET /operations/ecosystem` in Wv2; code/docs in `ecosystem/`.
- **Why:** Tailscale Serve `/wv2` cannot see sibling HTTP or podman; ADR-005 first paint must not hang.
- **Alternatives considered:** static HTML only (A); docker.sock Pulse (B, dropped).
- **Reversibility:** easy
- **Promote to ADR?** no

### Decision 3: DM emit now; WebSockets later
- **Choice:** `DownloadTask` running during acquire; Pulse stays 3s HTTP poll. Do **not** Cromwell-notify per-symbol start.
- **Why:** Operator wanted IBM visible *while* pulling. Cable needs `cable.yml` + Tailscale `/wv2/cable` (2–4 days). Telegram would flood if start events went to Cromwell.
- **Alternatives considered:** TestDownloadsController (bypasses DownloadTask); Action Cable in this session.
- **Reversibility:** easy
- **Promote to ADR?** no — tickets filed

### Decision 4: Code plane is docs + node metadata, not git/CI health
- **Choice:** Catalog ADRs/tickets/issues/plans via `index_work` → `public/ecosystem/work.json`. Cuboid metadata is authored in the indexer `NODES` list. Fetch JSON; do not inline bodies in HTML.
- **Why:** `ecosystem/docs` is not mounted in the Wv2 container. 285 bodies in a data attribute would bloat first paint.
- **Alternatives considered:** live scan from Rails; fifth cuboid for WQ as a monolith (rejected — WQ is a desk).
- **Reversibility:** easy
- **Promote to ADR?** no

### Decision 5: Book Board graphics = Active only; stack = free cash + deployed
- **Choice:** Inactive OPs stay in a table footnote. Height from `RiskEquity.snapshot` on Active OPs only (do not first-paint parquet for all).
- **Why:** Operator: do not graphically show lots of inactive portfolios; show stacked score.
- **Alternatives considered:** candidate C full rack of every OP (would hang / clutter).
- **Reversibility:** easy
- **Promote to ADR?** no

---

## 5. Insights Surfaced

- Pulse cannot show “Downloading IBM” unless DM writes `DownloadTask` **before** the HTTP acquire. Schema existed; writers did not.
- A single IBM pull finishes in ~4s — operator can miss the live frame. Longer uncovered symbols keep the map honest.
- WUT Redis `/1` `expected_returns` ~227k is a producer-only graveyard; Pulse must not treat queue depth as SLO.
- `ibkr_tickle` `last_enqueue_time` is often empty, so BG tickle flow is frequently absent on the map.
- WQ is a Wv2 desk (`/quiver_tracking`), not a fifth Rails app. Code cuboid sits under wv2.
- Work-item `owner_for` is a keyword heuristic — plans that mention `data_manager` can land on `dm` even when they are cross-cutting.

---

## 6. Issues & Tickets

### Resolved this session
- Parent WEV ticket still **In progress**; v1 console + DM emit + Code v2 shipped in working trees (uncommitted).
- DM Pulse emit: done (follow-on on parent ticket).

### Deferred
- Already filed: `2026-09-08-wev-pulse-turbo-frame.md`, `2026-09-08-wev-pulse-action-cable.md`, `2026-09-08-wev-pulse-other-monolith-emits.md`.
- Already listed on parent ticket: Tailscale host inventory without lying; Score Projection after first paint; real code-health (git/CI); OpenTelemetry; promotion gate; `expected_returns` drain.
- Filed 2026-09-09 as WEV children: `2026-09-09-wev-code-plane-visual-qa.md`, `2026-09-09-wev-index-work-owner-heuristic.md`, `2026-09-09-wev-index-work-refresh-hook.md`, `2026-09-09-wev-work-json-split-bodies.md`.

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| Wv2 Ecosystem request specs | `./bin/compose exec -T -e RAILS_ENV=test -e TEST_DB_HOST=wv2_postgres winston_v2 bundle exec rspec spec/requests/operations_ecosystem_spec.rb` | ✅ 5 examples, 0 failures |
| DM Pulse emit specs | compose rspec `ecosystem_data_sync_service_spec`, `consumer_sync_job_spec`, `internal_pulse_spec` (earlier in session) | ✅ 8 examples, 0 failures (as recorded; not re-run at wrap) |
| HTML / static assets | `curl` `:3002/operations/ecosystem`, `wev-live.js?v=20260908c`, `work.json` | ✅ 200; markup includes tabs/meta/doc pane; work.json 1 112 612 bytes |
| Pulse live IBM / six names | POST DM `request_consumer_sync` | ✅ earlier in session (IBM ~4s; SHOP MELI SNOW NET TEAM MDB queued) |
| Code plane click/tabs/reader | browser | ⚠️ no browser MCP this wrap; JS/CSS/catalog served; operator should hard-open Code tab |
| Book Board stacked cubes | request spec + earlier UI | ⚠️ request spec checks Active copy, not canvas pixels |
| Action Cable | not built | — |

**Test command(s):**

```bash
./bin/compose exec -T -e RAILS_ENV=test -e TEST_DB_HOST=wv2_postgres winston_v2 \
  bundle exec rspec spec/requests/operations_ecosystem_spec.rb
# DM (from earlier slice; TEST_DB_USER=postgres, host! localhost):
./bin/compose exec -T -e RAILS_ENV=test -e TEST_DB_HOST=dm_postgres -e TEST_DB_USER=postgres data_manager \
  bundle exec rspec spec/services/ecosystem_data_sync_service_spec.rb \
  spec/jobs/consumer_sync_job_spec.rb spec/requests/internal_pulse_spec.rb
```

---

## 8. Environment, Dependencies, Data

- **Dependencies:** none added
- **Services:** existing compose (`data_manager` :3001, `winston_v2` :3002). No new service. No `--profile ai` required.
- **Migrations:** none (DownloadRun/DownloadTask tables already existed)
- **Generated:** `python3 ecosystem/ecosystem_view/bin/index_work` → catalog + `winston_v2/public/ecosystem/work.json`

---

## 9. Risks & Technical Debt

- `work.json` is a generated snapshot. Stale after new ADRs/tickets unless indexer is re-run.
- Keyword `owner_for` mis-tags some cross-cutting plans onto `dm`.
- Pulse 3s poll on Tailscale; Turbo/Cable tickets exist.
- Tournament isolation is broken at workspace root (no git) — `WORK_GRAPH.md` contractor mode cannot worktree-isolate without per-monolith remotes.
- Unrelated dirty trees in Wv2 (WQ/fulfillment) and ecosystem (ponytail, vendor, Cromwell roster) — easy to commit by accident if someone `git add .`.

---

## 10. Open Questions

- **Does the operator want Score Projection on Book Board next, or leave UNKNOWN?** — operator; blocks parent-ticket follow-on.
- **Is 1.1 MB work.json acceptable on first Code-tab open?** — operator; optional split of index vs bodies.
- **Should Blow-away glossary hunk in CONTEXT.md ride along with this commit?** — operator; mixed file.

---

## 11. Handoff & Resume Notes

- **Where I left off:** Code plane v2 in working trees; wrap at follow-up promotion; nothing committed.
- **Next concrete step:** operator shortcut on §14; then commit the three precise file lists (not `git add .`); push `main`.
- **Files to read first:**
  1. `ecosystem/plans/winston-ecosystem-view.md`
  2. `ecosystem/interfaces/winston-ecosystem-view-v1.md`
  3. `winston_v2/public/ecosystem/wev-live.js` (Code section from `selectedCode`)
  4. `data_manager/app/services/dm_pulse_progress.rb`
  5. `ecosystem/ecosystem_view/bin/index_work` (`NODES`)

Pages: `http://127.0.0.1:3002/operations/ecosystem` and Tailscale `/wv2/operations/ecosystem`. Cache-bust `?v=20260908c`.

---

## 12. Stakeholder Communications

- _None._ Operator-facing console only.

---

## 13. Tools & Workflow Notes

- **Skills used:** wrap, session-report, operator-prose (this closeout). Earlier slices: contractor + tournament + adversary (WEV design).
- **What worked well:** inventory-first; UNKNOWN instead of invented services; fetching work.json instead of data attributes.
- **Friction points:** no git at sawtooth root (tournament isolation); no browser MCP at wrap; `TEST_DB_HOST=wv2_postgres` not localhost; DM pulse specs need `host! "localhost"`.
- **Subagent usage:** tournament candidates earlier; not used in Code v2 slice.

---

## 14. Follow-up Actions

Already filed (do not duplicate unless redesign):

- [ ] Pulse Turbo Frame — `docs/tickets/2026-09-08-wev-pulse-turbo-frame.md`
- [ ] Pulse Action Cable — `docs/tickets/2026-09-08-wev-pulse-action-cable.md`
- [ ] Pulse emit WUT/Wv2/BG — `docs/tickets/2026-09-08-wev-pulse-other-monolith-emits.md`
- [ ] Parent remaining: Tailscale inventory honesty, Score Projection, git/CI code-health, OTel, promotion gate, `expected_returns` — `docs/tickets/2026-09-07-winston-ecosystem-view.md`

Filed 2026-09-09 (WEV children; wrap promotion):

- [ ] Operator visual QA of Code plane — [`docs/tickets/2026-09-09-wev-code-plane-visual-qa.md`](../tickets/2026-09-09-wev-code-plane-visual-qa.md)
- [ ] Tighten `index_work` owner heuristic — [`docs/tickets/2026-09-09-wev-index-work-owner-heuristic.md`](../tickets/2026-09-09-wev-index-work-owner-heuristic.md)
- [ ] Re-run `index_work` when docs change — [`docs/tickets/2026-09-09-wev-index-work-refresh-hook.md`](../tickets/2026-09-09-wev-index-work-refresh-hook.md)
- [ ] Optional split work.json index vs bodies — [`docs/tickets/2026-09-09-wev-work-json-split-bodies.md`](../tickets/2026-09-09-wev-work-json-split-bodies.md)

---

## 15. Appendix

- Cache-bust: `wev-live.js?v=20260908c`, `wev-live.css?v=20260908c`
- Catalog counts: 13 ADR, 238 ticket, 14 issue, 20 plan; owners ecosystem 116, wv2 49, dm 38, wut 34, wq 32, bg 16
- DM node metadata (indexer `NODES`): EODHD + Quiver Quantitative Alt Filings; peers wut, wv2, ecosystem
- Do **not** Cromwell-emit `symbol_started` — `DmCromwellNotifier` posts every `event.message`
