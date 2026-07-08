---
Status: Proposed
---

# Ticket: Decide on bind-mount for data_manager in development (or document rebuild requirement)

**Related to:** ecosystem/docs/session-reports/2026-07-08-1430-dm-reconcile-container-cleanup.md

## Context
`data_manager/` source is deliberately not bind-mounted in `compose.yml` (commented line) because of rootless Podman permission issues on `bin/*`. Every code change (ReconciliationService, rakes, etc.) requires `bin/compose build data_manager` + recreate. This created repeated "container dependency hell" during this session.

## Acceptance Criteria
- [ ] Decide: 
  - Option A: Uncomment bind mount for dev (and solve/ document the bin/ permission workaround)
  - Option B: Keep current model + add clear docs + helper script for DM-only rebuild
  - Option C: Other (e.g. dev profile, volume mount only for app/, etc.)
- [ ] Update `compose.yml` comment and `data_manager/README.md` / `AGENTS.md` with the chosen policy and exact commands.
- [ ] If bind mount is enabled, verify `bin/rails` still works and hot-reload is usable.
- [ ] Add a note in the DM SoT plan or a new operational ticket.

## Links
- Session report: `ecosystem/docs/session-reports/2026-07-08-1430-dm-reconcile-container-cleanup.md`
- compose.yml comment around data_manager volumes
- ReconciliationService and rake changes that triggered repeated rebuilds

**Owner:** team  
**Due:** before next round of heavy DM development