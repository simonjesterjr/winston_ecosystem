# Issue: Cromwell cron posts placeholder-path hallucination to Sawtooth Main

**Status:** Open  
**Observed:** 2026-07-13 ~09:12 MDT  
**Channel:** Telegram Sawtooth Main (`chat_id=-1003884714483`)  
**Runtime:** `nanobot_cromwell` / model `cromwell-qwen2.5:3b`  
**Scope:** Cromwell agent quality (cron + memory), not monolith trading paths

## Symptom

At **9:12 AM MDT**, Sawtooth Main received:

> It seems that the file path/to/file.txt was not found. Could you please provide the correct file path so I can attempt reading the file again?

Error delivery worked (message reached Telegram). Content was spurious — no real ops file was missing.

## Root cause

**Agent loop quality after output truncation**, not a filesystem defect.

Verified timeline from `podman logs nanobot_cromwell` and session JSONL (UTC = MDT+6):

| UTC | MDT | Event |
|-----|-----|--------|
| 15:00 | 09:00 | Cron `market-snapshot-hourly` starts |
| 15:01 | 09:01 | `mcp_winston_wv2_market_snapshot({})` succeeds |
| 15:02 | 09:02 | `Output truncated on turn 1 for telegram:-1003884714483 (1/3); continuing` |
| 15:03–15:11 | 09:03–09:11 | **8×** `read_file({"path": "path/to/file.txt"})` — docs-style placeholder, not a real path |
| **15:12** | **09:12** | Assistant posts the Telegram ask-for-path message; cron marked completed |
| 15:12–15:14 | 09:12–09:14 | System `dream` job runs; also fails on wrong paths (`MEMORY.md` root vs `memory/MEMORY.md`; invents `ECOSYSTEM_STATUS.md`) |
| 15:28 | 09:28 | Idle compact archives the failure into permanent memory |

Primary evidence:

- Session: `ai/data/cromwell-bot/workspace/sessions/telegram_-1003884714483.jsonl` (user turn `Output limit reached. Continue…` → placeholder `read_file` loop)
- Memory poison: `ai/data/cromwell-bot/workspace/memory/history.jsonl` cursor 61  
  (`Error: File not found: path/to/file.txt - Tried different approaches but file not found.`)
- Dream session: `ai/data/cromwell-bot/workspace/sessions/dream_20260713-151240.jsonl`

### Stacked failure modes

1. **Primary:** Small cron model abandons snapshot formatting after truncation and hallucinates a textbook path instead of summarizing the MCP payload or stopping.
2. **Trigger:** Mid-turn output truncation recovery is brittle.
3. **Secondary (same morning):** Dream mis-routes `memory/MEMORY.md` → bare `MEMORY.md`; invents skill status file.
4. **Follow-on smell (same day):** 10:00 and 11:00 MT hourly jobs posted “no movers / stable” **with no `wv2_market_snapshot` tool call** (hallucinated completion). Separate from the placeholder path, same quality class.

## What is *not* broken

- Telegram transport / Bot API delivery
- MCP `wv2_market_snapshot` at 09:00 (tool returned; problem is agent recovery)
- Capital / portfolio mutation paths (read/report only)

## Impact

| Area | Impact |
|------|--------|
| Ops noise | Spurious human-facing message on Sawtooth Main |
| Missed duty | 09:00 hourly snapshot never produced a real ATR/mover line; job still “completed” |
| Memory | Nonsense permanent fact in `history.jsonl` |
| Trust | Cron “completed” does not mean required MCP tools ran |

No trading/capital risk from this incident.

## Suggested remediation (tickets filed 2026-07-13)

1. **Memory scrub** — [`docs/tickets/2026-07-13-cromwell-scrub-placeholder-path-memory.md`](../tickets/2026-07-13-cromwell-scrub-placeholder-path-memory.md)
2. **Cron hardening** (circuit-break, require MCP, no path-asks) — [`docs/tickets/2026-07-13-cromwell-cron-hallucination-hardening.md`](../tickets/2026-07-13-cromwell-cron-hallucination-hardening.md)
3. **Dream path hygiene** — [`docs/tickets/2026-07-13-cromwell-dream-memory-path-hygiene.md`](../tickets/2026-07-13-cromwell-dream-memory-path-hygiene.md)
4. **Observe hourlies** — [`docs/tickets/2026-07-13-observe-cromwell-market-snapshot-hourlies.md`](../tickets/2026-07-13-observe-cromwell-market-snapshot-hourlies.md)
5. **Align Jul 9 timeout acceptance** — [`docs/tickets/2026-07-13-extend-cron-llm-timeout-acceptance.md`](../tickets/2026-07-13-extend-cron-llm-timeout-acceptance.md)

May share mitigations with model/ctx work already tracked for cron timeouts (see Related).

## Related

- Ticket (open quality work): [`docs/tickets/2026-07-09-cromwell-cron-llm-timeout.md`](../tickets/2026-07-09-cromwell-cron-llm-timeout.md)
- Ticket (CPU model choice): [`docs/tickets/2026-07-09-cromwell-cpu-only-llm-tuning.md`](../tickets/2026-07-09-cromwell-cpu-only-llm-tuning.md)
- Session (this investigation): [`docs/session-reports/2026-07-13-1216-cromwell-telegram-placeholder-path.md`](../session-reports/2026-07-13-1216-cromwell-telegram-placeholder-path.md)
- Session (cron binding fix): [`docs/session-reports/2026-07-09-0736-cromwell-cron-telegram-fix.md`](../session-reports/2026-07-09-0736-cromwell-cron-telegram-fix.md)
- Schedule notes: `ecosystem/ai/schedule/README.md`
- Persona / truncation note: `ecosystem/ai/personas/cromwell-tools.md` (10k char output truncate)

## Evidence paths (runtime; not in ecosystem git)

```
ai/data/cromwell-bot/workspace/sessions/telegram_-1003884714483.jsonl
ai/data/cromwell-bot/workspace/sessions/dream_20260713-151240.jsonl
ai/data/cromwell-bot/workspace/memory/history.jsonl  # cursor 61
podman logs nanobot_cromwell  # 2026-07-13T15:00–15:28 UTC
```
