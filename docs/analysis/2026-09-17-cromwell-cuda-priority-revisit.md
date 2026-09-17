# Analysis: Nanobot-Cromwell priorities after RTX 3090 CUDA (2026-09-17)

**Status:** Working recommendation for John / CoS  
**Ingests:** `plans/winston-plus-llm.md` (2026-06-12) · `plans/loop-engineering-and-evolution-mode.md` (2026-07-19/20) · CUDA session `2026-09-16-1955-rtx3090-ollama-cuda.md` · inventory ticket `2026-09-17-winston-llm-desk-inventory.md`  
**Non-goals unchanged:** LLM is **not** the signal engine. Edge (R) stays Ruby. Fingerprint law / ADR-006 successor forks stay. Core Rails must run with `ai` profile down.

## What changed since Jun / Jul

| Then | Now (2026-09-17) |
|------|------------------|
| Phase 0 “foundation” gated on MCP + Telegram daily use | **Phase 0 largely landed:** `winston_mcp`, `nanobot_cromwell`, Ollama, Cromwell skills + `schedule/manifest.yaml`, Telegram path |
| Local models were CPU-bound / aspirational | **RTX 3090 CUDA live** — `cromwell-qwen3:8b` observed **100% GPU**, 8k context; tags also present for 3b/4b/9b and base qwen/llama |
| Loop plan said “architect the daily loop” before Evolution Mode | Still correct — and **more urgent** now that GPU makes verifier/narrative quality cheap enough to use daily |
| Phase 1 monolith `LlmClient` not started | Still thin/absent in Wv2/WUT (augmentation still mostly **outside** Rails via nanobot) |
| Evolution Mode parked on Auto vs HITL paper A/B | Still parked; Mode C paper LEAP books (Blue/Red/Orange/Mango/Rust) raise the value of **commentary + checker**, not auto-mutation |

## Honest phase board

| Roadmap phase | Status | Evidence |
|---------------|--------|----------|
| **0** MCP + Cromwell bot + Ollama | **Done as foundation** (ops hygiene remaining) | Containers up; skills under `ecosystem/ai/skills/`; cron catalog; GPU model loaded |
| **1** Lightweight augmentation in monoliths | **Started outside Rails; inside Rails thin** | DAR/Telegram narrative path via nanobot; no first-class `OllamaClient` / journal `notes_draft` pipeline confirmed as desk SoT |
| **2** Ranking / safe config suggestion | **Not started** (correct) | Would violate maker–checker if rushed |
| **3** Cromwell as first-class daily-loop owner | **Partial via nanobot** — not a separate Cromwell monolith | Skills + cron ≈ loop owner; missing explicit STATE + stop conditions + verifier split |
| **4** Fine-tune / multi-model routing | **Feasible now, not priority** | Second analyst adapter ticket still P3; QLoRA session exists; wait for corpus + eval |

## Nanobot-Cromwell capability priority (what to build next)

Order is **desk ROI under GPU**, aligned to loop-engineering §1A→1C before Evolution Mode §2.

### P0 — Make the GPU desk trustworthy (this week)

1. **Finish LLM desk inventory** — **done** [`../tickets/archive/2026-09-17-winston-llm-desk-inventory.md`](../tickets/archive/2026-09-17-winston-llm-desk-inventory.md).
2. **Health / DNS hygiene** for `winston_mcp` + `nanobot_cromwell` (compose network names; avoid DEGRADED false alarms).
3. **Pin primary + fallback model tags** on GPU (`cromwell-qwen3:8b` primary candidate; smaller 3b/4b for triage/cron if needed). Short latency/quality smoke (not a tournament).
4. Document CDI leftover as P3 only — classic mounts are good enough.

*Why first:* without this, Phase 1 narrative work is built on sand.

### P1 — Daily loop engineering on Cromwell (highest product leverage)

From loop plan **1A / 1B / 1F** — does **not** require a new Rails monolith:

1. **Explicit daily STATE + stop/skip conditions**  
   Codify in `winston-daily-ops` (or sibling skill): DM ready? trading day? DAR ok? Mode C books present?  
   Emit bounded `STATE-YYYY-MM-DD` (markdown or PG+export). Loop must not “succeed” on partial work.
2. **Maker–checker split for pending decisions**  
   - Maker: DAR + sizer (deterministic)  
   - Checker: **separate** Cromwell skill/prompt that only sees signal facts, open risk, recent similar journals — output `TAKE | SIZE_DOWN | SKIP | HOLD` + structured reason  
   - Human remains fill gate (ADR-006).
3. **DAR / briefing narrative quality on GPU**  
   Narrative section of daily Telegram/report: grounded in MCP tool facts; never invents fills. Mode C LEAP paper books need LEAP-aware wording (premium spend, OA caveats) without touching Edge math.

*Why ahead of in-Rails LlmClient:* Cromwell already owns the human-facing loop; GPU makes checker+narrative good enough to use every RTH day.

### P2 — Phase 1 augmentation that feeds the loop (drafts only)

1. **Passed-signal / journal note drafts** via MCP tool → Ollama (or thin Wv2 `LlmClient` if we want Sidekiq ownership). Store as `notes_draft` / commentary jsonb — never sole decision record.
2. **Light RAG** over last N journals for a symbol (pgvector later; file/DuckDB ok for lab). WUT “explain this backtest day” as lab twin.
3. **Lesson write-back (loop 1C)** after stop-outs / skipped runners — append capped Lessons to MEMORY/skill appendix; promote only on second ritual.

*Guardrail:* schema-validate JSON; degrade cleanly if Ollama down.

### P3 — Phase 2 selection (only after P1 checker is boring)

1. Cross-portfolio concentration commentary for daily briefing.
2. Safe config **proposals** (approved knobs only) → WUT micro-gate → human → **successor fingerprint** (never in-place Engaged edit).
3. Do **not** open Evolution Mode until a closed paper A/B of auto-confirm vs HITL on an evolution lane exists (plan §2 still holds).

### P4 — Optional research (GPU enables, desk does not need yet)

1. Multi-model routing (3b triage / 8b draft).
2. Second **analyst** adapter (`2026-07-15-cromwell-analyst-adapter-future.md`) — separate from Telegram tool-router.
3. QLoRA on private traces — only after P1–P2 corpus is real.

## What not to prioritize

- LLM recomputing Edge, stops, or LEAP packaging.
- Silent TS mutation / Evolution Mode auto-apply.
- Replacing nanobot with a Cromwell Rails monolith **before** STATE + verifier skills work.
- Model tournament for its own sake.

## Recommended next 3 desk moves

1. ~~Complete inventory ticket + GPU pin~~ **done** 2026-09-17.  
2. ~~Ship daily STATE + stop conditions + verifier skill~~ **shipped** 2026-09-17 ([ticket](../tickets/2026-09-17-cromwell-daily-state-verifier.md)); first Cromwell-written STATE still due next EOD.  
3. Add **LEAP-aware DAR narrative** grounded in MCP for Mode C paper books — ticket [`../tickets/2026-09-17-leap-aware-dar-narrative.md`](../tickets/2026-09-17-leap-aware-dar-narrative.md); then journal `notes_draft` path (P2).

## Role re-eval (same day)

See [`2026-09-17-llm-role-reeval-checker-narrator.md`](2026-09-17-llm-role-reeval-checker-narrator.md): widen slogan to **orchestrator + triage + checker (+ narrator)**; do not over-invest narrator ahead of STATE/attention.

## Links

- Plan: [`../../plans/winston-plus-llm.md`](../../plans/winston-plus-llm.md)  
- Loop/Evolution: [`../../plans/loop-engineering-and-evolution-mode.md`](../../plans/loop-engineering-and-evolution-mode.md)  
- Inventory ticket: [`../tickets/archive/2026-09-17-winston-llm-desk-inventory.md`](../tickets/archive/2026-09-17-winston-llm-desk-inventory.md)  
- CUDA session: [`../session-reports/2026-09-16-1955-rtx3090-ollama-cuda.md`](../session-reports/2026-09-16-1955-rtx3090-ollama-cuda.md)
