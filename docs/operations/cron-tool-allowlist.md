# Cromwell cron tool allowlist

## When

Morning/hourly crons call off-duty MCP tools (e.g. historical daily analysis), or Telegram receives non-EOD DARs / recovery noise from cron sessions.

## SOT

| Piece | Path |
|-------|------|
| Allowlist config | `ecosystem/ai/schedule/cron-tool-allowlist.json` |
| Seed into workspace | `bin/seed-cromwell-workspace` → bot workspace `schedule/` |
| Runtime enforce | nanobot patch under `ecosystem/ai/nanobot/patches/cron_tool_allowlist.py` (image must include patch) |
| Docs | `ecosystem/ai/schedule/README.md` |

Prompt-level FORBIDDEN is **not** sufficient alone.

## Change procedure

1. Edit `cron-tool-allowlist.json` (per session_key / cron id → allowed tools only).
2. `bin/seed-cromwell-workspace`
3. Rebuild/restart nanobot/cromwell if the Python patch or image changed.
4. Smoke: under a cron session key, `prepare_call` for a forbidden tool must fail closed; allowed tool still works.
5. Do not test by blasting Sawtooth Main with historical DARs.

## Related issues

- `docs/issues/2026-07-20-historical-dar-morning-telegram-leak.md`
- `docs/issues/2026-07-13-cromwell-cron-placeholder-path-hallucination.md`

## Related skills

`ship-to-test`, Cromwell skills under `ai/skills/`, `lightweight-bug-fix` for regressions.
