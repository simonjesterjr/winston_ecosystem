# Ticket: BG evidence volume — avoid double project prefix

**Status:** Proposed  
**Priority:** P3  
**Date:** 2026-08-12  
**Series:** `trade-fulfillment-engine`  
**Domain:** Broker Gateway, compose  
**Monoliths:** workspace root `compose.yml`; **broker_gateway**  
**Origin:** Session report [`docs/session-reports/2026-08-12-1152-bg-registry-dummy-sim-compose.md`](../session-reports/2026-08-12-1152-bg-registry-dummy-sim-compose.md)

## Problem

Root `compose.yml` names the evidence volume `sawtooth_bg_evidence`. With project name `sawtooth`, podman-compose creates **`sawtooth_sawtooth_bg_evidence`**. Cosmetic / ops confusion only; store path inside the container is fine.

## Scope

1. Rename volume key to something like `bg_evidence` (match `bg_postgres_data` pattern).  
2. Document one-time migrate if an existing volume has data: recreate or `podman volume` rename guidance.  
3. No change to Winston Broker Evidence Standard paths inside the app.

## Non-goals

- Changing JSONL layout under `data/evidence/{binding_id}/`  
- Shared volume with Wv2  

## Acceptance

- [ ] Volume name in `podman volume ls` is single-prefix (e.g. `sawtooth_bg_evidence`)  
- [ ] `broker_gateway` + sidekiq still mount evidence and smoke refresh works  
- [ ] Short note in BG `AGENTS.md` or ecosystem deploy hint if migration needed  

## Related

- Epic: [`2026-08-09-l1-confirmation-intake-bg-build.md`](2026-08-09-l1-confirmation-intake-bg-build.md)  
- Session: [`../session-reports/2026-08-12-1152-bg-registry-dummy-sim-compose.md`](../session-reports/2026-08-12-1152-bg-registry-dummy-sim-compose.md)  
