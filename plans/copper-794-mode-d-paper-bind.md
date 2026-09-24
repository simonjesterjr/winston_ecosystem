# Plan: Copper #794 → Mode D paper bind (shares-only TS75)

**Status:** Active  
**Date:** 2026-09-24  
**Tickets:** [`docs/tickets/2026-09-24-copper-794-mode-d-paper-bind.md`](../docs/tickets/2026-09-24-copper-794-mode-d-paper-bind.md)  
**Lane:** A (plan + System One + Grok CLI)  
**Operator go:** 2026-09-24 — draft plan, then implement with Grok CLI  

## Problem

Shares-only bakeoffs crowned **Copper Portfolio Backtest Run (PBR) #794** (Winston Unit Test / WUT portfolio **413**, TS75, 1% risk, caps 3/10) as best Edge_R (**0.311**). Existing Wv2 **Mode C** Copper **#1581** is a different fingerprint (LEAP `leap_fulfillment=all`, 2% risk from PBR #710). We need a **new** paper Operational Portfolio (OP) on the Level-1 / shares path that can later take covered calls — that is **Mode D**, not Mode C.

## Mode D doctrine (Operator lock 2026-09-24)

- Mode D is an **opt-in setting** on a Winston v2 (Wv2) portfolio, **not** a column and **not** present on existing paper books.
- Store it in JSON `fulfillment_packaging_policy` as `"fulfillment_mode": "mode_d"`.
- If that key is **blank**, the book stays what it is today: stock-only, or Mode C when `leap_fulfillment` is `all`.
- Pair with `leap_fulfillment=none` (do **not** stuff `mode_d` into `leap_fulfillment`).
- Covered calls are slate opt-in on open **longs** only; never on shorts; never on the entry line; unwind as one Connected Position.
- Interactive Brokers (IBKR) binding comes **after** unbound `dummy_sim` proof. Do not retry long-call BUY (Level-2 blocked).

See CONTEXT glossary **Mode D (fulfillment)** and session [`docs/session-reports/2026-09-24-1227-mode-d-phase-0-1.md`](../docs/session-reports/2026-09-24-1227-mode-d-phase-0-1.md).

## Candidate DNA (promote source)

| Field | Value |
|-------|-------|
| WUT PBR | **794** (twin metrics of heat-absent #784) |
| WUT book | Copper **413** — AMZN, GLD, GOOGL, JNJ, MSFT, PG, TSLA, TSM, WMT, XLE, XLV |
| Strategy | TS75 / Wv2 TradingStrategy **#341** `TurtleV1 S1 Breakout20/10` |
| Risk | **1%** |
| Capital | $30,000 |
| Instrument | **Shares** — `leap_fulfillment=none`; Mode D packaging |
| Heat | Full turtle heat hash knobs **3 / 6 / 10 / 10** + `heat_mode=turtle` (present; scoreboard-inert vs #784) |
| Caps | `max_positions_per_symbol=3`, `max_positions_per_portfolio=10` |
| Fill / stop | `resting_stop_touch` / `move_to_last_entry` × ATR 2 |
| Adapter | `dummy_sim`, `broker_binding_id=nil` until Operator greens IBKR |

**Framing:** promote is **Copper TS75 shares-only 1% caps 3/10** under Mode D. Heat did not improve Edge_R; do not claim a heat-knob win.

## Approach

1. **Land Mode D phases 0–1** on `winston_v2` (+ any Broker Gateway pieces already local) if still uncommitted — prerequisite for honest `fulfillment_mode=mode_d` packaging. Specs + `ecosystem/scripts/mode_d_uat_jev.sh` green.
2. **Mint a new Wv2 OP** (do **not** mutate Mode C Copper #1581 or Indigo/Teal Mode C books). Name clearly (e.g. `Portfolio Copper · mode-d-from-wut-794`). Attach Copper #413 markets; set risk/caps/heat/TS/stop from DNA table; set `fulfillment_packaging_policy` to include `fulfillment_mode: mode_d`; `leap_fulfillment=none`; `dummy_sim`; inactive → activate via PortfolioActivationService.
3. **Probe-before-promote** on #794 DNA + new OP fields (`ecosystem/scripts/probe_before_promote.sh` / v2 gates). Fail closed.
4. **Mode D TestDesk walk** on the new unbound book (`Operations::ModeD::TestDesk`) + Jev UAT script — nouls ≥ 0.85.
5. **Daily Analysis smoke** once: confirm drafts are stock (Mode D), not LEAP Plan A/B, and Capital Fit keys appear when applicable.
6. **Wrap in-band** (session report + ticket Results). IBKR / Client Portal Gateway (CPGW) bind is a **later** Operator gate — out of this phase.

## Grill notes

- Do not convert #1581 Mode C → Mode D in place (different risk, LEAP history, USDU overdrafts on sibling books).
- Teal/Indigo USDU overdrafts (1583/1584) are unrelated blockers for *those* books — not this mint.
- WEV Pulse must not invent health from compose `(starting)`.

## System One harness

**State:** PBR #794 Edge_R 0.311 / TR 168.55 / DD 16.32; bakeoff tickets; Mode D glossary; local Mode D code paths; new OP id after mint.

**Checkpoints:**

| id | type | instructions | pass rule |
|----|------|--------------|-----------|
| not_mode_c | Noul | New OP has leap_fulfillment none/omitted and is not Copper #1581 | noul ≥ 0.85 |
| mode_d_flag | Noul | fulfillment_packaging_policy.fulfillment_mode is exactly mode_d | noul ≥ 0.85 |
| dna_match | Noul | Markets, TS#341, risk 1%, caps 3/10, turtle heat knobs 3/6/10/10, $30k, dummy_sim unbound | noul ≥ 0.85 |
| desk_uat | Noul | Mode D TestDesk + mode_d_uat_jev.sh all nouls ≥ 0.85 | noul ≥ 0.85 |
| promote_framing | Choice | options: mode_d_shares_candidate, heat_knob_win, mode_c_leap | choice = mode_d_shares_candidate ∧ confidence ≥ 0.7 |

**Runner:** deterministic probes first; `jev ask` / `mode_d_uat_jev.sh` on residual.  
**Tee:** every `jev ask` (state + questions + answers) into TUI + wrap.  
**On fail:** stop; do not activate as paper-live narrative; do not IBKR-bind.

## Implementation phases

1. Commit/push Mode D 0–1 if dirty (Wv2 ± BG) + ecosystem script already tracked.
2. Checkpoint → harness `mode_d_flag` on a throwaway or the real mint.
3. Cutover script mint OP from #794 DNA; activate; record id on ticket.
4. Probe-before-promote + TestDesk UAT.
5. In-band wrap; INDEX Done when DoD met.

## Out of scope

- IBKR paper bind / CPGW orders  
- Long-call BUY / Level-2 options prove  
- Mutating Mode C Copper #1581  
- Restamping Teal LEAP #767–#770  
- Claiming heat improved Edge_R  
- Live size-up  
