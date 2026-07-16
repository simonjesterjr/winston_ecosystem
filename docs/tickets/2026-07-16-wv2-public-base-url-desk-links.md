# Ticket: Configure `WV2_PUBLIC_BASE_URL` for DAR desk links

**Status:** Proposed  
**Date:** 2026-07-16  
**Source:** Session `2026-07-16-1529-paper-fill-desk-handoffs-wrap.md`

## Problem

PDF/MD DAR handoffs default desk URLs to `http://localhost:3002`. On phone Telegram that is not usable.

## Scope

1. Set `WV2_PUBLIC_BASE_URL` (or `WV2_OPS_BASE_URL`) in compose/env to Tailscale/host URL  
2. Document in ops/README or AI schedule README  
3. Re-render one DAR PDF to verify link

## Acceptance

- [ ] PDF desk links open ops desk from mobile network  
