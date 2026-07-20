# Ticket: Cromwell transfer reply contract (skill + persona)

**Status:** **Done** (2026-07-16) — live Telegram handoff quality accepted (action + `#id` + fingerprint; no ops menus)  
**Date:** 2026-07-15  
**Priority:** High — **A** (closed)  
**Source:** Session `2026-07-15-1404-telegram-transfer-agent-gap.md`  
**Plan / context:** Paper Telegram ops; ADR-006 handoff via MCP  
**AI version:** `ecosystem/ai/VERSION` → `1.4.5`

## Problem

Telegram transfer of WUT run 57 **succeeded** (`wv2_transfer_portfolio_from_wut` → `legacy_updated` OP `#157`), but Cromwell’s user-facing reply ignored the transfer result and wrote a generic portfolio briefing with activate/sync/report **menus**. Operator concluded “it failed.”

Root cause: agent report-writing after tools return, not missing import machinery.

## Scope (A)

1. Harden `ecosystem/ai/skills/winston-wut-to-wv2/SKILL.md` (and seeded workspace copy via `bin/seed-cromwell-workspace` when ready):
   - After transfer, **lead** with: `status`, `action`, `portfolio.id`, `name`, `active`, `execution_mode`, top `warnings`.
   - Map actions to plain English: `created` / `legacy_updated` / `forked` / `adopted` / `engaged_refuse` / `closed_refuse`.
   - One line: sole Active OP if unchanged.
   - **Forbidden** unless user asked: activate, sync, daily report, menus, “would you like to proceed.”
2. Persona / tools guidance (`cromwell-tools.md`, `cromwell-channels.md`, workspace `TOOLS.md` / `AGENTS.md` as needed):
   - After any **mutating** MCP tool, lead with that tool’s result; never only summarize a subsequent list dump.
3. Optional MEMORY / few-shot line: “transfer run N → report #id action=…”.
4. Re-seed Cromwell workspace and smoke one Telegram transfer reply quality check.

## Acceptance

- [x] Skill documents mandatory success template and forbidden follow-ups  
- [x] Channel rules restate: no menus on handoff confirmation  
- [x] MCP emits paste-ready `reply_text` with action + `#id` on line 1 (2026-07-16)  
- [x] Live Telegram transfer / activate reports `action` + `#id` (operator accepted 2026-07-16; activate `#11` Rust · dd7e7c7a explicit PASS)  
- [x] No unsolicited activate/sync/report menus after handoff (operator accepted)  
- Residual (non-blocking): occasional preamble/footer around `reply_text` — 1.4.5 bans; polish-only

## Live smoke (2026-07-15 ~15:13–15:25 MT) — FAIL quality

| Step | Result |
|------|--------|
| Transfer run 57 | MCP **ok** `legacy_updated` `#157` (tool JSON had full portfolio block) |
| User-facing reply | **FAIL** — long briefing + activate/sync/daily-analysis **menu** |
| “activate the portfolio” | **FAIL** — asked for id despite `#157` in prior bot message |
| “activate portfolio 157” | MCP activate **ok** in 40ms; agent then chained `get_portfolio_status`; multi-minute silence (CPU 8b + Flood Control risk) |
| Ground truth | `#157` **active=true**; also Active: `#12` Portfolio Blue · PBR62 |

## Live smoke (2026-07-16 operator) — CLOSER, still miss `action`+`#id`

| Step | Result |
|------|--------|
| Transfer (Orange / run 41 path) | Machinery **ok** (fingerprinted OP; paper_caps warning surfaced) |
| User-facing reply | **Partial** — on-point, no ops menu; **missing** import `action` and OP `#id`; still markets inventory + soft “Would you like to check status/tasks/snapshots?” |
| Activate follow-up | **Good enough** — “Portfolio Orange (ID 6)…”, short fingerprint, correlation id; mild soft closer |

## Live smoke (2026-07-16 post-`reply_text`) — ACTIVATE PASS core

| Step | Result |
|------|--------|
| Activate `#11` Portfolio Rust · dd7e7c7a | **PASS core** — body includes exact template: `Activated #11 "…" · dd7e7c7a — action=activated` / `active=true` |
| Residual | Preamble (“successfully activated… Here’s the confirmation”) + meta footer (“This is the complete response. No further actions or tool calls…”) — model narrating `reply_hint` instead of pasting only `reply_text` |
| Transfer | _operator: confirm separately if not already_ |

**Root cause refinement:** Skills are **not auto-injected** — 8b must `read_file` them and usually does not. Always-on `AGENTS.md` HARD RULES + MCP **`reply_text`** (verbatim paste) + `summary` are required; skill alone is insufficient. Model rewrites from `portfolio.markets` / `capital_base` even when outcome is understood. Residual after `reply_text`: **wrapper prose** around a correct body, plus leaking internal “complete response / no tool calls” instructions into chat.

## Implementation notes (2026-07-15)

| Artifact | Change |
|----------|--------|
| `ecosystem/ai/skills/winston-wut-to-wv2/SKILL.md` | Mandatory success template; action map; no auto-chain activate/sync/report |
| `ecosystem/ai/personas/cromwell-tools.md` | Mutating-tool lead-with-result rule |
| `ecosystem/ai/personas/cromwell-channels.md` | Handoff: no menus |
| `ecosystem/ai/personas/cromwell-agents.md` | HARD RULES block (1.4.2); removed transfer→activate chain default |
| `ecosystem/ai/skills/winston-portfolio-lifecycle/SKILL.md` | Activate playbook: resolve “the portfolio”; no re-ask; no post-activate menus |
| `ecosystem/ai/skills/winston-wut-portfolio-lifecycle/SKILL.md` | Transfer stops at reply contract |
| `ecosystem/ai/memory/templates/MEMORY.template.md` | Few-shot handoff line |
| `ecosystem/interfaces/winston-mcp-tools.md` | Transfer notes + `summary` field |
| `ai/mcp_winston/.../server.py` (host) | `_attach_agent_summary` for transfer/activate/deactivate |
| `bin/seed-cromwell-workspace` | Re-run after docs land |

## Implementation notes (2026-07-16 second pass)

| Artifact | Change |
|----------|--------|
| `ai/mcp_winston/.../server.py` | `reply_text` multi-line paste contract; plain-English action labels; short fingerprint; stronger `reply_hint` forbidding markets inventory + soft status menus |
| Transfer tool description | Mentions paste `reply_text` (action + #id) |
| `cromwell-agents.md` HARD RULES | Paste `reply_text`; forbidden rewrite patterns from 07-16 smoke |
| `cromwell-channels.md` / `cromwell-tools.md` | Verbatim paste; soft-offer ban |
| `winston-wut-to-wv2` + activate skill | Priority: reply_text → summary → fields; anti-patterns |
| Wv2 activate/deactivate JSON | Include `fingerprint`, `execution_mode`, `seed_name` for agent |
| AI VERSION | `1.4.4` |
| AI VERSION + wrapper bans | `1.4.5` — no preamble/postscript; ban “Here’s the confirmation” / “complete response” / “no further tool calls” in user text |

## Related

- Skill: `ecosystem/ai/skills/winston-wut-to-wv2/SKILL.md`  
- Tickets B/C (export fidelity, MCP summary / reply_text) reduce model confusion  
- Session report: transfer ok, reply bad  

## Non-goals

- New import endpoints  
- Auto-activate on import  
- Model swap alone as the “fix”  

