# Session Report — Kelly / Risk Scale → Wv2 Ops

**Date:** 2026-08-09  
**Time:** ~session start–20:29 MDT  
**Duration:** ~multi-hour (gap analysis + Session 1–2 implementation)  
**Project:** sawtooth Winston ecosystem  
**Working directory:** `/home/johnkoisch/Documents/com/sawtooth`  
**Branch:** `main` on ecosystem, winston_unit_test, winston_v2  
**Model:** Grok 4.5  
**Operator:** John  

---

## 1. Goal & Outcome

**Stated goal:** Ensure Kelly / risk-scale work is exportable from Winston Unit Test (WUT), part of Trading Strategy (TS) canonical form, and live in Winston v2 (Wv2) portfolio management (periodic / smooth Kelly position sizing from equity / closed-trade path).

**Outcome:** Delivered (plumbing + doctrine + lab scorecard + parity specs)

**One-line summary:** ADR-010 locked base geometry ⊥ meta Kelly scale; WUT export + Wv2 import/PositionSizer/recompute/DAR visibility shipped; hybrid matrix shows Kelly is host-specific, not a global default.

---

## 2. Work Completed

- Gap analysis plan: WUT meta-layer vs Wv2 static+OWD-only path  
- **WS0:** ADR-010, CONTEXT glossary, handoff provenance, doctrine tickets closed  
- **WS1:** WUT TS export + PortfolioConfigExporter TS fallback for `risk_scale_*`  
- **WS2:** Wv2 import stores `risk_scale_policy` / `risk_scale_config` on TS.parameters  
- **WS3:** Ported `RiskScale::{Config,State,Engine}`; PositionSizer applies scale  
- **WS4:** `risk_scale_state` on Portfolio; trade history; Daily Analysis + exit recompute  
- **WS5:** ProposedSize / ops shell / auditor / DAR scale visibility  
- **WS6:** Kelly hybrid Phase 1+2 scorecard filled (23/23 PBRs)  
- **WS7:** Import→size parity specs  

---

## 3. Code Delivered

### Files changed (this session only)

#### ecosystem

| File | Change | Notes |
|------|--------|-------|
| `docs/adr/ADR-010-risk-scale-meta-layer.md` | added | Accepted product rule |
| `CONTEXT.md` | modified | Risk Scale Policy glossary |
| `docs/business-context/wut-to-wv2-handoff.md` | modified | risk_scale_* provenance |
| `docs/analysis/2026-07-31-risk-scale-meta-layer.md` | modified | ADR-010 link |
| `docs/analysis/2026-08-03-kelly-hybrid-price-level-pbr-map.md` | added/filled | Full scorecard |
| `docs/tickets/2026-07-30-kelly-martingale-sizing-portfolio-management.md` | modified | Progress + acceptance |
| `docs/tickets/2026-07-31-adr-risk-scale-orthogonality.md` | modified | Done |
| `docs/tickets/2026-07-31-kelly-scale-not-global-default.md` | modified | Done |
| `docs/tickets/2026-08-03-kelly-hybrid-matrix.md` | modified | Done |
| `docs/session-reports/2026-08-09-2029-kelly-risk-scale-wv2-ops.md` | added | This report |

#### winston_unit_test

| File | Change | Notes |
|------|--------|-------|
| `app/models/trading_strategy.rb` | modified | to_full_strategy_json emits risk_scale_* |
| `app/services/portfolio_config_exporter.rb` | modified | TS fallback for scale |
| `lib/tasks/strategy_configs.rake` | modified | Note thin run_id path |
| `spec/models/trading_strategy_pbr_payload_spec.rb` | modified | Export scale specs |
| `spec/services/portfolio_config_exporter_spec.rb` | modified | Fallback specs |

#### winston_v2

| File | Change | Notes |
|------|--------|-------|
| `db/migrate/20260809120000_add_risk_scale_state_to_portfolios.rb` | added | jsonb path state |
| `db/schema.rb` | modified | risk_scale_state |
| `app/services/risk_scale/{config,state,engine}.rb` | added | Port from WUT |
| `app/services/operations/position_sizer.rb` | modified | base × scale |
| `app/services/operations/portfolio_config_importer.rb` | modified | Persist scale |
| `app/services/operations/portfolio_trade_history.rb` | added | Closed PnL history |
| `app/services/operations/risk_scale_recomputer.rb` | added | Day/close hooks |
| `app/services/operations/daily_analysis_runner.rb` | modified | on_trading_day! |
| `app/services/operations/journal_confirmation_service.rb` | modified | on_close! on exit |
| `app/services/operations/proposed_size.rb` | modified | Scale in note |
| `app/services/operations/ops_shell_panels.rb` | modified | Scale on recipe |
| `app/services/operations/portfolio_trading_strategy_auditor.rb` | modified | Scale checks |
| `app/services/daily_report_payload_builder.rb` | modified | chapter risk_scale |
| `app/services/daily_activity_report_markdown_renderer.rb` | modified | Scale label |
| `app/models/portfolio.rb` | modified | risk_scale_* helpers |
| `app/models/trading_strategy.rb` | modified | risk_scale helpers + export |
| `spec/services/risk_scale_engine_spec.rb` | added | Engine parity subset |
| `spec/services/operations/position_sizer_spec.rb` | modified | Scale cases |
| `spec/services/operations/portfolio_config_importer_spec.rb` | modified | Kelly round-trip |
| `spec/services/operations/portfolio_trade_history_spec.rb` | added | |
| `spec/services/operations/risk_scale_recomputer_spec.rb` | added | |
| `spec/services/operations/risk_scale_parity_spec.rb` | added | WS7 |

### Commits

- _Pending at wrap — commit/push in wrap Step 3–4_

### Branch / PR state at sign-off

- Branch: `main` (all three) — dirty with this session + unrelated prior work  
- Pushed: pending wrap  
- PR: not opened (direct main workflow)

---

## 4. Decisions Made

### Decision 1: Meta layer not peer Kelly strategy
- **Choice:** `risk_scale_policy` orthogonal to `risk_evaluation_strategy` (static/OWD)  
- **Why:** OWD + Kelly coexistence; peer S/M/K deprecated  
- **Reversibility:** easy in lab; ops fingerprints once exported  
- **Promote to ADR?** Yes — **ADR-010** accepted  

### Decision 2: Kelly not global trade-ready default
- **Choice:** Default `none`; host-specific promotion only  
- **Why:** Hybrid matrix — Mango/Mint lift, Yellow regression  
- **Reversibility:** easy  
- **Promote to ADR?** Yes — ADR-010 §C  

### Decision 3: Runtime state on Portfolio, not fingerprint
- **Choice:** `risk_scale_state` jsonb on OP  
- **Why:** Mult/n_steps path-dependent; ADR-006 methodology immutability  
- **Reversibility:** easy  

### Decision 4: Port RiskScale into Wv2 (no gem)
- **Choice:** Copy-adapt under `app/services/risk_scale/`  
- **Why:** Majestic monoliths  
- **Reversibility:** easy  

---

## 5. Insights Surfaced

- Terminology collision: ADR-008 “risk scale into trends” = OWD ladder; `risk_scale_policy` = meta money management — must not conflate.  
- Classic Kelly flattens OWD rungs — can rescue Mint DD or destroy Mango.  
- Flat-edge ε on Yellow Winston barely helps; classic_flat_eps05 is only partial recovery vs ctrl.  
- Best candidate fingerprint family if promoting: Winston Kelly calendar **66** on hosts like Mango (best Sharpe among Mango Kelly arms).  
- Without WS4 state, Kelly policy still sizes at 1.0× (safe); recompute is what makes ops “live.”  

---

## 6. Issues & Tickets

### Resolved this session
- ADR orthogonality ticket → ADR-010  
- Kelly not global default doctrine ticket  
- Kelly hybrid matrix ticket (scorecard complete)  
- Primary Kelly portfolio-management ticket largely complete for plumbing  

### Deferred
1. Cross-link hybrid scorecard into Berlekamp business analysis §1 — ticket `docs/tickets/2026-08-09-berlekamp-lessons-kelly-hybrid-crosslink.md`  
2. Optional Blue DNA Kelly panel — ticket `docs/tickets/2026-08-09-kelly-blue-dna-panel.md`  
3. Capture Mango wk66 fingerprint → paper OP — ticket `docs/tickets/2026-08-09-kelly-mango-wk66-fingerprint-paper.md`  
4. Archaeology: PBR 340 vs 341 trade-count drift — ticket `docs/tickets/2026-08-09-pbr-340-vs-341-drift.md`

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| WUT export + TS JSON scale | rspec trading_strategy + exporter | ✅ 16 examples |
| Wv2 RiskScale + sizer + import + recompute + parity | rspec risk_scale* + position_sizer + importer | ✅ 48 examples |
| Migration risk_scale_state | db:migrate on compose | ✅ |
| Kelly hybrid scorecard | rails runner scorecard | ✅ 23/23 completed |

**Test command(s):**

```bash
bin/compose exec -T winston_unit_test bundle exec rspec \
  spec/models/trading_strategy_pbr_payload_spec.rb \
  spec/services/portfolio_config_exporter_spec.rb

bin/compose exec -T winston_v2 bundle exec rspec \
  spec/services/risk_scale_engine_spec.rb \
  spec/services/operations/position_sizer_spec.rb \
  spec/services/operations/portfolio_config_importer_spec.rb \
  spec/services/operations/portfolio_trade_history_spec.rb \
  spec/services/operations/risk_scale_recomputer_spec.rb \
  spec/services/operations/risk_scale_parity_spec.rb

bin/compose exec -T winston_unit_test bin/rails runner lib/scripts/kelly_hybrid_matrix_scorecard.rb
```

---

## 8. Environment, Dependencies, Data

- **Dependencies:** None new  
- **Services:** compose winston_v2, winston_unit_test  
- **Migrations:** `20260809120000_add_risk_scale_state_to_portfolios` (Wv2)  

---

## 9. Risks & Technical Debt

- Unrelated dirty trees in WUT/Wv2/ecosystem from prior sessions — wrap commits **only** this session’s paths.  
- Closed-trade PnL = sum of journal flows; option/instrument packaging edge cases may need hardening.  
- Calendar “trading days” counted by Daily Analysis runs, not market calendar — acceptable for paper ops; may diverge from lab if DA skips days.  
- Thin `wut:strategies:export_config[run_id]` still incomplete (documented); use portfolio export or `ts_id=`.  

---

## 10. Open Questions

- **Promote wk66 fingerprint on Mango-like books to observation OPs?** — operator choice; blocks real-capital Kelly recipes  
- **Should Phase params cells be run?** — optional lab depth  

---

## 11. Handoff & Resume Notes

- **Where I left off:** WS0–WS7 implemented and tested; wrap committing session files  
- **Next concrete step:** If promoting Kelly: capture TS fingerprint from winning PBR (e.g. 393 wk66 Mango), export, paper import, watch mult over DA days  
- **Files to read first:**  
  1. `ecosystem/docs/adr/ADR-010-risk-scale-meta-layer.md`  
  2. `ecosystem/docs/analysis/2026-08-03-kelly-hybrid-price-level-pbr-map.md`  
  3. `winston_v2/app/services/operations/risk_scale_recomputer.rb`  
  4. `winston_v2/app/services/operations/position_sizer.rb`  

---

## 12. Stakeholder Communications

- Operator: Kelly is **plumbing-ready** in ops but **not** a blanket recipe upgrade — promote host-by-host.  

---

## 13. Tools & Workflow Notes

- **Skills used:** operator-prose, session-report, wrap; parallel subagents for WS1 / WS2+WS3  
- **What worked well:** Frozen JSON keys from WUT RiskScale::Config; parallel agents  
- **Friction:** `maintain_test_schema!` noise (localhost PG) during compose rspec — tests still ran  
- **Subagent usage:** WUT export agent; Wv2 import+RiskScale agent  

---

## 14. Follow-up Actions

- [ ] Berlekamp lessons cross-link — `docs/tickets/2026-08-09-berlekamp-lessons-kelly-hybrid-crosslink.md`  
- [ ] Blue DNA Kelly panel — `docs/tickets/2026-08-09-kelly-blue-dna-panel.md`  
- [ ] Mango wk66 paper fingerprint — `docs/tickets/2026-08-09-kelly-mango-wk66-fingerprint-paper.md`  
- [ ] PBR 340 vs 341 archaeology — `docs/tickets/2026-08-09-pbr-340-vs-341-drift.md`

---

## 15. Appendix (optional)

**Hybrid winners (Phase 1 headline):**

| Book | Best Kelly-ish | Ctrl |
|------|----------------|------|
| Mango | wk66 +262.7% / 36.9% DD / 0.75 | +149.9% / 47.5% / 0.58 |
| Mint | wk66 +497% return; classic best Sharpe 0.79 | ctrl DD 113% |
| Yellow | **none** +81.7% / 0.43 | Kelly arms mostly negative |
