# Ticket: Recreate compose `data_manager` on latest image

**Status:** Done (2026-07-07/08)

**Date:** 2026-07-07

**Context:** Session [`2026-07-06-2020-portfolio-overlap-pipeline`](../session-reports/2026-07-06-2020-portfolio-overlap-pipeline.md). Symbol registry code is committed and the image builds (`localhost/sawtooth_data_manager:latest`), but the long-running `data_manager` compose container still runs a pre-registry image — `SymbolRegistryEntry` is unavailable via `./bin/compose exec data_manager`.

DM random batch succeeded only via one-off `podman run` on the latest image.

## Problem

Operators cannot run `dm:symbol_registry:*` rakes through the normal compose path. Future registry work risks volume/network mistakes if one-off containers become the default.

## Scope

1. Stop dependents if needed (`winston_mcp`, `nanobot_cromwell` blocked recreate in prior session).
2. `podman rm -f data_manager data_manager_sidekiq` (and dependents as required).
3. `./bin/compose build data_manager data_manager_sidekiq && ./bin/compose up -d data_manager data_manager_sidekiq`
4. `./bin/compose exec -T data_manager bin/rails db:migrate`
5. Verify: `bin/rails runner 'puts SymbolRegistryEntry.count'` returns a number.
6. Document the canonical compose path in `ecosystem/plans/portfolio-overlap-rebuild.md` commands section.

## Acceptance

- `./bin/compose exec -T data_manager bin/rails dm:symbol_registry:summary` works without `uninitialized constant`.
- Parquet volume remains `sawtooth_sawtooth_dm_data` (no accidental volume swap).

## Related

- Plan: `ecosystem/plans/portfolio-overlap-rebuild.md` task #1
- DM commit: `25c5409` (symbol registry)