---
id: ISSUE-20260728-wv2-portfolio-name-resolution-prefers-inactive-and-mutex-recovery-misguide
title: Vague portfolio name resolves to closed inactive OP; active_mutex recovery steers operators to deactivate the live seed
status: in-progress
type: bug
priority: high
created: 2026-07-28
updated: 2026-07-28
labels: [winston_v2, mcp, portfolio-lifecycle, adr-006, name-resolution, cromwell]
related:
  - docs/issues/2026-07-28-telegram-operator-interface-wrong-chatbot-tone.md
  - docs/issues/2026-07-20-historical-dar-morning-telegram-leak.md
  - docs/adr/ADR-006-operational-portfolio-lineage-and-lifecycle.md
  - interfaces/winston-mcp-tools.md
---

# Vague portfolio name resolves to closed inactive OP; active_mutex recovery steers operators to deactivate the live seed

**Status banner:** Under investigation / partial fix in tree — `Operations::PortfolioResolver` + safer `safe_next_step` (2026-07-28)

## Summary

Calling Winston v2 (Wv2) evaluate / `wv2_perform_daily_analysis` with a vague seed-style name (e.g. `"Portfolio Blue"`) resolves to the **oldest** matching row — often a **closed, inactive** Operational Portfolio (OP) — then auto-activates it and hits the ADR-006 Active mutex against the **current** live OP that shares `seed_name`. The HTTP `force_hint` and Cromwell’s Telegram recovery text then recommend deactivating the **live** OP (`#381`), which is the opposite of operator intent for desk daily analysis.

## Problem statement

Operators and agents must be able to address the current Active OP for a seed without reanimating closed lineage members. Mutex recovery copy must not instruct deactivation of the healthy Active OP when the requested name merely matched a dead row.

## Current behavior

1. `InternalController#evaluate_portfolios` and `find_portfolio_by_id_or_name` resolve non-numeric names with:

   ```ruby
   Portfolio.find_by(name: s) || Portfolio.where("name ILIKE ?", "%#{s}%").first
   ```

   No preference for `active`, non-closed, or fingerprint-suffixed display names. `.first` follows primary key order.

2. If the resolved OP is inactive, evaluate **auto-activates** via `PortfolioActivationService` before analysis.

3. ADR-006 mutex correctly blocks two Active OPs with the same `seed_name` (unless `force=true`).

4. Error payload lists the **already-active** conflict and `force_hint`:  
   `"retry evaluate with force=true or deactivate the conflicting OP first"`.

5. Cromwell paraphrases that into Telegram as “deactivate #381 …” even when the operator’s active paper list shows only one Blue.

### Confirmed 2026-07-28 incident

MCP audit `ecosystem/logs/audit/mcp/mcp_audit_20260728.jsonl`, correlation `7e236780-c0d6-46c6-9afd-930ac72497ba`:

```text
Active mutex blocked #7 "Portfolio Blue":
  conflicts with #381 "Portfolio Blue · f4dd31eb" (same_seed_name)
```

DB state (compose `winston_v2` rails runner):

| ID | name | seed_name | active | closed_at |
|----|------|-----------|--------|-----------|
| 7 | Portfolio Blue | Portfolio Blue | false | 2026-07-20 |
| 240 / 241 | Portfolio Blue · 9cf64e64 | Portfolio Blue | false | null |
| **381** | Portfolio Blue · f4dd31eb | Portfolio Blue | **true** | null |

`ILIKE '%Portfolio Blue%'` first match = **#7** (closed). Only **#381** is Active paper Blue.

## Expected behavior

1. **Name resolution** for `id_or_name` / `portfolio_id_or_name` (evaluate, activate, and shared `find_portfolio_by_id_or_name` paths at minimum):
   - Exact id still wins.
   - Exact full display name still wins.
   - Ambiguous substring matches must **prefer Active, non-closed** OPs over inactive/closed ones when a unique Active match exists under that seed/display fragment.
   - If multiple Active matches remain, return a structured ambiguity error (ids + names) rather than silently picking lowest id.
   - Prefer never auto-activating a **closed** OP from evaluate without explicit force/revive semantics.

2. **Mutex / recovery guidance** when activation of OP A is blocked by Active OP B (`same_seed_name` or `identical_books`):
   - State clearly: requested OP, blocking Active OP, reason.
   - Prefer: “use Active OP #B for daily analysis (omit id_or_name or pass #B)” when the caller’s goal is desk analysis.
   - Do **not** lead with “deactivate #B” as the recommended fix for daily analysis.
   - `force=true` remains an explicit dual-Active experiment path (ADR-006), not the default recovery.

3. **Agent layer:** on `active_mutex`, list portfolios or use conflict `id` from payload; do not invent “deactivate the live seed” as first advice.

## Reproduction

### Preconditions

- At least one closed/inactive OP named like seed `"Portfolio Blue"` (e.g. `#7`).
- One Active OP with same `seed_name` and fingerprint display name (e.g. `#381 Portfolio Blue · f4dd31eb`).

### Steps

1. `POST /internal/portfolios/evaluate` (or MCP `wv2_perform_daily_analysis`) with  
   `portfolio_id_or_name: "Portfolio Blue"` (no numeric id).
2. Observe 422 `active_mutex` naming `#7` blocked by `#381`.
3. Optionally call with `id_or_name` omitted or `"381"` / full display name.

### Observed result

- Vague name → #7 → activate attempt → mutex vs #381.
- Hint steers toward deactivating #381 or force dual-active.
- Active list correctly shows only one Blue; operator cannot “see” the other Blue as active (it isn’t).

### Reproducibility

Always given lineage + vague name.

## Environment

- Compose stack; `winston_v2` on host port 3002; paper OPs.
- MCP audit 2026-07-28; parent_correlation_id on the failing call included placeholder `abc123` (separate hygiene smell; see related historical DAR issue).
- Code: `winston_v2/app/controllers/internal_controller.rb` (`evaluate_portfolios`, `find_portfolio_by_id_or_name`); `winston_v2/app/services/operations/portfolio_activation_service.rb`.

## Evidence

| Evidence | Source | What it establishes |
|---|---|---|
| 422 body with `#7` vs `#381` same_seed_name | `ecosystem/logs/audit/mcp/mcp_audit_20260728.jsonl` correlation `7e236780-…` | evaluate tried to activate closed #7 against live #381 |
| Blue lineage table | `bin/compose exec winston_v2 bin/rails runner` 2026-07-28 | only #381 Active; #7 closed; ILIKE first = #7 |
| ILIKE `.first` resolution | `internal_controller.rb` ~200, ~822 | no active/closed preference |
| force_hint text | same controller evaluate/activate error payloads | steers to deactivate conflicting Active OP |
| Operator report | principal 2026-07-28 | Telegram recovery recommended deactivating #381; active list has one Blue |

## Impact and priority

| Area | Impact |
|------|--------|
| Desk ops | Daily analysis / evaluate blocked by self-inflicted activation of dead OP |
| Capital / attention | Wrong recovery can deactivate the live paper OP operators care about |
| Trust | Mutex message looks like dual-Active corruption when desk is healthy |
| Agent quality | Soft recovery amplifies bad `force_hint` into Telegram |

**Priority:** high — blocks legitimate daily path and invites harmful deactivate of live seed.

**Workaround (operators):** omit `portfolio_id_or_name` for full-desk analysis; or pass numeric id / full `"Portfolio Blue · f4dd31eb"`. Do not deactivate #381 for this error. Do not use `force=true` unless intentional dual-Active experiment.

## Scope and preservation requirements

### In scope

- Shared portfolio id-or-name resolution used by internal/MCP evaluate and activate (and ideally other `find_portfolio_by_id_or_name` / ILIKE `.first` call sites with the same pattern).
- `active_mutex` error payload / `force_hint` wording and structured fields (requested vs conflict, suggested safe next step).
- Tests covering: Active preferred over closed same seed fragment; ambiguity when multiple Active; closed not auto-activated from evaluate without explicit policy.
- Optional: Cromwell skill / persona note for `active_mutex` recovery (no deactivate-live-first).

### Must preserve

- ADR-006: at most one Active OP per `seed_name` / identical Books unless `force=true`.
- Numeric id resolution.
- Exact full display name resolution.
- Explicit dual-Active via `force=true` for short experiments.
- Activate/deactivate APIs themselves.

### Out of scope

- Deleting closed OPs or full lineage purge.
- Redesign of seed_name vs fingerprint product model.
- Telegram channel product voice (see related issue).

## Acceptance criteria

- [ ] Given closed `#7 Portfolio Blue` and Active `#381 Portfolio Blue · f4dd31eb`, when evaluate/MCP is called with `portfolio_id_or_name: "Portfolio Blue"`, resolution targets **#381** (or returns ambiguity with both ids) — not silent #7.
- [ ] Given only inactive matches, when evaluate targets a closed OP by vague name, system does **not** auto-activate it into conflict without a clear closed/revive error (or documented force path).
- [ ] Given Active #381, when desk analysis is requested without id, analysis runs with no mutex.
- [ ] `active_mutex` payload documents requested OP id/name, conflict id/name, reason, and a **safe** next-step string that does not lead with “deactivate the live Active OP” for ordinary analysis.
- [ ] Spec coverage for resolution preference and mutex message fields.
- [ ] Existing activate mutex behavior with true dual-Active conflict still blocks without force.

## Investigation notes

**Confirmed:**

- Mutex implementation is correct for true dual-Active same seed; the incident is **not** two Active Blues.
- Failure mode is name resolution + auto-activate on evaluate + recovery copy.
- Same ILIKE `.first` pattern appears in several Operations services (`ad_hoc_exit_service`, `bulk_market_exit_service`, `bulk_stop_update_service`, etc.) — fix should be centralized if possible.

**Hypotheses (not confirmed as sole cause of Telegram text):**

- Cromwell freeform paraphrase of `force_hint` without listing actives or reading `conflicts[]`.
- Cron/session reuse of vague `"Portfolio Blue"` / placeholder `parent_correlation_id: "abc123"`.

## Unknowns and clarifying questions

- [ ] Whether closed OPs should be excluded from all ILIKE resolution by default, or only when an Active same-seed candidate exists (safe default for fix: prefer Active non-closed; exclude closed unless id exact or `include_closed=true`).
- [ ] Product rule for auto-activate-on-evaluate: keep for inactive-open OPs only, or remove auto-activate entirely from perform_daily_analysis (analysis of actives only unless explicit activate tool).

## Dependencies and risks

- ADR-006 lifecycle; MCP tool schemas in `ecosystem/interfaces/winston-mcp-tools.md`.
- Related attention/Telegram product defect does not block this fix but shares the same incident narrative.
- Centralizing resolution touches multiple mutation paths — must not break exact-name and id paths used by ops shell.

## Verification plan

1. Rails specs: name resolution matrix (id, exact display, seed fragment with Active+closed, multi-Active ambiguity).
2. Request specs or service specs: evaluate with `"Portfolio Blue"` fixture pair → no 422 mutex when Active exists; or structured ambiguity.
3. Compose smoke: MCP `wv2_perform_daily_analysis` with no id; with full display name; with bare seed (after fix).
4. Confirm `force_hint` / error JSON in audit no longer recommends deactivating the only live seed as first step.

## History

- 2026-07-28 — Created from operator Telegram report + MCP audit `7e236780-…` + live DB inspection of Blue lineage.
- 2026-07-28 — Implemented `Operations::PortfolioResolver` (prefer Active open over closed/inactive); wired evaluate/activate + ops services; mutex payload gains `safe_next_step` / `requested`; closed OP evaluate returns `portfolio_closed`. Live smoke: `"Portfolio Blue"` → `#381`. Specs green (resolver + activation). Persona/MCP retry guidance updated. Remaining: full AC check after agent observation; mark resolved when Telegram no longer recommends deactivate-live.
