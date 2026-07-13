# Sawtooth Ecosystem — Permanent Knowledge Base

**This is the single source of truth for the Winston / data_manager / Cromwell / Winston v2 majestic monolith ecosystem.**

**Rule for all future work (AI or human):** Before planning, designing, or coding any change that touches DM, WUT, Wv2, Cromwell, data flows, or cross-monolith coordination, read the contents of this folder:

```bash
cat ecosystem/principles/*.md ecosystem/plans/*.md ecosystem/interfaces/*.md ecosystem/deployment/*.md 2>/dev/null | head -200
# or simply explore the subdirectories
```

## Contents
- `AGENTS.md` — Agent onboarding rules (read after this README).
- `principles/` — Core philosophy, vision, rules we live by (majestic monoliths, async + webhooks + agentic Cromwell, parquet Winston standard, etc.). Update on every material decision.
- `plans/` — Authoritative copies or references to major implementation plans (e.g. this data download service plan, winston-v2, and the new MCP access layer + LLM roadmap). The detailed working copy may live in `.grok/sessions/...` during a session; promote the final version here.
- `interfaces/` — Contracts: Winston EOD parquet standard schema, API shapes between monoliths, Cromwell notification payloads, etc.
- `CONTEXT.md` — Domain glossary (canonical terms; use with `/grill-with-docs`).
- `docs/` — ADRs, business-context, session reports, issues, tickets, technical analysis. See `docs/README.md` for the filing guide.
- `business_analysis/` — business / operator evaluations (PBR rankings, promotion candidates, experiment economics). See `business_analysis/README.md`.
- `.grok/skills/` — Developer session skills (`session-report`, `wrap`, `record`, `adversary`, `stakeholder`, `grill-with-docs`). Cromwell *runtime* skills remain in `ai/skills/`.
- `ai/` — Cromwell agent assets: personas, skills, memory templates. Deploy with `bin/seed-cromwell-workspace`. Part 2 backlog: `plans/cromwell-ai-skills-part2.md`.
- `deployment/` — Podman / compose, env templates, credential placement (EODHD key goes in the documented spot once supplied), volume strategies.
- `hints/` — Growing collection of cues, gotchas, "always do X", references back to WUT mature code, etc.

## Why this folder exists
Long-running multi-monolith project. We refuse to re-explain or hallucinate context every session. This folder (at the top of `~/Documents/com/sawtooth`) survives any single app and is the place the AI (and you) always come back to for hints, cues, and implemented plans.

Start here. Then explore the monoliths (`winston_unit_test/` is the current mature reference for data/portfolio patterns; `winston/` is legacy).

## Current Monoliths (as of 2026-06-12)
1. data_manager (DM) — EODHD → parquet Winston standard + PG metadata + reconciliation + Cromwell notifications. Symmetric support for WUT + Wv2 consumers.
2. winston_unit_test (WUT) — backtesting + daily ops (mature reference for data/portfolio/strategy patterns, Sidekiq, export of configs/TradingStrategies to Wv2).
3. winston_v2 (Wv2) — live operational trading (portfolios, CashEvents, TradingStrategies for loose methodology coupling, daily analysis, journals, MCP exposure surface).
4. winston (v1) — legacy, abandon.
5. Cromwell (agentic coordinator) — in progress via MCP + nanobot/Telegram layer (the "Cromwell bot") + webhooks; future dedicated monolith/service for full orchestration.
6. **eta-service-2.0** (sibling, separate repo in workspace) — Denali ETA calculation engine (.NET). Independent domain and governance; harvest agent/doc patterns only.

All communication: APIs (internal) + Sidekiq (internal) + webhooks (to Cromwell) + file mounts for parquet + MCP (new agentic surface for Wv2 core use cases) where beneficial. Podman compose at root (core services always available; AI/ollama/nanobot/MCP layer strictly optional via profiles).

**Session discipline:** End substantive sessions with `/wrap` or `/session-report`. Cross-monolith reports go in `docs/session-reports/`.

See principles/ and plans/ for details. Key recent additions (read these first for the current workstream):
- plans/winston-mcp-immediate.md (the only slice enabled for the next build turn)
- plans/winston-mcp-next-steps.md
- plans/winston-plus-llm.md (long-term native LLM + RAG + orchestration direction)

Always start a session by reading the ecosystem folder. New plans (MCP access layer + LLM roadmap) live alongside the original DM and Wv2 plans.

> **Do not use `___ecosystem/`** — it is deprecated. See `___ecosystem/DEPRECATED.md`.
