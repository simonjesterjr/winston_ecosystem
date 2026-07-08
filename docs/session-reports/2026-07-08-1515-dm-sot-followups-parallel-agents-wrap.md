# Session Report — DM SoT Follow-ups (6 Workers + Manager) + Wrap

**Date:** 2026-07-08
**Time:** ~14:55–15:15 MDT
**Duration:** ~1h 20m
**Project:** sawtooth (ecosystem + data_manager + winston_unit_test)
**Working directory:** /home/johnkoisch/Documents/com/sawtooth
**Branch:** main (each monolith)
**Model:** Grok (xAI)
**Operator:** main + 6 ticket workers + manager subagent

---

## 1. Goal & Outcome

**Stated goal:** Run parallel agents for the six DM-as-SOT follow-up tickets plus a manager; update tickets; decide whether DM-as-source-of-truth migrations are done and portfolio creation can resume. Then `/wrap` all streams.

**Outcome:** Delivered

**One-line summary:** Six follow-up tickets closed (or planning-complete); live E2E + scheduled no-dup verified; HARD GO to resume portfolio-overlap work.

---

## 2. Work Completed

- Spawned 6 workers + 1 manager in parallel on the follow-up tickets.
- **E2E smoke:** full reconcile (632/0), fresh PBR 29 + single BR 4, ACT/MIV Δ=0, pages 200.
- **Zero-delta specs:** first DM RSpec suite (15 examples, 0 failures).
- **Bind-mount:** Option A enabled on root `compose.yml`; root cause was non-executable `data_manager/bin/*`.
- **Manual symbols:** CDE, IBM, JNJ, PG, ROKU, RXT, WMT, WTI reclassified `manual` → `catalog` (live DB).
- **Outside-UI audit:** inventory + guards; `DataDownloader` routes DM through thin importer.
- **Schema cleanup:** inventory + phased plan (B/C/D deferred).
- **Manager board:** final HARD GO for core SoT + portfolio resume.
- Follow-up code: nil-activity fixes in `BacktestRunner` + `PyramidGroupTracker`; BR4 re-ran to completed.
- Session report + multi-repo commit/push (this wrap).

---

## 3. Code Delivered

### Files changed

| File | Change | Notes |
|------|--------|-------|
| `winston_unit_test/app/services/data_downloader.rb` | modified | DM symbols → thin importer; no ACT/MIV write |
| `winston_unit_test/app/services/dataset_loader.rb` | modified | Skip DM activity materialization |
| `winston_unit_test/app/services/backtest_runner.rb` | modified | `signal.date` / `bar_date` nil-safe paths |
| `winston_unit_test/app/services/pyramid_group_tracker.rb` | modified | `position_entry_date` for DM |
| `winston_unit_test/lib/parquet_data/backtest_activities_loader.rb` | modified | DM no-op ensure_calculated |
| `winston_unit_test/lib/tasks/parquet.rake` | modified | LEGACY + abort_if_dm_symbol |
| `winston_unit_test/lib/tasks/paper_trading.rake` | modified | notes/guards |
| `winston_unit_test/lib/tasks/dataset_setup.rake` | modified | notes |
| `winston_unit_test/app/jobs/refresh_portfolio_data_job.rb` | modified | notes |
| `winston_unit_test/lib/scripts/*` | modified | legacy annotations / DM abort |
| `data_manager/spec/**` | added | ReconciliationService + rake zero-delta suite |
| `data_manager/.rspec` | added | |
| `data_manager/db/schema.rb` | added | schema dump for test/bootstrap |
| `data_manager/AGENTS.md`, `README.md` | modified | bind-mount policy |
| `data_manager/bin/{rails,rake,setup}` | mode 100755 | fix Podman bind-mount |
| Root `compose.yml` | modified | **not in a git repo** — local orchestrator; bind-mount enabled |
| Root `bin/rebuild-dm` | added | **not in a git repo** — helper script |
| `ecosystem/docs/tickets/2026-07-08-*.md` (6 tickets) | modified | status + evidence |
| `ecosystem/docs/session-reports/2026-07-08-dm-sot-followups-manager-board.md` | added | manager final board |
| `ecosystem/plans/wut-dm-parquet-source-of-truth.md` | modified | bind-mount / follow-up notes |
| `ecosystem/deployment/README.md`, `hints/README.md`, `ai/schedule/README.md` | modified | DM rebuild/bind-mount docs |
| Related main ticket + issue | modified | outside-UI follow-up notes |

### Commits

- (filled at wrap) data_manager, winston_unit_test, ecosystem — see §3 after commit

### Branch / PR state at sign-off

- Branch: `main` on ecosystem, data_manager, winston_unit_test
- Pushed: yes (wrap)
- PR: not opened (direct main, matching recent session practice)

---

## 4. Decisions Made

### Decision 1: HARD GO — core DM-as-SOT done; resume portfolio creation
- **Choice:** Close follow-ups as done/planning-complete; resume `portfolio-overlap-rebuild`
- **Why:** Live PBR+BR Δ=0, reconcile 632/0, scheduled no-dup YES, manager synthesis
- **Alternatives considered:** Wait for schema column drops / full historical purge
- **Reversibility:** Easy (re-open tickets)
- **Promote to ADR?** No — covered by ADR-002/003 + plan

### Decision 2: Bind-mount Option A for data_manager
- **Choice:** Full `./data_manager:/app` like WUT/Wv2; keep `bin/*` executable
- **Why:** Rebuild tax caused session container hell; root cause was host `bin/*` 0644 masking image +x
- **Alternatives considered:** B (docs-only rebuild), C (partial mounts)
- **Reversibility:** Easy (comment out mount)
- **Promote to ADR?** No — operational policy in README/AGENTS/hints

### Decision 3: Manual registry symbols → catalog
- **Choice:** Reclassify all 8 to `list_source: catalog` with metadata
- **Why:** All present in WUT `market_catalog.json`
- **Reversibility:** Easy
- **Promote to ADR?** No

### Decision 4: Schema activity_id — plan only
- **Choice:** Phase A already done; B/C/D deferred
- **Why:** Dual-path readers remain; non-blocking for SoT
- **Promote to ADR?** No

---

## 5. Insights Surfaced

- DM bind-mount “Podman permission hell” was largely **mode bits on `bin/*`**, not an inherent Podman ban on bind-mounts.
- Single-market `BacktestRunner` still had residual `activity.date` assumptions after the big PBR cutover; portfolio path was already clean.
- `upsert_symbol!` does not promote existing `manual` → `catalog` on re-import — residual mega-caps need a code fix or direct assign.
- DM previously had **no** RSpec tree; zero-delta suite is green but needs image rebuild or bind-mount to stay in sync (bind-mount now fixes that).

---

## 6. Issues & Tickets

### Resolved this session
- `2026-07-08-dm-reconcile-full-e2e-smoke.md` — Completed
- `2026-07-08-dm-reconcile-zero-delta-specs.md` — Completed
- `2026-07-08-dm-bind-mount-decision.md` — Completed
- `2026-07-08-review-manual-registry-symbols.md` — Completed
- `2026-07-08-audit-outside-ui-callers-rakes-jobs.md` — Completed
- `2026-07-08-schema-cleanup-activity-id-columns.md` — Completed (planning)
- Prior main SoT ticket remains Completed; outside-UI deferred item closed

### Deferred
- Schema activity_id phases B/C/D
- Historical ACT/MIV purge (plan: optional)
- `upsert_symbol!` list_source promotion for AAPL/AMZN/GOOGL/MSFT/TSLA etc.
- Suitability evaluation for reclassed 8 (`suitable: 0` until evaluate_pending)
- Pure-0-activity `find_overlapping_date_range` (still may use legacy ACT for SPY)
- Root `compose.yml` / `bin/rebuild-dm` not in a git repo (workspace glue)

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| DM reconcile all | `bin/rails data:reconcile` | ✅ 632/0 |
| PBR 29 DM smoke | PortfolioBacktestRunner | ✅ completed, Δ=0 |
| BR4 single DM smoke | BacktestRunner after fixes | ✅ completed, Δ=0 |
| PBR pages 25/29 | HTTP GET | ✅ 200 |
| DM zero-delta specs | rspec 15 examples | ✅ 0 failures |
| Outside-UI scheduled | audit + DataDownloader fix | ✅ no-dup claim |
| Bind-mount | rails -v + runner in DM | ✅ |

**Test command(s):**

```bash
bin/compose exec -T data_manager bin/rails data:reconcile
bin/compose exec -T data_manager bash -c 'cd /app && RAILS_ENV=test bundle exec rspec spec/services/reconciliation_service_spec.rb spec/tasks/data_rake_spec.rb'
bin/compose exec -T winston_unit_test bin/rails runner 'BacktestRunner.new(4).execute; PortfolioBacktestRunner...'
```

---

## 8. Environment, Dependencies, Data

- **Dependencies:** None new (rspec-rails already in DM Gemfile)
- **Services:** full stack via `bin/compose` (DM, WUT, Redis, Postgres, …)
- **Migrations:** None new this session (schema.rb dump only in DM)
- **DB ops:** SymbolRegistryEntry list_source updates for 8 symbols (live, not migration)

---

## 9. Risks & Technical Debt

- Root orchestrator (`compose.yml`, `bin/rebuild-dm`) not versioned in a git repo — drift risk if only ecosystem docs change.
- LEAP/options dual-path edges may still touch `activity` in rarer single-backtest paths.
- Suitable symbol pool still needs evaluation for Orange/White ≥50 builds.

---

## 10. Open Questions

- **Should root `compose.yml` live in a tracked repo?** — needs operator decision; blocks: multi-machine fidelity
- **When to run `dm:symbol_registry:evaluate_pending`?** — portfolio ops; blocks: suitable pool size

---

## 11. Handoff & Resume Notes

- **Where I left off:** Follow-ups closed; HARD GO for portfolio; wrap commits/push.
- **Next concrete step:** Resume `ecosystem/plans/portfolio-overlap-rebuild.md` (Orange/White, evaluation framework, Red vet).
- **Files to read first:**
  1. `ecosystem/docs/session-reports/2026-07-08-dm-sot-followups-manager-board.md`
  2. `ecosystem/plans/portfolio-overlap-rebuild.md`
  3. `ecosystem/plans/wut-dm-parquet-source-of-truth.md` (closeout section)

---

## 12. Stakeholder Communications

- _None required._ Optional: short note that market-data ownership (DM parquet) is stable enough to return to portfolio construction.

---

## 13. Tools & Workflow Notes

- **Skills used:** wrap, session-report
- **What worked well:** Parallel subagents per ticket + manager board; live smoke after code fixes.
- **Friction points:** Nested `spec/spec/...` trees from agent writes (cleaned before commit); root compose not git-tracked.
- **Subagent usage:** 6 general-purpose workers + 1 manager (resume for final synthesis); no worktree isolation (shared stack).

---

## 14. Follow-up Actions

- [ ] Resume portfolio-overlap product work — owner: team — due: next session
- [ ] Optional ACT/MIV snapshot preflight before multi-hour vet — owner: operator
- [ ] Suitability evaluation for catalog/pending symbols — owner: ops
- [ ] Consider versioning root compose / rebuild-dm — owner: team
- [ ] Schema activity_id Phase B when dual-path quiet — owner: later

---

## 15. Appendix (optional)

### Ticket statuses after session

| Ticket | Status |
|--------|--------|
| dm-reconcile-full-e2e-smoke | Completed |
| dm-reconcile-zero-delta-specs | Completed |
| dm-bind-mount-decision | Completed |
| review-manual-registry-symbols | Completed |
| audit-outside-ui-callers-rakes-jobs | Completed |
| schema-cleanup-activity-id-columns | Completed (planning) |

### Manager verdict

- Core DM-as-SOT: **HARD GO**
- Resume portfolio creation: **HARD GO**
