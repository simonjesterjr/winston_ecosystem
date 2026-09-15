# Ticket: WUT LEAP Edge (R) — signal-path 1R fix

**Status:** In Progress  
**Priority:** P1  
**Date:** 2026-09-15  
**Mode:** contractor  
**Graph nodes:** winston_unit_test (primary); ecosystem analysis/interfaces  
**Human gates:** no pack promotion from broken Edge; re-run/refresh S1 LEAP panel after WUT fix lands  
**DoD:** Signal-path 1R for options merged; S1 LEAP panel (#682–#697) stored `edge_r` refreshed; absurd 100s–1000s R gone; cells roughly align with audit recompute (~1–10R order of magnitude)  
**Origin:** Analysis [`docs/analysis/2026-09-15-ts75-leap-edge-accounting-audit.md`](../analysis/2026-09-15-ts75-leap-edge-accounting-audit.md); interface [`interfaces/winston-edge-v1.md`](../../interfaces/winston-edge-v1.md)  
**Related:** domain law leap-extra-modal-proxy / measuring-edge if present

## Problem

Stored `edge_r` on LEAP Portfolio Backtest Runs is accounting-broken (S1 and S2). `TradeTimelineBuilder` feeds option premium as entry and underlying 2N as stop into share `EdgeCalculator.one_r_dollars`. Longs fall through to ATR×2×contracts without ×100 → absurd R (hundreds to thousands). Cash PnL/PF can be real; Edge (R) must not rank paper strategies until fixed.

Evidence: `docs/analysis/2026-09-15-ts75-leap-edge-accounting-audit.md`

## Locked solution (operator 2026-09-15)

**Signal-path 1R (A):**

```
one_r = |order_price − original_stop| × contracts × 100
```

Never mix premium with underlying stop. Never use ATR×contracts without ×100 for options.

## Scope

1. Track WUT code fix in `EdgeCalculator` / `TradeTimelineBuilder` — signal-path 1R for `is_option`  
2. Specs for option vs share 1R calculation  
3. After merge: refresh stored Edge on S1 LEAP panel PBRs #682–#697 (`strategy75_leap_risk_ab_v1`) — re-execute or re-persist edge snapshot; report new `edge_r` vs old  
4. Optionally refresh S2 LEAP refs #667/#668/#672 for scoreboard honesty (same bug)

## Non-goals

- Premium-at-risk default for stop calculation  
- Changing cash PnL or LEAP fulfillment path  
- Wv2 packaging changes  
- Promoting packs from this ticket alone

## Acceptance

- [ ] WUT PR merged with signal-path 1R for `is_option`  
- [ ] Share Edge regression specs green  
- [ ] S1 LEAP panel (#682–#697) stored `edge_r` refreshed; absurd hundreds–thousands gone; solvent cells roughly align with audit's recomputed signal-path column (~1–10R order of magnitude, not 900R)  
- [ ] Scoreboard guidance: still use solvency/PF/return/DD; Edge (R) is usable again after refresh

## Fix direction locked (operator 2026-09-15)

Signal-path 1R (A) is the locked direction for WUT `EdgeCalculator`:

```
one_r = |order_price − original_stop| × contracts × 100
```

Do not mix option premium with underlying 2N stop. Do not use ATR×contracts without ×100 multiplier for options.
