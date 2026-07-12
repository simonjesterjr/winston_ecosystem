# Portfolio Correlation Methodology, Score, and New Color Cohorts

**Status:** Phases 0–6 + ops follow-through complete; remaining work in tickets  
**Updated:** 2026-07-12  
**ADR:** `docs/adr/ADR-007-portfolio-correlation-score-sot.md`  
**Supersedes / extends:** `portfolio-overlap-rebuild.md` (membership doctrine); does **not** replace Red/Blue/Orange/White history  
**Session analysis:** correlation audit 2026-07-11 (calculator OK on clean pairs; White/Orange membership flawed)

---

## Goal

1. Harden WUT portfolio-correlation **methodology** (max pairwise, quality gates, fixed window, transparent metrics).
2. Define a durable, transparent **Portfolio Correlation Score** as a **time series** (lab → export → operational tracking → rebalance signal).
3. Ship **UI / visualizers** so correlation is inspectable in WUT portfolio chooser and correlation tools.
4. Build **four new** seed portfolios (**Green, Pink, Blank, Rust**) with the new methodology; vet for optimal **TradingStrategy**; export to Wv2 for **Paper Trading**.
5. Surface the score in **Daily Activity Report (DAR)** overview (time-series table) and on WUT **Portfolio Backtest Run (PBR)** metadata.

---

## Why (audit summary)

| Finding | Implication |
|---------|-------------|
| Pearson daily-return math is trustworthy on liquid pairs (GLTR/GLD ≈ 0.91; SPY/GLD ≈ 0.13; SPY/VXX ≈ −0.28) | Do **not** rewrite correlation formula first |
| Greedy objective = min **mean** \|r\| only | Admits twins; mean diluted by junk |
| No max-pairwise hard reject | White: **DBE/OILK ≈ 0.93** on final window |
| Window non-stationarity | DBE/OILK full-sample ~0.18 vs post-2022 ~0.93 — twins enter under long window |
| COPR unsuitable (~77% zero returns) | Dilutes Orange + White mean \|r\| |
| Orange “metals” is equity tech cluster | Theme not enforced |
| White “weak” rating is **correct** (high pair), not inverted labels | Close/rewrite label ticket |

External litmus anchors: Portfolio Visualizer asset-class matrices; Equinox 2018 (`winston_unit_test/planning/equinox_correlation_insights.md`); liquid golden pairs above.

---

## Domain terms (proposed — confirm in grill)

| Term | Meaning |
|------|---------|
| **Portfolio Correlation Score (PCS)** | Single scalar (0–100 or 0–1) summarizing diversification quality of a portfolio’s **Books** under a versioned methodology |
| **Correlation Snapshot** | Point-in-time record: score + component metrics + methodology version + date window + optional high pairs |
| **Correlation Methodology Version** | Immutable recipe id (e.g. `corr_v2`) for score components, windows, quality gates — required for comparable time series |
| **Color Cohort** | Named seed-anchored lab portfolios (existing Red/Blue/Orange/White; new Green/Pink/Blank/Rust) |

_Avoid:_ “correlation” alone (pairwise r vs portfolio score); treating PCS as a TradingStrategy metric.

**Rebalance (ops):** ADR-006 — shape change is **successor path**, not in-place mutation of an **Engaged Operational Portfolio**. PCS degradation should **flag** rebalance review, not auto-mutate Books.

---

## Architecture

```
WUT (SoT for PCS)                         Handoff / API                    Wv2 ops
─────────────────                         ────────────                     ───────
Build Books (corr_v2)              →      correlation_snapshot {}   →      baseline on import (optional cache)
PCS service + daily job (post-DM)  →      internal API / client     →      WUT client fetch for DAR / tasking
Snapshots time series (PG)         →      seed + Books identity     →      flag only if PCS degrades
Heatmap / chooser / PBR metadata          export fingerprint               DAR overview time-series table
```

**Grill decision:** WUT owns computation and durable time series. Wv2 does **not** recompute a parallel formula. After DM data is ready, a **WUT scheduled job** re-scores portfolios; Wv2 reaches **back** via a **WUT client** whenever tasking (DAR, etc.) needs current PCS/history.

### Storage (recommended)

**WUT (source of truth)**

| Store | Contents |
|-------|----------|
| `portfolio_correlation_snapshots` (new) | `portfolio_id`, `as_of_date`, `score`, components jsonb, `methodology_version`, `source` (`builder` \| `daily_job` \| `pbr` \| `manual`) |
| Daily job | After DM parquet readiness: recompute PCS for scored portfolio set; idempotent per (portfolio, date, methodology_version) |
| Internal API | e.g. list/latest/history snapshots by portfolio name/seed (and optional Books fingerprint) for Wv2 client |
| `portfolio_backtest_runs` | jsonb `correlation_snapshot` (or FK) at run time |
| Sidecar JSON | Matrix + PCS fields |

**Wv2 (consumer)**

| Store | Contents |
|-------|----------|
| Optional thin cache | Last-fetched snapshot for offline DAR resilience (not competing SoT) |
| Import | Embed baseline from handoff JSON |
| DAR / tasking | WUT client: pull series for Active OPs (match by seed_name / export provenance) |
| Daily Analysis | Does **not** recompute PCS; may attach client-fetched snapshot to notification payload |

**Handoff JSON** (`portfolio_configs/*.json`) — additive block:

```json
"correlation_snapshot": {
  "methodology_version": "corr_v2",
  "as_of_date": "2026-07-11",
  "score": 72.5,
  "mean_abs_correlation": 0.18,
  "max_abs_correlation": 0.48,
  "high_pair_count": 0,
  "pair_threshold": 0.70,
  "max_pairwise_build_cap": 0.55,
  "window_start": "2019-05-08",
  "window_end": "2026-07-10",
  "trading_days": 1799,
  "quality_flags": [],
  "high_pairs": [],
  "symbols": ["..."]
}
```

### PCS formula (`corr_v2`) — **decided in grill: max \|r\| first**

Components (all on **fixed** analysis window, quality-filtered symbols only):

| Component | Direction | Weight (draft) |
|-----------|-----------|----------------|
| `1 - max_abs_r` (clamped) | higher better | **0.50** |
| High-pair penalty (count of \|r\| > 0.70) | lower better | **0.25** |
| `1 - mean_abs_r` (clamped) | higher better | **0.15** |
| Quality / coverage penalty | lower better | **0.10** |

Scale to **0–100**. Publish formula in sidecar + DAR footnote. Changing weights → new `methodology_version` (do not rewrite history).

**Primary operator metric is max \|r\|**; mean is secondary (anti-dilution). PCS is the tracked composite for time series and rebalance *flags*.

### Methodology hardening (`corr_v2` build policy)

| Control | Default |
|---------|---------|
| Max pairwise \|r\| hard reject during greedy | **0.55** |
| Weak label threshold (advisor) | any \|r\| > **0.70** or mean > 0.50 |
| Fixed evaluation window for greedy + score | full available overlap **or** explicit `WINDOW_START`/`END` (same for all steps) |
| Symbol quality | min bars, min unique closes, max zero-return fraction (drops COPR-class) |
| Target size new cohorts | **8–12** markets (not 15–20) |
| Overlap | seed exclusivity + bilateral **≤25%** (existing `PortfolioOverlapPolicy`) |
| Theme | seed-first shortlist + diversifiers; no pure tech dump for metals seeds |

---

## Phased execution

### Phase 0 — Grill + docs — **Done**

- Grill decisions recorded (PCS max-first; WUT SoT; registry daily set; flag-only degradation; archive O/W; six common portfolios).
- `CONTEXT.md` terms: PCS, Correlation Snapshot, Methodology Version, DAR.
- ADR-007 accepted.
- Ticket `2026-07-08-diversification-advisor-label-scale.md` clarified (not inverted scale).

### Phase 1 — Litmus + transparency foundation (WUT) — **Done 2026-07-11**

- Rake `portfolios:correlation_litmus` — golden pairs + quality scan of registry books.
- Services: `PortfolioCorrelationLitmus`, `MarketSeriesQuality`.
- Document bands: `docs/analysis/portfolio-correlation-litmus.md`.
- Unit specs green; live compose run **PASS** (JSON: `portfolio_configs/correlation-litmus-latest.json`).
- Calculator fix: partial `start_date`/`end_date` now clamps to data overlap (post-2022 twin diagnostic works).
- Live findings: White max\|r\|≈0.93 (DBE/OILK); COPR/CIZ/CMDT quality fails; Red/Blue OK on high pairs.

### Phase 2 — Methodology + PCS engine (WUT) — **Done 2026-07-11**

- `PortfolioCorrelationScorer` (`corr_v2`, max-|r| first weights)
- `PortfolioCorrelationSnapshot` model + migration (WUT SoT table)
- `PortfolioCorrelationBuilder` hard max-pairwise (default 0.55), quality prefilter, rejection log, PCS + snapshot on build
- `MarketCorrelationCalculator::CandidateScore` includes `max_abs_correlation`
- Advisor summary surfaces max |r| / high-pair examples when weak
- Rake `build_correlation`: `MAX_PAIRWISE`, `REQUIRE_QUALITY`, `WINDOW_START`/`END`, `PERSIST_SNAPSHOT`
- Specs: scorer, builder twin/quality reject, advisor weak summary

**Files:**

- `app/services/portfolio_correlation_scorer.rb`
- `app/services/portfolio_correlation_builder.rb`
- `app/services/market_correlation_calculator.rb`
- `app/services/portfolio_diversification_advisor.rb`
- `app/models/portfolio_correlation_snapshot.rb`
- `db/migrate/20260711210000_create_portfolio_correlation_snapshots.rb`
- `lib/tasks/portfolio_correlation.rake`

### Phase 3 — WUT visualizers (portfolio chooser / correlation tools) — **Done 2026-07-11**

- Shared strip: `app/views/shared/_correlation_transparency_strip.html.erb` (mean, max, PCS, window, high pairs, quality flags, PCS sparkline)
- Portfolio Builder index + review: strip when ≥2 markets; candidate table columns **Avg |r|**, **Max |r|**, **Flags** (`quality`, `max_pairwise`, `high avg`)
- Correlation Calculator: strip + PCS/max in results summary after calculate
- Matrix cell colors: orange &gt; 0.55, amber &gt; 0.70 (`CorrelationCalculatorHelper`)
- Helper specs for cell classes + candidate badges

### Phase 4 — PBR metadata (WUT) — **Done 2026-07-11**

- Column `portfolio_backtest_runs.correlation_snapshot` (jsonb)
- `PortfolioBacktestCorrelationAttacher` — PCS + matrix on attach; also upserts portfolio snapshot SoT
- Capture on: UI create, factory `create_from_optimization!`, runner complete
- Export paths include `correlation_snapshot`: vet_trend, `wut:portfolios:export_config`, `/internal/portfolio_config`
- PBR show: PCS box in metadata, full transparency strip + heatmap/matrix + export JSON panel
- Spec: `portfolio_backtest_correlation_attacher_spec.rb`

### Phase 5 — Handoff + WUT daily job + Wv2 client + DAR — **Done 2026-07-11**

- WUT `PortfolioCorrelationDailyScorer` + `PortfolioCorrelationDailyScoreJob` (cron 07:30 MT + after DailyOperationsJob)
- Rake `portfolios:correlation_daily_score` (`AS_OF=`, `STRICT=1`)
- Internal API: `GET /internal/correlation_scores`, `GET /internal/correlation_scores/history`
- Wv2 `WutClient` + `PortfolioCorrelationReportEnricher` (lab name strip fingerprint; flags high max\|r\| / PCS drop ≥10)
- DAR markdown + PDF: correlation table, PCS multi-series chart, flags → next_steps `review`
- Notification payload field `correlation_scores`

### Phase 6 — New cohorts: Green, Pink, Blank, Rust — **Membership done 2026-07-12**

**Seeds (liquid, quality-pass, not legacy seeds):**

| Portfolio | Seed | Theme | n | PCS | Max \|r\| | Rating |
|-----------|------|-------|---|-----|-----------|--------|
| **Green** | **ICLN** | Clean energy / climate | 12 | 83.3 | 0.31 | strong |
| **Pink** | **PINK** | Healthcare / biotech | 12 | 76.3 | 0.44 | strong |
| **Blank** | **ZROZ** | Rates / vol diversifier | 12 | 71.3 | 0.53 | strong |
| **Rust** | **XLI** | Industrials / cyclicals | 12 | 77.2 | 0.42 | strong |

**Membership (2026-07-12):**

- Green: AMZA, BERZ, BFIX, CORN, ICLN, JNJ, PHYMF, SCHD, SH, SPTI, VXX, WMT  
- Pink: AFIF, AGZ, COM, DBA, FXI, IYH, JNJ, MSFT, PINK, UUP, WMT, WTI  
- Blank: AAAU, BIB, BWX, COMB, MSFT, PPLT, ROKU, RXT, SEF, SVXY, WTI, ZROZ *(rebuilt with fixed window after first pass max\|r\|=0.76)*  
- Rust: AAAU, AFIF, BFIX, BIS, DBA, DBE, GOOGL, RGI, RXT, SCHD, USDU, XLI  

**Infrastructure:**

- `PortfolioOverlapPolicy` seeds extended: ICLN/PINK/ZROZ/XLI  
- Rake `portfolios:build_new_cohorts` (optional `[green|pink|blank|rust]`)  
- Sidecars: `portfolio_configs/portfolio-{green,pink,blank,rust}-sidecar.json`  
- Registry: 8 color portfolios; all bilateral overlaps for new cohorts ≤25%  
- Daily PCS scores all 8  

**Follow-through (2026-07-12):**

1. Human heatmap review → **dashboard design** filed: `docs/analysis/2026-07-12-portfolio-correlation-dashboard.md`  
2. `vet_trend` **done** for Green/Pink/Blank/Rust (exports under `portfolio_configs/portfolio-*.json`)  
3. Wv2 paper import + **Active** for six common set **done** (Orange deactivated; White not activated)

### Phase 7 — Legacy colors

- **Red + Blue:** remain in the six common set; recompute PCS under corr_v2 for transparency (membership rebuild only if policy fails).
- **Orange + White:** **archived** (history/sidecars retained); not primary paper focus; optional PCS recompute for audit only.
- Blue strategy economics revisit remains separate ticket.

### Phase 8 — Closeout / remaining tickets

- [x] Plan status + `portfolio-overlap-rebuild.md` cross-link  
- [x] Session report (wrap)  
- [ ] Business-context PCS doc — ticket `docs/tickets/2026-07-12-pcs-business-context-doc.md`  
- [ ] WUT correlation dashboard — ticket `docs/tickets/2026-07-12-wut-portfolio-correlation-dashboard.md`  
- [ ] Re-vet Blank/Rust for trade-ready — ticket `docs/tickets/2026-07-12-re-vet-blank-rust-trade-ready.md`  
- [ ] Wv2 six-cohort evaluate smoke — ticket `docs/tickets/2026-07-12-wv2-six-cohort-evaluate-smoke.md`

---

## DAR design (overview)

**Winston Daily Activity Report — summary page**

Existing: equity chart, STATUS table, NEXT STEPS.

**Add section:** `CORRELATION SCORES (Active)`

| Portfolio | PCS | Max\|r\| | Mean\|r\| | Δ7d | Window | Ver |
|-----------|-----|---------|----------|-----|--------|-----|
| … | 72 | 0.48 | 0.18 | −3 | 2019-… | corr_v2 |

**Grill decision — both from day one:**

1. **Numeric table** — last ~15–20 as_of dates × Active portfolios (or portfolio rows with last-N scores). Required for PDF + markdown.
2. **Sparkline / multi-series PCS chart** — reuse `ReportPdfChartDrawer` equity-chart pattern where feasible; do not ship PDF without attempting chart (fallback: table-only if chart data missing).

Markdown renderer includes the same section for Telegram/MCP consumers.

---

## Litmus (calculator health)

| Pair | Band | Notes |
|------|------|-------|
| GLTR/GLD | r > 0.80 | Metals identity |
| SPY/GLD | \|r\| < 0.35 daily | Cross-asset |
| SPY/VXX | r < 0 | Stress diversifier sign |
| AAPL/XLK | 0.35–0.75 daily | Equity cluster |
| COPR quality | fail gate | Bad series |
| DBE/OILK | report **both** full and post-2022 | Non-stationary twin |

---

## Critical code paths

| Path | Role |
|------|------|
| `winston_unit_test/app/services/market_correlation_calculator.rb` | Engine |
| `winston_unit_test/app/services/portfolio_correlation_builder.rb` | Greedy build |
| `winston_unit_test/app/services/portfolio_overlap_policy.rb` | Seeds + 25% |
| `winston_unit_test/app/controllers/portfolio_builder_controller.rb` | Chooser UI |
| `winston_unit_test/app/controllers/correlation_calculator_controller.rb` | Tool UI |
| `winston_unit_test/app/models/portfolio_backtest_run.rb` | PBR metadata |
| `portfolio_configs/` | Handoff + registry |
| `winston_v2` Daily Analysis + `daily_activity_report_*_renderer.rb` | Ops PCS + DAR |
| `ecosystem/interfaces/` (handoff / notification) | Document snapshot fields if needed |

---

## Explicit non-goals

- Auto-rebalance Books when PCS drops (flag only; ADR-006 successor path is human/Cromwell).
- Scraping Portfolio Visualizer.
- Replacing Pearson unless litmus fails.
- Fixing Blue −98% economics in this plan (strategy ticket).
- Deleting Red/Blue/Orange/White history.

---

## Verification

1. Litmus rake green on golden pairs; COPR quality fail.
2. Builder rejects \|r\| > 0.55 twins; sidecar has PCS + max \|r\| + window.
3. UI shows high pairs and rejection reasons.
4. PBR stores snapshot; export JSON includes block.
5. Wv2 import baseline + daily snapshots idempotent.
6. DAR overview shows PCS table + multi-day series.
7. Green/Pink/Blank/Rust: built, vetted, exported, paper-imported, Active optional, series growing.
8. Overlap ≤25% across all registered color portfolios including new four.

---

## Grill decisions (so far)

| # | Topic | Decision |
|---|--------|----------|
| 1 | PCS primary signal | **Max \|r\| first** (mean secondary) |
| 2 | Green/Pink/Blank/Rust seeds | **Defer until corr_v2 works**; liquid seed pick = validation of the engine |
| 3 | PCS degradation on Engaged OP | **Flag only** in DAR / next_steps (max \|r\| > 0.70 or PCS drop >10 pts vs baseline). No auto Books change, no auto successor |
| 4 | Who computes PCS | **WUT is SoT** — service + post-DM daily job; **Wv2 WUT client** fetches for DAR/tasking (no parallel formula) |
| 5 | Daily scored set | **Registry color portfolios** in WUT (`portfolio_configs/registry.json` + successors). Wv2 maps Active OP → lab seed/name to fetch |
| 6 | DAR presentation | **Both** numeric time-series table **and** chart from day one (table required; chart with graceful fallback) |
| 7 | Orange / White | **Archive** (regime history). Do not rebuild as primary. New cohorts Green/Pink/Blank/Rust + existing **Red + Blue** → **six** common WUT↔Wv2 paper/observation portfolios |
| 8 | WUT↔Wv2 PCS identity | **seed_name** primary (export `name` / registry); fingerprint if multiple OP forks |

## Grill status

**Core decisions closed.** Ready for Phase 1–2 execution after optional ADR write-up for WUT PCS SoT + client contract.

---

## Grill recommendation

**Yes — run `/grill-with-docs` before Phase 2+ coding.**

Reasons: new glossary term (PCS), cross-monolith time series + handoff contract (ADR candidate), interaction with **Rebalance** / **Engaged OP** (ADR-006), seed selection for four new portfolios, and DAR as operator contract. Phase 1 litmus-only can proceed in parallel if desired; do not lock seeds or score formula without grill.
