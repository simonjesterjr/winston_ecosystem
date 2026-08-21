# Ticket: Wv2 — Desk Workflow HITL evidence UI

**Status:** Done  
**Priority:** P1  
**Date:** 2026-08-09  
**Series:** `trade-fulfillment-engine`  
**Domain:** Desk Workflow, Desk Confirm, Confirmation Intake, Human-Gated  
**Glossary:** Desk Workflow, Desk Confirm, Corrective Amend, Trade Notification, Desk Action  
**Monoliths:** **winston_v2**  
**Plan:** [`plans/trade-fulfillment-engine.md`](../../plans/trade-fulfillment-engine.md) Phase 7  
**Epic:** [`2026-08-09-l1-confirmation-intake-bg-build.md`](2026-08-09-l1-confirmation-intake-bg-build.md)

## Problem

Operators need to **see** matched broker evidence, mismatches, and orphans on the desk path. Without UI/ops surface, L1 prefill is invisible and humans cannot safely Confirm or Amend. Desk Confirm remains required — UI must never imply “evidence booked itself.”

## Scope

1. Extend Desk Workflow / ops desk surfaces (existing `/operations/desk` or adjacent) to show:  
   - Matched TradeNotification summary (symbol/side/qty/price/time/external ids)  
   - Match confidence / outcome  
   - Mismatch attention (signal story vs evidence)  
   - Orphan / unmatched queue (minimal list + attach action)  
2. Prefill fields visible and editable before **Desk Confirm**.  
3. Confirm / Corrective Amend remain explicit human actions — copy must not say “Send order.”  
4. No Desk Send control (L3 not authorized).  
5. Basic system specs or request specs for render + prefill display.  
6. Optional: MCP/Telegram phrase “review unmatched fills” deferred if UI-first is enough for v1 — note as follow-on.

## Non-goals

- Full journal browse redesign  
- L3 Send UI  
- Auto-confirm checkbox for real OPs  
- Email attach as primary path (human link workflow OK as secondary)

## Domain locks

- Human Confirm required  
- No place_order  
- Evidence is fulfillment truth, not Signal Spine rewrite  
- Ruby/Rails  

## Acceptance

- [x] Operator can view matched evidence on a desk handoff/journal  
- [x] Mismatch and orphan states visible  
- [x] Confirm still required after prefill  
- [x] No Send / place_order control  
- [x] Specs cover at least one happy-path prefill render  

Shipped 2026-08-19: `/operations/workflow` evidence panel; `/operations/intake` unmatched queue + human attach. Copy: Desk Confirm still books; does not send an order. MCP/Telegram “review unmatched fills” deferred.  

## Related

- Match: [`2026-08-09-wv2-match-prefill-confirmation-intake.md`](2026-08-09-wv2-match-prefill-confirmation-intake.md)  
- Integration specs: [`2026-08-09-wv2-confirmation-intake-integration-specs.md`](2026-08-09-wv2-confirmation-intake-integration-specs.md)  
