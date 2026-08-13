# Ticket: Rebuild winston_mcp after snapshot timeout + tool description

**Status:** Proposed
**Priority:** P2
**Date:** 2026-08-13
**Monoliths:** ecosystem (`winston_mcp` image), Cromwell
**See:** [`docs/session-reports/2026-08-13-1248-hourly-snapshot-shuffle-movers.md`](../session-reports/2026-08-13-1248-hourly-snapshot-shuffle-movers.md)

## Problem

`wv2_market_snapshot` is now a long-running shuffled scan (Sidekiq live evaluations until 3 non-quiet names). Source is updated:

- `ecosystem/ai/mcp/mcp_winston/server.py` — tool description + HTTP GET timeout 90s
- `ecosystem/ai/mcp/mcp_winston/tools_schema.py` — `LONG_RUNNING_TOOLS` / 90s estimate

`winston_mcp` is **image-only** (compose bind-mount is commented out). Cromwell still has the old 30s client timeout and the old “all Active books” description until the image is rebuilt.

Live compose smoke on 2026-08-13 finished well under 30s (16 of 70 names). A slow Yahoo day could still 30s-timeout the hourly.

## Scope

1. From sawtooth root: `./bin/compose --profile ai build winston_mcp`
2. Recreate `winston_mcp` (not just restart) so the new image is what nanobot calls.
3. Confirm tool description via MCP list/schema includes shuffle + 3-mover language.

## Acceptance

- [ ] Running `winston_mcp` image includes the 90s `wv2_market_snapshot` GET
- [ ] Tool description mentions shuffle + stop at 3 non-quiet
- [ ] One successful `wv2_market_snapshot` `{}` after recreate

## Non-goals

- Changing scan algorithm (already shipped in Wv2)
- Forcing a Telegram post
