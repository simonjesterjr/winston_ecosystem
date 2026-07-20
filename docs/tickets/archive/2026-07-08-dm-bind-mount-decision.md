# Ticket: Decide on bind-mount for data_manager in development (or document rebuild requirement)

**Status:** Done  
**Priority:** P3  
_Archived 2026-07-20: completed work; no further action._


**Related to:** ecosystem/docs/session-reports/2026-07-08-1430-dm-reconcile-container-cleanup.md

## Context
`data_manager/` source was deliberately not bind-mounted in root `compose.yml` (commented line) because of rootless Podman permission issues on `bin/*`. Every code change (ReconciliationService, rakes, etc.) required `bin/compose build data_manager` + recreate. This created repeated "container dependency hell" during heavy DM sessions.

## Decision

**Option A — Enable full source bind-mount for DM in development (same as WUT/Wv2).**

| | |
|--|--|
| **Choice** | Uncomment / enable `./data_manager:/app` on `data_manager` and `data_manager_sidekiq`; keep `sawtooth_dm_data:/app/data` for parquet |
| **Root cause of old failure** | Host/git `data_manager/bin/*` were mode `0644` / git `100644` (not executable). Image build runs `chmod +x bin/*`, but bind-mount masks those files with non-executable host copies → rootless Podman "permission denied" on `bin/rails` |
| **Fix applied** | `chmod +x data_manager/bin/*` + `git update-index --chmod=+x` so git mode is `100755` (matches WUT/Wv2) |
| **Why not B** | Rebuild tax was the friction that produced container hell; WUT already proves full bind-mount works on this host |
| **Why not C (partial mount)** | Unnecessary once `bin/*` +x is fixed; partial mounts add compose complexity without benefit |
| **Production-like default** | Unchanged for data (named volume) and image layers (Gemfile/Containerfile still need rebuild). Source bind-mount matches the other Rails monoliths already in this compose file |

## Rationale
Developer friction of mandatory rebuild on every DM edit was worse than a one-time permission fix. The "Podman rootless" story was incomplete: the real bug was non-executable host `bin/*` under bind mount, not an unsolved Podman limitation.

## Acceptance Criteria
- [x] Decide among A / B / C → **A**
- [x] Update `compose.yml` comment and `data_manager/README.md` / `AGENTS.md` with policy + exact commands
- [x] Bind mount enabled; verified `bin/rails` works
- [x] Note in ticket (+ plan closeout / deployment README / hints)

## Implementation

| Path | Change |
|------|--------|
| `compose.yml` | Enable `./data_manager:/app` on DM web + Sidekiq; document policy + rebuild fallback |
| `data_manager/bin/{rails,rake,setup}` | Executable + git `100755` |
| `bin/rebuild-dm` | Helper for Gemfile/Containerfile-only rebuilds |
| `data_manager/README.md`, `AGENTS.md` | Policy + commands |
| `ecosystem/deployment/README.md`, `ecosystem/hints/README.md` | Cross-links / gotcha |

### Commands (documented)

```bash
# Day-to-day Ruby edits — live via bind mount
./bin/compose restart data_manager data_manager_sidekiq   # Sidekiq-loaded code
./bin/compose exec -T data_manager bin/rails data:reconcile

# Gemfile / Containerfile / native deps only
./bin/rebuild-dm
# or:
./bin/compose build data_manager && ./bin/compose up -d data_manager data_manager_sidekiq

# If permission denied on bin/rails after bind mount
chmod +x data_manager/bin/*
git -C data_manager update-index --chmod=+x bin/rails bin/rake bin/setup
```

### Verification (2026-07-08)

```
podman inspect data_manager → bind .../data_manager -> /app ; volume ... -> /app/data
podman exec data_manager ls -la bin/rails → -rwxrwxr-x
podman exec data_manager bin/rails -v → Rails 7.0.10
podman exec data_manager bin/rails runner 'puts "ok #{Rails.env}"' → ok development
```

## Links
- Session report: `ecosystem/docs/session-reports/2026-07-08-1430-dm-reconcile-container-cleanup.md`
- Root `compose.yml` `data_manager` / `data_manager_sidekiq` volumes
- Plan note: `ecosystem/plans/wut-dm-parquet-source-of-truth.md` (closeout deferred list)

**Owner:** team  
**Due:** before next round of heavy DM development  
**Completed:** 2026-07-08
