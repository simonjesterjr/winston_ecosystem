# Loop B overnight — PCS depth + mid-band hold (refresh)

**Date:** 2026-09-25 ~21:55–22:15 MT (America/Denver)  
**Track:** Loop Engineering **Dimension B** — portfolio design (Portfolio Construction Score (PCS) / correlation / re-weight)  
**Status:** Evidence refresh. **No auto re-weight. No Architecture Decision Record (ADR).**  
**Refresh JSON:** [`2026-09-25-loop-b-overnight-refresh.json`](2026-09-25-loop-b-overnight-refresh.json)  
**Parameterized Backtest Run (PBR) / Sidekiq glance:** [`2026-09-25-loop-b-overnight-pbr-sidekiq-glance.json`](2026-09-25-loop-b-overnight-pbr-sidekiq-glance.json)  
**Runner:** [`_loop_b_overnight_refresh_2026-09-25.rb`](_loop_b_overnight_refresh_2026-09-25.rb)  
**Prior:** [`2026-09-24-overnight-loop-b-pcs-corr-midband.md`](2026-09-24-overnight-loop-b-pcs-corr-midband.md) · [`2026-09-24-loop-b-overnight-pcs-depth-midband.md`](2026-09-24-loop-b-overnight-pcs-depth-midband.md) · [`2026-09-21-loop-b-60d-forward-labels-feature-table.md`](2026-09-21-loop-b-60d-forward-labels-feature-table.md)  
**Ticket:** [`../tickets/2026-09-21-loop-b-60d-forward-label-pipeline.md`](../tickets/2026-09-21-loop-b-60d-forward-label-pipeline.md)

---

## 1. Questions answered tonight

| Question | Answer (evidence) |
|----------|-------------------|
| Unlock true `fwd_60d` yet? | **No.** `unlock_fwd_60d=false`. Max available forward still **46 trading days (td)** (Blue/Orange). Calendar depth from Red-first snap → container-today = **55 td** (unchanged vs last night: container `Date.today` is **2026-09-26** UTC Saturday, so the weekend adds no trading day). Calendar-only 60 td from that first snap still ≈ **2026-10-02**, **and** PBR Option-Aware (OA) equity must cover the window. |
| Reinforce interim `fwd_20d`? | **Yes.** Solvent parents still print usable `fwd_20d` / available-forward OA (Red +1.94%, Blue +1.31%, Mango +2.04%; magnitudes match prior refresh within rounding). Mode C books still lack depth for interim labels (Teal avail td=1 only). |
| Mid-band [60,72] membership-first still unlocked? | **Yes — reinforced.** Teal PCS **64.89**, Edge_R **17.10** on #743; #727 Edge_R **17.70** intact. Copper **60.89** / Edge **15.67**; Slate **60.83** / Edge **14.84**. Red/Blue/Mango mid-band + solvent OA → stub `hold`. High-pair count still **0** on mid-band books (mean_abs_r ~0.17–0.29). |
| New actionable ranking for Winston v2 (Wv2)-promoted? | **No material re-rank.** Mode C PCS flat vs last night (Teal 64.89; Indigo 72.25; Copper 60.89; Slate 60.83). Collapse stubs unchanged (Mint/Yellow/Rust/Orange = `reweight_candidate`; Walnut = `watch`; Indigo = `hold_diversifier_watch`). |

---

## 2. PCS depth / daily_job gap (Mode C)

| Book | n snaps | sources | latest as_of | latest src | PCS | Δ since first |
|------|---------|---------|--------------|------------|-----|---------------|
| Indigo | 4 | pbr:4 | 2026-09-24 | pbr | **72.25** | +0.81 |
| Teal | 5 | pbr:5 | 2026-09-24 | pbr | **64.89** | −1.52 |
| Copper | 4 | pbr:4 | 2026-09-24 | pbr | **60.89** | −0.02 |
| Slate | 3 | pbr:3 | 2026-09-19 | pbr | 60.83 | 0.00 |

Parents (Red/Blue/Mango/Mint/Yellow/Rust/Walnut/Orange) advanced **+1 daily_job** snap to **2026-09-25**. PCS day-over-day flat vs last night within rounding (Red **71.50**, Blue **66.39**, Orange **24.86** now latest src=`daily_job`).

**Pipeline blocker unchanged:** Mode C portfolio ids (pids) 411–414 still **not** on `daily_job` corr_v2 stream (ticket acceptance item open). Slate still stalled at 2026-09-19 pbr-only; Indigo/Teal/Copper still last snapped 2026-09-24 pbr-only (no Friday Mode C pbr advance overnight).

**Corr glance (mid-band):** high_pair_count=0 across Red/Blue/Mango/Teal/Copper/Slate. Blue `delta_pcs_20d` **−9.76**, Mango **−7.15**, Red **−1.51** — corridor membership holds; no new collapse signal overnight.

---

## 3. Forward-label status (refresh vs prior)

| Book | fwd20 OA% | avail td | avail OA% | fwd60 | stub |
|------|-----------|----------|-----------|-------|------|
| Red | +1.94 | 44 | +4.56 | insufficient (have=44) | hold |
| Blue | +1.31 | 46 | +1.68 | insufficient (have=46) | hold |
| Mango | +2.04 | 44 | +5.14 | insufficient (have=44) | hold |
| Orange | +0.19 | 46 | +4.00 | insufficient (have=46) | reweight_candidate |
| Mint | 0.0 | 37 | 0.0 | insufficient (have=37) | reweight_candidate |
| Yellow | 0.0 | 37 | 0.0 | insufficient (have=37) | reweight_candidate |
| Rust | 0.0 | 44 | 0.0 | insufficient (have=44) | reweight_candidate |
| Walnut | — | — | — | no_equity∩PCS | watch |
| Teal | insuff | 1 | +0.10 | insufficient (have=1) | hold |
| Copper/Slate/Indigo | — | ≤0 | — | insufficient | hold / hold_diversifier_watch (Indigo @72.25) |

**Do not maximize PCS.** Orange paradox intact: PCS **24.86** with full OA still huge and short-forward OA ≥0 → geometry `reweight_candidate`.

---

## 4. Lab / PBR read-only (not Loop B invent)

| PBR | Book | Status | Note |
|-----|------|--------|------|
| #743 / #727 | Teal | completed | Mid-band Edge anchors unchanged (17.10 / 17.70) |
| #767–#770 | Teal heat-ON | **failed** | Still failed; **do not requeue** ([ticket](../tickets/2026-09-22-wut-teal-heat-on-rangeerror-4byte-int.md)) |
| #771 | Orange | **completed** | Edge_R **−0.1458**, OA ≈598 — unchanged since 2026-09-23 |
| #788–#795 | shares TS75 mod-heat bakeoff | completed | Best Copper **#794** Edge_R **0.311** (Mode D paper book #1585 lineage; fingerprint adopt still Blocked — not a new stamp tonight) |

Winston Unit Test (WUT) Sidekiq: `pbr_in_retry=0`; RetrySet size=31 (non-PBR noise). `expected_returns` queue ~86k — **ops glance only**, not my claim of host Definition of Done (DoD).

Compose glance (not DoD claim): Rails monoliths + Sidekiq still **Up … (starting)** while Redis/Postgreses/Ollama stay **(healthy)** — specimen still matches [`../tickets/2026-09-24-compose-container-meaningful-status.md`](../tickets/2026-09-24-compose-container-meaningful-status.md).

---

## 5. Ticket triage (overnight — propose only; **do not archive**)

I consulted [`../tickets/INDEX.md`](../tickets/INDEX.md). Last night’s Done clutter (flatten-roll / min-ATR / bakeoffs / eod-pending) is **already off** the active INDEX (files under `archive/`). New hygiene tonight is Capital-fit duplication + Mode D Blocked stack.

### 5a. Discard / archive **candidates** (Operator morning approval required)

| File | Why propose discard/archive |
|------|-----------------------------|
| [`2026-09-24-desk-capital-fit-justification-check.md`](../tickets/2026-09-24-desk-capital-fit-justification-check.md) | **INDEX still lists P0 Proposed**, but `archive/2026-09-24-desk-capital-fit-justification-check.md` already says **Done (2026-09-24)** with journal **2103**. Morning: confirm browser verify landed; if yes, drop active row + keep archive Done only. **Do not archive tonight.** |
| [`2026-09-10-signal-inspect-focus-chart-browser-verify.md`](../tickets/2026-09-10-signal-inspect-focus-chart-browser-verify.md) | P3 browser-verify, ~15 days Proposed, **not in INDEX** — park/discard unless Operator still wants it. |
| [`2026-09-01-fulfillment-packaging-policy-ops-ui.md`](../tickets/2026-09-01-fulfillment-packaging-policy-ops-ui.md) | 24-day-old P2 Proposed; jsonb store already on OP (INDEX note) — demote/park if no Operator ask this cycle. |
| [`2026-09-09-wut-dataset-dm-sync-dead-jobs.md`](../tickets/2026-09-09-wut-dataset-dm-sync-dead-jobs.md) · [`2026-09-10-dar-wq-open-lots-unit-risk.md`](../tickets/2026-09-10-dar-wq-open-lots-unit-risk.md) · [`2026-09-10-unit-risk-vs-parked-gtc.md`](../tickets/2026-09-10-unit-risk-vs-parked-gtc.md) | Stale P2/P3 Proposed (≥15d) — discard or explicit defer at next Loop review. |

### 5b. Prioritize next (morning)

| Priority | File | Why |
|----------|------|-----|
| **P0** | [`2026-09-21-wut-heat-on-rst-portfolio-limit-bypass.md`](../tickets/2026-09-21-wut-heat-on-rst-portfolio-limit-bypass.md) | Capital-safety heat-ON bypass — keep In progress until WUT #55 path is proven closed. |
| **P0 reconcile** | [`2026-09-24-desk-capital-fit-justification-check.md`](../tickets/2026-09-24-desk-capital-fit-justification-check.md) | Active Proposed vs archive Done — Operator confirms Done or re-opens verify. |
| **P1 Lane A** | [`2026-09-25-copper-1585-fingerprint-importer-adopt.md`](../tickets/2026-09-25-copper-1585-fingerprint-importer-adopt.md) + [`…-paper-send.md`](../tickets/2026-09-24-mode-d-phase-2-paper-send.md) | Fingerprint named `d627cd79…`; adopt **stopped** on engaged draft journal **2105** before TST clear / POST. CLI seed on ticket. Paper Send remains Blocked. |
| **P1** | [`2026-09-25-mode-d-uat-resume.md`](../tickets/2026-09-25-mode-d-uat-resume.md) | Resume early next week after XLE flatten fills — calendar reminder. |
| **P1 Operator** | [`2026-09-24-teal-indigo-usdu-overdraft.md`](../tickets/2026-09-24-teal-indigo-usdu-overdraft.md) | Teal 1584 / Indigo 1583 USDU lots still need flatten-or-fund. |
| **P1 Lane B + CLI seed** | [`2026-09-24-compose-container-meaningful-status.md`](../tickets/2026-09-24-compose-container-meaningful-status.md) | Reconfirmed Up-N-days `(starting)` while serving — host smoke + honest status vocab. |
| **P1 Lane B** | [`2026-09-22-wut-teal-heat-on-rangeerror-4byte-int.md`](../tickets/2026-09-22-wut-teal-heat-on-rangeerror-4byte-int.md) | Code fix landed; Teal #767–#770 still failed — **Operator restamp decision** (not overnight invent). |
| **P1** | [`2026-09-15-bg-ibkr-opt-order-intent-prove.md`](../tickets/2026-09-15-bg-ibkr-opt-order-intent-prove.md) | Still **In progress**. Long-call print still open — morning Account Management (AM) grill, not overnight invent. |
| **P1 Lane A plan** | [`2026-09-21-loop-b-60d-forward-label-pipeline.md`](../tickets/2026-09-21-loop-b-60d-forward-label-pipeline.md) | Unlock = wire Mode C 411–414 onto `daily_job` corr_v2; keep `fwd_20d` interim. |
| **P1 reminder Oct 1** | [`2026-09-21-packaging-sub100-share-vs-option-m-band.md`](../tickets/2026-09-21-packaging-sub100-share-vs-option-m-band.md) | Packaging M-band review reminder — do not invent stamps overnight. |

**Not inventing:** A-track Trading Strategy (TS) + Interactive Brokers (IBKR) work beyond Mode D fingerprint adopt; new PBR stamps; Teal requeue; ticket archives; live `POST /internal/portfolios`.

---

## 6. What I did / did not

**Did:** Confirm GPU idle (ollama resident only); re-read INDEX + Loop B trail; read-only WUT refresh (PCS depth, sources, interim fwd labels, Edge_R, corr mid-band); read-only PBR + Sidekiq glance; file refresh JSON + this note + ticket progress pointers; Jev verify on mid-band / Mode C daily_job + Capital-fit INDEX claims; local commit (+ push if desk pattern).  
**Did not:** Mutate promote decisions; invent A-track stamps; pull Ollama / GPU training; open ADR; start Loop C (B was substantive); archive tickets; requeue Teal; message John; claim Ops host DoD; call importer POST.

---

## 7. Open next (morning digest)

1. **INDEX:** Capital-fit P0 Proposed vs archive Done — reconcile after Operator confirm.  
2. **Pipeline:** wire Mode C 411–414 onto `daily_job` corr_v2 (still the unlock for Mode C forward labels); Slate still 2026-09-19.  
3. **fwd_60d:** earliest *calendar* depth from Red-first ≈ **2026-10-02**; still need PBR equity covering as_of+60. Keep **fwd_20d interim**.  
4. **Mode D:** journal 2105 engagement blocked importer adopt on #1585 — Operator clears path (no SQL fingerprint); then paper Send gate.  
5. **USDU / Capital fit:** Operator flatten-or-fund Teal/Indigo; Capital-fit Done reconcile.  
6. **RangeError:** Teal #767–#770 still stopped — Operator decides Teal restamp.  
7. **IBKR OPT prove:** still open on long-call print.  
8. **Triage proposals** in §5 — archive/discard only after Operator approval.

---

## 8. Jev judgment (overnight)

| # | Claim (abbrev) | Verdict | Conf |
|---|----------------|---------|------|
| 1 | Teal PCS mid-band ~64.89 + #743 Edge_R ~17.10 → hold stub; Mode C still pbr-only | **verified** | 1.00 |
| 2 | Capital-fit P0 still Proposed in active INDEX while archive copy is Done (2026-09-24) → morning reconcile | **verified** | 1.00 |

Triage/analysis excerpt **screen PASS** (injection 0.07 / substance 0.99 / relevance 0.98).  
Ran via `scripts/jev-desk-helpers.sh verify` + `screen` (jev 0.2.x / jev-1.13.0 via typesafe).

