# Session Report — Risk Scale Matrix Setup, Badges, Findings

**Date:** 2026-07-31  
**Time:** ~11:49–15:56 MDT (continuation after morning wrap)  
**Duration:** ~4h operator-facing  
**Project:** sawtooth Winston ecosystem  
**Working directory:** `/home/johnkoisch/Documents/com/sawtooth`  
**Branch:** `main` (winston_unit_test + ecosystem)  
**Model:** Grok 4.5  
**Operator:** John  

---

## 1. Goal & Outcome

**Stated goal:** Finish risk-scale verification path — visual indicators, full 3×4 matrix PBRs, interpret completed results.

**Outcome:** Delivered (badges + 12 pending/completed PBRs + analysis)

**One-line summary:** Meta risk-scale is visible in WUT UI; 12-cell Yellow matrix ran; AM/M defaults never stepped; Kelly path-dependent; OWDC-none is the standout base recipe.

---

## 2. Work Completed

- Added risk-scale badges on PBR index (**Risk / Scale** column) and show-page **Money management** banner (martingale red guardrail, Kelly amber, AM sky, static gray).
- Model helpers: `PortfolioBacktestRun#risk_scale_policy` / `#risk_scale_config`.
- Created operator-runnable matrix (not agent-monitored):
  - **OWD + scale:** 345–348  
  - **static + scale:** 349–352  
  - **OWDC + scale:** 353–356  
- Analyzed completed scorecard (all 12 completed by operator).

---

## 3. Code Delivered

### Files changed (winston_unit_test)

| File | Change | Notes |
|------|--------|-------|
| `app/helpers/portfolio_backtest_runs_helper.rb` | modified | scale badges + banner |
| `app/models/portfolio_backtest_run.rb` | modified | risk_scale_policy helpers |
| `app/views/portfolio_backtest_runs/index.html.erb` | modified | Risk/Scale column |
| `app/views/portfolio_backtest_runs/show.html.erb` | modified | money-management banner |

### Commits

- _Filled after wrap commit/push._

### Branch / PR state at sign-off

- Branch: `main`  
- Prior morning wrap already pushed risk-scale engine (`6bd1666` WUT, `b22fdfc` ecosystem)  
- Badge UI commit: this wrap  

---

## 4. Decisions Made

### Decision 1: 3×4 matrix (base × scale)
- **Choice:** static / OWD / OWDC × none / AM / M / Kelly on Yellow  
- **Why:** isolate scale vs base geometry  
- **Reversibility:** easy  

### Decision 2: Findings interpretation
- **Choice:** Treat AM/M as **untested** (n_steps=0), not “neutral economics”; treat Kelly as live but recipe-specific; rank OWDC-none as best none-cell  
- **Why:** scorecard evidence  
- **Promote to ADR?** with prior risk-scale ADR if filed  

---

## 5. Insights Surfaced

- Default AM/M hybrid (44d, equity ±16%) never moved `n_steps` on Yellow full sample → noop vs none.  
- Kelly end mult only ~1.02–1.04 but path dependence large (static rescue, OWD mild lift, OWDC collapse).  
- Base ranking (scale=none): OWDC (+176% / 39% DD / 0.64) > OWD (+143% / 49% / 0.56) > static (−0.8% / 41% / 0.12).  
- OWD rows show large negative free cash vs positive equity — leverage/MTM residue; rank on return/DD/Sharpe.  

---

## 6. Issues & Tickets

### Tickets filed at wrap (2026-07-31)

- `docs/tickets/2026-07-31-am-m-forced-step-smoke.md`
- `docs/tickets/2026-07-31-adr-risk-scale-orthogonality.md`
- `docs/tickets/2026-07-31-business-analysis-risk-scale-matrix-345-356.md`
- `docs/tickets/2026-07-31-kelly-scale-not-global-default.md`
- `docs/tickets/2026-07-31-yellow-owdc-none-paper-candidate.md`


### Resolved this session
- Operator could not see scale policy at a glance → badges/banner  

### Deferred
- AM/M smoke with knobs that force steps (21d, ±8%, or streak 3)  
- Fair re-score AM/M after steps proven  
- Kelly promotion policy (do not ship globally; OWDC regression)  
- ADR for risk-scale orthogonality  
- Scorecard doc formalize in business_analysis  
- Parallel trading-system ticket still Proposed  
- Unrelated dirty ecosystem tickets / old session report left uncommitted  

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| Risk scale engine (prior) | rspec | ✅ morning wrap |
| 12-cell matrix | operator completed PBRs | ✅ metrics loaded |
| AM/M default behavior | n_steps end state | ⚠️ noop (config too soft) |
| UI badges | code + rails helper labels | ✅ created; operator hard-refresh |

**Test command(s):** inspect PBRs 345–356 show pages; index Risk/Scale column  

---

## 8. Environment, Dependencies, Data

- **Dependencies:** None  
- **Services:** WUT compose  
- **Migrations:** None  
- **Lab data:** Yellow portfolio, 17 books; control DNA 330 (OWD/OWDC) / 340 (static)  

---

## 9. Risks & Technical Debt

- Default AM/M knobs risk “false safety” (looks configured, never moves)  
- Kelly on OWDC can destroy good base economics  
- Negative cash on OWD cells confuses equity readouts  

---

## 10. Open Questions

- **AM/M thresholds** for TF: what equity/window actually steps on Yellow?  
- **Kelly policy:** host allowlist vs global toggle?  

---

## 11. Handoff & Resume Notes

- **Where I left off:** Findings analysis delivered to operator; wrap  
- **Next concrete step:** AM/M forced-step smoke; optional OWDC-none paper candidate path  
- **Files to read first:**  
  1. This report §5–6  
  2. `ecosystem/docs/analysis/2026-07-31-risk-scale-meta-layer.md`  
  3. PBR 353 (OWDC none) vs 356 (OWDC Kelly)  

---

## 12. Stakeholder Communications

- _None._  

---

## 13. Tools & Workflow Notes

- **Skills used:** wrap, session-report, operator-prose  
- **What worked well:** operator-run matrix without agent monitoring  
- **Friction points:** wrap follow-up promotion step needs explicit operator shortcut  

---

## 14. Follow-up Actions

- [ ] AM/M forced-step smoke PBRs (tighter knobs) — owner: lab  
- [ ] File ADR: risk_scale ⊥ base geometry  
- [ ] Business analysis scorecard for 345–356 findings  
- [ ] Do not promote Kelly globally; document OWDC regression  
- [ ] Consider OWDC-none as Yellow paper candidate (ops process)  

---

## 15. Appendix — Scorecard snapshot

| Base | Scale | PBR | Ret% | MaxDD% | Sharpe | Trades |
|------|-------|-----|------|--------|--------|--------|
| OWD | none/AM/M | 345–347 | 142.7 | 49.0 | 0.56 | 237 |
| OWD | kelly | 348 | 151.7 | 44.6 | 0.57 | 221 |
| static | none/AM/M | 349–351 | −0.8 | 40.9 | 0.12 | 178 |
| static | kelly | 352 | 35.1 | 39.9 | 0.30 | 123 |
| OWDC | none/AM/M | 353–355 | 176.1 | 39.0 | 0.64 | 319 |
| OWDC | kelly | 356 | 10.3 | 53.4 | 0.20 | 205 |

AM/M identical to none; end `n_steps=0`.  
