# Ticket: Unify compose orchestration (podman-compose vs podman compose)

**Status:** Proposed
**Priority:** P2
**Context:** `bin/compose --profile ai` failed with "container name already in use" when the stack was started by podman-compose but profile commands routed to `podman compose` → docker-compose (2026-07-02).

## Problem

Two compose front-ends manage the same `compose.yml`:

| Tool | How we use it | Issue |
|------|---------------|-------|
| **podman-compose** | Default for `./bin/compose up -d` (no profile) | Sets `io.podman.compose.project=sawtooth` labels |
| **podman compose / docker-compose** | Was used for `--profile` | Does not see podman-compose containers; tries to recreate fixed `container_name` values |

**Workaround shipped (2026-07-02):** `bin/compose --profile` strips `--profile` and sets `COMPOSE_PROFILES` for podman-compose. Documented in `bin/compose` comments.

## Goal

Pick one durable approach so operators never hit orchestrator conflicts:

1. **Migrate fully to `podman compose`** (native) — single tool, profiles native; requires one-time stack recreate or migration runbook.
2. **Stay on podman-compose** — extend `bin/compose` to route *all* verbs (including profile) through podman-compose + `COMPOSE_PROFILES`; document as the only supported path.
3. **Hybrid with detection** — `bin/compose` detects which orchestrator owns running containers and delegates accordingly (more complex).

## Acceptance criteria

- [ ] ADR or deployment note records the chosen orchestrator and why
- [ ] `bin/compose` and `bin/compose --profile ai up -d` work idempotently on a fresh machine and on an existing podman-compose stack
- [ ] `ecosystem/deployment/README.md` documents the single supported compose command(s)
- [ ] No "container name already in use" when switching between core-only and `--profile ai` bring-up
- [ ] Optional: `bin/compose doctor` prints which orchestrator owns the stack and what to run if mismatched

## Out of scope

- Changing container names or compose service layout
- Docker Engine / non-podman runtimes

## Related

- `bin/compose` — profile routing fix (2026-07-02)
- `ecosystem/deployment/README.md`
