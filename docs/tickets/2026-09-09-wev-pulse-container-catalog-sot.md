# Ticket: Pulse container metadata — source of truth (design grill)

**Status:** Proposed
**Priority:** P2
**Mode:** contractor
**Program:** Winston Ecosystem View
**Parent:** [`2026-09-07-winston-ecosystem-view.md`](2026-09-07-winston-ecosystem-view.md)
**Graph nodes:** ecosystem, winston_v2
**Human gates:** Do **not** implement a catalog until a `/grill-with-docs` session picks the source of truth. YAML is one candidate, not the decision.
**DoD:** Grill concludes: what a Pulse cuboid *is* (compose service vs Redis owner vs poster node), where identity/prose lives, and how it stays honest when compose changes. Output is an updated interface paragraph and/or ADR — not a drive-by `runtime.yaml` copy into JS.

## Why

Pulse landing (2026-09-09) shows container metadata on cuboid click (what / for / helps Winston / listen / this sample). The first pass is a **hand-written JS table** in `winston_v2/public/ecosystem/wev-live.js` (`CONTAINERS`). That will drift from `compose.yml` and from `ecosystem/ecosystem_view/catalog/runtime.yaml`.

A wrap follow-up proposed “generate from `runtime.yaml`.” Operator pushback: config-time YAML may be the wrong SoT. Prefer a design session over baking another static file.

## Forks to grill (not pre-decided)

1. **Config-time catalog** — `runtime.yaml` (or compose-derived JSON) is intended topology; Pulse metadata is a projection of Poster. Honest about “not live.” Drift is a regen hook.
2. **Organic / inventory-time** — `ecosystem_view/bin/inventory` (or a cheap Wv2 peek) emits identity from what is actually running: Redis DBs, Sidekiq processes, DM `/internal/pulse`. Prose still needs a home (glossary? node titles on the SVG?).
3. **Hybrid** — Poster/SVG owns identity (`data-id`, `data-parent`, `<title>`); live Pulse owns “this sample”; operator prose stays in CONTEXT / a thin table only for sentences YAML cannot invent.

Related: Pulse must not use `docker.sock`. Host `podman ps` is UNKNOWN on Tailscale. Any “live container” claim has to survive that.

## Not this ticket

- Implementing a YAML→JS pipeline
- Action Cable
- Inventing container health from compose `starting` healthchecks

## See

- Session: [`docs/session-reports/2026-09-09-1445-wev-pulse-named-work.md`](../session-reports/2026-09-09-1445-wev-pulse-named-work.md) §9 / §14
- Catalog today: `ecosystem/ecosystem_view/catalog/runtime.yaml` (intended topology, not live)
- Skill: `/grill-with-docs` against CONTEXT + ADR-001/005 + WEV plan
