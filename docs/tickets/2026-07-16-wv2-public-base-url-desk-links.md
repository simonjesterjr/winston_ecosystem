# Ticket: Configure `WV2_PUBLIC_BASE_URL` for DAR desk links

**Status:** Done (2026-07-16/17)  
**Date:** 2026-07-16  
**Source:** Session `2026-07-16-1529-paper-fill-desk-handoffs-wrap.md`

## Problem

PDF/MD DAR handoffs default desk URLs to `http://localhost:3002`. On phone Telegram that is not usable.

## Scope

1. Set `WV2_PUBLIC_BASE_URL` (or `WV2_OPS_BASE_URL`) in compose/env to Tailscale/host URL  
2. Document in ops/README or AI schedule README  
3. Re-render one DAR PDF to verify link

## Acceptance

- [x] PDF desk links open ops desk from mobile network  

## Implemented

- `compose.yml`: `WV2_PUBLIC_BASE_URL=https://sawtooth-ai.tail944ffb.ts.net/wv2` on `winston_v2` + `winston_v2_sidekiq`
- Docs: `ecosystem/deployment/wv2-public-url.md`
- `DeskActionHandoff` defaults `form_url` host from the same env
- Verified live MD/PDF handoff desk URL (session 2026-07-17)
