# Turtle S2 — pyramid, 2N stop, 20-day runner

**Type:** Domain / trading rules  
**Applies to:** Trend Following recipes whose Trading Strategy (TS) is System 2 Donchian — 55-day entry, 20-day exit, Average True Range (ATR) unit stop, `move_to_last_entry`. First Operational Portfolio: **Portfolio Walnut** (TS #266 TurtleV1 S2 Breakout55/20).  
**Knobs live on the TS** (do not hardcode 0.5N / 2N / 4 lots in code): `atr_multiplier` (stop distance, Walnut **2**), `pyramid_atr_multiplier` (add step, Walnut **0.5**), `max_pyramid` / `max_positions_per_symbol` (Walnut **4**), `stop_strategy` = `move_to_last_entry`.  
**Glossary:** `CONTEXT.md` — Working Stop, Protective Stop Guardrail, Session Order Slate, Unit Heat, Moment of Truth, Accept-Fill  
**Related:** ADR-013 §7; `docs/adr/2026-07-25-pyramid-scale-in-price-blocks.md`; ticket `2026-09-09-walnut-paper-session-order-slate.md`  
**Origin:** Operator grill 2026-09-09 (IBM walk-through; pyramid step is whatever the TS says)

## Purpose

State when the **2N protective stop** is in force, when the **20-day Donchian exit** is even *evaluated*, and how pyramids park. This is methodology law for the Session Order Slate — not Daily Analysis (DA) as it ships today.

**N** = the ATR the TS uses for unit risk. Stop distance = `atr_multiplier × N`. Add step = `pyramid_atr_multiplier × N`. Exemplars below use round numbers; Walnut uses **0.5N** adds and **2N** stops.

## Two phases on one name

Until that name holds **max lots**, the 20-day breakout is **not evaluated and not in play**. Only 2N and the next add exist at the broker.

Once that name is **maxed**, 20-day **is** evaluated each session. The working stop stays at last-entry 2N until the 20-day trigger has **passed** that 2N level in the trade’s favor. Then the working stop **is** the 20-day, which may ratchet (and may go through the last lot’s purchase — all units profitable — that is good).

## Long walk-through (operator IBM)

Max heat on the name = 4 units. Long IBM. Same mechanic if the TS add step is 0.5N or 1N.

**Three units on:**

| Park | Level | TIF |
|------|--------|-----|
| Protective stop, **all three lots** | 3rd lot purchase **− 2N** | **GTC** (replace only if the stop must move; do not cancel-all) |
| 4th unit | 3rd lot purchase **+ step×N** (Walnut: **+ 0.5N**) | **DAY** stop-market |
| 20-day breakdown | — | **Not evaluated. Not parked.** |

**Fourth unit fills** (Accept-Fill at the DUT print):

| Park | Level | TIF |
|------|--------|-----|
| Protective stop, **all four lots** | 4th lot purchase **− 2N** | **GTC** (`move_to_last_entry`) |
| Further add | — | None — name is maxed |
| 20-day breakdown | Now **evaluated** each session | Not parked until it has **passed** 4th−2N |

**After maxed — 20-day in play:**

- Each night, compute the 20-day Donchian **low** (long) from prior bars (same window rule as the 55-day entry: lookback excludes the session that would break it).
- If that low is still **at or below** 4th−2N → **keep** the GTC 2N stop. 20-day is watched, not used.
- If that low is **above** 4th−2N → **replace** the protective stop with the 20-day low. The 2N GTC comes off. The 20-day **moves** as the window rolls (replace the GTC each night, never cancel-all).
- If IBM keeps trending, the 20-day low can print **above the 4th lot’s purchase**. All four units are then stopped to a **winner**. That is intended.

## Short (mirror)

Stop = last lot purchase **+ 2N**. Next add = last purchase **− step×N**. 20-day is the Donchian **high**, in play only once maxed. Switch when that high is **below** last+2N. A 20-day high that later prints **below** the last short’s purchase means all units would cover at a profit.

## What this is not

- **Not** “always the tighter of 2N and 20-day.” While adding, 20-day does not exist.
- **Not** a daily ATR trail. `move_to_last_entry` only on a **pyramid fill**; 20-day only after **max lots**.
- **Not** two live protective stops on the same name. One Working Stop at the broker.
- **Not** DA’s current 20-day exit task while lots < max. If DA still mints that, it is a recipe gap; the slate rule wins at the broker.

## Session Order Slate mapping

| Role | When | Order |
|------|------|--------|
| Initial 55-day entry | Flat name | DAY stop-market at 55-day high/low |
| Pyramid | Lots < max | DAY stop-market at last fill ± step×N |
| Protective 2N | Any open lots, until 20-day takes over | GTC stop-market at last fill ± 2N; replace on pyramid fill |
| Protective 20-day | Maxed **and** 20-day has passed 2N | GTC stop-market at the 20-day; **replace nightly** as the channel moves |

Unfilled DAY entries/pyramids die at the close and are rebuilt. Protective GTC is replaced, never cancel-all.

## Protective Stop Guardrail

Any open Turtle lot has a Working Stop, so it **must** have a GTC stop-market at the broker (2N or 20-day per the phases above). Evaluate Interactive Brokers open lots vs resting protective stops continuously. A naked lot is a fail, not a gap to notice later. Extra-modal fills of the same signal: stop is still on the underlying; selling the LEAP/related is **HITL**. See `human-gated-desk-and-fulfillment.md`.
