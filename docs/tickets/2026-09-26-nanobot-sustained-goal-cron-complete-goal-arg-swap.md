# Ticket: Harden nanobot sustained-goal / cron against complete_goal arg swap loop

**Status:** Proposed  
**Priority:** P2  
**Date:** 2026-09-26  
**Lane:** B  
**Implementer:** Winston Dev (Operator assigned)  
**DoD:** Cron sessions no longer re-inject sustained-goal after a `complete_goal` schema miss; Definition of Done (DoD) checks below green on next `ecosystem-status-daily`.  
**Origin:** Operator / Chief of Staff (CoS) triage after Telegram tool-error spam on `cron:ecosystem-status-daily` (2026-09-26). Ops AI profile restart + cleared `goal_state` stopped spam temporarily.  
**Evidence:** [`../analysis/2026-09-26-nanobot-ai-stack-reboot.md`](../analysis/2026-09-26-nanobot-ai-stack-reboot.md); [`../analysis/2026-09-26-nanobot-complete-goal-pre-restart.log`](../analysis/2026-09-26-nanobot-complete-goal-pre-restart.log); [`../analysis/2026-09-26-nanobot-post-restart.log`](../analysis/2026-09-26-nanobot-post-restart.log); session `cron_ecosystem-status-daily.jsonl`; backups under `sessions/_triage_backups_20260926/`  
**Related (out of scope):** [`2026-09-08-wev-pulse-other-monolith-emits.md`](2026-09-08-wev-pulse-other-monolith-emits.md) — do not expand into Winston Ecosystem View (WEV) Pulse / DAR emit work  
**Contract:** [`../business-context/winston-bot-cli-ai-dlc-contract.md`](../business-context/winston-bot-cli-ai-dlc-contract.md)

## Goal

Stop the model from getting stuck in a sustained-goal / cron loop where it calls `complete_goal({goal, ui_summary})` (that schema belongs to `long_task`) and the injector keeps re-prompting while `goal_state.active` stays set on `cron:ecosystem-status-daily`. After this ticket, cron duties finish without Telegram tool-error spam and without sustained-goal injections on that session.

## Context / specimens

**Root smell (triage):**

- Spam was the model calling `complete_goal({goal, ui_summary})` — that schema is **`long_task`**; real `complete_goal` is **optional recap only**.
- Error: `Invalid parameters for tool 'complete_goal': unexpected parameter goal`
- Sustained-goal injector re-prompts while `goal_state.active`; stuck on `cron:ecosystem-status-daily`
- Ops AI profile restart + cleared `goal_state` stopped spam temporarily (not a durable fix)

**Sample from pre-restart log:**

```
Tool call: complete_goal({"goal": "Continue the previous task by breaking it into smaller steps and proceeding without recap.", "ui_summary": "Resuming interrupted task"})
Tool call: long_task({"goal": "Analyze the error and provide a corrected approach", "ui_summary": "Resolve invalid parameters for complete_goal"})
```

**Code / patch surfaces (image + desk):**

| Surface | Path |
|---------|------|
| Image tools | `nanobot/agent/tools/long_task.py`, `registry.py`, `runner.py` (inside `nanobot_cromwell` image) |
| Desk patches | `ecosystem/ai/nanobot/patches/` (incl. existing `cron_tool_allowlist.py` identical-fail circuit-break — extend / mirror for this smell) |
| Cron allowlist config | `ecosystem/ai/schedule/cron-tool-allowlist.json` |

## Work items

- [ ] **Cron policy:** deny or auto-noop `long_task` / `complete_goal` on `sessionKey` matching `cron:*` **or** clear `goal_state` at end of every cron turn (pick one durable policy; document in patch README / allowlist comment)
- [ ] **Validation User Experience (UX):** unexpected `goal` / `ui_summary` on `complete_goal` → one-shot hint pointing the model to `long_task` (do not loop the same Invalid parameters forever)
- [ ] **Circuit-break:** after **N** identical `Invalid parameters for complete_goal` failures (same tool + same unexpected-arg shape), hard-stop with ops guidance (reuse / extend desk identical-fail pattern in `cron_tool_allowlist.py`)
- [ ] **Optional HARD RULE** in seeded `AGENTS.md` / `TOOLS.md` — **ticket this text only; do not edit live persona files in this ticket**
- [ ] **Verify:** next `ecosystem-status-daily` completes without sustained-goal injections / Telegram tool-error spam
- [ ] In-band wrap + push `ecosystem` `main` (and image/vendor change if the fix lands outside desk patches — note path in Results)

## System One harness

Required for this Lane B hotfix.  
Law: [`../business-context/jev-desk-guardrails.md`](../business-context/jev-desk-guardrails.md).

**State:** triage analysis + pre/post logs above; live `goal_state` for Ops AI / Cromwell; next `cron:ecosystem-status-daily` session transcript; Telegram channel for tool-error spam absence; patch/diff under `ecosystem/ai/nanobot/patches/` (and image paths if touched).

**Checkpoints:**

| id | type | instructions | pass rule |
|----|------|--------------|-----------|
| cron_no_sustained_inject | Noul | After fix, a `cron:ecosystem-status-daily` turn shows no sustained-goal continuation inject while the duty is a normal cron status job | noul ≥ 0.85 |
| complete_goal_arg_hint | Noul | Unexpected `goal`/`ui_summary` on `complete_goal` yields a one-shot hint to `long_task`, not an infinite Invalid-parameters loop | noul ≥ 0.85 |
| circuit_break_fires | Noul | N identical Invalid parameters for `complete_goal` hard-stops with ops guidance (no death spiral) | noul ≥ 0.85 |
| daily_cron_clean | Noul | Next `ecosystem-status-daily` completes without Telegram tool-error spam for this smell | noul ≥ 0.85 |
| no_live_persona_edit | Noul | Did this work edit live seeded AGENTS.md/TOOLS.md persona files? | noul ≥ 0.85 → **FAIL** (ticket-only HARD RULE text is OK) |
| scope_pulse_untouched | Noul | Did this work expand into WEV Pulse / `2026-09-08-wev-pulse-other-monolith-emits`? | noul ≥ 0.85 → **FAIL** |

**Runner:** deterministic log/session/`goal_state` probes first; `jev ask` / `./ecosystem/scripts/jev-desk-helpers.sh` / prefer `jevctl` on residual semantic smells.  
**Order:** deterministic code/probe first; Jev on residual.  
**On fail:** stop · update ticket · do not claim Done · do not edit live persona.

## CLI seed

```
cwd: /home/johnkoisch/Documents/com/sawtooth/ecosystem
Lane B hotfix. Implementer = Winston Dev (Operator assigned). Not a parallel Grok CLI ticket unless Operator splits scope in writing.

Problem: model calls complete_goal({goal, ui_summary}) — that schema is long_task; real complete_goal is optional recap only.
Error: Invalid parameters for tool 'complete_goal': unexpected parameter goal
Sustained-goal injector re-prompts while goal_state.active; stuck on cron:ecosystem-status-daily.
Ops AI restart + cleared goal_state stopped spam temporarily only.

Follow ticket docs/tickets/2026-09-26-nanobot-sustained-goal-cron-complete-goal-arg-swap.md
Evidence: docs/analysis/2026-09-26-nanobot-ai-stack-reboot.md + pre/post logs.

Do (ticket DoD only — do not implement beyond this ticket):
1. Cron policy: deny or auto-noop long_task/complete_goal on sessionKey cron:* (or clear goal_state end of every cron turn).
2. Validation UX: unexpected goal/ui_summary on complete_goal → one-shot hint pointing to long_task.
3. Circuit-break: N identical Invalid parameters for complete_goal (extend desk cron_tool_allowlist identical-fail if natural).
4. Optional HARD RULE text for seeded AGENTS.md/TOOLS.md — ticket only; do NOT edit live persona.
5. Verify next ecosystem-status-daily completes without sustained-goal injections / Telegram tool-error spam.

Surfaces: image nanobot/agent/tools/long_task.py, registry.py, runner.py; desk ecosystem/ai/nanobot/patches/.
Out of scope: 2026-09-08-wev-pulse-other-monolith-emits.

System One harness on the ticket. Tee every jev ask (state + questions + answers) into TUI + wrap.
Push ecosystem main. In-band wrap. No PR theater.
```

### CLI seed — tee Jev System One (default)

At every System One checkpoint in this ticket:

1. Print a clear Terminal User Interface (TUI) banner: `=== Jev System One ===`
2. Print the **state** blob (facts / probe JSON / autopsy excerpt) verbatim.
3. Print each question (Noul / Choice / Score) before calling `jev`.
4. Run `jev ask` (desk: `jevctl` / `ecosystem/scripts/jev-desk-helpers.sh`); do not silently skip when `TYPESAFE_API_KEY` is set.
5. Print the JSON answers (and confidence) in the TUI; append the same block to the in-band wrap / ticket Results.
6. Branch fail-closed on harness pass rules. Deterministic probes run first; Jev judges residual semantic smells only.

If Jev is unavailable, print `Jev skipped: <reason>` and continue only if the ticket allows probe-only; never pretend Jev passed. Prefer `jevctl` over the TypeSafe Python Software Development Kit (SDK).

## Shared watchable session (Operator)

Preferred desk pattern ([`../business-context/winston-bot-cli-ai-dlc-contract.md`](../business-context/winston-bot-cli-ai-dlc-contract.md)): Operator opens a **visible** terminal on **sawtooth-ai** and starts the Winston Dev / Grok session with the seed as the initial prompt. CoS follows that session; do not start a second implementer on this ticket.

```bash
cd /home/johnkoisch/Documents/com/sawtooth/ecosystem
SEED=$(sed -n '/^## CLI seed$/,/^## /p' \
  /home/johnkoisch/Documents/com/sawtooth/ecosystem/docs/tickets/2026-09-26-nanobot-sustained-goal-cron-complete-goal-arg-swap.md \
  | sed '1d;$d' | sed '/^```/d')
# Winston Dev Lane B: paste SEED into the assigned Dev session, or:
# grok --fullscreen "$SEED"
```

Fallback (paste-only): `cd` same cwd → paste the ``` CLI seed ``` block once into the Winston Dev session.

## Non-goals

- Implementing / shipping WEV Pulse emits from [`2026-09-08-wev-pulse-other-monolith-emits.md`](2026-09-08-wev-pulse-other-monolith-emits.md)
- Live persona edits to seeded `AGENTS.md` / `TOOLS.md` (HARD RULE text may be drafted in ticket Results only)
- Changing compose recreate cascade ([`2026-09-17-compose-nanobot-recreate-cascade.md`](2026-09-17-compose-nanobot-recreate-cascade.md))
- Dual-route Cromwell cron model routing ([`2026-09-17-cromwell-cron-dual-route-3b.md`](2026-09-17-cromwell-cron-dual-route-3b.md))
- Parallel Grok CLI implement on this ticket unless Operator splits scope in writing
