# Ticket: Copper #794 Mode D paper bind (shares-only TS75)

**Status:** In progress  
**Priority:** P1  
**Date:** 2026-09-24  
**Lane:** A (plan + System One + Grok CLI)  
**Implementer:** Grok CLI  
**DoD:** New unbound Wv2 paper OP exists with Copper #794 DNA (TS75 / 1% / caps 3/10 / turtle heat knobs / $30k / shares), `fulfillment_packaging_policy.fulfillment_mode=mode_d`, `leap_fulfillment=none`, Mode D TestDesk + Jev UAT green, probe-before-promote green — **not** a mutate of Mode C Copper #1581; **no** IBKR bind in this ticket.  
**Plan:** [`../../plans/copper-794-mode-d-paper-bind.md`](../../plans/copper-794-mode-d-paper-bind.md)  
**Parents:** [`2026-09-24-shares-ts75-modified-heat-bakeoff.md`](2026-09-24-shares-ts75-modified-heat-bakeoff.md) · [`2026-09-23-shares-only-ts75-vs-ts77-bakeoff.md`](2026-09-23-shares-only-ts75-vs-ts77-bakeoff.md)  
**Mode D wrap:** [`../session-reports/2026-09-24-1227-mode-d-phase-0-1.md`](../session-reports/2026-09-24-1227-mode-d-phase-0-1.md)

## Goal

Graduate the shares-only Copper **#794** fingerprint to a **Mode D** paper book so the desk can trade underlying long/short (and later covered-call opt-ins) on the Level-1 path toward Level 2 — without touching Mode C LEAP Copper #1581.

## Mode D (Operator lock)

Opt-in JSON on the portfolio: `fulfillment_packaging_policy["fulfillment_mode"] = "mode_d"`. Not a column. Blank key ⇒ existing behavior (stock-only, or Mode C when `leap_fulfillment=all`). Use `leap_fulfillment=none` alongside Mode D.

## Context / specimens

| Item | Value |
|------|-------|
| WUT PBR | **794** — Edge_R **0.311**, TR 168.55%, DD 16.32%, 550 trades |
| WUT portfolio | Copper **413** |
| Markets | AMZN, GLD, GOOGL, JNJ, MSFT, PG, TSLA, TSM, WMT, XLE, XLV |
| Wv2 TS | **#341** TurtleV1 S1 Breakout20/10 |
| Do not touch | Mode C Copper **#1581** (LEAP, 2%, from #710) |

Heat knobs on #794 match modified bakeoff (3/6/10/10) but metrics equal heat-absent #784 — promote framing is **Mode D shares candidate**, not heat win.

## Work items

- [ ] Land Mode D phases 0–1 on `winston_v2` main if still dirty (see session wrap); keep `mode_d_uat_jev.sh` on ecosystem.
- [ ] Write cutover script (tmp or analysis) that mints **new** OP from #794 DNA + Mode D flag; dry-run then apply.
- [ ] Activate OP; record `portfolio_id` + name on this ticket.
- [ ] Run probe-before-promote against #794 + new OP fields; fail closed.
- [ ] Run `Operations::ModeD::TestDesk` + `ecosystem/scripts/mode_d_uat_jev.sh`; nouls ≥ 0.85.
- [ ] Optional: one DA cycle smoke — stock packaging, no LEAP candidates.
- [ ] In-band session report; update INDEX when Done.
- [ ] Stop before IBKR / CPGW bind (separate Operator ticket).

## System One harness

**State:** bakeoff scoreboard row #794; Mode D glossary; new OP attrs after mint.

**Checkpoints:**

| id | type | instructions | pass rule |
|----|------|--------------|-----------|
| not_mode_c | Noul | New OP ≠ #1581; leap_fulfillment is none | noul ≥ 0.85 |
| mode_d_flag | Noul | fulfillment_mode is mode_d in packaging policy JSON | noul ≥ 0.85 |
| dna_match | Noul | TS341, 1%, caps 3/10, heat 3/6/10/10, $30k, Copper markets, dummy_sim unbound | noul ≥ 0.85 |
| desk_uat | Noul | TestDesk + mode_d_uat_jev all nouls ≥ 0.85 | noul ≥ 0.85 |
| promote_framing | Choice | mode_d_shares_candidate / heat_knob_win / mode_c_leap | choice = mode_d_shares_candidate ∧ conf ≥ 0.7 |

**Runner:** probes first; tee every `jev ask` into TUI + wrap.  
**On fail:** stop · update ticket · do not claim paper-ready.

## CLI seed

```
cwd: /home/johnkoisch/Documents/com/sawtooth
Lane A. Copper #794 → new Mode D paper OP (shares-only TS75).
Follow ecosystem/plans/copper-794-mode-d-paper-bind.md
and ecosystem/docs/tickets/2026-09-24-copper-794-mode-d-paper-bind.md.

Mode D lock: fulfillment_packaging_policy.fulfillment_mode=mode_d (JSON opt-in, not a column).
Blank key keeps stock-only or Mode C when leap_fulfillment=all. Use leap_fulfillment=none.
Do NOT mutate Mode C Copper #1581. Do NOT IBKR-bind. Do NOT claim heat-knob win.

Prereq: commit Mode D phase 0–1 on winston_v2 if still uncommitted; specs green.
Then mint+activate new OP from WUT #794 / Copper 413 DNA (TS#341, 1%, caps 3/10,
turtle heat 3/6/10/10, $30k, dummy_sim unbound).
Run probe-before-promote + ModeD::TestDesk + ecosystem/scripts/mode_d_uat_jev.sh.
Tee every jev ask (state + questions + answers) into TUI + wrap.
Push main. In-band wrap. Host smoke per Sawtooth Ops DoD when touching running Wv2.
```

### CLI seed — tee Jev System One (default)

At every System One checkpoint in this ticket/plan:

1. Print a clear TUI banner: `=== Jev System One ===`
2. Print the **state** blob (facts / probe JSON / autopsy excerpt) verbatim.
3. Print each question (Noul / Choice / Score) before calling `jev`.
4. Run `jev ask` (desk: `jevctl` / `ecosystem/scripts/jev-desk-helpers.sh`); do not silently skip when `TYPESAFE_API_KEY` is set.
5. Print the JSON answers (and confidence) in the TUI; append the same block to the in-band wrap / ticket Results.
6. Branch fail-closed on harness pass rules. Deterministic probes run first; Jev judges residual semantic smells only.

If Jev is unavailable, print `Jev skipped: <reason>` and continue only if the ticket allows probe-only; never pretend Jev passed. Prefer `jevctl` over the TypeSafe Python SDK.

## Plant (shared watchable)

```bash
cd /home/johnkoisch/Documents/com/sawtooth
SEED=$(sed -n '/^## CLI seed$/,/^## /p'   ecosystem/docs/tickets/2026-09-24-copper-794-mode-d-paper-bind.md   | sed '1d;$d' | sed '/^### CLI seed/,$d' | sed '/^```$/d')
# Prefer shared grok TUI pane; fallback: grok then paste SEED once
```

## Non-goals

- IBKR bind / order send  
- Long-call Level-2 prove  
- Editing #1581 Mode C Copper  
- Teal/Indigo USDU flatten (sibling tickets)  
- Live size-up  

## Results

_(CLI fills)_
