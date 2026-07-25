# Session Report — PBR Fill Queue, Pyramid Stops, Cash/Return Literacy

**Date:** 2026-07-25  
**Time:** ~session (through 13:10 MDT wrap)  
**Duration:** multi-hour (continued from prior compaction)  
**Project:** sawtooth workspace (winston_unit_test + ecosystem)  
**Working directory:** `/home/johnkoisch/Documents/com/sawtooth`  
**Branch:** `winston_unit_test/main`, `ecosystem/main` (started from `origin/main`)  
**Model:** Grok 4.5  
**Operator:** johnkoisch  

---

## 1. Goal & Outcome

**Stated goal:** Investigate PBR trust failures (path selection vs geometry), fill cadence (same-bar vs next-open / T+1 queue), OWDC ladders & pyramid ATR reference, scale-in stops, heat design, PBR UI bugs, and how to read free-cash ledger / total return.

**Outcome:** Delivered (code + ADRs + ticket + operator literacy); heat implementation deferred to backlog ticket.

**One-line summary:** Lab T+1 fill queue and pyramid last-entry ATR / scale-in stop behavior landed in WUT with ADRs; portfolio heat ticketed; cash ledger MV and equity-vs-free-cash return framing clarified for TS evaluation.

---

## 2. Work Completed

- Designed and implemented **lab T+1 fill queue** (signal T → adjudicate open T+1; rank/reserve/expire discipline).
- ADRs accepted for T+1 queue and pyramid **scale-in price blocks** (last-entry ATR reference).
- Pyramid / position_manager: last-entry pyramid ATR; scale-in-only stop updates; fill-relative stop specs.
- Optional pyramid `confirming_signal` path and lab fill signal eval surfaces (controller/model/views/migration).
- OWDC / TS capture: ladder persistence and display; TS OWDC omit-ladder behavior addressed in session arc.
- PBR UI: new/show conf/status issues investigated; clear wiping risk ladder documented as issue.
- Ticketed multi-level **TS portfolio heat** (Turtle unit limits + correlations).
- Operator education: free-cash ledger **MV = market value**; equity = free cash + long MV − short MV; free-cash % is not total return (shorts inflate cash).

---

## 3. Code Delivered

### Files changed

#### winston_unit_test (uncommitted at wrap start)

| File | Change | Notes |
|------|--------|-------|
| `app/services/lab_fill_ticket_queue.rb` | added | T+1 ticket queue |
| `app/services/lab_fill_cadence.rb` | modified | cadence integration |
| `app/services/lab_fill_signal_eval_builder.rb` | added | confirming-signal eval build |
| `app/models/lab_fill_signal_eval.rb` | added | persistence model |
| `app/controllers/lab_fill_signal_evals_controller.rb` | added | UI/API surface |
| `app/views/lab_fill_signal_evals/` | added | views |
| `db/migrate/20260725120000_create_lab_fill_signal_evals.rb` | added | schema |
| `db/schema.rb` | modified | migration applied in tree |
| `app/services/portfolio_backtest_runner.rb` | modified | queue + end_of_run cash snapshot path |
| `app/services/position_manager.rb` | modified | scale-in stops / fill-relative |
| `app/services/pyramid_service.rb` | modified | last-entry ATR reference |
| `app/services/one_way_dynamic_risk_validator.rb` | modified | OWDC ladder |
| `app/services/portfolio_backtest/entry_requirement_calculator.rb` | modified | entry requirements |
| `app/models/portfolio_backtest_market_config.rb` | modified | config fields |
| `app/models/trading_strategy.rb` | modified | TS capture |
| `app/controllers/portfolio_backtest_runs_controller.rb` | modified | PBR flows |
| `app/controllers/trading_strategies_controller.rb` | modified | TS UI |
| `app/views/portfolio_backtest_runs/{new,show}.html.erb` | modified | conf/status/ladder |
| `app/views/trading_strategies/show.html.erb` | modified | ladder display |
| `config/routes.rb` | modified | lab fill signal eval routes |
| `spec/services/lab_fill_*.rb` | added/modified | queue + cadence |
| `spec/services/portfolio_backtest_*.rb` | added/modified | next-open + pyramid ref |
| `spec/services/position_manager_*.rb` | added | fill-relative + scale-in stops |
| `docs/issues/2026-07-24-pbr-clear-wipes-risk-ladder.md` | added | clear ladder bug |

#### ecosystem (uncommitted at wrap start)

| File | Change | Notes |
|------|--------|-------|
| `docs/adr/2026-07-25-lab-t1-fill-queue.md` | added | Accepted ADR |
| `docs/adr/2026-07-25-pyramid-scale-in-price-blocks.md` | added | Accepted ADR |
| `docs/tickets/2026-07-25-ts-portfolio-heat-unit-limits.md` | added | Proposed heat BA |
| `docs/session-reports/2026-07-25-1310-pbr-fill-queue-pyramid-cash.md` | added | this report |

**Note:** Other dirty ecosystem tickets (`2026-07-15-cromwell-*`, `2026-07-23-*`, INDEX) and `winston_v2` DAR/equity dirty files were **not** attributed to this session’s edits at wrap time — leave unstaged unless operator confirms ownership.

### Commits

- _Pending wrap commit(s)._

### Branch / PR state at sign-off

- Branch: `main` on WUT + ecosystem — dirty before wrap commit  
- Pushed: pending wrap  
- PR: not opened (main-line commits per local practice)

---

## 4. Decisions Made

### Decision 1: Lab T+1 fill queue
- **Choice:** Signal day T creates one ticket; adjudicate at open T+1; rank by ATR@T; reserve slots/cash; never upsize past planned units; expire unfilled.
- **Why:** Naive next-open without cohort discipline changed *which* tickets filled (path selection), not just stop geometry.
- **Alternatives considered:** Same-bar open; multi-day roll for holidays.
- **Reversibility:** Easy to toggle cadence; queue behavior is product-locked via ADR.
- **Promote to ADR?** Done — `ecosystem/docs/adr/2026-07-25-lab-t1-fill-queue.md`

### Decision 2: Pyramid ATR from last entry
- **Choice:** Scale-in price blocks and stop steps use **last-entry** ATR/price, not first lot only.
- **Why:** Pyramid geometry must track the latest risk unit; first-entry reference under-moves later adds.
- **Alternatives considered:** First-entry only (prior bug).
- **Reversibility:** Easy with config/tests.
- **Promote to ADR?** Done — `ecosystem/docs/adr/2026-07-25-pyramid-scale-in-price-blocks.md`

### Decision 3: Equity is total return; free cash is not
- **Choice:** Canonical wealth = `free_cash + long_mv − short_mv`; total return = (final equity − initial) / initial. Free cash % and gross MV are supporting metrics (liquidity / footprint).
- **Why:** Shorts credit free cash; free-cash +47% can coexist with ~+26% equity return and ~4× gross controlled.
- **Alternatives considered:** Reporting free-cash growth as “return” (rejected as misleading).
- **Reversibility:** Easy (docs/UI scorecard only).
- **Promote to ADR?** No — operator literacy; optional recon-strip UI later.

### Decision 4: Portfolio heat is backlog, not this session’s impl
- **Choice:** File multi-level Turtle-style heat (units + correlation clusters) as ticket; do not implement now.
- **Why:** Needs BA against PCS/correlation; flat max lots is temporary stand-in.
- **Alternatives considered:** Immediate integer heat on TS only.
- **Reversibility:** Easy.
- **Promote to ADR?** After BA — ticket `2026-07-25-ts-portfolio-heat-unit-limits.md`

---

## 5. Insights Surfaced

- Path selection (who gets capital/slots under delayed fills) often dominates geometry when comparing same_bar vs next_bar runs.
- Free cash alone is a poor TS success metric under two-way books: equity identity is required.
- Gross MV (~long+short) answers “how much market we control”; net MV answers directional bias; neither replaces equity return.
- Timeline P&L using exit MTM=0 and daily ATR trail under move_to_last_entry were prior failure modes in the same investigation arc.
- Confirming_signal and ladder capture on TS are product-sensitive; clear must not wipe ladder (issue filed).

---

## 6. Issues & Tickets

### Resolved this session
- T+1 queue product rules locked + implemented (pending commit/push).
- Pyramid last-entry / scale-in stop reference corrected with specs.
- Cash ledger MV / equity identity explained for operators.

### Deferred
- Multi-level TS portfolio heat — **ticketed:** `docs/tickets/2026-07-25-ts-portfolio-heat-unit-limits.md`
- OWDC/OWD 4-cell matrix — **ticketed:** `docs/tickets/2026-07-25-owdc-owd-four-cell-matrix.md`
- PBR status-poll missing-run UX — **ticketed:** `docs/tickets/2026-07-25-pbr-status-poll-missing-run-ux.md`
- Cash-ledger return scorecard — **ticketed:** `docs/tickets/2026-07-25-pbr-cash-ledger-return-scorecard.md`
- Confirm leftover dirty `winston_v2` DAR/equity files (wrap hygiene; not ticketed).

### Already filed (session-related)
- `winston_unit_test/docs/issues/2026-07-24-pbr-clear-wipes-risk-ladder.md`
- ADRs 2026-07-25 T+1 + pyramid scale-in
- Heat + 3 follow-up tickets (2026-07-25)

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| Lab fill ticket queue | unit specs (`lab_fill_ticket_queue_spec`) | ⚠️ present; re-run at ship |
| Lab fill cadence | `lab_fill_cadence_spec` | ⚠️ present |
| Next-open / pyramid ref | portfolio_backtest specs | ⚠️ present |
| Scale-in / fill-relative stops | position_manager specs | ⚠️ present |
| Live PBR smoke (147/148, 163/164, TSMC) | operator runs during session | ⚠️ mixed; post-fix next_bar improved |
| Cash identity arithmetic | manual (end_of_run row) | ✅ equity = cash+long−short |
| Heat feature | not implemented | ❌ N/A |

**Test command(s):**  
`cd winston_unit_test && bundle exec rspec spec/services/lab_fill_ticket_queue_spec.rb spec/services/lab_fill_cadence_spec.rb spec/services/portfolio_backtest_next_open_fill_spec.rb spec/services/portfolio_backtest_pyramid_reference_spec.rb spec/services/position_manager_fill_relative_stop_spec.rb spec/services/position_manager_scale_in_stops_spec.rb`

---

## 8. Environment, Dependencies, Data

- **Dependencies:** None new beyond Rails migration for `lab_fill_signal_evals`
- **Services:** local compose WUT assumed for operator PBR runs
- **Migrations:** `20260725120000_create_lab_fill_signal_evals.rb` — must migrate on deploy/ship

---

## 9. Risks & Technical Debt

- Uncommitted large WUT surface; must not `git add .` (secrets / stray files).
- Schema migration required before lab fill signal eval paths work on clean DB.
- Free-cash-led operator reads will keep overstating “success” until recon strip shows equity return + gross/net.
- Heat still a flat lot cap — concentration risk under correlated markets.
- Possible unrelated dirty trees in ecosystem tickets and winston_v2.

---

## 10. Open Questions

- **Ship heat BA now or after more PCS correlation maturity?** — needs product; blocks heat impl scope.
- **Should PBR recon strip always show total return % vs free-cash Δ?** — UX; blocks nothing.
- **OWDC 4-cell matrix still required for trust?** — product; blocks full OWDC sign-off.
- **Ownership of winston_v2 dirty files?** — operator; blocks accidental wrap commit.

---

## 11. Handoff & Resume Notes

- **Where I left off:** Explained MV and why free-cash +47% / $40k gross is not total return; operator invoked `/wrap`.
- **Next concrete step:** Promote follow-ups (or skip); commit WUT + ecosystem session files; migrate + re-run focused specs; optional ship-to-test.
- **Files to read first:**
  1. `ecosystem/docs/adr/2026-07-25-lab-t1-fill-queue.md`
  2. `ecosystem/docs/adr/2026-07-25-pyramid-scale-in-price-blocks.md`
  3. `ecosystem/docs/tickets/2026-07-25-ts-portfolio-heat-unit-limits.md`
  4. `winston_unit_test/app/services/lab_fill_ticket_queue.rb`
  5. `winston_unit_test/app/services/portfolio_position_manager.rb` (`cash_snapshot`)

---

## 12. Stakeholder Communications

- _None required._ Optional: short note that lab fill timing is now T+1 queue with explicit pass reasons, and PBR return should be read from equity not free cash.

---

## 13. Tools & Workflow Notes

- **Skills used:** wrap, session-report  
- **What worked well:** ADR + ticket separation for product locks vs backlog; cash identity is simple once formula is shown with the user’s row.  
- **Friction points:** Long session compacted; wrap must carefully attribute dirty files across monoliths.  
- **Subagent usage:** _None in wrap tail._

---

## 14. Follow-up Actions

- [ ] Commit + push WUT fill-queue/pyramid/stop work (migration included) — owner: operator/agent — due: wrap
- [ ] Commit + push ecosystem ADRs + heat ticket + this report — owner: agent — due: wrap
- [ ] Run focused rspec suite above after commit — owner: next session — due: before ship
- [x] BA/implement multi-level heat — **ticket already:** [`docs/tickets/2026-07-25-ts-portfolio-heat-unit-limits.md`](../tickets/2026-07-25-ts-portfolio-heat-unit-limits.md)
- [x] Cash-ledger recon scorecard — **filed:** [`docs/tickets/2026-07-25-pbr-cash-ledger-return-scorecard.md`](../tickets/2026-07-25-pbr-cash-ledger-return-scorecard.md)
- [x] PBR status-poll empty-state — **filed:** [`docs/tickets/2026-07-25-pbr-status-poll-missing-run-ux.md`](../tickets/2026-07-25-pbr-status-poll-missing-run-ux.md)
- [x] OWDC/OWD 4-cell matrix — **filed:** [`docs/tickets/2026-07-25-owdc-owd-four-cell-matrix.md`](../tickets/2026-07-25-owdc-owd-four-cell-matrix.md)
- [ ] Confirm winston_v2 dirty files not part of this session — owner: operator (not ticketed; wrap hygiene)

---

## 15. Appendix (optional)

### End-of-run cash identity (example row)

```
2026-07-02 end_of_run free_cash=$14699.89 equity=$12617.50 open=12
long_mv=$19086.72 short_mv=$21169.11
equity = 14699.89 + 19086.72 − 21169.11 = 12617.50
gross ≈ $40.3k; net ≈ −$2.1k short
```

If initial ≈ $10k: free-cash ~+47%; **equity total return ~+26%**.

### Key formulas

- **MV** = market value = units × mark (shorts as cover liability)
- **Equity** = free_cash + long_mv − short_mv
- **Total return** = (final_equity − initial_capital) / initial_capital
- **Gross controlled** = long_mv + short_mv
- **Net exposure** = long_mv − short_mv
