# Ticket: Optional MCP tool for portfolio PCS deep dive

**Status:** Proposed  
**Priority:** unset

**Date:** 2026-07-13  

**Session:** [`docs/session-reports/2026-07-13-1034-wut-portfolio-correlation-dashboard.md`](../session-reports/2026-07-13-1034-wut-portfolio-correlation-dashboard.md)  
**Related UI:** WUT PF Correlation dashboard (`/portfolios/correlation`, curated YAML deep dives)

## Problem

Operators and Cromwell can open curated “AI deep dive” narratives on the heatmap page (offline YAML under `winston_unit_test/config/correlation_deep_dives/`). There is no MCP tool that answers “analyze Portfolio Orange PCS vs peers” on demand with live snapshots + curated context.

## Scope

1. Decide product stance: keep curated YAML only vs add read-only MCP tool.  
2. If MCP: tool that loads latest WUT PCS snapshot + optional curated deep-dive YAML + peer ranking summary.  
3. Document in `ecosystem/interfaces/winston-mcp-tools.md` if shipped.  
4. Do **not** recompute a parallel formula in Wv2 (ADR-007 — WUT SoT).

## Out of scope

- Live free-form LLM rewrite of membership  
- Auto-rebalance from deep-dive output  

## Acceptance

- [ ] Product decision recorded (YAML-only or MCP tool)  
- [ ] If MCP: tool returns PCS + max|r| + peers + deep-dive sections for a named color portfolio  
- [ ] Interface doc updated when tool ships  

## Related

- ADR-007 PCS SoT  
- Curated content: `winston_unit_test/config/correlation_deep_dives/`  
- Ticket: dashboard done `2026-07-12-wut-portfolio-correlation-dashboard.md`  
