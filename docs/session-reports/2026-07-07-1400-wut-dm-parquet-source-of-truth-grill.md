# Session Report — WUT DM Parquet Source of Truth + Grill

**Date:** 2026-07-07
**Time:** ~ (multiple turns, continued session)
**Duration:** Multi-hour (planning + adversary + extensive grill)
**Project:** sawtooth (Winston ecosystem cross-monolith)
**Working directory:** /home/johnkoisch/Documents/com/sawtooth
**Branch:** (ecosystem planning + WUT target; not in git shell for this wrap)
**Model:** Grok (xAI)
**Operator:** (per context)

---

## 1. Goal & Outcome

**Stated goal:** Observe "Load Full Data from DM" vs "Sync" buttons on WUT /data_sets. Produce a verified plan to make DM the sole source of truth for time-series (no duplication into WUT activities or local parquets). Use /adversary to challenge. Create tracking tickets. Run /grill-with-docs against ecosystem docs, principles, CONTEXT, ADRs, code. Incorporate all user confirmations (composites over FKs, no long-lived shim, remove belongs_to :activity for DM data, legacy non-DM defunct, just re-pull from DM for views/results, DM owns indicators, no transitional paths).

**Outcome:** Delivered

**One-line summary:** Authoritative plan + updated tickets now reflect full direct refactor: DM loader + composite (market_id, date) + Bar everywhere for DM data; result parquets minimal with identity keys; runners and all creation/usage sites use loader directly; no shims/stubs/transitions.

---

## 2. Work Completed

- Relocated plan from session dir to `ecosystem/plans/wut-dm-parquet-source-of-truth.md` (per AGENTS correction).
- Ran /adversary on initial plan → "BROKEN" verdict on shim/FK assumptions; incorporated corrections (loaders first, full site audit, no naive proxy).
- Created/updated three tickets in `ecosystem/docs/tickets/2026-07-07-*` tracking the work.
- Extensive /grill-with-docs: inline CONTEXT.md updates for canonical terms (DataCoverage, activities deprecation, composites, "just use DM").
- Multiple user confirmations captured:
  - Data Sets page = pure DM registry (no load/sync hydration).
  - Remove or fully deprecate belongs_to :activity for DM-sourced (and legacy non-DM defunct, no curation).
  - Refactor creation + usage sites to composite key + Bar from DM loader.
  - Backtest results: use stored (market, date) + re-pull; minimal result parquet + identity required.
  - DM owns OHLCV + all indicators (ATR-17 today; new ones like MACD become DM job).
  - Runners: direct DM Bar loader in day-by-day loop; no Activity rows/local parquets for DM symbols.
  - No transitional/temporary/shim paths — "fix this and move on".
- Final capture: updated plan and all three tickets to match (removed all shim/stub/compatibility language; revised ACs, phasing, verification, open items).
- One-time clean of duplicated text in CONTEXT.md ambiguities section (trailing repeats from prior edits).
- Cross-checked against code (schema activity_id NOT NULLs, BacktestWriter/Reader, loaders, views doing Activity.where, DataSetDmImporter, etc.).
- Followed AGENTS: read ecosystem/CONTEXT, principles, interfaces, WUT AGENTS.md first; used ecosystem for cross-monolith artifacts.

---

## 3. Code Delivered

### Files changed (this session — docs and planning only; no runtime code yet)

| File | Change | Notes |
|------|--------|-------|
| `ecosystem/plans/wut-dm-parquet-source-of-truth.md` | heavily revised | Core decisions, phasing, verification, open items, goal updated for no-shim direct refactor, result identity, DM indicator ownership, composites + Bar. |
| `ecosystem/docs/tickets/2026-07-07-wut-dm-parquet-source-of-truth-no-duplication.md` | revised | Goal, ACs, title, description rewritten; removed shim language; added result identity, runner direct loader, DM indicators, DataCoverage. |
| `ecosystem/docs/tickets/2026-07-07-wut-dm-data-sets-ui-dm-truth-no-load-sync-buttons.md` | revised | Title, goal, ACs aligned to pure DM registry; no hydration. |
| `ecosystem/docs/tickets/2026-07-07-wut-activities-compatibility-shim-dm-stubs.md` | rewritten | Title, context, goal, ACs changed from "shim + stubs" to "refactor remove activity, composite + loader, result identity". |
| `ecosystem/CONTEXT.md` | modified + cleaned | Flagged ambiguities section strengthened with latest decisions (belongs_to removal, legacy defunct, re-pull, Data Sets registry, no long-lived shim); trailing duplication excised. |
| `ecosystem/docs/session-reports/2026-07-07-1400-wut-dm-parquet-source-of-truth-grill.md` | added | This wrap report (cross-monolith location). |

### Commits
- (Not executed in this tool env — "we are not in a git repo" per user. See exact staging instructions in wrap response.)

### Branch / PR state at sign-off
- No git operations performed in shell (env limitation noted by user).
- All changes are in ecosystem/ (cross-monolith planning for WUT).
- Plan and tickets are the deliverables; ready for implementation in winston_unit_test after user review.

---

## 4. Decisions Made

### Decision 1: DM sole source — direct composite + Bar, no activity for DM data
- **Choice:** Refactor creation/usage (runners, positions, signals, BIVs, result views, charts, calcs) to `(market_id, date)` + DM loader Bar. Remove/deprecate belongs_to :activity. Result rows must carry stable identity.
- **Why:** Matches principles/02, Wv2 pattern (ParquetBar id=nil), CONTEXT resolutions, and repeated user statements ("remove or fully deprecate", "refactor ... to composite key + Bar", "just use DM to pull", "no more transitional").
- **Alternatives considered:** Thin shim on activities (ruled out by adversary + user); preserving association for "legacy" (ruled out — legacy defunct).
- **Reversibility:** Costly once schema + many call sites changed (but correct direction).
- **Promote to ADR?** No (implements existing principles + ADRs 002/003); captured in plan + CONTEXT.

### Decision 2: Result parquets minimal + identity; re-pull for rich data + holes via DM
- **Choice:** Keep result parquet thin (P&L + captured snapshots + `(market_id, date)` key). Charts/views re-pull Bar from DM loader. DM callback for missing data/derived values.
- **Why:** User: "treat the data already stored ... as sufficient" + "every result row MUST be identifiable" + "if you don't have the quantity ... call back to DM".
- **Reversibility:** Medium (requires BACKTEST schema change + writer/reader update).

### Decision 3: DM owns all indicators going forward
- **Choice:** New indicators (e.g. MACD) added to DM responsibility + Winston EOD Standard.
- **Why:** "DM's job is pulling the data and then calculating the derivative stuff."
- **Reversibility:** Easy at interface level.

### Decision 4: No transitional / temporary paths
- **Choice:** Full cutover for DM symbols in runners and ingestion. Legacy non-DM isolated.
- **Why:** Explicit user rejection of "transitional temporary stuff".

---

## 5. Insights Surfaced

- The activities table + FKs were the "carrier" that made the old duplication invisible; removing them forces proper loader adoption everywhere (runners, views, calcs).
- Backtest result parquets already separate storage from source data — perfect for the "re-pull at render" model.
- Adding a new indicator is now explicitly a DM + interface change, not scattered consumer work (strong alignment with ADR-003).
- Grill process surfaced that "shim" framing in early plan/tickets was a holdover; user corrections made the scope "refactor the sites" rather than "preserve expressions".
- DataCoverage vs DmCoverage naming convergence is still needed in actual WUT code (plan notes it).

---

## 6. Issues & Tickets

### Resolved this session
- Incorrect plan location (moved to ecosystem/plans/).
- Outdated "shim + stubs" language in plan and the dedicated ticket (fully revised).
- Duplicated text in CONTEXT.md ambiguities (cleaned).
- Lack of explicit result row identity requirement (now in plan + tickets).

### Deferred
- Actual implementation in winston_unit_test (runners, loaders, result writer/reader, model changes, UI, schema for activity_id).
- Concrete choice of identity representation in BACKTEST schema (add market_id column? concat string? hash?) — noted as open in plan.
- Full audit of every Activity reference (grep showed ~100+ sites across views, services, jobs, lib/).
- DataCoverage model rename in WUT code (currently DmCoverage).
- Migration strategy for existing activity_id NOT NULL columns and historical data.
- winston_unit_test/docs/session-report for the monolith-specific follow-on work (when implementation starts).

Tickets created/updated this session are the three 2026-07-07 files (now accurate).

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| Plan + tickets alignment with user grill answers | Manual review of all user "Yes"/clarifications vs. final text | ✅ |
| No lingering "shim/stub/compatibility" language in deliverables | grep across plan + 3 tickets | ✅ (only in "no shim" context) |
| Captures "just re-pull", composite keys, DM indicator ownership, no transitional | Cross-check against last 3 user messages | ✅ |
| Adversary findings addressed | Plan section updated | ✅ |
| CONTEXT canonical terms | DataCoverage, activities deprecation, legacy defunct | ✅ (plus tail clean) |

**Test command(s):** N/A (planning/docs only). When implementing: `bin/rails dm:sync_dm_registry`, backtest runs, result view smoke, counts of new activity rows = 0 for DM symbols.

---

## 8. Environment, Dependencies, Data

- **Dependencies:** None changed (planning only).
- **Services:** None started in this phase (prior context had bin/compose).
- **Migrations:** None (future work when activity_id columns addressed).
- **Data:** Relied on existing DM mount + Wv2 ParquetBar/ loader patterns as reference.

---

## 9. Risks & Technical Debt

- Large number of Activity-dependent sites in WUT (views, expected_return/*, position_manager, backtest result charts, etc.) — risk of incomplete refactor if not systematically audited.
- Result parquet schema change required (currently no per-row market_id).
- Historical backtest runs may reference old activity_ids; result re-pull model helps but needs handling.
- FRED/special series may need exception paths (noted in plan).

---

## 10. Open Questions

- Exact identity key format for result rows (plan leaves as decision).
- Order of refactoring: loaders + result identity first, then runners, then all usage sites?
- How hole-filling "call back to DM" is triggered from result views (on-demand request vs. ensure coverage).
- When to make activity_id nullable or drop in schema (after all DM paths migrated).

---

## 11. Handoff & Resume Notes

- **Where I left off:** Plan and the three tickets fully updated to the final user-confirmed direction (direct DM loader in runners, composite keys, result identity + re-pull, no shims, DM owns indicators). Grill complete for this branch.
- **Next concrete step:** User review of updated `ecosystem/plans/wut-dm-parquet-source-of-truth.md` and tickets. Then implementation start in winston_unit_test (begin with DM Bar loader port + BACKTEST schema update for identity).
- **Files to read first:**
  1. `ecosystem/plans/wut-dm-parquet-source-of-truth.md` (current state)
  2. `ecosystem/CONTEXT.md` (ambiguities section)
  3. The three tickets in `ecosystem/docs/tickets/2026-07-07-*`
  4. WUT: `lib/parquet_data/writers/backtest_writer.rb`, `lib/parquet_data/readers/backtest_results_reader.rb`, `lib/parquet_data/schemas.rb`, `app/services/data_set_dm_importer.rb`, `lib/parquet_data/backtest_activities_loader.rb`
  5. Wv2 reference: `winston_v2/app/services/parquet_lookback_loader.rb` + `parquet_bar.rb`

---

## 12. Stakeholder Communications

- None needed beyond the plan/tickets themselves (internal ecosystem planning artifact). When implementation begins, surface in WUT standup or Cromwell.

---

## 13. Tools & Workflow Notes

**Skills used:** grill-with-docs (extensively, one-question-at-a-time + inline CONTEXT), adversary, record (implicit via tickets), wrap (this).

**What worked well:**
- Iterative user confirmations ("Yes", clarifications) directly shaped the final language.
- Adversary + grill forced scope realism (no underestimating the 100+ usage sites).
- Keeping artifacts in ecosystem/ for cross-monolith visibility.

**Friction points:**
- Early CONTEXT edits went into a duplication loop (user stopped it; one-time clean done here).
- Git not available in this tool environment (user guidance followed: use ecosystem for logs/plans).

**Subagent usage:** Adversary subagent run earlier (incorporated).

---

## 14. Follow-up Actions

- [ ] User: review + approve revised plan + tickets.
- [ ] (When starting impl) Create winston_unit_test/docs/session-reports/ entry for the code changes.
- [ ] Decide on result row identity representation (market_id column vs. concat vs. hash).
- [ ] Systematic grep + refactor of all Activity creation/usage for DM paths (no cherry-picking).
- [ ] Port/adapt Wv2 DM loader patterns into WUT as primary.
- [ ] Update BACKTEST schema + writer/reader for `(market_id, date)` identity.
- [ ] Add ACs/tests that DM flows create zero new activity rows.
- [ ] Handle DataCoverage naming convergence in code.

---

## 15. Appendix (optional)

Relevant prior artifacts:
- Original issue from user observation of data_sets buttons.
- Adversary verdict: BROKEN on thin shim details.
- Repeated user language: "Remove or fully deprecate the belongs_to :activity", "Refactor creation and usage sites", "all legacy non-DM records are defunct", "just use DM to pull the data again. It's that simple", "Yes, do this. No no no ... no more transitional temporary stuff."

All grill resolutions from the long conversation summary (DataCoverage canonical, no long-lived shim, composites, pure DM registry, etc.) are now in the plan and tickets.
