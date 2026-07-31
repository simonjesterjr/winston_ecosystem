# Ticket: Parallel trading system (swing / options / intraday) reusing Winston rails

**Status:** Proposed  
**Priority:** P2  
**Date:** 2026-07-30  
**Scope:** Cross-monolith product boundary — design first; build only after principal picks a first lane  
**Type:** Feature / research (not a defect — do not file under `docs/issues/`)  
**Rationale source:** `ecosystem/business_analysis/2026-07-30-berlekamp-simons-winston-lessons.md` §3  
**Related prior:** `docs/tickets/2026-07-23-game-theory-analysis-winston-stack.md` (EOD TF vs swing chapter)

---

## Problem

Winston’s center of gravity is **end-of-day (EOD) Trend Following (TF)** with:

- Winston EOD Standard parquet from data_manager (DM)  
- Winston Unit Test (WUT) lab → viability gates → export  
- Winston v2 (Wv2) Operational Portfolios, human-gated desk (ADR-009), fingerprint succession (ADR-006)

The Berlekamp / Simons analysis shows high-value **keys** that do **not** belong inside existing TF TradingStrategy fingerprints:

| Key | Why not inside TF Engaged OPs |
|-----|-------------------------------|
| Shorter holding / higher trial count | Changes edge class, cost model, and DAR cadence |
| Multi-strategy statistical inventory | Different research factory and attribution |
| Edge-conditioned / Kelly-family sizing at high turnover | Different ruin surface; see sizing ticket |
| Options-defined payoffs | Instrument, margin, and fulfillment model |
| Session / intraday timing | New data truth and confirm loop |

Forcing those into current Engaged TF Operational Portfolios would **violate fingerprint law**, scramble performance series, and confuse paper→real hygiene. We need a **parallel system** (named band / family / product surface) that **reuses Winston ecosystem rails** where possible and invents only what the new edge class requires.

---

## Desired outcome

1. Written **product boundary**: what is “core Winston TF” vs “parallel band.”  
2. **Ranked lanes** (swing, options, intraday) with a recommended first pilot.  
3. **Reuse matrix** (DM / WUT / Wv2 / Cromwell) — what stays shared.  
4. **Keys harvested** from Berlekamp analysis into design principles for the parallel band.  
5. Principal sign-off on first lane → spawn concrete bakeoff / data tickets (no orphan “build everything”).

---

## Keys to harvest (from Berlekamp business analysis)

These should shape the parallel system even if Medallion product shape is rejected:

1. **Horizon as first-class design knob** (not an accident of EOD batching).  
2. **Many independent trials** under explicit cost constraints (law of large numbers only after costs).  
3. **Kelly-family sizing** as a shared risk module if lab proves it (`2026-07-30-kelly-martingale-sizing-portfolio-management.md`); reject classic Martingale.  
4. **Ruthless kill** of non-replicating edges; observation book before real capital.  
5. **Story optional, replication mandatory** — but keep desk-interpretable enough for human confirm until auto-paper is deliberately designed.  
6. **Separate research book** (observation Operational Portfolios / paper band) analogous to a RenTec research book — never silent mutation of live TF series.

---

## Reuse vs new (leverage Winston where possible)

| Reuse by default | Likely new / extended |
|------------------|------------------------|
| DM parquet + registry + reconciliation *where bar frequency fits* | Intraday bars; options chains; different suitability rules |
| WUT patterns: Portfolio Backtest Run (PBR), TradingStrategy fingerprint, viability gates, export JSON | New strategy classes, fill models, cost models, experiment keys |
| Wv2 OP lifecycle: paper/real, Active, Engaged, Closed, CashEvent, succession | Possibly different Daily Analysis cadence or task types |
| Cromwell attention / generic MCP portfolio tools | Lane-specific skills later |
| Human-gated desk doctrine until proven otherwise | Optional auto-paper for high-frequency observation only |
| Portfolio Correlation Score (PCS) ideas | May need different correlation definitions per lane |

**Non-goal:** a second full copy of all three monoliths. Prefer **shared rails + parallel methodology family**.

---

## Candidate lanes (rank; do not implement all at once)

| Rank | Lane | Hypothesis | Ecosystem fit | Cost |
|------|------|------------|---------------|------|
| **1 (recommend first)** | **Multi-day swing** (EOD or hybrid 2–10 day holds) | Berlekamp-ish cadence without HFT; higher trial count than classic TF | Reuses EOD parquet; new entries/exits/stops; same desk possible | Medium |
| **2** | **Options-based** defined strategies | Premium / defined-risk payoffs; LEAP/proxy fulfillment already partial | Needs options data + multiplier/risk math; fulfillment_type paths exist | High |
| **3** | **Intraday** | Session momentum / mean-reversion skirmishes | Market radar ticket; new data truth; attention load | Highest |

### Explicit non-lanes (for now)

- Medallion clone / sub-second statistical arbitrage  
- Mutating existing TF Engaged OPs into swing midstream  
- LLM-invented indicators as primary edge  

---

## Scope of work (this ticket)

### Phase A — Design (in scope when ticket is picked up)

1. **Name the boundary** (proposal options for principal): e.g. “Winston Parallel,” “Band B,” `export_kind` / seed-family convention, or separate portfolio namespace.  
2. **First-lane recommendation** with assumptions table (information set, costs, confirm cadence, capital).  
3. **Minimal viable reuse map** — services/APIs that stay shared without forks.  
4. **Fingerprint / succession rules** for parallel recipes (same ADR-006 spirit).  
5. **Data prerequisites** checklist per lane (DM only vs new sources).  
6. Link to game-theory ticket’s EOD vs swing chapter; either complete that section here or spawn a thin plan under `ecosystem/plans/`.

### Phase B — First experiment (follow-on after sign-off)

Not this ticket’s implementation, but must be sketched:

- Frozen capital, paper OP only  
- Sparse strategy pack for multi-day swing (recommended)  
- Cost model honesty  
- Score vs TF control on **separate** series (no joint optimization narrative)

---

## Acceptance

- [ ] Written boundary: parallel vs TF core (principal-readable).  
- [ ] Ranked lanes + **first-lane recommendation** with experiment sketch.  
- [ ] Explicit reuse matrix (DM / WUT / Wv2 / Cromwell).  
- [ ] Harvested Berlekamp keys listed as design principles for the band.  
- [ ] Principal sign-off recorded; follow-on tickets or plan spawned (no orphan mega-build).  
- [ ] Cross-link from Berlekamp business analysis and game-theory ticket.

---

## Non-goals (this ticket)

- Implementing swing/options/intraday strategies in code  
- Changing TF viability gates or S4 pack freezes  
- Production capital on parallel band  
- Full rewrite of DAR for multi-cadence in one PR  

---

## Related

- `ecosystem/business_analysis/2026-07-30-berlekamp-simons-winston-lessons.md`  
- `docs/tickets/2026-07-30-kelly-martingale-sizing-portfolio-management.md`  
- `docs/tickets/2026-07-23-game-theory-analysis-winston-stack.md`  
- `docs/tickets/2026-07-13-market-radar-core-portfolio-scope.md`  
- `docs/tickets/2026-07-19-loop-engineering-evolution-mode.md`  
- `docs/adr/ADR-006-operational-portfolio-lineage-and-lifecycle.md`  
- `docs/adr/ADR-009-human-gated-desk-and-fulfillment.md`  
- Fulfillment LEAP/option paths (Wv2 MCP / journal related-instrument)  
