# Nanobot Cromwell AI stack reboot — 2026-09-26

**Host:** sawtooth-ai  
**Actor:** Sawtooth Ops  
**Ask:** Operator via Chief of Staff — stop Telegram spam from undefined/misused `complete_goal`; reboot AI stack; confirm health; capture log evidence.

## Restarted (compose `--profile ai`)

| Container | Result |
|-----------|--------|
| `ollama` | restarted; **healthy**; `ollama list` OK |
| `winston_mcp` | restarted; up (host port not published; internal-only) |
| `nanobot_cromwell` | restarted; **health HTTP 200** `{"status":"ok"}` on `127.0.0.1:18790/health` |

Not restarted: `open-webui` (left running; not required for Cromwell Telegram path). No separate `llama-server` service on this host.

Restart wall time: ~08:50 MT (2026-09-26).

## Log evidence (pre-restart)

Heavy loop of `Tool call: complete_goal(...)` alternating with `long_task(...)` and `Injected sustained-goal continuation after final response`, roughly 14:03–14:49 UTC on 2026-09-26. Sample:

```
Tool call: complete_goal({"goal": "Continue the previous task by breaking it into smaller steps and proceeding without recap.", "ui_summary": "Resuming interrupted task"})
Tool call: long_task({"goal": "Analyze the error and provide a corrected approach", "ui_summary": "Resolve invalid parameters for complete_goal"})
```

Also: `Empty response on turn 118 for cron:ecosystem-status-daily`; tool hallucination `my({"action":"check","key":"goal"})`.

Artifact: `ecosystem/docs/analysis/2026-09-26-nanobot-complete-goal-pre-restart.log`

## Post-restart note

On boot nanobot logged:

```
Registered 19 tools: [..., 'complete_goal', ..., 'long_task', ...]
```

So in this build `complete_goal` is **registered alongside** `long_task` (not absent from the schema). Operator/CoS triage said correct tool is `long_task` (goal + optional ui_summary); the spam was misuse / loop, not necessarily a missing registration. Restart cleared the hot loop; brief LLM connection errors during ollama bounce then Agent loop started clean.

## DoD probe

- `curl http://127.0.0.1:18790/health` → 200 `{"status":"ok"}`
- `ollama` healthy + model list present (`cromwell-qwen2.5:3b`, etc.)
