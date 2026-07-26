# Session Report — Strategy bake-off V1 + S4 Phase 2 tactics

**Date:** 2026-07-25 → 2026-07-26  
**Time:** ~session through 11:03 MDT wrap  
**Duration:** multi-block (lab design, operator-run PBRs, scoring)  
**Project:** sawtooth Winston ecosystem  
**Working directory:** `/home/johnkoisch/Documents/com/sawtooth`  
**Branch:** `winston_unit_test/main`, `ecosystem/main`  
**Model:** Grok 4.5  
**Operator:** johnkoisch  

---

## 1. Goal & Outcome

**Stated goal:** Understand Mint next-bar-open vs legacy hero Portfolio Backtest Runs (PBRs); run a cross-portfolio strategy bake-off; pick 2–3 Trading Strategies (TS); tune tactics (pyramid Average True Range (ATR), max/symbol, portfolio heat); assess Elephant risk sensitivity; design hybrid fill for ops.

**Outcome:** Delivered (lab science + scripts + freezes); hybrid fill designed but not implemented.

**One-line summary:** Under honest next-bar-open, S4 FastBO5 won the bake-off; S1 Elephant is a second family only at ~1% unit risk; Phase 2 froze pyr ATR 1.0, max/symbol 4, max portfolio lots 12; hybrid entry-next / pyramid same-day close ticketed for code + broker priority.

---

## 2. Work Completed

- Diagnosed Mint PBR 121 (legacy same-bar Elephant ~1367%) vs recent next-bar Maverick/Elephant paths (~350% / worse DD): multi-factor recipe + fill + exit stack, not one missing gate.
- Phase 1 bake-off B: 5 strategies × 11 portfolios = 55 PBRs; setup + scorecard scripts; scored → **S4 primary**, S1 optional second.
- Elephant risk 1% side panel (16 PBRs): half-ladder ≡ flat 1%; survivability improved; S4 still leads equal-risk head-to-head.
- Phase 2 step 1: S4 pyramid ATR 0.5/0.75/1.0 → freeze **1.0**.
- Phase 2 step 2: max/symbol 3/4/5 → freeze **4**.
- Phase 2 step 3: max portfolio lots 8/12/16 → freeze default **12** (non-monotonic; Orange likes 16).
- Operator goal framing: ~200% over ~7y ≈ ~19% Compound Annual Growth Rate (CAGR), not exceptional low-risk.
- Skill **operator-prose**: expand acronyms on first use in operator chat.
- Hybrid fill ticket: next-bar entry + same-day pyramid close; blocked on WUT code.

---

## 3. Code Delivered

### Files changed

#### winston_unit_test

| File | Change | Notes |
|------|--------|-------|
| `lib/scripts/strategy_bakeoff_v1_setup.rb` | added | 5 TS + 55 PBR setup |
| `lib/scripts/strategy_bakeoff_v1_scorecard.rb` | added | Core ranking scorecard |
| `lib/scripts/elephant_risk_1pct_setup.rb` | added | S1/S4 1% risk panel |
| `lib/scripts/elephant_risk_1pct_scorecard.rb` | added | vs bakeoff baseline |
| `lib/scripts/s4_phase2_pyr_atr_setup.rb` | added | step 1 |
| `lib/scripts/s4_phase2_pyr_atr_scorecard.rb` | added | step 1 |
| `lib/scripts/s4_phase2_max_symbol_setup.rb` | added | step 2 |
| `lib/scripts/s4_phase2_max_symbol_scorecard.rb` | added | step 2 |
| `lib/scripts/s4_phase2_max_port_setup.rb` | added | step 3 |
| `lib/scripts/s4_phase2_max_port_scorecard.rb` | added | step 3 |

#### ecosystem

| File | Change | Notes |
|------|--------|-------|
| `docs/tickets/2026-07-25-strategy-bakeoff-v1-phase1.md` | added/updated | master ticket + freezes |
| `docs/tickets/2026-07-26-hybrid-fill-entry-next-pyramid-same-day.md` | added | hybrid fill design |
| `docs/tickets/INDEX.md` | modified | index rows |
| `docs/analysis/2026-07-25-strategy-bakeoff-v1-*.md/json` | added | bake-off maps |
| `docs/analysis/2026-07-26-elephant-risk-1pct-pbr-map.md` | added | risk panel map |
| `docs/analysis/2026-07-26-s4-phase2-*-pbr-map.md` | added | steps 1–3 maps |
| `.grok/skills/operator-prose/SKILL.md` | added | acronym expansion skill |
| `docs/session-reports/2026-07-26-1103-strategy-bakeoff-phase2.md` | added | this report |

#### workspace root (not a git repo)

| File | Change | Notes |
|------|--------|-------|
| `AGENTS.md` | modified | register `operator-prose` |
| `.grok/skills/operator-prose/SKILL.md` | added | mirror of ecosystem skill |

### Runtime lab data (WUT DB, not in git)

| Experiment | PBR range | Result |
|------------|-----------|--------|
| `strategy_bakeoff_v1` | 198–252 | 55 completed; S4 wins Core |
| `elephant_risk_1pct_v1` | 253–268 | 16 completed; half≡flat; S1 calmer |
| `s4_phase2_pyr_atr_v1` | 269–280 | freeze pyr 1.0 |
| `s4_phase2_max_symbol_v1` | 281–292 | freeze max_sym 4 |
| `s4_phase2_max_port_v1` | 293–304 | freeze max_port 12 default |

### Commits

- `35d543f` (winston_unit_test) — feat(lab): bake-off and S4 Phase 2 setup/scorecard scripts  
- `7a270d1` (ecosystem) — docs: strategy bake-off Phase 1–2 results, tickets, operator-prose skill  

### Branch / PR state at sign-off

- Branch: `main` on both repos — commits local  
- Pushed: **failed** (DNS: could not resolve github.com) — operator must `git push origin main` in each repo when network is up  
- PR: not opened (direct main)  

**Monoliths touched:** `winston_unit_test` (scripts), `ecosystem` (docs/skills/report). Root `AGENTS.md` not in a git repo.

---

## 4. Decisions Made

### Decision 1: Phase 1 promote S4 FastBO5 (TS #48)
- **Choice:** Primary methodology under next_bar_open + OWD ladder A  
- **Why:** Only Core-positive median wealth/Sharpe/viable  
- **Alternatives:** Promote S3 on median Sharpe (rejected — return wipeout)  
- **Reversibility:** easy (lab recipe)  
- **Promote to ADR?** no  

### Decision 2: S1 Elephant second family only at ~1% unit risk
- **Choice:** Not co-champion at bakeoff 2%/ladder A  
- **Why:** Survivability recovered at 1%; equal-risk still trails S4  
- **Reversibility:** easy  
- **Promote to ADR?** no  

### Decision 3: Phase 2 freezes pyr ATR 1.0, max_sym 4, max_port 12
- **Choice:** Tactics pack for S4  
- **Why:** Panel medians; reject 0.5 pyr and max_sym 3; heat non-monotonic (reject 8, don’t force 16)  
- **Reversibility:** easy  
- **Promote to ADR?** optional later if ops default  

### Decision 4: Hybrid fill = design/ticket first, not fake PBRs
- **Choice:** Entry next_bar_open; pyramid same_day_close (B1); needs code  
- **Why:** Single fill flag today; same-day open would lookahead on close triggers  
- **Reversibility:** n/a  
- **Promote to ADR?** after lab if frozen  

### Decision 5: Operator prose skill
- **Choice:** Expand acronyms on first use in operator chat  
- **Why:** Operator request  
- **Reversibility:** easy  
- **Promote to ADR?** no  

---

## 5. Insights Surfaced

- Legacy Mint 121 (~49% CAGR / 24% DD same-bar) is not the honest next-open bar; S4 Mint ~19% CAGR / 43% DD.
- Exit stack (stop-dominated vs EMA structure exits) dominated early 121 vs Maverick confusion.
- OWD ladder levels are absolute % — changing only `risk_percentage` does not de-risk if ladder remains 2/3/4/6.
- half_ladder and flat 1% produced identical paths (level-1 1% dominates).
- max_port heat under next-bar-open is path selection, not free CAGR; Orange wants 16, Blue/Mango want 12.
- Exceptional returns **and** low risk not yet achieved; tactics freezes improve hygiene, not 121-shaped miracle.

---

## 6. Issues & Tickets

### Resolved this session
- Phase 1 bake-off scored and freezes recorded  
- Phase 2 steps 1–3 scored and freezes recorded  
- operator-prose skill added  

### Deferred
- Hybrid fill **implementation** + matrix PBRs — ticket `2026-07-26-hybrid-fill-entry-next-pyramid-same-day.md` (code not started)  
- Optional ladder mildness (step 3b) — not ticketed  
- Multi-level correlation heat — existing `2026-07-25-ts-portfolio-heat-unit-limits.md`  
- CAGR/Calmar in scorecard scripts — not ticketed  
- Ops transfer of S4 pack to Mint/Yellow/Blue / Wv2 — not ticketed  
- Root `AGENTS.md` / root `.grok` not in git (workspace root)  

### Already filed (session-related)
- `2026-07-25-strategy-bakeoff-v1-phase1.md`  
- `2026-07-26-hybrid-fill-entry-next-pyramid-same-day.md`  
- `2026-07-25-ts-portfolio-heat-unit-limits.md` (prior)  

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| Bake-off 55 PBRs | operator run + scorecard | ✅ completed |
| Elephant 1% panel | scorecard | ✅ completed |
| Phase 2 pyr/max_sym/max_port | scorecards | ✅ completed |
| Hybrid fill | design only | ❌ not implemented |
| rspec for new scripts | not added | ⚠️ N/A scripts |

**Test command(s):**  
`bin/compose exec -T winston_unit_test bin/rails runner lib/scripts/strategy_bakeoff_v1_scorecard.rb`  
`... elephant_risk_1pct_scorecard.rb`  
`... s4_phase2_pyr_atr_scorecard.rb`  
`... s4_phase2_max_symbol_scorecard.rb`  
`... s4_phase2_max_port_scorecard.rb`

---

## 8. Environment, Dependencies, Data

- **Dependencies:** None new  
- **Services:** local compose WUT for PBR execute  
- **Migrations:** None  

---

## 9. Risks & Technical Debt

- Scorecards are Rails runners only (no specs).  
- Large PBR result sets remain DB-local; experiment tags in `results_json`.  
- Half vs flat 1% identity unexplained at pyramid depth (may hide OWD/path quirk).  
- Workspace-root `AGENTS.md` change not versioned with monoliths.  

---

## 10. Open Questions

- **Implement hybrid fill next, or transfer S4@1.0/4/12 first?** — product; blocks ops path  
- **Per-portfolio max_port overrides (Orange 16)?** — ops policy; blocks nothing  
- **Target CAGR/DD bar for “exceptional”?** — product; blocks promotion criteria  

---

## 11. Handoff & Resume Notes

- **Where I left off:** Phase 2 step 3 max_port scored; map updated; freezes recorded; wrap  
- **Next concrete step:** Choose: hybrid fill code, optional ladder 3b, or promote S4 recipe to paper/transfer  
- **Files to read first:**  
  1. `ecosystem/docs/tickets/2026-07-25-strategy-bakeoff-v1-phase1.md`  
  2. `ecosystem/docs/analysis/2026-07-26-s4-phase2-max-port-pbr-map.md`  
  3. `ecosystem/docs/tickets/2026-07-26-hybrid-fill-entry-next-pyramid-same-day.md`  

**S4 working pack:** next_bar_open · OWD ladder A / 2% · pyr ATR **1.0** · max_sym **4** · max_port **12** · TS #48  

---

## 12. Stakeholder Communications

- _None required this wrap._ Operator already has CAGR framing: ~19%/yr on Mint S4 is good TF, not exceptional low-risk.

---

## 13. Tools & Workflow Notes

- **Skills used:** operator-prose, session-report, wrap  
- **What worked well:** pending PBR setup + operator-run + scorecard (token efficient)  
- **Friction points:** multi-repo git only under monoliths; root AGENTS unversioned  
- **Subagent usage:** none  

---

## 14. Follow-up Actions

- [ ] Implement hybrid fill cadence (entry next / pyramid same-day close) — see `docs/tickets/2026-07-26-hybrid-fill-entry-next-pyramid-same-day.md`  
- [ ] Run hybrid PBR matrix (S4 winners + Elephant pain books) after code  
- [x] Optional step 3b: milder OWD ladder — **ticketed** `docs/tickets/2026-07-26-s4-phase2-ladder-mildness.md`  
- [x] Multi-level heat evidence from max_port sweep — **updated** `docs/tickets/2026-07-25-ts-portfolio-heat-unit-limits.md`  
- [x] CAGR/Calmar scorecards — **ticketed** `docs/tickets/2026-07-26-bakeoff-scorecard-cagr-calmar.md`  
- [x] S4 recipe transfer Mint/Yellow/Blue — **ticketed** `docs/tickets/2026-07-26-s4-recipe-transfer-mint-yellow-blue.md`  
- [ ] Version root AGENTS / skill mirror policy if desired  

---

## 15. Appendix (optional)

### Phase 1 Core rank (bake-off)

| Key | Med Sharpe | Med return | Viable | Call |
|-----|------------|------------|--------|------|
| S4 | 0.52 | +79.5% | 3/6 | **Promote** |
| S3 | 0.40 | −101% | 1/6 | Reject (Sharpe trap) |
| S1 | 0.22 | −29% | 0/6 | Second only @1% risk |
| S2/S5 | low | deep loss | 0 | Reject |

### Mint honesty check

| Run | Approx CAGR | Max DD |
|-----|-------------|--------|
| S4 next_open | ~19% | ~43% |
| Elephant 121 same-bar | ~49% | ~24% |
