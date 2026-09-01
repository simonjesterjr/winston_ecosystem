# Fulfillment command vs broker executions (async reconciliation)

**Status:** working pattern (paper IBKR DUT, 2026-09-01)  
**Not an ADR.** Promote if we keep this as desk law.

## Problem

A Winston **command** is one Desk task / draft Journal (one WQ rebalance leg). A broker may emit **several** facts for that command: split executions (SPCX 1.0 + 0.06), delayed `/trades`, stale `/positions/0` vs live `portfolio2`, warning-reply before PreSubmitted.

This is a distributed, eventually consistent system. Treat it as **command/evidence**, not request/response.

## Identities (do not collapse)

| Layer | Identity | Mutability |
|-------|----------|------------|
| Command | Journal / OperationsTask (`client_order_key` / IBKR `cOID`) | One per leg |
| Evidence | `execution_id` (append-only JSONL) | Never merge |
| Witness A | `GET /iserver/account/trades` | Session/cache flaky |
| Witness B | `GET /iserver/account/orders` status | PreSubmitted → Filled |
| Witness C | Position delta (`portfolio2`, not `/positions/0`) | Laggy |

Byzantine-lite: **do not book from a single witness.** Confirm when **2 of 3** agree, or the human accepts a remainder. A lying/stale endpoint (empty trades, cached positions) must not veto a filled order.

## Trading / communication pattern

1. **Send (later) or hand-place:** one command, one `cOID` = `wq-{planId}-{legId}`.  
2. **Evidence:** each execution is its own `trade.executed` (idempotent on `execution_id`). Partial qty is **not** a mismatch.  
3. **Accumulate:** `SUM(exec.size)` on that `external_order_id` / `cOID` vs command units (round to broker increment 0.0001).  
4. **Desk Confirm once** when the sum is close enough, or HITL for remainder. Do not Confirm per execution.  
5. **Prefill** may attach many `broker_execution_ids`; it must **not** shrink command units to the first partial fill.  
6. **Kill switch:** auth-failed / competing session / o354 unanswered = attention, not invent.

## Class-share names

Same instrument, vendor spelling: `BRK.B` = `BRK-B` = `BRK B` via `TickerRemap.canonical` / `vendor_aliases`. Evidence may print `BRK B`; WQ market stays `BRK.B`; storage `BRK-B`.

## What we are not doing

Not PBFT consensus. Not auto-book from position snapshots. Not merging executions into one JSONL row (loses broker truth).
