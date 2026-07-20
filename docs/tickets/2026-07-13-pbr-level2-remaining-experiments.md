# Ticket: PBR Level 2 remaining experiments (anti-overfit matrix)

**Status:** Proposed  
**Priority:** P2
**Date:** 2026-07-13  
**Monolith:** winston_unit_test (WUT lab runs; results → `ecosystem/business_analysis/`)

## Context

Business analysis: [`business_analysis/2026-07-13-pbr-return-dd-pcs-evaluation.md`](../../business_analysis/2026-07-13-pbr-return-dd-pcs-evaluation.md).

**Done this session:**

| PBR | Path | Result (vs Blue 48) |
|-----|------|---------------------|
| 48 | baseline | +2073% / DD 20.9% / Sharpe 1.52 |
| 62 | C0 max_markets=4 | +1415% / DD 41.6% / still trade_ready |
| 63 | P1 position_swap on | +975% / DD 31.5% / **worse** than 48 |

**Do not overwrite** PBR 44/48. New IDs only. One axis at a time.

## Remaining pre-registered runs

### Risk (R)

- [ ] **R2** — Blue Swing + VolExit + TS13 ladder `[2,3,3,4,4]` long (vs R1 `[2,3,4,6,6]`)
- [ ] **R3** — Conservative / flat ladder — is acceleration necessary?

### Exit / confirm (X) — operator questions

- [ ] **X1** — Dual exit `[1,15]` on **same** Swing entry as 48 (isolates multi-exit)
- [ ] **X2** (optional) — Add ATR / max-holding exit only after X1
- [ ] **X3** — One confirmational entry (e.g. Penetration25Day) on Blue R1; score Sharpe/DD/pass mix, not max return

### Transfer (E) — repeatability

- [ ] Red winner entry (25) + R1 under documented caps (compare to 46)
- [ ] Green 55 entry + R1 — dynamic on trade_ready cohort
- [ ] Orange 41 entry + R1 under C0 (max_mkt=4)

### Capacity quality (P)

- [ ] **P1 under C0** — swap on + max_markets=4 (62 base + swap) — optional after R paths
- [ ] **P3** — Sample counterfactual: blocked `portfolio_limit`/`market_limit` signal vs weakest open position subsequent contribution (script, not full re-search)

### Leverage (K) — optional

- [ ] K1/K2 half risk / leverage 1 on Green 55 or Blue 62 for paper-friendly sizing  
  **Policy note (2026-07-13):** paper focus is already **force max_leverage=1×** and **max_markets=4** (`docs/tickets/2026-07-13-paper-first-cohort-decision.md`). K runs calibrate lab recipes to that policy; they do not reopen 3× for paper without a new operator decision.

## Acceptance

- [ ] Each completed run logged in business analysis experiment table (id, path, metrics, pass-reason top-N)
- [ ] Paper-first recommendation revised if stop-rules fire
- [ ] No joint re-grid of entry×exit×risk on full sample

## Related

- Blue membership ticket (update with risk-rescue evidence)
- WUT business analysis UI: `2026-07-13-wut-expose-business-analysis-link.md`
