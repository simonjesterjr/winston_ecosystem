# Ticket: Loop B — 60d forward OA/Edge label pipeline + scoreboard feed

**Status:** Proposed  
**Priority:** P1  
**Date:** 2026-09-21  
**Owner:** Forensics (export) · ML/spike owner (labels) · CoS (doctrine dial)  
**DoD:** Exporter writes PCS-feature + forward-label rows for Wv2-promoted cohort; `fwd_20d` live now; `fwd_60d` when snapshot depth allows; Edge window label stubbed or shipped; Operator scoreboard path documented — **no auto re-weight / no Wv2 mutate**  
**Analysis:** [`../analysis/2026-09-21-loop-b-60d-forward-labels-feature-table.md`](../analysis/2026-09-21-loop-b-60d-forward-labels-feature-table.md)  
**Seed:** [`../analysis/2026-09-21-loop-b-60d-forward-labels-seed.json`](../analysis/2026-09-21-loop-b-60d-forward-labels-seed.json)  
**Prior:** [`../analysis/2026-09-20-loop-b-pcs-vs-oa-mint-yellow-walnut.md`](../analysis/2026-09-20-loop-b-pcs-vs-oa-mint-yellow-walnut.md) · [`../analysis/2026-09-20-loop-eng-dimension-b-portfolio-design-spike.md`](../analysis/2026-09-20-loop-eng-dimension-b-portfolio-design-spike.md) · Edge scoreboard [`2026-09-11-measuring-edge-scoreboard.md`](2026-09-11-measuring-edge-scoreboard.md)

## Problem

Dimension B cannot test “high PCS / corr regime → worse Turtle OA?” or “when to re-weight” without **forward labels** joined to PCS snapshots. Full-horizon PBR OA/Edge are proxies only. Forensics 2026-09-20 pack explicitly flagged **60d forward labels missing**.

Host pull 2026-09-20 overnight: true `fwd_60d` blocked by **PCS history depth** (snaps from ~2026-07-11; PBR ends ~2026-09-18 → &lt;60 trading days after first snap). Mode C books 411–414 have only **3** `pbr`-sourced snaps.

## Scope

1. **Daily PCS depth** — ensure `daily_job` writes corr_v2 for Mode C pids (411–414) and parents; document backfill options if membership stable.  
2. **Exporter (read-only)** — JSONL/parquet panel: snapshot features + `fwd_20d_oa*` now; `fwd_60d_oa*` when `available_td ≥ 60`.  
3. **Edge window label** — lot R in `(t, t+H]` using Edge v1 persist (`edge_r` / lot timeline); defer if Phase 2 E-ratio still in flight.  
4. **Scoreboard feed** — file under `ecosystem/data/dimension_b/` (create when first export lands) + link from analysis; optional WUT strip later (not this ticket’s UI DoD).  
5. **Doctrine dial** — consume stubs from analysis §5; **human-only** membership recommendations.

## Non-goals

- Auto re-weight / Wv2 book mutate  
- Quiver rebalance mixed labels  
- A-track TS+IBKR invent work  
- New Ollama models / GPU training  
- ADR (wait for John lock on thresholds)

## Acceptance

- [ ] Mode C 411–414 appear on daily corr_v2 snap stream (or explicit blocker filed)  
- [ ] Repeatable host runner dumps feature+label panel for cohort in seed JSON  
- [ ] `fwd_20d` non-null for books with equity∩PCS overlap ≥20 td  
- [ ] `fwd_60d` column present; null with machine-readable `gap_reason` until depth ok  
- [ ] Analysis note updated with first automated export (date stamp)  
- [ ] No promote-screen / Mode C compile decisions mutated by this ticket

## Progress

- **2026-09-21 overnight:** Spec + seed + doctrine sketch filed; ticket opened.
- **2026-09-21/22 overnight refresh:** Re-pulled corr_v2 depth + interim fwd labels ([analysis](../analysis/2026-09-22-loop-b-overnight-pcs-depth-midband.md) · [JSON](../analysis/2026-09-22-loop-b-overnight-refresh.json)). True `fwd_60d` still blocked (max avail **46 td**; calendar-only 60td from Red-first ≈ **2026-10-02** + equity coverage). Mode C 411–414 still **pbr-only** (Teal n=3→4 via pbr 2026-09-21). Mid-band [60,72] hold reinforced (Teal PCS 64.88 / Edge_R 17.10; #727 Edge_R 17.70). No ranking re-order. Acceptance checkboxes unchanged.
- **2026-09-22/23 overnight refresh:** Re-pulled corr_v2 depth + interim fwd labels ([analysis](../analysis/2026-09-23-loop-b-overnight-pcs-depth-midband.md) · [JSON](../analysis/2026-09-23-loop-b-overnight-refresh.json)). True `fwd_60d` still blocked (max avail **46 td**; calendar depth Red-first→today **53 td**; calendar-only 60td ≈ **2026-10-02** + equity coverage). Mode C 411–414 still **pbr-only**. Mid-band [60,72] hold reinforced (Teal PCS 64.88 / Edge_R 17.10). Parents +1 daily_job to 2026-09-22. No ranking re-order. Lab note (non-invent): Orange #771 failed same 4-byte RangeError as Teal heat-ON — no requeue. Acceptance checkboxes unchanged.
- **2026-09-23/24 overnight refresh:** Re-pulled corr_v2 depth + interim fwd labels ([analysis](../analysis/2026-09-24-loop-b-overnight-pcs-depth-midband.md) · [JSON](../analysis/2026-09-24-loop-b-overnight-refresh.json)). True `fwd_60d` still blocked (max avail **46 td**; calendar depth Red-first→today **54 td**; calendar-only 60td ≈ **2026-10-02** + equity coverage). Mode C 411–414 still **pbr-only**. Mid-band [60,72] hold reinforced (Teal PCS 64.88 / Edge_R 17.10). Parents +1 daily_job to 2026-09-23. No ranking re-order. Lab note (non-invent): Teal #767–#770 still failed+operator_stop; Orange #771 **completed** 2026-09-23 10:29 MT — no Teal requeue. Acceptance checkboxes unchanged.

## Overnight progress (2026-09-24 ~22:00 MT)

I refreshed PCS/corr/mid-band evidence in [`../analysis/2026-09-24-overnight-loop-b-pcs-corr-midband.md`](../analysis/2026-09-24-overnight-loop-b-pcs-corr-midband.md). `unlock_fwd_60d` still false (max forward depth still 46 td on Blue/Orange). Mode C pids 411–414 still pbr-only (no `daily_job` corr_v2). Calendar depth from Red-first → container-today = **55 td**; calendar-only 60 td still ≈ **2026-10-02**. Interim `fwd_20d` reinforced on solvent parents.
