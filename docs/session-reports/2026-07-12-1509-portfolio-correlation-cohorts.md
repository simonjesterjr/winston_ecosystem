# Session Report — Portfolio Correlation Methodology, PCS, Color Cohorts

**Date:** 2026-07-12  
**Time:** multi-day session (2026-07-11 → 2026-07-12)  
**Duration:** ~ substantive multi-phase build  
**Project:** sawtooth Winston ecosystem  
**Working directory:** `/home/johnkoisch/Documents/com/sawtooth`  
**Branches:** `ecosystem` main, `winston_unit_test` main, `winston_v2` main  
**Model:** Grok (xAI)  

---

## 1. Goal & Outcome

**Stated goal:** Analyze portfolio correlation methodology (Red/Blue/White/Orange); plan optimization/litmus; implement corr_v2, PCS time series, WUT UI, PBR metadata, DAR, new cohorts Green/Pink/Blank/Rust; vet and paper-import to Wv2.

**Outcome:** Delivered (Phases 0–6 + vet/import ops). Dashboard implementation deferred to ticket.

**One-line summary:** corr_v2 PCS is live as WUT SoT with litmus, builder, PBR, DAR, and six Active paper cohorts (Green/Pink trade-ready).

---

## 2. Work Completed

- Audit of correlation math + White/Orange failure modes (twins, COPR dilution, window non-stationarity)
- Grill-with-docs: max\|r\|-first PCS, WUT SoT, flag-only degradation, archive O/W, six common set
- Phase 1: litmus rake + quality gates
- Phase 2: corr_v2 builder, PCS scorer, snapshots table
- Phase 3: WUT builder/calculator transparency UI
- Phase 4: PBR correlation_snapshot + export
- Phase 5: daily score job, internal API, Wv2 WutClient, DAR PCS section
- Phase 6: Green/Pink/Blank/Rust membership + registry + sidecars
- vet_trend all four new portfolios; export JSON
- Wv2 import + Active for Red/Blue/Green/Pink/Blank/Rust; Orange deactivated
- Preflight ATR DM-path fix + DM re-acquire CORN/WTI/XLI
- Plan, ADR-007, analysis docs, tickets filed

---

## 3. Code Delivered

### Files changed (high-signal)

| Area | Paths |
|------|--------|
| Ecosystem plan/ADR | `plans/portfolio-correlation-methodology-and-score.md`, `docs/adr/ADR-007-…`, `CONTEXT.md` |
| WUT correlation core | `market_correlation_calculator.rb`, `portfolio_correlation_builder.rb`, scorer, litmus, quality, snapshots |
| WUT UI | portfolio_builder, correlation_calculator, PBR show, `shared/_correlation_transparency_strip` |
| WUT ops | daily score job, internal correlation API, cohort build rake, preflight fix |
| Wv2 | `wut_client.rb`, enricher, DAR MD/PDF, daily analysis payload |
| Configs (bind mount, not git) | `portfolio_configs/portfolio-{green,pink,blank,rust}.{json,sidecar.json}`, registry |

### Commits

- _Pending wrap push — see wrap output below_

### Branch / PR state at sign-off

- Ecosystem / WUT / Wv2: `main` — commit+push in wrap  
- PR: not opened (direct main per wrap default unless asked)

---

## 4. Decisions Made

### Decision 1: PCS primary metric
- **Choice:** Max pairwise \|r\| first (mean secondary)
- **Why:** White mean looked fine while DBE/OILK ≈ 0.93
- **Reversibility:** easy via methodology version
- **Promote to ADR?** Yes — ADR-007

### Decision 2: WUT system of record for PCS
- **Choice:** WUT computes + stores; Wv2 WutClient fetches
- **Why:** Single formula; majestic-monolith independence
- **Reversibility:** costly if dual formulas diverge
- **ADR:** ADR-007

### Decision 3: Flag-only on PCS degradation
- **Choice:** DAR/next_steps review flags only (no auto rebalance)
- **Why:** ADR-006 engagement lock
- **Reversibility:** easy

### Decision 4: New cohorts, archive Orange/White
- **Choice:** Green/Pink/Blank/Rust + Red/Blue as six paper set
- **Why:** O/W membership quality failures
- **Reversibility:** easy (rebuild/reactivate)

### Decision 5: Seeds ICLN / PINK / ZROZ / XLI
- **Choice:** Liquid quality-pass thematic seeds
- **Why:** Validation of corr_v2 after engine shipped
- **Reversibility:** rebuild cohorts

---

## 5. Insights Surfaced

- Pearson implementation is trustworthy on liquid pairs (GLTR/GLD ≈ 0.91)
- Mean \|r\| alone is a bad primary metric (junk dilution + twin pairs)
- Greedy + shrinking date window admits twins that only appear correlated on final intersection
- Many DM symbols pass quality but lack `atr_17` until re-acquire — preflight must be DM-aware
- Green/Pink cleared DD gate; Blank/Rust still observation-only

---

## 6. Issues & Tickets

### Resolved this session
- Diversification “weak” label inversion suspicion — **clarified** (high pair); ticket closed
- Preflight ATR fall-through — **fixed**
- White/Orange non-correlation heuristics — **addressed** via archive + new cohorts

### Deferred (tickets created)
- `docs/tickets/2026-07-12-wut-portfolio-correlation-dashboard.md`
- `docs/tickets/2026-07-12-re-vet-blank-rust-trade-ready.md`
- `docs/tickets/2026-07-12-wv2-six-cohort-evaluate-smoke.md`
- `docs/tickets/2026-07-12-pcs-business-context-doc.md`
- `docs/tickets/2026-07-12-preflight-atr-return-dm-path.md` (Done note)
- Existing: Blue membership/strategy revisit (still open)

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| Litmus golden pairs | Live compose | ✅ PASS |
| Phase 2 specs | rspec scorer/builder | ✅ |
| Phase 3 helper specs | rspec | ✅ |
| Phase 4 attacher | rspec + PBR Red smoke PCS=73 | ✅ |
| Phase 5 daily score | 8 portfolios scored | ✅ |
| Phase 5 enricher | rspec | ✅ |
| Cohort builds | sidecars + registry + overlaps ≤25% | ✅ |
| vet_trend ×4 | Green/Pink trade_ready; Blank/Rust observation | ✅ |
| Wv2 import Active=6 | list | ✅ |
| Wv2 evaluate smoke | not run | ⚠️ ticket |

**Test commands:**
```bash
./bin/compose exec -T winston_unit_test bin/rails portfolios:correlation_litmus
./bin/compose exec -T winston_unit_test bin/rails portfolios:correlation_daily_score
./bin/compose exec -T winston_v2 bin/rails wv2:portfolios:list
```

---

## 8. Environment, Dependencies, Data

- **Dependencies:** None new (HTTParty already in Wv2)
- **Services:** compose WUT, Wv2, DM, redis, postgres
- **Migrations (WUT):**  
  - `20260711210000_create_portfolio_correlation_snapshots`  
  - `20260711220000_add_correlation_snapshot_to_portfolio_backtest_runs`
- **Data:** DM re-acquire CORN, WTI, XLI; portfolio_configs bind-mount (not a git repo)

---

## 9. Risks & Technical Debt

- Blank/Rust extreme DD — paper only  
- Fixed window should be default for all builds (cohort rake has it; builder CLI optional)
- portfolio_configs artifacts not versioned in git  
- Dual Active hygiene relies on operator discipline (six Active is intentional)

---

## 10. Open Questions

- **Should Blank/Rust membership be rebuilt before re-vet?** — operator; ticket  
- **Activate only trade_ready Green/Pink for quieter paper?** — operator preference  

---

## 11. Handoff & Resume Notes

- **Where I left off:** Six Active in Wv2; dashboard not implemented (design + ticket only)
- **Next concrete step:** Implement WUT correlation dashboard ticket, or run Wv2 evaluate smoke
- **Files to read first:**  
  1. `ecosystem/plans/portfolio-correlation-methodology-and-score.md`  
  2. `ecosystem/docs/adr/ADR-007-portfolio-correlation-score-sot.md`  
  3. `ecosystem/docs/analysis/2026-07-12-portfolio-correlation-dashboard.md`  
  4. `ecosystem/docs/tickets/2026-07-12-*.md`

---

## 12. Stakeholder Communications

- Operator: six paper portfolios Active; Green/Pink economically gate-pass; Blank/Rust observation-only  
- _No external email drafted_

---

## 13. Tools & Workflow Notes

- **Skills used:** grill-with-docs (inline), wrap, session-report, record  
- **What worked well:** phased plan + litmus before rebuild; fixed window rebuild of Blank  
- **Friction:** preflight ATR bug; long sequential vet_trend (~2.5h total); portfolio_configs not in git  
- **Subagent usage:** none for final wrap  

---

## 14. Follow-up Actions

- [ ] Build Portfolios correlation dashboard — ticket  
- [ ] Re-vet Blank/Rust for trade_ready — ticket  
- [ ] Wv2 evaluate smoke for six — ticket  
- [ ] PCS business-context doc — ticket  
- [ ] Commit/push ecosystem, WUT, Wv2 (wrap)  

---

## 15. Appendix

### Vet winners summary

| Portfolio | Entry | Exit | Ret% | MaxDD% | kind |
|-----------|-------|------|------|--------|------|
| Green | Breakout55Day | VolExit | 292 | 48.3 | trade_ready |
| Pink | Breakout5Day | VolExit | 137 | 49.5 | trade_ready |
| Blank | Breakout5Day | VolExit | 671 | 55.0 | observation |
| Rust | Breakout5Day | VolExit | 685 | 77.4 | observation |

### Six Active Wv2 IDs

Red #5, Blue #7, Green #8, Pink #9, Blank #10, Rust #11
