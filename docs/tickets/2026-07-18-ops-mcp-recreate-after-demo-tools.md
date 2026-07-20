# Ticket: Recreate winston_mcp after ops demo tool surface changes

**Status:** Proposed  
**Date:** 2026-07-18  
**Source:** Session `docs/session-reports/2026-07-18-1024-ops-demo-5-7-related-draft-equity.md`  
**Priority:** P1

## Problem

Ops daily demo epic #3–#7 added MCP tools and args under host `ai/mcp_winston/` (exit reasons, bulk exit/stops, related-instrument book, draft edit, equity compare). The running `winston_mcp` image / container may still expose the pre-change tool list until recreated. Nanobot tool cache may also lag.

## Scope

1. Recreate `winston_mcp` (and `nanobot_cromwell` if required for tool list refresh) using the established podman pattern from prior sessions.  
2. Verify tool list includes at least: `wv2_exit_all_trades`, `wv2_update_stops`, `wv2_edit_journal`, `wv2_compare_equity`, and related-instrument args on `wv2_book_trade` / `wv2_exit_trade`.  
3. Optional: one Telegram 1-1 probe that tools appear (full product smoke is separate ticket).  

## Acceptance

- [ ] Running MCP exposes new tools  
- [ ] Telegram/Cromwell can call at least one new tool without “unknown tool”  

## Related

- Session: `docs/session-reports/2026-07-18-1024-ops-demo-5-7-related-draft-equity.md`  
- MCP git-home: `docs/tickets/2026-07-13-mcp-winston-source-git-home.md`  
- Live smoke: `docs/tickets/2026-07-18-ops-telegram-demo-tools-smoke.md`  
