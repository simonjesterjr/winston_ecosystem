# Session Report — Portfolio Overlap Pipeline (Red/Blue + DM Batch + Blue Vet)

**Date:** 2026-07-06
**Time:** ~14:00–20:20 MDT (multi-step session)
**Duration:** ~6h (with long-running vet/DM batch wall time)
**Project:** Sawtooth Winston ecosystem
**Working directory:** `/home/johnkoisch/Documents/com/sawtooth`
**Branch:** `main` (ecosystem, winston_unit_test, data_manager — each repo)
**Model:** Grok
**Operator:** johnkoisch

---

## 1. Goal & Outcome

**Stated goal:** Correct portfolio-building rules (one seed per portfolio, ≤25% bilateral overlap), paginate WUT Data Sets UI, expand historical data via DM random acquisition, rebuild Portfolio Red and Blue, then vet Portfolio Blue.

**Outcome:** Delivered — all queued steps complete; Blue vet results are poor (see §5).

**One-line summary:** Red and Blue rebuilt under seed exclusivity and overlap controls; DM acquired 300 more symbols; Blue trend vet finished and exported, but all six strategies lost heavily on current membership.

---

## 2. Work Completed

- **`PortfolioOverlapPolicy` + `PortfolioRegistry`** — seed exclusivity, bilateral 25% cap, effective membership (strip alien seeds from peers), `portfolio_configs/registry.json`
- **Data Sets pagination** — 15 markets/page in WUT (`DataSetsController`, helper, index view)
- **Plan** — `ecosystem/plans/portfolio-overlap-rebuild.md` with phase status
- **Portfolio Red rebuilt** — AMAT seed, 9 markets, 0% overlap vs Blue, strong diversification
- **Portfolio Blue rebuilt** — TSMC seed, 11 markets, 0% overlap vs Red, strong diversification
- **DM random batch** — 300 symbols acquired (0 failures); suitable pool 15→18; parquet dirs ~331→630
- **Portfolio Blue vetting** — 6 entry strategies × VolatilityExit, winner exported to `portfolio-blue.json`
- **Export bug fixes** — `always_in` → `always_in_market`; pyramid fields from market config

---

## 3. Code Delivered

### Files changed

| File | Change | Notes |
|------|--------|-------|
| `winston_unit_test/app/services/portfolio_overlap_policy.rb` | added | Seed/overlap enforcement |
| `winston_unit_test/app/services/portfolio_registry.rb` | added | `registry.json` tracking |
| `winston_unit_test/app/services/portfolio_correlation_builder.rb` | modified | Peer filtering in greedy build |
| `winston_unit_test/lib/tasks/portfolio_correlation.rake` | modified | `PEERS=` env, registry register |
| `winston_unit_test/app/controllers/data_sets_controller.rb` | modified | 15/page pagination |
| `winston_unit_test/app/helpers/data_sets_helper.rb` | modified | Pagination link params |
| `winston_unit_test/app/views/data_sets/index.html.erb` | modified | Page controls |
| `winston_unit_test/app/services/portfolio_trend_vetter.rb` | modified | Export attribute fixes |
| `winston_unit_test/lib/tasks/portfolio_configs.rake` | modified | `always_in_market` fix |
| `winston_unit_test/spec/services/portfolio_overlap_policy_spec.rb` | added | Overlap policy specs |
| `data_manager/**` (symbol registry) | added/modified | Registry, suitability, acquire rake |
| `ecosystem/plans/portfolio-overlap-rebuild.md` | added/modified | Active plan + status |

### Artifacts (bind-mounted, not in git)

| Path | Notes |
|------|-------|
| `portfolio_configs/portfolio-red-sidecar.json` | Red membership |
| `portfolio_configs/portfolio-blue-sidecar.json` | Blue membership |
| `portfolio_configs/registry.json` | Finalized portfolios |
| `portfolio_configs/portfolio-blue.json` | Vetted Wv2 export (run 23) |
| `portfolio_configs/portfolio-blue-vet.log` | Vet log |

### Commits

- _Pending at wrap time — see §11_

### Branch / PR state at sign-off

- **ecosystem:** `main` — dirty (plan + session report)
- **winston_unit_test:** `main` — dirty; **behind origin/main by 4**
- **data_manager:** `main` — dirty (symbol registry uncommitted)
- Pushed: no
- PR: not opened

---

## 4. Decisions Made

### Decision 1: Effective membership for overlap math
- **Choice:** Strip alien seeds from peer portfolios before computing overlap fractions
- **Why:** Stale peer data (e.g. Red holding TSMC) blocked all diversifier picks
- **Alternatives considered:** Rebuild peer first; hard-fail on peer seed violations
- **Reversibility:** easy
- **Promote to ADR?** no — documented in plan

### Decision 2: Expanded candidate pool beyond DM-suitable-only
- **Choice:** Use WUT markets with `DmCoverage` ≥1000 bars when suitable pool too small
- **Why:** 15 suitable symbols capped Blue at 8 markets under overlap rules
- **Alternatives considered:** Wait for more DM batches only
- **Reversibility:** easy — rebuild with stricter pool later
- **Promote to ADR?** no

### Decision 3: DM batch via one-off `podman run`
- **Choice:** Run `acquire_random_batch` on latest image, not compose `data_manager` service
- **Why:** Running `data_manager` container still on pre-registry image; dependents block recreate
- **Reversibility:** easy — recreate service when convenient
- **Promote to ADR?** no

---

## 5. Insights Surfaced

- **Blue vet is economically meaningless on current membership** — all six entry strategies returned roughly -98% to -121% over 5yr; winner `SwingBreakout5DayStrategy` still -98.3% return, 100% max drawdown
- **Random ETF acquisition has low suitable yield** — 300 acquired → 3 new suitable (ACES, FPA, SOXQ); most fail Winston suitability (ATR/history)
- **Long WUT jobs must use `podman exec -d`** — `compose exec` session timeouts kill multi-hour vet runs
- **Export path had latent bugs** — `PortfolioTrendVetter` and `portfolio_configs.rake` referenced `always_in` and `pyramid_atr_multiplier` on wrong models

---

## 6. Issues & Tickets

### Resolved this session
- Portfolio seed exclusivity and overlap violations on Red/Blue — rebuilt under policy
- Data Sets UI unpaginated — 15/page added
- Blue vet export crash — attribute fixes applied; `portfolio-blue.json` written

### Deferred
- **Recreate compose `data_manager` on latest image** — See: `docs/tickets/2026-07-07-recreate-data-manager-compose-container.md`
- **Portfolio Red vetting** — See: `docs/tickets/2026-07-07-vet-portfolio-red-trend.md` (blocked by strategy evaluation framework)
- **Blue membership / strategy viability** — See: `docs/tickets/2026-07-07-revisit-portfolio-blue-membership-strategy.md`
- **Portfolio Orange (GLTR) and White (CPER)** — See: `docs/tickets/2026-07-07-build-portfolio-orange-white.md`
- **Portfolio trading-strategy evaluation framework (P0)** — See: `docs/tickets/2026-07-07-portfolio-trading-strategy-evaluation-framework.md`; plan task #5 in `plans/portfolio-overlap-rebuild.md.tasks.json`
- **Wv2 import / paper trading** — blocked until strategy framework; live gaps still deferred
- **DM↔WUT registry metadata sync** — `docs/tickets/2026-07-06-dm-wut-registry-metadata-sync-followups.md`

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| `PortfolioOverlapPolicy` specs | `rspec spec/services/portfolio_overlap_policy_spec.rb` in WUT container | ✅ 5 examples |
| Red rebuild | DB + sidecar + registry | ✅ seed OK, 0% overlap vs Blue |
| Blue rebuild | DB + sidecar + registry | ✅ seed OK, 0% overlap vs Red |
| DM batch | `acquire_random_batch[300]` | ✅ 300 ok, 0 failed |
| Blue vet | Opt 7 completed 6/6; run 23 completed | ✅ exported |
| Blue vet economics | Result metrics | ⚠️ all strategies large losses |

**Test command(s):**
```bash
./bin/compose exec -T winston_unit_test bundle exec rspec spec/services/portfolio_overlap_policy_spec.rb
```

---

## 8. Environment, Dependencies, Data

- **Dependencies:** None new
- **Services:** compose stack (WUT, DM, postgres, redis); `data_manager` image rebuilt (`localhost/sawtooth_data_manager:latest`) but running container stale
- **Migrations:** `symbol_registry_entries` exists in DM postgres (from prior session)
- **Data:** DM parquet volume `sawtooth_sawtooth_dm_data` — ~630 market dirs; registry 604 acquired, 18 suitable

---

## 9. Risks & Technical Debt

- **Blue (and likely Red) not trend-viable** on current diversified membership with standard breakout strategies
- **Running `data_manager` container out of sync with built image** — rake tasks via compose exec will fail for symbol registry
- **WUT `main` behind origin by 4** — pull/rebase before push
- **portfolio_configs JSON not versioned** — sidecars/registry/export live only on bind mount

---

## 10. Open Questions

- **Should Blue membership be revised** given -98% vet result, or should strategy parameters/risk be tuned first? — needs answer from: operator; blocks: Wv2 import
- **Is Winston suitability too strict** for random batch yield (3/300 new suitable)? — needs answer from: domain review

---

## 11. Handoff & Resume Notes

- **Where I left off:** `/wrap` — session report; commits pending
- **Next concrete step:** Decide whether to vet Red, revise Blue membership, or build Orange/White; recreate `data_manager` container on latest image
- **Files to read first:**
  1. `ecosystem/plans/portfolio-overlap-rebuild.md`
  2. `portfolio_configs/portfolio-blue.json`
  3. `portfolio_configs/registry.json`
  4. `winston_unit_test/app/services/portfolio_overlap_policy.rb`

### Final portfolio state

**Portfolio Red (id=6):** AMAT, CDE, MSFT, MSOS, PHYMF, ROKU, URA, VXX, XLV (9)

**Portfolio Blue (id=7):** AAL, AMZN, GLD, GOOGL, JNJ, PG, RXT, TSLA, TSMC, WMT, XLE (11)

**Blue vet winner:** `SwingBreakout5DayStrategy` + `VolatilityExitStrategy` (run 23, return -98.3%)

---

## 12. Stakeholder Communications

_None._

---

## 13. Tools & Workflow Notes

- **Skills used:** session-report, wrap
- **What worked well:** Detached `podman exec -d` for multi-hour vet; overlap policy with effective membership; polling optimization progress via DB
- **Friction points:** `compose exec` timeouts killing long jobs; DM service image drift; export bugs surfaced only at end of vet
- **Subagent usage:** none

---

## 14. Follow-up Actions

- [x] Filed tickets + plan tasks (2026-07-07) — see `docs/tickets/2026-07-07-*.md`, `plans/portfolio-overlap-rebuild.md.tasks.json`
- [ ] Recreate `data_manager` compose container — ticket `2026-07-07-recreate-data-manager-compose-container.md`
- [ ] **P0:** Portfolio trading-strategy evaluation framework — ticket `2026-07-07-portfolio-trading-strategy-evaluation-framework.md`
- [ ] Vet Portfolio Red — ticket `2026-07-07-vet-portfolio-red-trend.md` (after #5)
- [ ] Revisit Blue membership/strategy — ticket `2026-07-07-revisit-portfolio-blue-membership-strategy.md`
- [ ] Build Orange + White — ticket `2026-07-07-build-portfolio-orange-white.md`
- [ ] Import to Wv2 — blocked until strategy framework + viability gates

---

## 15. Appendix

**DM batch command (worked):**
```bash
podman run --rm --network sawtooth_default \
  -v sawtooth_sawtooth_dm_data:/app/data \
  --env-file ecosystem/deployment/eodhd.env \
  -e RAILS_ENV=development \
  localhost/sawtooth_data_manager:latest \
  bin/rails dm:symbol_registry:acquire_random_batch[300]
```

**Blue vet detached start:**
```bash
podman exec -d winston_unit_test sh -c \
  'env PORTFOLIO="Portfolio Blue" EXPORT=/portfolio_configs/portfolio-blue.json \
   bin/rails portfolios:vet_trend >> /portfolio_configs/portfolio-blue-vet.log 2>&1'
```

**Export error fixed:**
```
NoMethodError: undefined method `always_in' for PortfolioBacktestRun
```