# Ticket: Establish git home for `ai/mcp_winston`

**Status:** Proposed  
**Context:** Session `docs/session-reports/2026-07-13-1307-intraday-market-radar.md`. MCP tool description for `wv2_market_snapshot` was updated under workspace `ai/mcp_winston/`, which is **outside** every monolith git repo (`ecosystem`, `winston_v2`, etc.).

## Problem

Skills and interface docs version in `ecosystem/`; MCP Python is only in workspace + container image (`COPY` at build). Source edits can be lost or unreproducible across machines unless the image is rebuilt from a committed tree.

## Acceptance criteria

- [ ] Decide home: new repo, fold into `ecosystem/`, or document intentional image-only workflow
- [ ] If repo: initial import of `ai/mcp_winston` with history note; CI or compose build still works
- [ ] If image-only: write short note in `ecosystem/deployment/README.md` + `ai/mcp_winston` README
- [ ] Next MCP change has a clear `git commit` path

## Related

- Session: [`docs/session-reports/2026-07-13-1307-intraday-market-radar.md`](../session-reports/2026-07-13-1307-intraday-market-radar.md)
- Reinforced: [`docs/session-reports/2026-07-18-1024-ops-demo-5-7-related-draft-equity.md`](../session-reports/2026-07-18-1024-ops-demo-5-7-related-draft-equity.md) (edit/compare/related tools still host-only)
- Path: `ai/mcp_winston/mcp_winston/server.py`
- Interface: `ecosystem/interfaces/winston-mcp-tools.md`
- Interim ops recreate: `docs/tickets/2026-07-18-ops-mcp-recreate-after-demo-tools.md`
