# Ticket: MCP list-journals for a portfolio

**Status:** Proposed  
**Priority:** P3  
**Date:** 2026-08-18  
**Monolith:** winston_v2 + `winston_mcp`  
**Related:** Wv2 issue `winston_v2/docs/issues/2026-08-18-ops-shell-journals-command-missing.md`; interface [`interfaces/winston-mcp-tools.md`](../../interfaces/winston-mcp-tools.md); session `winston_v2/docs/session-reports/2026-08-18-1740-ops-shell-journals-and-chat-scroll.md`

---

## Problem

Winston v2 (Wv2) ops shell now has `journals <id|name|fp>` (list) plus `journal <id>` (one row). Model Context Protocol (MCP) only exposes `wv2_get_journal` (single id) and `wv2_get_portfolio_status` (`recent_journals`, default 10). Cromwell / Telegram cannot ask for a full Operational Portfolio (OP) ledger the way the desk can.

## Scope

Optional follow-up — not blocking paper desk.

- Internal list endpoint or reuse journals controller JSON (status filter + limit).
- MCP tool e.g. `wv2_list_journals` with `portfolio_id_or_name`, optional `status`, `limit`.
- Update `ecosystem/interfaces/winston-mcp-tools.md` and recreate `winston_mcp` after schema change.

## Acceptance

- [ ] Tool lists journals for OP #11 including drafts 937/938
- [ ] Existing `wv2_get_journal` unchanged
- [ ] Interface doc + MCP recreate noted

## Non-goals

- Mutating journals
- Replacing the HTML journals page
- Auto-confirm
