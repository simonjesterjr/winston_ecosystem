# Ticket: MCP `wv2_exit_trade` + Cromwell exit skill

**Status:** Done (2026-07-16)  
**Date:** 2026-07-16  
**Source:** Session `2026-07-16-1529-paper-fill-desk-handoffs-wrap.md`  
**Related:** human-gated desk, `AdHocExitService`, ad-hoc fill

## Problem

Ops shell and desk form can exit positions. MCP/Telegram lack a first-class exit tool and skill, so Telegram phrases for exit rely on free-form that may not map cleanly.

## Scope

1. MCP `wv2_exit_trade` → `POST` internal exit (or reuse book path) wrapping `AdHocExitService`
2. `reply_text` / summary attachment
3. Cromwell skill (or extend `winston-ad-hoc-fill`) for exit authorization
4. Interface doc update

## Acceptance

- [x] Telegram can exit via explicit human phrase (`wv2_exit_trade` + skill)  
- [x] Same accounting as shell exit (`AdHocExitService` → `JournalConfirmationService`)  

## Delivered

| Surface | Detail |
|---------|--------|
| Wv2 | `POST /internal/journals/exit` → `InternalController#exit_journal` |
| Service | `AdHocExitService` (enriched portfolio/position payload) |
| MCP | `wv2_exit_trade` + `reply_text` / `summary` |
| Skill | `winston-ad-hoc-fill` extended with exit playbook |
| Interface | `ecosystem/interfaces/winston-mcp-tools.md` §6b |
| Specs | `spec/services/operations/ad_hoc_exit_service_spec.rb` |
| Cromwell | personas + VERSION 1.4.7 |

## Human phrase examples

```text
exit 12 AMZN price=250
@sawtooth_nanobot exit MSFT on 157 at 450.25
```

