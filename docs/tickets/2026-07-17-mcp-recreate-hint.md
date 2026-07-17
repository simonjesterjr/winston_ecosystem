# Ticket: Document winston_mcp Podman recreate pattern as ecosystem hint

**Status:** Proposed  
**Date:** 2026-07-17  
**Source:** Session `2026-07-17-1257-mcp-smoke-shell-cash-parity.md`  
**Priority:** Low (ops hygiene; second-time ritual → skill/hint)

## Problem

`bin/compose --profile ai up -d --force-recreate winston_mcp` cascades dependent name conflicts (redis/postgres/mcp already exist). Working pattern was re-discovered mid-session; belongs in `ecosystem/hints/` so agents stop thrashing.

## Scope

1. Add `ecosystem/hints/winston-mcp-recreate.md` (or section in `hints/README.md`) with:

```bash
podman rm -f nanobot_cromwell
podman rm -f winston_mcp
bin/compose --profile ai build winston_mcp   # if source changed
bin/compose --profile ai up -d --no-deps winston_mcp
bin/compose --profile ai up -d --no-deps nanobot_cromwell
```

2. Note: host MCP source (`ai/mcp_winston`) still outside monolith git — see `2026-07-13-mcp-winston-source-git-home.md`.  
3. Optional: one-line pointer from `ai/README.md` or compose comment.

## Acceptance

- [ ] Hint file exists and is linked from `ecosystem/hints/README.md`  
- [ ] Next MCP rebuild session can follow without inventing the dance  

## Related

- MCP git-home: `docs/tickets/2026-07-13-mcp-winston-source-git-home.md`  
- Session: `docs/session-reports/2026-07-17-1257-mcp-smoke-shell-cash-parity.md`  
