# Ticket: Interactive Brokers Client Portal unattended session (tickle is not login)

**Status:** In progress  
**Priority:** P2  
**Date:** 2026-09-06  
**Mode:** contractor  
**Graph nodes:** broker_gateway  
**Human gates:** paper-username browser SSO remains  
**DoD:** A documented, fail-closed path keeps the Client Portal Gateway brokerage session alive without a human re-SSO every idle timeout — or an explicit decision that human login stays the ritual  
**Origin:** Grill 2026-09-06 Fulfillment Ritual — [`docs/session-reports/2026-09-06-2149-fulfillment-label-and-desk.md`](../session-reports/2026-09-06-2149-fulfillment-label-and-desk.md)  
**Related:** `2026-08-31-bg-ibkr-read-adapter-l1.md` (tickle job exists); `2026-09-01-wq-ibkr-paper-evidence-bind.md` (tickle every minute)  
**Runbook:** [`docs/operations/ibkr-cpgw.md`](../operations/ibkr-cpgw.md)  
**See also:** Pulse session truth [`2026-09-11-wev-pulse-ibkr-cpgw-session-truth.md`](2026-09-11-wev-pulse-ibkr-cpgw-session-truth.md)

## Problem

`GET /tickle` only keeps an **existing** Client Portal Gateway session (~6 min idle). A human must still start the gateway and log in with the **paper** username, and re-SSO on `needs_reauth`. The Fulfillment Desk documents that ritual. It is not unattended login. Confirm-Send and DUT cash polls fail when the session is dead.

## Spike (2026-09-11) — duration, not unattended login

Logs (`ecosystem/vendor/ibkr-clientportal-gw/logs/gw.2026-09-0{9,10,11}.log`):

- **SSO:** 2026-09-09 08:26:28 MT `Client login succeeds` paper user; first `tickle,200` 08:27:04.
- **10 Sep:** **zero** `/sso/Login` hits. `tickle,200` every hour 00–23 (n=4755). Orders/trades HTTP 200 all day (DAY-order eval included).
- **Hold:** 2026-09-09 08:26 → 2026-09-11 04:56 (~**44.5 hours**) until `api.ibkr.com` DNS failure → `CP_LOGIN_FAILED`. Tickle cannot recover; `ssodh/init` 401s.
- **Idle ~6 min** is without tickle. Logged-in CPGW **self-tickles ~30s**; Broker Gateway `TickleJob` was also every minute 24×7 (including after 401).

**Decision:** human paper SSO stays law. Keep-alive is an **explicit window** (`run-ibkr-cpgw up` / `keepalive on` / `down`), not 24×7 on the off chance Winston might need it. Unattended SSO is still open.

## Scope

1. [x] Spike: tickle + `ssodh/init` do **not** recover without a browser. SSO stays mandatory for individuals.  
2. [x] Ritual + ops: `run-ibkr-cpgw`; TickleJob gated on `tmp/ibkr_keepalive.on`; 401 closes the window; `needs login` on ops/WQ; no DAR/Telegram spam.  
3. [ ] Winston-owned window: stand CPGW up, wait for human SSO, keep-alive, Broker Gateway for bound clients, then `down` **or** leave up for 15-minute DAY-order eval — still no password in git.

## Non-goals

- Live IBKR `env=live` unattended  
- Competing TWS / IBKR Desktop and Client Portal Gateway on the same username  

## Acceptance

- [x] Spike on this ticket: unattended is **not** possible with tickle; human SSO stays law; measured hold ~44.5h after one SSO  
- [x] Fulfillment Ritual + runbook match (explicit window, not 24×7 tickle)  
- [ ] If a later login path is automated: kill switch + `needs_reauth` still refuse write (ADR-013)  
