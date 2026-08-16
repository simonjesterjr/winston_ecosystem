# Session Report — PCS copies and books-keyed heat

**Date:** 2026-08-16
**Time:** ~13:35–14:15 MDT
**Duration:** ~40m
**Project:** sawtooth Winston ecosystem (WUT + Wv2 + ecosystem)
**Working directory:** `/home/johnkoisch/Documents/com/sawtooth`
**Branch:** `main` on `ecosystem`, `winston_unit_test`, `winston_v2` (started from each repo’s `origin/main`)
**Model:** Grok 4.6
**Operator:** johnkoisch

---

## 1. Goal & Outcome

**Stated goal:** Explain Operational Portfolio (OP) **#797** Turtle geometry (ladder, N, pyramid), then persist heat + the Portfolio Backtest Run (PBR) pair map so Level 2 / Level 3 (L2/L3) bind on Yellow-class books. Keep Portfolio Correlation Score (PCS) computed in Winston Unit Test (WUT). Copy every evaluation into Winston v2 (Wv2). Evaluate heat from those copies regardless of Trading Strategy (TS), OP id, or fingerprint.

**Outcome:** Delivered.

**One-line summary:** WUT still owns PCS; each evaluation now carries a pairwise map and is copied into Wv2 keyed by Books. Desk heat uses that copy, so Mint sits at 12 lots and Yellow can drag via L3.

---

## 2. Work Completed

- Clarified #797 chassis for the operator: static 1% (no One-Way Dynamic ladder), N = Average True Range 17 (`atr_17`), stop 2×ATR, pyramid **0.5×ATR**, max 4 lots / market
- Clarified heat doctrine vs what was wired: L4 / `max_positions_per_portfolio` = **12**; L2/L3 were off because TS #266 had no heat hash or pair map
- Persisted compact pairwise maps on WUT `portfolio_correlation_snapshots.pairs`
- Push each WUT evaluation to Wv2 (`Wv2CorrelationPublisher` after daily score and PBR attach)
- Wv2 durable copy table keyed by `books_key` (sorted symbols), not OP / TS / fingerprint
- Daily Analysis runner pulls WUT latest + history before tasking; DAR enricher prefers local copies
- Heat resolver: TS heat if present, else Turtle L2=6 / L3=10 / L1+L4 from OP lot columns when a pair copy exists
- Turtle import stamps `heat: turtle` (also name/chassis detect) and ingests handoff `correlation_snapshot`
- Auditor dump now prints `pyr_atr`, L1–L4, and the PCS copy
- Live score + push: 11 registry books copied; #797 and all other Mint OPs share PCS **91.31** / 45 pairs; #798 Yellow PCS **73.04** / max \|ρ\| **0.505** / 136 pairs

---

## 3. Code Delivered

### Files changed

#### `winston_unit_test`

| File | Change | Notes |
|------|--------|-------|
| `app/services/correlation_pair_map.rb` | added | Compact `A\|B` pair keys |
| `app/services/wv2_client.rb` | added | POST to Wv2 internal API |
| `app/services/wv2_correlation_publisher.rb` | added | Best-effort push; never rolls back WUT |
| `app/services/portfolio_correlation_scorer.rb` | modified | `ScoreResult.pairs` from matrix |
| `app/models/portfolio_correlation_snapshot.rb` | modified | Persist + export pairs |
| `app/models/portfolio_backtest_run.rb` | modified | Handoff snapshot includes pairs |
| `app/services/portfolio_backtest_correlation_attacher.rb` | modified | Publish after attach |
| `app/services/portfolio_correlation_daily_scorer.rb` | modified | Publish after daily score |
| `app/services/portfolio_config_exporter.rb` | modified | Turtle heat default + pairs on snapshot |
| `app/controllers/internal_controller.rb` | modified | Serialize pairs on latest/history |
| `lib/tasks/portfolio_correlation.rake` | modified | `correlation_publish_wv2` |
| `db/migrate/20260816120000_add_pairs_to_portfolio_correlation_snapshots.rb` | added | `pairs jsonb` |
| `db/schema.rb` | modified | pairs column |
| `spec/services/correlation_pair_map_spec.rb` | added | |
| `spec/services/wv2_correlation_publisher_spec.rb` | added | |
| `spec/services/portfolio_backtest_correlation_attacher_spec.rb` | modified | Expect pairs |
| `spec/services/portfolio_correlation_daily_scorer_spec.rb` | modified | Expect pairs |

#### `winston_v2`

| File | Change | Notes |
|------|--------|-------|
| `app/models/portfolio_correlation_snapshot.rb` | added | Books-keyed copy; no `portfolio_id` |
| `app/services/correlation_pair_map.rb` | added | Same compact key contract |
| `app/services/operations/correlation_snapshot_ingest.rb` | added | Upsert by books_key + date + version |
| `app/services/operations/correlation_snapshot_sync.rb` | added | Pull latest + history from WUT |
| `app/services/operations/portfolio_heat.rb` | added | Resolve heat + pairs independent of TS |
| `app/services/operations/desk_heat_gate.rb` | modified | Use `PortfolioHeat` |
| `app/services/portfolio_heat_cluster_resolver.rb` | modified | Pairs from PCS copy first |
| `app/services/operations/portfolio_config_importer.rb` | modified | Turtle heat + ingest handoff snapshot |
| `app/services/operations/daily_analysis_runner.rb` | modified | Pull PCS copies before tasking |
| `app/services/portfolio_correlation_report_enricher.rb` | modified | Prefer local history; ingest on WUT fallback |
| `app/services/operations/portfolio_trading_strategy_auditor.rb` | modified | Print pyr_atr, heat, PCS copy |
| `app/controllers/internal_controller.rb` | modified | `POST /internal/correlation_snapshots` |
| `config/routes.rb` | modified | Ingest route |
| `lib/tasks/wv2.rake` | modified | `wv2:sync_correlation` |
| `db/migrate/20260816120000_create_portfolio_correlation_snapshots.rb` | added | |
| `db/schema.rb` | modified | New table |
| `spec/services/operations/correlation_snapshot_ingest_spec.rb` | added | |
| `spec/services/operations/portfolio_heat_spec.rb` | added | Two Mint OPs share pairs |
| `spec/services/operations/task_generator_heat_spec.rb` | modified | Heat from PCS copy, no TS hash |
| `spec/services/operations/portfolio_config_importer_spec.rb` | modified | Turtle heat + snapshot ingest |

#### `ecosystem`

| File | Change | Notes |
|------|--------|-------|
| `CONTEXT.md` | modified | PCS / snapshot: Wv2 copy, Books identity |
| `docs/adr/ADR-007-portfolio-correlation-score-sot.md` | modified | Durable copy + heat reads pairs, not PCS 0–100 |
| `docs/session-reports/2026-08-16-1411-pcs-copy-and-books-heat.md` | added | This report |

#### Shared volume (not a git repo)

| File | Change | Notes |
|------|--------|-------|
| `portfolio_configs/portfolio-mint-turtle-s2-ts77.json` | modified | `"heat": { "mode": "turtle" }` |
| `portfolio_configs/portfolio-yellow-turtle-s1-ts75.json` | modified | same |

### Commits

- `1aee4aa` — feat(pcs): persist pair maps and push every evaluation to Wv2 (WUT)
- `2d0ff72` — feat(ops): copy WUT PCS evaluations and heat by books (Wv2)
- ecosystem SHA filled after this docs commit

### Branch / PR state at sign-off

- Branch: `main` on all three
- Pushed: yes (this wrap)
- PR: not opened (direct `main` convention)

---

## 4. Decisions Made

### Decision 1: PCS stays in WUT; Wv2 stores copies
- **Choice:** WUT computes; every evaluation is copied (push + Daily Analysis pull).
- **Why:** ADR-007 forbids a second formula. Operator asked for local copies so heat and DAR do not depend on a live WUT GET at task time.
- **Alternatives considered:** Thin cache only; Wv2 recompute; fetch-only at DAR.
- **Reversibility:** easy (drop Wv2 table; WUT still SoT).
- **Promote to ADR?** Updated ADR-007 in place (addendum, not a new ADR).

### Decision 2: Copy identity is Books, not OP / TS / fingerprint
- **Choice:** Unique key `(books_key, as_of_date, methodology_version)`. `seed_name` is display / fallback lookup.
- **Why:** Operator: evaluate correctly regardless of TS, portfolio, or fingerprint. All Mint OPs share one series.
- **Alternatives considered:** Key by seed only; key by fingerprint; store pairs on TS.parameters.
- **Reversibility:** easy (lookup helpers).
- **Promote to ADR?** Covered in the ADR-007 addendum.

### Decision 3: Heat uses pairwise map, not the 0–100 PCS
- **Choice:** L2/L3 from copied \|ρ\|. L1/L4 from OP lot columns (or TS heat if present). Auto-enable heat when a pair copy exists.
- **Why:** High PCS means L2/L3 idle → you reach 12. Yellow max \|ρ\| 0.505 binds L3 without rewriting L4.
- **Alternatives considered:** Scale L4 from PCS; require TS heat hash; freeze only the promoting-PBR vintage.
- **Reversibility:** medium (desk tasking now depends on copies).
- **Promote to ADR?** No — heat ticket / BA already define L1–L4; this is the ops wiring.

### Decision 4: Latest copied pairs for ops heat
- **Choice:** Desk uses the latest books-keyed copy, not a frozen handoff-only vintage.
- **Why:** “Copy every evaluation” only matters for heat if the latest map is what binds. Books mutation still requires successor (ADR-006).
- **Alternatives considered:** Freeze import vintage forever; recompute every bar.
- **Reversibility:** easy (resolver can pin a date).
- **Promote to ADR?** No.

---

## 5. Insights Surfaced

- The strategy audit dump omitted `pyramid_atr_multiplier` (0.5) and printed a PBR80 One-Way Dynamic footer that does not apply to Turtle S2 — that is why 797 looked like it had no pyramid geometry
- Stored `risk%=1.0` is **1 percent**, not 100%; PositionSizer already treats `>= 1.0` as percent
- Compact handoff JSON omitted the correlation matrix, so import-time heat could never get L2/L3 without expanding the snapshot
- Daily WUT snapshots previously stored score components but **not** pairs — only PBR jsonb had the matrix
- Four Mint OPs (#311, #382, #384, #797) already share books; after this change they share one PCS copy (91.31 / 45 pairs) with recipe-specific L1 (5 vs 4)
- Yellow max \|ρ\| ≈ 0.51 is **L3-only** today (threshold 0.40); L2 (0.70) still idle

---

## 6. Issues & Tickets

### Resolved this session
- Heat L2/L3 not wired on Turtle paper OPs because pair map never crossed the handoff
- Strategy dump hid pyramid spacing and PCS/heat

### Deferred
- `portfolio_configs/*.json` heat stamps live on the compose volume only (sawtooth root is not a git repo)
- WUT test DB `db:test:purge` still tries `localhost:5432` in compose (pre-existing); specs ran against the mounted app DB
- Specs that scored against development published two junk copies (`PCS Attacher Portfolio`, `Portfolio Daily Score Test`); deleted from Wv2 after smoke
- History API points often omit symbols; sync stamps latest symbols onto history rows so the score series can copy
- No dedicated ticket filed; heat program ticket `2026-07-25-ts-portfolio-heat-unit-limits.md` already marked Phases 0–4 done

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| Wv2 ingest / heat / importer / desk gate | `bundle exec rspec` 6 files | ✅ 44 examples, 0 failures |
| WUT pairs / publisher / attacher / exporter | `bundle exec rspec` 5 files | ✅ 21 examples, 0 failures |
| Live WUT daily score | `PortfolioCorrelationDailyScorer.run!` | ✅ 11 scored, 0 errors |
| Live Wv2 copies | 11 registry rows; Mint 45 pairs; Yellow 136 | ✅ |
| #797 / #798 / other Mint OPs | `PortfolioHeat.resolve` + strategy auditor | ✅ `source=pcs_copy` |

**Test command(s):**

```bash
bin/compose exec -T winston_v2 bundle exec rspec \
  spec/services/operations/correlation_snapshot_ingest_spec.rb \
  spec/services/operations/portfolio_heat_spec.rb \
  spec/services/operations/task_generator_heat_spec.rb \
  spec/services/operations/portfolio_config_importer_spec.rb \
  spec/services/portfolio_correlation_report_enricher_spec.rb \
  spec/services/daily_report_payload_builder_attention_spec.rb

bin/compose exec -T winston_unit_test bundle exec rspec \
  spec/services/correlation_pair_map_spec.rb \
  spec/services/wv2_correlation_publisher_spec.rb \
  spec/services/portfolio_correlation_daily_scorer_spec.rb \
  spec/services/portfolio_backtest_correlation_attacher_spec.rb \
  spec/services/portfolio_config_exporter_spec.rb
```

---

## 8. Environment, Dependencies, Data

- **Dependencies:** None new (WUT already had HTTParty)
- **Services:** Existing compose stack; no rebuild
- **Migrations:** WUT `20260816120000` add `pairs`; Wv2 `20260816120000` create `portfolio_correlation_snapshots`. Applied on compose Postgres.

---

## 9. Risks & Technical Debt

- Auto-enabling heat whenever a pair copy exists changes S4-class books (L2/L3 can now pass signals). L1 stays that OP’s `max_positions_per_symbol`, so a 5-lot recipe is not cut to 4
- Latest-pair heat can tighten mid-series if WUT’s daily window moves a pair across 0.40 / 0.70 — intended, but operators should watch Yellow
- WUT publisher is fire-and-forget; if Wv2 is down, Daily Analysis pull is the backstop
- Duplicate `CorrelationPairMap` in both monoliths (no shared gem; ADR-001)
- Composer test-DB host still wrong; easy to pollute development PCS copies if specs run against it

---

## 10. Open Questions

- **Pin heat vintage to the promoting PBR window, or always latest?** — needs answer from: operator; blocks: none (latest is live)
- **Should White (max \|ρ\| 0.93) stay Active paper with L2 binding hard?** — needs answer from: operator; blocks: none

---

## 11. Handoff & Resume Notes

- **Where I left off:** Live copies in place; #797/#798 auditor shows heat + PCS; wrap in progress
- **Next concrete step:** Tomorrow’s Daily Analysis should pull/push without a manual score. Watch Yellow for `heat_loose_corr` passes
- **Files to read first:**
  1. `winston_v2/app/services/operations/portfolio_heat.rb`
  2. `winston_v2/app/models/portfolio_correlation_snapshot.rb`
  3. `winston_unit_test/app/services/wv2_correlation_publisher.rb`
  4. `ecosystem/docs/adr/ADR-007-portfolio-correlation-score-sot.md`

**Ops commands:**

```bash
bin/compose exec -T winston_unit_test bin/rails portfolios:correlation_daily_score
bin/compose exec -T winston_unit_test bin/rails portfolios:correlation_publish_wv2
bin/compose exec -T winston_v2 bin/rails wv2:sync_correlation
bin/compose exec -T winston_v2 bin/rails wv2:portfolios:inspect_strategy[797]
```

---

## 12. Stakeholder Communications

- Operator already has the desk one-liners. No external email needed.
- Optional `/stakeholder` if you want a non-engineer note: “Mint is diversified enough to run 12 units; Yellow will skip some adds when names move together.”

---

## 13. Tools & Workflow Notes

- **Skills used:** `operator-prose`, `session-report`, `wrap`
- **What worked well:** Live compose score + push proved Books-keyed identity immediately (four Mint fingerprints, one copy)
- **Friction points:** Unrelated dirty files in all three repos (risk_scale, fill cadence, BG tickets) — staged by path only
- **Subagent usage:** _None._

---

## 14. Follow-up Actions

- [ ] Confirm tomorrow’s DA copies a new `as_of_date` without a manual rake — owner: operator — due: next session
- [ ] Watch Yellow DAR / PassedSignals for `heat_loose_corr` — owner: operator — due: first Yellow cluster add
- [ ] Optionally file a ticket to pin heat vintage vs latest — owner: operator — due: if Yellow chatter is noisy

---

## 15. Appendix (optional)

Live after WUT `PortfolioCorrelationDailyScorer.run!(as_of_date: Date.current)` and push:

| Seed | PCS | max \|ρ\| | pairs | books |
|------|-----|-----------|-------|-------|
| Mint | 91.31 | 0.165 | 45 | 10 |
| Yellow | 73.04 | 0.505 | 136 | 17 |
| Walnut | 91.86 | 0.156 | 45 | 10 |
| White | 41.75 | 0.929 | 190 | 20 |

#797 auditor excerpt:

```
risk: static  stop=move_to_last_entry  atr=2.0  max_pyr=4  pyr_atr=0.5
heat: L1=4 L2=6 L3=10 L4=12 source=pcs_copy pairs=45
PCS copy: 91.31  max|r|=0.165  seed=Portfolio Mint
```
