# Ticket: Telegram equity compare charts (“Blue vs Mango”)

**Status:** Proposed  
**Date:** 2026-07-17  
**Epic:** `2026-07-17-ops-daily-demo-epic.md`  
**Priority:** Medium (demo polish; not blocking desk loop)

## Problem

Equity series and PDF chart primitives exist, but there is no ad-hoc “show equity of Blue vs Mango” image delivery over Telegram.

## Scope

1. Service: multi-OP equity series → PNG/chart image (reuse PDF chart drawer or new renderer).  
2. MCP or report path that returns media path for Cromwell.  
3. Speech contract for Cromwell skill.  
4. Non-goal: interactive live charts in Telegram.

## Acceptance

- [ ] Operator can request compare chart; Telegram receives image  
- [ ] Labels match OP display names / short fingerprints  

## Related

- `PortfolioEquitySeries`, `ReportPdfChartDrawer`  
