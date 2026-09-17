# Ticket: Cromwell daily STATE + stop/skip + verifier skill (8b)

**Status:** In progress  
**Date:** 2026-09-17  
**Priority:** P1  
**Origin:** Post-CUDA inventory close-out; companion analysis `docs/analysis/2026-09-17-cromwell-cuda-priority-revisit.md` next desk move. Spawns loop-engineering **L1**.

## Problem

Cromwell’s daily loop (cron + skills + MCP) can *narrate* a Daily Analysis Report (DAR) and still “succeed” on a partial day: missing DAR, stale coverage, or a pending list that is never checker-reviewed. Loop-engineering 1A/1B asked for:

1. Bounded per-day **STATE** so the loop does not re-litigate from zero.
2. Checkable **stop/skip** (not trading day / DAR missing / MCP error).
3. A **verifier** skill, separate from the EOD narrator, that grades pending drafts `TAKE | SIZE_DOWN | SKIP | HOLD` — human remains the fill gate.

GPU 8b (`cromwell-qwen3:8b`) makes this cheap enough to run on the existing 16:35 EOD turn. No new model, no Rails `LlmClient`, no Evolution Mode.

## Scope

1. `STATE-YYYY-MM-DD.md` template + write path `workspace/state/` (runtime; not git).
2. Skill `winston-daily-loop` — stop/skip + STATE write from MCP facts only.
3. Skill `winston-decision-verifier` — advisory verdicts only; **never** `wv2_confirm_journal`.
4. Wire into existing `eod-daily-report` (not a second Telegram ping). Path-restricted `write_file` via cron allowlist patch (`write_allow: state/`).
5. Interactive triggers: “daily state”, “verify pending”.

## Non-goals

- Auto-confirm / paper autofill (umbrella V1)
- In-Rails journal `notes_draft` / RAG
- Lesson write-back (loop 1C)
- Dual-route 3b cron
- File-only cron (nanobot unbound patch)
- Changing the live 8b pin

## Acceptance

- [x] Template + two skills in `ecosystem/ai/skills/` (seeded, `ecosystem/ai` VERSION 1.6.0)
- [x] EOD cron message + allowlist: fetch_only DAR required; STATE write only under `state/`; **`force_omit: date`**
- [x] Verifier cannot confirm; confirmation-loop still requires human authorize
- [x] Patch tests for `read_allow` / `write_allow` / `force_omit` (21 passed)
- [x] Seed + nanobot rebuild (patch) + nanobot recreate
- [x] INDEX + umbrella L1 pointer
- [ ] First **Cromwell-written** `state/STATE-YYYY-MM-DD.md` on a scheduled EOD (2026-09-17 EOD hallucinated `date=2023-10-15` → OPS ERROR; bootstrap file written by hand)

## 2026-09-17 ship notes

- Do **not** `compose --force-recreate nanobot_cromwell` — podman-compose cascades and stops redis/Wv2/Ollama. Recreate nanobot only after an accidental cascade recovered.
- EOD 16:35 MT posted OPS ERROR (required MCP never succeeded). Session: `cron_eod-daily-report.jsonl`.
- Bootstrap STATE: `ai/data/cromwell-bot/workspace/state/STATE-2026-09-17.md` (15 pending; verifier not_run).

## Related

- Plan: [`../../plans/loop-engineering-and-evolution-mode.md`](../../plans/loop-engineering-and-evolution-mode.md) §1A–1B
- Umbrella: [`2026-07-19-loop-engineering-evolution-mode.md`](2026-07-19-loop-engineering-evolution-mode.md)
- Priority: [`../analysis/2026-09-17-cromwell-cuda-priority-revisit.md`](../analysis/2026-09-17-cromwell-cuda-priority-revisit.md)
- Inventory: [`archive/2026-09-17-winston-llm-desk-inventory.md`](archive/2026-09-17-winston-llm-desk-inventory.md)
- Confirm skill: [`../../ai/skills/winston-confirmation-loop/SKILL.md`](../../ai/skills/winston-confirmation-loop/SKILL.md)
- Pin: [`../../ai/MODEL_PIN.md`](../../ai/MODEL_PIN.md)
