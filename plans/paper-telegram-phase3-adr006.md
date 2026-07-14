# Plan: Paper Telegram Phase 3 — ADR-006 Minimum (Safe Paper History)

**Status:** Done (2026-07-14) — **PR 1–4 complete** (ADR-006 minimum for safe paper history)  
**Prerequisite:** Paper Telegram Phase 0–2 done (Blue PBR62 engaged OP `#12`; Grok-like ops shell; MCP deactivate + confirmation skill).  
**Domain law:** [ADR-006](../docs/adr/ADR-006-operational-portfolio-lineage-and-lifecycle.md), [`wv2-operational-portfolio-lifecycle.md`](../docs/business-context/wv2-operational-portfolio-lifecycle.md), [`wut-to-wv2-handoff.md`](../docs/business-context/wut-to-wv2-handoff.md).  
**Roadmap origin:** Paper Telegram viability plan (session plan, 2026-07-14) Phases 0–5.

## Why now

Core paper loop is proven (confirm + next-day position). OP `#12` is **Engaged** (journals exist). Re-import / multi-recipe campaigns without ADR-006 will:

- silent name-upsert wipe regime samples  
- reshape engaged Books/TS mid-series  
- leave Active hygiene as operator discipline only  

Phase 3 is **safe paper history**, not Capital Activation or LEAPs.

## Out of scope (explicit)

| Item | Where it lives |
|------|----------------|
| Capital Activation (real series + MCP) | Ticket `2026-07-09-capital-activation-mcp-telegram.md` — after minimum |
| Close / successor rebalance **services** | Schema columns land in PR 1; verbs later |
| Phase 4 cash inflow + ad-hoc paper fill MCP | Paper roadmap Phase 4 tickets |
| Phase 5 LEAPs | Deferred |
| Fingerprint payload versioning **code** | Ticket design-only until next WUT payload bump |
| WUT-style CRUD UI | Never (ops shell wraps tools only) |

## Current state (gap)

| Surface | Today | ADR-006 target |
|---------|-------|----------------|
| `portfolios` columns | name, active, risk/strategy legacy | + seed_name, fingerprint, execution_mode, export_kind, closed_at, successor_of_id, paper caps |
| `trading_strategies` | name-unique methodology | + fingerprint, fingerprint_payload, wut_trading_strategy_id |
| Import | `find_or_initialize_by(name)` | fingerprint / adopt / auto-fork; engaged refuse; always inactive |
| Activate | unconstrained | seed_name + Books mutex unless force |
| Export JSON | often no fingerprint | fingerprint + WUT TS id on handoff |
| Paper caps | annotation only on blue-pbr62 | enforce 4 / 1× on paper path |

Phase 1 workaround: human-named `Portfolio Blue · PBR62` so static Blue `#7` was not overwritten. That is **not** lineage.

## Definition of done (Phase 3 minimum)

1. Schema persists all ADR-006 lineage / lifecycle fields; backfill safe for existing OPs.  
2. Import uses lineage resolution; never silent upsert-by-name for fingerprinted methodology.  
3. Engaged OP rejects shape mutation via import.  
4. Import always lands inactive; missing `export_kind` → observation.  
5. Activate (rake + internal + MCP) enforces Active mutex with force override.  
6. Reference exports carry fingerprint (or documented legacy warning).  
7. Paper path applies `max_markets=4` and `max_leverage=1×` (normalize or reject; lab uncapped still possible).  
8. Specs + smoke against live `#12` (engaged refuse) and a second-fingerprint fork.

## PR plan (dependency order)

```
PR 1  Schema + model helpers
  │
  ├─► PR 2  Import lineage service (+ export_kind + land inactive)
  │
  ├─► PR 3  Active mutex (needs seed_name)
  │
  └─► PR 4  Fingerprint export refresh + paper caps enforce
```

Capital Activation and close/successor **verbs** are follow-ons, not blockers for “safe re-import of paper recipes.”

---

### PR 1 — Lifecycle schema + model helpers

**Ticket:** `docs/tickets/2026-07-09-wv2-op-lifecycle-schema.md`  
**Monolith:** `winston_v2`

**Columns (portfolios):**

| Column | Type | Notes |
|--------|------|--------|
| `seed_name` | string, indexed | From JSON `name` / bare seed; mutex key |
| `fingerprint` | string, indexed (non-unique) | Full hash; multiple OP series may share methodology |
| `execution_mode` | string, default `"paper"`, not null | `paper` \| `real` |
| `export_kind` | string | `observation` \| `trade_ready`; null until import sets |
| `closed_at` | datetime, nullable | Presence ⇒ closed |
| `successor_of_id` | FK portfolios, nullable | Navigation for later successor path |
| `max_markets_per_portfolio` | integer, nullable | Paper cap surface (enforce in PR 4) |
| `max_leverage` | decimal, nullable | Paper cap surface (enforce in PR 4) |
| `wut_backtest_run_id` | bigint, nullable | Provenance optional |

**Columns (trading_strategies):**

| Column | Type | Notes |
|--------|------|--------|
| `fingerprint` | string, unique where not null | Methodology identity |
| `fingerprint_payload` | jsonb, default `{}` | Canonical payload if provided |
| `wut_trading_strategy_id` | bigint, nullable | Lab provenance |

**Model helpers:**

- `Portfolio#engaged?` — any Journal exists  
- `Portfolio#closed?` — `closed_at.present?`  
- `Portfolio#open_for_signals?` — not closed (Active is separate)  
- `Portfolio.display_name_for(seed_name:, fingerprint:)` — `seed · shortFp` (8 hex) when fingerprint present  
- `Portfolio.derive_seed_name_from_display(name)` — strip ADR short-suffix only  
- Validations: `execution_mode` inclusion; `export_kind` inclusion allow nil  
- Scopes: `open_series` (`closed_at` nil), `by_seed(seed_name)`, `by_fingerprint(fp)`

**Backfill (in migration):**

- `seed_name` ← derive from `name` (or full name if no hex suffix)  
- `execution_mode` ← `"paper"`  
- fingerprint / export_kind / closed_at left null  

**Acceptance:** migrate dev DB; models load fields; helper specs green; no import behavior change yet.

**Does not:** rewrite import, activate mutex, or require fingerprint on existing JSON.

---

### PR 2 — Import lineage service

**Tickets:**  
`2026-07-09-wv2-import-lineage-fingerprint-adopt-fork.md`  
`2026-07-08-wv2-importer-honor-export-kind.md` (fold in)

**Extract** `Operations::PortfolioConfigImporter` (or equivalent) from `wv2.rake` + any internal import path.

**Resolution:**

1. Full fingerprint match → update that OP+TS if **not engaged** (shape); refuse if engaged  
2. No fingerprint match; bare `seed_name` OP exists and Books symbols equal → **adopt** (attach fingerprint, rename display to suffix form)  
3. Else → **auto-fork** new OP + TS  
4. No fingerprint in JSON → legacy bare-name path + loud warning  
5. Always `active: false` on import (ignore JSON `active`)  
6. Missing `export_kind` → store `observation`  
7. Store `seed_name` from JSON `name` (bare seed, not display with suffix)  
8. TS: upsert by fingerprint when present; else legacy name path  

**Acceptance:** re-import new fingerprint does not touch `#12` journals; same-fp pre-engagement idempotent; engaged refuse; specs cover all branches.

---

### PR 3 — Active mutex

**Ticket:** `2026-07-09-wv2-active-mutex-seed-books.md`

On activate (rake, `InternalController`, MCP):

- Refuse if another Active OP shares `seed_name` **or** identical Books symbol set, unless `force`  
- Clear error with conflicting id/name  
- Apply same rules when any future Capital Activation sets Active  

**Acceptance:** seed conflict, Books conflict, force override, no-conflict specs; MCP/internal accept force flag.

---

### PR 4 — Fingerprint exports + paper caps

**Tickets:**  
`2026-07-09-refresh-portfolio-exports-with-ts-fingerprint.md`  
`2026-07-13-enforce-paper-max-markets-and-leverage.md`

**WUT / portfolio_configs:**

- Re-export or patch so nested TS includes `fingerprint`, `wut_trading_strategy_id`  
- blue-pbr62 and color cohort files used for paper must not be forced onto bare-name path  

**Enforce paper caps (prefer both surfaces with override):**

| Policy | Value |
|--------|-------|
| `max_markets` | 4 for paper-intended handoff |
| `max_leverage` | 1× for paper-intended handoff |

Lab uncapped / 3× research remains possible without fighting the gate (observation archives, explicit force).

**Acceptance:** paper import path applies or documents caps; fingerprint present on primary paper configs; smoke import uses lineage not bare name.

---

## Smoke script (end of Phase 3)

```bash
# After PR 1–4
bin/compose exec -T winston_v2 bin/rails db:migrate
bin/compose exec -T winston_v2 bin/rails wv2:portfolios:list

# 1) Engaged refuse: re-import that would reshape #12 → error
# 2) Auto-fork: new fingerprint under seed Portfolio Blue → new OP; #12 journals intact
# 3) Mutex: activate second same seed → blocked; force → ok then deactivate
# 4) Panels/ops shell still list Active + capital for #12
```

## Ticket status tracking

| Ticket | PR | Status |
|--------|-----|--------|
| `2026-07-09-wv2-op-lifecycle-schema.md` | 1 | **Done** (2026-07-14) |
| `2026-07-09-wv2-import-lineage-fingerprint-adopt-fork.md` | 2 | **Done** (2026-07-14) |
| `2026-07-08-wv2-importer-honor-export-kind.md` | 2 | **Done** (folded into importer) |
| `2026-07-09-wv2-active-mutex-seed-books.md` | 3 | **Done** (2026-07-14) |
| `2026-07-09-refresh-portfolio-exports-with-ts-fingerprint.md` | 4 | **Done** (2026-07-14) |
| `2026-07-13-enforce-paper-max-markets-and-leverage.md` | 4 | **Done** (2026-07-14) |
| `2026-07-09-capital-activation-mcp-telegram.md` | later | Proposed (out of Phase 3 min) |
| `2026-07-09-trading-strategy-fingerprint-versioning.md` | later | Design-only |

## Risks

| Risk | Mitigation |
|------|------------|
| Multiple OPs share fingerprint (paper + future real) | Non-unique portfolio fingerprint index; import match may need seed_name + fingerprint + mode later |
| Legacy JSON without fingerprint | Warn + bare-name path; PR 4 shrinks the set |
| Backfill wrong seed_name for human suffixes (`· PBR62`) | Only strip 8-hex ADR suffix; leave human labels as seed_name until re-import |
| Import rewrite mid-engaged production | PR 2 refuses engaged shape mutation; smoke on `#12` first |

## Related

- Paper Phase 0–1 report: `docs/session-reports/2026-07-14-1112-paper-telegram-phase0-1.md`  
- Paper Phase 2 report: `docs/session-reports/2026-07-14-1139-paper-telegram-phase2-ops-shell.md`  
- Cromwell skills Part 2 (MCP ease): `plans/cromwell-ai-skills-part2.md`  
- Ops shell: does not gain mutation paths outside journal/confirm services  

## Immediate next step

**Phase 3 minimum complete (PR 1–4).** Operator verification: see session report `docs/session-reports/2026-07-14-1640-paper-telegram-phase3-wrap.md` § verification runbook.

## Follow-on tickets (not Phase 3 minimum)

| Ticket | Priority | Notes |
|--------|----------|-------|
| `2026-07-09-capital-activation-mcp-telegram.md` | High when going real | Needs schema + mutex + lineage |
| `2026-07-14-wv2-cash-inflow-mcp.md` | Paper Phase 4 | CashEvent MCP |
| `2026-07-14-wv2-ad-hoc-paper-fill-mcp.md` | Paper Phase 4 | Journal without DAR draft |
| `2026-07-14-wv2-close-and-successor-rebalance-services.md` | Medium | Columns exist; verbs missing |
| `2026-07-14-refresh-remaining-color-portfolio-json-fingerprints.md` | Medium | blue-pbr62/red done |
| `2026-07-13-mcp-winston-source-git-home.md` | Hygiene | Host MCP not in git |
| `2026-07-14-workspace-compose-portfolio-configs-tracking.md` | Hygiene | Host JSON not in git |
| `2026-07-09-trading-strategy-fingerprint-versioning.md` | When payload changes | Design-only |
