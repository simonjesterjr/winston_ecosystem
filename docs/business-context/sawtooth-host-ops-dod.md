# Sawtooth host ops — Definition of Done (DoD)

**Date:** 2026-09-21  
**Status:** Desk law (process)  
**Owner:** Sawtooth Ops (primary); Chief of Staff (fallback if Ops down)  
**Related:** Winston Artificial Intelligence Development Life Cycle (AI-DLC); Portfolio Backtest Run (PBR) stamps; Winston Unit Test (WUT) / Winston v2 (Wv2) pulls

## Problem

Background workers run on the Grok Bot computer (“the box”), not on **sawtooth-ai**. They can draft `rails runner` scripts and notes but cannot reliably execute `./bin/compose exec`, live database probes, or container restarts on the host. Calling that “done” caused half-finished stamps (e.g. heat-ON restamps that only landed after Chief of Staff re-ran the script with `machineId`).

## Law

Any Winston task whose success is **“live on sawtooth”** is incomplete until a **host-bound** step has run and been probed.

### Definition of Done (DoD) — host mutation

Before anyone tells the Operator a stamp, cancel, requeue, or pull is finished, all of the following must be true:

1. **Host execution** — command ran on sawtooth-ai via registered-machine Shell (not box-only).
2. **Ids / SHA** — new Portfolio Backtest Run (PBR) ids, or deployed git SHA inside the relevant container, reported explicitly.
3. **Probe** — at least one live check matching the intent (examples: `heat_enabled?` + heat hash present; `status` pending/running/completed; `git rev-parse` in container matches expected merge).
4. **Non-mutation of kept rows** — Operator-kept PBRs untouched unless the ask said otherwise.

A prepared script on the box **without** host ids/SHA/probe is **prep only**, not done.

## Roles

| Role | Duty |
|------|------|
| **Sawtooth Ops** | Primary host runner: CopyFromBox → compose/rails/git/restart → probe → report |
| **Chief of Staff** | Orchestrates handoffs; runs host leg only if Sawtooth Ops is unavailable |
| **Box executors / Grok CLI / cloud agents** | May author scripts and Pull Requests (PRs); must not claim host success |
| **Winston Dev** | Code and PRs; not routine `rails runner` babysitting |
| **Forensics / Scribe** | Consume Ops probe output into analysis / Artificial Intelligence Development Life Cycle (AI-DLC) trail |

## Handoff shape (into Sawtooth Ops)

Include: script or command path, success criteria, explicit “do not mutate …” list, and whether to enqueue jobs. Ops replies with:

```text
action: …
ids: […]
sha: …
heat_enabled: …   # when relevant
status: …
errors: …
```

## Non-goals

- This is **not** an Architecture Decision Record (ADR); it is operational desk law.
- Does not change Trend Following (TF) signal or packaging product rules.
