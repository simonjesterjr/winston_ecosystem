# S2 Working Stop — doctrine A align (2026-09-14)

## Decision
Desk intent = **A**: after pyramid **maxed**, nightly Working Stop = more protective of last-entry 2N and Donchian 20 (`max` long / `min` short). 20-day **silent** while lots &lt; max. **Not** a LEAP profit-target.

## Why realign
Prior B3 text/code used a sticky “20d has **passed** 2N → then follow 20d only (no revert to 2N)”. Desk thought the rule was already better-of each night after max.

## #672 measure (pre-change)
| Bucket | n |
|--------|---|
| Closes | 215 |
| Stop elevated vs original 2N (heuristic) | 117 |
| Stop still near original 2N | 98 |
| Stop ≥15% above strike (fat ITM lock) | 34 |

## Implementation
- Law: `turtle-s2-pyramid-and-working-stop.md`, `wut-s2-working-stop-lab.md` (this pass)
- Code/fixtures: Cursor cloud agent on `simonjesterjr/winston_unit_test` → PR → apply on sawtooth
- Then re-stamp Red LEAP vs #672 before full 7-book panel re-roll


## Reversal (2026-09-14 later)
Desk locked **sticky 20D_BO** as correct; doctrine A undone. Ambiguity was desk reading A as daily-recomputed ATR 2N vs last-entry 2N floor — sticky 20D_BO = last-entry 2N until 20d passes, then follow 20d.
