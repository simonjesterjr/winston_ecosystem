# Cromwell cron tool allowlist + duty guards

## When

Morning/hourly crons call off-duty MCP tools (e.g. historical daily analysis), invent “stable market” without MCP, loop on `read_file(path/to/file.txt)` after truncation, or Telegram receives path-asks / recovery noise from cron sessions.

## SOT

| Piece | Path |
|-------|------|
| Allowlist + duty config | `ecosystem/ai/schedule/cron-tool-allowlist.json` |
| Seed into workspace | `bin/seed-cromwell-workspace` → bot workspace `schedule/` |
| Runtime enforce | nanobot patch under `ecosystem/ai/nanobot/patches/cron_tool_allowlist.py` (image must include patch) |
| Docs | `ecosystem/ai/schedule/README.md` |

Prompt-level FORBIDDEN is **not** sufficient alone.

### Config keys (per job)

| Key | Purpose |
|-----|---------|
| `mcp_allow` | Allowed MCP logical names |
| `mcp_require` | Must succeed once this turn or final text → OPS ERROR |
| `builtin_deny` | Hard-deny builtins (`read_file`, …) |
| `force_args` | Forced tool args (e.g. `fetch_only: true`) |
| `identical_fail_limit` | Circuit-break after N identical failures (default 2) |

## Change procedure

1. Edit `cron-tool-allowlist.json` (per `cron:<job-id>` → allow/require/deny).
2. `bin/seed-cromwell-workspace` (and `--force-cron` if job prompt text changed).
3. Rebuild/restart nanobot/cromwell if the Python patch or image changed.
4. Unit tests: `pytest ecosystem/ai/nanobot/patches/test_cron_tool_allowlist.py`.
5. Smoke: under a cron session key, `prepare_call` for a forbidden tool must fail closed; allowed tool still works; finishing without `mcp_require` should surface OPS ERROR text.
6. Live hourlies: follow observe ticket (do not invent Telegram success offline).
7. Do not test by blasting Sawtooth Main with historical DARs.

## Related issues

- `docs/issues/2026-07-20-historical-dar-morning-telegram-leak.md`
- `docs/issues/2026-07-13-cromwell-cron-placeholder-path-hallucination.md`

## Related skills

`ship-to-test`, Cromwell skills under `ai/skills/`, `lightweight-bug-fix` for regressions.
