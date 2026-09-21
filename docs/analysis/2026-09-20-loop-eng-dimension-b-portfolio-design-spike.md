# Loop Engineering Dimension B — Portfolio design research brief + P0 spike

**Date:** 2026-09-20 (America/Denver)  
**Audience:** John (Operator / Chief of Staff)  
**Scope:** WUT correlation scoring / PCS, regime change, need to re-weight — classical ML/stats-native (not LLM price prediction)  
**Out of scope:** Dimension A (TS+IBKR); new Ollama models; Wv2 mutate  
**Status:** Box-side research brief. **Host gaps flagged** — ListMachines / machineId Shell to sawtooth-ai was unavailable to this executor.

**Suggested host path (parent to file/copy):**  
`/home/johnkoisch/Documents/com/sawtooth/ecosystem/docs/analysis/2026-09-20-loop-eng-dimension-b-portfolio-design-spike.md`  
Box mirror written at: `/workspace/ecosystem/docs/analysis/2026-09-20-loop-eng-dimension-b-portfolio-design-spike.md`

---

## 1. Situation

Dimension B is the portfolio-geometry layer: measure how books correlate over time (PCS / `corr_v2`), detect when that geometry **regime-shifts**, and decide **when membership / weights must change** — before Turtle heat or insolvency does the job the hard way.

We already have a strong **static gate** for book compile (PCS ∈ [60, 90] raw). We do **not** yet have an offline, validated detector for “this sleeve’s PCS path has left the mid-band / high-pair structure flipped → re-weight or rebuild.” That detector is classical ML/stats work on existing snapshot history + PBR outcomes.

**Access blocker (this pass):** Executor MCP catalog = `user-Otter` only. No `ListMachines`. Box Shell cannot reach `/home/johnkoisch/Documents/com/sawtooth` or `./bin/compose exec winston_unit_test`. Live dumps of snapshot depth, ADR-007 full text, and daily_job cadence remain **host-bound**. Inventory below is from box mirrors + prior cloud-agent WUT source extracts. **Forensics did not run new host jobs in this pass.**

---

## 2. Inventory (what already exists)

### 2.1 PCS / corr_v2 (system of record)

| Artifact | Location / fact |
|----------|-----------------|
| Methodology | `METHODOLOGY_VERSION = "corr_v2"` — **ADR-007** (grill 2026-07-11) |
| Scorer | `winston_unit_test/app/services/portfolio_correlation_scorer.rb` |
| Snapshot model | `PortfolioCorrelationSnapshot` — sources: `builder`, `daily_job`, `pbr`, `manual`, `litmus` |
| WUT table | `portfolio_correlation_snapshots`: `portfolio_id`, `as_of_date`, `score`, `methodology_version`, `source`, `components`, `symbols`, `pairs`, `window_*`, `trading_days`, `mean_abs_correlation`, `max_abs_correlation`, `high_pair_count` — unique `(portfolio_id, as_of_date, methodology_version)` |
| PBR attach | `portfolio_backtest_runs.correlation_snapshot` jsonb; lazy `capture_correlation_snapshot!(source: "pbr")` on show |
| UI | `shared/_correlation_transparency_strip.html.erb` — “PCS · 0–100 · max-\|r\| first”; sparkline from last 30 snapshots |
| Wv2 mirror | `portfolio_correlation_snapshots` with `books_key` / `wut_snapshot_id` (unique on books_key+date+version) |
| **Not the same** | Turtle heat `pcs_pairwise` (close 0.7 / loose 0.4) — position gating, not book compile score |

**corr_v2 formula (locked in code):**

```
score = 100 * (
  0.50 * (1 - max_|r|) +
  0.25 * max(1 - 0.35 * high_pair_count, 0) +
  0.15 * (1 - mean_|r|) +
  0.10 * quality_pass_fraction
)
```

Thresholds: high pair > **0.70**; build-cap highlight **0.55**. Changing weights ⇒ new `METHODOLOGY_VERSION`.

**Sanity (Orange #667 offline):** score **24.86**, mean\|r\| **0.235**, max\|r\| **0.919**, high_pairs **3**. Diversification proxy `(1 − mean) × 100 ≈ 76.5`. Reconstructed corr_v2 ≈ **25.5** — matches raw score, **not** the proxy.

### 2.2 Mode C book-selection / PCS gate docs (box)

| Path | Role |
|------|------|
| `ecosystem/docs/analysis/2026-09-17-mode-c-new-book-pcs-proposal.md` | First-cut proposal; initially gated on **diversification proxy** pending Forensics |
| `ecosystem/docs/tickets/2026-09-17-mode-c-new-books-pcs-60-90.md` | **Doctrine locked:** raw PCS `score` ∈ [60, 90]; refs Blue 66.4 / Mango 64.2 / Red 71.4 |
| `ecosystem/docs/analysis/2026-09-17-mode-c-indigo-teal-copper-slate-screen.md` | Screen stub; live PCS **unconfirmed** (box-only) |
| `mode-c-cutover/00_PROBE_THEN_COMPILE.rb`, `HOST_COMPILE_FOUR_BOOKS.rb` | Host compile scripts; gate on raw score |
| CoS claims (unverified): Indigo 411@71.44, Teal 412@66.41, Copper 413@60.91, Slate 414@60.83 | Align with **raw** mid-band, not proxy |

Host-only paths still needed when bound: `ecosystem/docs/adr/ADR-007*`, `ecosystem/docs/business-context/*`, `ecosystem/plans/*`, `2026-09-17-mode-c-new-book-pcs-band.md` (ticket cites host analysis).

### 2.3 Rebalance / regime-adjacent code (not Dimension B ML yet)

| Piece | Notes |
|-------|--------|
| `quiver_rebalance_plans` + `quiver_tracking_snapshots` | Quiver Quant PDF → weekly top-20 replace. **Rule/ops path**, not PCS regime ML. |
| `portfolios.risk_scale_state` + TS risk-scale policy (ADR-010) | Kelly / anti-martingale **sizing** meta-layer — not membership re-weight. |
| TradingStrategy “selection ledger” comment | Regime/frequency insight hook for fingerprint wins — no ML pipeline found offline. |
| **Gap** | No sklearn/LightGBM/River drift job, no purged CV harness, no “reweight_signal” table found in offline dumps. |

### 2.4 Tickets

- INDEX: Mode-C PCS compile **P1 In progress** (host-blocked for several executors).  
- No dedicated “Dimension B / re-weight detector” ticket yet — this note is the seed.

---

## 3. Open Operator question — PCS gate conflict (RESOLVED for ops; confirm with John)

| Source | Gate |
|--------|------|
| Proposal 2026-09-17 §4 | Diversification proxy `(1 − mean_abs) × 100 ∈ [60, 90]` |
| Ticket doctrine (locked) + compile scripts + screen note | **Raw `score` ∈ [60, 90]** |
| UI / ADR-007 / scorer | PCS **is** the raw 0–100 max-\|r\|-first score |

**Recommendation for Operator:** Treat **raw corr_v2 `score` ∈ [60, 90]** as the Mode C compile gate. The early proxy guess was a reasonable misread when Orange’s UI-green “looks diversified” intuition (~76 proxy) collided with a low raw score (~25) dominated by max\|r\| and high pairs.

**Ask John (one sentence):** When you said successful Mode C books sit in 60–90, were you reading the **PCS number on the transparency strip** (raw), or a mental “sort-of-uncorrelated” mean-\|r\| band?  
Evidence already leans **raw** (Blue/Mango/Red refs + Indigo–Slate claims all sit mid-60s raw; Orange solvent at raw ~25 would fail a raw gate — which is exactly why Copper edits aim to break the SMH/XLK/NVDA cluster).

Do **not** use proxy ∈ [60, 90] for compile acceptance going forward unless John explicitly overrides doctrine.

---

## 4. Recommended P0 research spike (1–2 weeks)

**Goal:** Offline, leakage-safe answer to: *Given a book’s PCS path + pair structure, when should we re-weight / rebuild membership?*  
**Owners:** Operator (John) decides label doctrine + go/no-go; **Forensics** (host export); **ML spike owner** (box or host Python — John or designee); CoS tracks ticket.

### Step 1 — Data export (host, READ-ONLY) — Day 1–2

Export parquet/CSV under e.g. `ecosystem/data/dimension_b/` (host):

**A. Snapshot panel** (`portfolio_correlation_snapshots` where `methodology_version = 'corr_v2'`):

- Keys: `portfolio_id`, `as_of_date`, `source`
- Targets/features: `score`, `mean_abs_correlation`, `max_abs_correlation`, `high_pair_count`, `trading_days`, `window_start`, `window_end`
- Structure: `symbols` (json), `pairs` or `components.high_pairs`, `components` weights/components, `quality_flags`
- Derived: `Δscore_5d/20d`, `Δmax_abs`, `Δhigh_pair_count`, days_outside_[60,90], EWMA of score

**B. Portfolio roster:** `portfolios.id, name, color, seed_name, active, closed_at, trading_strategy_id` + market membership history if available (books join).

**C. Outcome labels (construct carefully):** from completed PBRs on same portfolio (or successor lineage):

- Forward 20/60 trading-day: OA/cash return, OA max DD, insolvency flag, profit factor (prefer OA doctrine; ignore stored `edge_r` until trusted)
- Optional: binary `should_have_reweighted` = PCS exited [60,90] for ≥N days **or** high_pair_count jumped ≥2 **and** next window OA DD worsened vs prior median

**D. Negative control:** Quiver rebalance legs are **out of band** for Turtle books — do not mix label definitions.

Host one-liner sketch (Forensics):

```bash
cd /home/johnkoisch/Documents/com/sawtooth
./bin/compose exec -T winston_unit_test bin/rails runner '
# dump PCS history + latest PBR outcomes for active lab portfolios
# write /tmp/pcs_panel.jsonl + /tmp/pbr_outcomes.jsonl
'
```

### Step 2 — Label + purge design — Day 2–3

- Embargo: features at `t` may only use snapshots with `as_of_date ≤ t`; outcomes from `(t, t+H]`
- **Purged walk-forward** (Lopez de Prado style): embargo ≥ corr window length (use `trading_days` / window span from snapshots, typically ~1y lookback if that is how matrix is built — **confirm on host**)
- Split by portfolio clusters (Mode C solvent vs insolvent panels) to avoid one book dominating

### Step 3 — Candidate models (classical only) — Day 3–8

| Tier | Model | Role |
|------|--------|------|
| Baseline | Threshold rules on `score`, `Δscore_20`, `high_pair_count` | Interpretable Operator dial |
| Batch | sklearn `HistGradientBoostingClassifier` / logistic on engineered PCS deltas | Strong tabular baseline |
| Batch+ | LightGBM on same features + pair-count interactions | If sklearn underfits |
| Online | River ADWIN / Page-Hinkley on `score` and `max_abs` streams | Drift alarm without labels |
| Explicit non-goal | LLM price prediction, new Ollama pulls | Forbidden |

### Step 4 — Success metrics (“when to re-weight”) — Day 8–10

Primary (decision quality):

1. **Precision @ alert** — of re-weight alerts, fraction followed by material OA-DD improvement or avoidance of insolvency in next H days vs hold  
2. **Alert lead time** — median days before PCS leaves [60,90] or before insolvency event  
3. **False alarm rate** — alerts while book stays solvent and mid-band  

Secondary:

4. Brier / AUC on binary label (report, don’t optimize alone)  
5. Stability across books (Indigo/Teal/Copper/Slate + Orange/Blue/Red/Mango/Rust)  
6. Drift detector agreement with batch model (≥X% overlap)

**Done when:** Operator can set a dial (e.g. alert if P(reweight) > 0.6 **or** ADWIN fires on max\|r\|) with documented false-alarm cost — not when a shiny model exists.

### Step 5 — Write-back + ticket — Day 10–12

- File results note: `ecosystem/docs/analysis/YYYY-MM-DD-dimension-b-reweight-spike-results.md`
- Open ticket under `ecosystem/docs/tickets/` (P1): implement daily_job hook or Operator dashboard strip only after metrics clear
- **Do not** auto-mutate books in Wv2 from the spike

---

## 5. Stretch — how B unlocks C (pointer only)

Dimension **C** (non-trend / options+swing sleeves) needs a **correlation budget** and a **regime clock**:

- B’s mid-band PCS gate + re-weight detector tells C *when the trend sleeve is crowded / co-moving* so capital can tilt to mean-reversion or options overlays without guessing.
- Pair-level `high_pairs` + max\|r\| path become constraints for C book construction (avoid stacking another SMH/XLK clone).
- Drift alarms become the trigger to *evaluate* C sleeves — not to invent C strategies in this spike.

No C build in this pass.

---

## 6. Host gaps / unblock

1. Re-dispatch executor **with** `machineId=ef709a5e-51b1-4c4b-9154-d3935ef25f91` (sawtooth-ai) **or** parent runs export + pastes counts.  
2. Confirm ADR-007 path + daily_job schedule for PCS snapshots (history depth is the ML bottleneck).  
3. Live-confirm Indigo–Slate PCS 411–414 vs CoS claims (still UNCONFIRMED on box).  
4. Parent: copy this note onto host `ecosystem/docs/analysis/` if box mirror is not synced.

---

## 7. Open questions for John

1. Confirm PCS 60–90 = **raw strip score** (recommended) vs diversification proxy.  
2. Re-weight action preferred: **membership swap** (Mode C style), **risk_scale only**, or **both**?  
3. Label horizon H: 20 vs 60 trading days for “material OA DD”?  
4. Which portfolio cohort for v1 panel: Mode C lab only (411–414 + solvent parents) vs all WUT books with ≥30 snapshots?  
5. Who owns the Python spike week: John solo, Forensics+John, or external?

---

## 8. What this executor did / did not do

**Did:** Inventory box ecosystem docs + cloud-agent WUT extracts (scorer, snapshot model, schema, UI); clarify PCS gate conflict with formula reconstruction; draft P0 spike; write this analysis note on box.  
**Did not:** Access sawtooth-ai; run Forensics/rails jobs; pull Ollama models; mutate Wv2; claim live PCS numbers; deep-build Dimension C.
