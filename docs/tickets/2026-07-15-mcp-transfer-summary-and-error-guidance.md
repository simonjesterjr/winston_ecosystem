# Ticket: MCP transfer summary + cleaner error guidance

**Status:** Done (error-guidance 2026-07-17; summary/reply_text prior)  
**Date:** 2026-07-15  
**Priority:** Medium (C — supports weak/local models)  
**Source:** Session 2026-07-15; transfer ok but model ignored structured result  
**Repos / path:** `ai/mcp_winston` (host; see also `2026-07-13-mcp-winston-source-git-home.md`)

## Problem

1. Successful `wv2_transfer_portfolio_from_wut` returns rich JSON (`action`, portfolio block, warnings) but models still narrate **list_portfolios** only. A one-line **`summary`** field is harder to skip.  
2. Generic 422 **`retry_guidance`** (“fetch_only after 4:30 PM MT”) appears on unrelated errors (e.g. `wut_add_market` portfolio not found). Models paste it into wrong contexts.  
3. Partial work this session: null-tolerant schema for `run_id`/`ts_id`/`parent_correlation_id`; `_optional_int` coercion; prefer run_id over ts_id. Must land in git-tracked MCP home and image rebuild path.

## Scope (C)

1. Transfer response: add top-level `summary` string, e.g.  
   `"legacy_updated #157 Portfolio Mango (WUT run 57) active=false"`.  
2. Error builder: tool-specific `retry_guidance`; remove report/EOD boilerplate from non-report tools.  
3. Ensure null-tolerant transfer schema + coercion are in the canonical MCP source and rebuild instructions.  
4. Optional: document in `interfaces/winston-mcp-tools.md`.  

## Acceptance

- [x] Transfer success JSON includes stable `summary` (also activate/deactivate; `reply_hint` added)  
- [x] `wut_add_market` / similar 422s do not mention fetch_only / 4:30 PM  
- [x] Schema accepts omitted or null optional ids without nanobot pre-validation failure (partial prior session — verify in image)  
- [ ] MCP source tracked or ticket for git-home closed *(still open: `2026-07-13-mcp-winston-source-git-home.md` — host path rebuild works; not monorepo git)*  

**Impl note:** `_attach_agent_summary` in `ai/mcp_winston/mcp_winston/server.py`; `errors.py` tool-specific `retry_guidance` (2026-07-17); image rebuilt.  

## Related

- Ticket A (reply contract)  
- Ticket: `2026-07-13-mcp-winston-source-git-home.md`  
- Interface: `ecosystem/interfaces/winston-mcp-tools.md`  

## Non-goals

- Changing importer semantics  
