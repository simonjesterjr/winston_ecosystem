# Jev / TypeSafe desk guardrails (Winston + Grok Bot + Grok CLI)

**Status:** Active process law  
**Date:** 2026-09-24  
**Parent:** [`winston-bot-cli-ai-dlc-contract.md`](winston-bot-cli-ai-dlc-contract.md)  
**External truth:** https://docs.typesafe.ai/llms.txt · https://docs.typesafe.ai/introduction/coding-agents.md  

Mental model stays: **bots act, CLI codes, AI-DLC remembers, Jev judges.**  
Jev is **not** a cheaper coding LLM. It is a System One decision model: state + typed questions → structured answers code (or a harness) can branch on.

## api.typesafe.ai vs `jevctl`

| Layer | What it is | When to use on this desk |
|-------|------------|---------------------------|
| **HTTP API** (`api.typesafe.ai`) | Canonical product: `state` + Choice / Score / Noul → typed answers | In-app Rails/Node/Python code; anything that must be a library call |
| **Official SDKs** (Python / JavaScript) | Typed clients over the same API | Product features inside WUT/Wv2/BG/DM when we add them |
| **`jevctl` (`jev` CLI)** | Opinionated recipes **on top of** the same API: `verify`, `screen`, `classify`, `extract`, `match`, `route`, `ask`, `find`, `rerank`, `compact`, `batch` | Desk agents, overnight Loop, probe gates, autopsy claim checks, transcript shrink |
| **`langchain-typesafe`** | LangChain middleware (router, tool guardrails) | Only if we deliberately build a LangChain agent (not default Winston stack) |
| **Agent skill `typesafe-ai`** | Docs/context so a **coding agent writes correct TypeSafe integrations** | Grok CLI (and bots) when implementing harnesses — **does not auto-call Jev** |

Credentials: `TYPESAFE_API_KEY` (or OpenRouter / Cloudflare providers via `jev --provider`). On sawtooth: `~/.config/jev/typesafe_api_key` + `ecosystem/scripts/jev-desk-helpers.sh`.

**Rule:** Prefer `jev` CLI for bot/CLI desk judgments. Prefer SDK/HTTP when shipping judgments **inside** a monolith. Never invent a second parallel protocol.

## What is implementable (inventory, 2026-09-22)

**On sawtooth today**
- `jevctl@0.2.3` (`jev`) with TypeSafe key wired
- Desk helper: `ecosystem/scripts/jev-desk-helpers.sh` (screen / verify / classify-actionable / doctor)
- Probe-before-promote System One asks (`probe_before_promote.sh`)
- Overnight Loop B screen/verify/classify hooks
- Grok CLI skill copies: `.agents/skills/typesafe-ai`, `.grok/skills/typesafe-ai`

**Not installed (optional later)**
- Python `typesafe` / `langchain-typesafe` SDK
- JS TypeSafe SDK in any monolith
- TypeSafe MCP server (none on desk)
- Claude Code `jev` compact plugin (irrelevant unless we use that harness)

**Not a Jev product**
- Replacing Grok CLI / Grok Bot generative model with `jev-latest` — unsupported and wrong instrument ([coding-agents doc](https://docs.typesafe.ai/introduction/coding-agents.md))

## Division of labour (do not blur)

| Actor | Owns | Does not own |
|-------|------|--------------|
| Generative model (bots / CLI) | Drafts, plans, code, explanations, autopsies | Pretending noul output is a narrative |
| **Jev** | Bounded semantic judgments (route, classify, verify claim, score risk, screen inbound, compact tool noise) | Writing replies, multi-step plans, inventing policy |
| **Code** | Arithmetic, caps, SHA checks, probe peaks, permissions, side effects, thresholds | Soft “does this feel right?” without a typed question |
| **Human** | Ambiguous / high-risk / money / archive-discard | Being asked to parse free-form JSON from an LLM |

## Desk HLD — accepted with bounds

1. **Compress context with `jev compact` when tool-heavy** — drops stale tool calls/results; **keeps text verbatim** (not a summary). Use on long CLI/bot sessions with tool spam. Do **not** compact every short chat turn.
2. **System One harness on plans / tickets / issues that drive implementation** — Lane A: required in the plan. Lane B: required short checklist on the ticket. Trivial typos / pure doc renames: skip.
3. **At each harness checkpoint, adjudicate with Jev** — pass **state** (facts, probe JSON, autopsy excerpt) + atomic questions; branch in code/shell on noul/choice/score + confidence. Deterministic probe checks run **first**; Jev judges residual semantic smells.
4. **CLI seeds must tee System One calls** — every Lane A/B `## CLI seed` tees each `jev ask` (state + questions + answers) into the watchable TUI and the in-band wrap. See [`winston-bot-cli-ai-dlc-contract.md`](winston-bot-cli-ai-dlc-contract.md) § CLI seed — tee Jev System One. Grok thinking ≠ Jev.
5. **`typesafe-ai` skill ≠ auto-Jev** — with `/plan` it only improves how CLI **designs** harnesses and API calls. Someone still must write questions into the ticket/plan and invoke `jev` or the SDK at runtime.

### Forensics / PBR Ops / CoS

May structure evaluations as System One blocks (state blob + noul/choice questions) so analysis has a foundation — then **Jev adjudicates** those blocks. Jev does not replace DuckDB inventory, Edge math, or host probes.

## Anti-oversell (when not to call Jev)

- Exact lookups, arithmetic, git SHA, portfolio caps from `cash_events` (code/probe)
- Desk **law** already in ADR / business-context (do not re-vote policy every night)
- Generative work: session reports, grill prose, code edits
- Low-stakes chatter where a wrong 0.6 noul costs more than a human glance
- Replacing Operator discard approval with a noul

Jev **can be wrong** while still well-typed. Confidence gates belong in **code** (middle band → human / regenerate state), not in vibes.

## Required harness shape (ticket / plan)

```markdown
## System One harness
**State:** (paths or inline facts the judge may see — probe JSON, journal fields, …)
**Checkpoints:**
1. name — Noul|Choice|Score — instructions — pass rule (e.g. noul≥0.85 or choice=X ∧ confidence≥0.7)
2. …
**Runner:** `jev ask …` / desk helper / probe wrapper / SDK
**On fail:** stop · update ticket · do not promote
```

## Migration order (desk)

1. Keep instrumenting existing chokepoints (screen inbound, verify autopsy, probe smells, overnight compact of research claims).
2. Template System One harness into Lane A plans + non-trivial Lane B tickets.
3. Teach Forensics/PBR Ops to emit state+questions, not only prose.
4. In-monolith SDK (Python/JS) — **Operator deferred 2026-09-22**; not worth effort until a critical in-process caller appears. Stay on `jevctl`.

## Commands (sawtooth)

```bash
source ~/.nvm/nvm.sh && nvm use 22
export TYPESAFE_API_KEY="$(cat ~/.config/jev/typesafe_api_key)"   # if unset
./ecosystem/scripts/jev-desk-helpers.sh doctor
jev ask --help
jev compact --help
python3 - <<'PY'
# Prefer official docs for HTTP/SDK shapes — skill typesafe-ai points at docs.typesafe.ai
PY
```
