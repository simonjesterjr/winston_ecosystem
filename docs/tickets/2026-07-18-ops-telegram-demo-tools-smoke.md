# Ticket: Live Telegram smoke — ops demo tools (#5–#7 + bulk/exit_reason)

**Status:** Proposed  
**Date:** 2026-07-18  
**Source:** Session `docs/session-reports/2026-07-18-1024-ops-demo-5-7-related-draft-equity.md`  
**Priority:** Medium (demo confidence; depends on MCP recreate)  
**Blocked by:** `2026-07-18-ops-mcp-recreate-after-demo-tools.md`

## Problem

RSpec and Rails-runner smokes passed for related-instrument fill, draft edit, and equity compare, but end-to-end Telegram (Cromwell → MCP → media attach / confirm speech) was not run this session.

## Scope

On a disposable paper OP (or known Active paper band), via Telegram:

1. **Related instrument** — book LEAP-style fill (or dry-run speech → tool args) and confirm journal shows `fulfillment_type=leap` + cash impact ×100.  
2. **Draft edit** — create or use pending draft → `edit_journal` / MCP edit → confirm sticky units/price.  
3. **Equity compare** — `wv2_compare_equity` Blue/Mango (or Orange/Rust); receive `reply_text` + chart PDF via `telegram_media_path` media attach.  
4. **Bulk / external stop** (if not already smoked on Telegram) — `exit_all` or `reason=external_stop` once.

## Acceptance

- [ ] Operator completes the three #5–#7 paths without Rails console  
- [ ] Equity compare chart arrives as Telegram document (not a bare path string)  
- [ ] Failures recorded with tool error codes  

## Related

- Epic: `docs/tickets/2026-07-17-ops-daily-demo-epic.md`  
- MCP recreate: `docs/tickets/2026-07-18-ops-mcp-recreate-after-demo-tools.md`  
- Confirm phrase smoke: `docs/tickets/2026-07-17-ops-live-telegram-confirm-phrase-smoke.md`  
