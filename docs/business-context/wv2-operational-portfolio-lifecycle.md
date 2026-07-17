# Wv2 Operational Portfolio Lifecycle

**Type:** Domain workflow  
**Related ADR:** ADR-006  
**Glossary:** `CONTEXT.md` — Operational Portfolio, Active, Engaged, Closed, Rebalance, Execution Mode, Capital Activation, Journal, CashEvent  
**Companion:** `wut-to-wv2-handoff.md` (lab → ops import)

## Purpose

Define how an **Operational Portfolio** lives in **Wv2** after handoff: attention, engagement, paper vs real intent, rebalance, close, and **Capital Activation**. Protects risk sizing and performance evaluation once execution (including paper) has started.

**WUT** selects candidates. **Wv2** executes and tasks humans. Wv2 is not end-to-end automated broker trading.

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

Operator speech (Telegram):  
`Activate Portfolio Red + Ts10 with initial capital of $13,986`

Canonical term: **Capital Activation** (not the same as setting **Active** alone).

| Default | Value |
|---------|--------|
| New OP Execution Mode | `real` |
| New OP Active | true |
| Initial capital | Stated $X only (new CashEvent) — **not** paper start or paper terminal equity |
| Paper A | Unchanged (not auto-closed, not auto-deactivated) |
| Dual Active same seed/Books | **Force required** to keep paper Active |
| Trade-ready gate | Real requires trade_ready provenance **or** explicit force |

Paper series remains the regime sample that justified the decision. Real series is a separate capital narrative.

### Example

1. Paper `Portfolio Red · a1b2c3d4`, mode=paper, initial $20K, equity later $45K, engaged.  
2. Capital Activation with $13,986.  
3. New OP (real, Active) with CashEvent $13,986 and empty journal series.  
4. Paper A still exists; operator should Close it for hygiene but may leave it running only with force if both Active.

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
- `wut-to-wv2-handoff.md`  
- `trade-ready-viability-gates.md`  
- `portfolio-and-trading-strategy-lifecycle.md` (WUT lab + loose coupling)  
- Tickets: fingerprint export refresh, importer export_kind, importer lineage rewrite  
