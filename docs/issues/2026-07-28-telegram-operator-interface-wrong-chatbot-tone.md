---
id: ISSUE-20260728-telegram-operator-interface-wrong-chatbot-tone
title: Telegram treated as generic AI chatbot instead of directed operator control surface
status: in-progress
type: bug
priority: high
created: 2026-07-28
updated: 2026-07-28
labels: [cromwell, telegram, attention, operator-ux, persona, product]
related:
  - docs/issues/2026-07-28-wv2-portfolio-name-resolution-prefers-inactive-and-mutex-recovery-misguide.md
  - docs/issues/2026-07-21-cromwell-hourly-verbose-quiet-attention-waste.md
  - docs/issues/2026-07-20-historical-dar-morning-telegram-leak.md
  - docs/issues/2026-07-13-cromwell-cron-placeholder-path-hallucination.md
  - principles/01_core_principles.md#12
  - ecosystem/ai/personas/cromwell-channels.md
  - ecosystem/ai/personas/cromwell-soul.md
---

# Telegram treated as generic AI chatbot instead of directed operator control surface

**Status banner:** Under investigation / partial fix in tree — persona + always-on heartbeat skill + daily-ops/audit-trail hardened (2026-07-28); needs live channel observe

## Summary

On Sawtooth Main and related Telegram paths, Cromwell often replies as a **generic AI analyst**: essay-style “Key Observations,” portfolio overlap commentary, invented next-step menus, and recovery tutorials after tool errors. That tone **obfuscates real ops defects** (e.g. Active mutex on a dead OP name) and violates the product intent of Telegram as the operator’s **directed, discrete control surface** — hourly radar, focused Daily Activity Report (DAR) summaries, actionable links / short confirmations, evolving into conversational shortcuts for concrete desk actions — not open-ended “what do you notice about this data?” chat.

## Problem statement

Telegram is not a freeform research chatbot interface. Human attention is the scarce resource (`principles/01_core_principles.md` §12). Posts must be **directed and discrete**: what changed, what needs a decision, what to do next (or silence). Generic market-commentary and workshop-style feedback train operators to ignore the channel and hide real failures behind prose.

## Current behavior

### Example A — generic portfolio “analyst” dump (operator report 2026-07-28)

Telegram content shaped like:

- “The data provided appears to represent a collection of stock portfolios (Orange, Rust, Yellow…)”
- “Key Observations” / overlap narratives (RXT, AAPL, NVDA across books)
- Misread position notionals as insight (“NVDA ~$114.67M”, ATR as “strategy clues”)
- “Potential Next Steps” (calculate Sharpe, assess diversification, strategy alignment…)
- Open-ended workshop tone as if Winston asked for feedback on facts

That is the wrong **register** for this channel even if some facts in the dump were true.

### Example B — wrong recovery after real tool error (same day cluster)

After `wv2_perform_daily_analysis` returned `active_mutex` (inactive `#7 Portfolio Blue` vs Active `#381`), Cromwell posted multi-option recovery (force dual-active / deactivate #381) framed as a helpful assistant tutorial — amplifying a bad `force_hint` and further burying “your desk Active Blue is fine; stop naming the closed OP.”

See related: `docs/issues/2026-07-28-wv2-portfolio-name-resolution-prefers-inactive-and-mutex-recovery-misguide.md`.

### Example C — prior attention failures (same product family)

| Issue | Failure class |
|-------|----------------|
| `2026-07-21-cromwell-hourly-verbose-quiet-attention-waste` | Quiet hourlies as tables + menus |
| `2026-07-20-historical-dar-morning-telegram-leak` | Forbidden tools + essay after bad evaluate |
| `2026-07-13-cromwell-cron-placeholder-path-hallucination` | Hallucinated path ask on Sawtooth Main |

Persona already forbids some of this (`cromwell-channels.md`: no “Would you like me to”, no routine inventory tables, no numbered menus on scheduled posts). Soft text is insufficient when the model defaults to chatbot analysis mode.

## Expected behavior

Telegram (especially Sawtooth Main) is an **operator interface of choice** for:

| Mode | Intent | Shape |
|------|--------|--------|
| Hourly market radar | Only what needs eyes | Movers / breaches **or** one-line all-clear; no essay |
| DAR / EOD | Focused operator summarization | Decisions, pending confirms, capital-relevant deltas; links to full report/PDF |
| Discrete actions | Confirm / reject / fill / activate | Short ack with OP id, symbol, units, price, stop — not strategy lectures |
| Error / mutex / tool fail | Unblock the human | One-line OPS ERROR + **one** safe next action (or “no action; desk unchanged”) |
| Evolution (target) | Conversational shortcut for the same discrete acts | e.g. “Blue buying 200 X at $Y stop $Z” → structured confirm path — still not freeform equity research |

**Forbidden register on Sawtooth Main (unless principal explicitly asks for research prose):**

- “Key Observations / Potential Next Steps / Would you like me to…”
- Treating tool JSON or portfolio lists as a case study for diversification commentary
- Invented Sharpe/drawdown homework when no tool computed it
- Multi-option recovery menus that include capital-risky suggestions first

**Allowed:** staid/dry trader voice (`cromwell-soul.md`), short tables only when each row is actionable, deep links or ids that continue a discrete workflow.

## Reproduction

### Preconditions

- Cromwell online on Sawtooth Main; active paper portfolios listed or tool payload available.
- Optional: tool error (`active_mutex`) or list/snapshot payload in session.

### Steps

1. Trigger or observe a turn where Cromwell has portfolio list / position-like data (or a mutex error) and is expected to post to Telegram.
2. Read the human-facing message.

### Observed result

Chatbot-analyst or multi-option tutorial prose instead of directed operator copy.

### Reproducibility

Intermittent by model/session, but **class is systemic** (multiple issues; persona already documents forbidden openings). Treat as always until hard constraints reduce it.

## Environment

- Channel: Telegram Sawtooth Main (and any agent path that mirrors Main tone into ops chat)
- Runtime: `nanobot_cromwell` + persona/skills under `ecosystem/ai/`
- Related MCP tools: list portfolios, market snapshot, perform daily analysis, get DAR
- Date observed: 2026-07-28 (analyst dump + mutex recovery); family since at least 2026-07-13

## Evidence

| Evidence | Source | What it establishes |
|---|---|---|
| Operator-quoted “Key Observations / Potential Next Steps” Telegram | Principal 2026-07-28 | Wrong chatbot tone on portfolio-shaped data |
| Mutex recovery recommending deactivate #381 | Same session / related issue | Error path also uses assistant-tutorial register |
| Channel rules forbidding menus / runtime dumps | `ecosystem/ai/personas/cromwell-channels.md` | Intended product already documented |
| Attention principle | `ecosystem/principles/01_core_principles.md` §12 | Correct-but-noisy is still a product failure |
| Prior issues | hourly quiet; historical DAR; placeholder path | Same failure class recurring |

## Impact and priority

| Area | Impact |
|------|--------|
| Attention | High — trains ignore on Sawtooth Main |
| Incident clarity | High — real defects (name resolution, mutex) hidden under essays |
| Capital | Indirect — recovery menus can suggest deactivate live OP / force dual-Active |
| Trust | Medium–high — looks like generic LLM, not desk coordinator |

**Priority:** high (product defect; principle §12). Not P0 capital mutation by itself.

**Workaround:** Operators ignore prose; act only on tool-backed ids and Wv2 UI/MCP with explicit ids. Prefer not following multi-option “deactivate / force” menus without checking `wv2_list_portfolios`.

## Scope and preservation requirements

### In scope

- Persona / channel / skill hardening for **operator-directed Telegram voice** (scheduled + freeform recovery).
- Structured error reply templates for MCP failures (`active_mutex`, not_found, historical blocked, etc.).
- Alignment of DAR delivery and hourly skills with “discrete + link” not “essay + menu”.
- Optional runtime guards (length, section headers, forbidden phrases) where prior tickets already discuss them.
- Documentation of target conversational shortcuts for desk actions (spec-level; implementation may be phased).

### Must preserve

- Ability to answer explicit research questions when the principal **asks** for analysis prose in 1-1 or clearly scoped thread.
- Dry trader identity (Cromwell), not a different product name.
- Existing hard guards on historical DAR Telegram and quiet-hour rules (do not regress).
- Tool-backed facts only; no invented trades.

### Out of scope

- Fixing Wv2 name resolution / mutex payload (tracked in sibling issue; this issue consumes better error fields when available).
- Broker / capital path redesign.
- Replacing Telegram transport.

## Acceptance criteria

- [ ] Given a portfolio list or snapshot payload on Sawtooth Main without an explicit research ask, Cromwell does **not** post “Key Observations / Potential Next Steps / diversification essay” style content.
- [ ] Given tool error `active_mutex` (or similar), Telegram is ≤ ~5 short lines: what failed, requested vs Active OP ids if present, **one** safe next step (e.g. “use Active #381 or omit name; do not deactivate live seed for desk analysis”).
- [ ] Hourly quiet path remains one-line all-clear (existing issue AC still hold).
- [ ] DAR path remains focused operator summary + report link/PDF — not generic strategy workshop.
- [ ] Persona/skills state the product rule in one place operators and agents share: Telegram = directed discrete ops surface.
- [ ] No regression: explicit “explain diversification of Orange vs Rust” style principal questions may still get longer answers (preferably in 1-1).

## Investigation notes

**Confirmed:**

- Product intent from operator 2026-07-28: directed activities, DAR summarization, links, evolve to conversational fills — not chatbot feedback on facts.
- Soft persona rules already ban many menus; analyst-essay mode is a gap not fully covered by “no Would you like me to”.
- Mutex incident shows **error paths** need the same discipline as cron hourlies.

**Hypotheses:**

- Small/local models default to “summarize the JSON as a briefing” when skills don’t supply a rigid template for freeform turns.
- Long tool JSON in context triggers generic analysis completion rather than ops shell formatting.
- Recovery after truncation (historical pattern) increases essay/menu likelihood.

## Unknowns and clarifying questions

- [ ] Whether freeform John 1-1 should stay slightly more conversational than Sawtooth Main (safe default: same discrete bias; longer only when asked).
- [ ] Priority order of hardening: skill templates vs runtime phrase/length guards vs better MCP error schemas (recommend all three, MCP error first for mutex class).

## Dependencies and risks

- Sibling issue on name resolution + `force_hint` — better structured errors make short OPS replies easier.
- Existing ticket cluster on hourly attention discipline.
- Over-constraining replies must not block legitimate confirm-entry conversational shortcuts once that path ships.

## Verification plan

1. Golden-message fixtures or skill evals: portfolio list → allowed shapes; mutex error → OPS one-pager; quiet snapshot → one line.
2. Live observe Sawtooth Main after persona/skill deploy (compare to 2026-07-21/28 failures).
3. Adversarial prompt: paste portfolio JSON into Telegram; require non-essay response.
4. Cross-check no regression on EOD DAR delivery skill.

## History

- 2026-07-28 — Created from operator report of chatbot-toned Telegram dump + same-day mutex recovery misguidance; linked prior attention/Telegram issues and principle §12.
- 2026-07-28 — Hardened `cromwell-channels.md`, `cromwell-agents.md`, `winston-heartbeat` (always-on), `winston-daily-ops`, `winston-portfolio-lifecycle`, `winston-audit-trail`; seeded workspace v1.5.2; restarted `nanobot_cromwell`. Soft-text fix only — runtime length/phrase guards still optional follow-up.
