# Session Report — Close-Trigger Strength + Lab Fill Cadence

**Date:** 2026-07-24  
**Time:** ~09:50–16:58 local (MDT)  
**Duration:** ~7h  
**Project:** sawtooth Winston ecosystem (cross-monolith)  
**Working directory:** `/home/johnkoisch/Documents/com/sawtooth`  
**Branch:** `ecosystem` `main`; `winston_unit_test` `main`  
**Model:** Grok 4.5 (xAI)  
**Operator:** johnkoisch  

---

## 1. Goal & Outcome

**Stated goal:**  
1. File BA ticket: close price as stronger trigger than high/low; strength-aware one-way dynamic.  
2. Run Axis A (close entry) and Axis B (`one_way_dynamic_close`) PBR experiments.  
3. Axis C: verify Signal(T)→fill T+1 open; fix lab if wrong.  
4. Close research with BA + business rules.

**Outcome:** Delivered  

**One-line summary:** Close-trigger and strength-risk experiments completed (PBRs 142–150); H3 found lab same-day open fills; lab next-open fill path implemented and smoke-verified; research ticket archived; BA written.

---

## 2. Work Completed

- Filed research ticket (later archived Done) + INDEX  
- Parent freeze for active one_way_dynamic PBRs  
- Phase 1 Axis A: close-breakout strategies + CT01–CT05 (142–146)  
- Phase 2 Axis B: strength classifier + `OneWayDynamicCloseRiskEvaluation` + CT06–CT09 (147–150)  
- Axis C audit: lab Signal(T)→**same-day open** (not T+1)  
- Fixed lab fill cadence: default `next_bar_open` pending queue  
- Fixed `TradingSignal` attr_accessor shadowing `bar_date`/`market_id`  
- BA write-up + business rules  
- Follow-on fill ticket Done/archived  
- Controlled A/B cadence impact (PBR 154 vs 155, 3y Blue 62 window)

---

## 3. Code Delivered

### Files changed

**winston_unit_test**

| File | Change | Notes |
|------|--------|-------|
| `app/strategies/entry_exit/swing_breakout_5_day_close_strategy.rb` | added | Close-confirmed Swing5 |
| `app/strategies/entry_exit/breakout_20_day_close_strategy.rb` | added | Close-confirmed BO20 |
| `app/strategies/risk/signal_strength_classifier.rb` | added | weak/standard/aggressive |
| `app/strategies/risk/one_way_dynamic_close_risk_evaluation.rb` | added | W-base / W-step + aggressive |
| `app/services/lab_fill_cadence.rb` | added | next_bar_open default |
| `lib/scripts/close_trigger_experiment_matrix.rb` | added | AXIS=A\|B matrix |
| `app/services/portfolio_backtest_runner.rb` | modified | pending fills; strength; cadence |
| `app/services/position_manager.rb` | modified | fill_activity pricing/date |
| `app/services/portfolio_backtest/entry_requirement_calculator.rb` | modified | fill_price |
| `app/models/trading_signal.rb` | modified | remove attr_accessor shadow |
| `app/strategies/strategy_registry.rb` | modified | register new strategies |
| `app/services/strategy_lookback.rb` | modified | close strategy periods |
| `app/strategies/risk/*_risk_evaluation.rb` | modified | signal_strength kwarg |
| `spec/strategies/close_breakout_strategies_spec.rb` | added | 14 examples |
| `spec/strategies/one_way_dynamic_close_risk_evaluation_spec.rb` | added | risk + classifier |
| `spec/services/lab_fill_cadence_spec.rb` | added | cadence modes |
| `spec/services/portfolio_backtest_next_open_fill_spec.rb` | added | enqueue smoke |

**ecosystem**

| File | Change | Notes |
|------|--------|-------|
| `business_analysis/2026-07-24-close-trigger-signal-strength.md` | added | H1/H2/H3 + rules + fill fix note |
| `business_analysis/README.md` | modified | index |
| `docs/tickets/archive/2026-07-24-close-trigger-signal-strength-one-way-dynamic.md` | added | research Done |
| `docs/tickets/archive/2026-07-24-lab-pbr-signal-x-fill-x1-open.md` | added | fill fix Done |
| `docs/tickets/INDEX.md` | modified | backlog |
| `docs/session-reports/2026-07-24-1658-close-trigger-and-lab-fill-cadence.md` | added | this report |

### Runtime lab data (WUT DB, not in git)

| PBR | Role |
|-----|------|
| 142–146 | Axis A close entry |
| 147–150 | Axis B strength risk |
| 153 | Short smoke next_open |
| 154 | A/B same_bar_open (3y) |
| 155 | A/B next_bar_open (3y) |

### Commits

- _Pending at report write — see wrap commit step_

### Branch / PR state at sign-off

- Ecosystem + WUT `main` — dirty until wrap commit  
- PR: not opened (direct main)

**Monoliths touched:** `ecosystem` (docs), `winston_unit_test` (code)

---

## 4. Decisions Made

### Decision 1: Research as ticket + BA (not defect issue)
- **Choice:** Business analysis ticket → BA doc  
- **Why:** Methodology evaluation, not a capital defect  
- **Reversibility:** easy  

### Decision 2: Axis A then B (entry then risk)
- **Choice:** Close primary first; strength risk keeps high/low primary  
- **Why:** Isolate H1 vs H2; anti-overfit one axis  
- **Reversibility:** easy  

### Decision 3: Lab default fill = next_bar_open
- **Choice:** Signal(T) queue → fill T+1 open; stops same-day  
- **Why:** ADR-009 ops parity; Axis C failed  
- **Alternatives:** same_bar_open legacy via ENV  
- **Reversibility:** easy (ENV override)  
- **Promote to ADR?** no (implementation of existing ADR-009 lab side)

### Decision 4: Do not re-run full close-trigger matrix under next_open in-session
- **Choice:** Document historical 142–150 as same-day open; smoke + 3y A/B for impact  
- **Why:** Time; path dependency large  
- **Reversibility:** re-run later  

---

## 5. Insights Surfaced

- Breakouts use high/low; MAs/penetration already use close — H1 most relevant to breakouts.  
- CT01 (close Swing5 on Blue 62) strong H1 win; stacking close primary on hard confirm hurts return.  
- CT06≡CT07 — W-base vs W-step no separation on Blue 62.  
- CT08 (80 + strength risk) large return lift, worse DD.  
- Lab fill bug was **systemic and path-changing**, not small unidirectional slippage: 3y Blue A/B old **380%**/882 trades vs next **552%**/394 trades (old looked *worse* on this window).  
- `TradingSignal` attr_accessor blocked signal-date persistence — silent data bug.

---

## 6. Issues & Tickets

### Resolved this session
- Research: close-trigger / one_way_dynamic_close — Done, archived  
- Lab PBR Signal(T)→T+1 open — Done, archived  

### Deferred
- Re-run close-trigger PBRs 142–150 (or promotion candidates) under `next_bar_open`  
- Walk-forward CT08 under next_open before any paper recipe change  
- Optional: weak-path diagnostics (why CT06≡CT07)  
- PBR show ladder UI (existing issue, not fixed this session)

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| Close breakout specs | rspec 14 ex | ✅ |
| Close risk + classifier specs | rspec | ✅ |
| Lab fill cadence specs | rspec 8 ex | ✅ |
| Axis A PBRs 142–146 | full execute | ✅ completed |
| Axis B PBRs 147–150 | full execute | ✅ completed |
| Axis C audit | 50-entry samples | ✅ same-day open pre-fix |
| Next-open smoke PBR 153 | 43/43 fill_after signal | ✅ |
| Cadence A/B 154 vs 155 | 3y Blue 62 | ✅ large path delta |

**Test command(s):**  
`bundle exec rspec spec/strategies/close_breakout_strategies_spec.rb spec/strategies/one_way_dynamic_close_risk_evaluation_spec.rb spec/services/lab_fill_cadence_spec.rb spec/services/portfolio_backtest_next_open_fill_spec.rb`

---

## 8. Environment, Dependencies, Data

- **Dependencies:** None new  
- **Services:** compose WUT + DM parquet for bars  
- **Migrations:** None  

---

## 9. Risks & Technical Debt

- Historical PBR absolute economics (pre-fill-fix) not ops-comparable  
- Pending-fill path is new; long full-sample re-runs of all color PBRs not yet done under next_open  
- LEAP entry path may not pass `fill_activity` yet (stock path covered)  
- Dual exit/entry queue edge cases on sparse market calendars — smoke OK, not exhaustively tested  

---

## 10. Open Questions

- **Re-run which parents under next_open first?** — 62, 80, paper candidates; blocks: promotion confidence  
- **Should soft-confirm / always_in_market interact with pending queue differently?** — needs product call if odd behavior appears  

---

## 11. Handoff & Resume Notes

- **Where I left off:** Fill cadence fixed and verified; A/B impact quantified; research closed; wrap in progress  
- **Next concrete step:** Re-run Blue 62 full sample + PBR 80 under `next_bar_open`; optionally re-run close-trigger winners CT01/CT08  
- **Files to read first:**  
  1. `ecosystem/business_analysis/2026-07-24-close-trigger-signal-strength.md`  
  2. `winston_unit_test/app/services/lab_fill_cadence.rb`  
  3. `winston_unit_test/app/services/portfolio_backtest_runner.rb` (pending fills)  
  4. Archive tickets for close-trigger + lab fill  

---

## 12. Stakeholder Communications

- _None required._ Operator already has BA rules. Optional: one-liner that lab fills now match ops T+1 open doctrine.

---

## 13. Tools & Workflow Notes

- **Skills used:** record (ticket filing), session-report/wrap  
- **What worked well:** Parent freeze from live DB; FAST_BACKTEST; campaign tags in results_json  
- **Friction points:** Host tool timeouts killing long PBR shells (container process sometimes continued); `attr_accessor` shadow was subtle  
- **Subagent usage:** none  

---

## 14. Follow-up Actions

- [ ] Re-run Blue 62 full history under `next_bar_open` — compare to PBR 62 baseline  
- [ ] Re-run PBR 80 (EMA20 confirm winner) under `next_bar_open`  
- [ ] Optionally re-run CT01/CT08 under next_open for H1/H2 refresh  
- [ ] Walk-forward CT08-class recipe before paper promotion  
- [ ] Consider LEAP `add_leap_position` fill_activity parity  
- [ ] PBR UI ladder visibility (existing open issue)

---

## 15. Appendix (optional)

### Axis A headline (old same-day open)

| Cell | PBR | Δ vs parent |
|------|-----|-------------|
| CT01 | 142 | ret +300, DD −16, Sh +0.49 vs 62 |
| CT04 | 145 | Orange quality + return win |
| CT02/03 | 143/144 | ret down, DD better on confirm stack |
| CT05 | 146 | uncapped 48 loses under close primary |

### Axis B headline

| Cell | PBR | Note |
|------|-----|------|
| CT06/07 | 147/148 | identical; ~flat vs 62 |
| CT08 | 149 | ret +1041, DD worse vs 80 |
| CT09 | 150 | DD/Sharpe win vs 72 |

### Cadence A/B (2020–2022 Blue 62)

| | Ret | DD | Sh | Trades |
|--|-----|-----|-----|--------|
| same_bar_open 154 | 380 | 31.7 | 1.31 | 882 |
| next_bar_open 155 | 552 | 27.5 | 1.59 | 394 |
