# Ticket: Telegram handoff — explicit non-goals (E)

**Status:** Proposed (reference / anti-scope)  
**Date:** 2026-07-15  
**Priority:** Low — decision record for planners  
**Source:** Session 2026-07-15 gap analysis E  

## Purpose

Capture what **not** to build for the “Telegram transfer felt broken” incident, so the next session stays on A–D.

## Non-goals (do not implement as “the fix”)

1. **New Telegram-only import product surface** — MCP transfer + Wv2 importer already work.  
2. **Desk / rake as primary operator path** for handoff — agent path is the goal; desk is verification only.  
3. **Auto-activate on import** — ADR-006 import always lands **inactive**; correct safety default.  
4. **Dual-Active automation** for same seed without force — mutex stays intentional.  
5. **Treating “only #12 Active” after transfer as failure** — paper focus OP stays Active; new OP inactive is success.  

## Prefer instead

| Priority | Ticket |
|----------|--------|
| A | `2026-07-15-cromwell-transfer-reply-contract.md` |
| B | `2026-07-15-wut-portfolio-config-fingerprint-export.md` |
| C | `2026-07-15-mcp-transfer-summary-and-error-guidance.md` |
| D | `2026-07-15-cromwell-llm-cpu-reliability.md` |

## Acceptance

- [x] Non-goals written (this doc)  
- [ ] Linked from session report handoff  

## Related

- ADR-006; Phase 3 wrap runbook  
- Live OP `#157` = WUT run 57 handoff artifact  
