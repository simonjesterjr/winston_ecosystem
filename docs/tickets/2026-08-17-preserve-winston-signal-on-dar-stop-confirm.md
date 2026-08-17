# Ticket: Preserve winston_signal when confirming a DAR exit at stop

**Status:** Proposed  
**Priority:** P2  
**Date:** 2026-08-17  
**Monolith:** winston_v2  
**Domain:** Desk Workflow, Daily Analysis Report (DAR), Stop-Out Reconciliation  
**See:** [`2026-08-17-1315-leftover-dirty-trees.md`](../session-reports/2026-08-17-1315-leftover-dirty-trees.md) §6; Aug 3 desk-workflow report deferred item

## Problem

`Operations::StopOutReconciliation.snapshot` always writes `winston_signal: false`. That is correct for an unsignaled ad-hoc stop-out. When **Exit at stop** confirms an existing DAR methodology exit draft, the merge can overwrite `winston_signal: true` and make a signaled exit look ad-hoc on the audit spine.

Does not block desk booking. Blocks pure provenance.

## Scope

1. Snapshot should take an optional `winston_signal:` (or preserve the journal’s existing flag).
2. `ExitAtStopService` / `JournalConfirmationService` keep `true` when confirming a DAR/methodology draft; stay `false` on ad-hoc.
3. Specs for both paths. Do **not** invent a Winston exit signal for unsignaled stop-outs (ADR-009).

## Acceptance

- [ ] Confirming a DAR exit draft at working stop leaves `winston_signal: true` (or an explicit stop-fill flag beside it)
- [ ] Ad-hoc Exit-at-stop / `AdHocExitService` still stamps `winston_signal: false`
- [ ] `stop_out_reconciliation_spec` and `exit_at_stop_service_spec` lock both

## Related

- `winston_v2/app/services/operations/stop_out_reconciliation.rb` (`"winston_signal" => false`)
- `winston_v2/app/services/operations/exit_at_stop_service.rb`
- `winston_v2/app/services/operations/ad_hoc_exit_service.rb`
- ADR-009
