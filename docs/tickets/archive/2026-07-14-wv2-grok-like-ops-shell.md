# Ticket: Grok-like Wv2 ops shell (chat + verification panels)

**Status:** Done (2026-07-14 Phase 2A)  
**Date:** 2026-07-14  
**Source:** Paper Telegram roadmap Phase 2; session `2026-07-14-1112-paper-telegram-phase0-1.md`

## Context

Phase 1 proved paper confirm via services/MCP. Operator wants a **desk** surface that is not WUT-style REST CRUD:

- **Chat shell** = control plane (same tool contract as Telegram Cromwell)  
- **Verification panels** = truth plane (Active OPs, positions, pending, last DAR)  
- **Separate browser session** (not embed nanobot v1)

## Scope

1. Replace plain-text `Operations::HomeController` with bare-bones layout (chat + panels).  
2. Panels: read-only, ADR-005 snappy (metadata only).  
3. Chat: server-side turns calling same internal APIs / services as MCP.  
4. Mutations only through journal/CashEvent tool path.  
5. Auth: local/dev trust for v1.  

## Non-goals

- WUT-parity portfolio admin  
- Capital Activation UI  
- LEAP engine  

## Acceptance

- [x] `http://localhost:3002` paints shell &lt;1s (~12–130ms observed)  
- [x] Panels match `wv2:portfolios:list` / portfolio status for Active focus (#12 capital + AMZN)  
- [x] Chat can list pending + confirm (idempotent confirm journal #16)  
- [x] No write path bypassing confirm/CashEvent services (`OpsShellChat` → services only)  

## Delivery notes (2026-07-14)

- Shell: `Operations::HomeController` + `ops_shell.css` + chat/panels JSON endpoints  
- Services: `Operations::OpsShellPanels`, `Operations::OpsShellChat`  
- Commands: `help`, `list`, `status`, `pending`, `journal`, `confirm`, `done`

## Related

- ADR-005 responsive pages  
- MCP contract `interfaces/winston-mcp-tools.md`  
- Phase 1 live OP: `#12 Portfolio Blue · PBR62`  
