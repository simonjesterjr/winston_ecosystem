# WUT lab — overnight park list under resting stop-touch

**Type:** Domain / lab application  
**Monolith:** winston_unit_test (WUT) only  
**Plan:** `ecosystem/plans/winston-rst-slate-exit-parity-grok-cli.md` workstream A  
**Fill:** `resting_stop_touch` (RST)  
**Law:** parent ticket `docs/tickets/2026-08-20-resting-session-stop-orders.md` §4 (over-subscription); operator lock 2026-09-13 (Average True Range (ATR) rank, overflow **not armed**, no intra-bar first-to-touch)

This is **not** a Winston v2 (Wv2) Session Order Slate product. WUT has no slate object. The lab stand-in is one ranked **arm list** on `LabFillTicketQueue`: `entry` and `pyramid` parks (protective Working Stop is already the GTC path).

## When parks are built

At the **start** of session T, from the T−1 book (open lots, cash, last known N / Donchian), **before** T’s high/low is used to fill. Unfilled DAY parks expire at the end of T (adjudicate pops them). Next morning rebuilds.

Protective stops are not in this list.

## Candidates (one list)

| Role | When | Park level | ATR for rank / size |
|------|------|------------|---------------------|
| `entry` | Flat name, high/low Donchian primary | Prior-window Donchian high (long) / low (short) | T−1 bar ATR |
| `pyramid` | Open name, lots &lt; max, last fill is a **prior** session | Last fill ± `pyramid_atr_multiplier` × N | ATR of last-lot bar |

Long and short entry on the same flat name are two candidates with the same ATR. First armed wins; the other is not parked (one-cancels-other). Confirmational / skip-after-winner names are not parked (not a price).

## Rank and refuse (before park)

1. `EntryDecisionMaker.rank` — higher ATR first, `market_id` ascending.  
2. Walk that order. **Heat** (`HeatCapacityGate`) sees open Faith units **plus already-armed parks**. Turtle heat on → L1–L4 refuse. Heat off → legacy symbol / portfolio caps with the same armed counts.  
3. **Cash:** reserve notional at park level × planned units (`LabFillTicketQueue`).  
4. Overflow = **not parked** (`PassedSignal` with the heat/cash/cap reason). Do not park everyone and hope.

Size units from risk equity + N at park. Gap fill still sets the stop from **actual fill**.

## Fill

Only armed names may fill. Touch / gap-open via `LabFillCadence.price_level_fill`. Unarmed names that print a breakout do **not** fill. Same-bar first-to-touch is **not** modeled.

## Not in this spec

- Fingerprint / handoff changes  
- Edge (R) A/B (Grok Bot, after fixtures)  
- Wv2 Daily Analysis / Desk Send  

## Fixtures

`winston_unit_test/spec/services/portfolio_backtest_rst_overnight_arm_spec.rb`
