# Session Report — Portfolio Overlap: Orange/White + Eval Gates + Red PBR

**Date:** 2026-07-08  
**Time:** ~15:25–17:44 MDT  
**Duration:** ~2h 20m  
**Project:** Sawtooth Winston ecosystem  
**Working directory:** `/home/johnkoisch/Documents/com/sawtooth`  
**Branch:** `main` (ecosystem, winston_unit_test)  
**Model:** Grok  
**Operator:** johnkoisch  

---

## 1. Goal & Outcome

**Stated goal:** Resume `ecosystem/plans/portfolio-overlap-rebuild.md` — Orange/White builds, evaluation framework, Red vet via PBR — after DM SoT closeout (“portfolio path green; scheduled jobs will not re-duplicate DM data”).

**Outcome:** Delivered membership for Orange + White; evaluation-framework gates/export_kind; Red labeled observation via PBR 25. Orange/White strategy vets not run.

**One-line summary:** Four seed portfolios now registered under overlap rules; trade-ready gates label Red/Blue as observation; suitable pool ≥50; next is Orange/White `vet_trend` and Blue membership revisit.

---

## 2. Work Completed

- **TradeReadyViabilityGates** — return ≥0%, max DD ≤50%, trades ≥20; wires into `PortfolioTrendVetter` export + `vet_trend` summary
- **export_kind** on portfolio JSON (`trade_ready` | `observation`) + `vetting.viability` block
- **Null-Sharpe ranking fallback** — `practical_sharpe_ratio` null sorts by `total_return`
- **RANKING_METRIC** env on `portfolios:vet_trend`
- Labeled existing **portfolio-red.json** / **portfolio-blue.json** as observation
- **DM random batches** ×3 → suitable **26 → 51**, acquired **1532**
- **Portfolio Orange** (GLTR, 15 markets) + **Portfolio White** (CPER, 20 markets) built, registry + sidecars
- Verified all bilateral overlaps ≤25% and seed exclusivity
- **Red PBR 25** re-confirmed (HTTP 200, completed metrics) on DM-green path
- **Perf fix** for greedy correlation builds (DmCoverage date bounds + process-level close cache)
- Plan/tasks/tickets updated for portfolio-overlap rebuild

---

## 3. Code Delivered

### Files changed

| File | Change | Notes |
|------|--------|-------|
| `winston_unit_test/app/services/trade_ready_viability_gates.rb` | added | Gate service |
| `winston_unit_test/spec/services/trade_ready_viability_gates_spec.rb` | added | Unit specs |
| `winston_unit_test/app/services/portfolio_trend_vetter.rb` | modified | export_kind + viability block |
| `winston_unit_test/app/services/portfolio_signal_optimizer.rb` | modified | null-Sharpe → total_return |
| `winston_unit_test/lib/tasks/portfolio_trend_vet.rake` | modified | RANKING_METRIC + gate summary |
| `winston_unit_test/spec/services/portfolio_signal_optimizer_spec.rb` | modified | fallback spec |
| `winston_unit_test/app/services/market_correlation_calculator.rb` | modified | date bounds + closes cache + faster align |
| `winston_unit_test/app/services/portfolio_correlation_builder.rb` | modified | clear closes cache per build |
| `ecosystem/plans/portfolio-overlap-rebuild.md` | modified | Phase status Orange/White + Phase 7 |
| `ecosystem/plans/portfolio-overlap-rebuild.md.tasks.json` | modified | tasks 1–4 done; task 6 vet pending |
| `ecosystem/docs/analysis/portfolio-trading-strategy-evaluation.md` | modified | implemented items |
| `ecosystem/docs/business-context/trade-ready-viability-gates.md` | modified | WUT implementation note |
| `ecosystem/docs/tickets/2026-07-07-portfolio-trading-strategy-evaluation-framework.md` | modified | ~90% progress |
| `ecosystem/docs/tickets/2026-07-07-vet-portfolio-red-trend.md` | modified | Done / PBR 25 results |
| `ecosystem/docs/tickets/2026-07-07-build-portfolio-orange-white.md` | modified | Membership done |
| `ecosystem/docs/tickets/2026-07-07-recreate-data-manager-compose-container.md` | modified | Done |
| `portfolio_configs/README.md` | modified | RANKING_METRIC + export_kind docs |
| `portfolio_configs/portfolio-red.json` | modified | observation + viability |
| `portfolio_configs/portfolio-blue.json` | modified | observation + viability |
| `portfolio_configs/portfolio-orange-sidecar.json` | added (ops) | Orange membership |
| `portfolio_configs/portfolio-white-sidecar.json` | added (ops) | White membership |
| `portfolio_configs/registry.json` | modified (ops) | four portfolios |

### Commits

- _Pending at wrap time_

### Branch / PR state at sign-off

- **ecosystem:** `main` — dirty (this session + pre-existing untracked tickets)
- **winston_unit_test:** `main` — dirty (session code)
- **data_manager:** clean (batches only; no code)
- Pushed: no
- PR: not opened

---

## 4. Decisions Made

### Decision 1: Observation vs trade-ready via gates on export
- **Choice:** Enforce placeholder gates; sub-breakeven or high-DD winners export as `observation`
- **Why:** Blue/Red economics must not look “Wv2-ready” without an explicit kind
- **Alternatives considered:** Soft docs only; block export entirely
- **Reversibility:** easy (tune thresholds in one service)
- **Promote to ADR?** no — domain rule already in business-context

### Decision 2: Build Orange/White on WUT coverage pool, not DM-suitable-only
- **Choice:** Candidates = DmCoverage bar_count ≥1000 (minus alien seeds), after suitable ≥50 gate
- **Why:** Suitable-only pool still too small for 12–20 market builds under overlap
- **Alternatives considered:** Wait for larger suitable-only pool
- **Reversibility:** easy (rebuild with different CANDIDATES)
- **Promote to ADR?** no

### Decision 3: Cache full close series by market_id for correlation greedy
- **Choice:** Process-level cache; slice by date range; DmCoverage for bounds
- **Why:** Per-step full parquet reload was multi-hour / OOM risk
- **Alternatives considered:** Kill and manual membership; smaller candidate sets only
- **Reversibility:** easy
- **Promote to ADR?** no

---

## 5. Insights Surfaced

- Red is **high return / high DD** (observation), not catastrophic like Blue (−98%)
- `MarketCorrelationCalculator.overlapping_date_range` was loading full history only to get first/last dates — primary build-time cost
- Caching by (market_id, start, end) still reloads every greedy step because range shrinks; cache by market_id only
- Random acquire batches yield low suitable hit-rate; three 300-batches needed to go 26→51 suitable
- Full stack briefly cycled mid-session (container name conflicts on recreate); recovered via compose up

---

## 6. Issues & Tickets

### Resolved this session
- Evaluation framework remaining export gates / null-Sharpe / RANKING_METRIC
- Orange + White membership under overlap rules
- Suitable pool ≥50 gate
- Red vet ticket status (observation via PBR 25)
- DM compose recreate ticket status (already operational)

### Deferred
- Orange + White `portfolios:vet_trend` (multi-hour) — plan task #6
- Blue membership/strategy revisit — existing ticket
- Framework residual: Blue post-mortem template
- Viability threshold tuning after more vets
- portfolio_configs ops artifacts not in any monolith git (bind-mount only)
- Pre-existing ecosystem dirty/untracked files outside this session (wrap skill, old tickets/reports)

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| TradeReadyViabilityGates | rspec | ✅ 4 examples |
| PortfolioTrendVetter FIRST_PASS / create | rspec | ✅ |
| Null-Sharpe fallback | rspec | ✅ |
| Red PBR 25 | rails runner + HTTP show | ✅ completed; page 200 |
| Orange/White overlaps | rails runner bilateral fractions | ✅ all ≤25% |
| Seed exclusivity | rails runner | ✅ |
| DM suitable count | `dm:symbol_registry:summary` | ✅ 51 |
| Orange/White vet | not run | ⚠️ pending |
| Full optimizer/vet CI | not run | ⚠️ |

**Test command(s):**

```bash
./bin/compose exec -T winston_unit_test bundle exec rspec \
  spec/services/trade_ready_viability_gates_spec.rb \
  spec/services/portfolio_trend_vetter_spec.rb \
  spec/services/portfolio_signal_optimizer_spec.rb -e "falls back"
```

---

## 8. Environment, Dependencies, Data

- **Dependencies:** None added
- **Services:** compose stack (DM, WUT, Wv2, redis, postgres); brief full restart mid-session
- **Migrations:** None
- **Data:** +900 symbols acquired via three random batches; suitable 51; registry four portfolios

---

## 9. Risks & Technical Debt

- Correlation greedy still ~15–25 min for large candidate sets (import + first full_history load)
- `PortfolioDiversificationAdvisor` labeled White mean \|r\|≈0.105 as “Weak Diversification” (likely scale/label confusion)
- Observation portfolios can still be imported to Wv2 without hard importer block on `export_kind`
- Red 64% DD may be strategy-ok for lab but fails current placeholder gates

---

## 10. Open Questions

- **Should Wv2 importer reject `export_kind: trade_ready` failures?** — needs product rule; blocks unsafe promotion
- **Retune DD gate after Orange/White vets?** — needs more data; blocks gate finalization
- **White “Weak Diversification” label** — is advisor inverted for low mean \|r\|?

---

## 11. Handoff & Resume Notes

- **Where I left off:** Four portfolios registered; eval gates live; Orange/White unvetted
- **Next concrete step:** Detached `portfolios:vet_trend` for Portfolio Orange then White (or Blue revisit)
- **Files to read first:**
  1. `ecosystem/plans/portfolio-overlap-rebuild.md`
  2. `ecosystem/plans/portfolio-overlap-rebuild.md.tasks.json`
  3. `winston_unit_test/app/services/trade_ready_viability_gates.rb`
  4. `portfolio_configs/registry.json`

```bash
# Orange vet (detached)
podman exec -d winston_unit_test sh -c \
  'env PORTFOLIO="Portfolio Orange" EXPORT=/portfolio_configs/portfolio-orange.json \
   bin/rails portfolios:vet_trend >> /portfolio_configs/portfolio-orange-vet.log 2>&1'
```

---

## 12. Stakeholder Communications

- _None required beyond lab handoff._ Red remains paper/observation only despite high headline return (drawdown).

---

## 13. Tools & Workflow Notes

- **Skills used:** wrap, session-report (this wrap)
- **What worked well:** compose-path DM batches; gate service small and testable; registry for peers
- **Friction points:** long correlation builds; container restart name conflicts; stdout buffering hid progress until end
- **Subagent usage:** none

---

## 14. Follow-up Actions

- [ ] Run `portfolios:vet_trend` for Portfolio Orange — ticket: [`2026-07-08-vet-portfolio-orange-trend.md`](../tickets/2026-07-08-vet-portfolio-orange-trend.md)
- [ ] Run `portfolios:vet_trend` for Portfolio White — ticket: [`2026-07-08-vet-portfolio-white-trend.md`](../tickets/2026-07-08-vet-portfolio-white-trend.md)
- [ ] Blue membership/strategy revisit — already tracked: [`2026-07-07-revisit-portfolio-blue-membership-strategy.md`](../tickets/2026-07-07-revisit-portfolio-blue-membership-strategy.md)
- [ ] Wv2 importer honor `export_kind` — ticket: [`2026-07-08-wv2-importer-honor-export-kind.md`](../tickets/2026-07-08-wv2-importer-honor-export-kind.md)
- [ ] Fix diversification rating labels for low mean \|r\| — ticket: [`2026-07-08-diversification-advisor-label-scale.md`](../tickets/2026-07-08-diversification-advisor-label-scale.md)
- [ ] Close-only parquet load for correlation — ticket: [`2026-07-08-correlation-close-only-parquet-load.md`](../tickets/2026-07-08-correlation-close-only-parquet-load.md)

---

## 15. Appendix (optional)

### Membership snapshot

| Portfolio | Seed | N | mean \|r\| |
|-----------|------|---|------------|
| Red | AMAT | 9 | ~0.21 |
| Blue | TSMC | 11 | ~0.12 |
| Orange | GLTR | 15 | 0.171 |
| White | CPER | 20 | 0.105 |

### Red PBR 25

- Winner: Breakout50DayNoHistoryStrategy + VolatilityExitStrategy  
- Return +636.3%, max DD 64.0%, trades 1051, Sharpe null → `export_kind: observation`
