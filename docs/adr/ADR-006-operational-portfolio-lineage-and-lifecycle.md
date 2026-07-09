# ADR-006: Operational Portfolio Lineage and Lifecycle

**Status:** Accepted  
**Date:** 2026-07-09  
**Deciders:** Architecture (via `/grill-with-docs` session)  
**Builds on:** ADR-001  
**Domain context:** `docs/business-context/wv2-operational-portfolio-lifecycle.md`, `docs/business-context/wut-to-wv2-handoff.md`  
**Glossary:** `CONTEXT.md` — Operational Portfolio, Engaged, Closed, Rebalance, Execution Mode, Capital Activation, TradingStrategy fingerprint

## Context

WUT is the laboratory (candidate selection). Wv2 is the operational component: **Daily Analysis**, journals, and human tasking (paper or real). Handoff is file-based JSON via `portfolio_configs/`.

Problems that accumulated:

1. **Silent overwrite** — `wv2:portfolios:import` used `find_or_initialize_by(name)` for Portfolio and TradingStrategy. Re-vet with a new methodology under the same seed label destroyed the prior regime sample.
2. **Fingerprint vs name** — WUT lab identity is content **fingerprint**; ops used **name** as merge key with no provenance.
3. **Paper = theory myth** — Paper journals in Wv2 are execution for hygiene; mutating Books/TS after journals corrupt risk and performance evaluation.
4. **Capital confusion** — Paper equity ($20K → $45K) is not deployable real capital; promoting intent in place would poison capital_base.
5. **Attention overload** — Many observation variants are useful; many **Active** variants on the same seed or Books set dilute operator focus.

Alternatives considered:

- **A. Keep name-only upsert forever** — simple; erases regime history and engaged series integrity  
- **B. Fingerprint as Wv2 merge key only** — good lineage; date windows in lab fingerprints still fragment ops if used as sole identity without seed hygiene  
- **C. Lineage + lifecycle model** — fingerprint provenance, auto-fork, engagement lock, successor paths, Capital Activation  

## Decision

We choose **C: Operational Portfolio lineage and lifecycle**.

### Roles

| Monolith | Role |
|----------|------|
| **WUT** | Candidate selection lab (markets, strategies, fingerprints, gates, export) |
| **Wv2** | Operations (import, Active attention, journals, close, rebalance, Capital Activation) |
| **Cromwell** | Operator surface (Telegram/MCP) for lifecycle verbs |

Wv2 is an **observation post that tasks humans**, not an end-to-end autotrader.

### Handoff lineage

1. Export may carry full **fingerprint**, WUT TS id, `export_kind`, seed `name`.  
2. When fingerprint is present, OP and TS **display names** always use **seed + short fingerprint suffix** (including first import).  
3. **Lineage match key** = full fingerprint stored on **both** OP and TS (suffix is display-only).  
4. Import resolution:
   - same fingerprint → update that pair (**pre-engagement only** for shape fields)  
   - no match; bare seed OP exists **and** Books symbols match → **adopt** (attach fingerprint, rename to suffix form)  
   - else → **auto-fork** new OP + TS  
5. Legacy JSON without fingerprint → bare-name path (transition only).  
6. Import always lands **inactive**. Missing `export_kind` → treat as **observation**.  
7. Store **seed_name** from JSON `name` for hygiene mutexes.

### Attention hygiene (**Active**)

- **Active** = attention priority for Daily Analysis + human task surface (not “live money”).  
- Default: at most one **Active** OP per **seed_name**, and at most one **Active** OP per identical **Books** set, unless force.  
- Many inactive OPs per seed are normal (regime archive).

### Engagement lock

- First **Journal** (paper or real) **engages** the OP.  
- Engaged: **Books** and **TradingStrategy** immutable until **Closed** or successor **Rebalance**.  
- Capital may still change via **CashEvent**.  
- Silent re-import must not reshape an engaged OP.

### Rebalance

- **Capital only** → CashEvent on same OP.  
- **Shape** (Books and/or TS/fingerprint) → **successor path**: end signals on A, open A′ (journals stay on A).  

### Close

- **Execution Mode** `paper` → soft-close allowed (stop signals; historical residue OK).  
- **Execution Mode** `real` → flat-required before close (optional force-flatten).  
- Closed ≠ deleted; history retained; signals no longer meaningful on that OP+TS series.

### Execution Mode and Capital Activation

- Explicit `paper` | `real` on OP; default **paper** on import. Independent of Active and `export_kind`.  
- **Capital Activation** (operator speech often “Activate … with capital $X”):
  - Opens **new** OP series with stated initial CashEvent  
  - Defaults: mode `real`, Active true  
  - Does **not** auto-close or auto-deactivate paper A  
  - Dual Active same seed/Books requires force  
  - Real requires **Trade-Ready** provenance or explicit force override  
  - Paper terminal equity never becomes real capital_base  

### Three independent axes

| Axis | Meaning |
|------|---------|
| `export_kind` | WUT economic promotion (observation vs trade_ready) |
| **Active** | Attention / Daily Analysis inclusion |
| **Execution Mode** | paper vs real capital intent |

## Rationale

### Why not name-only upsert?

Destroys regime heuristics and can rewrite engaged series mid-flight. Contradicts “performance is a property of fingerprint + series, not seed label alone.”

### Why not promote paper→real in place?

Paper capital path ($20K start, $45K equity) is not the capital the operator will commit ($5K or $50K). Risk sizing and performance attribution require a **new** CashEvent series.

### Why not auto-close paper on Capital Activation?

Operators may want a short dual-run experiment; hygiene is enforced by the **Active** mutex + force, not by destroying paper history.

### Why trade-ready gate on real Capital Activation?

Viability gates exist for the money boundary. Force override preserves operator judgment after paper evidence without making gates advisory-only.

## Consequences

### Positive

- Regime samples (multiple fingerprints per seed) survive re-vet and re-import  
- Engaged series protect risk and performance integrity  
- Capital Activation matches human Telegram workflow with clear capital_base  
- Attention stays laser-focused unless dual-active is explicit  

### Negative

- More OP rows over time (forks, successors) — needs list/filter by seed_name  
- Importer and activate paths must be rewritten vs current name-upsert  
- Schema fields: fingerprint, seed_name, execution_mode, closed_at, successor links  
- Legacy JSON without fingerprint remains a transition footgun until refresh  

### Risks mitigated

- Silent methodology overwrite → fingerprint lineage + auto-fork  
- Corrupted equity curves after mid-stream membership/TS change → engagement lock + successor rebalance  
- Dual attention confusion → seed_name + Books Active mutex  
- Paper equity mistaken for real capital → Capital Activation new series only  
- Observation configs becoming real capital by accident → trade-ready (or force) gate  

## Implementation notes (non-normative)

- Current code (`wv2:portfolios:import`) does **not** implement this ADR yet.  
- Related tickets: export fingerprint refresh, importer honor export_kind, fingerprint versioning.  
- Prefer MCP/Cromwell verbs aligned to glossary: Capital Activation vs set Active vs Close.

## Related

- ADR-001 — majestic monoliths and coordination  
- `CONTEXT.md` — full term set  
- `docs/business-context/wv2-operational-portfolio-lifecycle.md`  
- `docs/business-context/wut-to-wv2-handoff.md`  
- `docs/business-context/trade-ready-viability-gates.md`  
