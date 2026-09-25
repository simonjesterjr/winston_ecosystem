# Loop B overnight — PCS / corr / mid-band refresh + triage

**Date:** 2026-09-24 ~21:55–22:10 MT (America/Denver)  
**Track:** Loop Engineering **Dimension B** — portfolio design (Portfolio Construction Score (PCS) / correlation / re-weight)  
**Status:** Evidence refresh. **No auto re-weight. No Architecture Decision Record (ADR).**  
**Refresh JSON:** [`2026-09-24-overnight-loop-b-refresh.json`](2026-09-24-overnight-loop-b-refresh.json)  
**Parameterized Backtest Run (PBR) / Sidekiq glance:** [`2026-09-24-overnight-loop-b-pbr-sidekiq-glance.json`](2026-09-24-overnight-loop-b-pbr-sidekiq-glance.json)  
**Runner:** [`_loop_b_overnight_refresh_2026-09-24.rb`](_loop_b_overnight_refresh_2026-09-24.rb)  
**Prior:** [`2026-09-24-loop-b-overnight-pcs-depth-midband.md`](2026-09-24-loop-b-overnight-pcs-depth-midband.md) · [`2026-09-23-loop-b-overnight-pcs-depth-midband.md`](2026-09-23-loop-b-overnight-pcs-depth-midband.md) · [`2026-09-21-loop-b-60d-forward-labels-feature-table.md`](2026-09-21-loop-b-60d-forward-labels-feature-table.md)  
**Ticket:** [`../tickets/2026-09-21-loop-b-60d-forward-label-pipeline.md`](../tickets/2026-09-21-loop-b-60d-forward-label-pipeline.md)

---

## 1. Questions answered tonight

| Question | Answer (evidence) |
|----------|-------------------|
| Unlock true `fwd_60d` yet? | **No.** `unlock_fwd_60d=false`. Max available forward still **46 trading days (td)** (Blue/Orange). Calendar depth from Red-first snap → container-today = **55 td** (was 54 last night); calendar-only 60 td from that first snap still ≈ **2026-10-02**, **and** PBR Option-Aware (OA) equity must cover the window. |
| Reinforce interim `fwd_20d`? | **Yes.** Solvent parents still print usable `fwd_20d` / available-forward OA (Red +1.94%, Blue +1.31%, Mango +2.04%; magnitudes match prior refresh within rounding). Mode C books still lack depth for interim labels (Teal avail td=1 only). |
| Mid-band [60,72] membership-first still unlocked? | **Yes — reinforced.** Teal PCS **64.89**, Edge_R **17.10** on #743; #727 Edge_R **17.70** intact. Copper **60.89** / Edge **15.67**; Slate **60.83** / Edge **14.84**. Red/Blue/Mango mid-band + solvent OA → stub `hold`. High-pair count still **0** on mid-band books (mean_abs_r ~0.17–0.29). |
| New actionable ranking for Winston v2 (Wv2)-promoted? | **No material re-rank.** Mode C PCS flat vs last night (Teal 64.89 vs 64.88; Indigo 72.25 vs 72.29, now with a fresh **pbr** snap @ 2026-09-24). Collapse stubs unchanged (Mint/Yellow/Rust/Orange = `reweight_candidate`; Walnut = `watch`; Indigo = `hold_diversifier_watch`). |

---

## 2. PCS depth / daily_job gap (Mode C)

| Book | n snaps | sources | latest as_of | latest src | PCS | Δ since first |
|------|---------|---------|--------------|------------|-----|---------------|
| Indigo | **4** | pbr:4 | **2026-09-24** | pbr | **72.25** | +0.81 |
| Teal | **5** | pbr:5 | **2026-09-24** | pbr | **64.89** | −1.52 |
| Copper | **4** | pbr:4 | **2026-09-24** | pbr | **60.89** | −0.02 |
| Slate | 3 | pbr:3 | 2026-09-19 | pbr | 60.83 | 0.00 |

Parents (Red/Blue/Mango/Mint/Yellow/Rust/Walnut/Orange) advanced **+1 daily_job** snap to **2026-09-24** (Blue latest src tonight = `pbr` @ 2026-09-24 with PCS **66.39**). PCS day-over-day within ±0.04 vs last night's refresh.

**Pipeline blocker unchanged:** Mode C portfolio ids (pids) 411–414 still **not** on `daily_job` corr_v2 stream (ticket acceptance item open). Slate still stalled at 2026-09-19 pbr-only.

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
| #788–#795 | shares TS75 mod-heat bakeoff | completed | Best Copper **#794** Edge_R **0.311** (ticket Done; Mode D paper book #1585 minted from #794 — not a new stamp tonight) |

Winston Unit Test (WUT) Sidekiq: `pbr_in_retry=0`; RetrySet size=29 (non-PBR noise). `expected_returns` queue ~86k — **ops glance only**, not my claim of host Definition of Done (DoD).

---

## 5. Ticket triage (overnight — propose only; **do not archive**)

I consulted [`../tickets/INDEX.md`](../tickets/INDEX.md) (working tree) and restored the accidentally deleted P0 Capital-fit ticket file from `HEAD`.

### INDEX hygiene I fixed tonight
- **P0** [`2026-09-24-desk-capital-fit-justification-check.md`](../tickets/2026-09-24-desk-capital-fit-justification-check.md) was **deleted from the working tree** and **missing from WT INDEX** while still on `origin/main` @ P0 Proposed. I restored the file and re-inserted the INDEX row. Morning: confirm no other intentional drop.

### 5a. Discard / archive **candidates** (Operator morning approval required)

| File | Why propose discard/archive |
|------|-----------------------------|
| [`2026-09-20-standard-call-flatten-roll-desk.md`](../tickets/2026-09-20-standard-call-flatten-roll-desk.md) | **Status already Done** — still listed in active INDEX. Move to `archive/` when Operator okays. |
| [`2026-09-22-min-atr-capital-consumption-guard.md`](../tickets/2026-09-22-min-atr-capital-consumption-guard.md) | **Status already Done** — still in active INDEX. Archive candidate (Capital Fit law landed; siblings are USDU + Justification check). |
| [`2026-09-24-shares-ts75-modified-heat-bakeoff.md`](../tickets/2026-09-24-shares-ts75-modified-heat-bakeoff.md) · [`2026-09-23-shares-only-ts75-vs-ts77-bakeoff.md`](../tickets/2026-09-23-shares-only-ts75-vs-ts77-bakeoff.md) | Both **Done** — still in active INDEX. Archive after Operator okays. |
| [`2026-09-17-eod-pending-15-human-confirm.md`](../tickets/2026-09-17-eod-pending-15-human-confirm.md) | Seven-day-old one-shot pending-draft list (2026-09-17). Likely stale — confirm pending count=0 or explicit defer, then archive. |
| [`2026-09-20-wut-standard-call-plan-b-parity.md`](../tickets/2026-09-20-wut-standard-call-plan-b-parity.md) | P3 “only if operator asks” — park/discard if no ask by next Loop review. |
| [`2026-09-11-fulfillment-desk-adapters-yield-browser-verify.md`](../tickets/2026-09-11-fulfillment-desk-adapters-yield-browser-verify.md) · [`2026-09-10-signal-inspect-first-paint-eval-card.md`](../tickets/2026-09-10-signal-inspect-first-paint-eval-card.md) | Stale P3 browser-verify chores (~13–14 days) — discard or demote unless Operator still wants them. |

### 5b. Prioritize next (morning)

| Priority | File | Why |
|----------|------|-----|
| **P0 Lane B** | [`2026-09-24-desk-capital-fit-justification-check.md`](../tickets/2026-09-24-desk-capital-fit-justification-check.md) | Browser-only Capital fit Justification verify — same-day intent from elevate; still Proposed / unchecked. |
| **P0** | [`2026-09-21-wut-heat-on-rst-portfolio-limit-bypass.md`](../tickets/2026-09-21-wut-heat-on-rst-portfolio-limit-bypass.md) | Capital-safety heat-ON bypass — keep In progress until WUT #55 path is proven closed. |
| **P1 Lane A** | [`2026-09-24-mode-d-phase-2.md`](../tickets/2026-09-24-mode-d-phase-2.md) + [`…-paper-send.md`](../tickets/2026-09-24-mode-d-phase-2-paper-send.md) | Desk walk / list / assignment done; **paper send Blocked** on null Trading Strategy fingerprint for Copper #1585 — Operator names fingerprint before any order. |
| **P1 Operator** | [`2026-09-24-teal-indigo-usdu-overdraft.md`](../tickets/2026-09-24-teal-indigo-usdu-overdraft.md) | Teal 1584 / Indigo 1583 USDU lots still need flatten-or-fund — blocks new longs while free cash negative. |
| **P1 Lane B + CLI seed** | [`2026-09-24-compose-container-meaningful-status.md`](../tickets/2026-09-24-compose-container-meaningful-status.md) | Reconfirmed Up-N-days `(starting)` while serving — host smoke + honest status vocab. |
| **P1 Lane B** | [`2026-09-22-wut-teal-heat-on-rangeerror-4byte-int.md`](../tickets/2026-09-22-wut-teal-heat-on-rangeerror-4byte-int.md) | Code fix landed; Teal #767–#770 still failed — **Operator restamp decision** (not overnight invent). #771 completed. |
| **P1** | [`2026-09-15-bg-ibkr-opt-order-intent-prove.md`](../tickets/2026-09-15-bg-ibkr-opt-order-intent-prove.md) | Still **In progress**. Long-call print still open (MD + strategy permission rejects on 2026-09-23 probes); covered-call Level 1 path is desk-episode context — morning Account Management (AM) grill, not overnight invent. |
| **P1 Lane A plan** | [`2026-09-21-loop-b-60d-forward-label-pipeline.md`](../tickets/2026-09-21-loop-b-60d-forward-label-pipeline.md) | Unlock = wire Mode C 411–414 onto `daily_job` corr_v2; keep `fwd_20d` interim. |
| **P1 reminder Oct 1** | [`2026-09-21-packaging-sub100-share-vs-option-m-band.md`](../tickets/2026-09-21-packaging-sub100-share-vs-option-m-band.md) | Packaging M-band review reminder — do not invent stamps overnight. |

**Not inventing:** A-track Trading Strategy (TS) + Interactive Brokers (IBKR) work beyond Mode D fingerprint naming; new PBR stamps; Teal requeue; ticket archives.

---

## 6. What I did / did not

**Did:** Confirm GPU idle (ollama resident only); re-read INDEX + Loop B trail; read-only WUT refresh (PCS depth, sources, interim fwd labels, Edge_R, corr mid-band); read-only PBR + Sidekiq glance; restore missing P0 Capital-fit ticket + INDEX row; file refresh JSON + this note + ticket progress pointers; Jev verify on mid-band / Mode C daily_job claims; local commit (+ push if desk pattern).  
**Did not:** Mutate promote decisions; invent A-track stamps; pull Ollama / GPU training; open ADR; start Loop C (B was substantive); archive tickets; requeue Teal; message John; claim Ops host DoD.

---

## 7. Open next (morning digest)

1. **INDEX:** Capital-fit P0 restored — confirm; archive Done rows after approval.  
2. **Pipeline:** wire Mode C 411–414 onto `daily_job` corr_v2 (still the unlock for Mode C forward labels); Slate still 2026-09-19.  
3. **fwd_60d:** earliest *calendar* depth from Red-first ≈ **2026-10-02**; still need PBR equity covering as_of+60. Keep **fwd_20d interim**.  
4. **Mode D:** name Trading Strategy fingerprint on #1585 before paper covered-call send.  
5. **USDU / Capital fit:** Operator flatten-or-fund Teal/Indigo; browser-verify Justification Capital fit line.  
6. **RangeError:** fix in code; Teal #767–#770 still stopped — Operator decides Teal restamp.  
7. **IBKR OPT prove:** still open on long-call print.  
8. **Triage proposals** in §5 — archive/discard only after Operator approval.

---

## 8. Jev judgment (overnight)

| # | Claim (abbrev) | Verdict | Conf |
|---|----------------|---------|------|
| 1 | Teal PCS mid-band ~64.89 + #743 Edge_R ~17.10 → hold stub; Mode C still pbr-only | **verified** | 1.00 |
| 2 | Capital-fit P0 was missing from WT INDEX/file; Done bakeoffs still clutter active INDEX | **verified** | 0.95 |

Triage excerpt **screen PASS** (injection 0.07 / substance 0.99 / relevance 0.98).  
Ran via `scripts/jev-desk-helpers.sh verify` + `screen` (jev 0.2.3 / jev-1.13.0 via typesafe).
