# Ticket: EOD Signal Date / Fill Date + next-open prefill

**Status:** Done  
**Priority:** P1  
**Date:** 2026-07-20  
**Series:** `adr-009-desk-fulfillment` **#1**  
**Domain:** ADR-009, `docs/business-context/human-gated-desk-and-fulfillment.md`  
**Glossary:** Signal Date, Fill Date, Desk Handoff, Human-Gated  
**Completed:** 2026-07-21

## Problem

Canonical Winston EOD cadence is **signal on day T → fill at next session open on T+1**. Journals used a single `trade_date`; DA did not prefill next-open for confirm; dual spine dates were glossary-only.

## Delivered (2026-07-21)

1. **`Operations::EodCadence`** — stamps `signal_date`, `fill_date`, `next_open_*`, `price_source` into `fulfillment_details` / task metadata.
2. **`ParquetLookbackLoader.next_bar_after`** — next session bar for Fill Date / open prefill.
3. **`TaskGenerator`** — DA drafts carry dual dates; suggested_price only when next open known (never invent open from close).
4. **`JournalConfirmationService`** — prefers next-open prefill; books `trade_date` to fill (or today if early confirm); preserves signal_date in details.
5. **`ActionItemWindow` + `ExpireStaleActionItemsService`** — fill_date-aware process-miss expiry (`process_miss` metadata).
6. **Desk handoff / DAR / presenter / desk UI** — surface signal/fill cadence notes.
7. Specs: 27+ examples green (EodCadence, TaskGenerator, expire, confirm, parquet next_bar).

## Acceptance

- [x] Draft from DA stores signal date T and intended fill date T+1  
- [x] Confirm path can prefill next-session open when parquet present  
- [x] Unconfirmed past window → Passed Signal with clear reason  
- [x] Docs/MCP skills mention T/T+1 cadence (confirmation-loop skill)

## Related

- ADR-009  
- Series #2 Desk Workflow, #3 Signaled Entry, #6 DAR process-miss attention  
