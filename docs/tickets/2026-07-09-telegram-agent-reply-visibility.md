# Ticket: Telegram agent reply visibility (inbound OK, human may not see)

**Status:** Proposed  
**Priority:** unset
**Context:** Session `docs/session-reports/2026-07-09-1410-cromwell-cpu-tuning-and-watchdog.md`. Operator saw own DMs in nanobot logs but reported no bot replies. Server-side Bot API `sendMessage` / `sendRichMessage` to chat `8383774629` returned `ok: true` (message_ids 189–193). Agent also logged `Response to telegram:…` for at least one greeting.

## Problem

Unclear whether failure is: (a) Telegram client UX (wrong chat/account/folder), (b) nanobot outbound path intermittent, or (c) replies too slow (~70s) so operator left chat early.

## Acceptance criteria

- [ ] Operator confirms visibility of a Bot API DIAG/`🔔` message in `@sawtooth_nanobot` private chat  
- [ ] Operator confirms a short agent `ping` reply after `NANOBOT_MAX_CONCURRENT_REQUESTS=1`  
- [ ] If DIAG visible but agent not: capture nanobot logs around `Response to` + Telegram send errors; fix send path  
- [ ] If DIAG invisible: document client-side checklist (account, Message Requests, muted, multi-device)  

## Related

- Session report §5/§10/§11  
- Runtime: `nanobot_cromwell`, bot `@sawtooth_nanobot`  
