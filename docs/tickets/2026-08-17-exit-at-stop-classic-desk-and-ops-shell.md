# Ticket: Exit-at-stop on classic desk and ops shell

**Status:** Proposed  
**Priority:** P2  
**Date:** 2026-08-17  
**Monolith:** winston_v2  
**Domain:** Desk, ops shell, Stop-Out Reconciliation  
**See:** [`2026-08-17-1315-leftover-dirty-trees.md`](../session-reports/2026-08-17-1315-leftover-dirty-trees.md) §6/§14; [`winston_v2/docs/session-reports/2026-08-03-1013-desk-workflow-exit-at-stop.md`](../../../winston_v2/docs/session-reports/2026-08-03-1013-desk-workflow-exit-at-stop.md)

## Problem

Desk Workflow now has a one-click **Exit at stop** path (`Operations::ExitAtStopService`, landed `00306e2`). Classic desk and the ops shell do not. Operator still has to invent a price or walk the workflow page to book the working stop.

## Scope

1. Classic desk: same shortcut when an open lot has a working stop (confirm draft if present; else ad-hoc stop-out).
2. Ops shell: command of the form `exit_at_stop <port> <sym>` (or journal/task id) that calls the same service.
3. Same flatten rule as workflow: multi-lot only under `move_to_last_entry` / `move_to_stepped_entry`.
4. Telegram / Cromwell is **out of scope** unless the shell path is reused.

## Acceptance

- [ ] Classic desk shows Exit at stop when `exit_at_stop_context` would be available
- [ ] Ops shell books at working stop via `ExitAtStopService` (request or service spec)
- [ ] Flatten / isomorphic behavior matches workflow
- [ ] No live capital book without operator click

## Related

- `winston_v2/app/services/operations/exit_at_stop_service.rb`
- `winston_v2/app/controllers/operations/desk_workflows_controller.rb` (`exit_at_stop_context`, `dispatch!`)
- ADR-009 Stop-Out Reconciliation
