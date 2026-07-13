# Session Report — PBR Business Analysis + Level 2 C0/P1

**Date:** 2026-07-13  
**Time:** ~14:30–17:15 MDT  
**Duration:** ~2h 45m  
**Project:** sawtooth Winston ecosystem (cross-monolith lab evaluation)  
**Working directory:** `/home/johnkoisch/Documents/com/sawtooth`  
**Branch:** `ecosystem` `main`; WUT runtime only for PBR executes  
**Model:** Grok 4.5 (xAI)  
**Operator:** johnkoisch  

---

## 1. Goal & Outcome

**Stated goal:**  
1. Evaluate PBRs for return, drawdown, survivability, risk vs composition/PCS; extract repeatable traits (esp. Blue 48).  
2. Avoid curve-fitting; assess top PBRs for optimization paths (TS13 only as sample).  
3. Operator review: passed-signal capacity; component attribution (risk vs pyramid vs multi-exit vs confirm).  
4. `/wrap` — file business analysis, next-step tickets, WUT exposure task, commit/push.

**Outcome:** Delivered  

**One-line summary:** Business analysis library created; Blue 48 success attributed mainly to accelerating risk + stop trail (not multi-exit/confirm); C0 and P1 experiments show capacity and swap are real levers; paper candidates Green 55 vs Blue 62 documented with full next-step tickets.

---

## 2. Work Completed

- Level 1 freeze of live WUT PBR metrics + PCS + viability gates  
- Passed-signal reason histograms and capacity narrative (Blue/Orange/Green)  
- Component attribution for PBR 44 vs 48 vs 23  
- New PBRs: **62** (C0 max_markets=4), **63** (P1 position_swap on)  
- Created `ecosystem/business_analysis/` as business-eval bucket; moved analysis there  
- Stub pointer left in `docs/analysis/`  
- Tickets: Level 2 remaining, paper-first decision, WUT business-analysis link; Blue membership ticket updated  
- Filing guides: `docs/README.md`, ecosystem `README.md`, `business_analysis/README.md`

---

## 3. Code Delivered

### Files changed

| File | Change | Notes |
|------|--------|-------|
| `ecosystem/business_analysis/README.md` | added | Bucket purpose + index |
| `ecosystem/business_analysis/2026-07-13-pbr-return-dd-pcs-evaluation.md` | added | Canonical business analysis |
| `ecosystem/docs/analysis/2026-07-13-pbr-return-dd-pcs-evaluation.md` | added | Move stub |
| `ecosystem/docs/README.md` | modified | Filing guide for business_analysis |
| `ecosystem/README.md` | modified | Contents bullet |
| `ecosystem/docs/tickets/2026-07-13-wut-expose-business-analysis-link.md` | added | WUT UI task |
| `ecosystem/docs/tickets/2026-07-13-pbr-level2-remaining-experiments.md` | added | R/X/E/P matrix |
| `ecosystem/docs/tickets/2026-07-13-paper-first-cohort-decision.md` | added | Green vs Blue paper |
| `ecosystem/docs/tickets/2026-07-07-revisit-portfolio-blue-membership-strategy.md` | modified | Risk-rescue evidence |
| `ecosystem/docs/session-reports/2026-07-13-1713-pbr-business-analysis-wrap.md` | added | This report |

### Runtime data (WUT DB, not in git)

| PBR | Path | Ret % | Max DD % | Sharpe | Gates |
|-----|------|-------|----------|--------|-------|
| 48 | baseline Blue dynamic | 2073.5 | 20.9 | 1.52 | trade_ready |
| 62 | C0 max_mkt=4 | 1415.4 | 41.6 | 1.11 | trade_ready |
| 63 | P1 swap on | 974.6 | 31.5 | 1.22 | trade_ready |

### Commits

- `ea906c2` — docs: business_analysis bucket, PBR evaluation, Level 2 tickets

### Branch / PR state at sign-off

- Ecosystem: `main` — clean, pushed (`ea906c2`)  
- WUT / Wv2 / DM: no source commits (lab executes only)  
- PR: not opened (direct main)

**Monoliths touched:** `ecosystem` (docs); `winston_unit_test` (runtime PBR 62/63 only).

---

## 4. Decisions Made

### Decision 1: Business analysis bucket
- **Choice:** `ecosystem/business_analysis/` for operator/stakeholder evaluations  
- **Why:** Distinct from technical `docs/analysis/` and domain `business-context/`  
- **Alternatives considered:** Keep only under `docs/analysis/`; root `business_analysis` as user suggested (adopted at ecosystem root)  
- **Reversibility:** easy  
- **Promote to ADR?** no  

### Decision 2: Anti-overfit experiment doctrine
- **Choice:** One axis at a time; new PBR IDs; no joint re-grid; transfer tests required  
- **Why:** Operator concern about curve-fitting  
- **Reversibility:** easy  
- **Promote to ADR?** no (document in business analysis)

### Decision 3: Provisional paper ranking
- **Choice:** Green 55 (discipline) vs Blue 62 (explore under honest caps); not uncapped 48 as default  
- **Why:** C0 degraded but did not kill Blue; swap-on hurt  
- **Reversibility:** easy — ticket for formal decision  
- **Promote to ADR?** no  

---

## 5. Insights Surfaced

- Blue static failure + dynamic success → **risk regime dominates** membership for this cohort.  
- Multi-exit and confirmational entry are **not** what made PBR 48 win (single VolExit, no confirm).  
- Large passed-signal piles ≠ reclaimable alpha via position swap (63 worse than 48).  
- Uncapped max_markets was a large free lunch; C0 still trade_ready.  
- Dynamic risk is **not** portable free lunch (Red DD worse; Orange 49 collapse).  
- final_cash ≫ final_equity on Blue dynamic runs with max_leverage=3 — accounting flag before real capital.

---

## 6. Issues & Tickets

### Resolved this session
- Business analysis filing location  
- Level 1 evaluation + C0/P1 experiments  

### Deferred (filed)
- `2026-07-13-pbr-level2-remaining-experiments.md` — R2/R3, X1/X3, transfer, P3  
- `2026-07-13-paper-first-cohort-decision.md` — Green vs Blue paper  
- `2026-07-13-wut-expose-business-analysis-link.md` — WUT UI link  
- Blue membership ticket updated in place  

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| PBR metrics freeze | rails runner vs DB | ✅ |
| Gates 48/44/55/56/62/63 | TradeReadyViabilityGates | ✅ |
| PBR 62 execute | completed ~31 min | ✅ |
| PBR 63 execute | completed ~20 min | ✅ |
| WUT UI for business_analysis | not built | ⚠️ ticket only |

**Test command(s):** `PortfolioBacktestRunner.new(62|63).execute`; gate evaluate; PassedSignal group counts.

---

## 8. Environment, Dependencies, Data

- **Dependencies:** None  
- **Services:** winston_unit_test compose for PBR executes  
- **Migrations:** None  
- **Data:** New WUT PBR rows 62, 63 + passed_signals (local PG)

---

## 9. Risks & Technical Debt

- In-sample full-window metrics only for 62/63 — holdout not yet run  
- Cash/equity identity under leverage still fuzzy  
- PBR 50 cash anomaly still open (unrelated, do not trust that ID)

---

## 10. Open Questions

- **First paper OP: Green 55 or Blue 62?** — operator; blocks Wv2 attention  
- **max_markets policy for ops?** — operator  
- **Invest in P3 counterfactual pass study?** — optional  

---

## 11. Handoff & Resume Notes

- **Where I left off:** Business analysis + tickets filed; wrap commit.  
- **Next concrete step:** Operator paper decision ticket **or** run R2/X1 from Level 2 ticket.  
- **Files to read first:**
  1. `ecosystem/business_analysis/2026-07-13-pbr-return-dd-pcs-evaluation.md`  
  2. `ecosystem/docs/tickets/2026-07-13-pbr-level2-remaining-experiments.md`  
  3. `ecosystem/docs/tickets/2026-07-13-paper-first-cohort-decision.md`  
  4. `ecosystem/docs/tickets/2026-07-13-wut-expose-business-analysis-link.md`  

**Useful URLs:**  
- http://localhost:3000/wut/portfolio_backtest_runs/48  
- http://localhost:3000/wut/portfolio_backtest_runs/62  
- http://localhost:3000/wut/portfolio_backtest_runs/63  

---

## 12. Stakeholder Communications

- Business analysis is the stakeholder-facing summary of “what should we paper first?”  
- Use `/stakeholder` if an email rewrite is needed.

---

## 13. Tools & Workflow Notes

- **Skills used:** wrap, session-report, record (inline tickets)  
- **What worked well:** Pre-registered single-axis PBRs; freezing live metrics before narrative  
- **Friction points:** Full portfolio backtests ~20–30 min each; results_json JSON type edge cases  
- **Subagent usage:** none this wrap  

---

## 14. Follow-up Actions

- [ ] Level 2 remaining experiments — owner: lab session — ticket: `2026-07-13-pbr-level2-remaining-experiments.md`  
- [ ] Paper-first decision — owner: johnkoisch — ticket: `2026-07-13-paper-first-cohort-decision.md`  
- [ ] WUT business analysis link — owner: eng — ticket: `2026-07-13-wut-expose-business-analysis-link.md`  
- [ ] Optional close/narrow Blue membership ticket after paper decision  

---

## 15. Appendix — Headline tables

### Top PBRs (live 2026-07-13)

| PBR | Port | Ret % | DD % | Sharpe | Risk |
|-----|------|-------|------|--------|------|
| 48 | Blue | 2073.5 | 20.9 | 1.52 | one_way_dynamic |
| 44 | Blue | 1532.1 | 34.7 | 1.49 | one_way_dynamic |
| 62 | Blue C0 | 1415.4 | 41.6 | 1.11 | one_way_dynamic |
| 41 | Orange | 839.8 | 59.7 | 1.05 | static |
| 55 | Green | 292.4 | 48.3 | 0.95 | static trade_ready |
| 63 | Blue P1 | 974.6 | 31.5 | 1.22 | one_way_dynamic + swap |

### Component ranking (hypothesis)

1. Risk regime (one_way_dynamic accelerating)  
2. Stop move_to_last_entry  
3. Capacity (max_markets)  
4. Entry class (secondary)  
5. Multi-exit / confirm — not drivers of 48  
