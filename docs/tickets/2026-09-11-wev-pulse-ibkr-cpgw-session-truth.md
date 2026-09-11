# Ticket: Pulse `ibkr_cpgw` from brokerage session, not tickle cron

**Status:** Proposed  
**Priority:** P2  
**Date:** 2026-09-11  
**Mode:** contractor  
**Program:** Winston Ecosystem View  
**Graph nodes:** winston_v2, broker_gateway  
**Human gates:** none  
**DoD:** Winston Ecosystem View (WEV) Pulse lights `ibkr_cpgw` only when the Client Portal Gateway (CPGW) brokerage session is authenticated (HTTP 200 / `authenticated: true`), not merely because Broker Gateway (BG) `ibkr_tickle` cron enqueued in the last 120s  
**Origin:** [`docs/session-reports/2026-09-11-0900-ibkr-cpgw-keepalive-session-yield.md`](../session-reports/2026-09-11-0900-ibkr-cpgw-keepalive-session-yield.md)  
**Related:** [`2026-09-06-ibkr-cpgw-unattended-session.md`](2026-09-06-ibkr-cpgw-unattended-session.md); [`2026-09-08-wev-pulse-other-monolith-emits.md`](2026-09-08-wev-pulse-other-monolith-emits.md) (TickleJob is silent Pulse Work by design); runbook [`docs/operations/ibkr-cpgw.md`](../operations/ibkr-cpgw.md)

## Problem

`Operations::EcosystemPulse` treats CPGW as live when `cron_fresh?(owners, "bg", "ibkr_tickle", 120)` (`winston_v2/app/services/operations/ecosystem_pulse.rb`). After keep-alive gating, `Adapters::Ibkr::TickleJob` still **enqueues every minute** and no-ops when the window is off or the session is 401. Pulse can show the `ibkr_cpgw` node and a `tickle` edge while `/iserver/auth/status` is 401 (observed 2026-09-11 08:12 MDT).

Silent Pulse Work for TickleJob is correct (no tablet row). Using cron freshness as **session truth** is not.

## Scope

1. Projector: `ibkr_cpgw` busy/flow from brokerage auth (BG binding `last_refresh_status`, keep-alive flag + HTTP 200, or a cheap BG health sample) — fail closed if unknown.  
2. Do not emit a Pulse Work row per tickle.  
3. Session Yield (`operator_holds_session`) must not look like a live Winston CPGW session.

## Non-goals

- Unattended paper Single Sign-On (SSO)  
- Telegram / Daily Activity Report (DAR) `needs login`  
- Changing TickleJob cadence

## Acceptance

- [ ] Pulse `ibkr_cpgw` off when CPGW process is up but auth is 401  
- [ ] Pulse `ibkr_cpgw` off when keep-alive window is off, even if `ibkr_tickle` cron is fresh  
- [ ] Pulse `ibkr_cpgw` off (or a distinct yielded state) during Session Yield  
- [ ] Spec on `EcosystemPulse` for the three cases  
