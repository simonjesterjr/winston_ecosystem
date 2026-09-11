# Ticket: Winston-owned IBKR paper login (secrets never in Grok)

**Status:** Proposed  
**Priority:** P2  
**Date:** 2026-09-11  
**Mode:** contractor  
**Graph nodes:** broker_gateway, winston_v2  
**Human gates:** paper DUT only; kill switch default off; Session Yield still blocks; no live `env=live`  
**DoD:** Phase 0 spike in the plan is written up (2FA?, secret home, headless CPGW login possible or not) — **not** an implementation of auto-login or websocket  
**Origin:** Operator 2026-09-11 after Initiate connection shipped — Winston should decide when DUT is needed and log in; Fulfillment Desk stays the glance  
**Plan:** [`plans/winston-owned-ibkr-login.md`](../../plans/winston-owned-ibkr-login.md)  
**Related:** [`2026-09-06-ibkr-cpgw-unattended-session.md`](2026-09-06-ibkr-cpgw-unattended-session.md) (tickle ≠ login; desk wait is shipped); [`2026-09-10-bg-broker-push-websocket-eval.md`](2026-09-10-bg-broker-push-websocket-eval.md) (socket **depends on** this); ADR-013

## Problem

**Initiate connection** waits for a human at https://localhost:5000/. Tickle cannot recover `needs_reauth`. The operator wants Winston to open the paper Client Portal Gateway (CPGW) session when a named function needs Device Under Test (DUT), with credentials in 1Password or a gitignored env file — never in Grok, git, Telegram, or session reports.

The Fulfillment Desk page for `bnd_3d6a5020d839c315583277d2` remains the glance, Yield, and kill switch.

## Scope (this ticket = plan Phase 0 only)

1. Spike: paper CPGW login 2FA / IB Key on this username.  
2. Spike: 1Password vs gitignored env; `secrets_pointer` only in PG.  
3. Spike: headless login against localhost:5000 (host script; redact logs).  
4. Confirm `sts` on a paper websocket while a **human** session is up (subscribe only).  
5. Kill-switch sketch on the desk (`Allow auto-login`, default off).

Implementation of auto-login is a **later** ticket after Phase 0 is green.

## Non-goals

- Shipping auto-login  
- Building the BG websocket listener  
- Live IBKR  
- Putting the password in a prompt or repo  

## Acceptance

- [ ] Plan Phase 0 boxes checked or explicitly blocked (2FA)  
- [ ] Websocket eval ticket updated with this dependency  
- [ ] No secret material in git / Grok traces  
