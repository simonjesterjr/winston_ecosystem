# Session Report — Confirmational Entry Experiment + One-Way Dynamic Export

**Date:** 2026-07-19  
**Time:** ~session through wrap  
**Duration:** multi-hour (lab matrix + export fix)  
**Project:** sawtooth Winston ecosystem  
**Working directory:** `/home/johnkoisch/Documents/com/sawtooth`  
**Branch:** `main` on `ecosystem`, `winston_unit_test`, `winston_v2`  
**Model:** Grok (xAI)  
**Operator:** johnkoisch  

**Monoliths touched:** `ecosystem`, `winston_unit_test`, `winston_v2`

---

## 1. Goal & Outcome

**Stated goal:** Strategy discussion on trend-following optimizations (risk scale + confirmatory signals); then run a comprehensive confirmational-entry experiment on winning PBRs; capture analysis/ADRs; fix missing pyramid ladder in handoff JSON.

**Outcome:** Delivered

**One-line summary:** Ran a 20-cell confirmational-entry matrix (winner **PBR 80 / EMA20 hard** on Blue 62); shipped soft-confirm + ATR confirms + FAST_BACKTEST; ADR-008; fixed dangerous omission of `pyramid_risks` from WUT→Wv2 export with hard validation.

---

## 2. Work Completed

- Strategy analysis: confirmational entry vs pyramiding; passed-signal / reallocation research program (discussion).
- 20-PBR confirm matrix on parents **62, 71, 72, 57, 55** (not 76).
- Soft confirm (entry-only 0.5× risk) + ATR contraction/expansion confirm strategies.
- Lookback fix so confirms longer than primary breakout_period receive enough history.
- FAST_BACKTEST path (~10–15× wall-clock) for lab campaigns.
- Business analysis write-up of all 20 cells; ADR-008; glossary terms.
- Diagnosed one-way dynamic ladder **is** active in lab fills; UI/export gaps.
- **Critical fix:** export/fingerprint/Wv2 import now carry and validate pyramid ladder.

---

## 3. Code Delivered

### Files changed (this session only)

| File | Change | Notes |
|------|--------|-------|
| `winston_unit_test/app/strategies/testing_strategy.rb` | modified | Soft confirm + risk_size_multiplier |
| `winston_unit_test/app/strategies/entry_exit/atr_contraction_confirm_strategy.rb` | added | Non-price confirm |
| `winston_unit_test/app/strategies/entry_exit/atr_expansion_confirm_strategy.rb` | added | Non-price confirm |
| `winston_unit_test/app/strategies/strategy_registry.rb` | modified | Register ATR confirms |
| `winston_unit_test/app/services/strategy_lookback.rb` | modified | ATR confirm periods |
| `winston_unit_test/app/services/portfolio_backtest_runner.rb` | modified | Soft config, lookback, FAST_BACKTEST |
| `winston_unit_test/app/services/portfolio_backtest/entry_requirement_calculator.rb` | modified | Soft size mult (clamp issue remains for ladder) |
| `winston_unit_test/app/services/position_manager.rb` | modified | Soft size mult; gated debug file |
| `winston_unit_test/app/services/one_way_dynamic_risk_validator.rb` | added | Export/capture validation |
| `winston_unit_test/app/services/portfolio_config_exporter.rb` | modified | Embed + validate ladder |
| `winston_unit_test/app/services/trading_strategy_fingerprint_capture.rb` | modified | Ladder in payload/full_config |
| `winston_unit_test/lib/scripts/confirm_entry_experiment_matrix.rb` | added | 20-cell campaign runner |
| `winston_unit_test/lib/tasks/portfolio_configs.rake` | modified | Abort if dynamic missing ladder |
| `winston_unit_test/spec/services/*` / `spec/strategies/*` | added/modified | Soft, ATR, validator, exporter |
| `winston_v2/app/services/operations/portfolio_config_importer.rb` | modified | Store ladder on TS.parameters |
| `winston_v2/app/services/operations/position_sizer.rb` | modified | Level-aware risk fraction |
| `ecosystem/business_analysis/2026-07-18-confirmational-entry-experiment.md` | added | Full results |
| `ecosystem/business_analysis/README.md` | modified | Index link |
| `ecosystem/docs/adr/ADR-008-confirmational-entry-and-risk-scale.md` | added | Doctrine + handoff rule |
| `ecosystem/docs/issues/2026-07-19-one-way-dynamic-pyramid-risk-visibility-and-cap.md` | added | Visibility + clamp + export |
| `ecosystem/docs/tickets/2026-07-19-pbr-show-pyramid-ladder-and-estimate-cap.md` | added | Remaining UI/clamp work |
| `ecosystem/CONTEXT.md` | modified | Confirmational Entry; One-Way Dynamic Risk |
| `ecosystem/docs/session-reports/2026-07-19-1400-confirm-entry-experiment-and-export.md` | added | This report |

### Lab artifacts (DB / volume, not all git)

- PBRs **78–97** confirm matrix; winner **PBR 80** (C03 EMA20 hard).  
- Export file: `/portfolio_configs/portfolio-blue-pbr80.json` (includes ladder).  
- TSS 21/22 ATR confirm strategies seeded in WUT.

### Commits

- _Pending wrap commit._

### Branch / PR state at sign-off

- Branch: `main` on each monolith — dirty with session + unrelated local changes  
- Pushed: pending wrap  
- PR: not opened (direct main workflow)

---

## 4. Decisions Made

### Decision 1: Confirmational entry is initial-entry only
- **Choice:** Confirms gate first entry; pyramids stay ATR-step risk adds.  
- **Why:** Operator product rule; code already separated.  
- **Reversibility:** easy  
- **Promote to ADR?** Yes → **ADR-008**

### Decision 2: Hard confirm preferred over soft for promotion
- **Choice:** Soft 0.5× did not beat hard twins on Blue 62.  
- **Why:** Experiment C09/C10 vs C01/C04.  
- **Reversibility:** easy  
- **Promote to ADR?** Yes (ADR-008)

### Decision 3: Paper-science recipe after experiment
- **Choice:** Blue C0 + Swing5 + **EMA20 hard confirm** + VolExit + one_way R1 (PBR 80). Alternate SMA20 (PBR 78). Transfer confirm: Penetration.  
- **Why:** Best Sharpe/return/DD package on honest caps.  
- **Reversibility:** easy (paper first)  
- **Promote to ADR?** Yes (ADR-008 provisional)

### Decision 4: Handoff must include pyramid ladder
- **Choice:** Export fails without ladder when `one_way_dynamic`.  
- **Why:** Silent flat risk in Wv2 is dangerous.  
- **Reversibility:** costly if broken in prod  
- **Promote to ADR?** Yes → ADR-008 §E

---

## 5. Insights Surfaced

- Empty confirms on “winning” TSs left large edge on Blue 62 (EMA20/SMA20 hard).  
- Soft confirm ≠ free lunch.  
- Penetration transfers better than SMA20 across books.  
- Green 55 + SMA20 was a noop (primary already 55d).  
- One-way ladder **works in lab** when concurrent pyramids exist; UI/export made it look flat.  
- PBR status write every day + double write + debug file I/O caused ~30 min runs; FAST_BACKTEST → ~2–3 min.  
- Entry lookback used primary breakout_period only — confirms with longer windows saw empty history (fixed).

---

## 6. Issues & Tickets

### Resolved this session
- Confirm experiment campaign complete (PBR 78–97).  
- Export missing `pyramid_risks` — fixed + validated.  
- ATR confirm strategies + soft confirm + lookback + FAST_BACKTEST.

### Deferred
- PBR show ladder UI + journal risk % column — ticket partially done.  
- `EntryRequirementCalculator` clamp of ladder to base 2% — still open.  
- Paper import of PBR 80 to Wv2 Active OP + re-import any old one_way_dynamic OPs.  
- Walk-forward on C03 before real capital.  
- Broader strategy epics: passed-signal P3 counterfactual, R2/R3 ladders, multi-OP capital, heat caps.  
- Soft confirm productization.

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| Soft/ATR/validator/exporter specs | rspec (8 examples) | ✅ |
| Confirm matrix 20/20 | WUT DB metrics | ✅ |
| PBR 80 export ladder | rails runner + JSON file | ✅ |
| Wv2 PositionSizer ladder | inline rails runner | ✅ |
| Wv2 import e2e | not re-run full import this session | ⚠️ |
| EntryRequirementCalculator clamp | code review only | ❌ open |

**Test command(s):**  
`bundle exec rspec spec/services/one_way_dynamic_risk_validator_spec.rb spec/services/portfolio_config_exporter_spec.rb`  
(+ soft/ATR specs earlier)

---

## 8. Environment, Dependencies, Data

- **Dependencies:** None new gems  
- **Services:** `winston_unit_test`, `winston_v2`, postgres, redis  
- **Migrations:** None  
- **Data:** WUT PBR 78–97; TSS 21–22; portfolio config volume file pbr80  

---

## 9. Risks & Technical Debt

- Old Wv2 OPs imported before fix still lack ladder until re-import.  
- Fingerprint of pre-fix TS may not hash ladder until re-capture (export backfills full_config).  
- Estimate clamp can desync cash/pass from true fill risk under deep pyramids.  
- Dirty trees on main contain unrelated uncommitted work — wrap must stage **session files only**.

---

## 10. Open Questions

- **Promote PBR 80 to paper Active in Wv2 this week?** — operator; blocks paper path.  
- **Force re-fingerprint when ladder added to payload?** — may create new TS id; currently backfill only.  
- **Align Wv2 unit formula with WUT (risk$/stop$ vs risk$/(atr×mult×price))?** — separate review; not changed this session.

---

## 11. Handoff & Resume Notes

- **Where I left off:** Export fix verified; wrap started.  
- **Next concrete step:** Import `portfolio-blue-pbr80.json` to Wv2 (or re-export with `PAPER_CAPS=1`); confirm TS.parameters has ladder; activate paper OP.  
- **Files to read first:**  
  1. `ecosystem/business_analysis/2026-07-18-confirmational-entry-experiment.md`  
  2. `ecosystem/docs/adr/ADR-008-confirmational-entry-and-risk-scale.md`  
  3. `winston_unit_test/app/services/portfolio_config_exporter.rb`  
  4. `ecosystem/docs/tickets/2026-07-19-pbr-show-pyramid-ladder-and-estimate-cap.md`

---

## 12. Stakeholder Communications

- Operator: confirm experiment winner is **PBR 80 (EMA20 hard)**; re-export/import required for one_way_dynamic ladder handoff safety.

---

## 13. Tools & Workflow Notes

- **Skills used:** wrap, session-report, (prior) record-style filing  
- **What worked well:** Pre-registered 20-cell matrix; FAST_BACKTEST after diagnosing I/O; validate export refuse-path.  
- **Friction:** 30 min PBRs until FAST_BACKTEST; container bind-mount git; broad dirty trees.  
- **Subagent usage:** None for final wrap  

---

## 14. Follow-up Actions

- [ ] Import/re-import PBR 80 JSON to Wv2 with ladder present  
- [ ] PBR show UI ladder + journal risk % (ticket remaining)  
- [ ] Fix EntryRequirementCalculator one_way clamp  
- [ ] Walk-forward C03 before real capital  
- [ ] File/run passed-signal P3 + R2/R3 transfer experiments (strategy backlog)  
- [ ] Commit/push session files only across ecosystem / WUT / Wv2  

---

## 15. Appendix

### Headline matrix (Blue 62 parent: +1415% / DD 41.6% / Sh 1.11)

| Cell | Confirm | Ret | DD | Sharpe |
|------|---------|-----|-----|--------|
| C03 PBR80 | EMA20 hard | **2357%** | **27.5%** | **1.57** |
| C01 PBR78 | SMA20 hard | 2349% | 32.8% | 1.43 |
| C04 | Penetration hard | 1285% | 21.9% | 1.34 |

### R1 ladder (parent 62 / PBR 80)

`long [2,3,4,6,6]%` · `short [2,2,2,3,3]%`
