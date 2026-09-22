# Loop B overnight — PCS depth + mid-band hold (refresh)

**Date:** 2026-09-21 ~22:15–22:25 MT (America/Denver)  
**Track:** Loop Engineering **Dimension B** — portfolio design (PCS / corr / re-weight)  
**Status:** Evidence refresh. **No auto re-weight. No ADR.**  
**Refresh JSON:** [`2026-09-22-loop-b-overnight-refresh.json`](2026-09-22-loop-b-overnight-refresh.json)  
**Prior:** [`2026-09-21-loop-b-60d-forward-labels-feature-table.md`](2026-09-21-loop-b-60d-forward-labels-feature-table.md) · seed [`2026-09-21-loop-b-60d-forward-labels-seed.json`](2026-09-21-loop-b-60d-forward-labels-seed.json)  
**Ticket:** [`../tickets/2026-09-21-loop-b-60d-forward-label-pipeline.md`](../tickets/2026-09-21-loop-b-60d-forward-label-pipeline.md)

---

## 1. Questions answered tonight

| Question | Answer (evidence) |
|----------|-------------------|
| Unlock true `fwd_60d` yet? | **No.** `unlock_fwd_60d=false`. Max available forward still **46 td** (Blue/Orange). Oldest cohort snap (Red 2026-07-11) → today ≈ **51–52 td**; calendar-only 60td from that first snap ≈ **2026-10-02**, **and** PBR OA equity must cover the window (current best cells end ~2026-09-14/18). |
| Reinforce interim `fwd_20d`? | **Yes.** Parents with equity∩PCS overlap still print usable `fwd_20d` / `fwd_available` (unchanged magnitudes vs prior seed). Mode C books still lack depth for interim labels. |
| Mid-band [60,72] membership-first still unlocked? | **Yes — reinforced.** Teal PCS **64.88** (was 64.86), Edge_R **17.10** on #743; #727 Edge_R **17.70**. Copper **60.90** / Edge **15.67**; Slate **60.83** / Edge **14.84**. Red/Blue/Mango also mid-band + solvent OA. |
| New actionable ranking for Wv2-promoted? | **No material re-rank.** Mode C PCS flat except Teal +0.02 from new **pbr** snap 2026-09-21. Stubs unchanged for collapses (Mint/Yellow/Rust/Orange = `reweight_candidate`; Walnut = `watch`). |

---

## 2. PCS depth / daily_job gap (Mode C)

| Book | n snaps | sources | latest as_of | latest src | PCS | Δ since first |
|------|---------|---------|--------------|------------|-----|---------------|
| Indigo | 3 | pbr:3 | 2026-09-19 | pbr | 72.29 | +0.85 |
| Teal | **4** | pbr:4 | **2026-09-21** | pbr | **64.88** | −1.53 |
| Copper | 3 | pbr:3 | 2026-09-19 | pbr | 60.90 | −0.01 |
| Slate | 3 | pbr:3 | 2026-09-19 | pbr | 60.83 | 0.00 |

Parents (Red/Blue/Mango/Orange/Mint/Yellow/Rust/Walnut) advanced **+1 daily_job** snap to **2026-09-21**; PCS scores **unchanged** day-over-day.

**Pipeline blocker unchanged:** Mode C pids 411–414 still **not** on `daily_job` corr_v2 stream (ticket acceptance item open).

---

## 3. Forward-label status (refresh vs prior seed)

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

Magnitudes match 2026-09-20 seed within rounding.

**Sketch nuance:** Red/Blue stubs tonight = `hold` (mid-band + solvent), vs prior night’s more conservative `hold_diversifier_watch`. Doctrine §5.2 mid-band hold preference supports tonight’s label; not an ADR change.

---

## 4. Mid-band + Teal Edge anchor

- **#743** Teal legacy r02 LEAP: OA ≈ +19992%, Edge_R **17.0985**, PCS regime `mid_band_corridor` @ 64.88 → **hold**.  
- **#727** Teal turtle r02 LEAP: Edge_R **17.6998** (higher than #743) — still mid-band geometry support.  
- Heat-ON post-#55 cells **#767/#768 running**, **#769/#770 failed** (lab status only; not Loop B ranking input until completed).

**Do not maximize PCS.** Orange paradox intact: PCS **24.87** (Δ −43.47 since first) with full OA still huge and short-forward OA ≥0 → geometry `reweight_candidate`, Operator keeps-for-alpha vs rebuild-for-gate.

---

## 5. What I did / did not

**Did:** Re-read tickets INDEX + Loop B trail; read-only WUT refresh (PCS depth, sources, interim fwd labels, Edge_R); file refresh JSON + this note; update pipeline ticket progress; session wrap; optional Jev verify on mid-band / fwd60 claims.  
**Did not:** Mutate promote decisions; invent A-track TS+IBKR; pull Ollama / GPU inference; open ADR; start Loop C; message John.

---

## 6. Open next (morning digest)

1. **Pipeline:** wire Mode C 411–414 onto `daily_job` corr_v2 (still the unlock for Mode C forward labels).  
2. **fwd_60d:** expect earliest *calendar* depth from Red-first ≈ **2026-10-02**; still need PBR equity covering as_of+60 (re-stamp/extend or wait for newer completed cells). Keep **fwd_20d interim** as operating scoreboard.  
3. **Doctrine:** mid-band [60,72] membership-first remains sketch — John dial on membership vs risk_scale still open.  
4. **Optional:** Walnut LEAP OA cell still missing (diversifier watch).  
5. Heat-ON #767/#768 completion is A/lab ops — not Loop B invent work.
