# ADR: Lab T+1 Fill Queue (signal T → adjudicate T+1)

**Status:** Accepted (implementation 2026-07-25)  
**Monolith:** winston_unit_test  
**Related:** ADR-009 ops signal/fill; session close-trigger / fill cadence work  

## Context

Same-bar lab fills and naive next-open fills produced wildly different paths: not because stop math alone, but because **delay without cohort discipline** changed which tickets filled (path selection). Locked product rules (operator session 2026-07-25):

## Decision

### Tickets
- Signal day **T** creates a queue ticket; **single chance**; unfilled at T+1 adjudication → **passed** (expired).
- No multi-day roll (holiday / missing bar → pass).

### Planning on T
- Signals from **price only** (not cash).
- Rank by **ATR@T** (EntryDecisionMaker / ER-family proxy; frozen for ticket life).
- Plan `units_T` and `atr_T` on signal bar.
- **Reserve:** slot/market for each valid ticket; **cash/margin rank-ordered** until deployable free cash is consumed (remainder slot-only).

### Adjudication morning T+1 (strict order)
1. Stops on **live** positions (same session once live).
2. **Exit** queue fills (never capacity-passed).
3. **Entry/pyramid** queue fills, rank order:  
   `units = min(units_T, floor(afford/open_T1))` — never upsize past T.  
   `entry = open_T1`, `stop = entry ± mult × atr_T`.
4. Expire unfilled T tickets → passed + reason.
5. Generate **new** T+1 price signals → enqueue for T+2 (pyramids allowed **same day after fill** as signals for next open).

### Market rules
- One initial entry life until flat; pending blocks second initial entry.
- Opposite signal cancels pending → pass `cancelled_opposite`.
- SoS reverse (confirm-gated) is a separate policy ticket; timing stays T→T+1.
- No parity requirement vs same-bar science.

## Consequences
- Lab default cadence remains configurable (`LabFillCadence`); next_bar_open uses this queue.
- Full-window returns will differ from same-bar; success = non-chaotic T+1 path, smoke ≥ 75% of same-bar return on scoped window.
