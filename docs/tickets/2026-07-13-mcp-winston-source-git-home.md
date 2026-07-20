# Ticket: Establish git home for `ai/mcp_winston`

**Status:** Done  
**Context:** Session `docs/session-reports/2026-07-13-1307-intraday-market-radar.md`. MCP tool description for `wv2_market_snapshot` was updated under workspace `ai/mcp_winston/`, which is **outside** every monolith git repo (`ecosystem`, `winston_v2`, etc.).

## Problem

Skills and interface docs version in `ecosystem/`; MCP Python is only in workspace + container image (`COPY` at build). Source edits can be lost or unreproducible across machines unless the image is rebuilt from a committed tree.

## Acceptance criteria

- [x] Decide home: new repo, fold into `ecosystem/`, or document intentional image-only workflow → **fold into `ecosystem/ai/`**
- [x] If repo: initial import of `ai/mcp_winston` with history note; CI or compose build still works
- [x] If image-only: write short note in `ecosystem/deployment/README.md` + `ai/mcp_winston` README — N/A (not image-only)
- [x] Next MCP change has a clear `git commit` path → edit `ecosystem/ai/mcp_winston/`, commit `winston_ecosystem`, rebuild image

## Implementation (2026-07-20)

| Decision | Fold into **ecosystem** (`winston_ecosystem`) — MCP is ecosystem glue exercised by Cromwell |
|----------|---------------------------------------------------------------------------------------------|
| MCP SOT | `ecosystem/ai/mcp_winston/` |
| Nanobot SOT | `ecosystem/ai/nanobot/` (Containerfile + cron allowlist patch; same orphan class) |
| Compose | Root `compose.yml` build contexts → `./ecosystem/ai/mcp_winston` and `./ecosystem/ai/nanobot` |
| Legacy paths | Workspace `ai/mcp_winston/` and `ai/nanobot/` are pointer READMEs only |

**Commit path for MCP changes:**

```bash
cd ecosystem
# edit ai/mcp_winston/...
git add ai/mcp_winston && git commit && git push
cd ..
./bin/compose --profile ai build winston_mcp
# recreate winston_mcp only when possible
```

## Related

- Session: [`docs/session-reports/2026-07-13-1307-intraday-market-radar.md`](../session-reports/2026-07-13-1307-intraday-market-radar.md)
- Reinforced: [`docs/session-reports/2026-07-18-1024-ops-demo-5-7-related-draft-equity.md`](../session-reports/2026-07-18-1024-ops-demo-5-7-related-draft-equity.md) (edit/compare/related tools still host-only)
- Reinforced: [`docs/session-reports/2026-07-20-1031-historical-dar-telegram-guards.md`](../session-reports/2026-07-20-1031-historical-dar-telegram-guards.md) — `allow_historical` / evaluate pass-through + error guidance edited in host `ai/mcp_winston` only; image rebuilt live, still no commit path
- Path: `ai/mcp_winston/mcp_winston/server.py`
- Interface: `ecosystem/interfaces/winston-mcp-tools.md`
- Interim ops recreate: `docs/tickets/2026-07-18-ops-mcp-recreate-after-demo-tools.md`
