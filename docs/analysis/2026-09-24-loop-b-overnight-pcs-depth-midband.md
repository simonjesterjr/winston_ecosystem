# Loop B overnight — PCS depth + mid-band hold (refresh)

**Date:** 2026-09-23 ~21:55–22:20 MT (America/Denver)  
**Track:** Loop Engineering **Dimension B** — portfolio design (Portfolio Construction System (PCS) / correlation / re-weight)  
**Status:** Evidence refresh. **No auto re-weight. No Architecture Decision Record (ADR).**  
**Refresh JSON:** [`2026-09-24-loop-b-overnight-refresh.json`](2026-09-24-loop-b-overnight-refresh.json)  
**PBR/Sidekiq glance:** [`2026-09-24-loop-b-overnight-pbr-sidekiq-glance.json`](2026-09-24-loop-b-overnight-pbr-sidekiq-glance.json)  
**Runner:** [`_loop_b_overnight_refresh_2026-09-23.rb`](_loop_b_overnight_refresh_2026-09-23.rb)  
**Prior:** [`2026-09-23-loop-b-overnight-pcs-depth-midband.md`](2026-09-23-loop-b-overnight-pcs-depth-midband.md) · [`2026-09-22-loop-b-overnight-pcs-depth-midband.md`](2026-09-22-loop-b-overnight-pcs-depth-midband.md) · [`2026-09-21-loop-b-60d-forward-labels-feature-table.md`](2026-09-21-loop-b-60d-forward-labels-feature-table.md)  
**Ticket:** [`../tickets/2026-09-21-loop-b-60d-forward-label-pipeline.md`](../tickets/2026-09-21-loop-b-60d-forward-label-pipeline.md)

---

## 1. Questions answered tonight

| Question | Answer (evidence) |
|----------|-------------------|
| Unlock true `fwd_60d` yet? | **No.** `unlock_fwd_60d=false`. Max available forward still **46 trading days (td)** (Blue/Orange). Calendar depth from Red-first snap → today = **54 td** (was 53); calendar-only 60 td from that first snap still ≈ **2026-10-02**, **and** Parameterized Backtest Run (PBR) Option-Aware (OA) equity must cover the window. |
| Reinforce interim `fwd_20d`? | **Yes.** Parents with equity∩PCS overlap still print usable `fwd_20d` / available-forward OA (magnitudes match prior refresh within rounding). Mode C books still lack depth for interim labels. |
| Mid-band [60,72] membership-first still unlocked? | **Yes — reinforced.** Teal PCS **64.88**, Edge_R **17.10** on #743; #727 Edge_R **17.70** intact. Copper **60.90** / Edge **15.67**; Slate **60.83** / Edge **14.84**. Red/Blue/Mango mid-band + solvent OA → stub `hold`. |
| New actionable ranking for Winston v2 (Wv2)-promoted? | **No material re-rank.** Mode C PCS flat vs last night (Teal still 64.88; Indigo 72.29). Collapse stubs unchanged (Mint/Yellow/Rust/Orange = `reweight_candidate`; Walnut = `watch`; Indigo = `hold_diversifier_watch`). |

---

## 2. PCS depth / daily_job gap (Mode C)

| Book | n snaps | sources | latest as_of | latest src | PCS | Δ since first |
|------|---------|---------|--------------|------------|-----|---------------|
| Indigo | 3 | pbr:3 | 2026-09-19 | pbr | 72.29 | +0.85 |
| Teal | **4** | pbr:4 | **2026-09-21** | pbr | **64.88** | −1.53 |
| Copper | 3 | pbr:3 | 2026-09-19 | pbr | 60.90 | −0.01 |
| Slate | 3 | pbr:3 | 2026-09-19 | pbr | 60.83 | 0.00 |

Parents (Red/Blue/Mango/Mint/Yellow/Rust/Walnut) advanced **+1 daily_job** snap to **2026-09-23**; PCS scores **unchanged** day-over-day within ±0.01 rounding (Red 71.49 vs 71.50). Orange latest snap source tonight = `pbr` @ 2026-09-23 with PCS **24.87** unchanged (paradox intact); Orange `latest_daily_job_as_of` still **2026-09-21**.

**Pipeline blocker unchanged:** Mode C portfolio ids (pids) 411–414 still **not** on `daily_job` corr_v2 stream (ticket acceptance item open).

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
| Teal/Copper/Slate/Indigo | — | ≤1 | — | insufficient | hold / hold_diversifier_watch (Indigo @72.29) |

**Do not maximize PCS.** Orange paradox intact: PCS **24.87** (Δ −43.47 since first) with full OA still huge and short-forward OA ≥0 → geometry `reweight_candidate`, Operator keeps-for-alpha vs rebuild-for-gate.

---

## 4. Lab / PBR read-only (not Loop B invent)

| PBR | Book | Status | Note |
|-----|------|--------|------|
| #743 / #727 | Teal | completed | Mid-band Edge anchors unchanged (17.10 / 17.70) |
| #767–#770 | Teal heat-ON | **failed** + `operator_stop` | Same 4-byte RangeError strings — **do not requeue** ([ticket](../tickets/2026-09-22-wut-teal-heat-on-rangeerror-4byte-int.md)) |
| #771 | Orange RST r01 | **completed** (updated 2026-09-23 10:29 MT) | Same cell key; Edge_R **−0.1458**, OA ≈598. Ticket text still says operator restamp pending / do not requeue 767–771 — I did **not** invent a Teal restamp. Morning: reconcile INDEX status vs completed #771. |

Winston Unit Test (WUT) Sidekiq: no Portfolio Backtest jobs in RetrySet (`pbr_in_retry=0`); RetrySet size=27 (non-PBR noise). Named PBR queue empty / not listed; `expected_returns` queue large (~79k) — **ops glance only**, not my claim of host Definition of Done (DoD).

---

## 5. Ticket triage (overnight — propose only; **do not archive**)

I consulted [`../tickets/INDEX.md`](../tickets/INDEX.md).

### 5a. Discard / archive **candidates** (Operator morning approval required)

| File | Why propose discard/archive |
|------|-----------------------------|
| [`2026-09-20-standard-call-flatten-roll-desk.md`](../tickets/2026-09-20-standard-call-flatten-roll-desk.md) | **Status already Done** — still listed in active INDEX. Move to `archive/` when Operator okays. |
| [`2026-09-22-min-atr-capital-consumption-guard.md`](../tickets/2026-09-22-min-atr-capital-consumption-guard.md) | **Status already Done** (Operator locked 2026-09-23) — still in active INDEX. Archive candidate. |
| [`2026-09-17-eod-pending-15-human-confirm.md`](../tickets/2026-09-17-eod-pending-15-human-confirm.md) | Six-day-old one-shot pending-draft list (2026-09-17 journals). Likely stale — confirm pending count=0 or explicit defer, then archive. |
| [`2026-09-20-wut-standard-call-plan-b-parity.md`](../tickets/2026-09-20-wut-standard-call-plan-b-parity.md) | P3 “only if operator asks” — park/discard if no ask by next Loop review. |
| [`2026-09-11-fulfillment-desk-adapters-yield-browser-verify.md`](../tickets/2026-09-11-fulfillment-desk-adapters-yield-browser-verify.md) · [`2026-09-10-signal-inspect-first-paint-eval-card.md`](../tickets/2026-09-10-signal-inspect-first-paint-eval-card.md) | Stale P3 browser-verify chores (~12–13 days) — discard or demote unless Operator still wants them. |

### 5b. Prioritize next (morning)

| Priority | File | Why |
|----------|------|-----|
| **P0** | [`2026-09-21-wut-heat-on-rst-portfolio-limit-bypass.md`](../tickets/2026-09-21-wut-heat-on-rst-portfolio-limit-bypass.md) | Capital-safety heat-ON bypass — keep In progress until WUT #55 path is proven closed. |
| **P1 Lane B** | [`2026-09-22-wut-teal-heat-on-rangeerror-4byte-int.md`](../tickets/2026-09-22-wut-teal-heat-on-rangeerror-4byte-int.md) | **Code fix landed** (`passed_signals.would_have_units` fail-closed). Teal #767–#770 still failed+operator_stop — **Operator restamp decision** (not overnight invent). Orange #771 now **completed** in WUT — reconcile ticket Status/INDEX. Still no auto-requeue of Teal. |
| **P1** | [`2026-09-15-bg-ibkr-opt-order-intent-prove.md`](../tickets/2026-09-15-bg-ibkr-opt-order-intent-prove.md) | Still **In progress**. Ticket evidence: Day LMT/MKT long-call probes rejected (MD + options-strategy permission). Desk episodes (parent): Level 1 covered-call path worked; long-call still needs Level 2 / Account Management (AM) permissions+MD — Operator morning grill, not overnight invent. |
| **P1 Lane A plan** | [`2026-09-21-loop-b-60d-forward-label-pipeline.md`](../tickets/2026-09-21-loop-b-60d-forward-label-pipeline.md) | Unlock = wire Mode C 411–414 onto `daily_job` corr_v2; keep `fwd_20d` interim. |
| **P1 reminder Oct 1** | [`2026-09-21-packaging-sub100-share-vs-option-m-band.md`](../tickets/2026-09-21-packaging-sub100-share-vs-option-m-band.md) | Packaging M-band review reminder — do not invent stamps overnight. |
| **P1 / P2** | [`2026-09-17-leap-aware-dar-narrative.md`](../tickets/2026-09-17-leap-aware-dar-narrative.md) | Excerpt in tool preview; quiet checkpoint still short — continue CLI seed, not new scope. |
| **P1** | [`2026-09-21-probe-before-promote.md`](../tickets/2026-09-21-probe-before-promote.md) | Keep as promote gate; attach PASS output before prefer-language. |

**Not inventing:** A-track Trading Strategy (TS) + Interactive Brokers (IBKR) work; new PBR stamps; Teal requeue; ticket archives.

---

## 6. What I did / did not

**Did:** Confirm ecosystem path + git main; GPU idle given by parent; re-read INDEX + Loop B trail; read-only WUT refresh (PCS depth, sources, interim fwd labels, Edge_R); read-only Teal/Orange PBR + Sidekiq glance; file refresh JSON + this note + ticket progress; Jev verify on mid-band / RangeError claims; local commit of overnight artifacts.  
**Did not:** Mutate promote decisions; invent A-track; pull Ollama / GPU inference; open ADR; start Loop C; archive tickets; requeue Teal; message John; claim Ops host DoD.

---

## 7. Open next (morning digest)

1. **Pipeline:** wire Mode C 411–414 onto `daily_job` corr_v2 (still the unlock for Mode C forward labels).  
2. **fwd_60d:** earliest *calendar* depth from Red-first ≈ **2026-10-02**; still need PBR equity covering as_of+60. Keep **fwd_20d interim** as operating scoreboard.  
3. **Doctrine:** mid-band [60,72] membership-first remains sketch — John dial on membership vs risk_scale still open.  
4. **RangeError:** fix in code; **#771 completed**; Teal #767–#770 still stopped — Operator decides Teal restamp; update INDEX Status wording.  
5. **IBKR OPT prove:** still open on long-call print; covered-call Level 1 evidence is desk-episode context — morning AM Level 2 / MD path.  
6. **Triage proposals** in §5 — archive/discard only after Operator approval.

---

## 8. Jev judgment (overnight)

| # | Claim (abbrev) | Verdict | Conf |
|---|----------------|---------|------|
| 1 | Teal PCS mid-band ~64.88 + #743 Edge_R ~17.10 → hold stub | **verified** | 1.00 |
| 2 | Teal #767–#770 still failed+operator_stop; #771 completed; no Teal requeue overnight | **verified** | 0.99 |

Ran via `scripts/jev-desk-helpers.sh verify` against this note (jev 0.2.3 / jev-1.13.0 via typesafe).
