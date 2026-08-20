# Ticket: Inventory compose services stuck in (starting)

**Status:** Proposed  
**Priority:** P3  
**Date:** 2026-08-20  
**Monoliths:** ecosystem compose (DM, WUT, Wv2, BG, AI profile)  
**See:** [`docs/session-reports/2026-08-19-1505-dm-pending-migration-telegram.md`](../session-reports/2026-08-19-1505-dm-pending-migration-telegram.md); sibling [`2026-08-20-dm-rails-health-up-404.md`](2026-08-20-dm-rails-health-up-404.md)

## Problem

On 2026-08-19 ~15:05 MDT, `./bin/compose ps` showed many long-running containers as `(starting)` while Postgres/Redis were `(healthy)`:

| Name | Status then |
|------|-------------|
| data_manager | Up 5 hours (starting) |
| data_manager_sidekiq | Up 5 hours (starting) |
| winston_unit_test | Up 9 days (starting) |
| winston_unit_test_sidekiq | Up 2 weeks (starting) |
| winston_v2 | Up 2 days (starting) |
| winston_v2_sidekiq | Up Less than a second (starting) |
| winston_mcp | Up 2 weeks (starting) |
| nanobot_cromwell | Up 2 weeks (starting) |
| broker_gateway / sidekiq | Up 9 days (starting) |
| open-webui | Up 2 weeks (starting) |
| redis, postgres, wut/wv2/bg postgres, ollama | healthy |

Root `compose.yml` healthchecks in source are only on Redis, the four Postgres services, and Ollama. No `HEALTHCHECK` in the Rails `Containerfile`s (grep 2026-08-19). So `(starting)` is unexplained: image HEALTHCHECK, a compose snippet not in the expected file, or Podman reporting `start_period` forever.

Same smell noted earlier: [`docs/session-reports/2026-07-12-1828-six-cohort-evaluate-smoke.md`](../session-reports/2026-07-12-1828-six-cohort-evaluate-smoke.md) — Sidekiq “long starting health but exec worked.”

`winston_v2_sidekiq` “Up Less than a second” may be a restart loop — separate from cosmetic `(starting)`.

## Scope

1. For each `(starting)` service: inspect `podman inspect` / compose healthcheck / image HEALTHCHECK.
2. Classify: no check (display bug) vs failing check vs crash loop.
3. Fix only what is actually failing. Do not add `/up` healthchecks until the DM `/up` 404 ticket is resolved.
4. Record a one-line operator hint in `ecosystem/hints/` if `(starting)` is harmless Podman noise.

## Acceptance

- [ ] Table of service → healthcheck source → pass/fail/none
- [ ] Crash loops (if any) have a follow-up ticket or are fixed
- [ ] `compose ps` is either healthy/up without perpetual `(starting)`, or hints explain the label

## Non-goals

- Redesigning the watchdog (it already probes HTTP from Sidekiq)
- Recreating the whole stack
