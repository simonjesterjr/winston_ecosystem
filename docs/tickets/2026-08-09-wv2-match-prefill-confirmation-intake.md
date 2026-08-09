# Ticket: Wv2 — match + prefill Confirmation Intake (never auto-book)

**Status:** Ready  
**Priority:** P1  
**Date:** 2026-08-09  
**Series:** `trade-fulfillment-engine`  
**Domain:** Confirmation Intake, Single Fulfillment Identity, Extra-Modal Fulfillment, Human-Gated  
**Glossary:** Trade Notification, Single Fulfillment Identity, Desk Confirm, Corrective Amend, Extra-Modal Fulfillment  
**Monoliths:** **winston_v2**  
**Plan:** [`plans/trade-fulfillment-engine.md`](../../plans/trade-fulfillment-engine.md) Phase 7; atomics `match_notification` / `prefill_from_match`  
**Epic:** [`2026-08-09-l1-confirmation-intake-bg-build.md`](2026-08-09-l1-confirmation-intake-bg-build.md)

## Problem

Inbound TradeNotifications must attach to a **Single Fulfillment Identity** (draft journal/task/package leg) for desk prefill — without silent booking. Extra-modal fulfillment forbids symbol-equality-only match. Grill B Q9 match detail is deferred; ship a **safe v1 matcher** with explicit failure modes.

## Scope

1. **Match algorithm sketch (v1):**  
   - Explicit human/prior link if present  
   - Soft match: OP binding + side + time window + underlying-aware / size band (not broker.symbol == Book.symbol alone)  
   - Outcomes: `exact` | `soft` | `ambiguous` | `orphan` | `mismatch`  
2. **Prefill:** write draft journal field deltas (price, qty, packaging hints) from match — **do not** execute journal or open Position.  
3. **Ambiguous / orphan:** queue for human pick; never pick silently.  
4. **Mismatch:** surface attention; allow Corrective Amend path after human review (UI ticket).  
5. Integrate with existing Desk Confirm / amend services **only as prefill inputs**.  
6. Specs for each match outcome; extra-modal case (signal IBM / fill LEAP symbol).

## Non-goals

- Silent auto-book (explicitly forbidden)  
- L3 Desk Send  
- Final Q9 product law (document assumptions; revisit post-build)  
- Exit Capital Reconcile application (D10)  

## Domain locks

- Human still **Desk Confirms**  
- No `place_order`  
- No email SoT  
- Ruby/Rails  
- Match ownership in **Wv2** (not BG)  

## Acceptance

- [ ] Match service returns typed MatchResult outcomes  
- [ ] Prefill updates draft fields only  
- [ ] Specs prove **no** Position open / journal execute from match alone  
- [ ] Extra-modal: no symbol-equality-only match  
- [ ] Orphan + ambiguous paths do not invent links  
- [ ] Q9 deferred notes documented  

## Related

- Store: [`2026-08-09-wv2-trade-notification-store-and-normalize.md`](2026-08-09-wv2-trade-notification-store-and-normalize.md)  
- Desk UI: [`2026-08-09-wv2-desk-workflow-hitl-evidence-ui.md`](2026-08-09-wv2-desk-workflow-hitl-evidence-ui.md)  
- D10 capital (related): [`2026-08-05-signal-path-truth-fulfillment-link-exit-reconcile.md`](2026-08-05-signal-path-truth-fulfillment-link-exit-reconcile.md)  
