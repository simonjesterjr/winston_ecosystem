# Human-Gated Desk and Fulfillment

**Type:** Domain workflow  
**Related ADR:** ADR-009 (boundary), ADR-006 (lifecycle / engagement)  
**Status:** Accepted via `/grill-with-docs` (2026-07-20)  
**Glossary:** `CONTEXT.md` — Human-Gated, Desk Action, Desk Handoff, Desk Workflow, Daily Analysis, Journal, Signal Date, Fill Date, Signal Spine, Booked Capital Spine, Fulfillment, Fulfillment Packaging, Signaled Entry Rule, Unsignaled Exit Allowance, Working Stop, Stop-Out Reconciliation, Passed Signal, Operational Portfolio, Engaged  
**Companions:** `wv2-operational-portfolio-lifecycle.md`, `daily-analysis-phase1-design.md`, `docs/analysis/2026-07-15-winston-journal-vs-trading-ledger.md`

## Purpose

Define how Winston **signals** become desk work and how humans (or a future **separate** automation component) **fulfill** them — without treating Wv2 as a broker OMS or letting **Daily Analysis** mutate lots.

**Winston** = programmatic trend/methodology engine + **prioritization** of desk work (WMS analogy).  
**Fulfillment** = what actually happens in the market. Winston does not assume full fulfillment truth.

## Product boundary (non-negotiable)

| Layer | Does | Does not |
|-------|------|----------|
| **Daily Analysis** | Evaluate **Active** OPs; emit signals; draft **Journals** + tasks; algorithmic **Passed Signals**; **Desk Handoffs** | Open/close **Positions**; invent broker state |
| **Desk Action** | Confirm, exit (incl. unsignaled), update stops, amend drafts before confirm | Re-rank expected returns as the default product |
| **Fulfillment** | Human (or future separate autotrader) realizes signals | Owned end-to-end by DA |

**Execution Mode `real`:** always **Human-Gated**.  
**Paper:** still confirm today. Optional paper autofill and full autotrader are **later explicit decisions**, not implied by draft creation.

## EOD cadence (target; not fully built)

Winston is an **EOD** system:

1. **Signal Date T** — DA fires entrance/exit recommendation → draft **Journal** + task (**Signal Spine**).  
2. **Fill Date T+1** — next session; default fill price = that session’s **open** when known.  
3. Human **Desk Action** confirms (or process misses → **Passed Signal**).

Confirm is allowed from T evening through the action window; prefill next open when DM parquet has it; explicit price override allowed. Unconfirmed past the window → **Passed Signal** (not silent success).

| Mode | Unconfirmed / process miss |
|------|----------------------------|
| Paper | Mostly theoretical / regime impact |
| **Active real** | High attention — possible stakeholder or market/clearing error; DAR must flag for correction |

Casual “I chose to skip” is **not** a normal strategy lever. Algorithmic pass (capacity, no valid swap) is different from process miss.

## Signaled entry vs unsignaled exit

### Signaled Entry Rule

No enter/pyramid **Position** without a **methodology-originated** Winston signal:

- DA draft enter/pyramid **Journal** + task, or  
- Leg of an algorithm **Desk Handoff** package  

Confirm may change **Fulfillment Packaging** (stock → LEAP/option/proxy), units, and price, but must **reference** the signal (`signal_journal_id` / task).  

Naked free-form enter is **out of policy**. Force + audit is the only exception. Transitional ad-hoc book-enter tools must converge.

### Unsignaled Exit Allowance

Exits **may** be booked without a Winston exit signal: stop-outs, broker/clearing misses, downstream errors, discretionary flatten. Do **not** invent fake exit signals to tidy the ledger. Use reason codes + lot linkage.

## Capacity and multi-leg packages

When max markets / pyramid / capital constraints make signals compete:

- The **algorithm** emits **one** deterministic package (or algorithmic **Passed Signal** with reason).  
- Human does **not** re-rank expected returns by default.  
- Force/ad-hoc discretionary override is the escape hatch, not the DAR menu.

**Multi-leg example:** exit ABC (weakest) then enter XYZ:

- **One logical Desk Handoff**, **N** linked journals/tasks, **ordered** (exit first).  
- Each leg has a **Desk Workflow** link.  
- Confirm enter while exit still open → **warn** (and refuse when capacity still full).

WUT backtest has swap evaluators; Wv2 ops must port deterministic packages into handoffs over time. Until then, at-capacity **algorithmic pass** is an acceptable v1 subset — not multi-choice human menus.

## Desk Handoff and Desk Workflow

Every DAR next step should include:

| Artifact | Role |
|----------|------|
| **Desk Handoff** | What / why / band (paper\|real) / links |
| **Desk Workflow** | Guided Wv2 page: review signal → next-open prefill → units/price/stop → packaging → confirm |
| Telegram / shell phrases | Alternate surfaces for the same **Desk Action** |

**Today:** partial — `/operations/desk` prefill, ops panels, DAR `form_path` / `form_url`, MCP/Telegram. **Not** a full journal workflow app. Product intent remains the guided page.

Human may ignore links; ignore past the action window = **process miss**, not strategy design.

## Dual spines

| Spine | Content | Used for |
|-------|---------|----------|
| **Signal Spine** | What fingerprint/DA recommended (size story, next-open, pass/swap reasons) | Methodology & process audit |
| **Booked Capital Spine** | Executed journals, positions, cash | Live OP equity, risk sizing, DAR cash |

Example: signal sized 206 shares ABC; human confirms 2× Jan 2028 LEAP calls → **booked** cash uses contracts × premium × multiplier; **signal** spine keeps the 206 @ next-open story. Do not rewrite booked history to synthetic stock.

## Stops

| Concept | Role |
|---------|------|
| Signal / default stop | ATR × methodology at open (or strategy update) |
| **Working Stop** | Current stop on the open **Position** (desk-updatable) |
| Broker stop | Outside Winston — not system of record |

### Stop-Out Reconciliation

When life stops out a lot:

1. Human books exit linked to **required** `position_id` (or unique open lot).  
2. Journal stores snapshot: `working_stop_at_exit`, `fill_price`, gap, reason e.g. `external_stop`.  
3. **Warn** if \|fill − working_stop\| large; allow confirm with note (no hard-block by default).  
4. No Winston exit signal invented.

Order lifecycle (resting stop orders separate from Position fields) remains **deferred** until this path is insufficient.

## Engagement (restated)

Any **Journal** — including a **draft** on **Signal Date** — **engages** the OP (ADR-006). Shape (Books + TS fingerprint) locks until **Close** or successor **Rebalance**. Independent of **Active**, paper, and real.

Same seed + fingerprint = one series (no parallel second OP). Different fingerprints of the same lab seed = separate OPs and separate journal series.

## Implementation gap checklist (non-normative)

| Capability | Status (as of grill) |
|------------|----------------------|
| DA drafts only (no auto position open/close) | Policy + largely true in code |
| Human confirm / exit / stop tools | Partial (MCP, shell, desk form) |
| Next-open T/T+1 dual date + prefill | **Built** (2026-07-21 — EodCadence + TaskGenerator + confirm) |
| Full Desk Workflow page | **Built** (2026-07-21 — /operations/workflow) |
| Deterministic swap packages in Wv2 DA | **Gap** (WUT lab has evaluators) |
| Stop-out snapshot + gap warn | **Built** (2026-07-21 — StopOutReconciliation) |
| Enforce Signaled Entry Rule on book-enter | **Built** (2026-07-21 — force+notes escape hatch) |
| DAR attention for real process misses | **Thin** |

## Non-goals

- End-to-end broker automation inside DA  
- Assuming Winston state equals market state  
- Multi-choice expected-return menus as default desk UX  
- Order OMS / multi-leg option structures as first-class Positions  
- In-place paper→real capital promotion (ADR-006 Capital Activation)

## Related

- ADR-009 — this boundary  
- ADR-006 — lineage, engagement, Active, Capital Activation  
- `interfaces/winston-mcp-tools.md`  
- `docs/analysis/2026-07-15-winston-journal-vs-trading-ledger.md`  
- Tickets: human-gated desk foundation, ad-hoc fill, journal→ledger series, exit/stop MCP  

## Open implementation follow-ups (tickets filed 2026-07-20)

| # | Ticket | Priority |
|---|--------|----------|
| 1 | [`docs/tickets/2026-07-20-eod-signal-fill-dates-next-open.md`](../tickets/2026-07-20-eod-signal-fill-dates-next-open.md) | P1 |
| 2 | [`docs/tickets/2026-07-20-desk-workflow-guided-confirm-page.md`](../tickets/2026-07-20-desk-workflow-guided-confirm-page.md) | P1 |
| 3 | [`docs/tickets/2026-07-20-enforce-signaled-entry-rule.md`](../tickets/2026-07-20-enforce-signaled-entry-rule.md) | P1 |
| 4 | [`docs/tickets/2026-07-20-stop-out-reconciliation-snapshot.md`](../tickets/2026-07-20-stop-out-reconciliation-snapshot.md) | P1 |
| 5 | [`docs/tickets/2026-07-20-wv2-capacity-swap-desk-packages.md`](../tickets/2026-07-20-wv2-capacity-swap-desk-packages.md) | P2 |
| 6 | [`docs/tickets/2026-07-20-dar-real-process-miss-attention.md`](../tickets/2026-07-20-dar-real-process-miss-attention.md) | P1 |
