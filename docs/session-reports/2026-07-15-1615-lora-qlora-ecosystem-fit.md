# Session Report — LoRA/QLoRA Fit for Winston Ecosystem

**Date:** 2026-07-15
**Time:** ~16:00–16:15 MDT
**Duration:** ~15m
**Project:** sawtooth / Winston ecosystem (Cromwell + LLM roadmap)
**Working directory:** `/home/johnkoisch/Documents/com/sawtooth`
**Branch:** `ecosystem` repo `main` (docs-only; no code branches touched)
**Model:** Grok (xAI)
**Operator:** johnkoisch

---

## 1. Goal & Outcome

**Stated goal:** Understand how to fine-tune an LLM (and “I matrix”); explore whether LoRA/QLoRA belongs in the Winston ecosystem as a natural extension of MCP work and future LLM analysis.

**Outcome:** Delivered (conceptual / architectural alignment only — no code)

**One-line summary:** Fine-tuning was explained (full FT vs LoRA/QLoRA vs imatrix); LoRA was positioned as a Phase-4-style optional AI adapter for Cromwell tool-use and Winston dialect, not a new monolith or signal engine.

---

## 2. Work Completed

- Explained LLM fine-tuning pipeline (data → full FT / PEFT / QLoRA → eval → deploy/quantize).
- Clarified **imatrix** (llama.cpp importance matrix for quantization) vs **LoRA matrices** (A/B adapters) vs identity matrix.
- Grounded discussion in existing plans:
  - `ecosystem/plans/winston-plus-llm.md` (Phase 4: tool-use fine-tuning on traces)
  - `ecosystem/plans/winston-mcp-next-steps.md` (MCP as forcing function; traces → training/RAG)
  - Current AI layer: Ollama + nanobot + `winston_mcp`, CPU-only `cromwell-qwen2.5:3b`
- Proposed architecture placement: offline train → versioned adapters → serve in `ai/` profile only; rails monoliths unchanged.
- Recommended sequencing: stabilize MCP + gold traces → RAG/few-shot → LoRA (not train on messy traces first).
- Outlined future ticket slice (trace harvest, gold set, train recipe, A/B, second analyst adapter) — **not filed this session**.

---

## 3. Code Delivered

### Files changed

| File | Change | Notes |
|------|--------|-------|
| `ecosystem/docs/session-reports/2026-07-15-1615-lora-qlora-ecosystem-fit.md` | added | This report (at wrap) |

### Commits

- _None prior to wrap; commit may include this report only._

### Branch / PR state at sign-off

- Branch: `ecosystem` `main` — dirty from **other sessions** (unrelated skills/tickets/WUT); this session’s only intentional artifact is the session report
- Pushed: pending wrap
- PR: not opened

**Note:** Pre-existing dirty trees were observed and must not be committed as part of this session:

- `ecosystem/`: many modified AI skills, tickets, interfaces (prior work)
- `winston_unit_test/`: portfolio config exporter WIP (prior work)

---

## 4. Decisions Made

### Decision 1: LoRA is ecosystem-optional, not a monolith
- **Choice:** Treat QLoRA/LoRA adapters as versioned AI artifacts under the optional `ai/` profile (Ollama Modelfile / model tags), not as logic inside DM/WUT/Wv2.
- **Why:** Matches majestic monoliths + “core runs without AI”; MCP remains the safe surface.
- **Alternatives considered:** Train-in-compose on trading host; embed training in Wv2; replace skills with fine-tune only.
- **Reversibility:** easy (swap model tag; disable `ai` profile)
- **Promote to ADR?** yes — candidate ADR when scoped (“model adapters are optional AI config; training offline”)

### Decision 2: Fine-tune for operator fit, not alpha
- **Choice:** Primary LoRA targets = tool selection, Winston vocabulary, Telegram voice, fail-closed behavior — not signal generation.
- **Why:** Aligns with `winston-plus-llm.md` non-goals (deterministic strategies remain decision engines).
- **Alternatives considered:** Train on OHLCV/price prediction.
- **Reversibility:** easy
- **Promote to ADR?** optional (can live in plan note)

### Decision 3: Sequencing before training
- **Choice:** Stabilize MCP + collect gold traces → RAG/few-shot → LoRA; training GPU may be off-box; serve small adapters on CPU Ollama.
- **Why:** Fine-tuning amplifies data quality; sawtooth-ai is CPU-only for inference.
- **Alternatives considered:** Immediate QLoRA on current session/MCP noise.
- **Reversibility:** easy
- **Promote to ADR?** no — plan/sequencing note is enough

---

## 5. Insights Surfaced

- Existing roadmap already anticipates this: Phase 4 “tool-use fine-tuning on our traces” and next-steps “preparation for deeper LLM integration.”
- High-value training corpus already accruing: `ecosystem/logs/audit/mcp/`, nanobot session JSONL, skills/SOUL — but quality is mixed until cron/tool reliability work lands.
- Skills + MCP `summary` fields are stopgaps for weak models; LoRA reduces babysitting but does not replace the MCP contract or confirmation rails.
- **imatrix** is quantization quality, orthogonal to LoRA training (pipeline order: adapt → merge → optional imatrix quant).
- Dual-adapter future: ops bot (`cromwell-winston`) vs research/analysis adapter later — same base, different PEFT heads.

---

## 6. Issues & Tickets

### Resolved this session
- _None (Q&A / architecture only)._

### Deferred
- File a short plan note or ADR: “Winston model specialization” — **See:** `docs/tickets/2026-07-15-winston-model-specialization-plan.md`
- Trace harvest + gold multi-turn SFT set (50–200) — **See:** `docs/tickets/2026-07-15-cromwell-trace-harvest-gold-sft.md`
- Offline QLoRA recipe + Ollama tag A/B — **See:** `docs/tickets/2026-07-15-cromwell-qlora-ollama-ab.md`
- Second adapter for Winston analysis (future) — **See:** `docs/tickets/2026-07-15-cromwell-analyst-adapter-future.md`
- Do not train until cron/tool reliability work is further along (see e.g. `docs/tickets/2026-07-15-cromwell-llm-cpu-reliability.md`)

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| Architecture claims vs plans | Read `winston-plus-llm.md`, MCP plans, `ai/` Modelfile | ✅ |
| Implementation | N/A | _None_ |

**Test command(s):** _None._

---

## 8. Environment, Dependencies, Data

- **Dependencies:** None
- **Services:** None started this session
- **Migrations:** None

---

## 9. Risks & Technical Debt

- Training on current noisy Cromwell traces could encode hallucination patterns (placeholder paths, skip-tool hourlies).
- Operator may under-estimate GPU need for training vs CPU-only inference.
- Pre-existing uncommitted work in `ecosystem/` and WUT risks accidental bundling if wrap uses broad `git add`.

---

## 10. Open Questions

- **When to file the specialization plan/ADR?** — needs answer from: operator priority; blocks: nothing urgent
- **Which base model for first adapter (3B CPU vs 7B/8B)?** — needs answer from: hardware + tool-call A/B; blocks: train recipe
- **Primary RAG store when Phase 1 starts?** — already open in `winston-plus-llm.md`

---

## 11. Handoff & Resume Notes

- **Where I left off:** Conceptual agreement that LoRA is a natural later extension; offered to draft a half-page plan/ADR when requested; no artifacts filed beyond this report.
- **Next concrete step (if resuming this thread):** Draft `ecosystem/plans/winston-model-specialization.md` (or ADR) with problem, non-goals, data sources, artifact lifecycle, placement in `ai/`.
- **Files to read first:**
  1. `ecosystem/plans/winston-plus-llm.md`
  2. `ecosystem/plans/winston-mcp-next-steps.md` (§ Open / Later)
  3. `ecosystem/interfaces/winston-mcp-tools.md`
  4. `ai/ollama/Modelfile.cromwell-cpu`
  5. This session report

---

## 12. Stakeholder Communications

- _None required._ Optional: one-paragraph note that private model specialization is planned after MCP reliability and gold traces, not a change to trading signal engines.

---

## 13. Tools & Workflow Notes

- **Skills used:** `wrap`, `session-report` (this wrap)
- **What worked well:** Reading existing LLM/MCP plans before inventing architecture; tying LoRA to real pain (tool reliability, dialect) not generic ML hype
- **Friction points:** Workspace has large unrelated dirty trees — wrap must commit only this session’s report
- **Subagent usage:** None

---

## 14. Follow-up Actions

- [ ] Draft plan note or ADR: Winston model specialization — **See:** `docs/tickets/2026-07-15-winston-model-specialization-plan.md`
- [ ] Trace harvest → gold SFT dataset (after MCP reliability healthier) — **See:** `docs/tickets/2026-07-15-cromwell-trace-harvest-gold-sft.md`
- [ ] Offline QLoRA recipe + Ollama tag A/B — **See:** `docs/tickets/2026-07-15-cromwell-qlora-ollama-ab.md`
- [ ] Second adapter for Winston analysis (future) — **See:** `docs/tickets/2026-07-15-cromwell-analyst-adapter-future.md`

---

## 15. Appendix (optional)

### Mental model agreed this session

```
Pretrained LLM
  → (optional) domain continued pretrain
  → SFT / QLoRA on Winston tool-use + dialect
  → (optional) preference (DPO) on preferred vs rejected agent turns
  → serve via Ollama (ai profile)
  → (optional) imatrix-aware quant for smaller GGUF
```

### Explicit non-goals

- LLM does not replace deterministic signal/risk engines
- Training does not run as a Sidekiq job on the trading host
- Core monoliths remain fully functional without adapters
```
