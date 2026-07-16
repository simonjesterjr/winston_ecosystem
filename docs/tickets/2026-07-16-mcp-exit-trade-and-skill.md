# Ticket: MCP `wv2_exit_trade` + Cromwell exit skill

**Status:** Proposed  
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

- [ ] Telegram can exit via explicit human phrase  
- [ ] Same accounting as shell exit  
