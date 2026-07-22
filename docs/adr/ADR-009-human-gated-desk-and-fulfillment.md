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
5. **Unsignaled Exit Allowance:** exits may be booked without a Winston exit signal (stop-out, broker/clearing miss, discretionary flatten) with reason + lot linkage.  
6. **Capacity contests:** algorithm emits one deterministic **Desk Handoff** package (or algorithmic pass) — not multi-choice ER menus. Multi-leg packages ordered; out-of-order confirm **warns**.  
7. **Dual spines:** **Signal Spine** (methodology/process) + **Booked Capital Spine** (live cash/risk/DAR). Live OP uses booked.  
8. **Stops:** methodology default ATR + **Working Stop** on Position; real-world stop-out via **Stop-Out Reconciliation** (required position link, working-stop snapshot, warn on gap).  
9. **Desk Workflow:** every handoff carries a guided Wv2 confirm path link (plus Telegram/shell). Full workflow page is product intent; partial desk form today.  
10. **Engagement:** any **Journal** including draft engages the OP (ADR-006); independent of Active/paper/real.

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
- Fake exit signals to tidy ledger → Unsignaled Exit Allowance + reconciliation  
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
