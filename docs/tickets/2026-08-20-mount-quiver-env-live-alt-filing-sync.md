# Ticket: Mount quiver.env and run live Alt Filing sync

**Status:** Proposed  
**Priority:** P2  
**Date:** 2026-08-20  
**Monoliths:** data_manager (DM), ecosystem compose  
**See:** [`docs/session-reports/2026-08-18-2032-git-free-cash-quiver.md`](../session-reports/2026-08-18-2032-git-free-cash-quiver.md); [`docs/session-reports/2026-08-19-1505-dm-pending-migration-telegram.md`](../session-reports/2026-08-19-1505-dm-pending-migration-telegram.md); ADR-011

## Problem

Alt Filing code and Sidekiq cron (`quiver_alt_sync` 16:00 MT weekdays, `QuiverSyncJob`) are in DM. Live sawtooth still cannot fetch Quiver:

- **Done 2026-08-19:** migration `20260819000000_create_quiver_filings_and_sync_runs` applied on compose Postgres (schema version `20260819000000`).
- **Still open:** `ecosystem/deployment/quiver.env` is not mounted on `data_manager` / `data_manager_sidekiq`. Root `compose.yml` `env_file` for those services is `eodhd.env` (+ `watchdog.env` on Sidekiq) only. Without `QUIVER_API_KEY`, `QuiverClient` raises and the 16:00 job cannot persist filings.

Template: `ecosystem/deployment/quiver-env-template.txt`. Runbook: `ecosystem/deployment/README.md` (mount on DM only — never WUT, Wv2, or MCP).

Promoted from the 2026-08-18 session report §10/§14 (was session-only, not a ticket). Migrate half of that open question is done.

## Scope

1. Confirm `quiver.env` exists on the host (gitignored) and contains `QUIVER_API_KEY`.
2. Add `ecosystem/deployment/quiver.env` to `env_file` for `data_manager` and `data_manager_sidekiq` only. Recreate those two services so env is loaded.
3. Smoke: `./bin/compose exec -T data_manager bin/rails data:quiver_sync` (or equivalent) → `quiver_filings` count > 0; `GET /internal/alt/quiver` returns rows.
4. Confirm weekday 16:00 MT cron has the key in the Sidekiq process (`QuiverSyncJob`).

## Acceptance

- [ ] `data_manager` and `data_manager_sidekiq` have `QUIVER_API_KEY` in env (not in git)
- [ ] One successful live sync writes `quiver_filings` + a `quiver_sync_runs` row
- [ ] Internal read API returns filings
- [ ] Key is not mounted on WUT, Wv2, or MCP

## Non-goals

- Weekly House 130/30 WUT runner (still deferred on the 2026-08-18 report)
- Baking Alt Filings into Winston EOD Standard parquet (ADR-011)
- Committing `quiver.env` or the API key
