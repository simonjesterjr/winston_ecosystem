# Ticket: Meaningful container deployment status (beyond perpetual `starting`)

**Status:** Proposed
**Priority:** P1
**Date:** 2026-09-24
**Lane:** B (ops / compose honesty; short harness)
**Implementer:** Grok CLI (Sawtooth Ops host smoke) — Winston Dev only if Operator splits UI work
**DoD:** Operator-facing status for Winston stack containers distinguishes at least: healthy / ready-and-serving / up-but-no-healthcheck / unhealthy-or-restarting — so a service that has been Up for days and still executes is never stuck labeled only `starting`.
**Parent inventory:** [`2026-08-20-compose-starting-healthcheck-inventory.md`](2026-08-20-compose-starting-healthcheck-inventory.md)
**Related:** [`2026-09-09-wev-pulse-container-catalog-sot.md`](2026-09-09-wev-pulse-container-catalog-sot.md) (Pulse must not invent health from compose `starting`); [`2026-08-20-dm-rails-health-up-404.md`](2026-08-20-dm-rails-health-up-404.md)

## Goal

Stop treating Podman/compose `(starting)` as a useful deployment signal. Today Rails monoliths and Sidekiq sit **Up N days (starting)** while Postgres/Redis/Ollama show `(healthy)`. Winston v2 on port 3002 is serving desk work in that state. Operators need a status vocabulary that matches reality (executing vs crash-loop vs truly still starting).

## Context / specimens

Operator report 2026-09-24: `winston_v2` is up but status `starting` for ~2 days; may still exec.

Host snapshot same day (`./bin/compose ps` on sawtooth):

| Name | Status |
|------|--------|
| redis / postgres / wut_postgres / wv2_postgres / bg_postgres / ollama | Up … **(healthy)** |
| winston_v2 | Up 2 days **(starting)** — ports `3002→3000` |
| winston_v2_sidekiq | Up 3 days **(starting)** |
| data_manager (+ sidekiq), winston_unit_test (+ sidekiq), broker_gateway (+ sidekiq), open-webui, winston_mcp, nanobot_cromwell | Up … **(starting)** |

Historical same smell: Aug 2026 inventory ticket (Wv2 Up 2 days starting); [`docs/session-reports/2026-07-12-1828-six-cohort-evaluate-smoke.md`](../session-reports/2026-07-12-1828-six-cohort-evaluate-smoke.md) — Sidekiq long starting but exec worked.

Likely cause class (hypothesis, verify): root `compose.yml` healthchecks only on Redis / Postgreses / Ollama; Rails Containerfiles lack `HEALTHCHECK`, so compose never leaves `starting` once a start_period or missing-check path applies.

## Work items

- [ ] Finish or absorb the Aug 20 inventory table: service → healthcheck source → pass/fail/none (podman inspect + compose + image).
- [ ] Classify each `(starting)` name: **no check (display noise)** vs **failing check** vs **crash / restart loop**.
- [ ] Define operator-facing status contract (compose ps and/or a thin hint / Pulse glance — pick one SoT; do not invent live health via `docker.sock`).
- [ ] Implement the minimal fix path: add real healthchecks where safe **or** suppress perpetual `starting` when no check exists **or** document + hint when the label is known-harmless — preference: honest labels over more green.
- [ ] Do not add Rails `/up` healthchecks until DM `/up` 404 sibling is resolved (or use an alternate path that already 200s).
- [ ] Verify `winston_v2` on `:3002` still serves while status vocabulary is corrected; host smoke after change.
- [ ] One-line operator hint under `ecosystem/hints/` if any residual Podman quirk remains.
- [ ] Close or supersede Aug 20 inventory once this DoD lands; update INDEX.

## System One harness

**State:** compose ps table above; Aug 20 inventory ticket; which services have compose/image healthchecks after inspect.

**Checkpoints:**

| id | type | instructions | pass rule |
|----|------|--------------|-----------|
| starting_lie | Noul | A container Up ≥ 1 day that still executes HTTP/jobs remains labeled only `starting` with no operator explanation | noul ≥ 0.85 → FAIL Done |
| status_vocab | Choice | options: healthchecks_added, no_check_relabeled, hint_only, mixed | choice ≠ hint_only unless inventory proves zero failing checks ∧ Operator greens hint-only |
| wv2_still_serves | Noul | After the status change, Winston v2 desk on :3002 still responds for a known path | noul ≥ 0.85 |

**Runner:** deterministic inspect/`compose ps` first; `jev ask` on residual “is this honest enough for operators?” only. Tee every jev ask (state + questions + answers) into TUI + wrap.
**On fail:** stop · update ticket · do not claim Done.

## CLI seed

```
cwd: /home/johnkoisch/Documents/com/sawtooth
Lane B. Meaningful compose/container status beyond perpetual (starting).
Follow ecosystem/docs/tickets/2026-09-24-compose-container-meaningful-status.md.
Parent inventory 2026-08-20-compose-starting-healthcheck-inventory.md.
Tee every jev ask (state + questions + answers) into TUI + wrap.
Push main. In-band wrap. Host smoke via Sawtooth Ops DoD when touching running stack.
```

### CLI seed — tee Jev System One (default)

At every System One checkpoint in this ticket:

1. Print a clear TUI banner: `=== Jev System One ===`
2. Print the **state** blob (facts / probe JSON / autopsy excerpt) verbatim.
3. Print each question (Noul / Choice / Score) before calling `jev`.
4. Run `jev ask` (desk: `jevctl` / `ecosystem/scripts/jev-desk-helpers.sh`); do not silently skip when `TYPESAFE_API_KEY` is set.
5. Print the JSON answers (and confidence) in the TUI; append the same block to the in-band wrap / ticket Results.
6. Branch fail-closed on harness pass rules. Deterministic probes run first; Jev judges residual semantic smells only.

If Jev is unavailable, print `Jev skipped: <reason>` and continue only if the ticket allows probe-only; never pretend Jev passed. Prefer `jevctl` over the TypeSafe Python SDK.

## Non-goals

- Redesigning the Sidekiq HTTP watchdog
- Recreating the whole stack
- Pulse cuboid catalog SoT (separate grill ticket)
- Claiming live container health over Tailscale without a proven path

## Overnight note (2026-09-24 ~22:00 MT)

I reconfirmed on host `./bin/compose ps`: Rails monoliths + Sidekiq still **Up … (starting)** (Wv2 Up 3 days starting on :3002; WUT Up 37 hours starting) while Redis/Postgreses/Ollama stay **(healthy)**. Specimen still matches DoD. No code change overnight.
