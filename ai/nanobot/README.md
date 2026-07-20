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
| `patches/cron_tool_allowlist.py` | Cron duty guards: MCP allowlist/require, builtin deny, placeholder-path block, identical-fail circuit-break, path-ask suppress (`session_key=cron:<job-id>`) |
| `patches/test_cron_tool_allowlist.py` | Unit tests (no nanobot install required) |

Allowlist config SOT: `ecosystem/ai/schedule/cron-tool-allowlist.json` (seeded into the bot workspace).

After changing the patch module: rebuild `nanobot_cromwell`. After config/skill/cron message changes: `bin/seed-cromwell-workspace` (and `--force-cron` if job messages changed).

## Runtime data (not this tree)

Bot config, sessions, and memory live under host `ai/data/cromwell-bot/` (gitignored secrets). Personas/skills seed from `ecosystem/ai/` via `bin/seed-cromwell-workspace`.
