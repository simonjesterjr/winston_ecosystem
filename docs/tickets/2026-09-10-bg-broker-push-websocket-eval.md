# Ticket: Evaluate broker push / websocket vs 15-minute poll (IBKR, later Schwab)

**Status:** Proposed  
**Priority:** P1  
**Date:** 2026-09-10  
**Mode:** contractor  
**Graph nodes:** broker_gateway, winston_v2  
**Human gates:** paper DUT only; do not Desk-Send; do not turn on a live stream in this ticket  
**DoD:** A written evaluation (this ticket or a linked analysis) states what Interactive Brokers (IBKR) Client Portal Gateway (CPGW) and Charles Schwab can actually *push* to us, whether a Broker Gateway (BG) listener is worth it, and a go / no-go for a small ingest sidecar — **not** an implementation  
**Origin:** Walnut fill-driven repark plan 2026-09-10 (operator: websocket may help; evaluate before building; 15-minute poll is the start)  
**Related:** [`2026-09-09-walnut-paper-session-order-slate.md`](2026-09-09-walnut-paper-session-order-slate.md); ADR-013; `interfaces/winston-broker-evidence-standard.md`; [`2026-09-06-ibkr-cpgw-unattended-session.md`](2026-09-06-ibkr-cpgw-unattended-session.md); **depends on Winston-owned login** [`2026-09-11-winston-owned-ibkr-login.md`](2026-09-11-winston-owned-ibkr-login.md) / [`plans/winston-owned-ibkr-login.md`](../../plans/winston-owned-ibkr-login.md)

## Problem

Walnut Session Order Slate stop-markets **Accept-Fill** from a **poll**: BG `refresh` → CPGW `GET /iserver/account/trades` and `GET /iserver/account/orders` → Winston v2 (Wv2) Confirmation Intake → `WqFillBind`. There is **no HTTP webhook** from IBKR to Sawtooth today. CPGW has an optional websocket (`wss://localhost:5000/v1/api/ws`) we do not use. **Official:** [Open Websocket](https://ibkrcampus.com/docs/web-api/api-reference/websocket/open-websocket), [Subscribing to Websocket Topics](https://ibkrcampus.com/docs/web-api/v1/ws/subscribing-to-websocket-topics.md), [Request Live Order Updates](https://ibkrcampus.com/docs/web-api/v1/ws/order-position-operations/request-live-order-updates.md), [connect tutorial](https://www.interactivebrokers.com/campus/ibkr-quant-news/tutorial-web-api-how-to-connect-to-websocket/). Vendored: `ecosystem/vendor/ibkr-clientportal-gw/doc/RealtimeSubscription.md`.

Operator lock 2026-09-10: **15-minute poll is adequate** for End of Day (EOD) Trend Following (TF) (~32 evaluations in regular hours; ~96/day if left on). “As soon as possible” is **not** a live-data mandate. A websocket (or any broker push) is a **P1 evaluation**, not this grain’s implementation.

A faster path would only matter for:

- Naked-lot window after a DAY STP prints (Protective Stop Guardrail)
- Stop-out of a Good-Til-Cancelled (GTC) protective during the session
- Later extra-modal / Schwab live, if those venues actually push

## What to evaluate (do not skip)

### 1. What can IBKR send us?

Document against **current CPGW paper DUT**, not TWS lore:

- REST we already poll: `/iserver/account/trades`, `/iserver/account/orders`, `/portfolio/.../positions`
- Websocket topics (order status `sor` / `tr` / account updates — **verify in IBKR Campus docs and a paper subscribe**, do not assume)
- Session coupling: does the socket die with the ~6 minute brokerage idle? Does `tickle` keep it? Does `compete: true` kick TWS the same way?
- Auth: SSO vs iserver; does a socket survive `needs_reauth`? Unsolicited **`sts`** (authenticated / competing) is how DUT **informs** Winston the session died without a REST poll.
- **Dependency:** the socket requires an authenticated CPGW session. An unattended listener is blocked until Winston-owned login (plan above) can re-SSO. Do not implement the listener in this eval. Phase 0 of that plan may **subscribe** on a human-held session to confirm `sts` / `sor` payloads.
- Payload: do we get `execution_id` / `order_id` / `cOID` that map to Winston Broker Evidence Standard `trade.executed` / `order.filled`?
- Rate limits, reconnect, duplicate prints (idempotency keys already exist on the JSONL log)
- **No webhook URL** we can register — confirm this is still true

### 2. What can Schwab send us?

Schwab Trader API is L1 **read** today. Evaluate (sandbox first):

- REST poll vs streaming (Streamer / `CHASE_TRADE` style) vs any webhook
- Whether a fill event exists that is not “we asked again”
- Binding split: WQ live Schwab vs IBKR paper DUT — one listener vs per-adapter

### 3. Architecture if we implement later

Operator sketch to stress-test, not to build now:

- A **small listener inside BG** (not a fifth majestic monolith, not Wv2) that accepts *any* downstream broker update (socket, later webhook)
- Normalize into the existing Winston Broker Evidence Standard JSONL (`trade.executed`, `order.upserted`, …) with the same idempotency keys as poll
- Wv2 still **adjudicates** (match / Accept-Fill / Fill-Driven Repark). The listener does **not** book journals
- Poll remains the fallback (15 min) so a dead socket does not naked the book
- Fail closed on auth; no invent

Questions the eval must answer:

- Is this a Sidekiq thread, a Puma process, or a tiny compose service next to `broker_gateway`?
- One socket per AdapterBinding vs one process for all IBKR paper bindings?
- How does it share CPGW session with `TickleJob` without a second `compete`?
- If `sts` says unauthenticated: call Winston-owned login, or HITL if Session Yield / kill switch off / 2FA? Dead socket must not be treated as `needs login` without REST confirm.

## Non-goals (this ticket)

- Implementing a websocket or webhook
- Changing the 15-minute WorkingFill / Confirmation Intake cadence
- Native IBKR `replace_order`
- Extra-modal LEAP evaluation
- Treating poll lag as a defect (EOD TF accepts it)

## Acceptance

- [ ] Table: IBKR CPGW — webhook? websocket topics? session/auth constraints? evidence field mapping?  
- [ ] Table: Schwab — same columns, sandbox vs live  
- [ ] Go / no-go: build a BG listener sidecar, stay on 15-minute poll, or hybrid (poll + socket for order status only)  
- [ ] If go: one-page sketch of process boundary, Evidence Standard events, and fallback poll — still a later ticket to implement  
- [ ] Go path names Winston-owned login as a **prerequisite** for unattended `sts` / `sor` (human SSO is enough for the eval subscribe)  
