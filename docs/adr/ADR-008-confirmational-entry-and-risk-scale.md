# ADR-008: Confirmational Entry (Initial Only) + Risk Scale into Trends

**Status:** Accepted  
**Date:** 2026-07-19  
**Deciders:** Operator + lab (confirm experiment campaign `confirm_entry_2026_07_18`)  
**Builds on:** ADR-006 (lineage), ADR-007 (PCS), first-pass vet doctrine  
**Evidence:** `ecosystem/business_analysis/2026-07-18-confirmational-entry-experiment.md`  
**Glossary:** `CONTEXT.md` — TradingStrategy, Portfolio Signal Optimization, Trade-Ready / Observation Portfolio

## Context

Winston’s verbal thesis is: **non-correlated books + trend entry + scale risk when the market confirms**. Two different “confirmation” mechanisms exist:

1. **Confirmational entry strategies** — second signal class AND-gated with primary on *whether to open* (or soft-size) an **initial** entry.  
2. **One-way dynamic pyramid risk** — after entry, add size on ATR steps with an **accelerating risk % ladder** (price path confirms the trend → scale into it).

Historically, top PBRs left **confirmational entry empty** while using (2). The 2026-07-18 matrix (20 cells on parents 62/71/72/57/55) showed large economics from (1) on Blue C0, and clarified product rules for both layers.

## Decision

### A. Confirmational entry is **initial-entry only**

1. Confirmational strategies apply in `TestingStrategy#evaluate_entry` only.  
2. **Pyramids are not gated by confirmational strategies** — they remain ATR-step risk adds under position management.  
3. Soft confirm (size dial when confirm fails) is supported for research; **hard confirm** is the promotion default based on experiment evidence (soft SMA20/Penetration underperformed hard twins on Blue 62).

### B. Risk scale into trends is the **pyramid ladder**, not the confirm slot

1. **One-way dynamic** means a per-direction risk % array indexed by **concurrent open pyramid level** on that market (1-based): e.g. long `[2%, 3%, 4%, 6%, 6%]`.  
2. Economic intent: a move that sustains multiple ATR adds is treated as a longer trend; later adds risk **more** capital per unit risk budget (not flat 2%).  
3. Confirmational entry and dynamic pyramid risk are **orthogonal** and may both be present (e.g. PBR 80 = EMA20 confirm + R1 ladder).

### C. Lab promotion candidate from this experiment (provisional)

1. **Primary paper-science recipe after this campaign:** Portfolio Blue C0 (max_markets=4) + SwingBreakout5Day + **EMA20 hard confirm** + VolExit + one_way_dynamic R1 ladder + move_to_last_entry (PBR **80** / cell C03).  
2. Alternate: SMA20 hard confirm (PBR **78** / C01).  
3. **Transfer default confirm** for non-Blue books when adding confirms: **Penetration25** (Donchian-class), not SMA20 (failed/no-op outside Swing5 Blue).  
4. Real capital still requires existing paper hygiene / viability process (ADR-006, trade-ready gates) — this ADR does not auto-promote to real.

### D. Lab batch execution

1. Long PBR campaigns may set `FAST_BACKTEST=1` (throttled status JSON, slim day payload, quiet logs).  
2. Fast path **must not** change signal/risk math — only I/O and reporting frequency.

### E. Handoff JSON must carry the pyramid ladder (mandatory)

1. Any **Trade-Ready / Observation** export (and internal portfolio_config) with `risk_evaluation_strategy: one_way_dynamic` **must** include an explicit ladder:  
   - top-level `pyramid_risks` and `risk_evaluation_config.pyramid_risks`  
   - same under `trading_strategy`  
2. **Validation fails the export** if `one_way_dynamic` is set without a non-empty long/short fraction ladder (`OneWayDynamicRiskValidator`). Silent flat-risk handoff is forbidden.  
3. Fingerprint payload includes the ladder (methodology identity).  
4. Wv2 stores the ladder on `TradingStrategy.parameters` and uses it for level sizing.

## Consequences

- Exports / TradingStrategy fingerprints for confirm winners must include **confirmational_entry_strategy_ids** and **risk_evaluation_config.pyramid_risks**.  
- UI must surface the ladder (not only the string `one_way_dynamic`) so operators can verify scale-in (see related issue).  
- Re-vet grids may later include confirm as a first-class axis; until then, post-vet confirm matrices are valid science if one-axis and parent-frozen.  
- Soft confirm remains available for research; do not paper-promote soft recipes without new evidence.  
- Re-export existing one_way_dynamic OPs after 2026-07-19 exporter fix before trusting Wv2 sizing.

## Rejected

- Using confirmational strategies to gate pyramid adds (conflicts with explicit “entry only” product rule).  
- Treating empty confirm as equivalent to soft confirm.  
- Joint re-grid of entry × confirm × ladder × exit on full sample in one pass (anti-overfit).  
- Promoting nil `max_markets` Blue recipes as ops defaults (C0 honesty from prior PBR analysis).

## Related

- Business results: `ecosystem/business_analysis/2026-07-18-confirmational-entry-experiment.md`  
- Prior risk-regime evidence: `ecosystem/business_analysis/2026-07-13-pbr-return-dd-pcs-evaluation.md`  
- Issue (visibility + estimate cap): `ecosystem/docs/issues/2026-07-19-one-way-dynamic-pyramid-risk-visibility-and-cap.md`  
- Code: `TestingStrategy`, `OneWayDynamicRiskEvaluation`, `PortfolioBacktestRunner` (`FAST_BACKTEST`)
