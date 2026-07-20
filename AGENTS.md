# Ecosystem — General Contractor Rules

**Single source of truth** for the Winston / DM / WUT / Wv2 / Cromwell majestic monolith ecosystem.

Before planning, designing, or coding any cross-monolith change, read:

- `principles/` — vision and core rules
- `plans/` — active implementation plans (start with `winston-mcp-immediate.md`)
- `interfaces/` — parquet standard, MCP tools, API contracts
- `deployment/` — Podman compose, env templates
- `hints/` — gotchas and cues
- `CONTEXT.md` — domain glossary (canonical terms)
- `docs/README.md` — filing guide for dated work artifacts
- `docs/adr/` — architecture decision records (ADR-001..005; see especially ADR-005 responsive user pages)
- `docs/business-context/` — domain rules and explainers

## What lives here vs monolith repos

| Knowledge type | Location |
|----------------|----------|
| Cross-monolith principles, contracts, plans | `ecosystem/` |
| App-specific architecture, code, ops | Each monolith repo |
| Session reports (cross-monolith) | `docs/session-reports/` |
| Session reports (single app) | `{monolith}/docs/session-reports/` |
| Cromwell runtime bot skills | `ai/skills/` |
| Developer session skills | `.grok/skills/` |

## Sibling repos (not governed here)

- **`eta-service-2.0/`** — Denali ETA calculation service (.NET). Harvest patterns only; do not merge ADRs or tickets into ecosystem unless a decision truly spans Winston + ETA.

## Session workflow

End every substantive session with `/wrap` or `/session-report`. Skills in `.grok/skills/`:

| Skill | Use |
|-------|-----|
| `/session-report`, `/wrap` | Audit handoff; commit/push |
| `/record` | Route to issues / tickets / analysis / operations / ADRs |
| `manage-issue-ticket` | Defect intake with readiness gate (`docs/issues/_template.md`) |
| `lightweight-bug-fix` | Ready issue → regression test → minimal fix → verify |
| `investigate-system-variance` | WUT/Wv2/DM/agent parity investigations (Winston project-notes) |
| `baseline-replay` | One scoped baseline vs candidate replay |
| `ship-to-test` | Checks → compose → `bin/test-*` / parity smokes |
| `/adversary` | Hostile review before committing to a conclusion |
| `/stakeholder` | Plain-English outward communication |
| `/grill-with-docs` | Stress-test a plan against CONTEXT.md and ADRs |

Rails app review: use `rails-code-review` **inside** `data_manager/`, `winston_unit_test/`, or `winston_v2/` (each has `PROJECT_PROFILE.md`).

## Operating discipline

- Promote finished plans from `.grok/sessions/...` into `plans/`.
- Irreversible decisions → `docs/adr/`. Domain rules → `docs/business-context/`. Terms → `CONTEXT.md`.
- Unexpected defects → `docs/issues/` (not tickets-only); ready issues → `lightweight-bug-fix`.
- Tickets: `**Priority:** P0–P3|unset`; Done → `docs/tickets/archive/`; see `docs/tickets/INDEX.md`.
- Second time you explain an ops ritual → `docs/operations/` runbook.
- Use `/grill-with-docs` before large cross-monolith designs.
- Use `bin/seed-cromwell-workspace` after changing `ai/` assets.

## Current workstream (2026-06)

Read first: `plans/winston-mcp-immediate.md`, then `plans/winston-mcp-next-steps.md`.