# Cromwell nanobot image (Sawtooth)

Slim image: pin `nanobot-ai` from PyPI, plus Sawtooth-only patches (cron MCP tool allowlist, Telegram rich-message latch).

**Git home:** `ecosystem/ai/nanobot` in `winston_ecosystem`.

## Build

```bash
./bin/compose --profile ai build nanobot_cromwell
```

Compose context: `./ecosystem/ai/nanobot`.

## Patches

| File | Purpose |
|------|---------|
| `patches/cron_tool_allowlist.py` | Hard MCP allowlist for `session_key=cron:<job-id>` |
| `patches/test_cron_tool_allowlist.py` | Unit tests (no nanobot install required) |

Allowlist config SOT: `ecosystem/ai/schedule/cron-tool-allowlist.json` (seeded into the bot workspace).

## Runtime data (not this tree)

Bot config, sessions, and memory live under host `ai/data/cromwell-bot/` (gitignored secrets). Personas/skills seed from `ecosystem/ai/` via `bin/seed-cromwell-workspace`.
