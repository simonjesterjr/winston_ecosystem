---
Status: Completed
---

# Ticket: Complete zero-delta specs for DM reconcile path

**Related to:** ecosystem/docs/session-reports/2026-07-08-1430-dm-reconcile-container-cleanup.md

**Status:** Completed (2026-07-08)

## Context
The main WUT DM-parquet ticket and plan closeout note that zero-delta specs were partially advanced (importer_spec has a DM branch asserting no activity growth). Full coverage for the new `ReconciliationService`, `data:reconcile` rake, and related paths is still needed.

## Acceptance Criteria
- [x] Add/expand specs that assert:
  - After `reconcile_all` / `reconcile_symbol` on DM symbols: **metadata-only path** — 0 new `download_runs` / `download_tasks` (DM has no `activities` / `market_indicator_values` tables; those invariants live in WUT zero-delta specs)
  - `DataCoverage` is updated from actual parquet (min/max date, bar_count, indicators_present)
  - `SymbolRegistryEntry.dm_data_status` set to "acquired" (with `list_source` default `"manual"`; existing sources preserved)
  - No parquet rewrite / no extra files under fixture tree for DM symbols
  - Error paths (bad parquet, missing columns, missing file, per-symbol exception in `reconcile_all`) are handled without crashing the run
- [x] Cover the rake tasks (`data:reconcile`, `data:reconcile_symbol`) — smoke + service E2E via same API
- [x] Specs run cleanly against **temp parquet fixtures** (not the live 600+ corpus) via `Dir.mktmpdir` + stubbed `Dir.glob` for `reconcile_all`
- [x] Update this ticket with progress / evidence

## Delivery (2026-07-08)

### Spec files added
| Path | Role |
|------|------|
| `data_manager/.rspec` | RSpec defaults |
| `data_manager/spec/spec_helper.rb` | Core RSpec config |
| `data_manager/spec/rails_helper.rb` | Rails/test DB + transactional fixtures |
| `data_manager/spec/support/parquet_fixture_helper.rb` | Mini Winston EOD parquet writer (JSON→DuckDB COPY) |
| `data_manager/spec/services/reconciliation_service_spec.rb` | Service zero-delta + error paths |
| `data_manager/spec/tasks/data_rake_spec.rb` | Rake smoke + service path used by rake |

### Evidence
```text
cd /app && RAILS_ENV=test bundle exec rspec \
  spec/services/reconciliation_service_spec.rb \
  spec/tasks/data_rake_spec.rb

# Finished in ~0.5s
# 15 examples, 0 failures
```

Commands used (DM source is not bind-mounted; copy then run, or rebuild):
```bash
# Ensure test DB exists once
bin/compose exec data_manager bash -c 'RAILS_ENV=test bundle exec rails db:prepare'

# If image lacks host specs (no bind-mount):
podman cp data_manager/spec data_manager:/app/spec
podman cp data_manager/.rspec data_manager:/app/.rspec

bin/compose exec data_manager bash -c \
  'cd /app && RAILS_ENV=test bundle exec rspec \
    spec/services/reconciliation_service_spec.rb \
    spec/tasks/data_rake_spec.rb'
```

### Notes / mapping of ticket language to DM
- **activities / market_indicator_values:** not present in DM schema; WUT importer zero-delta covers consumer no-duplication (`2026-07-08-wut-dm-parquet-zero-delta-specs.md`). DM specs assert metadata-only (no download run/task growth, no parquet rewrite).
- **list_source default:** `entry.list_source ||= "manual"` — covered for new rows; preserve existing (`catalog`) covered separately.
- **Corpus independence:** fixtures under tmpdir; `reconcile_all` stubs `Dir.glob` for the `data/markets/*/bars.parquet` pattern so CI does not depend on the shared volume corpus.

## Links
- Main ticket: `2026-07-07-wut-dm-parquet-source-of-truth-no-duplication.md`
- Session report: `ecosystem/docs/session-reports/2026-07-08-1430-dm-reconcile-container-cleanup.md`
- ReconciliationService: `data_manager/app/services/reconciliation_service.rb`
- Existing importer zero-delta work: see 2026-07-08-wut-dm-parquet-zero-delta-specs.md

**Owner:** follow existing ticket  
**Due:** before declaring the DM SoT effort fully tested in CI

## Residual gaps
- Specs are not yet baked into the DM image until next `bin/compose build data_manager` (or bind-mount enabled); host tree has the files.
- No CI job yet that runs `data_manager` RSpec by default (first RSpec suite in this monolith).
- Full live-corpus reconcile is still an ops/smoke concern (separate e2e smoke ticket), not unit-spec scope.
