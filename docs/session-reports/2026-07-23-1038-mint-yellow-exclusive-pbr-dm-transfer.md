# Session Report — Mint/Yellow Exclusive Books, DM Lookback Fix, PBR121 Transfer

**Date:** 2026-07-22 → 2026-07-23  
**Time:** ~15:30 MDT (Jul 22) – ~10:38 MDT (Jul 23)  
**Duration:** ~19h wall (multi-block; includes overnight vets + next-day debugging)  
**Project:** sawtooth Winston ecosystem  
**Working directory:** `/home/johnkoisch/Documents/com/sawtooth`  
**Branch:** `winston_unit_test` main; `ecosystem` main; Wv2 runtime import only  
**Model:** Grok (xAI)  
**Operator:** johnkoisch  

---

## 1. Goal & Outcome

**Stated goal:** Add two non-correlated smoke-test portfolios (Mint &lt;11 markets, Yellow &gt;13), avoid duplicating active Wv2 books, verify EODHD/DM data, run TS testing, then move strong recipes to Wv2. Follow-on: exclusive books, fix PBR/transfer failures on Mint/Yellow + Elephant5+20.

**Outcome:** Partially delivered → core path delivered

**One-line summary:** Built exclusive Mint (VNQ, 10) and Yellow (EEM, 17); expanded DM/WUT universe; fixed DM-only PBR date-range + lookback bugs (0 trades); unblocked one_way_dynamic export; imported Mint+Elephant PBR121 → Wv2 OP#311.

---

## 2. Work Completed

- Mapped active Wv2 books; designed Mint (REIT/VNQ) and Yellow (EM/EEM) themes
- Enforced **zero market overlap** vs all color peers (not 25% cap) for exclusive smoke cohorts
- Expanded EODHD universe: random batch 300 + 169 varied liquid ETFs; WUT Markets 1416→1588; coverage≥1000 834→1003
- Rebuilt exclusive books (PCS Mint 91.2, Yellow 73.5); verified ∅ bilateral shared markets
- Overnight first-pass `vet_trend` completed (opts #47 Mint / #48 Yellow) — winners Breakout50DayNoHistory + VolatilityExit; exports incomplete until runner fixes
- Diagnosed and fixed **PortfolioBacktestRunner** DM SoT gaps (overlap window + entry lookback)
- Fixed PBR UI null `innerHTML` on status polling
- Unblocked transfer of WUT run 121 (Elephant5+20): missing `pyramid_risks` ladder on export
- Imported to Wv2: **OP#311** `Portfolio Mint · 3749c990` (paper, inactive, trade_ready)

---

## 3. Code Delivered

### Files changed

| File | Change | Notes |
|------|--------|-------|
| `winston_unit_test/app/services/portfolio_overlap_policy.rb` | modified | VNQ/EEM seeds; exclusive max_overlap=0 support |
| `winston_unit_test/app/services/portfolio_correlation_builder.rb` | modified | `max_overlap_fraction` plumb |
| `winston_unit_test/lib/tasks/portfolio_correlation.rake` | modified | `MAX_OVERLAP`, `EXCLUDE_TAKEN` |
| `winston_unit_test/lib/tasks/portfolio_cohort_build.rake` | modified | Mint/Yellow exclusive cohorts |
| `winston_unit_test/lib/scripts/mint_yellow_risk_transfer.rb` | added | risk/capacity transfer experiments (post-vet) |
| `winston_unit_test/app/services/portfolio_backtest_runner.rb` | modified | DM date range + lookback; preserve methodology keys in results_json |
| `winston_unit_test/app/services/portfolio_backtest_run_factory.rb` | modified | seed pyramid ladder from TS provenance |
| `winston_unit_test/app/services/one_way_dynamic_risk_validator.rb` | modified | fall back to TS full_config for ladder |
| `winston_unit_test/app/views/portfolio_backtest_runs/show.html.erb` | modified | null-guard status_updates |
| `winston_unit_test/app/views/portfolio_backtest_runs/new.html.erb` | modified | null-guard market_configs_container |
| `ecosystem/docs/session-reports/2026-07-23-1038-mint-yellow-exclusive-pbr-dm-transfer.md` | added | this report |
| `portfolio_configs/portfolio-mint*.json`, `portfolio-yellow*.json`, sidecars | runtime artifacts | bind-mount volume; not monolith git |

### Commits

- _Pending wrap commit on `winston_unit_test` + ecosystem report._

### Branch / PR state at sign-off

- **winston_unit_test:** `main` — dirty with session fixes (commit this wrap)
- **ecosystem:** `main` — session report to add
- **winston_v2:** dirty files present but **not from this session** (equity series / DAR renderers) — **do not commit as part of this wrap**
- **data_manager:** clean (runtime acquire only)

**Monoliths touched:** `winston_unit_test` (code); `ecosystem` (report); `data_manager` / `winston_v2` (runtime data/import only).

---

## 4. Decisions Made

### Decision 1: Exclusive books for Mint/Yellow
- **Choice:** 0% peer market overlap (`MAX_OVERLAP=0` + `EXCLUDE_TAKEN=1`)
- **Why:** Operator requirement for smoke populations; 25% cap was too loose (DBA/VXX/AFIF leaks)
- **Alternatives considered:** Keep 25% bilateral (legacy colors)
- **Reversibility:** easy (rebuild membership)
- **Promote to ADR?** No — smoke-expansion policy; optional note in overlap plan later

### Decision 2: Seeds VNQ + EEM
- **Choice:** Mint=REIT (VNQ), Yellow=EM multi-asset (EEM)
- **Why:** Liquid, quality-pass, themes underrepresented vs Red/Blue/Orange/White/Green/Pink/Mango/Rust
- **Reversibility:** easy
- **Promote to ADR?** No

### Decision 3: DM lookback/date-range in PortfolioBacktestRunner
- **Choice:** Prefer DmCoverage/parquet over empty `activities` for DM-only markets
- **Why:** Optimization context already DM-aware; runner was not — caused false “no overlap” and 0 trades
- **Reversibility:** easy
- **Promote to ADR?** No (implementation of existing DM SoT)

### Decision 4: Refuse silent one_way_dynamic export without ladder
- **Choice:** Keep validator hard-fail; seed ladder from TS + preserve on run
- **Why:** Silent flat-risk handoff is dangerous (existing issue/ADR-008 spirit)
- **Reversibility:** n/a (correct)
- **Promote to ADR?** No

---

## 5. Insights Surfaced

- **Activities table is empty for pure DM books** — any runner path still on `market.activities` silently no-ops (lookback) or fails (overlap).
- **First-pass vet can “complete” screening** while validation export fails if runner still broken — opt #47/#48 winners existed without durable export JSON initially.
- **MCP transfer “hang”** was often a **fast 422/exception** (missing pyramid_risks) poorly surfaced, plus WUT puma under load (~2GB RSS) causing HTTP timeouts on `/internal/portfolio_config`.
- **PBR results_json progress writes** can drop methodology keys unless explicitly preserved.
- DM suitability flag is strict (~136 suitable); WUT quality + bar count is the practical build universe.

---

## 6. Issues & Tickets

### Resolved this session
- Exclusive Mint/Yellow membership (0 peer overlap)
- PBR “No overlapping date range” on DM-only portfolios
- PBR 0 trades on Mint/Yellow (empty lookback)
- Elephant5+20 transfer refuse (missing pyramid_risks)
- Mint PBR121 → Wv2 OP#311 import

### Deferred
- Yellow + Elephant5+20 full PBR + transfer — See: [`docs/tickets/2026-07-23-yellow-elephant-pbr-and-wv2-transfer.md`](../tickets/2026-07-23-yellow-elephant-pbr-and-wv2-transfer.md)
- Re-export opt#47/#48 vet winners — See: [`docs/tickets/2026-07-23-reexport-mint-yellow-vet-winners.md`](../tickets/2026-07-23-reexport-mint-yellow-vet-winners.md)
- Risk-transfer matrix script — See: [`docs/tickets/2026-07-23-mint-yellow-risk-transfer-matrix.md`](../tickets/2026-07-23-mint-yellow-risk-transfer-matrix.md)
- WUT puma / large `results_json` — See: [`docs/tickets/2026-07-23-wut-puma-large-pbr-results-json.md`](../tickets/2026-07-23-wut-puma-large-pbr-results-json.md)
- MCP transfer + activate flow smooth — See: [`docs/tickets/2026-07-23-mcp-transfer-activate-flow-smooth.md`](../tickets/2026-07-23-mcp-transfer-activate-flow-smooth.md)
- Activate OP#311 smoke — See: [`docs/tickets/2026-07-23-activate-wv2-mint-op311-smoke.md`](../tickets/2026-07-23-activate-wv2-mint-op311-smoke.md)
- Specs DM lookback + exclusive overlap — See: [`docs/tickets/2026-07-23-dm-lookback-exclusive-overlap-specs.md`](../tickets/2026-07-23-dm-lookback-exclusive-overlap-specs.md)
- Unrelated dirty tree on **winston_v2** (equity series / DAR) — not this session

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| Exclusive membership | bilateral shared markets check | ✅ ∅ vs peers + Mint∩Yellow |
| Mint PCS | corr_v2 sidecar | ✅ 91.2 max\|r\| 0.17 |
| Yellow PCS | corr_v2 sidecar | ✅ 73.5 max\|r\| 0.50 |
| DM lookback fix | PBR121 Mint+Elephant | ✅ +1366.8% ret, 23.6% DD, 1357 trades, Sharpe 1.42 |
| Export run 121 | PortfolioConfigExporter | ✅ after ladder patch |
| Wv2 import | `wv2:portfolios:import` | ✅ OP#311 paper inactive trade_ready |
| MCP internal HTTP | curl /internal/portfolio_config | ⚠️ timeouts when puma loaded |
| Yellow Elephant transfer | not completed | ⏳ deferred |

**Test command(s):**
```bash
# overlap / lookback proven via PBR 121
bin/compose exec -T winston_unit_test bin/rails runner 'puts PortfolioBacktestRun.find(121).slice(:total_return,:max_drawdown,:total_trades)'

# import already done; activate when ready:
bin/compose exec -T winston_v2 bin/rails wv2:portfolios:activate[311]
```

---

## 8. Environment, Dependencies, Data

- **Dependencies:** None changed in gemfiles  
- **Services:** compose stack (DM, WUT, Wv2, Redis, Postgres) already up  
- **Migrations:** None  
- **Data:** DM acquired ~2704; varied ETF batch + random 300; WUT Markets ~1588  
- **Runtime artifacts:** `portfolio_configs/portfolio-mint*`, `portfolio-yellow*`, registry updates on volume  

---

## 9. Risks & Technical Debt

- Large multi-market PBR `results_json` (equity_history × days) stresses puma and MCP transfer timeouts  
- Factory attach / runner must stay in lockstep for one_way_dynamic ladders or handoff fails again  
- Exclusive cohorts not yet documented as standing doctrine next to 25% color-cohort rule  
- Specs not added for DM lookback / exclusive overlap env flags  

---

## 10. Open Questions

- **Activate OP#311 for multi-cohort smoke DAR?** — operator  
- **Yellow OP import now or after Elephant PBR on fixed runner?** — operator  
- **Should exclusive 0-overlap become default for all new color cohorts?** — product  

---

## 11. Handoff & Resume Notes

- **Where I left off:** Mint Elephant PBR121 fixed and imported as Wv2 **#311** (paper, inactive). Code fixes in WUT uncommitted pending wrap.  
- **Next concrete step:** Commit WUT fixes; optionally activate #311; run Yellow+Elephant PBR and transfer.  
- **Files to read first:**  
  1. `winston_unit_test/app/services/portfolio_backtest_runner.rb` (DM date range + lookback)  
  2. `winston_unit_test/app/services/portfolio_backtest_run_factory.rb` (ladder seed)  
  3. `winston_unit_test/app/services/one_way_dynamic_risk_validator.rb`  
  4. `portfolio_configs/portfolio-mint-elephant-pbr121.json`  

**Final exclusive books:**

- **Mint (10):** AMCR, APLD, ASTS, OIH, SHY, UNG, USO, VNQ, WEAT, XOP  
- **Yellow (17):** ABBV, AEP, AKAM, AMGN, AMLP, ANET, AXON, BNO, BTAL, CANE, EEM, IAU, IEF, PALL, REMX, SGOL, SOYB  

---

## 12. Stakeholder Communications

- _None formal._ Operator-facing: smoke cohort Mint landed in Wv2 as paper OP#311 with Elephant5+20 recipe.

---

## 13. Tools & Workflow Notes

- **Skills used:** wrap, session-report (this file)  
- **What worked well:** Reproduce transfer via direct WUT export + Wv2 import when MCP/HTTP flaky  
- **Friction points:** Overnight vet wall clock; puma timeouts; `results_json` size; activities vs DM dual path  
- **Subagent usage:** none  

---

## 14. Follow-up Actions

- [ ] Activate OP#311 — [`2026-07-23-activate-wv2-mint-op311-smoke.md`](../tickets/2026-07-23-activate-wv2-mint-op311-smoke.md)  
- [ ] Yellow Elephant PBR + transfer — [`2026-07-23-yellow-elephant-pbr-and-wv2-transfer.md`](../tickets/2026-07-23-yellow-elephant-pbr-and-wv2-transfer.md)  
- [ ] Re-export opt#47/#48 — [`2026-07-23-reexport-mint-yellow-vet-winners.md`](../tickets/2026-07-23-reexport-mint-yellow-vet-winners.md)  
- [ ] Risk-transfer matrix — [`2026-07-23-mint-yellow-risk-transfer-matrix.md`](../tickets/2026-07-23-mint-yellow-risk-transfer-matrix.md)  
- [ ] WUT puma / results_json — [`2026-07-23-wut-puma-large-pbr-results-json.md`](../tickets/2026-07-23-wut-puma-large-pbr-results-json.md)  
- [ ] Specs lookback + exclusive — [`2026-07-23-dm-lookback-exclusive-overlap-specs.md`](../tickets/2026-07-23-dm-lookback-exclusive-overlap-specs.md)  
- [ ] **MCP transfer + activate flow** — [`2026-07-23-mcp-transfer-activate-flow-smooth.md`](../tickets/2026-07-23-mcp-transfer-activate-flow-smooth.md)  
- [ ] Leave winston_v2 unrelated dirty tree alone or wrap separately — owner: operator  

---

## 15. Appendix

### Transfer failure (pre-fix)
```
OneWayDynamicRiskValidator::Error
TradingStrategyFingerprintCapture run #121: risk_evaluation_strategy is one_way_dynamic
but pyramid_risks ladder is missing.
```

### MCP log
```
wv2_transfer_portfolio_from_wut error in 165ms
```

### Successful import
```
Wv2: Import action=forked portfolio #311 "Portfolio Mint · 3749c990"
export_kind: trade_ready execution_mode: paper active: false
```
