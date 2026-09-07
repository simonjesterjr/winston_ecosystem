# Ticket: Interactive Brokers Client Portal unattended session (tickle is not login)

**Status:** Proposed  
**Priority:** P2  
**Date:** 2026-09-06  
**Mode:** contractor  
**Graph nodes:** broker_gateway  
**Human gates:** paper-username browser SSO remains until this is solved  
**DoD:** A documented, fail-closed path keeps the Client Portal Gateway brokerage session alive without a human re-SSO every idle timeout — or an explicit decision that human login stays the ritual  
**Origin:** Grill 2026-09-06 Fulfillment Ritual — [`docs/session-reports/2026-09-06-2149-fulfillment-label-and-desk.md`](../session-reports/2026-09-06-2149-fulfillment-label-and-desk.md)  
**Related:** `2026-08-31-bg-ibkr-read-adapter-l1.md` (tickle job exists); `2026-09-01-wq-ibkr-paper-evidence-bind.md` (tickle every minute)

## Problem

`GET /tickle` only keeps an **existing** Client Portal Gateway session (~6 min idle). A human must still start the gateway and log in with the **paper** username, and re-SSO on `needs_reauth`. The Fulfillment Desk documents that ritual. It is not unattended login. Confirm-Send and DUT cash polls fail when the session is dead.

## Scope

1. Spike: can tickle + `ssodh/init` recover without a browser, or is SSO mandatory for individuals?  
2. If SSO stays: keep the ritual; surface `needs login` on ops/WQ (already v1); do not spam DAR/Telegram.  
3. If a keep-alive/login path exists: fail closed, paper username only, never store the password in git.

## Non-goals

- Live IBKR `env=live` unattended  
- Competing TWS and Client Portal Gateway on the same username  

## Acceptance

- [ ] Spike note in `docs/analysis/` or a decision on this ticket: unattended is possible **or** human SSO stays law  
- [ ] If still human: Fulfillment Ritual text stays accurate  
- [ ] If automated: kill switch + `needs_reauth` still refuse write (ADR-013)  
