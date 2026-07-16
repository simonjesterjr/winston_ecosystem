# Ticket: Cromwell core model promotion policy (checklist)

**Status:** Proposed  
**Date:** 2026-07-16  
**Priority:** Medium (process guardrail; blocks careless swaps)  
**Repos:** `ai/` ops  
**Source:** Session report `docs/session-reports/2026-07-16-1000-bonsai-core-model-advice.md`

## Problem

New local models (Bonsai 8B/27B, Qwen point releases, LoRA tags) will keep appearing. On CPU-only sawtooth-ai, swapping `agents.defaults.model` without a gate has already correlated with timeouts, think-token burn, and cron hallucinations. We need a **short, durable checklist** before any model becomes the Cromwell default.

## Decision recorded (2026-07-16)

- **Current production core:** `cromwell-qwen3:8b`  
- **Do not** promote Bonsai 27B to core until lab eval + this checklist pass.  
- Prefer **dual roles:** small/fast cron model (or thin non-LLM template) + quality interactive model.  
- A single heavier model owning cron + chat is disallowed by default on this host.

## Promotion checklist (all required)

- [ ] **Runner fit:** Model served via Ollama OpenAI-compat path nanobot already uses (or ADR for alternative).  
- [ ] **Side tag first:** Eval under a non-default tag for ≥1 session of real use or full harness.  
- [ ] **Tool harness:** Pass scenarios in 8B A/B ticket (or equivalent) — no placeholder paths, no invent-capital, transfer `reply_text` discipline.  
- [ ] **Latency:** Warm multi-tool turn within configured timeouts under normal load (Rails/Sidekiq idle-ish).  
- [ ] **Cron isolation:** Default cron model remains ≤3–4B class **or** thin template path; document which.  
- [ ] **Think off:** Qwen-family thinking disabled if it burns CPU (`think: false` / equivalent).  
- [ ] **Rollback:** One-line config revert documented; previous tag still on disk.  
- [ ] **Docs:** `ai/README.md` or example nanobot config updated; session report or ticket log notes the promote.  
- [ ] **No automatic pull** in compose health path that surprises operators with multi-GB downloads.

## Acceptance (for this process ticket)

- [ ] Checklist above lives in this ticket (or promoted to `ai/README.md` / deployment README)  
- [ ] Bonsai tickets link here as hard gate  
- [ ] Optional: add one-line pointer in `ecosystem/ai/schedule/README.md` CPU note  

## Non-goals

- Picking the next model in this ticket  
- GPU purchase decision (separate ticket)  

## Related

- `docs/session-reports/2026-07-16-1000-bonsai-core-model-advice.md`  
- `docs/tickets/2026-07-16-bonsai-8b-cromwell-ab-eval.md`  
- `docs/tickets/2026-07-16-bonsai-27b-lab-eval-when-runnable.md`  
- `docs/tickets/2026-07-15-cromwell-llm-cpu-reliability.md`  
- `docs/tickets/2026-07-15-cromwell-parallel-capacity-dual-runtime.md`  
- `docs/tickets/2026-07-15-cromwell-qlora-ollama-ab.md`  
- `ai/configs/nanobot-cromwell.example.json`  
