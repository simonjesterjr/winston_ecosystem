# ADR-006: Operational Portfolio Lineage and Lifecycle

**Status:** Accepted  
**Date:** 2026-07-09  
**Deciders:** Architecture (via `/grill-with-docs` session)  
**Builds on:** ADR-001  
**Domain context:** `docs/business-context/wv2-operational-portfolio-lifecycle.md`, `docs/business-context/wut-to-wv2-handoff.md`, `docs/business-context/human-gated-desk-and-fulfillment.md`  
**Glossary:** `CONTEXT.md` — Operational Portfolio, Engaged, Closed, Rebalance, Execution Mode, Capital Activation, TradingStrategy fingerprint  
**Fulfillment boundary:** ADR-009

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

Wv2 is an **observation post that tasks humans**, not an end-to-end autotrader. Fulfillment boundary and desk rules: **ADR-009**.

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

- **Active** = included in Daily Analysis + human task surface (not “live money,” not “only one OP”).  
- **Multi-Active across seeds is product intent:** several Active paper OPs (learning / risk) and a smaller set of Active real OPs (capital) run in parallel. Soft planning norms ~1–7 Active paper, ~1–3 Active real (operator horizon ~2 months) — advisory only, never activate/DA hard caps without a new decision.  
- **Mutex** (unless force): at most one **Active** OP per **seed_name**, and at most one **Active** OP per identical **Books** set — prevents duplicate attention on the same recipe/membership; does **not** force a single Active OP ecosystem-wide.  
- Many inactive OPs per seed are normal (regime archive / noise).  
- **DAR and Wv2** must surface attention bands explicitly: Active real → Active paper → inactive hygiene (see ticket `2026-07-16-attention-bands-dar-ops.md`).

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
- **Capital Activation** (prefer speech “**Make** … **real** with capital $X” / “make \<fp\> real …”; avoid “Activate … with capital”):
  - Source recipe must already exist in Wv2 (OP Books + TS); missing → import error, not a wizard  
  - Opens **new** OP series with stated initial CashEvent; **same methodology fingerprint** as source  
  - Defaults: mode `real`, Active true  
  - Does **not** auto-**Close** paper A  
  - **Default:** auto-**deactivate** paper A (same seed/Books) when real A′ is Active; dual Active requires force / keep_paper_active  
  - Non-**Trade-Ready** / observation provenance: **soft warn** in operator reply — do **not** hard-block (capital hygiene is human; refined 2026-07-20 Capital Activation grill)  
  - Paper terminal equity never becomes real capital_base  
  - **CashEvent top-up** (“add $X to fingerprint”): **Active + real only** — never paper (paper series live and die on initial capital as attention tests). Not Capital Activation.

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

### Why soft-warn (not hard-block) on non-trade-ready Capital Activation?

Viability / `export_kind` still inform the operator (warnings, confirmations). Hard-blocking real series was rejected: **capital hygiene is a human duty**; Winston must not pretend software can own the money boundary alone. Soft warn keeps provenance visible without a FORCE_REAL ceremony that becomes ritual.

## Consequences

### Positive

- Regime samples (multiple fingerprints per seed) survive re-vet and re-import  
- Engaged series protect risk and performance integrity  
- Capital Activation matches human Telegram workflow with clear capital_base  
- Attention is banded (real vs paper Active) rather than collapsed to a single OP; same-seed dual Active still requires force  

### Negative

- More OP rows over time (forks, successors) — needs list/filter by seed_name  
- Importer and activate paths must be rewritten vs current name-upsert  
- Schema fields: fingerprint, seed_name, execution_mode, closed_at, successor links  
- Legacy JSON without fingerprint remains a transition footgun until refresh  

### Risks mitigated

- Silent methodology overwrite → fingerprint lineage + auto-fork  
- Corrupted equity curves after mid-stream membership/TS change → engagement lock + successor rebalance  
- Duplicate same-recipe attention → seed_name + Books Active mutex  
- Flat “all Active” noise → DAR/ops attention bands by execution_mode  
- Paper equity mistaken for real capital → Capital Activation new series only  
- Observation configs becoming real capital unnoticed → soft warn + human responsibility (not hard block)  

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
