# Loop B — 60d forward-label feature table (spec + seed)

**Date:** 2026-09-21 (filed overnight 2026-09-20 ~22:10 MT, America/Denver)  
**Track:** Loop Engineering **Dimension B** — portfolio design (PCS / corr / re-weight)  
**Status:** Spec + seed evidence. **No auto re-weight. No ADR.**  
**Seed JSON:** [`2026-09-21-loop-b-60d-forward-labels-seed.json`](2026-09-21-loop-b-60d-forward-labels-seed.json)  
**Prior evidence:** [`2026-09-20-loop-b-pcs-vs-oa-mint-yellow-walnut.md`](2026-09-20-loop-b-pcs-vs-oa-mint-yellow-walnut.md) · [`2026-09-20-loop-eng-dimension-b-portfolio-design-spike.md`](2026-09-20-loop-eng-dimension-b-portfolio-design-spike.md)  
**Ticket:** [`../tickets/2026-09-21-loop-b-60d-forward-label-pipeline.md`](../tickets/2026-09-21-loop-b-60d-forward-label-pipeline.md)

---

## 1. Purpose

Close the Forensics gap: **60d forward OA / Edge labels** attached to PCS snapshot features for the **Wv2-promoted (paper) cohort**, so re-weight doctrine can be evidence-tested before any real or automated membership change.

This note defines the **feature table**, files **seed rows** from live WUT (read-only), and sketches **re-weight doctrine** (not ADR).

---

## 2. Column dictionary (v1)

| Column | Type | Source | Notes |
|--------|------|--------|-------|
| `book` | string | portfolio name/color | Walnut, Mint, … Slate |
| `portfolio_id` | int | WUT `portfolios.id` | |
| `cohort` | enum | desk tag | `mode_c_wv2_promoted` · `mode_c_parent_solvent` · `promote_screen_hold` · `diversifier_contrast` |
| `feature_as_of` | date | PCS `as_of_date` | Features only from snaps with `as_of_date ≤ t` |
| `pcs` / `pcs_window` | float / string | `portfolio_correlation_snapshots.score` · `corr_v2` | Raw strip score (ADR-007) |
| `mean_abs_r` | float | snapshot | |
| `max_abs_r` | float | snapshot | **Dominates** corr_v2 |
| `high_pair_count` | int | snapshot | \|r\| > 0.70 |
| `delta_pcs_20d` | float | derived | `pcs(t) − pcs(t−20d)` |
| `delta_max_r_20d` | float | derived | |
| `delta_pcs_since_first` | float | derived | Collapse detector on short history |
| `days_outside_60_90` | int | derived | Count of snaps outside Mode C compile gate |
| `regime_tag` | enum | derived | `mid_band_corridor` [60,72] · `high_mid_band` (72,90] · `ultra_high_pcs` >90 · `below_gate` [40,60) · `low_pcs_cluster` <40 |
| `fwd_60d_oa_pct` | float \| null | **label** | OA equity change over **60 trading days** after `feature_as_of` |
| `fwd_60d_oa_dd_pct` | float \| null | **label** | Peak-to-trough DD inside that window |
| `fwd_60d_edge_r` | float \| null | **label** | Mean lot R in window (gap tonight) |
| `fwd_20d_oa_pct` | float \| null | interim label | Usable while 60d depth builds |
| `fwd_available_td` / `fwd_available_oa_pct` | int / float | interim | Max forward ≤60 td currently sliceable |
| `pbr_full_oa_pct` / `pbr_full_edge_r` | float | PBR columns | **Non-forward proxies** — full-horizon stamp only |
| `best_pbr_id` / `pbr_cell` | int / string | lab cell | Prefer `leap_fulfillment=all`, rank by OA |
| `membership_recommendation_stub` | enum | stub only | `hold` · `hold_diversifier_watch` · `watch` · `reweight_candidate` — **human gate** |
| `label_kind` / `label_caveat` | string | meta | Leakage + proxy warnings |

**Embargo:** features at `t` may only use snapshots with `as_of_date ≤ t`; outcomes from `(t, t+H]` on equity/lots.

---

## 3. How labels are (will be) computed

### 3.1 Target (pipeline)

1. For each `(portfolio_id, feature_as_of)` with corr_v2 snap  
2. Take completed LEAP-preferred PBR whose membership matches book lineage at `t` (or successor stamp)  
3. Slice `option_aware_equity_history` from first bar `≥ t` for **60 trading days** → `fwd_60d_oa_pct`, `fwd_60d_oa_dd_pct`  
4. Attribute closed lots with exit in `(t, t+60td]` → `fwd_60d_edge_r` (Edge v1 / ADR-015)  
5. Write scoreboard rows (parquet/JSON under `ecosystem/data/dimension_b/` when created)

### 3.2 Seed method tonight (read-only)

- Live WUT via `./bin/compose exec -T winston_unit_test bin/rails runner`  
- Feature panel from `PortfolioCorrelationSnapshot` (`methodology_version = corr_v2`)  
- Forward OA attempted from best-cell `option_aware_equity_history` at **first available snap** (maximizes forward under current depth)  
- Full-horizon `option_aware_total_return` + `edge_r` kept as **proxies**, clearly marked

### 3.3 Structural gap (why `fwd_60d_*` is null)

| Fact | Implication |
|------|-------------|
| Oldest PCS daily_job snaps ≈ **2026-07-11** (Red); Mint/Yellow **2026-07-22**; Walnut **2026-08-12** | Short panel |
| Best LEAP PBRs end ≈ **2026-09-17/18** | ≤ **~44–46 trading days** after first snap — **not 60** |
| Mode C Indigo/Teal/Copper/Slate: **n=3** snaps, source=`pbr`, max as_of **2026-09-19** | No daily_job depth yet; forward slice impossible |
| Walnut share PBRs #496/#498 end **2026-07-21** | **Before** first Walnut PCS snap → no equity∩PCS overlap |

**Interim:** use `fwd_20d_*` + `fwd_available_*` (37–46 td) until PCS history deepens **or** historical PCS is backfilled.

---

## 4. Seed scoreboard (2026-09-20 host pull)

| Book | pid | PCS first → now | ΔPCS | avail td | avail OA % | fwd20 OA % | full OA % | Edge_R | stub |
|------|-----|-----------------|------|----------|------------|------------|-----------|--------|------|
| Teal | 412 | 66.41 → 64.86 | −1.55 | — | — | — | **+19992** | **17.10** | hold |
| Copper | 413 | 60.91 → 60.90 | −0.01 | — | — | — | +15931 | 15.67 | hold |
| Slate | 414 | 60.83 → 60.83 | 0 | — | — | — | +15749 | 14.84 | hold |
| Blue | 7 | 76.15 → 66.41 | −9.74 | 46 | +1.68 | +1.31 | +11875 | 7.80 | hold_diversifier_watch |
| Orange | 35 | 68.34 → **24.87** | **−43.47** | 46 | +4.00 | +0.19 | +10374 | 5.60 | reweight_candidate |
| Indigo | 411 | 71.44 → 72.29 | +0.85 | — | — | — | +8979 | 10.26 | hold |
| Red | 6 | 73.01 → 71.48 | −1.53 | 44 | +4.56 | +1.94 | +8109 | 8.44 | hold_diversifier_watch |
| Mango | 65 | 71.30 → 64.15 | −7.15 | 44 | +5.14 | +2.04 | +2795 | 4.13 | hold |
| Walnut | 223 | 91.86 → **79.10** | −12.76 | — | — | — | (share only) | — | watch |
| Mint | 110 | 91.21 → **44.01** | **−47.2** | 37 | 0.0 | 0.0 | **−263** | 3.79 | reweight_candidate |
| Yellow | 111 | 73.52 → **38.71** | **−34.81** | 37 | 0.0 | 0.0 | **−286** | −0.19 | reweight_candidate |
| Rust | 66 | 77.25 → **22.99** | **−54.26** | 44 | 0.0 | 0.0 | **−311** | −3.38 | reweight_candidate |

Raw rows: seed JSON.

---

## 5. Re-weight doctrine sketch (not ADR)

**Principle:** Re-weight = **membership** change (Mode C style compile/swap), not merely `risk_scale`. Doctrine before real capital; paper cohort first. **No automation** until precision@alert is known.

### 5.1 Triggers (OR — draft)

1. **Corr regime shift**  
   - `delta_pcs_20d ≤ −15` **or** `delta_pcs_since_first ≤ −20` **or** `high_pair_count` jumps ≥2  
   - **or** PCS exits Mode C gate [60, 90] for ≥5 consecutive daily snaps  
2. **Sleeve non-performance (60d look)**  
   - Once labels exist: `fwd_60d_oa_pct` materially worse than cohort median **or** insolvency / cash ruin in window  
   - Interim: full-horizon OA < −50% **or** available-forward OA ≤ 0 while peers print positive  

Either trigger alone → **`reweight_candidate`** (human). Both → stronger candidate.

### 5.2 Mid-band PCS corridor hypothesis

- **Hold preference** when PCS ∈ **[60, 72]** (`mid_band_corridor`) and sleeve is solvent on OA — Teal #743 best OA sits here.  
- **(72, 90]** = `high_mid_band` — allowed by compile gate; treat as **hold_diversifier_watch** until 60d labels show they compound (Walnut is the clean diversifier geometry; LEAP cell still missing).  
- **Do not maximize PCS.** High PCS ≠ Turtle alpha (Walnut vs Orange paradox, 2026-09-20 pack).

### 5.3 Walnut vs Mint/Yellow (narrative lock)

| Book | Live PCS | max\|r\| | Read |
|------|----------|---------|------|
| **Walnut** | **79.1** | 0.39 | **True diversifier.** Not a Mode-C LEAP compounder on available PBRs. Membership = diversifier sleeve, not “non-corr Mint/Yellow twin.” |
| Mint | 44.0 | 0.89 | **Not** high-PCS. Mean\|r\| lore lied; max\|r\|-first corr_v2 fails gate. Insolvent LEAP → reweight/new-book path (already Mode C replacements). |
| Yellow | 38.7 | ~1.0 | Same as Mint. |

**Stop grouping Mint/Yellow with Walnut as “non-corr.”**

### 5.4 Orange paradox (keep explicit)

Orange PCS collapsed **68 → 25** (Δ −43) yet full-horizon LEAP OA remains huge and short available-forward OA still ≥0.  
→ PCS collapse alone is **not** an automatic kill if OA/Edge stay strong — but it **is** a membership **watch** because compile gate and pair geometry have left the Mode C band. Doctrine: flag `reweight_candidate` for **geometry**, Operator decides keep-for-alpha vs rebuild-for-gate.

### 5.5 Non-goals (this sketch)

- Auto mutate Wv2 books  
- Quiver rebalance labels mixed into Turtle panel  
- LLM price prediction / new Ollama pulls  
- ADR until John locks trigger thresholds + action (membership vs risk_scale vs both)

---

## 6. Pipeline next (ticket)

1. **Backfill or extend** corr_v2 daily_job so Mode C pids 411–414 get daily snaps; optionally reconstruct historical snaps where membership stable.  
2. Implement exporter → `fwd_20d` scoreboard now; promote to `fwd_60d` when depth ≥60 td post-as_of.  
3. Lot-window Edge_R label.  
4. Stamp Walnut LEAP TS75 r01/r02 for apples-to-apples diversifier OA cell (separate promote/PBR ops ask — not invented A-track).  
5. Operator dial: alert if stub=`reweight_candidate` for ≥N days; measure precision later (spike §4).

---

## 7. What I did / did not do

**Did:** Read Loop B packs + litmus + tickets INDEX; read-only WUT PCS depth + PBR equity probes; design column dict; seed JSON + forward interim labels; doctrine sketch; open pipeline ticket.  
**Did not:** Mutate promote decisions; pull Ollama models; invent A-track TS+IBKR work; file ADR; message John; build Loop C.

---

## 8. Open for morning report (no overnight blocker)

1. Confirm cohort v1 = Wv2-promoted paper + Mode C parents + contrast (as seeded) vs Mode C–only.  
2. Prefer **membership** vs risk_scale when stub fires?  
3. Accept **20d interim** scoreboard until 60d depth exists?  
4. Walnut LEAP stamp priority vs leave as diversifier-only?
