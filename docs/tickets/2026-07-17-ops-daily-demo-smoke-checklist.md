# Ticket: Ops daily demo smoke checklist (Ops UI + Telegram)

**Status:** Proposed  
**Date:** 2026-07-17  
**Epic:** `2026-07-17-ops-daily-demo-epic.md`  
**Priority:** High  

## Problem

Several “missing” daily functions may already work and just need operator verification. Without a written smoke, we keep re-implementing.

## Scope

Run once on live paper Active OPs; record pass/fail (no greenfield features unless smoke fails hard).

### Checklist

- [ ] Ops shell `list` — bands real → paper  
- [ ] Ops shell `positions` — all Active open lots  
- [ ] Ops shell `status <fp>` — capital, markets, journals  
- [ ] Desk form / `confirm` draft journal  
- [ ] `enter` / `exit` / `stop` on paper OP  
- [ ] Cash: MCP or API inflow + adjustment (note if shell missing)  
- [ ] `close_portfolio` on disposable OP (not cohort)  
- [ ] `successor` add-market on disposable engaged OP  
- [ ] Telegram: confirm phrase + one MCP mutation (after MCP rebuild)  

## Acceptance

- [ ] Results table (pass/fail/notes) in ticket or linked session report  
- [ ] Failures spawn or update gap tickets  

## Related

- Epic: `2026-07-17-ops-daily-demo-epic.md`  
