# Ticket: Second LoRA adapter for Winston analysis (future)

**Status:** Proposed  
**Date:** 2026-07-15  
**Priority:** Future / unscoped  
**Source:** Session report `docs/session-reports/2026-07-15-1615-lora-qlora-ecosystem-fit.md`

## Problem

Ops Cromwell (tool routing, Telegram voice, confirmation discipline) and “LLM analysis of Winston” (journals, regimes, backtest commentary) are different jobs. One fine-tuned ops adapter may be a poor fit for long-form research voice; a second adapter (or separate model tag) keeps roles clean.

## Scope (when prioritized)

1. Define analysis use cases (journal explain, regime commentary, WUT backtest day notes) — still drafts only; no capital mutation.
2. Corpus: journals, passed_signals, reports, WUT run summaries (not raw MCP tool spam).
3. Separate Ollama tag (e.g. `cromwell-analyst:…`) vs ops `cromwell-winston:…`; same or different base.
4. Call sites: Phase 1+ of `plans/winston-plus-llm.md` (optional `LlmClient` in Wv2/WUT), not live trade confirmation path.
5. Explicit: analysis adapter must not be the default Telegram tool-router.

## Acceptance (when work starts)

- [ ] Use cases + non-goals written
- [ ] Corpus sources listed
- [ ] Tag naming and which process loads which model documented
- [ ] No path where analyst model can confirm journals or move capital without human/ops bot rails

## See also

- `docs/session-reports/2026-07-15-1615-lora-qlora-ecosystem-fit.md`
- `docs/tickets/2026-07-15-cromwell-qlora-ollama-ab.md` (ops adapter first)
- `plans/winston-plus-llm.md` Phases 1–4
