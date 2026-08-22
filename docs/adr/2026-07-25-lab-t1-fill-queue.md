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

## Addendum (2026-07-26) — hybrid fill switch

Third PBR `fill_cadence` mode (same switch surface as `next_bar_open`):

| Mode | Initial entry | Pyramid |
|------|---------------|---------|
| `same_bar_open` | same bar open | same bar open |
| `next_bar_open` | T+1 open queue | T+1 open queue |
| `hybrid_entry_next_pyramid_same_day` | T+1 open queue | **same-day close (B1)** |

Hybrid keeps this ADR’s morning order for entries (stops → exit fills → entry fills → new signals). Pyramids then fill at **close of signal day T** after the book is live — no open-lookahead on close-based pyramid triggers. Audit stamps: `entry_fill_cadence`, `pyramid_fill_cadence`. Ticket: `2026-07-26-hybrid-fill-entry-next-pyramid-same-day.md`.

**Scored 2026-07-26:** same-day-close hybrid **rejected** as S4 pack default (path-destructive vs pure next_bar).

### Addendum (2026-07-26) — pyramid price-level (resting stop)

Fourth mode: `hybrid_entry_next_pyramid_price_level` — entries T+1 open; pyramids fill when OHLC **touches** `last_entry ± N×ATR` (ATR frozen from last-lot bar; only sessions after last lot). Ops analogy: park buy-stop at known scale-in price. Ticket: `2026-07-26-hybrid-fill-price-level-pyramid.md`.

### Addendum (2026-08-20) — resting stop-touch entries (lab opt-in)

Fifth mode: `resting_stop_touch` — **not** pack default, **not** ADR-009 ops default.

| Leg | Cadence |
|-----|---------|
| Initial entry | `price_level_touch` on the **signal bar** (no T+1 entry queue) |
| Pyramid | existing `price_level_touch` |
| Protective stop | working stop vs bar low/high once live; gap-through stop fills at **open** |

Fill helper: `LabFillCadence.price_level_fill`. Entry level for high/low Donchian: prior-window max high / min low. v1 strategies: `Breakout20DayStrategy` / `Breakout55DayStrategy` and the other `high > max_high` family. Close-confirm recipes are out of v1.

Same-bar OHLC freeze: mid-bar touch (fill = level) does **not** protective-stop on that bar; gap-through (fill = open) may. Ticket: `2026-08-20-wut-resting-stop-touch-fill-cadence.md`.

**Scored 2026-08-21** (Mint S2 #533 vs #532, Yellow S1 #535 vs #534): **do not promote**. Median Δret **−205**, Δdd **+33**. Yellow made more with worse DD. Mint −100% is **not** a clean cadence result: 2026-08-22 diagnosis (`docs/analysis/2026-08-22-mint-resting-stop-touch-ruin.md`) — unadjusted USO/XOP reverse-split jumps × cover-at-open; same-bar stops = 0. Lab switch remains opt-in. Scorecard: `docs/analysis/2026-08-21-resting-stop-touch-v1-scorecard.md`.
