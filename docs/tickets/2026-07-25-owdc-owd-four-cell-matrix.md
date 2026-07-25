# Ticket: OWDC / OWD 4-cell lab matrix (trust close-out)

**Status:** Proposed  
**Priority:** P2  
**Date:** 2026-07-25  
**Monolith:** winston_unit_test  
**Related:** ADR `2026-07-25-lab-t1-fill-queue.md`; ADR `2026-07-25-pyramid-scale-in-price-blocks.md`; close-trigger / one_way_dynamic work; session `2026-07-25-1310-pbr-fill-queue-pyramid-cash.md`

---

## Problem

Fill cadence and path selection (same_bar vs T+1 queue) dominated recent PBR trust investigations. After T+1 queue + pyramid last-entry fixes, operators still may need a **structured 4-cell matrix** before declaring OWDC/OWD exit stack trustworthy:

Suggested axes (confirm with product before large re-runs):

| Axis A | Axis B | Intent |
|--------|--------|--------|
| Fill: `same_bar_open` vs `next_bar_open` / T+1 queue | Exit stack: OWD vs OWDC (and ladder on/off if relevant) | Separate geometry from path selection |
| Optional: pyramid confirming_signal on/off | Fixed portfolio + date range + capital | Isolate TS capture vs fill timing |

Without a matrix, single-run anecdotes (147 vs 148, 163/164, TSMC churn) keep reopening “is the strategy broken?” when the variable was fill path or cohort rank.

---

## Scope

1. Agree fixed lab portfolio, capital, date window, and TS variants.
2. Run ≤4–8 cells (not a grid explosion); record run IDs, equity return, open lots, pass reasons.
3. Classify diffs with `investigate-system-variance` when unexplained.
4. Write short conclusion: OWDC trusted / needs fix / matrix incomplete.

---

## Acceptance

- [ ] Product confirms axes and cell list (or explicitly defers forever)
- [ ] Cell table with PBR IDs + primary metrics landed in analysis or ticket update
- [ ] Path-selection confounds called out when same geometry differs by fill cadence only
- [ ] Open defects filed as issues if any cell fails for non-path reasons

---

## Out of scope

- Implementing new exit strategies
- Heat unit limits (separate ticket)
- Production capital changes
