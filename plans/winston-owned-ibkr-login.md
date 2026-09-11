# Plan: Winston-owned Interactive Brokers paper login

**Status:** Proposed  
**Date:** 2026-09-11  
**Monoliths:** broker_gateway (BG), winston_v2 (Wv2), ecosystem  
**Mode:** contractor  
**Ticket:** [`docs/tickets/2026-09-11-winston-owned-ibkr-login.md`](../docs/tickets/2026-09-11-winston-owned-ibkr-login.md)  
**Depends on (shipped):** Fulfillment Desk **Initiate connection** + **Session Yield**; CPGW keep-alive window; ADR-013 fail-closed write  
**Peer (do not skip):** Broker push / websocket eval [`docs/tickets/2026-09-10-bg-broker-push-websocket-eval.md`](../docs/tickets/2026-09-10-bg-broker-push-websocket-eval.md)  
**Does not replace:** Human **Session Yield** to Interactive Brokers Desktop. The Fulfillment Desk binding page stays the glance and the kill switch.

## 1. Why this plan exists

Today Winston can **wait** for paper Single Sign-On (SSO) and then tickle. A human still types the paper username and password at https://localhost:5000/. That is **Initiate connection**. It is not unattended login.

The operator wants Winston to **decide** that Device Under Test (DUT) `DUT070450` is needed for a function (Desk Send, Accept-Fill, 15-minute DAY-order eval, overnight slate rebuild, Risk Capital snapshot) and then open the brokerage session **without** a human at the keyboard.

Tickle cannot do that. Measured 2026-09-11: after DNS/`CP_LOGIN_FAILED`, `ssodh/init` 401s until a browser SSO. See [`docs/tickets/2026-09-06-ibkr-cpgw-unattended-session.md`](../docs/tickets/2026-09-06-ibkr-cpgw-unattended-session.md).

## 2. Current law (do not regress)

| Surface | Today |
|---------|--------|
| Fulfillment Desk IBKR page | Session glance: Winston holds / keep-alive off / needs login / Desktop holds / waiting for login. **Initiate connection** waits for human SSO then keep-alive. **Yield** only while Winston holds. |
| Secrets | `AdapterBinding.secrets_pointer` is an opaque env-key name. BG never stores the paper password. `ibkr.env` has account id and flags only. |
| Write | ADR-013: `needs_reauth` / 401 refuses `place_order`. |
| Pulse | `ibkr_cpgw` is still cron-freshness, not session truth ([`2026-09-11-wev-pulse-ibkr-cpgw-session-truth.md`](../docs/tickets/2026-09-11-wev-pulse-ibkr-cpgw-session-truth.md)). |

The desk page remains **valid** after this plan. Auto-login does not delete the glance, Yield, or a kill switch. It adds a third verb: Winston may **take** the session when a named function needs DUT and the operator has not yielded.

## 3. Secrets — never in Grok, git, Telegram, or session reports

Paper username and password (and any one-time code) are **host secrets**.

**Allowed homes (pick one in the spike, not both forever):**

1. **1Password** — item for the paper username only. Runtime: `op inject` / `op read` into the BG process environment at start, or a host helper that exports into `broker_gateway/tmp/` with mode 0600 and never logs the value. Grok, Cromwell, and session reports see only `secrets_pointer` (e.g. `op://Sawtooth/IBKR-paper/password`).
2. **Gitignored env file** — same pattern as `ecosystem/deployment/ibkr.env`. New keys for username/password. File never committed. `printenv` in session reports must redact.

**Forbidden:**

- Pasting credentials into a Grok / Cromwell / Telegram prompt
- `CONTEXT.md`, tickets, session reports, Graphify Graph
- Winston v2 process memory as the home (BG owns broker secrets; Wv2 already must not)
- Checking `ibkr.env` into git “for convenience”

`secrets_pointer` on the DUT binding stays an opaque name. The value is resolved only inside BG at login time.

## 4. How Winston would log in (individuals)

Interactive Brokers (IBKR) **Web API OAuth 2.0** is aimed at organizations. Individuals on Client Portal Gateway (CPGW) still authenticate with a **browser SSO** to the local Java proxy. This plan does **not** assume a long-lived bearer token appears for paper DUT.

Realistic path:

1. Host CPGW already listening (`run-ibkr-cpgw start` or a later host unit). Compose still cannot SIGTERM that Java.
2. BG (or a tiny host helper next to CPGW) drives the CPGW login page **headless** (Playwright against https://localhost:5000/) using the secret from §3.
3. Same `ssodh/init compete:true` + keep-alive window we already have after a human SSO.
4. Fail closed on 2FA / IB Key / CAPTCHA — HITL on the Fulfillment Desk (`needs login`), do not invent a token.

**Spike (must precede implementation):** does paper DUT CPGW login require IB Key / 2FA on this username? If yes, either store TOTP in 1Password and type it headless, or stop — Winston cannot own login without a second factor.

## 5. Demand-driven connection (the point)

Winston does **not** hold DUT 24×7 “just in case.” Auto-login fires only when a **named consumer** needs the brokerage session and all of these are true:

- Auto-login is enabled (desk kill switch + env, default **off** until the spike is green)
- Binding is not **Session Yield** (Desktop holds)
- Function is one of: Desk Send, open-order/fill refresh for Accept-Fill, 15-minute DAY-order eval, overnight Session Order Slate rebuild, Risk Capital snapshot, websocket (re)subscribe

If the session is already Winston holds, do nothing. If CPGW is down, start is still a **host** problem (later unit/script); do not pretend compose can spawn Java.

When the cash session ends and no GTC/working DAY remains that needs DUT, Winston may `keepalive off` (leave Java up) or leave the window open for overnight rebuild — explicit, not 24×7 401 tickle.

## 6. Fulfillment Desk after auto-login

https://sawtooth-ai.tail944ffb.ts.net/wv2/operations/fulfillment/bnd_3d6a5020d839c315583277d2 stays the operator surface.

| Verb | After this plan |
|------|-----------------|
| Glance | Same session tags. Add `auto` vs `human` on Winston holds if useful. |
| **Initiate connection** | Force-now (same wait path). Still valid when auto-login is off or 2FA HITL. |
| **Yield session to Desktop** | Blocks auto-login until Resume / Initiate. Unchanged. |
| New: **Allow auto-login** | Binding-wide kill switch. Off = today’s human SSO. |
| Pulse / ops-shell `needs login` | Still glance-only; not DAR/Telegram spam. |

Wv2 never receives the password. It calls BG `session_hold` (already exists) or a later `session_hold auto=true`.

## 7. Dependency: CPGW websocket (DUT informs Winston)

A websocket does **not** replace login. IBKR documents the socket as something you open **after** the gateway session is authenticated.

Official:

- Open socket: [IBKR Campus — Open Websocket](https://ibkrcampus.com/docs/web-api/api-reference/websocket/open-websocket) — `GET wss://localhost:5000/v1/api/ws` (CPGW) or `wss://api.ibkr.com/v1/api/ws` (OAuth).
- Topics / subscribe: [Subscribing to Websocket Topics](https://ibkrcampus.com/docs/web-api/v1/ws/subscribing-to-websocket-topics.md), [Request Live Order Updates](https://ibkrcampus.com/docs/web-api/v1/ws/order-position-operations/request-live-order-updates.md), [Introduction](https://ibkrcampus.com/docs/web-api/v1/ws/introduction.md).
- Tutorial (session cookie / `{"session":"…"}` from `/tickle`): [How to connect to WebSocket](https://www.interactivebrokers.com/campus/ibkr-quant-news/tutorial-web-api-how-to-connect-to-websocket/).
- Vendored with this CPGW tree: `ecosystem/vendor/ibkr-clientportal-gw/doc/RealtimeSubscription.md` (`wss://localhost:5000/v1/api/ws`; solicited `sor` live orders, `spl` PnL, `ech+hb` heartbeat; unsolicited **`sts`** authentication / competing).

What the socket can do **for this plan** once a session exists:

| Topic | Why it matters |
|-------|----------------|
| **`sts`** | Unsolicited auth/compete. DUT/CPGW **informs** Winston the session died or Desktop competed — without a REST poll. That is the trigger to auto-login **or** to HITL if yielded / 2FA. |
| **`sor`** | Live order updates. Fills and cancels can append Winston Broker Evidence Standard events without waiting for the 15-minute poll. |
| **`system` / `ech+hb`** | Socket liveness. Dead socket ≠ dead brokerage session (must not flip `needs login` from socket drop alone). |

**Implication:** unattended websocket is useless if SSO is still a human. The socket dies with the brokerage session. **Winston-owned login is a prerequisite** for an unattended listener. The reverse is also true: `sts` is how auto-login knows it must run, instead of discovering 401 on the next REST poll.

**Do not implement the socket in the login spike.** Keep the eval ticket as eval-first. Update it so the go/no-go names this plan as a dependency (done in that ticket).

Poll remains the fallback even after a listener: 15-minute refresh so a silent socket cannot naked the book (Protective Stop Guardrail).

## 8. Phases

### Phase 0 — spike (this plan’s first ticket)

- [ ] Paper CPGW login: 2FA / IB Key or not, on **this** paper username  
- [ ] 1Password vs gitignored env: pick one home; document redaction  
- [ ] Headless login against localhost:5000 in a throwaway script on the host (not in Grok logs)  
- [ ] Confirm `sts` on a paper socket while a human session is up (subscribe only; no listener product)  
- [ ] Kill-switch sketch on the Fulfillment Desk  

### Phase 1 — BG auto-login behind the kill switch (paper only)

- [ ] Resolve `secrets_pointer` in BG only  
- [ ] `session_hold auto=true` no-ops if yielded, if kill switch off, or if already Winston holds  
- [ ] Named consumers may request hold; 401 after auto-login still refuse write (ADR-013)  
- [ ] Desk still shows waiting / needs login / Winston holds  

### Phase 2 — demand windows

- [ ] Cash-session / 15-minute eval / overnight rebuild request hold  
- [ ] Optional keepalive off when no working DAY/GTC needs DUT  
- [ ] Pulse session truth (existing P2 ticket) can then use `sts` or auth/status, not tickle cron  

### Phase 3 — websocket listener (only if eval ticket says go)

- [ ] BG listener (not a fifth monolith) on `wss://localhost:5000/v1/api/ws`  
- [ ] `sts` → auto-login or HITL  
- [ ] `sor` → evidence JSONL, same idempotency as poll  
- [ ] Poll stays fallback  

## 9. Non-goals

- Live IBKR (`env=live`) auto-login  
- Storing the password in Wv2, Grok, or Cromwell  
- Skipping Session Yield (auto-login must not steal Desktop)  
- Implementing the websocket in Phase 0–1  
- Unattended 2FA without a stored TOTP decision  
- Treating a dead websocket as `needs login` without REST confirm  

## 10. Acceptance (plan, not one PR)

- [ ] Spike answers 2FA and secret home  
- [ ] Fulfillment Desk still truthful with auto-login off (today’s behavior)  
- [ ] Auto-login never runs while Desktop holds  
- [ ] ADR-013 write still fail-closed on auth failure  
- [ ] Websocket eval ticket names this plan as a dependency and does not implement until Phase 0 is green  
