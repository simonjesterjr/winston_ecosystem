# Ticket: LEAP-aware DAR / EOD narrative (MCP-grounded)

**Status:** Proposed  
**Date:** 2026-09-17  
**Priority:** P2  
**Origin:** Wrap follow-up; CUDA priority analysis item 3. Session `docs/session-reports/2026-09-17-1700-cromwell-llm-desk-and-daily-state.md`

## Problem

Mode C paper books (Blue / Red / Orange / Mango / Rust and siblings) use extra-modal Long-term Equity AnticiPation Securities (LEAP) / option packaging. Cromwell’s End of Day (EOD) Telegram still speaks like share Daily Analysis Report (DAR): units × price, no premium/expiry/cash-vs-premium flags. GPU 8b can narrate from Model Context Protocol (MCP) facts; it must not recompute Edge (R) or invent fills.

Loop-engineering put **narrator polish after** STATE + verifier. L1 skills are shipped; this is the next product slice on the same 8b, still drafts/commentary only.

## Scope

1. Skill (extend `winston-report-delivery` / `winston-daily-loop` — do not add a third narrator) with LEAP-aware lines: underlying, contracts, premium, expiry, cash impact vs share notional — **only fields present in the DAR/MCP payload**.
2. Quiet when no option-like pending/fills.
3. Never confirm, never edit journals, never recompute Edge.
4. Smoke: one EOD or interactive “the daily” on a Mode C book with a LEAP draft; Telegram has packaging fields or an honest “payload has no option fields”.

## Non-goals

- In-Rails `notes_draft` / `LlmClient` (priority analysis P2)
- Changing LEAP packaging math (ADR-017 / Wv2)
- Evolution Mode / auto-confirm

## Related

- Priority: [`../analysis/2026-09-17-cromwell-cuda-priority-revisit.md`](../analysis/2026-09-17-cromwell-cuda-priority-revisit.md)
- Role re-eval: [`../analysis/2026-09-17-llm-role-reeval-checker-narrator.md`](../analysis/2026-09-17-llm-role-reeval-checker-narrator.md)
- L1: [`2026-09-17-cromwell-daily-state-verifier.md`](2026-09-17-cromwell-daily-state-verifier.md)
- ADR-017, `docs/business-context/leap-extra-modal-proxy.md`
