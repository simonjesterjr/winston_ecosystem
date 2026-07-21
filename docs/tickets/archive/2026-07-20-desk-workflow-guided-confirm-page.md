# Ticket: Full Desk Workflow guided confirm page

**Status:** Done  
**Priority:** P1  
**Date:** 2026-07-20  
**Completed:** 2026-07-21  
**Series:** `adr-009-desk-fulfillment` **#2**  
**Domain:** ADR-009  

## Problem

Every Desk Handoff should deep-link to a guided Wv2 page. Only partial desk form existed.

## Delivered (2026-07-21)

1. Routes: `GET/POST /operations/workflow` → `Operations::DeskWorkflowsController`.  
2. Guided page: signal spine (dates/prefill), packaging, confirm/edit/exit intents; stop-out preview.  
3. `DeskActionHandoff.form_path` → `/operations/workflow` when journal/task present; classic `/operations/desk` for free-form.  
4. Closed OP / non-draft journal refuse mutate with clear messaging.  
5. Multi-leg package_order warn stub (series #5 full packages later).  
6. Request + handoff specs green; responsive CSS (max-width stack).

## Acceptance

- [x] Operator can complete confirm + packaging from linked workflow page  
- [x] DAR handoffs use workflow URLs (via form_path)  
- [x] Closed OP / executed journal refuse mutate with clear error  
- [x] Responsive page shell  
