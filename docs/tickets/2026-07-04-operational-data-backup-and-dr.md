# Ticket: Operational data backup and disaster recovery

**Status:** Proposed
**Priority:** P1
**Context:** Sawtooth operational data (parquet tree, Postgres metadata, Redis, configs, Cromwell artifacts) lives on the dev/server host with no periodic off-site backup or exercised DR runbook (2026-07-04).

## Problem

The ecosystem treats parquet as the source of truth and keeps independent Postgres volumes per monolith, but we do not yet:

- Back up those artifacts on a schedule as **operational data** (distinct from git source).
- Store copies in a **secure off-site** location.
- Run a **disaster recovery drill** end-to-end, measure restore time, and optimize the process.

Partial coverage exists today (e.g. WUT `ActiveAccountsBackupJob` → `storage/backups/`), but there is no cross-monolith policy, no off-site transfer, and no validated restore path for DM parquet + all DBs + key bind-mounted files.

## Scope (what must be protected)

| Category | Examples | Notes |
|----------|----------|-------|
| **Parquet (primary)** | `sawtooth_dm_data` → DM `data/` tree | Winston EOD Standard; highest value; reconciliation can rebuild PG from disk |
| **Postgres metadata** | `dm_postgres_data`, `wut_postgres_data`, `wv2_postgres_data` | Markets, portfolios, journals, coverage registry, audit rows |
| **Redis** | `redis_data` (AOF) | Sidekiq queues/schedules; lower priority than parquet/PG but affects in-flight work |
| **Host bind mounts** | `./portfolio_configs`, Cromwell notifier dir, report artifacts | Not in named volumes today |
| **Secrets / credentials** | `eodhd.env`, per-app credentials | Backup **procedure** must exist; ciphertext or env templates only — never plaintext secrets in git |
| **AI / Cromwell workspace** | `ai/data/cromwell-bot/workspace` (seeded from `ecosystem/ai/`) | Recoverable from seed script, but runtime state may differ |

## Goal

Establish a durable backup + DR capability:

1. **Periodic on-server snapshots** of classified operational data.
2. **Off-site copy** to a chosen destination (options below — decision required).
3. **Documented DR runbook** that we **actually execute** at least once, then refine (RPO/RTO, failure modes, operator steps).

## Off-site destination (decision pending)

Evaluate and pick one primary + optional secondary:

| Option | Pros | Cons |
|--------|------|------|
| **Private git repo** | Versioned, familiar | Large parquet/binary unsuitable; LFS cost/limits; secrets risk |
| **Object/cloud storage** (S3, B2, GCS, etc.) | Built for bulk immutable blobs; encryption at rest | Cost, credentials, lifecycle rules |
| **Encrypted thumb drive / NAS** | Air-gap option; no recurring cloud bill | Manual rotation; physical custody |
| **rsync/scp to second host** | Simple | Still need that host secured and backed up |

Human operator involvement is expected for destination credentials, billing, and physical media — agent work covers inventory, scripts, runbooks, and drill automation where possible.

## Acceptance criteria

- [ ] Inventory doc lists every backup target, priority tier, and estimated size growth (`ecosystem/plans/operational-data-backup-dr.md` Phase 1)
- [ ] Scheduled backup job or `bin/` script produces timestamped archives on-server
- [ ] Off-site destination chosen and documented (ADR or deployment note)
- [ ] Off-site transfer runs automatically or via documented operator step with verification (checksum / manifest)
- [ ] DR runbook restores compose stack from **empty volumes** using only backups
- [ ] At least one DR drill completed; results recorded (actual RTO, gaps, follow-up tasks)
- [ ] WUT existing `ActiveAccountsBackupJob` aligned with ecosystem policy (not a one-off)

## Out of scope (for this ticket)

- Continuous replication / hot standby
- Backing up EODHD upstream (re-download + reconcile remains the fallback)
- eta-service-2.0 (separate domain)

## Related

- Plan: [`ecosystem/plans/operational-data-backup-dr.md`](../../plans/operational-data-backup-dr.md)
- Task tracking: [`operational-data-backup-dr.md.tasks.json`](../../plans/operational-data-backup-dr.md.tasks.json)
- `ecosystem/deployment/README.md` — volumes and portability notes
- `winston_unit_test/docs/operations_flow.md` — existing active-accounts backup
- `compose.yml` — volume names (`sawtooth_dm_data`, `*_postgres_data`, `redis_data`)
