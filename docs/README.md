# `docs/` — where each kind of document goes

This is the filing guide for the **ecosystem** repo. It answers: **I have something to write down — which folder does it go in?**

Cross-monolith knowledge also lives in sibling folders at the ecosystem root (`principles/`, `plans/`, `interfaces/`, `deployment/`, `hints/`). This `docs/` tree is for **dated, session-scoped, and work-tracking** artifacts.

## Pick a folder

| If the document is… | It goes in | One-line test |
|---|---|---|
| How we intend to build something (design + step plan) | `../plans/` or `plans/` | "This is a plan for work not yet done." |
| A durable *technical* finding not tied to one defect | `analysis/` | "Future work will consult this as engineering reference." |
| **Business / operator evaluation** (what lab evidence says to trade, rank, promote) | **`../business_analysis/`** | "This is stakeholder- or capital-relevant analysis of results." |
| The investigation of one specific defect | `issues/` | "Something is wrong; here's the root-cause trace." |
| A scoped piece of work that will drive a pull request | `tickets/` | "This is work on the backlog." |
| Active backlog overview | `tickets/INDEX.md` | "What is open and at what priority?" |
| Closed tickets | `tickets/archive/` | "Done / Completed / Superseded." |
| A record of what one work session accomplished | `session-reports/` | "This is what happened on \<date\>." |
| An architecture decision | `adr/` | "We decided X over Y, and here's why." |
| A domain explainer (rules, lifecycle, gates as concepts) | `business-context/` | "This teaches a reader the domain." |
| A repeatable ops procedure | `operations/` | "Diagnosed twice → runbook." |
| An outward-facing message | `communications/` | "This is addressed to a person/team." |
| Brainstorm output before promotion to a plan | `superpowers/specs/` | "Raw design thinking, not yet authoritative." |
| Fully shipped / superseded (non-ticket) | `archive/` | "Done and embedded elsewhere." |

## The five that get confused

- **`issues/`** — defect investigation. One file per defect. Prefer YAML frontmatter from `issues/_template.md` (`triage` → `ready` → …) **and** a plain status banner. Not for trivial one-commit fixes. **Promote defects here** before `lightweight-bug-fix`; do not collapse serious ops/capital bugs into tickets only.
- **`tickets/`** — scoped work driving a PR. Forward-looking. An issue may spawn a ticket. Include `**Priority:** P0–P3|unset`. See [`tickets/INDEX.md`](tickets/INDEX.md).
- **`plans/`** (at `ecosystem/plans/`) — how we'll build something cross-monolith. Bigger and more design-heavy than a ticket.
- **`analysis/`** — standing *technical* reference. Issues and tickets cite analyses rather than repeating them.
- **`../business_analysis/`** — standing *business* evaluation (PBR rankings, paper-first candidates, experiment economics). Not domain glossary; not eng deep-dives.
- **`session-reports/`** — audit-grade record of one session. Written at session end via `/session-report` or `/wrap`.
- **`operations/`** — runbooks. Create when a procedure is explained twice (or blast radius is high). See [`operations/README.md`](operations/README.md).

**How they relate:** plan → build → may surface **issue** → cites analysis → spawns **ticket** → PR → session-report records the session. Cross-system “why differ?” → `investigate-system-variance` / `baseline-replay`.

## Where a "what we did" summary goes

Completion narratives go in the **session report**, not a ticket or plan. Pull deferred follow-ups into **tickets**. Move **Done** tickets into `tickets/archive/`.

## Naming

- **Dated documents:** `YYYY-MM-DD-short-kebab-slug.md`
- **Session reports:** `YYYY-MM-DD-HHMM-<slug>.md`
- **Issues** — `_template.md` + status banner; readiness required before bug-fix lane
- **Tickets** — `**Status:**` (`Proposed` / `In progress` / `Done` / `Blocked`) and `**Priority:**` (`P0`–`P3` / `unset`)

## Monolith repos

Each monolith (`data_manager/`, `winston_unit_test/`, `winston_v2/`) has its own `docs/` for app-scoped session-reports, issues, and tickets. Cross-monolith sessions and most backlog live here in `ecosystem/docs/`.

## Spec-first chain

```
business-context/ (domain rules) + interfaces/ (contracts)
  → plans/ (design) → build → adr/ (irreversible decisions)
  → session-reports/ (audit trail)
```

Promote material decisions from session reports into `adr/`. Promote domain clarifications into `business-context/`. Promote unexpected defects into `issues/`.

## Glossary

Canonical terms: [`../CONTEXT.md`](../CONTEXT.md). Stress-test plans with `/grill-with-docs`.

## Agent skills

`.grok/skills/`:

| Skill | Use |
|-------|-----|
| `session-report`, `wrap` | End-of-session audit + commit |
| `record` | File into the right bucket |
| `manage-issue-ticket` | Evidence-based defect intake → `ready` |
| `lightweight-bug-fix` | Ready issue → test → minimal fix → verify |
| `investigate-system-variance`, `baseline-replay` | Parity / cross-system differences |
| `ship-to-test` | Checks → compose → smoke |
| `rails-code-review` | On each Rails monolith |
| `adversary`, `stakeholder`, `grill-with-docs` | Challenge, communicate, design grill |

## See also

- [`../README.md`](../README.md) — ecosystem index
- [`../CONTEXT.md`](../CONTEXT.md) — domain glossary
- [`../principles/`](../principles/) — core rules
- [`../interfaces/`](../interfaces/) — cross-monolith contracts
- [`adr/`](adr/) — architecture decision records
- [`business-context/`](business-context/) — domain explainers
- [`../business_analysis/`](../business_analysis/) — business / operator portfolio & strategy evaluations
- [`tickets/INDEX.md`](tickets/INDEX.md) — active backlog
- [`operations/`](operations/) — runbooks
- [`../hints/`](../hints/) — gotchas and cues
