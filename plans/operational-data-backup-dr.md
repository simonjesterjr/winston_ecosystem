# Plan: Operational Data Backup & Disaster Recovery

**Status:** Pending — not scheduled for immediate execution (captured 2026-07-04).

**Task tracking:** [`operational-data-backup-dr.md.tasks.json`](operational-data-backup-dr.md.tasks.json)

**Ticket:** [`docs/tickets/2026-07-04-operational-data-backup-and-dr.md`](../docs/tickets/2026-07-04-operational-data-backup-and-dr.md)

## Context

Sawtooth's valuable operational state spans:

- **DM parquet tree** (`sawtooth_dm_data`) — canonical market data; PG metadata is reconcilable from disk.
- **Three Postgres volumes** — DM, WUT, Wv2 metadata (portfolios, journals, coverage, audit).
- **Redis** — Sidekiq backing store (AOF enabled in compose).
- **Bind-mounted paths** — `portfolio_configs`, Cromwell notifications, generated reports.
- **Partial WUT backup** — `ActiveAccountsBackupJob` exports journals/positions/reports/tasks to JSON under `storage/backups/`; not ecosystem-wide.

There is no periodic off-site backup and no exercised restore path. A real DR drill will surface gaps (volume names, stop/start order, reconciliation rake, secret recovery).

## Principles

- **Parquet first** — protect the DM data tree before optimizing PG dumps; reconciliation is the PG recovery path when parquet is intact.
- **Secrets never in git backups** — document how to restore credentials from operator-controlled stores.
- **Prove it** — a backup policy that has never been restored is unknown policy; run the drill.
- **Operator + agent split** — scripts, inventory, runbooks, and automation on the agent side; cloud accounts, encryption keys, physical media, and billing on the operator side.

## Phasing

### Phase 1 — Inventory & classification

- Enumerate all compose volumes, bind mounts, and host paths worth protecting.
- Assign **tier** (P0 parquet, P1 Postgres, P2 Redis/bind mounts, P3 re-seedable AI workspace).
- Estimate sizes and growth (symbol count, journal history).
- Define target **RPO** (how stale is acceptable) and **RTO** (how long until trading ops resume).

### Phase 2 — On-server backup automation

- Design timestamped archive layout (e.g. `backups/sawtooth/YYYYMMDD-HHMM/`).
- Implement `bin/backup-sawtooth` (or Sidekiq job) that:
  - Dumps each Postgres DB (`pg_dump`) while stack is quiesced or via consistent snapshot strategy.
  - Archives parquet tree (incremental if size warrants; full for v1).
  - Copies bind mounts and WUT `storage/backups/` manifest.
  - Writes `manifest.json` (checksums, sizes, compose git sha, backup tool version).
- Schedule via cron, Sidekiq, or documented manual ritual.
- Retention policy on-server (e.g. keep 7 daily, 4 weekly).

### Phase 3 — Off-site destination

- Compare options: private git (likely **not** for parquet bulk), object storage, encrypted removable media, second host.
- Pick primary destination; document in ADR or `ecosystem/deployment/README.md`.
- Implement transfer (`rclone`, `aws s3 sync`, `restic`, or operator rsync) with encryption.
- Verify remote copy against manifest.

### Phase 4 — DR runbook & first drill

- Write runbook: empty volumes → restore archives → `bin/compose up` → DM reconcile → smoke tests (symbol pull, daily analysis dry run).
- Execute drill on a **non-production** clone or isolated machine if possible; otherwise document production-risk mitigations.
- Record actual RTO, failures, manual steps.
- File session report with findings.

### Phase 5 — Optimize

- Address drill gaps (missing paths, slow parquet copy, PG restore order).
- Automate what was manual; adjust schedule/retention.
- Optional: integrate Cromwell notification on backup success/failure.

## Key artifacts to produce

- `bin/backup-sawtooth` (and optionally `bin/restore-sawtooth-drill`)
- Backup manifest schema
- Off-site transfer config template (non-secret)
- DR runbook in `ecosystem/deployment/`
- ADR or deployment note for off-site choice
- Session report from first completed drill

## Dependencies

- Stable compose volume names (`compose.yml`)
- Operator availability for destination credentials and drill window

## Not in scope

- Multi-region HA, streaming replication
- EODHD re-download as sole recovery (valid fallback, not the plan's focus)
- eta-service-2.0