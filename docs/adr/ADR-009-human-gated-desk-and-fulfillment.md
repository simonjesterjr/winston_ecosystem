# ADR-009: Human-Gated Desk and Fulfillment Boundary

**Status:** Accepted  
**Date:** 2026-07-20  
**Deciders:** Architecture (via `/grill-with-docs`)  
**Builds on:** ADR-006  
**Domain context:** `docs/business-context/human-gated-desk-and-fulfillment.md`  
**Glossary:** `CONTEXT.md` — Human-Gated, Desk Action, Desk Handoff, Desk Workflow, Signal Date, Fill Date, Signal Spine, Booked Capital Spine, Fulfillment, Signaled Entry Rule, Unsignaled Exit Allowance, Working Stop, Stop-Out Reconciliation, Passed Signal

## Context

Wv2 **Daily Analysis** can create draft journals and tasks. Ops also has ad-hoc book/exit tools, Telegram phrases, and a partial desk form. Without a hard boundary, readers and implementers assume one of:

- DA auto-opens/closes **Positions** (especially paper), or  
- Free-form “I bought X” is normal ops entry, or  
- Winston is a broker OMS with full fulfillment truth, or  
- Humans re-rank expected-return alternatives when at capacity.

Alternatives considered:

- **A. Auto-execute paper; human-gate only real** — faster paper; splits modes and poisons process discipline  
- **B. Full autotrader in DA** — not the product; folds fulfillment into the signal engine  
- **C. Human-gated fulfillment with WMS-style prioritization** — DA proposes; desk confirms; signal ≠ OMS  

## Decision

We choose **C: Human-gated desk and fulfillment boundary**.

1. **Daily Analysis never opens or closes Positions.** It may only create draft **Journals**, tasks, **Passed Signals**, and **Desk Handoffs**.  
2. **Real** is always **Human-Gated**. **Paper** still requires confirm today; optional paper autofill and future autotrader are **separate explicit decisions**, not implied by drafts. Future automation is a **separate component**, not DA silently filling.  
3. **EOD cadence (target):** **Signal Date** T → **Fill Date** T+1 next session **open** as default paper/EOD fill story. Dual concepts even if schema is interim single `trade_date`.  
4. **Signaled Entry Rule:** enter/pyramid only against a **methodology-originated** signal (DA draft or algorithm package leg). Naked free-form enter is out of policy (force + audit only).  
5. **Unsignaled Exit Allowance:** exits may be booked without a Winston exit signal (broker/clearing miss, discretionary flatten, a print the engine never computed) with reason + lot linkage. A **Working Stop** pierce Daily Analysis **does** compute is a **signaled** stop-out — see addendum 2026-09-10.  
6. **Capacity contests:** algorithm emits one deterministic **Desk Handoff** package (or algorithmic pass) — not multi-choice ER menus. Multi-leg packages ordered; out-of-order confirm **warns**.  
7. **Dual spines:** **Signal Spine** (methodology/process) + **Booked Capital Spine** (live cash/risk/DAR). Live OP uses booked.  
8. **Stops:** methodology default ATR + **Working Stop** on Position. Daily Analysis evaluates that Working Stop as **methodology** (same Trend Following / Donchian / 2N rules on paper HITL as live). Realization is **Fulfillment** (Stop-Out Reconciliation: required position link, working-stop snapshot, warn on gap). See addendum 2026-09-10.  
9. **Desk Workflow:** every handoff carries a guided Wv2 confirm path link (plus Telegram/shell). Full workflow page is product intent; partial desk form today.  
10. **Engagement:** any **Journal** including draft engages the OP (ADR-006); independent of Active/paper/real.  
11. **Plan Approve (WQ addendum, 2026-08-28; corrected 2026-08-30; IBKR paper 2026-09-06):** On the **WQ Shadow Portfolio** only, the Human-Gated verb is **Plan Approve** of a **Monday Rebalance Plan** (or flatten plan). Approve **locks** the package (buttons disabled). Remaining ready legs run **one at a time** (exits, then rebalances, then enters). dummy_sim Confirm still **books** that lot. On the Interactive Brokers **paper**-bound WQ OP, that Confirm is **Desk Send** of one market **Order Intent**; the journal stays working until matched fill **Accept-Fills** at the print (**ADR-013**). A name that cannot resolve a fill is a per-leg HITL flag, not a plan-wide fail. Reject leaves lots unchanged. Test **blow-away** is allowed only on paper tracking OPs and also clears Quiver target snapshots. Mint / Ops Trend Following / Execution Mode `real` stay per-leg Human-Gated Confirm (book only). Live WQ Schwab write is a later binding change — not implied. Do **not** auto-book or auto-send the whole remaining package on Approve.

## Rationale

- Winston is a **signal and prioritization** system (WMS analogy), not an OMS.  
- Entries must stay methodology-comparable; exits must stay honest about downstream **Fulfillment**.  
- Auto-filling paper without a flag collapses process miss into “strategy.”  
- Free-form enter breaks fingerprint evaluation and the signal spine.

## Consequences

### Positive

- Clear product boundary for DA, desk, Cromwell, and future autotrader  
- Real process misses surface as **Passed Signals** / DAR attention  
- LEAP/packaging and stop-outs fit without pretending stock-share fantasy accounting  

### Negative

- Next-open dual-date machinery, full Desk Workflow, and swap packages are **not fully built**  
- Ad-hoc enter tools must converge (deprecate as normal path)  
- More journal metadata (signal link, stop snapshot, package ids)  

### Risks mitigated

- Silent DA fills → Human-Gated invariant  
- Naked entries → Signaled Entry Rule  
- Fake channel-exit signals to tidy a stop-out ledger → Unsignaled Exit Allowance + reconciliation (a computed Working Stop pierce is **not** fake; it is signaled)  
- Human re-solving strategy at capacity → deterministic Desk Handoff  
- OMS illusion → Fulfillment / dual spines  

## Related

- ADR-006 — OP lineage, engagement, Active, Capital Activation  
- `docs/business-context/human-gated-desk-and-fulfillment.md`  
- `docs/business-context/wv2-operational-portfolio-lifecycle.md`  
- `docs/business-context/daily-analysis-phase1-design.md`  
- `interfaces/winston-mcp-tools.md`  
- `docs/analysis/2026-07-15-winston-journal-vs-trading-ledger.md`  
- Implementation series `adr-009-desk-fulfillment` #1–#6 under `docs/tickets/2026-07-20-*.md` (see INDEX)  
- ADR-013 — fulfillment write (IBKR paper WQ first; Order Intent types stay open for Mint)

## Addendum (2026-09-10) — Working Stop is a methodology signal

**Deciders:** Operator grill 2026-09-10 (paper HITL vs live).  
**Issue:** `winston_v2/docs/issues/2026-09-09-da-20day-exit-under-max-lots.md`

Paper Human-in-the-Loop, Winston Unit Test, Session Order Slate, and live brokered books share one **methodology**. Paper vs live vs Walnut slate differs only in **Fulfillment**.

1. **Signaled stop-out.** A Working Stop pierce Daily Analysis computes (2N GTC, or 20-day Working Stop after Turtle S2 max lots when that channel has passed 2N) is a **Winston signal** (`:stop_out` on the Signal Spine). It is not an invented 20-day/10-day channel exit and not an ad-hoc unsignaled book. `winston_signal: true`. Move-together recipes flatten all open lots on the name.

2. **GTC fill (same session).** Touch → Working Stop price; gap-through → session **open**. Skip the newest lot’s fill bar. This is **not** the default EOD story in decision 3 (channel entries/exits remain Signal Date T → Fill Date T+1 next open).

3. **Fulfillment split (same signal).**
   - Paper dummy_sim (e.g. Mint): DA mints a stop-out draft; Desk Confirm **books** at the simulated GTC fill.
   - Walnut paper Session Order Slate: same Working Stop; protective GTC stop-market is parked; **Accept-Fill** at the DUT print is source of truth. Do not dummy-sim Confirm or send a second order while that GTC is live.
   - Live / brokered: parked GTC; print is the book.

4. **Unsignaled Exit Allowance (narrowed).** Still required for closes Winston **did not compute**: broker/clearing miss, discretionary flatten, a print the engine never saw. Decision 1 still holds: Daily Analysis never opens or closes Positions — Confirm / Accept-Fill does.

5. **Turtle S2.** While lots on the name are under max, 20-day is **not evaluated**. After maxed, 20-day is watched; Working Stop stays 2N until 20-day has passed 2N in the trade’s favor, then Working Stop **is** the 20-day. A pierce of the then-current Working Stop is still a signaled stop-out.

Related: `CONTEXT.md` Working Stop / Unsignaled Exit Allowance / Stop-Out Reconciliation; `docs/business-context/turtle-s2-pyramid-and-working-stop.md`.  
