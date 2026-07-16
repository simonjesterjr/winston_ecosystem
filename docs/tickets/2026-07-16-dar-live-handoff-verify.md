# Ticket: Live DAR cron verify PDF handoffs

**Status:** Proposed  
**Date:** 2026-07-16  
**Source:** Session `2026-07-16-1529-paper-fill-desk-handoffs-wrap.md`

## Problem

Handoff sections were smoke-rendered with synthetic/injected next_steps. Next scheduled Daily Analysis must prove live payload → PDF includes DESK HANDOFFS from real pending tasks.

## Scope

1. After next DAR job, open `storage/reports/wv2_YYYYMMDD.pdf`  
2. Confirm DESK HANDOFFS + Telegram phrase + desk URL for a real pending task  
3. Confirm MD mirror  

## Acceptance

- [ ] Production-path PDF shows human-gated phrases without manual inject  
