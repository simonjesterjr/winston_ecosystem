# Ticket: Decide first paper Operational Portfolio (Green 55 vs Blue 62 family)

**Status:** Partial — policies locked 2026-07-13; cohort deferred  
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

## Operator decision (2026-07-13)

| # | Question | Decision | Notes |
|---|----------|----------|-------|
| 1 | First paper OP seed | **Deferred** | No Green-vs-Blue focus chosen yet. Do **not** re-rank Active attention or re-import for paper focus until this lands. |
| 2 | Ops `max_markets` | **Force 4** | Honest ops config. Uncapped Blue 48 is lab upper bound only, not paper default. |
| 3 | Paper `max_leverage` | **Force 1×** on paper focus | Avoid cash≫equity leverage residue until accounting proven. Lab `max_leverage=3` stays lab-only until explicitly reopened. |

**Real capital:** still out of scope until paper hygiene proves out (unchanged).

Canonical write-up: business analysis §15 addendum  
[`business_analysis/2026-07-13-pbr-return-dd-pcs-evaluation.md`](../../business_analysis/2026-07-13-pbr-return-dd-pcs-evaluation.md).

### Live Wv2 snapshot (at decision time)

Six color Actives: Red, Blue, Green, Pink, Blank, Rust (Orange inactive).

| OP | Risk / stop (imported TS) | Implication |
|----|---------------------------|-------------|
| **Portfolio Green** | static + `move_to_last_entry`, Breakout55Day / VolExit | Already close to PBR 55 discipline recipe |
| **Portfolio Blue** | **static + isomorphic**, SwingBreakout5Day / VolExit | **Not** PBR 62 (dynamic R1 + move_to_last). Choosing Blue 62 later requires re-export/import (or successor), not just attention focus |

No Active-set or import changes made this session (cohort still open).

## Acceptance

- [x] Written operator decision recorded (partial: policies + defer cohort) in business analysis addendum + this ticket
- [ ] Cohort choice recorded (Green 55 vs Blue 62 vs dual vs other)
- [ ] Wv2 paper import / Active set updated only after cohort decision
- [x] Real capital activation explicitly out of scope until paper hygiene proves out

## Remaining when cohort is chosen

1. Record seed choice + rationale in business analysis §15.  
2. Apply attention hygiene: primary paper focus Active; demote non-focus color Actives unless force dual.  
3. If **Green**: confirm TS matches PBR 55 gates recipe; ensure ops caps `max_markets=4`, paper leverage 1×.  
4. If **Blue 62**: do **not** engage current static isomorphic Blue as if it were 62 — export C0 recipe from WUT, import as lineage-correct OP/TS (auto-fork if fingerprint differs), then Active + paper.  
5. Prefer first journal confirm on the chosen seed (supersedes or pairs with Red paper-confirm ticket once focus is set).

## Related

- After cohort hygiene/import: `2026-07-13-paper-focus-active-hygiene-and-recipe.md`
- First paper journal (focus seed): `2026-07-13-confirm-first-paper-journal-focus-cohort.md`
- Enforce caps in export/import: `2026-07-13-enforce-paper-max-markets-and-leverage.md`
- Level 2 experiments ticket: `2026-07-13-pbr-level2-remaining-experiments.md` (K1/K2 leverage 1 paths align with policy #3)
- Red paper confirm (still open if Red remains secondary): `2026-07-10-confirm-first-red-paper-pending-action.md`
- Capital activation domain: ADR-006 / business-context OP lifecycle
- Session: `docs/session-reports/2026-07-13-1741-paper-first-cohort-partial.md`
