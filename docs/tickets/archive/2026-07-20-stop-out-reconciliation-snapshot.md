# Ticket: Stop-Out Reconciliation (position link + working-stop snapshot)

**Status:** Done  
**Priority:** P1  
**Date:** 2026-07-20  
**Completed:** 2026-07-21  
**Series:** `adr-009-desk-fulfillment` **#4**  
**Domain:** ADR-009  

## Problem

Real-world stop-outs must book onto the **Booked Capital Spine** tied to the Winston lot’s **Working Stop**. `reason=external_stop` existed; required position link, working-stop snapshot, and fill-vs-stop warn were incomplete.

## Delivered (2026-07-21)

1. `Operations::StopOutReconciliation` — working stop snapshot, gap, warn threshold.  
2. `AdHocExitService` — require unique open lot or `position_id` (ambiguous multi-lot → refuse); stamp details + warnings.  
3. `JournalConfirmationService` exit path — same snapshot on confirm.  
4. Ops shell exit reply surfaces working_stop / gap / WARN.  
5. DAR recent journals + journal presenter expose provenance fields.  
6. Specs green.

## Acceptance

- [x] Exit without resolvable open lot refused  
- [x] Executed exit journal carries working_stop snapshot + gap  
- [x] Large gap returns warning; still confirmable  
- [x] DAR/recent journals can show stop-out provenance  
