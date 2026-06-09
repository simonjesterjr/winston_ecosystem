# Sawtooth Ecosystem — Permanent Knowledge Base

**This is the single source of truth for the Winston / data_manager / Cromwell / Winston v2 majestic monolith ecosystem.**

**Rule for all future work (AI or human):** Before planning, designing, or coding any change that touches DM, WUT, Wv2, Cromwell, data flows, or cross-monolith coordination, read the contents of this folder:

```bash
cat ecosystem/principles/*.md ecosystem/plans/*.md ecosystem/interfaces/*.md ecosystem/deployment/*.md 2>/dev/null | head -200
# or simply explore the subdirectories
```

## Contents
- `principles/` — Core philosophy, vision, rules we live by (majestic monoliths, async + webhooks + agentic Cromwell, parquet Winston standard, etc.). Update on every material decision.
- `plans/` — Authoritative copies or references to major implementation plans (e.g. this data download service plan). The detailed working copy may live in `.grok/sessions/...` during a session; promote the final version here.
- `interfaces/` — Contracts: Winston EOD parquet standard schema, API shapes between monoliths, Cromwell notification payloads, etc.
- `deployment/` — Podman / compose, env templates, credential placement (EODHD key goes in the documented spot once supplied), volume strategies.
- `hints/` — Growing collection of cues, gotchas, "always do X", references back to WUT mature code, etc.

## Why this folder exists
Long-running multi-monolith project. We refuse to re-explain or hallucinate context every session. This folder (at the top of `~/Documents/com/sawtooth`) survives any single app and is the place the AI (and you) always come back to for hints, cues, and implemented plans.

Start here. Then explore the monoliths (`winston_unit_test/` is the current mature reference for data/portfolio patterns; `winston/` is legacy).

## Current Monoliths (as of plan creation)
1. data_manager (DM) — being built (EODHD → parquet Winston standard + PG metadata + reconciliation + Cromwell status).
2. winston_unit_test (WUT) — backtesting + daily ops (mature data handling, Sidekiq, reuse its Portfolio/Market/Book + services).
3. winston (v1) — legacy, abandon.
4. Cromwell (agentic coordinator) — future (will drive DM triggers and consume status).

All communication: APIs (internal) + Sidekiq (internal) + webhooks (to Cromwell) + file mounts for parquet where beneficial. Podman compose at root.

See principles/ and plans/ for details.
