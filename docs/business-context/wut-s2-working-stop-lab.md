# WUT lab — Turtle S2 Working Stop under resting stop-touch

**Type:** Domain / lab application  
**Monolith:** winston_unit_test (WUT) only  
**Law:** [`turtle-s2-pyramid-and-working-stop.md`](turtle-s2-pyramid-and-working-stop.md)  
**Plan:** `ecosystem/plans/winston-rst-slate-exit-parity-grok-cli.md` workstream B  
**Fill for this pass:** `resting_stop_touch` (RST)

This is how Turtle System 2 (S2) Working Stop phases apply in the WUT Portfolio Backtest Run (PBR) runner. It is **not** a Winston v2 (Wv2) Daily Analysis (DA) spec and does not change Trading Strategy (TS) fingerprint / handoff.

## Recipe gate

S2 here means all three:

- primary entry `Breakout55DayStrategy`
- exit includes `Breakout20DayStrategy`
- stop `move_to_last_entry`

System 1 (S1) 20/10 is out: the 10-day stays in play while adding.

## Gap inventory (B0, 2026-09-13)

| S2 law | WUT under RST before this pass |
|--------|--------------------------------|
| While lots &lt; max, 20-day is **not evaluated** | `TestingStrategy#evaluate_exit` ORs Breakout20 with no lot-count gate. `process_exits` uses `positions.first` only. |
| After maxed, 20-day is watched; Working Stop **becomes** 20-day only when it has **passed** 2N | `PositionManager#update_trailing_stops` does **not** daily-trail under `move_to_last_entry` (correct). There is **no** 20-day ratchet onto `updated_stop`. Maxed 20-day still fires as a **channel exit at close**. |
| Pierce of the Working Stop = one stop-out flatten-all; no parallel Donchian that bar | RST same-bar day loop is **channel exits → entries → pyramids → stops**. A 20-day print can close lot 1 at close **before** 2N is checked. Stop path then loops remaining lots. |
| Fulfillment: touch → stop, gap → open, same session | `update_stops_and_check_hits` already does this for the Working Stop (plus RST same-bar fill freeze). Keep it. |

Call sites: `PortfolioBacktestRunner#process_portfolio_day_same_bar`, `#process_exits`, `#evaluate_market_signals`, `#update_stops_and_check_hits`. Next-open day loop already checks stops first; this pass does not change hybrid / next-open.

## Shipped (B1–B4, RST + S2)

1. **B1** — lots &lt; max: do not run channel `evaluate_exit`. Only 2N + the next pyramid exist.
2. **B2** — on the max-fill bar, Working Stop stays last ± 2N. Watch 20-day from the **next** session (prior-bar window). Never a second protective stop.
3. **B3** — when that 20-day has **passed** 2N (long: 20-day low > 2N; short: 20-day high < 2N), Working Stop **becomes** the 20-day and **replaces** nightly with the current channel. No revert to 2N. Lookback excludes the session bar (same rule as entry). **Desk lock 2026-09-14:** sticky 20D_BO (not doctrine A).
4. **B4** — pierce of the then-current Working Stop flattens every lot (touch / gap-open). No parallel Donchian close.

`skip_s2_channel_exit?` is true for the whole RST+S2 recipe: 20-day is never a close-priced channel exit.

## Not in this pass

- Overnight arm list / entry+pyramid contest (workstream A).
- Fingerprint payload, pack defaults, Wv2 DA.

## Fixtures

`winston_unit_test/spec/services/portfolio_backtest_s2_working_stop_spec.rb`
