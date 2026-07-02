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
- `docs/adr/` — architecture decision records (ADR-001..003 seeded)
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

- `/session-report` — audit-grade handoff doc
- `/wrap` — report + commit + push
- `/record` — route finding to issues/tickets/plans/analysis
- `/adversary` — hostile review before committing to a conclusion
- `/stakeholder` — plain-English outward communication
- `/grill-with-docs` — stress-test a plan against CONTEXT.md and ADRs

## Operating discipline

- Promote finished plans from `.grok/sessions/...` into `plans/`.
- Irreversible decisions → `docs/adr/`. Domain rules → `docs/business-context/`. Terms → `CONTEXT.md`.
- Use `/grill-with-docs` before large cross-monolith designs.
- Use `bin/seed-cromwell-workspace` after changing `ai/` assets.

## Current workstream (2026-06)

Read first: `plans/winston-mcp-immediate.md`, then `plans/winston-mcp-next-steps.md`.