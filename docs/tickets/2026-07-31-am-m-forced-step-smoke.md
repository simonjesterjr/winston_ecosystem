# Ticket: AM/M forced-step smoke (risk scale knobs that actually move)

**Status:** Proposed  
**Priority:** P2  
**Date:** 2026-07-31  
**Monolith:** winston_unit_test  
**Session:** `docs/session-reports/2026-07-31-1556-risk-scale-matrix-findings.md`

---

## Problem

Default Anti-Martingale / Martingale hybrid (44 trading days, equity ±16%) left `n_steps = 0` for the full Yellow sample on static/OWD/OWDC rows (PBRs 346/347, 350/351, 354/355 identical to none). Scale looked configured but was a **noop**.

## Desired outcome

1. Smoke PBRs (or unit + short lab) with knobs that **force** steps: e.g. review 21d, equity ±8%, and/or win/loss streak 2–3.  
2. Confirm mid-run `risk_history[].risk_scale.n_steps ≠ 0`.  
3. Document default vs stress knobs for operators.

## Acceptance

- [ ] At least one AM and one M cell show non-zero `n_steps` during the sample.  
- [ ] Note filed under `docs/analysis/` or update to `2026-07-31-risk-scale-meta-layer.md`.  

## Related

- Meta design: `docs/analysis/2026-07-31-risk-scale-meta-layer.md`  
- Matrix findings: session report 2026-07-31-1556  
