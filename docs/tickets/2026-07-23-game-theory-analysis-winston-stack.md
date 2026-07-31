# Ticket: Game-theory analysis of the Winston stack

**Status:** Proposed  
**Date:** 2026-07-23  
**Priority:** P3 — strategic research / methodology design; not blocking paper desk or capital path  
**Scope:** Cross-monolith (WUT lab, Wv2 ops, DM data truth, Cromwell attention) — analysis first, implementation only if findings demand it

## Problem

Winston’s stack encodes a long chain of adversarial decisions — market vs trader, signal vs noise, portfolio construction vs capacity, desk vs broker, EOD doctrine vs alternative timeframes — but we have never framed that chain explicitly in **game-theoretic** terms.

Without that lens we risk:

- Treating portfolio creation, optimization, EOD setups, signal strength, and execution as isolated engineering modules rather than **linked moves** against a non-stationary opponent (the market) and constrained partners (capital, broker, human confirmer).
- Optimizing local objectives (Sharpe on a backtest, fill rate on paper, signal count on DAR) that are **incentive-incompatible** with survival, capacity, or realized edge.
- Defaulting to **EOD trend following** by historical path dependence without a formal comparison to **intraday swing** (or hybrid) strategies on the same capital, cost, and information assumptions.

## Desired outcome

A durable analysis (and optional follow-on plan) that:

1. Maps the Winston decision stack as games (players, information sets, strategies, payoffs, equilibrium concepts where useful).
2. Stresses where our current doctrine is coherent vs where it leaks value or invites adverse selection.
3. Explicitly compares **EOD trend following** vs **intraday swing trading** (and when a hybrid is rational) under Winston’s real constraints (human-gated confirm, parquet/EOD truth, paper → real path, fingerprint law).

**Deliverable home (when work starts):** `ecosystem/docs/analysis/` (technical) and/or `ecosystem/business_analysis/` (capital/stakeholder ranking). Promote irreversible choices to ADR; promote build work to new tickets.

## Analysis scope

### 1. Portfolio creation and optimization (lab → observation → trade-ready)

| Lens | Questions to answer |
|------|---------------------|
| Players | Lab (WUT), principal, capacity constraints, overlapping color books, market regime |
| Strategies | Membership rules, risk %, pyramid, max markets, correlation / diversification, first-pass vs vet gates |
| Payoffs | Return, max DD, trade count, capacity, succession cost (fingerprint churn) |
| Game ideas | Cooperative portfolio design vs zero-sum capacity; multi-objective optimization as bargaining; adverse selection when screening only “easy” history |

Relate to existing first-pass doctrine, color portfolios, PBR/vet paths, and viability gates.

### 2. EOD setups (daily process)

| Lens | Questions to answer |
|------|---------------------|
| Information | What is known at EOD close vs next open? Who moves first (signal → draft → confirm → fill)? |
| Timing game | Signal on close / fill next open as a commitment device vs optionality loss |
| Opponent | Overnight gap, open auction, other participants reacting to same EOD factors |
| Desk game | Human confirmer as imperfectly informed second mover; maker–checker vs auto-paper |

Map DAR → pending action → confirm → journal/fill under ADR-006 / ADR-008 style constraints.

### 3. Signal strength

| Lens | Questions to answer |
|------|---------------------|
| Signaling | Is “strength” a **separating** signal of edge or a **pooling** artifact of parameter fit? |
| Thresholds | Entry filters, confirm-entry matrix, risk scale, attention bands — incentives for over-trading vs under-trading |
| Adversary | Overfit as the market’s reply to published/static rules; regime shift as strategy invalidation |
| Scoring | How should strength rank when capital, correlation, and opportunity cost are strategic, not scalar? |

### 4. Trade execution

| Lens | Questions to answer |
|------|---------------------|
| Players | Desk, broker, market microstructure, optional Cromwell attention |
| Strategies | Market vs limit, stop placement, partials, related-instrument fill, delay to confirm |
| Payoffs | Slippage, gap risk, opportunity cost of waiting, operational error cost |
| Mechanism design | Human-gated fills as costly signaling of conviction; paper autofill as a different game (no broker adversary) |

### 5. Explicit comparison: EOD trend following vs intraday swing trading

**Required chapter of the analysis** — not a side note.

| Dimension | EOD trend (current center of gravity) | Intraday swing (candidate alternative / hybrid) |
|-----------|----------------------------------------|--------------------------------------------------|
| Information set | Daily bars, EOD signals, next-open fills | Intraday bars/radar, session timing, same-day exits |
| Move order | Close → signal → overnight → open | Continuous / session-bound; more moves per day |
| Costs | Lower turnover, overnight gap risk | Spread, commissions, attention, false starts |
| Capacity | Often better for larger books | Often thinner; harder at scale |
| Ops fit | Aligns with DAR, fingerprint, human confirm cadence | Needs radar scope, intraday data truth, different confirm loop |
| Game type | Patient commitment / regime riding | Repeated short games / mean-reversion or momentum skirmishes |

**Answer at minimum:**

- Under what payoff and information assumptions is pure EOD trend **dominant**, **dominated**, or **mixed** with swing?
- What would a fair lab A/B require (data, costs, stop rules, capital, fingerprint freeze)?
- Does Winston’s stack already partially mix (e.g. EOD entry + intraday risk radar) and is that intentional or accidental?
- Recommendation: stay EOD-primary, pilot swing on a set-aside paper OP, or design a formal hybrid doctrine.

## Non-goals (this ticket)

- Implementing a new swing-trading product or rewriting DAR math.
- Changing Engaged OP fingerprints or capital activation policy.
- Claiming a new “optimal” strategy without evidence and principal review.
- LLM inventing indicators or replacing signal math (see loop-engineering / winston-plus-llm non-goals).

## Suggested method (when scheduled)

1. **Inventory** — map current Winston flow (portfolio create → optimize/vet → export → activate → EOD signal → confirm → execute) to game boards; cite code and ADRs, not memory.
2. **Formalize lightly** — players, actions, information, payoffs per stage; use equilibrium language only where it clarifies (no math theater).
3. **EOD vs swing chapter** — assumptions table + qualitative dominance regions + optional lab experiment design.
4. **Findings** — coherent doctrine, leaks, and ranked follow-ups (tickets / ADR / plan).
5. **Stakeholder pass** — short plain-English summary for principal (`/stakeholder` optional).

## Acceptance

- [ ] Analysis document filed under `ecosystem/docs/analysis/` (and business summary if capital-facing).
- [ ] Stack map covers: portfolio creation/optimization, EOD setups, signal strength, trade execution.
- [ ] Dedicated section: **EOD trend following vs intraday swing trading** with recommendation and experiment design if pilot is warranted.
- [ ] Cross-links to relevant ADRs, principles, first-pass doctrine, and any existing intraday radar tickets.
- [ ] Follow-on work split into concrete tickets or a plan (no orphan “we should rethink everything”).
- [ ] Principal reviewed recommendation; priority of any build work set explicitly.

## External frame (Part 0 — filed 2026-07-30)

Berlekamp / Simons read-through is filed as operator business analysis (not a substitute for this ticket’s stack map):

- **`ecosystem/business_analysis/2026-07-30-berlekamp-simons-winston-lessons.md`** — CGT vs Kelly framing, Winston as sum-of-Books, perpendicular Medallion product vs parallel process lessons, impact statement.

Productization of non-TF lanes (swing / options / intraday) is **not** owned by this ticket alone:

- **`docs/tickets/2026-07-30-parallel-trading-system-swing-options-intraday.md`** — parallel system boundary + first-lane ranking.

Sizing science (Kelly-family vs Martingale baseline → Wv2 daily managers):

- **`docs/tickets/2026-07-30-kelly-martingale-sizing-portfolio-management.md`**

This ticket remains open for the full multi-stage game inventory (lab → desk → execution) and the formal EOD TF vs swing dominance chapter.

## Related

- `ecosystem/CONTEXT.md` — domain language and operating model
- `ecosystem/docs/tickets/2026-07-09-first-pass-doctrine-gates-review.md` — doctrine / gates stress
- `ecosystem/docs/tickets/2026-07-19-loop-engineering-evolution-mode.md` — closed-loop verification before evolution
- `ecosystem/docs/tickets/2026-07-13-market-radar-core-portfolio-scope.md` — intraday radar scope (partial swing surface)
- `ecosystem/docs/tickets/2026-07-30-parallel-trading-system-swing-options-intraday.md` — parallel product boundary
- `ecosystem/docs/tickets/2026-07-30-kelly-martingale-sizing-portfolio-management.md` — Kelly / Martingale sizing
- `ecosystem/business_analysis/2026-07-30-berlekamp-simons-winston-lessons.md` — external frame / impact statement
- `ecosystem/docs/adr/ADR-006-operational-portfolio-lineage-and-lifecycle.md` — fingerprint / succession
- `ecosystem/docs/adr/ADR-008-confirmational-entry-and-risk-scale.md` — confirm path / risk scale
- Plans: `portfolio-overlap-rebuild`, `loop-engineering-and-evolution-mode`, `winston-plus-llm` as applicable
