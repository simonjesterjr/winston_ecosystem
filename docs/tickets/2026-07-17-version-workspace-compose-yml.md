# Ticket: Version workspace root `compose.yml` in git

**Status:** Proposed  
**Date:** 2026-07-17  
**Source:** Session `docs/session-reports/2026-07-16-2210-public-url-cash-dar-error-guidance.md`  
**Priority:** Medium (ops durability)

## Problem

Sawtooth workspace root `/home/johnkoisch/Documents/com/sawtooth/compose.yml` orchestrates DM + WUT + Wv2 + optional AI profile, but sits **outside** every monolith git repo (`ecosystem`, `winston_v2`, etc.). Session changes such as `WV2_PUBLIC_BASE_URL` are only on disk/host — easy to lose on machine rebuild and invisible to PR review.

Related gap: host `ai/mcp_winston` (see git-home ticket).

## Scope

1. Decide home for orchestration:
   - Fold into `ecosystem/` (e.g. `ecosystem/compose.yml` + root wrapper), **or**
   - New thin `sawtooth-workspace` / ops repo, **or**
   - Document intentional host-only + backup path.
2. If git-tracked: import current `compose.yml` + `bin/compose` conventions without secrets (`*.env` stay gitignored).
3. Document recreate gotchas (podman name conflicts) in deployment notes.
4. Cross-link MCP git-home decision so compose build `context: ./ai/mcp_winston` has a committed tree.

## Acceptance

- [ ] Written decision on compose ownership  
- [ ] If tracked: `compose.yml` changes reviewable via git commit  
- [ ] Env secrets remain out of git (`ecosystem/deployment/*.env`)  
- [ ] Next env change (e.g. public URL) has a clear commit path  

## Related

- MCP git-home: `docs/tickets/2026-07-13-mcp-winston-source-git-home.md`  
- Public URL note: `deployment/wv2-public-url.md`  
- Session: [`docs/session-reports/2026-07-16-2210-public-url-cash-dar-error-guidance.md`](../session-reports/2026-07-16-2210-public-url-cash-dar-error-guidance.md)
