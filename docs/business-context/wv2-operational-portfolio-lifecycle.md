# Wv2 Operational Portfolio Lifecycle

**Type:** Domain workflow  
**Related ADR:** ADR-006  
**Glossary:** `CONTEXT.md` — Operational Portfolio, Active, Engaged, Closed, Rebalance, Execution Mode, Capital Activation, Journal, CashEvent  
**Companion:** `wut-to-wv2-handoff.md` (lab → ops import)

## Purpose

Define how an **Operational Portfolio** lives in **Wv2** after handoff: attention, engagement, paper vs real intent, rebalance, close, and **Capital Activation**. Protects risk sizing and performance evaluation once execution (including paper) has started.

**WUT** selects candidates. **Wv2** executes and tasks humans. Wv2 is not end-to-end automated broker trading. Signal vs desk fulfillment (Human-Gated, EOD T/T+1, dual spines): **`human-gated-desk-and-fulfillment.md`** / **ADR-009**.

## Three independent axes

| Axis | Values | Meaning |
|------|--------|---------|
| `export_kind` | observation \| trade_ready | WUT economic promotion at export |
| **Active** | true \| false | Attention: Daily Analysis + human task surface |
| **Execution Mode** | paper \| real | Capital intent (default paper on import) |

Do not derive one from another.

## Lifecycle sketch

```
Import (inactive, usually paper)
    │
    ├─ set Active ──────────────────► Active, not engaged
    │                                      │
    │                              first Journal
    │                                      ▼
    │                               Engaged + Active
    │                                      │
    │              ┌───────────────────────┼───────────────────────┐
    │              │                       │                       │
    │         CashEvent              shape Rebalance            Close
    │       (same series)           (successor A′)         (end signals)
    │              │                       │                       │
    │              ▼                       ▼                       ▼
    │         still Engaged            A closed;              Closed
    │                                 A′ new series           (history kept)
    │
    └─ Capital Activation ($X) ──► new real A′ (Active); paper A not auto-closed
```

**Engaged** is derived: any **Journal** exists. **Closed** is explicit.

## Import → pre-engagement

See `wut-to-wv2-handoff.md` and ADR-006 for lineage (fingerprint, adopt, auto-fork).

- Land **inactive**.  
- Missing `export_kind` → observation.  
- Pre-engagement: same-fingerprint re-import may update methodology/Books/provenance.  
- Display names with fingerprint: `seed · shortHash` always.

## Active (attention)

- Operator (or Cromwell) marks which OPs enter **Daily Analysis** and the human task surface.  
- **Multi-Active is normal and desired** across different seeds / methodologies:
  - **Active paper** — attention on strategies/markets that are too risky or under-researched; soft planning norm ~1–7 concurrent (warn only, not a hard cap)  
  - **Active real** — capital at risk; TS + non-correlated books + way forward; soft planning norm ~1–3 concurrent (warn only, not a hard cap)  
- **Mutex** (unless force) only blocks *conflicting* dual attention:  
  - at most one Active per **seed_name**  
  - at most one Active per identical **Books** symbol set  
  Same-seed / same-Books dual Active remains a short forced experiment, not the default.  
- **Inactive** OPs are the archive/noise queue (expected many per seed). Operator may clean up, remove, or later activate — not daily capital work.  
- **DAR / ops surfaces must make bands super clear:** real Active first, paper Active second, inactive only as hygiene appendix when useful. Do not collapse attention to “sole Active OP” or hide paper behind real.

## Engagement lock

When the first Journal is written (paper or real):

| Mutable | Immutable until close / successor |
|---------|-----------------------------------|
| CashEvents (capital) | Books membership |
| descriptions / some provenance | TradingStrategy linkage & methodology |
| Active flag (attention) | Silent re-import reshape |

Rationale: paper is still execution. Mutating shape mid-series corrupts risk and performance as regime heuristics.

## Rebalance

| Change | Path |
|--------|------|
| Capital only | **CashEvent** on same OP |
| Books and/or TS / fingerprint | **Successor**: close or end signals on A; open A′; journals stay on A |

Optional: store `successor_of` / `rebalanced_from` links for navigation.

## Close

| Execution Mode | Preconditions |
|----------------|---------------|
| **paper** | Soft-close allowed: mark closed, stop signals; open position residue may remain for human cleanup |
| **real** | Flat-required (no open positions; pending journals resolved). Optional force-flatten path |

Closed portfolios:

- Keep journals and history  
- Do not receive new signal evaluation  
- Are not “deleted”

## Capital Activation

Preferred operator speech (Telegram):  
`Make Portfolio Red + Ts10 real with initial capital of $13,986`  
or `Make dd653f33 real with initial capital of $13,986` (fingerprint / short fingerprint of an existing Wv2 unit).

Canonical term: **Capital Activation** (not the same as setting **Active** alone). Avoid “Activate … with capital” in skills — “activate” alone is the **Active** flag.

| Default | Value |
|---------|--------|
| New OP Execution Mode | `real` |
| New OP Active | true |
| Methodology fingerprint | **Same** as source unit (fingerprint ≠ paper/real) |
| Initial capital | Stated $X only (new CashEvent) — **not** paper start or paper terminal equity |
| Prerequisites | Seed OP (Books) and **TradingStrategy** already in **Wv2**; else hard error → import from WUT (not a transfer wizard) |
| Paper A | Not auto-**Closed**; journals/capital unchanged |
| Paper Active (default) | **Auto-deactivate** paper A when real A′ is Active (same seed/Books) |
| Dual Active same seed/Books | **Force** / `keep_paper_active` required |
| Trade-ready / observation | **Soft warn** if not trade_ready — still allow; do not hard-block (human capital hygiene) |

Paper series remains the regime sample (typically inactive after CA). Real series is a separate capital narrative with the **same** recipe fingerprint and a new journal/cash spine.

### Capital top-up (not Capital Activation)

Operator speech (Telegram):  
`Add $5000 to dd653f33` / `We are adding $5000 to Portfolio Red · dd653f33`

| | Capital Activation | CashEvent top-up |
|--|--------------------|------------------|
| Verb | **Make … real** with initial capital $X | **Add** $X **to** fingerprint / OP |
| Result | **New** real OP series | Same OP; capital_base += $X |
| Eligible OPs | Source paper/import unit in Wv2 | **Only Active + real** |
| Paper | N/A (source may be paper) | **Never** — paper lives and dies on initial capital |
| Tool (today) | *deferred* | `wv2_add_cash_event` (exists; must enforce Active+real) |

Do not treat “add capital” as “make real.” Fingerprint resolution: only among **Active real** matches; if multiple, ask; refuse paper / inactive / closed.

### Example

1. Paper `Portfolio Red · a1b2c3d4`, mode=paper, **Active**, initial $20K, equity later $45K, engaged.  
2. Capital Activation: make that unit real with $13,986.  
3. New OP (real, Active, **same fingerprint** `a1b2c3d4…`) with CashEvent $13,986 and empty journal series.  
4. Paper A remains open but is **deactivated** by default (still in archive; not Closed). Dual Active only with force.

## Remove vs close

- **Close** = end signals; keep history (normal).  
- **Remove/delete** = not the primary path; only if no need for regime history (rare). Prefer closed archive.

## Cromwell / MCP (intent)

Expose verbs aligned to this model, e.g.:

- import / list OPs by seed  
- set Active / deactivate (respect mutex)  
- Capital Activation (capital $X, force flags)  
- Close (respect paper vs real preconditions)  
- CashEvent (capital top-up)  
- shape rebalance → successor  

**Implemented (2026-07-17):**

| Verb | Service | Internal API | MCP | Ops shell / rake |
|------|---------|--------------|-----|------------------|
| Close | `Operations::PortfolioCloseService` | `POST /internal/portfolios/close` | `wv2_close_portfolio` | `close_portfolio` / `wv2:portfolios:close` |
| Successor | `Operations::PortfolioSuccessorService` | `POST /internal/portfolios/successor` | `wv2_successor_portfolio` | `successor` / `wv2:portfolios:successor` |
| CashEvent | `Operations::CashEventService` | `POST /internal/cash_events` | `wv2_add_cash_event` | (MCP / API; shell later) |
| Active | `Operations::PortfolioActivationService` | activate/deactivate | existing | `wv2:portfolios:activate` |

Exact tool names live in `interfaces/winston-mcp-tools.md`.  
**Still deferred:** Capital Activation (new real series with stated $X).

## Non-goals

- Automated broker fills end-to-end  
- In-place paper→real on the same capital series  
- Silent name-upsert overwrite of engaged OPs  
- Treating Active as “live money”

## Related

- ADR-006  
- ADR-009 / `human-gated-desk-and-fulfillment.md`  
- `wut-to-wv2-handoff.md`  
- `trade-ready-viability-gates.md`  
- `portfolio-and-trading-strategy-lifecycle.md` (WUT lab + loose coupling)  
- Tickets: fingerprint export refresh, importer export_kind, importer lineage rewrite  
