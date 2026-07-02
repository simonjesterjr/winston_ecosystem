# `docs/` — where each kind of document goes

This is the filing guide for the **ecosystem** repo. It answers: **I have something to write down — which folder does it go in?**

Cross-monolith knowledge also lives in sibling folders at the ecosystem root (`principles/`, `plans/`, `interfaces/`, `deployment/`, `hints/`). This `docs/` tree is for **dated, session-scoped, and work-tracking** artifacts.

## Pick a folder

| If the document is… | It goes in | One-line test |
|---|---|---|
| How we intend to build something (design + step plan) | `../plans/` or `plans/` | "This is a plan for work not yet done." |
| A durable technical finding not tied to one defect | `analysis/` | "Future work will consult this as reference." |
| The investigation of one specific defect | `issues/` | "Something is wrong; here's the root-cause trace." |
| A scoped piece of work that will drive a pull request | `tickets/` | "This is work on the backlog." |
| A record of what one work session accomplished | `session-reports/` | "This is what happened on \<date\>." |
| An architecture decision | `adr/` | "We decided X over Y, and here's why." |
| A domain explainer | `business-context/` | "This teaches a reader the domain." |
| An outward-facing message | `communications/` | "This is addressed to a person/team." |
| Brainstorm output before promotion to a plan | `superpowers/specs/` | "Raw design thinking, not yet authoritative." |
| Fully shipped / superseded | `archive/` | "Done and embedded elsewhere." |

## The five that get confused

- **`issues/`** — defect investigation. One file per defect. Status banner: `Open` / `Under investigation` / `Decision pending` / `Fixed in <sha>` / `Won't fix`. Not for trivial one-commit fixes.
- **`tickets/`** — scoped work driving a PR. Forward-looking. An issue may spawn a ticket.
- **`plans/`** (at `ecosystem/plans/`) — how we'll build something cross-monolith. Bigger and more design-heavy than a ticket.
- **`analysis/`** — standing reference. Issues and tickets cite analyses rather than repeating them.
- **`session-reports/`** — audit-grade record of one session. Written at session end via `/session-report` or `/wrap`.

**How they relate:** plan → build → may surface issue → cites analysis → spawns ticket → PR → session-report records the session.

## Where a "what we did" summary goes

Completion narratives go in the **session report**, not a ticket or plan. Pull deferred follow-ups into **tickets**.

## Naming

- **Dated documents:** `YYYY-MM-DD-short-kebab-slug.md`
- **Session reports:** `YYYY-MM-DD-HHMM-<slug>.md`
- **Issues** — status banner at top
- **Tickets** — `Status:` line (`Proposed` / `In progress` / `Done` / `Blocked`)

## Monolith repos

Each monolith (`data_manager/`, `winston_unit_test/`, `winston_v2/`) has its own `docs/session-reports/` for app-scoped sessions. Cross-monolith sessions save here in `ecosystem/docs/session-reports/`.

## Spec-first chain

```
business-context/ (domain rules) + interfaces/ (contracts)
  → plans/ (design) → build → adr/ (irreversible decisions)
  → session-reports/ (audit trail)
```

Promote material decisions from session reports §4 into `adr/`. Promote domain clarifications into `business-context/`.

## Glossary

Canonical terms: [`../CONTEXT.md`](../CONTEXT.md). Stress-test plans with `/grill-with-docs`.

## Agent skills

`.grok/skills/`: `session-report`, `wrap`, `record`, `adversary`, `stakeholder`, `grill-with-docs`.

## See also

- [`../README.md`](../README.md) — ecosystem index
- [`../CONTEXT.md`](../CONTEXT.md) — domain glossary
- [`../principles/`](../principles/) — core rules
- [`../interfaces/`](../interfaces/) — cross-monolith contracts
- [`adr/`](adr/) — architecture decision records
- [`business-context/`](business-context/) — domain explainers
- [`../hints/`](../hints/) — gotchas and cues