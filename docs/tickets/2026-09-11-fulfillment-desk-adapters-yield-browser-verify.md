# Ticket: Browser-verify All adapters header + Session Yield

**Status:** Proposed  
**Priority:** P3  
**Date:** 2026-09-11  
**Mode:** contractor  
**Graph nodes:** winston_v2  
**Human gates:** operator click; paper Single Sign-On (SSO) only if testing Resume → Client Portal Gateway (CPGW) `up`  
**DoD:** On a desktop viewport (≥901px), ops-shell **All adapters** navigates; Fulfillment Desk index links to the IBKR binding page; **Yield session to Desktop** / **Resume Client Portal Gateway** round-trip  
**Origin:** [`docs/session-reports/2026-09-11-0900-ibkr-cpgw-keepalive-session-yield.md`](../session-reports/2026-09-11-0900-ibkr-cpgw-keepalive-session-yield.md)  
**Related:** [`2026-09-06-fulfillment-desk-compose-clickthrough.md`](2026-09-06-fulfillment-desk-compose-clickthrough.md) (older full-desk click path); [`2026-09-06-wv2-fulfillment-label-and-desk.md`](2026-09-06-wv2-fulfillment-label-and-desk.md); runbook [`docs/operations/ibkr-cpgw.md`](../operations/ibkr-cpgw.md)

## Problem

Desktop CSS set `pointer-events: none` on the ops-shell header `<summary>` and only re-enabled Quiver Tracking and Refresh. **All adapters** (and Ecosystem) looked like links and did nothing. Fix landed 2026-09-11 (`ops_shell.css`: all header `a`/`button` get `pointer-events: auto`). Session Yield form shipped on the IBKR binding detail. Verified via curl + digested CSS. **Not** clicked in a real browser.

## Work

1. Desktop width: ops shell → click **All adapters** → `/wv2/operations/fulfillment` (not a no-op / fold-only).  
2. Index: **IBKR L1 CPGW paper** (and the adapter-class row link) → `bnd_3d6a5020d839c315583277d2`.  
3. Binding page: **Yield session to Desktop** → flash + **Desktop holds session**; TickleJob / live polls held (optional: confirm IBKR Desktop stays connected).  
4. **Resume Client Portal Gateway** → hold cleared; does **not** log in.  
5. Ecosystem header link still works. Repeat once on a phone-width viewport (summary fold).

## Acceptance

- [ ] Desktop: All adapters click opens the Fulfillment Desk index  
- [ ] Index → IBKR binding detail  
- [ ] Yield / Resume round-trip visible on the page (tag + flash)  
- [ ] Mobile fold still allows the same links  

## Out of scope

- Playwright CI  
- Unattended SSO  
- Rebind  
