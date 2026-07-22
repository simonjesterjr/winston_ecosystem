---
id: ISSUE-20260721-cromwell-hourly-verbose-quiet-attention-waste
title: Cromwell hourly market snapshot wastes attention with verbose all-quiet dumps
status: ready
type: bug
priority: high
created: 2026-07-21
updated: 2026-07-21
labels: [cromwell, telegram, market-snapshot, attention]
related:
  - docs/tickets/2026-07-21-cromwell-hourly-telegram-attention-discipline.md
  - docs/tickets/2026-07-09-confirm-cromwell-hourly-telegram.md
  - docs/tickets/2026-07-13-cromwell-scrub-placeholder-path-memory.md
  - docs/tickets/2026-07-13-observe-cromwell-market-snapshot-hourlies.md
  - docs/issues/2026-07-13-cromwell-cron-placeholder-path-hallucination.md
  - principles/01_core_principles.md#12
---

# Cromwell hourly market snapshot wastes attention with verbose all-quiet dumps

**Status:** Ready (product defect — skill already forbids this; agent still does it)  
**Observed:** 2026-07-21 ~10:21 AM local (payload timestamp 2026-07-21 16:17:15 UTC)  
**Channel:** Telegram Sawtooth Main  
**Scope:** Cromwell scheduled `market-snapshot-hourly` message quality (not capital/mutation paths)

## Summary

Hourly market-snapshot posts exist to surface **volatility that needs human eyes**. When all Active symbols are quiet, Cromwell still posts multi-symbol price/ATR tables, invented placeholders, and a numbered “Would you like me to…” menu. That burns the scarcest resource — **human attention** — without actionable content. Principle: *Human attention is the most valuable commodity* (`principles/01_core_principles.md` §12).

## Problem statement

Scheduled radar broadcasts must engage only when markets show testing/breach (or tool failure). All-quiet must be a single all-clear line, not a briefing.

## Current behavior

Example Sawtooth Main post (2026-07-21, last hourly noted ~10:21 local):

- Multi-symbol “Key Metrics Overview” for quiet names (AAAU, AAL, AAPL, …)
- Status “Quiet” repeated per symbol with prices and ATR multiples
- Placeholders such as AAPL ATR `[calculated value]` and missing previous close
- Closing offer menu: highlight symbol / compare history / check anomalies / generate chart

Skill `winston-market-snapshot` already requires: movers list **or** one brief quiet line; **Never Do** includes numbered next-steps menus. Soft skill text is not enough.

## Expected behavior

| Tool result | Telegram |
|-------------|----------|
| `movers` non-empty | Short radar list only (symbol, prev → now, ATR, status) |
| All quiet / empty movers (tool OK) | **One line**, e.g. `All markets quiet.` (or equivalent staid/humorous rotation) |
| Tool failure / no required MCP | One-line **OPS ERROR** only |

No per-quiet-symbol tables. No menus. No placeholders. No “would you like me to…”.

## Reproduction

### Preconditions

- NYSE session MT window; `market-snapshot-hourly` enabled
- Active portfolios with books that resolve quiet (inside 1× ATR)

### Steps

1. Wait for (or force) a natural `market-snapshot-hourly` when `wv2_market_snapshot` returns empty/all-quiet movers.
2. Read Sawtooth Main + cron session / `nanobot_cromwell` logs.

### Observed result

Verbose quiet dump + menu (see Summary). Delivery worked; content failed product intent.

### Reproducibility

At least once on 2026-07-21; treat as always until skill+prompt+runtime make quiet path non-generative.

## Environment

- Cromwell / nanobot; model family as deployed for cron
- Skills: `winston-market-snapshot`, `winston-heartbeat`
- MCP: `wv2_market_snapshot`

## Evidence

| Evidence | Source | What it establishes |
|---|---|---|
| Telegram text ~10:21 local 2026-07-21 | Principal report | Verbose quiet + menu + placeholders |
| Payload time `2026-07-21 16:17:15 UTC` | Same message | Tool-shaped data was available |
| Skill rules 5–6 + Never Do menus | `ecosystem/ai/skills/winston-market-snapshot/SKILL.md` | Intended behavior already documented |

## Impact and priority

| Area | Impact |
|------|--------|
| Attention | High — trains operators to ignore Sawtooth Main |
| Trust | Medium — placeholders look broken even when quiet is true |
| Capital | None direct (read/report only) |

**Priority:** high (P1 ticket) — same cluster as live hourly confirm/observe.

## Scope and preservation requirements

### In scope

- Quiet-path message shape for open + hourly snapshot cron
- Ban menus / offer-lists on scheduled snapshot turns
- Align prompts, cron messages, optional runtime post-check

### Must preserve

- Required successful `wv2_market_snapshot` each run (no invented quiet without tool)
- Mover posts that list real testing/breach symbols
- OPS ERROR on tool failure

### Out of scope

- Changing ATR thresholds or MCP payload schema (unless needed for clearer empty-movers)
- Capital activation / desk confirm flows

## Acceptance criteria

- [ ] Given tool returns no movers, when hourly cron completes, then Telegram is **≤ ~2 short lines** and contains no per-symbol quiet table
- [ ] Given same, then message has **no** numbered menu / “Would you like me to”
- [ ] Given movers present, then only movers are listed (quiet symbols omitted)
- [ ] No invented placeholders (`[calculated value]`, etc.)

## Investigation notes

- Skill already correct; defect is **compliance** (small cron model + prompt pressure).
- Cluster with reliability/memory work: confirm hourlies fire, scrub `path/to/file.txt` memory, observe MCP+clean Telegram (see Related).
- Last noted post ~10:21 local same day — later hourlies may also be missing; track under confirm/observe tickets, not only this copy defect.

## Dependencies and risks

Related cluster (Cromwell hourly Telegram):

1. Confirm natural hourlies after CPU tuning  
2. Scrub placeholder-path permanent memory  
3. Observe real MCP + clean Telegram  
4. **This issue** — attention-respecting quiet path  

## Verification plan

- Natural or forced hourly during session; capture Telegram + logs
- Unit/contract tests if runtime rewrite added for overlong quiet posts
- Skill copy review after seed

## History

- 2026-07-21 — Filed from principal feedback on verbose all-quiet hourly; principle §12 added.
