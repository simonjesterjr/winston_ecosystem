# Manager Board — DM-as-SOT Closeout Follow-ups

**Date:** 2026-07-08  
**Role:** Manager agent (track + synthesize; do not implement worker tickets)  
**Workspace:** `/home/johnkoisch/Documents/com/sawtooth`  
**Authoritative closeout:** `ecosystem/plans/wut-dm-parquet-source-of-truth.md` § Manager Final Phase Closeout  
**Main ticket:** `ecosystem/docs/tickets/2026-07-07-wut-dm-parquet-source-of-truth-no-duplication.md` (Completed)  
**Prior sessions:**
- `ecosystem/docs/session-reports/2026-07-08-1620-dm-source-of-truth-closeout-parallel-subagents.md`
- `ecosystem/docs/session-reports/2026-07-08-1430-dm-reconcile-container-cleanup.md`

**Next product plan:** `ecosystem/plans/portfolio-overlap-rebuild.md` (Red/Blue rebuilt; Orange/White + Red vet + strategy evaluation next)

**Board phase:** FINAL SYNTHESIS (all 6 workers reported)

---

## 0. Executive answer

**Yes — core DM-as-source-of-truth migrations are done, and we should move back to portfolio creation.** Reconcile is clean (632/0), a fresh DM-only PortfolioBacktestRun (29) and single BacktestRun (4) completed with ACT/MIV Δ=0, result identity + loader re-pull and PBR pages work, scheduled/outside-UI paths were audited and guarded (including DataDownloader routing DM through the thin importer), zero-delta specs and bind-mount DX landed, and schema cleanup remains explicitly deferred. Follow-up fixes closed the single-market `BacktestRunner` nil-activity crash (`signal.date` / `position.bar_date` / pyramid tracker). Portfolio-overlap (Orange/White build, evaluation framework, Red vet via PBR) is **HARD GO**.

---

## 1. FINAL status board

| Ticket | Status | Outcome this session | Blocking SoT claim? | Blocking portfolio? | Residual |
|--------|--------|----------------------|---------------------|---------------------|----------|
| [dm-reconcile-full-e2e-smoke](../tickets/2026-07-08-dm-reconcile-full-e2e-smoke.md) | **Completed** | Reconcile 632/0; PBR 29 + BR4 completed; ACT/MIV Δ=0; pages 200; nil-activity fixes landed | No | No | Pure-0-activity date-range discovery still legacy-backed |
| [dm-reconcile-zero-delta-specs](../tickets/2026-07-08-dm-reconcile-zero-delta-specs.md) | **Completed** | First DM RSpec suite: 15 examples, 0 failures; ReconciliationService + rake specs with fixtures | No | No | None material |
| [dm-bind-mount-decision](../tickets/2026-07-08-dm-bind-mount-decision.md) | **Completed** | **Option A:** full bind-mount; root cause `bin/*` not executable (0644); compose.yml + `bin/rebuild-dm` + docs; rails verified in container | No | No | Keep bin/* executable in repo hygiene |
| [review-manual-registry-symbols](../tickets/2026-07-08-review-manual-registry-symbols.md) | **Completed** | All 8 reclassified `manual` → `catalog` + metadata; all 8 in `awaiting_evaluation`; suitable=0 (pending evaluation) | No | No | `upsert_symbol!` won't promote remaining manual mega-caps (AAPL/AMZN/GOOGL/MSFT/TSLA) without code fix |
| [audit-outside-ui-callers-rakes-jobs](../tickets/2026-07-08-audit-outside-ui-callers-rakes-jobs.md) | **Completed** | Jobs/rakes inventoried; **key fix:** `DataDownloader.download_and_save` routes DM via thin importer; guards on parquet rakes, DatasetLoader, fill_nvda_gap abort. **"No duplication paths remain" for scheduled jobs: YES** | No (claim satisfied for scheduled) | No | Manual legacy rakes labeled only; FRED intentional; historical activities not purged |
| [schema-cleanup-activity-id-columns](../tickets/2026-07-08-schema-cleanup-activity-id-columns.md) | **Completed planning** | Phase A historical; B/C/D deferred; no migrations this session | No | No | Phased migration when ready to drop legacy |

### Classification after workers

| Bucket | Items |
|--------|-------|
| **Core SoT — DONE** | Loaders, identity, re-pull, pure registry, thin importer, MIV skip, model DM branches, reconcile 632, PBR zero-delta live, scheduled-path no-dup audited |
| **Confidence — largely DONE** | E2E PBR path green; residual single-market BacktestRunner only |
| **Hardening — DONE this pass** | Zero-delta specs (15/0), bind-mount Option A, manual-8 reclass, outside-UI guards |
| **Deferred / residual backlog** | Single BacktestRunner nil-activity; upsert_symbol! promotion; mega-cap list_source; schema B/C/D; historical ACT/MIV purge; suitability evaluation for reclassed 8 |

---

## 2. Definition of Done — gate check (final)

### Must (gate to resume portfolio) — all met for PBR/portfolio path

| # | Criterion | Final |
|---|-----------|-------|
| 1 | DM owns time-series; consumers read | ✅ |
| 2 | WUT DM loader + composite identity + re-pull | ✅ |
| 3 | No new duplication on primary paths | ✅ (live Δ=0 + scheduled audit YES) |
| 4 | Registry + coverage / reconcile usable | ✅ (632 reconciled, 0 errors) |
| 5 | PBR view crash fixed | ✅ (HTTP 200 on 25 and 29) |
| 6 | Documented confidence smoke (reconcile → DM PBR → views, deltas) | ✅ for **portfolio** path; ⚠️ single-market BacktestRunner fails |

### Nice-to-have — outcomes

| Item | Final |
|------|-------|
| Zero-delta RSpec for reconcile | ✅ 15 examples, 0 failures |
| Outside-UI no unguarded scheduled materializers | ✅ YES for scheduled jobs |
| Bind-mount decision | ✅ Option A enabled |
| Manual symbols reclassified | ✅ 8/8 → catalog |
| Schema activity_id cleanup | ⚪ Deferred (non-blocking) |

---

## 3. FINAL Go / No-Go

### 3a. Claiming core DM-as-SOT migrations done

| Verdict | **HARD GO** |
|---------|-------------|
| Meaning | Core architecture cutover + main ticket ACs + plan closeout remain closed and are now **re-verified** with live reconcile+PBR smoke, scheduled-path audit, and CI-oriented zero-delta suite. |
| Caveat | Do **not** claim “every entrypoint including single-market BacktestRunner is flawless.” Claim: **DM is SoT; portfolio/PBR and scheduled paths do not duplicate; single-backtest has one known nil-activity bug.** |

### 3b. Returning to portfolio creation / portfolio-overlap work

| Verdict | **HARD GO** |
|---------|-------------|
| Meaning | Orange/White build, correlation/sidecars, evaluation framework, Red vet, Blue revisit — **resume now** on the PBR / portfolio runners. |
| Do not block on | Schema cleanup, single BacktestRunner fix, mega-cap list_source promotion, historical purge |
| Preflight still wise | Before multi-hour `portfolios:vet_trend`, optional ACT/MIV snapshot before/after short PBR (cheap regression check) |

| Criterion | Final status | Notes |
|-----------|--------------|-------|
| Plan + main ticket closed | ✅ HARD GO | Unchanged |
| Principles 02 alignment (new DM data) | ✅ HARD GO | |
| Live zero-delta importer/loader/PBR | ✅ HARD GO | PBR 29 + global/SPY Δ=0 |
| Pure registry + thin importer | ✅ HARD GO | |
| ReconciliationService operational | ✅ HARD GO | 632/0 |
| PBR views | ✅ HARD GO | 25 + 29 HTTP 200 |
| Documented E2E reconcile→PBR | ✅ HARD GO (portfolio path) | Partial ticket only for single BacktestRunner |
| Outside-UI scheduled clean | ✅ HARD GO | Explicit YES from Worker 5 |
| Zero-delta specs | ✅ Done | Informational |
| Bind-mount DX | ✅ Done | Option A |
| Manual 8 symbols | ✅ Done | Suitable still 0 until evaluation |
| Schema activity_id | ⚪ Deferred | Non-block |
| Single-market BacktestRunner | ⚠️ Residual bug | **Not** portfolio path |

### Upgrade from preliminary

| Phase | Portfolio resume | Core SoT claim |
|-------|------------------|----------------|
| Preliminary (pre-workers) | CONDITIONAL GO | YES (core) / not fully hardened |
| **Final (post-workers)** | **HARD GO** | **HARD GO** (with single-runner caveat) |

Soft blocks cleared:
1. E2E smoke — **cleared for PBR/portfolio** (partial only on solo BacktestRunner).
2. Outside-UI audit — **cleared** (scheduled no-dup YES; DataDownloader fix).

---

## 4. What remains open without blocking portfolio

| Item | Status | Why non-blocking |
|------|--------|------------------|
| Single-market BacktestRunner nil `activity` | **Fixed this session** (BR4 completed) | Residual: pure-0-activity overlapping date range |
| Schema activity_id phases B/C/D | Deferred | Optional FKs already; no growth on DM paths |
| Historical ACT/MIV purge | Deferred | No growth; plan: no curation required |
| Mega-caps still `manual` + upsert promotion | Residual ops | Loader/coverage unaffected; registry hygiene |
| Suitability eval for reclassed 8 | Portfolio *ops* | Needed for pool quality (≥50 suitable), not SoT architecture |
| FRED / labeled legacy rakes | Intentional | Isolated |

---

## 5. Residual risk (updated post-workers)

| Risk | Likelihood | Impact | Mitigation / disposition |
|------|------------|--------|---------------------------|
| Single BacktestRunner residual dual-path edges | Low | LEAP/options/expected-return with nil activity_id | BR4 completed; watch under LEAP-heavy runs |
| Multi-symbol portfolio edge (non-SPY) not fully smoke-tested | Low–med | Rare view/indicator hole | First Orange/White build will exercise; re-pull already works on SPY PBR |
| Suitable pool still small for Orange/White | Med (ops) | Build may hit pool caps | Run suitability evaluation + acquire as portfolio plan already requires |
| Manual mega-caps stuck if re-upserted | Low | list_source hygiene | Fix `upsert_symbol!` promotion rules later |
| Historical activity rows still present | Low | Confusion in counts if someone queries raw ACT | Document; pre/post Δ on vet optional |

Risks **closed** this session:
- Scheduled re-duplication via DataDownloader / rakes → **closed** by audit + guards.
- Rebuild tax / bind-mount → **closed** (Option A).
- Reconcile + list_source crash class → **closed** (632/0).
- Undocumented PBR E2E → **closed** (Portfolio 32 / PBR 29 evidence).

---

## 6. Residual backlog (priority order)

1. **P1 — Suitability evaluation + pool expansion** for catalog symbols (incl. reclassed 8 still `suitable: 0`) so Orange/White can hit ≥50 suitable — portfolio plan ops.
2. **P2 — DM date-range discovery** for pure-0-activity markets (`find_overlapping_date_range` still uses activities for SPY legacy rows).
3. **P3 — `upsert_symbol!` list_source promotion** so remaining manual mega-caps (AAPL/AMZN/GOOGL/MSFT/TSLA) and future re-upserts can move to `catalog` when appropriate.
4. **P4 — Schema activity_id phases B/C/D** when ready for a cleanup release.
5. **P5 — Optional historical ACT/MIV purge** for DM symbols (explicitly non-required by plan).
6. **P6 — Repo hygiene:** keep `data_manager/bin/*` executable so bind-mount stays healthy.

---

## 7. Worker evidence rollup (checklist closed)

### E2E smoke (Worker 1) — required for HARD GO portfolio

- [x] Reconcile succeeded (632 reconciled, 0 errors)
- [x] Fresh DM PBR run (Portfolio 32, PBR 29, SPY 2025-H1)
- [x] ACT/MIV before/after Δ=0 (global + SPY)
- [x] `bar_date` + `market_id` on positions
- [x] Views / pages HTTP 200 (29 and 25); loader re-pull works
- [x] Gap severity documented: **single BacktestRunner only — does not block portfolio**

### Outside-UI audit (Worker 5) — required for HARD GO on no-dup

- [x] Inventory of jobs/rakes
- [x] Key unguarded path fixed (`DataDownloader` → thin importer for DM)
- [x] Explicit: scheduled jobs **cannot** grow ACT/MIV for DM symbols → **YES**

### Informational workers

- [x] Zero-delta specs: 15/0 green
- [x] Bind-mount: Option A + verified
- [x] Manual 8 → catalog; residual mega-caps + upsert noted
- [x] Schema: planning complete; no migrations; non-blocking

### Final synthesis checklist

- [x] Soft-block tickets cleared for portfolio path → **HARD GO**
- [x] E2E not hard-fail on PBR → no NO-GO on portfolio
- [x] Audit: no remaining unguarded scheduled materializer
- [x] Board §3 final verdict + timestamp (this section, 2026-07-08 final pass)

---

## 8. Snapshot status (FINAL)

| Question | Final answer |
|----------|--------------|
| Core DM-as-SOT migrations done? | **HARD GO — YES** |
| Hardened enough (scheduled no-dup + PBR smoke)? | **YES** |
| Single-market BacktestRunner fully clean? | **YES for core trend path** (BR4 completed; LEAP edges residual) |
| Resume portfolio creation / portfolio-overlap? | **HARD GO — YES** |
| Long multi-hour portfolio vet via PBR? | **HARD GO** (optional Δ preflight recommended) |
| Solo DM BacktestRunner / single-backtest UI? | **GO** for trend-following SPY path verified |

### Dependency map (final)

```
portfolio-overlap-rebuild
├── DM data + reconcile + registry ........ HARD GO (632/0)
├── WUT PBR / portfolio vet on DM ......... HARD GO (PBR 29 Δ=0)
├── Outside-UI / scheduled no-dup ......... HARD GO (audit YES)
├── Single-market BacktestRunner .......... GO (BR4 completed this session)
├── evaluation framework (P0) ............. portfolio domain next
├── Orange/White build .................... HARD GO (ops: suitable pool)
└── Red vet / Blue revisit ................ portfolio plan gates (framework), not SoT
```

---

## 9. Preliminary section (historical — superseded)

Preliminary verdict was **CONDITIONAL GO** pending E2E + outside-UI workers. Both soft blocks cleared for the portfolio path. See git history / earlier revision of this file conceptually as superseded by §0–§8 FINAL.

---

**Board path:** `ecosystem/docs/session-reports/2026-07-08-dm-sot-followups-manager-board.md`  
**Manager actions:** synthesize only — no ticket implementation, no commit from this pass.  
**Next operator action:** start portfolio-overlap product work (`ecosystem/plans/portfolio-overlap-rebuild.md`). Optional preflight: snapshot ACT/MIV before long vet.
