# Ticket: Stack ARR + MER on trade timeline; risk-scale path chart

**Status:** Phase 0–3 implemented — evaluate on live PBRs  
**Priority:** P2  
**Date:** 2026-08-04  
**Monolith:** Winston Unit Test (WUT) lab  
**Scope:** Measurement + UI through Phase 3 (no smooth-Kelly policy yet)

---

## Locked definitions

| Term | Definition |
|------|------------|
| **Engagement** | One market + direction from first open lot until flat |
| **Lot \(r_i\)** | Signed \((P_{exit} - P_{entry}) / ATR_i\) (flip for short) |
| **\(ATR_i\)** | Per-lot entry ATR (signal/fill bar); stop-distance fallback |
| **Stack ARR** | Unweighted \(\sum r_i\) — OWD risk % does **not** weight |
| **MER (opportunity)** | **L1 only +4 ATR**; pyramid adds **0** (same trend thesis) |
| **MER (expectancy)** | L1: \(p\cdot 4+(1-p)(-s)\); adds: \(-(1-p)s\) (win payoff 0) |
| **MER stack** | Unweighted ∑ lot opportunity MER → typically **4** per engagement |
| **p** | Empirical if \(n\ge 20\) closed lots; else prior **0.30** |

Full write-up: `docs/analysis/2026-08-04-stack-arr-mer-engagement-defaults.md`

Canonical example: entries 20/25/30/35, exit 25, ATR=5 → lot R = +1, 0, −1, −2 → **ARR stack = −2**.

---

## Phases (this ticket)

| Phase | Deliverable | Status |
|-------|-------------|--------|
| 0 | Ticket + rules | this file |
| 1 | `StackArrCalculator` + timeline ATR/R + engagements | code |
| 2 | MER lot/stack + summary strip | code |
| 3 | Enrich Kelly `risk_history` diagnostics + PBR risk-scale chart | code |
| later | smooth_kelly policy + matrix | **out of scope** |

---

## Acceptance

- [x] Unit specs pass toy −2 ATR stack  
- [x] Trade timeline shows lot \(r_i\), stack ARR, MER  
- [x] PBR show: ARR summary strip + risk-scale path chart from `risk_history`  
- [x] Kelly recompute stores p, b, f*, κ in state snapshot for tooltips  
- [x] No change to bet sizing math (measurement only)  

**Note:** Kelly diagnostics appear on **new** PBR runs after this ship. Historical `risk_history` still charts multiplier/streaks but may lack p/b tooltips.

**2026-08-17 leftover land:** `TradeTimelineBuilder` and `_stack_arr_summary.html.erb` are now on WUT `main` (`ffe18ef`). Remaining work is operator eval on live PBRs, then mark this ticket Done — do not open a second ticket.

---

## Related

- Kelly meta layer: `docs/analysis/2026-07-31-risk-scale-meta-layer.md`  
- Kelly hybrid matrix: `docs/tickets/2026-08-03-kelly-hybrid-matrix.md`  
- Operator discussion 2026-08-04 (stack ARR unweighted)
