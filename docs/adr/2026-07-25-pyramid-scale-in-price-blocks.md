# ADR: Pyramid / scale-in = price blocks (+ optional confirm)

**Status:** Accepted  
**Date:** 2026-07-25  
**Monolith:** winston_unit_test (lab); TS JSON contract for export  

## Context

Scale-in was incorrectly referenced to the **first** entry only, allowing adds on pullbacks (churn). Turtle-style scaling is: **add only when price extends further in the trade’s favor by N ATR (N) from the prior add level.**

## Decision

### Price rule (always on)

- Reference = **last open lot’s execution price** (not first entry).
- Long: `close > last_entry + pyramiding.atr_multiplier × ATR`
- Short: `close < last_entry − pyramiding.atr_multiplier × ATR`
- Default step: **1.0** ATR (Turtles often used **0.5N** with max 4 units; same framework).
- Max lots: `pyramiding.max_positions` (lab default 5).

### Stops (scale-in only)

- Each unit: stop **risk.atr_multiplier × ATR** from **that unit’s** entry (typically 2N).
- `move_to_last_entry`: after an add, move **all** stops to **2N from the newest unit’s entry**.
- **No daily ATR trailing** for scale-in stop strategies.

### Optional confirming signal (default **null**)

TS:

```json
"risk": {
  "pyramiding": {
    "max_positions": 5,
    "atr_multiplier": 1.0,
    "confirming_signal": null
  }
}
```

- `confirming_signal`: `null` | TradingSignalStrategy id or `{ "id", "strategy_class" }`
- When **null**: price block alone is sufficient (pure trend scale-in).
- When **set**: price block **and** that strategy evaluates **true in the open book’s direction** on the signal bar (additional business rule — not a re-fire of the primary breakout).

Initial-entry confirms (`entrance_strategy.confirmation_signals`) remain **entry-only**; they do not apply to pyramids unless also set as `pyramiding.confirming_signal`.

## Consequences

- Clear separation: entry thesis vs scale-in mechanics.
- Knob for step size already exists: `risk.pyramiding.atr_multiplier`.
- Optional confirm is opt-in science / ops discipline, not required for turtle-like path.
