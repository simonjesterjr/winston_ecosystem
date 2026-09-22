# Ticket: Min ATR / capital-consumption guard (Turtle / TF spirit)

**Status:** Proposed  
**Priority:** P1  
**Date:** 2026-09-22  
**Lane:** A (plan + evaluate first; **no implement** until Operator greens after plan)  
**Implementer:** (deferred — Grok CLI after plan lock)  
**Parent plans:** [`../../plans/spending-capacity-and-leap-fulfillment.md`](../../plans/spending-capacity-and-leap-fulfillment.md) · [`../../plans/trade-fulfillment-engine.md`](../../plans/trade-fulfillment-engine.md)  
**Sibling:** [`2026-09-04-tf-p3-live-sizing-and-capital-authority.md`](2026-09-04-tf-p3-live-sizing-and-capital-authority.md) (Spending Capacity / Capital Authority into sizer)  
**Related:** [`2026-09-21-packaging-sub100-share-vs-option-m-band.md`](2026-09-21-packaging-sub100-share-vs-option-m-band.md) (sub-100 share vs option packaging — different axis)

## Goal

Evaluate and lock a desk rule that refuses or caps **egregiously capital-consuming** share entries where Turtle / Trend Following (TF) unit sizing is *correct* at 1–2% risk but Average True Range (ATR) / stop distance is so small that share count × price eats most (or more than) free cash — then, only after plan + Operator evaluate, implement the smallest guard.

**DoD (after evaluate):** written law + grill locks (where / when / refuse vs resize) + System One harness; **code out of scope until that lock**.

## Context / specimens (2026-09-22 DAR)

Operator walked Pending on Daily Activity Report (DAR) `wv2_20260922.json` and flagged capital math:

| Journal | Portfolio | Market | Price | Confirm units | Rough notional | Book free_cash (chapter) | Risk % |
|--------:|-----------|--------|------:|--------------:|---------------:|-------------------------:|-------:|
| 2029 | Teal · evolved-from-wut-727 | USDU | 26.65 | 2872 | ~$76.5k | $28,890 | 2% |
| 2028 | Indigo · evolved-from-wut-724 | USDU | 26.65 | 2809 | ~$74.8k | $37,234 | 2% |

Implied stop distance if units = (risk% × risk_equity) / N for Teal ≈ **$0.20/share** (2% of ~$28.7k risk_equity ÷ 2872) — classic “tiny N → huge shares → portfolio-blocking notional.”

Operator ask (verbatim spirit): rule in the spirit of TF / Turtles to limit consuming trades where risk is egregiously small and position size gets huge — e.g. **minimum ATR (or N) for trade / portfolio inclusion**. **Do not implement until we plan and evaluate.**

Forensics is auditing 2026-09-22 paper trades separately (equity/cash correctness + Interactive Brokers (IBKR) Long-term Equity Anticipation Security (LEAP) / long-call / stock validation). Fold any sizing-formula evidence from that autopsy into this ticket’s Specimens section when it lands.

## Problem (desk)

Turtle unit risk alone does **not** bound cash/notional. Spending Capacity (SC) / Leverage Guardrail work in [`2026-09-04-tf-p3-live-sizing-and-capital-authority.md`](2026-09-04-tf-p3-live-sizing-and-capital-authority.md) is the capital ceiling spine; this ticket is the **volatility / inclusion** spine: markets whose ATR is too small relative to price (or whose dollar-N is below a floor) should not draft multi–cash-stack share units on a ~$30k Mode C book.

## Candidate rule shapes (evaluate — pick 0–2, do not ship yet)

1. **Min ATR (absolute $)** — refuse DA draft / slate if ATR < floor (per market class or global).  
2. **Min N / stop distance ($)** — refuse if `|entry − original_stop|` < floor.  
3. **Min ATR% of price** — refuse if ATR/price < X% (cross-asset).  
4. **Max notional / free_cash (or Risk Capital)** — refuse or clip units if `units × price > κ × free_cash` (overlaps SC; may be the SC Check already planned).  
5. **Max units or max capital fraction per initiation** — hard clip with HITL override.  
6. **Portfolio inclusion filter** — keep signal for lab/WUT; exclude from live/Mode C slate until ATR recovers (softer than refuse).

Prefer rules that preserve **1R methodology comparability** and do not silently rewrite Edge (R). Prefer **refuse / HITL** over silent downsize unless Operator locks clip.

## Work items (plan / evaluate only)

- [ ] Pull Forensics 2026-09-22 sizing math for journals 2028/2029 (ATR, N, risk$, units formula).  
- [ ] Grill: absolute ATR vs ATR% vs max notional-of-cash vs SC-only — which is Turtle-spirit and desk-operable.  
- [ ] Decide refuse vs resize vs slate-exclude; Mode C paper vs IBKR paper vs live authority.  
- [ ] Relate to SC / Capital Authority ticket — avoid duplicate gates; document order of checks.  
- [ ] Write short analysis note under `docs/analysis/` with specimen table + recommendation.  
- [ ] Promote locks into plan (`spending-capacity-…` or small child plan) + business-context blurb; ADR only if irreversible.  
- [ ] **Stop.** No PositionSizer / DA code until Operator greens implement.

## System One harness

**State:** DAR `winston_v2/storage/cromwell_notifications/wv2_20260922.json` actions for journals 2028/2029 (USDU @ 26.65, units 2809/2872); Teal/Indigo chapter free_cash / risk_equity / risk_percentage 2%; parent SC plan + TF-P3 ticket paths above.

**Checkpoints:**

| id | type | instructions | pass rule |
|----|------|--------------|-----------|
| specimen_math | Noul | Teal 2029 notional ≫ free_cash while unit risk ≈ 2% is a real capital-consumption smell, not a journal bug | noul ≥ 0.85 |
| rule_shape | Choice | options: min_atr_abs, min_atr_pct, min_stop_dollars, max_notional_of_cash, sc_only_defer, mix | choice ∈ {min_atr_abs,min_atr_pct,min_stop_dollars,max_notional_of_cash,mix} ∧ confidence ≥ 0.7 |
| no_silent_clip | Noul | Recommended first ship is refuse/HITL or slate-exclude, not silent unit rewrite without Operator lock | noul ≥ 0.85 |
| sc_overlap | Choice | options: child_of_sc, parallel_volatility_gate, defer_to_tf_p3_only | choice ≠ defer_to_tf_p3_only if specimen would pass SC wording but still block the book |

**Runner:** `jev ask` after analysis note exists  
**Order:** Forensics numbers + deterministic notional math first; Jev on rule-shape judgment  
**On fail:** keep Proposed; do not implement

## CLI seed

```
(deferred — no implement session until Operator greens after plan/evaluate)
```

## Non-goals

- Implementing PositionSizer / Daily Analysis / slate changes in this ticket’s Proposed phase  
- Changing LEAP / standard_call packaging math or ADR-017  
- Resolving Teal/Indigo `cash_exposure_disagree` flags (separate Forensics/accounting track)  
- Sub-100 share vs option M-band packaging (sibling ticket)

## Operator notes

- 2026-09-22: pleased with Pending workflow (LEAP / long calls / stock; exits / pyramids / entries). Capital-consumption rule is the follow-on concern, not a workflow defect.  
- Explicit: **plan and evaluate before any implement.**
