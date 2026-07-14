# Ticket: Decide first paper Operational Portfolio (Green 55 vs Blue 62 family)

**Status:** Done (decision 2026-07-14; Phase 1 hygiene + first paper journal same day)  
**Date:** 2026-07-13  

## Context

From [`business_analysis/2026-07-13-pbr-return-dd-pcs-evaluation.md`](../../business_analysis/2026-07-13-pbr-return-dd-pcs-evaluation.md):

| Candidate | Case |
|-----------|------|
| **A — Green PBR 55** | trade_ready static, best PCS (83), capacity-clean, lower lab return |
| **B — Blue PBR 62** | C0 honest caps, still trade_ready (+1415% / DD 41.6%), risk-regime dependent; cash≫equity / leverage flag |
| Lab upper bound | Blue 48 uncapped — **not** preferred ops default without explicit policy |

## Decision needed

1. First **paper** OP seed: Green discipline vs Blue exploration (or both with dual-active force)?
2. Ops `max_markets`: force **4** vs allow nil?
3. Paper `max_leverage`: allow 3 vs force 1×?

## Operator decision

### 2026-07-13 (policies)

| # | Question | Decision | Notes |
|---|----------|----------|-------|
| 2 | Ops `max_markets` | **Force 4** | Honest ops config. Uncapped Blue 48 is lab upper bound only, not paper default. |
| 3 | Paper `max_leverage` | **Force 1×** on paper focus | Avoid cash≫equity leverage residue until accounting proven. Lab `max_leverage=3` stays lab-only until explicitly reopened. |

### 2026-07-14 (Phase 0 — cohort)

| # | Question | Decision | Notes |
|---|----------|----------|-------|
| 1 | First paper OP seed | **Blue 62 (exploration)** | C0 honest-cap Blue family for first paper journals. **Not** live Wv2 “Portfolio Blue” as currently imported. |
| 0.2 | Active hygiene timing | **Record only — no Active changes yet** | Six color Actives left as-is until Phase 1 hygiene session (`2026-07-13-paper-focus-active-hygiene-and-recipe.md`). |

**Real capital:** still out of scope until paper hygiene proves out (unchanged).

Canonical write-up: business analysis §15 addendum  
[`business_analysis/2026-07-13-pbr-return-dd-pcs-evaluation.md`](../../business_analysis/2026-07-13-pbr-return-dd-pcs-evaluation.md).

### Live Wv2 snapshot (re-checked 2026-07-14)

Six color Actives: Red, Blue, Green, Pink, Blank, Rust (Orange inactive). Unchanged this session.

| OP | Live TS (import) | Implication for paper focus |
|----|------------------|-----------------------------|
| **Portfolio Blue** (id=7) | SwingBreakout5Day / VolExit, **static**, **isomorphic** stop | **Not PBR 62**. Phase 1 must WUT-export C0 recipe (dynamic R1 + move_to_last, max_markets=4, leverage 1× policy) → import/auto-fork → then Active as paper focus |
| **Portfolio Green** (id=8) | Breakout55Day / VolExit, static, move_to_last | Close to PBR 55; **not** first paper focus after this decision (archive / demote when hygiene runs) |

## Acceptance

- [x] Written operator decision recorded (policies 2026-07-13)
- [x] Cohort choice recorded (**Blue 62** exploration, 2026-07-14)
- [x] Wv2 paper import / Active set updated (OP #12, sole Active) — Phase 1
- [x] Real capital activation explicitly out of scope until paper hygiene proves out

## Phase 1 completion (2026-07-14)

1. ~~Record seed choice + rationale in business analysis §15.~~  
2. ~~Attention hygiene: only `Portfolio Blue · PBR62` (#12) Active.~~  
3. ~~WUT PBR 62 export → import as new OP (static Blue #7 left inactive).~~  
4. ~~JSON paper policy: max_markets=4, max_leverage=1.~~  
5. ~~First paper journal confirm (AMZN long 5 @ 251.03) — confirm ticket Done.~~  

## Related

- Hygiene/import: `2026-07-13-paper-focus-active-hygiene-and-recipe.md` (**next**)
- First paper journal (focus seed): `2026-07-13-confirm-first-paper-journal-focus-cohort.md`
- Enforce caps in export/import: `2026-07-13-enforce-paper-max-markets-and-leverage.md`
- Level 2 experiments: `2026-07-13-pbr-level2-remaining-experiments.md`
- Red paper confirm (secondary; do not prefer over Blue 62): `2026-07-10-confirm-first-red-paper-pending-action.md`
- Capital activation domain: ADR-006 / business-context OP lifecycle
- Prior partial: `docs/session-reports/2026-07-13-1741-paper-first-cohort-partial.md`
