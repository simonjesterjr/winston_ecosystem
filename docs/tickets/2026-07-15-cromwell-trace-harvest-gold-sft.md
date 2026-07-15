# Ticket: Cromwell trace harvest → gold SFT dataset

**Status:** Proposed  
**Date:** 2026-07-15  
**Priority:** Low (blocked on MCP/Cromwell reliability health)  
**Source:** Session report `docs/session-reports/2026-07-15-1615-lora-qlora-ecosystem-fit.md`

## Problem

QLoRA on noisy agent turns will encode hallucinations (placeholder paths, skipped tools, wrong sequences). We already emit useful raw material (`ecosystem/logs/audit/mcp/`, nanobot session JSONL) but have no process to turn successful multi-turn workflows into a reviewed gold SFT set.

## Preconditions

- Meaningful progress on Cromwell tool reliability / cron isolation (see `docs/tickets/2026-07-15-cromwell-llm-cpu-reliability.md` and related transfer/cron tickets).
- Plan note for model specialization exists or is co-drafted (`docs/tickets/2026-07-15-winston-model-specialization-plan.md`).

## Scope

1. Define harvest sources and retention (MCP audit lines + session JSONL success paths).
2. Sanitization rules: strip secrets, tokens, allowFrom IDs, PII; keep tool names, arg shapes, outcome structure.
3. Target example shape: system (Cromwell rules + tools) → user → tool_call(s) → tool results → grounded assistant summary.
4. Human review checklist for “gold” (correct tool order, no invented paths, Winston vocabulary, fail-closed on errors).
5. Initial volume goal: 50–200 multi-turn examples; store path convention under `ecosystem/` or `ai/` (offline corpus, not served to production rails).
6. Document “do not train on unreviewed dumps.”

## Acceptance

- [ ] Written harvest + sanitization procedure
- [ ] At least a seed gold set directory layout documented (even if empty)
- [ ] Review checklist checked in
- [ ] Explicit gate: no train job until gold set size/quality threshold met

## See also

- `docs/session-reports/2026-07-15-1615-lora-qlora-ecosystem-fit.md`
- `docs/tickets/2026-07-15-winston-model-specialization-plan.md`
- `ecosystem/logs/audit/mcp/` (source)
- `interfaces/winston-mcp-tools.md`
