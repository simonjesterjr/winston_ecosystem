# Session Report — MACD 12/26/9 parquet, TS rule, inspect pane

**Date:** 2026-09-10
**Time:** ~08:00–08:51 MDT (implementation); analysis started 2026-09-09
**Duration:** ~analysis session (abandoned plan) + ~1h implementation
**Project:** sawtooth Winston ecosystem — `data_manager`, `winston_unit_test`, `winston_v2`, `ecosystem/`
**Working directory:** `/home/johnkoisch/Documents/com/sawtooth`
**Branch:** `main` on each touched repo (from `origin/main`)
**Model:** Grok 4.6
**Operator:** johnkoisch

---

## 1. Goal & Outcome

**Stated goal:** From the Hidden Markov Model (HMM) analysis (`Winston/math/hidden markov chains tied to Winston.md`), take the one concrete leftover: bake Moving Average Convergence/Divergence (MACD) 12/26/9 in data_manager (DM), add it as a selectable Trading Strategy (TS) rule in Winston Unit Test (WUT), and paint it under Average True Range (ATR) on Winston v2 (Wv2) Signal Inspect.

**Outcome:** Delivered. HMM overlay itself was not built. GOOGL parquet re-baked; inspect live on Tailscale.

**One-line summary:** MACD 12/26/9 is now a Winston EOD Standard v0.2 derivative, a `Macd1269Strategy` primitive in WUT and Wv2, and a third pane under ATR on Signal Inspect.

---

## 2. Work Completed

- HMM analysis treated as a dead end except MACD; no HMM states in parquet, no bake-off.
- DM always computes `macd_line` / `macd_signal` / `macd_histogram` (12/26/9), including the default path when WUT requirements are missing.
- Fixed DM write bug: `compute_macd` used to key by date while `standardize` read integer indices, so MACD never landed.
- Winston EOD Standard bumped 0.1 → **0.2**; ADR-003 and CONTEXT glossary updated.
- `ParquetRestandardizeService` + `rake data:restandardize[SYMBOL]` re-bakes derivatives without re-download.
- GOOGL restandardized: 1801 bars, 1768 with MACD.
- WUT `Macd1269Strategy` (state: long iff line > signal), registry path, lookback 34, `db:seed_strategies`.
- Wv2 matching class + inspect three-pane Plotly (price / ATR / MACD) with fallback compute from closes if parquet is old.
- Live inspect payload verified for GOOGL 2026-09-09.

---

## 3. Code Delivered

### Files changed (this session only — do not stage the rest of the dirty trees)

#### data_manager

| File | Change | Notes |
|------|--------|-------|
| `app/services/parquet_standardizer.rb` | modified | Always-on MACD; array-aligned `compute_macd` |
| `app/services/parquet_restandardize_service.rb` | added | In-place re-bake |
| `lib/tasks/data.rake` | modified | `data:restandardize[SYMBOL]` |
| `spec/services/parquet_standardizer_spec.rb` | added | Default path + warm-up index 33 |
| `spec/services/parquet_restandardize_service_spec.rb` | added | Columns land on existing parquet |
| `AGENTS.md`, `README.md`, `data/README.md` | modified | ATR-17 + MACD + MAs |

#### winston_unit_test

| File | Change | Notes |
|------|--------|-------|
| `app/strategies/entry_exit/macd_1269_strategy.rb` | added | Uses `IndicatorCalculator.calculate_macd` |
| `app/strategies/strategy_registry.rb` | modified | Explicit `FILE_PATHS` (underscore would be `macd1269_…`) |
| `app/services/strategy_lookback.rb` | modified | `PERIODS["Macd1269Strategy"] = 34` |
| `lib/tasks/seed_strategies.rake` | modified | Catalog row |
| `spec/strategies/macd_1269_strategy_spec.rb` | added | Rising/falling/short lookback/registry |
| `spec/services/strategy_lookback_spec.rb` | modified | Assert 34 |

#### winston_v2

| File | Change | Notes |
|------|--------|-------|
| `app/strategies/entry_exit/macd_1269_strategy.rb` | added | Inlined SMA-seeded EMA; 6-arg evaluate arity |
| `app/strategies/strategy_registry.rb` | modified | `CATALOG` |
| `app/services/strategy_lookback.rb` | modified | 34 |
| `app/services/operations/signal_inspect_payload.rb` | modified | `MACD_COLUMNS` on chart bars |
| `app/services/operations/signal_inspect_overlay_builder.rb` | modified | Always `macd_pane` (parquet or compute) |
| `app/services/operations/signal_inspect_pdf_renderer.rb` | modified | Ignores `macd_pane` |
| `app/views/operations/signal_inspect/show.html.erb` | modified | yaxis3, hist column, taller chart |
| `spec/strategies/macd_1269_strategy_spec.rb` | added | |
| `spec/services/operations/signal_inspect_overlay_builder_spec.rb` | added | |
| `spec/services/operations/signal_inspect_payload_spec.rb` | modified | |
| `spec/strategies/strategy_registry_spec.rb` | modified | |

#### ecosystem

| File | Change | Notes |
|------|--------|-------|
| `interfaces/winston-eod-parquet-standard.md` | modified | v0.2; required MACD columns |
| `docs/adr/ADR-003-dm-owns-derivatives.md` | modified | MACD bullet |
| `CONTEXT.md` | modified | Winston EOD Standard glossary |
| `docs/session-reports/2026-09-10-0851-macd-1269-parquet-inspect.md` | added | This report |

**Not this session (leave unstaged):** WUT ponytail tickets / INDEX; Wv2 slate, Quiver Tracking, schema, ops-shell; ecosystem ADR-013, Walnut tickets, `vendor/`, etc.

### Commits

- _Pending wrap Step 2 (follow-up promotion) then per-monolith commit._

### Branch / PR state at sign-off

- Branch: `main` on DM / WUT / Wv2 / ecosystem — dirty with this session plus unrelated prior work
- Pushed: not yet
- PR: not opened (direct `main`)

---

## 4. Decisions Made

### Decision 1: Bake MACD, not HMM
- **Choice:** First-class parquet columns + TS primitive + inspect pane. No hidden-state column, no regime overlay engine.
- **Why:** HMM on EOD Trend Following (TF) is a fifth orthogonal layer that needs residual-signal / true walk-forward first; MACD is the theoretically next TF rule (semi-Markov → MACD-like) and was already half-implemented.
- **Alternatives considered:** HMM in DM; MACD as lab-only; wait for P1 residual-signal ticket.
- **Reversibility:** easy (columns are extra; consumers tolerate missing)
- **Promote to ADR?** No — ADR-003 one-line update is enough. Standard bump is the contract.

### Decision 2: `Macd1269Strategy` state, not crossover
- **Choice:** Long when `macd_line > macd_signal` on lookback **plus current bar**.
- **Why:** Matches EMA-20 style (current state). Periods locked in the class name.
- **Alternatives considered:** Previous-bar crossover; configurable 12/26/9 knobs.
- **Reversibility:** easy (new class; unused by live fingerprints)
- **Promote to ADR?** No

### Decision 3: Inspect always shows MACD under ATR
- **Choice:** Third Plotly pane whenever points exist; parquet preferred, else compute from chart closes.
- **Why:** Operator asked for the pane on inspect, not only when the OP uses the MACD rule.
- **Alternatives considered:** Overlay only when TS includes Macd1269.
- **Reversibility:** easy
- **Promote to ADR?** No

---

## 5. Insights Surfaced

- DM already had `compute_macd` but never wrote it: date-keyed Hash vs `macd_data[i]`. Also WUT compact EMA arrays vs DM index-aligned `compute_ema` needed a compact-line scatter-back.
- 60% CAGR / HMM lore is Medallion-class, not an EOD TF overlay target (already in Berlekamp lessons 2026-07-30).
- WUT `IndicatorRequirements` already listed `macd_*`; that is not the DM always-on switch. Defaults when WUT fetch failed omitted MACD.
- Restandardize must go through `ParquetStandardizer` (split-adjust is idempotent on already-adjusted files because jumps no longer detect).

---

## 6. Issues & Tickets

### Resolved this session
- MACD never written to parquet despite code existing (`parquet_standardizer.rb` index bug).
- Inspect had no MACD pane; ATR-only `yaxis2`.

### Deferred
- Full-corpus parquet re-bake (only GOOGL done). Other symbols: next acquire or `data:restandardize[SYM]`. Inspect still paints from closes.
- One-axis MACD-confirm vs EMA-20 on frozen Blue C03 / Turtle Mint — blocked on `2026-09-04-tf-p1-residual-signal-and-oos.md`.
- HMM regime overlay (causal Forward posterior) — research only; do not start until measurement layer exists.
- WUT vs Wv2 `Macd1269Strategy` implementations are duplicated (calculator vs inlined EMA), not a shared gem (ADR-003).

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| DM standardizer + restandardize | compose rspec | ✅ 5 examples |
| WUT strategy / registry / lookback | compose rspec | ✅ 10 examples |
| Wv2 strategy / inspect payload / overlay | compose rspec | ✅ 15 examples (plus prior 20 from contractor) |
| GOOGL parquet | `data:restandardize[GOOGL]` | ✅ 1768/1801 MACD |
| WUT TS picker | GET `/trading_signal_strategies` | ✅ "MACD 12/26/9" |
| Inspect live | curl payload local + Tailscale | ✅ 90/90 MACD points, `yaxis3`, hist column |
| Plotly click-through in a browser | none | ⚠️ payload + JS present; no mouse/legend exercise |

**Test command(s):**

```bash
./bin/compose exec -T -e RAILS_ENV=test data_manager bundle exec rspec \
  spec/services/parquet_standardizer_spec.rb spec/services/parquet_restandardize_service_spec.rb

./bin/compose exec -T -e RAILS_ENV=test -e TEST_DB_HOST=wut_postgres winston_unit_test \
  bundle exec rspec spec/strategies/macd_1269_strategy_spec.rb \
  spec/strategies/strategy_registry_breakout10_spec.rb spec/services/strategy_lookback_spec.rb

./bin/compose exec -T -e RAILS_ENV=test -e TEST_DB_HOST=wv2_postgres winston_v2 \
  bundle exec rspec spec/strategies/macd_1269_strategy_spec.rb \
  spec/services/operations/signal_inspect_payload_spec.rb \
  spec/services/operations/signal_inspect_overlay_builder_spec.rb
```

**Live:** https://sawtooth-ai.tail944ffb.ts.net/wv2/operations/signal_inspect?as_of=2026-09-09&portfolio_id=11&symbol=GOOGL&window=90  
Last MACD: line −3.623, signal −2.865, histogram −0.758 (2026-09-09).

---

## 8. Environment, Dependencies, Data

- **Dependencies:** None added
- **Services:** compose DM / WUT / Wv2 already up; Wv2 restarted after inspect JS change
- **Migrations:** None
- **Data:** GOOGL `bars.parquet` rewritten on DM volume (MACD columns). Other symbols still v0.1 until restandardize/acquire.

---

## 9. Risks & Technical Debt

- Inspect fallback MACD on a 90-bar window has warm-up nils at the left of the pane; full-history parquet (GOOGL) does not.
- Two copies of MACD math (DM standardizer, WUT calculator, Wv2 strategy/overlay). Drift risk if periods or EMA seed change.
- `Macd1269Strategy` is selectable but unused by engaged Operational Portfolios; do not treat presence as a recipe change.
- Dirty trees in Wv2/WUT/ecosystem contain unrelated work — wrap must stage precise paths only.

---

## 10. Open Questions

- **Restandardize the whole parquet tree now, or wait for natural acquire?** — operator; blocks inspect table column on non-GOOGL names (pane still works via compute).
- **Promote MACD as a confirmational experiment after P1 residual-signal?** — lab; does not block this landing.

---

## 11. Handoff & Resume Notes

- **Where I left off:** Live inspect shows MACD under ATR for GOOGL; WUT seed applied; wrap report written, commits pending follow-up promotion.
- **Next concrete step:** Operator shortcut on follow-ups, then commit/push four repos (precise file lists). Optionally `data:restandardize` other active Book symbols.
- **Files to read first:**
  1. `ecosystem/interfaces/winston-eod-parquet-standard.md` (v0.2)
  2. `data_manager/app/services/parquet_standardizer.rb` (`compute_macd`)
  3. `winston_unit_test/app/strategies/entry_exit/macd_1269_strategy.rb`
  4. `winston_v2/app/views/operations/signal_inspect/show.html.erb` (yaxis3)

---

## 12. Stakeholder Communications

- _None._ Operator-facing: MACD is available to pick on a TS and to see on inspect. It is not a live default and does not change Capital Activation.

---

## 13. Tools & Workflow Notes

- **Skills used:** operator-prose, wrap, session-report; four subagents (chief of staff + DM + WUT + Wv2)
- **What worked well:** Frozen class/periods/evaluate contract in parallel prompts; monoliths did not collide.
- **Friction points:** Host `bundle exec rspec` cannot reach compose Postgres (`TEST_DB_HOST=*postgres`). Nested-quote Python in bash failed; heredoc worked.
- **Subagent usage:** Chief of staff (read-only checklist); DM, WUT, Wv2 implementers. Parent added restandardize rake, GOOGL bake, seed, inspect smoke, 6-arg evaluate on Wv2.

---

## 14. Follow-up Actions

- [ ] Restandardize remaining DM parquet (or at least Active OP Book symbols) so inspect table/parquet columns match GOOGL — owner: operator/DM — due: when convenient
- [ ] One-axis MACD confirm vs EMA-20 on frozen parents — owner: lab — due: after P1 residual-signal / walk-forward
- [ ] Do not start HMM overlay until that measurement layer exists — owner: lab — due: later
- [ ] Optional: keep WUT/Wv2 MACD math comments pointing at DM as SoT if they ever drift — owner: whoever next touches them

---

## 15. Appendix (optional)

Evaluate rule (frozen): lookback 34 + current bar; long `macd_line > macd_signal`; short opposite; false if unwarm.

```bash
./bin/compose exec -T data_manager bin/rails data:restandardize[GOOGL]
# {:symbol=>"GOOGL", :bar_count=>1801, :macd_count=>1768, :error=>nil}
```
